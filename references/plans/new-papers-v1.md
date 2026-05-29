# Plan v1 — Integrating newly downloaded sources

_Date: 2026-05-29. Scope: 26 new PDFs found in `references/` that are not yet in `download_report.md`._

## Context

The manuscript is a **meta-survey ("survey of surveys")** with:
- a curated catalog of **24 surveys (S1–S24)**, inclusion window **2016–2025**, each tied to a verified PDF + resolvable DOI;
- cross-cutting challenge sections (C1–C18) and five lifecycle-phase sections, supported by **primary-study / systems citations**;
- demographic figures (`fig:byyear`, `fig:bytopic`, `fig:byvenue`), a PRISMA funnel (412 → selected), and a synthesis table keyed by S-IDs.

Two distinct roles exist for a new paper:
1. **Catalog entry (S-ID)** — only for *surveys/reviews of cloud databases* that are in-window and from a credible venue. Adding one changes the survey count and **every demographic figure + PRISMA number**.
2. **Supporting citation** — primary studies, systems papers, and older/foundational overviews cited inside challenge/background prose. No catalog/figure impact.

**Guiding principle:** protect the integrity of the rigorously-curated 24-survey catalog and the SLR methodology. Prefer adding new material as *supporting citations*; only promote a new paper to the catalog if it is a genuine, credibly-published, in-window cloud-database survey.

## 1. Inventory & classification of the 26 files

### 1a. Duplicates — delete, do not cite (5 files, 4 papers)
| File | Reason |
|------|--------|
| `010086183.pdf` **and** `010086183 (1).pdf` | Identical (same md5); a **21 MB full PVLDB vol.15(12) proceedings dump**, not a citable single paper. Delete both. |
| `A_Survey_of_Cloud_Database_Systems (1).pdf` | Same paper (Deka) as existing `A_Survey_of_Cloud_Database_Systems.pdf` in Additional sources. |
| `CLOUD_DATABASE_DATABASE_AS_A_SERVICE (1).pdf` | Byte-identical to existing `CLOUD_DATABASE_DATABASE_AS_A_SERVICE.pdf`. |
| `Cloud-Native_Databases_A_Survey.pdf` | Same paper as verified `Li2024CloudNativeSurvey.pdf` (Dong et al., TKDE 2024). |
| `Databases_in_Cloud_Computing_A_Literatur (1).pdf` | Dup of `Bhatti2017CloudDBReview` (already in catalog). |

### 1b. Catalog-eligible surveys (in-window 2016–2025, cloud-DB review) — candidates for S25+
| File | Paper / venue / year | Notes / quality flag |
|------|----------------------|----------------------|
| `2301.10673v2.pdf` | "An Overview on Cloud Distributed Databases for Business Environments", arXiv 2301.10673, 2023 | arXiv preprint; overview, not peer-reviewed — verify depth. |
| `Datamigration.pdf` | "Data migration in the cloud database: A review of vendor solutions and challenges", 2025 | Strong topical fit (migration); **venue/peer-review unclear — verify**. |
| `Advancements_in_Cloud_Database_Migration.pdf` | "Advancements in Cloud Database Migration…", SAGE (~2024) | Migration review; verify exact year/venue/DOI. |
| `10.24271_psr.2022.301247.1104.pdf` | "A Survey of Comparing Different Cloud Database Performance: SQL and NoSQL", Passer J. 4(2022) | ⚠️ low-tier regional venue — likely **support cite, not catalog**. |
| `A Systematic Review of Cloud Computing Big Data and Databases o.pdf` | "A Systematic Review of Cloud Computing, Big Data and Databases on the Cloud", Litchfield | SLR but **broader than cloud DB**; verify year (likely 2015–16). Related-work cite, probably not catalog. |

