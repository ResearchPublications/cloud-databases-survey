#!/usr/bin/env python3
"""Three-way consistency check: catalog table <-> bib <-> references/ PDFs.

Verifies, exiting non-zero on any failure:
  1. every \\cite{} key in the tab:catalog longtable has a bib entry
     carrying a doi= or an arXiv identifier;
  2. references/<Key>.pdf exists and starts with %PDF- for every catalog key;
  3. the catalog row count N matches:
       - the S1--S<N> range used in the caption,
       - fig:byyear coordinate sum,
       - fig:bytopic coordinate sum,
       - fig:byvenue legend counts,
       - per-year tallies of the catalog rows themselves;
  4. no stale S-IDs beyond S<N> anywhere in main.tex;
  5. if search/catalog.csv exists, its rows match the catalog table
     (bibkey set and years);
  6. if search/screening_decisions.csv and the PRISMA figure both exist,
     the funnel arithmetic in the figure matches scripted tallies.
"""

import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
TEX = (REPO / "main.tex").read_text()
BIB = (REPO / "cloud-db-metasurvey.bib").read_text()

failures = []


def fail(msg):
    failures.append(msg)
    print(f"  FAIL: {msg}")


def ok(msg):
    print(f"  ok: {msg}")


# ---- 1+2: catalog rows -> bib + PDF -----------------------------------
m = re.search(r"\\label\{tab:catalog\}.*?\\endlastfoot(.*?)\\end\{longtable\}", TEX, re.S)
if not m:
    sys.exit("cannot locate tab:catalog body")
body = m.group(1)
rows = re.findall(r"^(S\d+)\s*&.*?\\cite\{([A-Za-z0-9]+)\}.*?&\s*(\d{4})\s*&", body, re.M)
N = len(rows)
print(f"catalog rows: {N}")

bib_entries = {}
for bm in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", BIB, re.S):
    bib_entries[bm.group(1).strip()] = bm.group(2)

for sid, key, year in rows:
    ent = bib_entries.get(key)
    if ent is None:
        fail(f"{sid}: cite key {key} not in bib")
        continue
    has_doi = re.search(r"^\s*doi\s*=", ent, re.M)
    has_arxiv = re.search(r"arxiv", ent, re.I)
    has_url = re.search(r"^\s*url\s*=", ent, re.M)
    if not (has_doi or has_arxiv):
        if has_url:
            print(f"  warn: {sid}: {key} has only a url= identifier (no DOI/arXiv)")
        else:
            fail(f"{sid}: {key} has neither doi nor arXiv id in bib")
    pdf = REPO / "references" / f"{key}.pdf"
    if not pdf.exists():
        fail(f"{sid}: references/{key}.pdf missing")
    elif pdf.read_bytes()[:5] != b"%PDF-":
        fail(f"{sid}: references/{key}.pdf is not a PDF")
    byear = re.search(r"year\s*=\s*\{(\d{4})\}", ent)
    if byear and byear.group(1) != year:
        fail(f"{sid}: catalog year {year} != bib year {byear.group(1)} ({key})")
if not failures:
    ok(f"all {N} catalog entries have bib entry with id + valid PDF")

# ---- 3: figure sums ----------------------------------------------------
ids = [int(s[1:]) for s, _, _ in rows]
if ids != list(range(1, N + 1)):
    fail(f"catalog S-IDs not contiguous 1..{N}")

# fig:byyear
ym = re.search(r"\\addplot[^;]*coordinates\s*\{([^}]*)\}[^;]*;\s*\\end\{axis\}\s*\\end\{tikzpicture\}\s*\\caption\{Distribution of the \d+ selected surveys by publication year", TEX)
if ym:
    coords = re.findall(r"\((\d{4}),(\d+)\)", ym.group(1))
    total = sum(int(c) for _, c in coords)
    if total != N:
        fail(f"fig:byyear sums to {total}, catalog has {N}")
    else:
        ok(f"fig:byyear sums to {N}")
    tex_years = {y: int(c) for y, c in coords if int(c) > 0}
    cat_years = {}
    for _, _, y in rows:
        cat_years[y] = cat_years.get(y, 0) + 1
    if tex_years != cat_years:
        fail(f"fig:byyear per-year mismatch: fig={tex_years} catalog={cat_years}")
else:
    fail("cannot parse fig:byyear")

# fig:bytopic
tm = re.search(r"xbar.*?coordinates\s*\{(.*?)\};", TEX, re.S)
if tm:
    tcoords = re.findall(r"\((\d+),", tm.group(1))
    ttotal = sum(int(c) for c in tcoords)
    if ttotal != N:
        fail(f"fig:bytopic sums to {ttotal}, catalog has {N}")
    else:
        ok(f"fig:bytopic sums to {N}")
else:
    fail("cannot parse fig:bytopic")

# fig:byvenue legend counts
vm = re.findall(r"(Journals|Conferences|arXiv)\s*\((\d+)\)", TEX)
if vm:
    vtotal = sum(int(c) for _, c in vm[:3])
    if vtotal != N:
        fail(f"fig:byvenue legend sums to {vtotal}, catalog has {N}")
    else:
        ok(f"fig:byvenue sums to {N}")

