#!/usr/bin/env python3
"""Full-text retrieval for title/abstract-screening survivors.

Input CSV (default search/fulltext_targets.csv) columns:
  record_id,bibkey,title,year,doi,arxiv_id,oa_pdf_url

Waterfall per record: explicit oa_pdf_url -> arXiv -> Unpaywall ->
Semantic Scholar openAccessPdf -> Crossref fulltext links.

Every fetched file must (a) start with %PDF- and (b) have page-1 text
whose token overlap with the record title is >= OVERLAP_MIN. Failures
are quarantined under search/quarantine/, never written to references/.
Unretrievable records are listed in search/manual_retrieval_todo.md
(EC5 exclusions if still missing at freeze time).

Results log: search/fetch_log.csv (record_id, bibkey, outcome, source, note)
"""

import csv
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import pypdf
except ImportError:  # pragma: no cover
    sys.exit("pypdf required: pip install pypdf")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
REFS = REPO / "references"
QUAR = HERE / "quarantine"
MAILTO = "hello@swiftride.net"
UA = f"cloud-db-metasurvey-fetch (mailto:{MAILTO})"
OVERLAP_MIN = 0.60

STOP = set("a an the of on in for and or to with using from at by is are".split())


def tokens(text):
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOP]


def fetch(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def title_overlap(pdf_path, title):
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        page_text = ""
        for page in reader.pages[:2]:
            page_text += " " + (page.extract_text() or "")
        ttoks = tokens(title)
        if not ttoks:
            return 0.0
        ptoks = set(tokens(page_text))
        return sum(1 for t in ttoks if t in ptoks) / len(ttoks)
    except Exception:
        return 0.0


def candidate_urls(rec):
    urls = []
    if rec.get("oa_pdf_url"):
        urls.append(("oa_pdf_url", rec["oa_pdf_url"]))
    if rec.get("arxiv_id"):
        urls.append(("arxiv", f"https://arxiv.org/pdf/{rec['arxiv_id']}"))
        urls.append(("arxiv-export", f"https://export.arxiv.org/pdf/{rec['arxiv_id']}"))
    doi = rec.get("doi")
    if doi:
        # Unpaywall
        try:
            import json
            data = json.loads(fetch(
                f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={MAILTO}",
                timeout=60).decode())
            locs = []
            if data.get("best_oa_location"):
                locs.append(data["best_oa_location"])
            locs += data.get("oa_locations") or []
            for loc in locs:
                u = loc.get("url_for_pdf") or loc.get("url")
                if u:
                    urls.append(("unpaywall", u))
            time.sleep(0.6)
        except Exception:
            pass
        # Semantic Scholar
        try:
            import json
            data = json.loads(fetch(
                f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(doi)}"
                "?fields=openAccessPdf", timeout=60).decode())
            u = ((data.get("openAccessPdf") or {}).get("url")) or ""
            if u:
                urls.append(("s2", u))
            time.sleep(1.2)
        except Exception:
            pass
    seen, out = set(), []
    for src, u in urls:
        if u not in seen:
            seen.add(u)
            out.append((src, u))
    return out


def main():
    global REFS
    targets_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "fulltext_targets.csv"
    if len(sys.argv) > 2:
        REFS = Path(sys.argv[2])
        REFS.mkdir(parents=True, exist_ok=True)
    QUAR.mkdir(exist_ok=True)
    rows = list(csv.DictReader(open(targets_path)))
    log_rows, todo = [], []

    for rec in rows:
        bibkey = rec["bibkey"]
        dest = REFS / f"{bibkey}.pdf"
        if dest.exists() and title_overlap(dest, rec["title"]) >= OVERLAP_MIN:
            log_rows.append((rec["record_id"], bibkey, "already-present", "", ""))
            print(f"  = {bibkey}: already on disk, verified")
            continue
        outcome = None
        for src, url in candidate_urls(rec):
            try:
                data = fetch(url)
            except Exception as exc:
                print(f"    {bibkey}: {src} fetch failed ({exc!r:.60})")
                continue
            if not data.startswith(b"%PDF-"):
                print(f"    {bibkey}: {src} returned non-PDF")
                continue
            tmp = QUAR / f"{bibkey}.pdf"
            tmp.write_bytes(data)
            ov = title_overlap(tmp, rec["title"])
            if ov >= OVERLAP_MIN:
                tmp.rename(dest)
                outcome = ("fetched", src, f"overlap={ov:.2f}")
                print(f"  + {bibkey}: fetched via {src} (overlap {ov:.2f})")
                break
            print(f"    {bibkey}: {src} content mismatch (overlap {ov:.2f}) -> quarantined")
            outcome = ("quarantined", src, f"overlap={ov:.2f}")
            time.sleep(0.5)
        if outcome and outcome[0] == "fetched":
            log_rows.append((rec["record_id"], bibkey, *outcome))
        else:
            log_rows.append((rec["record_id"], bibkey,
                             outcome[0] if outcome else "not-retrieved",
                             outcome[1] if outcome else "",
                             outcome[2] if outcome else "no OA source"))
            todo.append(rec)
        time.sleep(0.5)

    with open(HERE / "fetch_log.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["record_id", "bibkey", "outcome", "source", "note"])
        w.writerows(log_rows)

    if todo:
        lines = ["# Manual retrieval TODO",
                 "",
                 "Surveys passing title/abstract screening for which no open-access",
                 "PDF could be fetched. Retrieve via institutional access / browser and",
                 "save as `references/<bibkey>.pdf`. Anything still missing at catalog",
                 "freeze is excluded under EC5 and counted in PRISMA as 'reports not",
                 "retrieved'.", ""]
        for rec in todo:
            link = f"https://doi.org/{rec['doi']}" if rec.get("doi") else rec.get("oa_pdf_url", "")
            lines.append(f"- [ ] `{rec['bibkey']}` — {rec['title']} ({rec['year']}). {link}")
        (HERE / "manual_retrieval_todo.md").write_text("\n".join(lines) + "\n")

    fetched = sum(1 for r in log_rows if r[2] in ("fetched", "already-present"))
    print(f"\n{fetched}/{len(rows)} retrieved; {len(todo)} need manual retrieval")


if __name__ == "__main__":
    main()
