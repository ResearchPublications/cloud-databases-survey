#!/usr/bin/env python3
"""Systematic discovery search for the cloud-databases meta-survey.

Queries OpenAlex (primary), the arXiv API (primary), and optionally
Crossref / Semantic Scholar (supplementary) for survey-type papers on
cloud database topics published 1999--2026, using the canonical search
terms from main.tex Section 4.1 (frozen in queries.json).

Outputs (all under search/):
  candidates.csv / candidates.json  -- deduplicated candidate pool
  search_log.json                   -- per-query URLs + counts + UTC date
                                       (the PRISMA identification record)

Stdlib-only, mirroring download_references.py. Usage:
  python3 search/search_surveys.py [--with-crossref] [--with-s2]
"""

import argparse
import csv
import difflib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAILTO = "hello@swiftride.net"
UA = f"cloud-db-metasurvey-search (mailto:{MAILTO})"

QUERIES = json.loads((HERE / "queries.json").read_text())

OPENALEX_SLEEP = 0.15
ARXIV_SLEEP = 3.0
CROSSREF_SLEEP = 1.0
S2_SLEEP = 1.2


def http_json(url, retries=4, backoff=5.0):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as resp:
                return json.load(resp)
        except Exception as exc:  # noqa: BLE001 - log and retry
            if attempt == retries - 1:
                print(f"    ! giving up on {url[:120]}: {exc!r}", file=sys.stderr)
                return None
            time.sleep(backoff * (attempt + 1))
    return None


def http_text(url, retries=4, backoff=5.0):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as resp:
                return resp.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001
            if attempt == retries - 1:
                print(f"    ! giving up on {url[:120]}: {exc!r}", file=sys.stderr)
                return None
            time.sleep(backoff * (attempt + 1))
    return None


def norm_doi(doi):
    if not doi:
        return ""
    doi = doi.strip().lower()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
    doi = re.sub(r"/(pdf|full|abstract)$", "", doi)
    if not re.match(r"^10\.\d{4,9}/\S+$", doi):
        return ""
    return doi


def norm_arxiv(aid):
    if not aid:
        return ""
    aid = aid.strip().lower()
    aid = re.sub(r"^(https?://)?(export\.)?arxiv\.org/(abs|pdf)/", "", aid)
    aid = re.sub(r"^arxiv:", "", aid)
    aid = re.sub(r"v\d+$", "", aid)
    aid = re.sub(r"\.pdf$", "", aid)
    return aid


def norm_title(title):
    return re.sub(r"[^a-z0-9]+", "", (title or "").lower())


def invert_abstract(inv):
    """Reconstruct plain text from an OpenAlex abstract_inverted_index."""
    if not inv:
        return ""
    positions = []
    for word, idxs in inv.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort()
    return " ".join(w for _, w in positions)


# ---------------------------------------------------------------- OpenAlex

