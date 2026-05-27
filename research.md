# Manuscript Review — *Cloud Databases: A Systematic Meta-Survey*
### Target journal: Data & Knowledge Engineering (Elsevier)

**Date:** 2026-05-27
**Reviewed file:** `main.tex` (1,532 lines), `cloud-db-metasurvey.bib` (102 entries)
**Status after this pass:** compiles cleanly (71 pages, BibTeX OK, no undefined citations).

---

## Executive summary

The manuscript is a good thematic and structural fit for DKE: it explicitly frames
cloud-database challenges in data- and knowledge-engineering terms (knowledge graphs,
ontology-mediated access, metadata/lineage, schema evolution), uses the Elsevier
`elsarticle` class with `elsarticle-num`, and follows a recognizable SLR structure.

Two problems dominated the review:

1. **Citation / data integrity (CRITICAL, author action required).** The 58 catalog
   references — the actual *dataset* of this survey-of-surveys — are largely
   **unverified** and show signs of being machine-generated placeholders.
2. **Internal data inconsistency (FIXED this pass).** The stated time window and all
   three demographic figures did not match the master catalog. These have been
   reconciled to the catalog.

Plus a set of **DKE submission-readiness gaps** (keywords, highlights, AI declaration,
PRISMA reporting, threats-to-validity, corresponding-author markup), all **fixed this
pass**.

> **Top of the to-do list:** before submitting, **verify every one of the 58 catalog
> references against a real DOI / publisher page.** Fabricated references in the core
> dataset are a desk-reject (and integrity) risk that no amount of formatting fixes
> mitigates. See Part 2.

---

## Part 1 — DKE journal-fit check

### Scope alignment — strong
DKE publishes survey articles at "the interface of data engineering and knowledge
engineering." The manuscript's Knowledge-Engineering perspective (§2.3), the per-
challenge "DKE relevance" research directions, and contribution **C5** make the fit
explicit. No scope concern.

### Compliance checklist (against Elsevier *Guide for Authors*)

| Item | Requirement | Before | Status |
|---|---|---|---|
| Article class | `elsarticle`, `elsarticle-num` | Present | ✅ OK |
| Keywords | ≤ 7, avoid multi-word | 8 keywords | ✅ **Fixed** → 7 |
| Highlights | 3–5 bullets, ≤ 85 chars | Absent | ✅ **Added** (as versioned comment block) |
| Declaration of generative AI | Required | Absent | ✅ **Added** (author must confirm wording) |
| Competing-interest declaration | Required | Present | ✅ OK |
| Data availability | Required | Weak ("upon request") | ✅ **Strengthened** (supplementary material) |
| PRISMA reporting | Expected for SLRs | Diagram only, uncited | ✅ **Added** PRISMA-2020 citation + reporting |
| Threats to validity | Expected for SLRs | Absent | ✅ **Added** subsection |
| Corresponding-author markup | `\cortext` for `\corref` | Commented out | ✅ **Restored** |
| Author bio (≤100 w) + photo | Requested | Absent | ⛔ Author action (camera-ready) |
| CRediT roles | Encouraged | Absent | ⚠️ Optional (single author) |

---

## Part 2 — Critical issue: citation & data integrity (AUTHOR ACTION)

**This was not fully resolved — it requires the author to verify real publications.**

### Evidence
- The flagged catalog `.bib` entries have **no DOI/URL**, generic titles
  ("…: A Comprehensive Survey"), and round page ranges (`1--35`, `1--28`):
  `Lee2023CloudCost`, `Abraham2023DataGovCloud`, `Wang2023HybridCloud`,
  `Kumar2023PerfTuning`, `Howard2022Consensus`, and others.
- `references/download_report.txt` (the only verification artifact found) records that
  the download script tried **166 entries: 37 downloaded, 118 FAILED, 11 skipped.**
  Of the S1–S58 catalog, only a handful resolved to a real PDF — e.g. **S6**
  `Jainaga2023Lakehouse`, **S51** `Gao2024RAGSurvey`, **S54**
  `Thirumuruganathan2024DBLLMSurvey`, **S55** `Deutsch2022GQL`.
- The script's failure reasons ("no open-access PDF", "Semantic Scholar returned
  nothing") **do not distinguish a real-but-paywalled paper from one that does not
  exist** — so the `references/` folder is *not* evidence that the catalog is real.

