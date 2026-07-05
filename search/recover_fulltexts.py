#!/usr/bin/env python3
"""Recovery pass for records fetch_fulltexts.py could not retrieve.

Three strategies, in order:
  1. local  — page-1 title-token overlap against PDFs already in references/
              that are not yet claimed by a bib key (the Additional-sources
              pool); >= 0.75 overlap adopts a copy into the dest dir.
  2. openalex — batch works lookup by openalex_id; try every
              locations[].pdf_url not already attempted.
  3. s2     — title search (for records lacking DOIs); try openAccessPdf.

Usage: recover_fulltexts.py <targets.csv> <dest_dir> <fetch_log.csv> [...more logs]
Appends outcomes to <dest_dir>/../recover_log.csv
"""

import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pypdf

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
MAILTO = "hello@swiftride.net"
UA = f"cloud-db-metasurvey-recover (mailto:{MAILTO})"
STOP = set("a an the of on in for and or to with using from at by is are".split())


def tokens(text):
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOP]


def overlap(pdf_path, title):
    try:
        r = pypdf.PdfReader(str(pdf_path))
        txt = " ".join((p.extract_text() or "") for p in r.pages[:2])
        tt = tokens(title)
        return sum(1 for t in tt if t in set(tokens(txt))) / max(1, len(tt))
    except Exception:
        return 0.0


def fetch(url, timeout=90):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def main():
    targets_path, dest = Path(sys.argv[1]), Path(sys.argv[2])
    logs = sys.argv[3:]
    dest.mkdir(exist_ok=True)
    missed = set()
    for lg in logs:
        for r in csv.DictReader(open(lg)):
            if r["outcome"] == "not-retrieved":
                missed.add(r["record_id"])
    targets = [r for r in csv.DictReader(open(targets_path)) if r["record_id"] in missed
               and not (dest / f"{r['record_id']}.pdf").exists()]
    print(f"{len(targets)} records to recover")

    # local pool: files listed in download_report.md's Additional-sources table
    # with their KNOWN titles (title-to-title matching only — content-token
    # containment produced false positives and must not be used).
    import difflib
    pool_titles = []
    for ln in (REPO / "references" / "download_report.md").read_text().split("\n"):
        m = re.match(r"\| \[([^\]]+)\]\([^)]+\) \| (.+?) \|", ln)
        if m and (REPO / "references" / m.group(1)).exists():
            pool_titles.append((REPO / "references" / m.group(1), m.group(2)))
    print(f"local pool: {len(pool_titles)} report-listed PDFs")

    out = open(dest.parent / "recover_log.csv", "a", newline="")
    w = csv.writer(out)
    recovered = 0

    # collect openalex ids for batch lookup
    cand_meta = {c["record_id"]: c for c in json.loads((HERE / "candidates.json").read_text())}

    for rec in targets:
        rid, title = rec["record_id"], rec["title"]
        got = False
        # 1. local: strict title-to-title match against report-listed files
        tn = re.sub(r"[^a-z0-9]+", "", title.lower())
        best, bestp = 0.0, None
        for p, ptitle in pool_titles:
            r = difflib.SequenceMatcher(None, tn, re.sub(r"[^a-z0-9]+", "", ptitle.lower())).ratio()
            if r > best:
                best, bestp = r, p
        if best >= 0.92:
            (dest / f"{rid}.pdf").write_bytes(bestp.read_bytes())
            w.writerow([rid, "recovered-local", str(bestp.name), f"{best:.2f}"])
            recovered += 1
            continue
        # 2. openalex locations
        oid = (cand_meta.get(rid) or {}).get("openalex_id")
        urls = []
        if oid:
            try:
                data = json.loads(fetch(f"https://api.openalex.org/works/{oid}?select=locations&mailto={MAILTO}", 60))
                for loc in data.get("locations") or []:
                    u = loc.get("pdf_url")
                    if u:
                        urls.append(u)
            except Exception:
                pass
            time.sleep(0.2)
        # 3. s2 title search when no doi
        if not rec.get("doi"):
            try:
                q = urllib.parse.quote(title[:120])
                data = json.loads(fetch(
                    f"https://api.semanticscholar.org/graph/v1/paper/search?query={q}&fields=title,openAccessPdf&limit=3", 60))
                for it in data.get("data") or []:
                    u = (it.get("openAccessPdf") or {}).get("url")
                    if u:
                        urls.append(u)
            except Exception:
                pass
            time.sleep(1.2)
        for u in urls:
            try:
                data = fetch(u)
            except Exception:
                continue
            if not data.startswith(b"%PDF-"):
                continue
            tmp = dest / f"{rid}.pdf"
            tmp.write_bytes(data)
            ov = overlap(tmp, title)
            if ov >= 0.60:
                w.writerow([rid, "recovered-web", u[:120], f"{ov:.2f}"])
                recovered += 1
                got = True
                break
            tmp.unlink()
        if not got and best < 0.75:
            w.writerow([rid, "still-missing", "", ""])
        time.sleep(0.3)
    out.close()
    print(f"recovered {recovered}/{len(targets)}")


if __name__ == "__main__":
    main()
