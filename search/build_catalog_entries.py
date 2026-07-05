#!/usr/bin/env python3
"""Build verified bib entries + catalog rows for the frozen new includes.

For each record id in final_new_ids.json:
  - resolve metadata: Crossref (DOI) > arXiv API (arxiv_id) > OpenAlex (id)
  - dedupe against EVERY existing bib key (DOI match, then normalized title
    ratio >= 0.92): if matched, reuse the existing key, add no bib entry
  - generate bibkey Surname+Year+Tag (unique), emit bib entry text
  - copy search/fulltext/<rid>.pdf -> references/<bibkey>.pdf
Outputs:
  search/new_entries_meta.json   {rid: {bibkey, title, authors, venue, year,
                                        doi, arxiv, pages_pp, existing}}
  search/new_bib_entries.bib     entries to append (excluding existing)
"""

import csv
import difflib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
MAILTO = "hello@swiftride.net"
UA = f"cloud-db-metasurvey-bib (mailto:{MAILTO})"
SCRATCH = Path(sys.argv[1])  # scratchpad dir containing final_new_ids.json + qa_merged.json


def http_json(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception:
            time.sleep(3 * (i + 1))
    return None


def norm_t(t):
    return re.sub(r"[^a-z0-9]+", "", (t or "").lower())


def tex_escape(s):
    return s.replace("&", "\\&").replace("%", "\\%").replace("_", "\\_").replace("#", "\\#")


def main():
    new_ids = json.load(open(SCRATCH / "final_new_ids.json"))
    qa = json.load(open(SCRATCH / "qa_merged.json"))
    cands = {c["record_id"]: c for c in json.load(open(HERE / "candidates.json"))}
    manual_meta = {
        "CAND-M-001": {"title": "An Overview on Cloud Distributed Databases for Business Environments",
                        "year": 2023, "arxiv_id": "2301.10673", "doi": ""},
        "CAND-M-004": {"title": "A Survey of Comparing Different Cloud Database Performance: SQL and NoSQL",
                        "year": 2022, "arxiv_id": "", "doi": "10.24271/psr.2022.301247.1104"},
        "CAND-M-005": {"title": "A Systematic Review of Cloud Computing, Big Data and Databases on the Cloud",
                        "year": 2014, "arxiv_id": "", "doi": ""},
    }

    bib = (REPO / "cloud-db-metasurvey.bib").read_text()
    existing = {}  # key -> (doi, normtitle)
    for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", bib, re.S):
        key, body = m.group(1).strip(), m.group(2)
        dm = re.search(r"doi\s*=\s*\{([^}]+)\}", body)
        tm = re.search(r"title\s*=\s*\{(.+)\}", body)
        existing[key] = ((dm.group(1).lower() if dm else ""),
                         norm_t(re.sub(r"[{}]", "", tm.group(1)) if tm else ""))
    used_keys = set(existing)

    out_meta, bib_texts = {}, []
    for rid in new_ids:
        v = qa[rid]
        c = cands.get(rid, {})
        doi = (c.get("doi") or manual_meta.get(rid, {}).get("doi") or "").lower()
        arxiv = c.get("arxiv_id") or manual_meta.get(rid, {}).get("arxiv_id") or ""
        title_rec = c.get("title") or manual_meta.get(rid, {}).get("title") or v[17]
        year = c.get("year") or manual_meta.get(rid, {}).get("year")

        # dedupe vs existing bib
        match_key = None
        for k, (kdoi, ktitle) in existing.items():
            if doi and kdoi and doi == kdoi:
                match_key = k; break
            if ktitle and difflib.SequenceMatcher(None, norm_t(title_rec), ktitle).ratio() >= 0.92:
                match_key = k; break

        meta = {"authors": [], "title": title_rec, "venue": v[13], "year": year,
                "doi": doi, "arxiv": arxiv, "pages_pp": "", "volume": "", "number": ""}
        src = None
        if doi:
            data = http_json(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}")
            if data:
                m = data["message"]
                meta["authors"] = [f"{a.get('given','')} {a.get('family','')}".strip()
                                    for a in m.get("author", [])]
                if m.get("title"): meta["title"] = m["title"][0]
                if m.get("container-title"): meta["venue"] = m["container-title"][0]
                dp = m.get("published", {}).get("date-parts", [[None]])
                if dp[0][0]: meta["year"] = dp[0][0]
                meta["pages_pp"] = m.get("page") or ""
                meta["volume"] = m.get("volume") or ""
                meta["number"] = m.get("issue") or ""
                src = "crossref"
            time.sleep(1.0)
        if not src and arxiv:
            try:
                req = urllib.request.Request(
                    f"https://export.arxiv.org/api/query?id_list={arxiv}&max_results=1",
                    headers={"User-Agent": UA})
                root = ET.fromstring(urllib.request.urlopen(req, timeout=60).read())
                A = "{http://www.w3.org/2005/Atom}"
                e = root.find(A + "entry")
                if e is not None:
                    meta["authors"] = [a.find(A + "name").text for a in e.findall(A + "author")]
                    meta["title"] = re.sub(r"\s+", " ", e.find(A + "title").text).strip()
                    meta["venue"] = "arXiv"
                    src = "arxiv"
                time.sleep(3.0)
            except Exception:
                pass
        if not src and c.get("openalex_id"):
            data = http_json(f"https://api.openalex.org/works/{c['openalex_id']}?select=authorships,title,publication_year&mailto={MAILTO}")
            if data:
                meta["authors"] = [a["author"]["display_name"] for a in data.get("authorships", [])]
                if data.get("title"): meta["title"] = data["title"]
                src = "openalex"
            time.sleep(0.2)

        if match_key:
            out_meta[rid] = {"bibkey": match_key, "existing": True, **meta, "source": src}
            print(f"{rid}: matches existing bib key {match_key}")
            continue

        surname = (v[15] or (meta["authors"][0].split()[-1] if meta["authors"] else "Anon"))
        surname = re.sub(r"[^A-Za-z]", "", surname.split()[-1]) or "Anon"
        # tag from topic
        tag_map = {"NoSQL/NewSQL": "NoSQL", "Graph Databases": "GraphDB", "Distributed DBs": "DistDB",
                   "AI4DB/Learned Opt.": "AI4DB", "Security/Privacy": "Sec", "DBaaS": "DBaaS",
                   "Vector Databases": "VectorDB", "Benchmarking": "Bench", "Multi-Model DBs": "MultiModel",
                   "HTAP Systems": "HTAP", "Cloud-Native Arch.": "CloudNative", "NL/LLM-Database": "NLIDB",
                   "Data Lakehouse": "Lakehouse", "Edge/Fog DBs": "EdgeFog", "Cloud DB Migration": "Migration",
                   "Time-Series DBs": "TSDB", "In-Memory DBs": "InMemory"}
        tag = tag_map.get(v[11], "Survey")
        base = f"{surname}{meta['year']}{tag}"
        key, n = base, 2
        while key in used_keys:
            key = f"{base}{n}"; n += 1
        used_keys.add(key)

        authors_bib = " and ".join(meta["authors"]) if meta["authors"] else "Unknown"
        is_conf = v[14] == "conference"
        etype = "inproceedings" if is_conf else ("misc" if v[14] == "arxiv" else "article")
        lines = [f"@{etype}{{{key},", f"  author    = {{{authors_bib}}},",
                 f"  title     = {{{tex_escape(meta['title'])}}},"]
        if etype == "article":
            lines.append(f"  journal   = {{{tex_escape(meta['venue'])}}},")
        elif etype == "inproceedings":
            lines.append(f"  booktitle = {{{tex_escape(meta['venue'])}}},")
        else:
            lines.append(f"  howpublished = {{arXiv:{arxiv}}},")
        if meta["volume"]: lines.append(f"  volume    = {{{meta['volume']}}},")
        if meta["number"]: lines.append(f"  number    = {{{meta['number']}}},")
        if meta["pages_pp"]: lines.append(f"  pages     = {{{meta['pages_pp'].replace('-', '--')}}},")
        lines.append(f"  year      = {{{meta['year']}}},")
        if doi: lines.append(f"  doi       = {{{doi}}},")
        elif arxiv and etype != "misc": lines.append(f"  note      = {{arXiv:{arxiv}}},")
        lines.append("}")
        bib_texts.append("\n".join(lines))
        out_meta[rid] = {"bibkey": key, "existing": False, **meta, "source": src}
        # place PDF
        srcpdf = HERE / "fulltext" / f"{rid}.pdf"
        dst = REPO / "references" / f"{key}.pdf"
        if srcpdf.exists() and not dst.exists():
            dst.write_bytes(srcpdf.read_bytes())
        print(f"{rid}: {key} [{src}] {meta['title'][:60]}")

    json.dump(out_meta, open(HERE / "new_entries_meta.json", "w"), indent=1)
    (HERE / "new_bib_entries.bib").write_text("\n\n".join(bib_texts) + "\n")
    print(f"\n{len(bib_texts)} new bib entries; {sum(1 for m in out_meta.values() if m['existing'])} matched existing keys")


if __name__ == "__main__":
    main()