def openalex_queries(log):
    cfg = QUERIES["openalex"]
    indicators = QUERIES["survey_indicators"]
    ind_block = " OR ".join(
        f'"{t}"' if " " in t else t for t in indicators
    )
    records = []
    for term in QUERIES["cloud_db_terms"]:
        q = f'"{term}" ({ind_block})'
        filt = ",".join([
            f"title_and_abstract.search:{q}",
            f"from_publication_date:{QUERIES['window']['from']}",
            f"to_publication_date:{QUERIES['window']['to']}",
            f"type:{cfg['type_filter']}",
            f"language:{cfg['language']}",
        ])
        base = (
            "https://api.openalex.org/works?filter=" + urllib.parse.quote(filt, safe=",:|")
            + "&select=id,doi,title,display_name,publication_year,type,language,"
            + "primary_location,open_access,cited_by_count,abstract_inverted_index,ids"
            + f"&per-page={cfg['per_page']}&mailto={MAILTO}"
        )
        cursor = "*"
        got, total, pages = 0, None, 0
        while cursor and pages < cfg["max_pages_per_query"]:
            data = http_json(base + "&cursor=" + urllib.parse.quote(cursor))
            if data is None:
                break
            if total is None:
                total = data["meta"]["count"]
            for w in data.get("results", []):
                loc = (w.get("primary_location") or {}).get("source") or {}
                oa = w.get("open_access") or {}
                records.append({
                    "title": w.get("title") or w.get("display_name") or "",
                    "year": w.get("publication_year"),
                    "venue": loc.get("display_name") or "",
                    "doi": norm_doi(w.get("doi")),
                    "arxiv_id": norm_arxiv((w.get("ids") or {}).get("arxiv") or ""),
                    "openalex_id": (w.get("id") or "").rsplit("/", 1)[-1],
                    "type": w.get("type") or "",
                    "cited_by_count": w.get("cited_by_count") or 0,
                    "oa_pdf_url": oa.get("oa_url") or "",
                    "abstract": invert_abstract(w.get("abstract_inverted_index")),
                    "source_apis": ["openalex"],
                    "query_ids": [f"openalex:{term}"],
                })
            got += len(data.get("results", []))
            cursor = data["meta"].get("next_cursor")
            pages += 1
            time.sleep(OPENALEX_SLEEP)
        truncated = bool(cursor) and got < (total or 0)
        log["queries"].append({
            "api": "openalex", "term": term, "url": base,
            "hits_reported": total, "hits_fetched": got,
            "truncated_at_page_cap": truncated,
        })
        flag = "  [TRUNCATED]" if truncated else ""
        print(f"  openalex '{term}': {got}/{total}{flag}")
    return records


# ------------------------------------------------------------------ arXiv

ATOM = "{http://www.w3.org/2005/Atom}"
OS = "{http://a9.com/-/spec/opensearch/1.1/}"


def arxiv_query(log):
    cfg = QUERIES["arxiv"]
    ind = " OR ".join(
        f'ti:"{t}"' if " " in t else f"ti:{t}" for t in cfg["title_indicators"]
    )
    sq = f"cat:{cfg['category']} AND ({ind})"
    base = (
        "https://export.arxiv.org/api/query?search_query="
        + urllib.parse.quote(sq)
        + f"&max_results={cfg['page_size']}&sortBy=submittedDate&sortOrder=descending"
    )
    records, start, total = [], 0, None
    while True:
        text = http_text(base + f"&start={start}")
        if text is None:
            break
        root = ET.fromstring(text)
        if total is None:
            total = int(root.find(OS + "totalResults").text)
        entries = root.findall(ATOM + "entry")
        if not entries:
            break
        for e in entries:
            aid_raw = e.find(ATOM + "id").text
            year = None
            pub = e.find(ATOM + "published")
            if pub is not None and pub.text:
                year = int(pub.text[:4])
            doi_el = e.find("{http://arxiv.org/schemas/atom}doi")
            records.append({
                "title": re.sub(r"\s+", " ", e.find(ATOM + "title").text or "").strip(),
                "year": year,
                "venue": "arXiv (cs.DB)",
                "doi": norm_doi(doi_el.text if doi_el is not None else ""),
                "arxiv_id": norm_arxiv(aid_raw),
                "openalex_id": "",
                "type": "preprint",
                "cited_by_count": 0,
                "oa_pdf_url": f"https://arxiv.org/pdf/{norm_arxiv(aid_raw)}",
                "abstract": re.sub(r"\s+", " ", e.find(ATOM + "summary").text or "").strip(),
                "source_apis": ["arxiv"],
                "query_ids": ["arxiv:cs.DB-title-indicators"],
            })
        start += len(entries)
        if start >= total:
            break
        time.sleep(ARXIV_SLEEP)
    log["queries"].append({
        "api": "arxiv", "term": "cs.DB x title indicators", "url": base,
        "hits_reported": total, "hits_fetched": len(records),
        "truncated_at_page_cap": False,
    })
    print(f"  arxiv cs.DB: {len(records)}/{total}")
    return records


