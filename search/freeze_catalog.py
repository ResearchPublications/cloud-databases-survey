#!/usr/bin/env python3
"""Assemble the frozen catalog.csv (single source of truth for the manuscript).

Rows = 22 retained existing entries + new entries from new_entries_meta.json
(qa/topic/phases from the QA assessment). Chronological S-numbering is applied
by generate_catalog_artifacts.py, not here.

Usage: freeze_catalog.py <scratchpad_dir>
"""

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRATCH = Path(sys.argv[1])

# Retained existing entries: bibkey, title_abbrev, year, topic, venue, vtype, qa, phases
# (QA for Haas/Pan from the fresh reassessment; others from the existing catalog.)
EXISTING = [
    ("Li2024CloudNativeSurvey", "Cloud-Native Databases: A Survey", 2024, "Cloud-Native Arch.", "IEEE TKDE", "journal", 8, "Design;Deploy;Operate;Optimize"),
    ("Haas2024HTAPSurvey", "HTAP Databases: A Survey", 2024, "HTAP Systems", "arXiv", "arxiv", 6.5, "Design;Operate;Optimize"),
    ("Pan2024VectorDB", "Survey of Vector Database Management Systems", 2024, "Vector Databases", "VLDB Journal", "journal", 7.5, "Design;Deploy;Optimize"),
    ("Zhou2022AI4DB", "Database Meets AI: A Survey", 2022, "AI4DB/Learned Opt.", "IEEE TKDE", "journal", 8, "Optimize;Evolve"),
    ("Woltmann2023DNNIndex", "Learned Index: A Comprehensive Experimental Evaluation", 2023, "AI4DB/Learned Opt.", "PVLDB", "journal", 7, "Optimize"),
    ("Davoudian2018NoSQL", "A Survey on NoSQL Stores", 2018, "NoSQL/NewSQL", "ACM Comp. Surv.", "journal", 8, "Design;Deploy"),
    ("Khasawneh2020SQLNewSQL", "SQL, NewSQL, and NoSQL Databases: A Comparative Survey", 2020, "NoSQL/NewSQL", "IEEE ICICS", "conference", 6, "Design;Deploy"),
    ("Tu2024CassandraMongo", "Cassandra vs. MongoDB: A Systematic Review", 2024, "NoSQL/NewSQL", "IEEE BDAI", "conference", 6, "Design;Optimize"),
    ("Kaur2021NoSQLReview", "NoSQL Databases: A Survey", 2025, "NoSQL/NewSQL", "ARIMA", "journal", 7.5, "Design;Deploy"),
    ("Mouhibha2025NoSQLDW", "NoSQL Data Warehouse Optimizing Models", 2025, "NoSQL/NewSQL", "Big Data Research", "journal", 6, "Design;Optimize"),
    ("Lu2019MultiModel", "Multi-Model Databases: A New Journey", 2019, "Multi-Model DBs", "ACM Comp. Surv.", "journal", 8, "Design;Deploy"),
    ("Angles2020GraphDB", "Foundations of Query Languages for Graph DBs", 2017, "Graph Databases", "ACM Comp. Surv.", "journal", 8, "Design;Optimize"),
    ("Gomes2024EdgeFog", "Databases in Edge and Fog Environments: A Survey", 2024, "Edge/Fog DBs", "ACM Comp. Surv.", "journal", 7.5, "Design;Deploy;Operate"),
    ("Harby2022Lakehouse", "From Data Warehouse to Lakehouse: A Comparative Review", 2022, "Data Lakehouse", "IEEE BigData", "conference", 6.5, "Design;Deploy"),
    ("Pohl2024LakehouseTS", "Data Lakehouse for Time Series Data: An SLR", 2024, "Data Lakehouse", "IEEE BigData", "conference", 6.5, "Design;Operate"),
    ("Bader2017TSDB", "Open Source Time Series Databases: A Survey", 2017, "Time-Series DBs", "BTW", "conference", 6, "Design;Operate"),
    ("Affolter2019NLIDB", "Recent NL Interfaces for Databases: A Comparative Survey", 2019, "NL/LLM-Database", "VLDB Journal", "journal", 7.5, "Optimize"),
    ("Gao2024RAGSurvey", "Retrieval-Augmented Generation for LLMs: A Survey", 2024, "NL/LLM-Database", "arXiv", "arxiv", 7, "Deploy;Operate"),
    ("Sanka2022CloudSecSurvey", "Cloud Computing Security: Threats & Mitigation--An SLR", 2021, "Security/Privacy", "IEEE Access", "journal", 7, "Operate"),
    ("Khan2019DaaSAnalytic", "Architecture, Security & Performance of DBaaS", 2019, "Security/Privacy", "Trans. Emerg. Telecom. Tech.", "journal", 6.5, "Design;Operate"),
    ("Taipalus2024DBMSPerf", "DBMS Performance Comparisons: An SLR", 2024, "Benchmarking", "J. Syst. Softw.", "journal", 7.5, "Optimize"),
    ("Mathew2021CloudMigration", "Cloud Migration Process: A Survey", 2016, "Cloud DB Migration", "J. Syst. Softw.", "journal", 7.5, "Deploy;Evolve"),
]


def abbrev_title(t, maxlen=64):
    t = t.strip().rstrip(".")
    return (t[: maxlen - 1] + "…") if len(t) > maxlen else t


def main():
    qa = json.load(open(SCRATCH / "qa_merged.json"))
    meta = json.load(open(HERE / "new_entries_meta.json"))
    rows = []
    for key, title, year, topic, venue, vtype, q, phases in EXISTING:
        rows.append({"bibkey": key, "record_id": "", "title_abbrev": title, "year": year,
                     "venue_abbrev": venue, "venue_type": vtype, "primary_topic": topic,
                     "qa": q, "phases": phases})
    seen = {r["bibkey"] for r in rows}
    for rid, m in meta.items():
        if m["bibkey"] in seen:
            continue  # resurfaced-existing already covered above
        v = qa[rid]
        rows.append({"bibkey": m["bibkey"], "record_id": rid,
                     "title_abbrev": abbrev_title(m["title"]),
                     "year": int(m["year"]), "venue_abbrev": v[13], "venue_type": v[14],
                     "primary_topic": v[11], "qa": v[10], "phases": v[12].replace(",", ";") if v[12] else ""})
        seen.add(m["bibkey"])
    rows.sort(key=lambda r: (int(r["year"]), r["bibkey"].lower()))
    with open(HERE / "catalog.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["sid", "bibkey", "record_id", "title_abbrev", "year",
                                            "venue_abbrev", "venue_type", "primary_topic", "qa", "phases"])
        w.writeheader()
        for i, r in enumerate(rows, 1):
            r["sid"] = f"S{i}"
            w.writerow(r)
    print(f"catalog.csv frozen: {len(rows)} entries, years {rows[0]['year']}–{rows[-1]['year']}")


if __name__ == "__main__":
    main()