### Required action (highest priority)
1. For **each** of S1–S58, confirm the paper exists: locate a DOI / publisher landing
   page; add `doi = {…}` to the `.bib` entry. Any entry you cannot confirm must be
   replaced with a real survey or removed.
2. Re-derive the demographic figures and the master catalog **from the verified set**
   (the figures were aligned to the *current* catalog this pass — they must be
   re-checked once the catalog is confirmed/curated).

### Related inclusion-criteria issue
- **S16** (`Pavlo2017SelfDriving`, "Self-Driving DBMS", CIDR 2017) is a **vision/position
  paper, not a survey** → violates **IC1**. Recommend removing it (and re-checking
  **S7** `Davoudian2018NoSQL`, 2018) or justifying its inclusion. *Not removed here*
  because deletion renumbers S-IDs across Tables 2–3 — an author decision.

---

## Part 3 — What was changed in this pass

All edits are in `main.tex` (and one `.bib` addition). The PDF rebuilds cleanly.

### Data-consistency fixes (figures reconciled to the master catalog)
The catalog (S1–S58) actually spans **2017–2024 with zero 2025 papers**; the prose said
"2019–2025" and the figures used non-matching numbers. Recomputed from the catalog:

- **By-year** (Fig. `byyear`): now `2017:1, 2018:1, 2019:3, 2020:6, 2021:8, 2022:13,
  2023:13, 2024:13` (= 58). Previously `2019–2025` summing with a fictitious 2025 bar.
- **By-topic** (Fig. `bytopic`): now sums to **58** (was **72**, despite being labelled
  "primary topic"). Counts: Cloud-Native 12, AI4DB 10, NoSQL/NewSQL 4, Migration 4,
  Security 4, Vector 3, Graph 3, Benchmarking 3, HTAP 2, Lakehouse 2, Cost 2,
  Multi-Model 2, Governance 2, Serverless 2, Edge/Fog 2, Sustainability 1. Bars sorted;
  added a clarifying note that each survey has one primary topic.
- **By-venue** (Fig. `byvenue`): now **Journals 43, Conferences 12, arXiv 3** (= 58).
  Previously claimed 10 arXiv + **4 book chapters that do not exist in the catalog**.
  PVLDB/CIDR/IEEE BigData counted as conferences (noted in the figure source).
- **Scope window:** "2019–2025" → "2017–2024" in the abstract, introduction, C1, RQ1,
  IC3, and Final Remarks; "past seven years" → "recent years"; trend wording updated.

### Figure styling (black & white, no rounded corners)
- Remapped the 10 color macros (`cblue`, `corange`, …) to **gray levels**, so every
  TikZ/pgfplots figure renders monochrome at once. Bars and pie wedges are colored on
  the `\addplot`/wedge directly (pgfplots ignores axis-level `fill`), with **black
  borders** and **black data labels** for print contrast.
- Removed all `rounded corners` from node styles — boxes now have square corners.

### DKE compliance / editorial fixes
- **Keywords** trimmed 8 → 7 (dropped "distributed databases").
- **Highlights** block added (5 bullets, each ≤ 85 chars) as a versioned comment.
- **Declaration of generative AI** section added before Data availability.
- **Data availability** statement strengthened to promise supplementary material.
- **Corresponding-author** footnote `\cortext[cor1]{…}` restored (was commented out).
- **PRISMA 2020** entry (`Page2021PRISMA`, BMJ, DOI 10.1136/bmj.n71) added to the
  `.bib` and cited in the methodology intro, the flow-diagram caption, and the results.
- **Threats to validity** subsection added (construct / internal / external / conclusion
  validity, incl. the single-reviewer limitation).
- **Stray duplicate** `SECTION 7: RESEARCH ROADMAP` comment banner removed.
- **Abstract** claim softened: "research roadmap … is proposed" → "set of … research
  directions is outlined", matching the condensed Future-Work subsection.

---

## Part 4 — Remaining recommendations (ready-to-paste where applicable)

### 4.1 Verify references — see Part 2 (do this first).

### 4.2 Provide the supplementary material now promised
The Data-availability statement now references a protocol/logs/QA-scores/extraction
package. Either attach it at submission, deposit it (e.g., Zenodo/OSF) and cite the DOI,
or revert the statement to "available upon request" if no package will be provided.

### 4.3 Surface per-paper quality-assessment scores
The method states a QA1–QA8 rubric and a ≥4/8 threshold but never shows scores. Add a
`QA (/8)` column to the Appendix catalog (Table `catalog`) so the rubric is auditable:

