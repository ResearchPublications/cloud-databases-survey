#!/usr/bin/env python3
"""Generate every catalog-derived LaTeX artifact from search/catalog.csv.

catalog.csv columns:
  sid,bibkey,title_abbrev,year,venue_abbrev,venue_type,primary_topic,qa,phases
  - venue_type in {journal, conference, arxiv}
  - phases: semicolon list drawn from {Design, Deploy, Operate, Optimize, Evolve}
  - sid is regenerated here (chronological: year asc, then bibkey) unless
    --keep-sids is passed.

Prints to stdout, in order:
  1. tab:catalog longtable rows
  2. fig:byyear \\addplot coordinates (numeric x axis) + ymax
  3. fig:bytopic symbolic y coords + coordinates + xmax
  4. fig:byvenue slice angles + legend counts
  5. tab:lifecycle-phases S-ID lists + counts
  6. per-year and per-topic tallies (for prose checking)
  7. PRISMA funnel numbers derived from screening_decisions.csv + qa_scores.csv
"""

import csv
import sys
from collections import Counter, OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def esc(s):
    return (s.replace("&", "\\&").replace("%", "\\%").replace("#", "\\#")
             .replace("…", "\\ldots{}").replace("_", "\\_"))


def main():
    rows = list(csv.DictReader(open(HERE / "catalog.csv")))
    if "--keep-sids" not in sys.argv:
        rows.sort(key=lambda r: (int(r["year"]), r["bibkey"].lower()))
        for i, r in enumerate(rows, 1):
            r["sid"] = f"S{i}"
    N = len(rows)

    phase_code = {"Design": "D", "Deploy": "Dp", "Operate": "O", "Optimize": "Op", "Evolve": "E"}

    def fmt_qa(q):
        return str(int(float(q))) if float(q) == int(float(q)) else str(q)

    print(f"%% ===== 1. tab:catalog rows (N={N}) =====")
    for i, r in enumerate(rows):
        sep = " \\\\\n\\addlinespace" if i < N - 1 else " \\\\"
        codes = " ".join(phase_code[p] for p in r["phases"].split(";") if p)
        typ = r.get("type", "S")
        print(f"{r['sid']} & {esc(r['title_abbrev'])}~\\cite{{{r['bibkey']}}} & {r['year']} & {typ} & "
              f"{esc(r['primary_topic'])} & {esc(r['venue_abbrev'])} & {fmt_qa(r['qa'])} & "
              f"{codes}{sep}")

    years = Counter(int(r["year"]) for r in rows)
    y0, y1 = min(years), max(years)
    print(f"\n%% ===== 2. fig:byyear (numeric axis {y0}--{y1}) =====")
    coords = " ".join(f"({y},{years.get(y, 0)})" for y in range(y0, y1 + 1))
    print(f"%% ymax suggestion: {max(years.values()) + 2}")
    print(f"\\addplot[fill=cblue!60, draw=black] coordinates {{{coords}}};")

    topics = Counter(r["primary_topic"] for r in rows)
    ordered = topics.most_common()
    print(f"\n%% ===== 3. fig:bytopic (xmax suggestion: {ordered[0][1] + 1}) =====")
    print("symbolic y coords={")
    for t, _ in reversed(ordered):
        print(f"    {{{esc(t)}}},")
    print("},")
    print("coordinates {")
    for t, c in ordered:
        print(f"    ({c},{{{esc(t)}}})")
    print("};")

    vt = Counter(r["venue_type"] for r in rows)
    nj, nc, na = vt.get("journal", 0), vt.get("conference", 0), vt.get("arxiv", 0)
    print(f"\n%% ===== 4. fig:byvenue: Journals {nj}, Conferences {nc}, arXiv {na} =====")
    a1 = 360 * nj / N
    a2 = a1 + 360 * nc / N
    print(f"%% Journals ({nj}): {100*nj/N:.1f}%  slice 0 -> {a1:.1f} deg, label at {a1/2:.1f}")
    print(f"%% Conferences ({nc}): {100*nc/N:.1f}%  slice {a1:.1f} -> {a2:.1f} deg, label at {(a1+a2)/2:.1f}")
    print(f"%% arXiv ({na}): {100*na/N:.1f}%  slice {a2:.1f} -> 360 deg, label at {(a2+360)/2:.1f}")

    print("\n%% ===== 5. tab:lifecycle-phases =====")
    for ph in ["Design", "Deploy", "Operate", "Optimize", "Evolve"]:
        sids = [r["sid"] for r in rows if ph in r["phases"].split(";")]
        print(f"{ph}: n={len(sids)}  {', '.join(sids)}")

    print("\n%% ===== 6. tallies =====")
    print("by year:", dict(sorted(years.items())))
    print("by topic:", dict(ordered))
    era = Counter()
    for r in rows:
        y = int(r["year"])
        era["1999-2009" if y < 2010 else "2010-2015" if y < 2016 else "2016-2020" if y < 2021 else "2021-2026"] += 1
    print("by era:", dict(era))

    dec_path = HERE / "screening_decisions.csv"
    if dec_path.exists():
        import json as _json
        dec = list(csv.DictReader(open(dec_path)))
        def arm(rid):
            if rid.startswith("CAND-M"): return "manual"
            if rid.startswith("CAND-S"): return "snowball"
            return "api"
        log = _json.loads((HERE / "search_log.json").read_text())
        api_stage = lambda st: [d for d in dec if d["stage"] == st and arm(d["record_id"]) == "api"]
        auto_ex = sum(1 for d in api_stage("automation") if d["decision"] == "exclude")
        ta = api_stage("title_abstract")
        ta_ex = sum(1 for d in ta if d["decision"] == "exclude")
        rc_ex = sum(1 for d in api_stage("recheck") if d["decision"] == "exclude")
        rc_ov = len(api_stage("recheck_override"))
        sought = len(ta) - ta_ex - rc_ex + rc_ov
        retr = api_stage("retrieval")
        nr = sum(1 for d in retr if d["decision"] == "exclude")
        assessed = sought - nr
        ft = api_stage("full_text")
        ft_by = {}
        for d in ft:
            ft_by[d["criteria_codes"]] = ft_by.get(d["criteria_codes"], 0) + (d["decision"] == "exclude")
        ft_inc = sum(1 for d in ft if d["decision"] == "include")
        fr = [d for d in dec if d["stage"] == "freeze_review" and arm(d["record_id"]) == "api"]
        fr_ex = sum(1 for d in fr if d["decision"] == "exclude")
        fr_merge = sum(1 for d in fr if d["decision"] == "merge")
        va = [d for d in dec if d["stage"] == "venue_audit" and d["decision"] == "exclude"]
        va_api = sum(1 for d in va if arm(d["record_id"]) == "api")
        api_included = ft_inc - fr_ex - fr_merge - va_api
        # NOTE: full_text 'include' rows above are QA>=6 includes only if the
        # threshold was applied upstream; below-threshold appear as QA-threshold rows.
        man_inc = sum(1 for d in dec if arm(d["record_id"]) == "manual"
                      and d["stage"] == "full_text" and d["decision"] == "include") \
                  - sum(1 for d in dec if arm(d["record_id"]) == "manual"
                        and d["stage"] == "freeze_review" and d["decision"] == "exclude")
        sb_ids = {d["record_id"] for d in dec if arm(d["record_id"]) == "snowball"}
        sb_nr = sum(1 for d in dec if arm(d["record_id"]) == "snowball"
                    and d["stage"] == "retrieval" and d["decision"] == "exclude")
        prior = N - api_included - man_inc
        print(f"\n%% ===== 7. PRISMA (arm-aware) =====")
        print(f"ARM A - databases: raw records {log['dedup']['raw_records']}, "
              f"duplicates removed {log['dedup']['raw_records'] - log['dedup']['final_candidates']}, "
              f"unique {log['dedup']['final_candidates']}")
        print(f"  marked ineligible by automation (canonical search string): {auto_ex}")
        print(f"  screened (title/abstract): {len(ta)} -> excluded {ta_ex} + strict-recheck {rc_ex - rc_ov}")
        print(f"  reports sought: {sought}; not retrieved (EC5): {nr}; assessed: {assessed}")
        print(f"  full-text excluded by code: {ft_by}")
        print(f"  full-text includes: {ft_inc}; freeze-review exclusions: {fr_ex}; merged duplicate: {fr_merge}; venue-integrity exclusions (EC6): {va_api}")
        print(f"  included via databases: {api_included}")
        print(f"ARM B - other methods: prior catalog 24 (2 fail raised QA bar -> {prior} carried), "
              f"manual PDFs 5 -> included {man_inc}, snowballing {len(sb_ids)} -> not retrieved {sb_nr}, included 0")
        print(f"TOTAL included in catalog: {N} = {api_included} (databases) + {man_inc} (manual) + {prior} (prior version)")


if __name__ == "__main__":
    main()