### 1c. Supporting primary studies / systems (cite in challenge sections — NOT catalog)
| File | Paper | Target section | Proposed bib key |
|------|-------|----------------|------------------|
| `p1221-tan.pdf` | iBTune: Individualized Buffer Tuning, PVLDB 12(10) 2019, doi 10.14778/3339490.3339503 | AI4DB / knob-&-buffer tuning (C-tuning, Optimization) | `Tan2019iBTune` (reuse old key) |
| `p1176-ma.pdf` | Diagnosing Root Causes of Intermittent Slow Queries, PVLDB 13(8) 2020, doi 10.14778/3389133.3389136 | AI4DB / autonomous diagnosis (Operation) | `Ma2020SlowQuery` |
| `3318464.3389704.pdf` | Learning a Partitioning Advisor for Cloud Databases, SIGMOD 2020, doi 10.1145/3318464.3389704 | AI4DB / partitioning (Optimization) | `Hilprecht2020Partitioning` |
| `Distributed_Concurrent_..._Encrypted_Cloud_Databases.pdf` | Encrypted cloud DB access, IEEE TPDS 25(2) 2014, doi 10.1109/TPDS.2013.154 | Security & privacy (C-security) | `Ferretti2014Encrypted` |
| `Private_databases_on_the_cloud_....pdf` | Private Databases on the Cloud, IEEE BigData 2016 (Cuzzocrea) | Security & privacy | `Cuzzocrea2016PrivateDB` |
| `cloud_computing_2011_6_30_20083.pdf` | Measuring Elasticity for Cloud Databases, 2011 | Scalability & elasticity (background) | `Dory2011Elasticity` |
| `Cloud_Databases_for_Internet-of-Things_Data.pdf` | Cloud Databases for IoT Data, IEEE iThings 2014, doi 10.1109/iThings.2014.26 | Edge–cloud continuum (background) | `XX2014IoTCloudDB` |
| `High_variety_cloud_databases.pdf` | High Variety Cloud Databases (Jain, Moritz, Howe, UW) | Multi-model / data variety (background) | `Jain2014HighVariety` |
| `Comparison_..._SimpleDB_and_..._Bigtable.pdf` | SimpleDB vs Bigtable, 2011 | NoSQL origins / data models (background) | `Ramesh2011SimpleDBBigtable` |

### 1d. Older / non-survey overviews (optional background cites; mostly out-of-window 2011–2015)
`A_Study_on_Cloud_Database.pdf` (Deka 2012) · `A_Survey_of_Cloud_Database_Systems.pdf` (Deka 2012/14) · `The_future_of_database_services_Cloud_database.pdf` · `bea6d93618c688c54130b06d13997288b1f5.pdf` ("Database Services for Cloud Computing – An Overview", 2012) · `Study_on_cloud_computing_and_cloud_database.pdf` (2015) · `A_Novel_E_Service_for_E_Government.pdf` (actually *"Cloud Databases: A Paradigm Shift in Databases"*, Arora & Gupta, IJCSI 2012 — filename misleading).
→ Use **at most one or two** as a single grouped background citation in §Introduction/§Concepts; the rest add little and risk low-venue clutter.

### 1e. Likely exclude
`868-Article Text-3141-1-10-20230930.pdf` — Modern Management Review 28(3) 2023 (management venue; off-core-topic — verify, likely drop).

## 2. Recommended approach

**Keep the catalog at 24 (do not expand by default).** Integrate the new material as **supporting citations**:
- Add the four strong primary studies (§1c rows 1–4: iBTune, slow-query diagnosis, partitioning advisor, encrypted DB) to the relevant AI4DB / security prose — these materially strengthen claims.
- Add 2–3 background cites (elasticity, IoT, high-variety) where a foundational reference is currently thin.
- Hold the §1b "surveys" for a **separate decision** (see §5) — most are low-tier venues; promoting them could weaken a DKE submission.

**Alternative (only if the author wants a bigger catalog):** promote the 2–3 credible in-window migration/distributed reviews (`Datamigration`, `Advancements…Migration`, `Vikiru2023`) to S25–S27. This requires the cascade in §4.