```latex
% in the longtable preamble, add a column:
\begin{longtable}{c p{3.6cm} c p{2.3cm} p{2.3cm} c p{4.3cm}}
\toprule
\textbf{ID} & \textbf{Title (Abbreviated)} & \textbf{Year} & \textbf{Primary Topic}
 & \textbf{Venue} & \textbf{QA (/8)} & \textbf{Lifecycle Phases Covered} \\
```

### 4.4 Decide on the two out-of-window / non-survey entries
Either remove **S16** (vision paper, IC1) and re-check **S7** (2018) — restoring a clean
2019–2024 window and `N=56` — or keep them and retain the widened 2017–2024 window used
here. If you remove them, renumber S-IDs and re-run the figure counts.

### 4.5 Optional: strengthen the "roadmap" contribution (C4)
The dedicated roadmap section was condensed into a short Future-Work list. If you keep
C4 as a headline contribution, consider a compact prioritized table mapping the 18
challenges → near/medium/long-term actions, so the contribution matches the claim.

### 4.6 Author bio + photo (camera-ready)
DKE requests a ≤100-word bio and a passport-style photo per author.

---

## Prioritized action list

**Must-fix before submission**
1. Verify/replace all 58 catalog references (DOIs). *(Part 2)*
2. Decide on S16/S7 inclusion and finalize the time window. *(4.4)*
3. Confirm the generative-AI declaration text reflects actual usage. *(done; confirm)*
4. Provide or rescope the supplementary-material promise. *(4.2)*

**Should-fix**
5. Add per-paper QA scores to the catalog. *(4.3)*
6. Re-verify the three figures against the *verified* catalog. *(Part 3)*

**Nice-to-have**
7. Expand the prioritized roadmap into a table. *(4.5)*
8. CRediT statement; author bio/photo at camera-ready. *(4.6)*

---

## Reference integration log (2026-05-27)

The user downloaded ~43 real reference PDFs into `references/` and asked for them to be
studied and integrated, while the user concurrently removes the AI-generated catalog
entries. Decisions: **additive now, catalog swap later**; **widen the inclusion window**
(applied during the deferred catalog rebuild — here, pre-2017 surveys are cited as
foundational background only).

**Done this pass (additive):**
- Added **37 verified BibTeX entries** (with DOIs/arXiv ids where available) to
  `cloud-db-metasurvey.bib` under a "NEWLY VERIFIED REFERENCES" block.
- Wired **35** of them into the prose (1–2 cites per point) across: DBaaS spectrum (§3.2),
  data-model landscape (§3.4), lakehouse (§3.5), KE/knowledge-graphs (§2.3), cost (§2.4),
  and challenges C1 (scalability), C3 (performance/benchmarking), C4 (security), C7 (data
  models), C8 (heterogeneous QP), C14 (AI–DB), design-phase schema, and the LLM/NLIDB
  section (§6.1).
- `Stefanidis2011Prefs` (query preferences — tangential) left in the `.bib` uncited,
  available if needed.
- Confirmed the two pre-existing entries that now have real PDFs — `Pan2024VectorDB` (S3)
  and `Zhou2022AI4DB` (S4, "Database Meets AI") — already carry correct metadata + DOIs;
  no change needed.
- Build: clean compile, **no undefined citations**, 74 pages.

**Excluded (off-topic / superseded):** traffic-safety SLR (`S0022437526000800`, mis-download),
Object-Oriented Databases survey (1995), Tourism Knowledge Graphs SLR (domain-specific).

**Deferred — catalog rebuild (after the user flags the AI-generated entries):**
1. Replace AI-generated `S1–S58` entries with verified surveys (many of the new ones are
   catalog-eligible under the widened window).
2. Update IC3 + abstract/intro window text to the finalized widened range.
3. Regenerate the three demographic figures (year/topic/venue) and all counts from the
   rebuilt catalog.
4. Update the coverage (Table `challenge-coverage`) and synthesis (Table
   `challenge-synthesis`) `S`-IDs to match.

## Sources (DKE author guidance)
- [Guide for authors — Data & Knowledge Engineering (Elsevier/ScienceDirect)](https://www.sciencedirect.com/journal/data-and-knowledge-engineering/publish/guide-for-authors)
- [DKE journal home / aims & scope](https://www.sciencedirect.com/journal/data-and-knowledge-engineering)
- [PRISMA 2020 statement (Page et al., BMJ 2021)](https://doi.org/10.1136/bmj.n71)
