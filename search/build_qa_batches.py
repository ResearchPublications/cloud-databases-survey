#!/usr/bin/env python3
"""Build QA batch assignment files for full-text assessment agents.

For every PDF in search/fulltext/, precompute page count and a rough
reference count (regex over the last third of the text), pair with the
candidate metadata, and emit batch files of N records each.

Usage: build_qa_batches.py <out_dir> [batch_size]
"""

import csv
import json
import re
import sys
from pathlib import Path

import pypdf

HERE = Path(__file__).resolve().parent


def ref_count_estimate(reader):
    n = len(reader.pages)
    text = ""
    for p in reader.pages[max(0, n - max(3, n // 3)):]:
        try:
            text += "\n" + (p.extract_text() or "")
        except Exception:
            pass
    nums = re.findall(r"^\s*\[(\d{1,3})\]", text, re.M)
    if nums:
        return max(int(x) for x in nums)
    nums = re.findall(r"^\s*(\d{1,3})\.\s+[A-Z]", text, re.M)
    return max((int(x) for x in nums), default=0)


def main():
    out_dir = Path(sys.argv[1])
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    out_dir.mkdir(parents=True, exist_ok=True)
    cands = {c["record_id"]: c for c in json.loads((HERE / "candidates.json").read_text())}
    # manual-arm records get metadata stubs
    pdfs = sorted((HERE / "fulltext").glob("*.pdf"))
    entries = []
    for pdf in pdfs:
        rid = pdf.stem
        meta = cands.get(rid, {})
        try:
            r = pypdf.PdfReader(str(pdf))
            pages = len(r.pages)
            refs = ref_count_estimate(r)
        except Exception as exc:
            pages, refs = 0, 0
        entries.append({
            "record_id": rid,
            "pdf": str(pdf.resolve()),
            "pages": pages,
            "ref_estimate": refs,
            "title": meta.get("title", ""),
            "year": meta.get("year", ""),
            "venue": meta.get("venue", ""),
            "cites": meta.get("cited_by_count", ""),
            "doi": meta.get("doi", ""),
        })
    nb = 0
    for i in range(0, len(entries), batch_size):
        nb += 1
        with open(out_dir / f"qa_batch_{nb:02d}.txt", "w") as fh:
            for e in entries[i:i + batch_size]:
                fh.write(
                    f"RECORD: {e['record_id']}\nPDF: {e['pdf']}\n"
                    f"PAGES: {e['pages']}  REF_ESTIMATE: {e['ref_estimate']}  CITES: {e['cites']}\n"
                    f"EXPECTED_TITLE: {e['title']}\nYEAR: {e['year']}  VENUE: {e['venue']}  DOI: {e['doi']}\n---\n")
    print(f"{len(entries)} PDFs -> {nb} batches in {out_dir}")


if __name__ == "__main__":
    main()
