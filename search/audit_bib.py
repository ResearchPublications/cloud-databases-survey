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
            if not fm:
                continue
            val = fm.group(1)
            if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]|�|&#x", val):
                check(key, "E1", f"encoding junk in {f}: {val[:60]!r}")
            if re.search(r"&amp;|&lt;|&gt;|&#\d+;", val):
                check(key, "E2", f"HTML entity in {f}: {val[:60]!r}")
            if f == "title":
                for w in re.findall(r"[A-Za-z]{2,}-[a-z]{2,}", val):
                    left = w.split("-")[0].lower()
                    # heuristic: mid-word hyphenation artifact if the left part
                    # is not a word that legitimately precedes a hyphen
                    if left in ("op", "sys", "data-bases".split("-")[0], "manage",
                                 "environ", "tech", "eval", "im", "pro", "compu",
                                 "opti", "distri", "applica", "informa"):
                        check(key, "E3", f"hyphenation artifact in title: {w!r}")
                if re.search(r",\S", re.sub(r"\{|\}", "", val)):
                    check(key, "E4", f"missing space after comma in title: {val[:60]!r}")
        if am:
            if re.search(r"\b[A-Z]{4,}\b", am.group(1)) and "{" not in am.group(1):
                check(key, "A4", f"ALL-CAPS author token: {am.group(1)[:60]!r}")
            parts2 = [p.strip() for p in re.split(r"\s+and\s+", re.sub(r"\s+", " ", am.group(1)))]
            comma_fmt = [p for p in parts2 if re.match(r"^[A-Z][\w'\\{}~^\"-]+,\s", p)]
            if comma_fmt and len(comma_fmt) < len(parts2):
                check(key, "A5", f"mixed author name format: {comma_fmt[0][:40]!r}")
        if re.search(r"howpublished\s*=\s*\{arXiv:\}", body):
            check(key, "X1", "empty arXiv identifier")

    # cross-bib duplicate detection: DOI, arXiv id, normalized title
    import difflib
    seen_doi, seen_eprint, titles = {}, {}, []
    for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", text, re.S):
        key, body = m.group(1).strip(), m.group(2)
        dm = re.search(r"doi\s*=\s*\{([^}]+)\}", body)
        if dm:
            d = dm.group(1).lower()
            if d in seen_doi:
                check(key, "DUP", f"same DOI as {seen_doi[d]}: {d}")
            seen_doi[d] = key
        em = re.search(r"(?:eprint\s*=\s*\{|howpublished\s*=\s*\{arXiv:|note\s*=\s*\{arXiv:)([\d.]+)", body)
        if em and em.group(1):
            e = em.group(1)
            if e in seen_eprint:
                check(key, "DUP", f"same arXiv id as {seen_eprint[e]}: {e}")
            seen_eprint[e] = key
        tm = re.search(r"title\s*=\s*\{(.+)\}", body)
        if tm:
            nt = re.sub(r"[^a-z0-9]+", "", tm.group(1).lower())
            for k2, nt2 in titles:
                if abs(len(nt) - len(nt2)) < max(len(nt), len(nt2)) * 0.15 and \
                        difflib.SequenceMatcher(None, nt, nt2).ratio() >= 0.95:
                    check(key, "DUP", f"near-identical title to {k2}")
            titles.append((key, nt))

    if defects:
        print(f"{len(defects)} DEFECTS:")
        for key, code, msg in defects:
            print(f"  [{code}] {key}: {msg}")
        sys.exit(1)
    print("bibliography audit: no defects")


if __name__ == "__main__":
    main()
