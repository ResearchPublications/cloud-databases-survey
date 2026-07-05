#!/usr/bin/env python3
"""Line-by-line bibliography defect audit.

Scans every entry in cloud-db-metasurvey.bib for:
  A1  author field starting or ending with 'and' (dangling connector)
  A2  empty author segments ('and and', leading/trailing whitespace joins)
  A3  author field empty or 'Unknown'
  D1  DOI not matching ^10.\\d{4,9}/\\S+$
  D2  DOI ending in /pdf, /full, /abstract (URL-path contamination)
  T1  @misc entries labeled arXiv that carry a non-arXiv (e.g. IEEE/ACM) DOI
  E1  title/journal/booktitle containing mojibake or control characters

Exit code 1 if any defect found. Run after any bib regeneration.
"""

import re
import sys
from pathlib import Path

BIB = Path(__file__).resolve().parent.parent / "cloud-db-metasurvey.bib"

defects = []


def check(key, code, msg):
    defects.append((key, code, msg))


def main():
    text = BIB.read_text()
    for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", text, re.S):
        etype, key, body = m.group(1), m.group(2).strip(), m.group(3)

        am = re.search(r"author\s*=\s*\{(.+?)\},?\n", body, re.S)
        if am:
            authors = re.sub(r"\s+", " ", am.group(1)).strip()
            if re.match(r"(?i)^and\b", authors) or re.search(r"(?i)\band$", authors):
                check(key, "A1", f"dangling 'and' in author field: {authors[:80]!r}")
            parts = [p.strip() for p in re.split(r"\s+and\s+", authors)]
            if any(not p for p in parts):
                check(key, "A2", f"empty author segment: {authors[:80]!r}")
            if authors.lower() in ("", "unknown"):
                check(key, "A3", "author field empty/Unknown")

        dm = re.search(r"doi\s*=\s*\{([^}]+)\}", body)
        if dm:
            doi = dm.group(1).strip()
            if not re.match(r"^10\.\d{4,9}/\S+$", doi):
                check(key, "D1", f"malformed DOI: {doi!r}")
            if re.search(r"/(pdf|full|abstract)$", doi, re.I):
                check(key, "D2", f"URL-path contaminated DOI: {doi!r}")

        if etype.lower() == "misc" and re.search(r"arXiv", body):
            if dm and not dm.group(1).lower().startswith("10.48550/"):
                check(key, "T1", f"arXiv-typed entry with non-arXiv DOI: {dm.group(1)!r}")

        for f in ("title", "journal", "booktitle"):
            fm = re.search(f + r"\s*=\s*\{(.+?)\},?\n", body)
            if fm and re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]|�|&#x", fm.group(1)):
                check(key, "E1", f"encoding junk in {f}: {fm.group(1)[:60]!r}")

    if defects:
        print(f"{len(defects)} DEFECTS:")
        for key, code, msg in defects:
            print(f"  [{code}] {key}: {msg}")
        sys.exit(1)
    print("bibliography audit: no defects")


if __name__ == "__main__":
    main()
