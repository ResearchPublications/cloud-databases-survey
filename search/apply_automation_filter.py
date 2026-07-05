#!/usr/bin/env python3
"""Stage-1 automation eligibility marking (PRISMA 2020: 'records marked as
ineligible by automation tools').

Applies the paper's canonical boolean search string uniformly to every
deduplicated candidate: title+abstract must contain at least one of the 18
cloud-DB terms AND at least one of the 7 survey-indicator terms. Records
identified via the relevance-ranked supplementary APIs (Crossref, Semantic
Scholar) that do not actually satisfy the search string are marked
ineligible here; OpenAlex records satisfy it by construction of the query.

Appends one row per record to search/screening_decisions.csv:
  stage=automation, decision in {advance, exclude},
  criteria_codes=search-string, rationale.
"""

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUERIES = json.loads((HERE / "queries.json").read_text())

TERMS = [t.lower() for t in QUERIES["cloud_db_terms"]]
# 'database-as-a-service' should also match the unhyphenated spelling
TERMS.append("database as a service")

IND_RE = re.compile(
    r"\b(survey|review|tutorial|taxonomy|systematic|state[- ]of[- ]the[- ]art|overview)\b",
    re.I,
)


def has_cloud_term(text):
    t = text.lower()
    return next((term for term in TERMS if term in t), None)


def main():
    cands = json.loads((HERE / "candidates.json").read_text())
    now = datetime.now(timezone.utc).date().isoformat()
    out = HERE / "screening_decisions.csv"
    new_file = not out.exists()
    kept = excluded = 0
    with open(out, "a", newline="") as fh:
        w = csv.writer(fh)
        if new_file:
            w.writerow(["record_id", "title", "year", "stage", "decision",
                        "criteria_codes", "rationale", "date"])
        for c in cands:
            text = (c.get("title") or "") + " " + (c.get("abstract") or "")
            term = has_cloud_term(text)
            ind = IND_RE.search(text)
            if term and ind:
                w.writerow([c["record_id"], c["title"], c["year"], "automation",
                            "advance", "search-string",
                            f"matches canonical string (term='{term}', indicator='{ind.group(0).lower()}')",
                            now])
                kept += 1
            else:
                missing = []
                if not term:
                    missing.append("no cloud-DB term")
                if not ind:
                    missing.append("no survey indicator")
                w.writerow([c["record_id"], c["title"], c["year"], "automation",
                            "exclude", "search-string",
                            "; ".join(missing) + " in title+abstract", now])
                excluded += 1
    print(f"automation stage: {kept} advance, {excluded} excluded, of {len(cands)}")


if __name__ == "__main__":
    main()