## 3. Cleanup actions (no paper impact)
1. Delete the 5 duplicate files in §1a (keep the canonical copies already in the report).
2. Rename the kept supporting PDFs to `<BibKey>.pdf` per §1c (matches the report's `<CitationKey>.pdf` convention).
3. For each cited paper, extract exact author list/venue/pages from the PDF first page before writing the bib entry (do **not** hand-fabricate metadata — this is the failure mode that produced the earlier bad citations).

## 4. If catalog is expanded (per-survey cascade) — otherwise skip
For each promoted survey:
1. Add `@article`/`@inproceedings` to `cloud-db-metasurvey.bib` (verified metadata).
2. Add a catalog row `Sn & Title~\cite{key} & year & topic & venue & phases \\` in the App.\ catalog table.
3. Update **all** of: `fig:byyear` coordinates + `ymax`/symbolic coords; `fig:bytopic` and `fig:byvenue` counts; the **PRISMA** "n selected" and the running "24 surveys" → new N in abstract, intro (×2), RQ1, conclusion, and `tab:lifecycle-phases`/synthesis tables.
4. Re-verify each figure sums to the new N.

## 5. Open decisions for the author
1. **Expand the catalog or not?** Recommended: **no** — keep 24; use new papers as support cites. (Expanding pulls in low-tier venues and forces re-derivation of every demographic figure + PRISMA.)
2. **Venue-quality bar:** confirm whether Passer J., IJCSI, IJCT, Modern Management Review, and non-peer-reviewed arXiv overviews are acceptable to cite at all in a DKE submission. Recommend excluding the weakest (§1e and most of §1d).
3. **Migration emphasis:** the *Evolution/Migration* phase is the least-covered (per §6 of the paper). If the author wants to strengthen it, `Datamigration` (2025) and `Advancements…Migration` are the best candidates to promote — pending venue verification.

## 6. Execution checklist (once decisions in §5 are made)
- [ ] Delete §1a duplicates; rename §1c keepers to `<BibKey>.pdf`.
- [ ] Extract verified metadata for each paper to be cited.
- [ ] Add bib entries (support cites + any approved catalog entries).
- [ ] Insert `~\cite{}` calls at the target sections in `main.tex` (§1c/§1d mappings).
- [ ] If catalog expanded: run the §4 cascade and re-check figure sums.
- [ ] Update `download_report.md`: move cited papers to Verified, list the rest under Additional sources, drop deleted dups, fix counts.
- [ ] `latexmk` clean build; confirm no undefined citations and figures still sum correctly.

## Appendix — files → disposition (quick index)
- **Delete (dup):** `010086183.pdf`, `010086183 (1).pdf`, `A_Survey_of_Cloud_Database_Systems (1).pdf`, `CLOUD_DATABASE_DATABASE_AS_A_SERVICE (1).pdf`, `Cloud-Native_Databases_A_Survey.pdf`, `Databases_in_Cloud_Computing_A_Literatur (1).pdf`
- **Cite (primary/support):** `p1221-tan.pdf`, `p1176-ma.pdf`, `3318464.3389704.pdf`, `Distributed_..._Encrypted_Cloud_Databases.pdf`, `Private_databases_on_the_cloud_....pdf`, `cloud_computing_2011_6_30_20083.pdf`, `Cloud_Databases_for_Internet-of-Things_Data.pdf`, `High_variety_cloud_databases.pdf`, `Comparison_..._SimpleDB_..._Bigtable.pdf`
- **Catalog candidates (decide):** `2301.10673v2.pdf`, `Datamigration.pdf`, `Advancements_in_Cloud_Database_Migration.pdf`, `10.24271_psr.2022.301247.1104.pdf`, `A Systematic Review of Cloud Computing Big Data and Databases o.pdf`
- **Background (optional, mostly out-of-window):** `A_Study_on_Cloud_Database.pdf`, `A_Survey_of_Cloud_Database_Systems.pdf`, `The_future_of_database_services_Cloud_database.pdf`, `bea6d93618c688c54130b06d13997288b1f5.pdf`, `Study_on_cloud_computing_and_cloud_database.pdf`, `A_Novel_E_Service_for_E_Government.pdf`
- **Likely exclude:** `868-Article Text-3141-1-10-20230930.pdf`