# --------------------------------------------------------------- Crossref

def crossref_queries(log):
    records = []
    for term in QUERIES["crossref_terms"]:
        base = (
            "https://api.crossref.org/works?query.bibliographic="
            + urllib.parse.quote(term)
            + "&filter=" + urllib.parse.quote(
                f"from-pub-date:{QUERIES['window']['from']},type:journal-article", safe=",:-")
            + "&rows=100&select=DOI,title,container-title,published,type,is-referenced-by-count,abstract"
            + f"&mailto={MAILTO}"
        )
        data = http_json(base)
        got = 0
        if data:
            for it in data["message"].get("items", []):
                title = (it.get("title") or [""])[0]
                if not title:
                    continue
                dp = (it.get("published") or {}).get("date-parts", [[None]])
                records.append({
                    "title": title,
                    "year": dp[0][0],
                    "venue": (it.get("container-title") or [""])[0],
                    "doi": norm_doi(it.get("DOI")),
                    "arxiv_id": "",
                    "openalex_id": "",
                    "type": it.get("type") or "",
                    "cited_by_count": it.get("is-referenced-by-count") or 0,
                    "oa_pdf_url": "",
                    "abstract": re.sub(r"<[^>]+>", " ", it.get("abstract") or "").strip(),
                    "source_apis": ["crossref"],
                    "query_ids": [f"crossref:{term}"],
                })
                got += 1
        log["queries"].append({
            "api": "crossref", "term": term, "url": base,
            "hits_reported": data["message"]["total-results"] if data else None,
            "hits_fetched": got,
            "truncated_at_page_cap": bool(data and data["message"]["total-results"] > 100),
        })
        print(f"  crossref '{term}': fetched {got} (relevance-ranked top 100)")
        time.sleep(CROSSREF_SLEEP)
    return records


# ------------------------------------------------------- Semantic Scholar

def s2_queries(log):
    records = []
    for term in QUERIES["crossref_terms"]:
        base = (
            "https://api.semanticscholar.org/graph/v1/paper/search/bulk?query="
            + urllib.parse.quote(term)
            + "&fields=title,year,venue,externalIds,citationCount,openAccessPdf,abstract"
            + "&year=1999-2026"
        )
        data = http_json(base)
        got = 0
        if data:
            for it in (data.get("data") or []):
                ext = it.get("externalIds") or {}
                records.append({
                    "title": it.get("title") or "",
                    "year": it.get("year"),
                    "venue": it.get("venue") or "",
                    "doi": norm_doi(ext.get("DOI")),
                    "arxiv_id": norm_arxiv(ext.get("ArXiv") or ""),
                    "openalex_id": "",
                    "type": "",
                    "cited_by_count": it.get("citationCount") or 0,
                    "oa_pdf_url": (it.get("openAccessPdf") or {}).get("url") or "",
                    "abstract": it.get("abstract") or "",
                    "source_apis": ["s2"],
                    "query_ids": [f"s2:{term}"],
                })
                got += 1
        log["queries"].append({
            "api": "s2", "term": term, "url": base,
            "hits_reported": data.get("total") if data else None,
            "hits_fetched": got,
            "truncated_at_page_cap": bool(data and (data.get("total") or 0) > got),
        })
        print(f"  s2 '{term}': fetched {got} of {data.get('total') if data else '?'}")
        time.sleep(S2_SLEEP)
    return records


# ------------------------------------------------------------------ dedup