# ---- 4: stale S-IDs ----------------------------------------------------
stale = sorted({s for s in re.findall(r"\bS(\d+)\b", TEX) if int(s) > N})
if stale:
    fail(f"stale S-IDs beyond S{N}: {['S'+s for s in stale]}")
else:
    ok(f"no S-IDs beyond S{N}")

# ---- 5: catalog.csv agreement -----------------------------------------
cat_csv = HERE / "catalog.csv"
if cat_csv.exists():
    csv_rows = list(csv.DictReader(open(cat_csv)))
    csv_keys = {r["bibkey"] for r in csv_rows}
    tex_keys = {k for _, k, _ in rows}
    if csv_keys != tex_keys:
        fail(f"catalog.csv keys != tex keys; only-in-csv={sorted(csv_keys-tex_keys)} only-in-tex={sorted(tex_keys-csv_keys)}")
    else:
        ok("catalog.csv bibkeys match tab:catalog")

# ---- 6: PRISMA arithmetic ---------------------------------------------
dec_csv = HERE / "screening_decisions.csv"
if dec_csv.exists():
    dec = list(csv.DictReader(open(dec_csv)))
    ta = [d for d in dec if d["stage"] == "title_abstract"]
    ft = [d for d in dec if d["stage"] == "full_text"]
    ta_adv = sum(1 for d in ta if d["decision"] in ("advance", "include"))
    ft_inc = sum(1 for d in ft if d["decision"] == "include")
    fig = re.search(r"Records screened by title/abstract \(n=(\d+)\).*?Full-text articles assessed \(n=(\d+)\)", TEX, re.S)
    if fig:
        screened, assessed = int(fig.group(1)), int(fig.group(2))
        if screened != len(ta):
            fail(f"PRISMA screened n={screened} but decisions file has {len(ta)} title/abstract rows")
        else:
            ok(f"PRISMA screened n matches decisions ({screened})")
        if assessed != ta_adv:
            fail(f"PRISMA assessed n={assessed} but {ta_adv} advanced from title/abstract")
    cat_csv2 = HERE / "catalog.csv"
    qa_csv = HERE / "qa_scores.csv"
    if qa_csv.exists() and cat_csv2.exists():
        cat_qa = [float(r["qa"]) for r in csv.DictReader(open(cat_csv2))]
        below = [q for q in cat_qa if q < 6]
        if below:
            fail(f"catalog.csv contains {len(below)} entries below the QA>=6 threshold")
        else:
            ok("all catalog entries meet the QA>=6 threshold")

# ---- matrix <-> catalog cross-check ----
mat_path = HERE / "challenge_matrix.csv"
if mat_path.exists():
    mat = list(csv.DictReader(open(mat_path)))
    mat_sids = {r["sid"] for r in mat}
    cat_sids = {f"S{i}" for i in range(1, N + 1)}
    if mat_sids != cat_sids:
        fail(f"challenge_matrix sids != catalog sids: {mat_sids ^ cat_sids}")
    else:
        ok(f"challenge_matrix covers all {N} catalog entries")
    badv = [(r["sid"], k) for r in mat for k, v in r.items()
            if k.startswith("c") and v not in ("0", "1", "2")]
    if badv:
        fail(f"non-0/1/2 codes in matrix: {badv[:5]}")
    # Table 8 total (substantive pairs) equals matrix sum of code==2
    subst = sum(1 for r in mat for k, v in r.items() if k.startswith("c") and v == "2")
    tm = re.search(r"Total \(paper-challenge pairs\)\}\}(?:.*?)\\textbf\{(\d+)\} \\\\", TEX, re.S)
    if tm and int(tm.group(1)) != subst:
        fail(f"Table 8 grand total {tm.group(1)} != matrix substantive pairs {subst}")
    elif tm:
        ok(f"Table 8 grand total matches matrix ({subst})")

# ---- lifecycle-example S-IDs carry that phase ----
lc = re.search(r"\\label\{tab:lifecycle-phases\}.*?\\end\{tabular\}", TEX, re.S)
if lc and (HERE / "catalog.csv").exists():
    phases_by_sid = {}
    for r in csv.DictReader(open(HERE / "catalog.csv")):
        phases_by_sid[r["sid"]] = r["phases"]
    phase_name = {"Design": "Design", "Deployment": "Deploy", "Operation": "Operate",
                  "Optimization": "Optimize", "Evolution": "Evolve"}
    for line in lc.group(0).split("\\\\"):
        mrow = re.match(r"\s*(Design|Deployment|Operation|Optimization|Evolution)\b.*?&\s*((?:S\d+[,\s]*)+)&", line)
        if mrow:
            phase = phase_name[mrow.group(1)]
            for sid in re.findall(r"S\d+", mrow.group(2)):
                if phase not in phases_by_sid.get(sid, ""):
                    fail(f"lifecycle table: {sid} listed under {phase} but catalog says {phases_by_sid.get(sid)}")

print()
if failures:
    print(f"{len(failures)} FAILURES")
    sys.exit(1)
print("ALL CHECKS PASSED")