def dedup(records, log):
    by_doi, by_arxiv, by_title = {}, {}, {}
    merged = []

    def merge(target, rec):
        target["source_apis"] = sorted(set(target["source_apis"]) | set(rec["source_apis"]))
        target["query_ids"] = sorted(set(target["query_ids"]) | set(rec["query_ids"]))
        for f in ("doi", "arxiv_id", "openalex_id", "abstract", "venue", "oa_pdf_url"):
            if not target.get(f) and rec.get(f):
                target[f] = rec[f]
        target["cited_by_count"] = max(target["cited_by_count"], rec["cited_by_count"])

    for rec in records:
        key_hits = []
        if rec["doi"] and rec["doi"] in by_doi:
            key_hits.append(by_doi[rec["doi"]])
        if rec["arxiv_id"] and rec["arxiv_id"] in by_arxiv:
            key_hits.append(by_arxiv[rec["arxiv_id"]])
        nt = norm_title(rec["title"])
        if nt and nt in by_title:
            key_hits.append(by_title[nt])
        if key_hits:
            merge(key_hits[0], rec)
            target = key_hits[0]
        else:
            merged.append(rec)
            target = rec
        if target["doi"]:
            by_doi.setdefault(target["doi"], target)
        if target["arxiv_id"]:
            by_arxiv.setdefault(target["arxiv_id"], target)
        if nt:
            by_title.setdefault(nt, target)

    # fuzzy pass: near-identical titles within +/-1 year
    fuzzy_dropped = 0
    keep = []
    seen = []  # (norm_title, year, rec)
    for rec in sorted(merged, key=lambda r: (-(r["cited_by_count"]), r["title"])):
        nt = norm_title(rec["title"])
        dup_of = None
        for snt, sy, srec in seen:
            if rec["year"] and sy and abs(rec["year"] - sy) > 1:
                continue
            if abs(len(snt) - len(nt)) > max(len(snt), len(nt)) * 0.15:
                continue
            if difflib.SequenceMatcher(None, nt, snt).ratio() >= 0.92:
                dup_of = srec
                break
        if dup_of is not None:
            merge(dup_of, rec)
            fuzzy_dropped += 1
        else:
            keep.append(rec)
            seen.append((nt, rec["year"], rec))

    log["dedup"] = {
        "raw_records": len(records),
        "after_key_dedup": len(merged),
        "fuzzy_merged": fuzzy_dropped,
        "final_candidates": len(keep),
    }
    return keep


# ------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-crossref", action="store_true")
    ap.add_argument("--with-s2", action="store_true")
    args = ap.parse_args()

    log = {
        "search_date_utc": datetime.now(timezone.utc).isoformat(),
        "window": QUERIES["window"],
        "queries": [],
    }

    print("OpenAlex sweep (18 term queries)...")
    records = openalex_queries(log)
    print("arXiv sweep (cs.DB x title indicators)...")
    records += arxiv_query(log)
    if args.with_crossref:
        print("Crossref supplementary sweep...")
        records += crossref_queries(log)
    if args.with_s2:
        print("Semantic Scholar supplementary sweep...")
        records += s2_queries(log)

    print("Deduplicating...")
    final = dedup(records, log)
    # deterministic ordering + ids
    final.sort(key=lambda r: (r["year"] or 0, norm_title(r["title"])))
    for i, rec in enumerate(final, 1):
        rec["record_id"] = f"CAND-{i:04d}"

    fields = ["record_id", "title", "year", "venue", "doi", "arxiv_id",
              "openalex_id", "type", "cited_by_count", "oa_pdf_url",
              "abstract", "source_apis", "query_ids"]
    with open(HERE / "candidates.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for rec in final:
            row = dict(rec)
            row["source_apis"] = ";".join(rec["source_apis"])
            row["query_ids"] = ";".join(rec["query_ids"])
            row["abstract"] = (row["abstract"] or "")[:2000]
            w.writerow({k: row.get(k, "") for k in fields})
    (HERE / "candidates.json").write_text(json.dumps(final, indent=1))
    (HERE / "search_log.json").write_text(json.dumps(log, indent=2))

    print(f"\nRaw records: {log['dedup']['raw_records']}")
    print(f"Final candidates: {log['dedup']['final_candidates']}")
    print(f"Wrote {HERE/'candidates.csv'}, candidates.json, search_log.json")


if __name__ == "__main__":
    main()
