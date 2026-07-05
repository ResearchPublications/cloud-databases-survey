# Download Report — Cloud DB Meta-Survey References

Status of the references after manual link verification and PDF download. Unverifiable orphan entries (never cited, not in the bibliography) have been removed; the remaining Missing entries are real, cited papers still lacking a local PDF. Each verified entry links to its local PDF (named `<CitationKey>.pdf` in this folder) and to its DOI/source. Additional sources collected beyond the original 166 are listed in the final section.

## Catalog reconciliation (2026-05-29)

The "survey-of-surveys" catalog was rebuilt from verified papers only. The previous S1--S58 catalog was largely AI-generated: ~38 entries had no resolvable DOI and no PDF and have been **removed** from `cloud-db-metasurvey.bib`. The catalog is now **24 surveys (S1--S24)**, window **2016--2025**, each tied to a content-verified PDF on disk and a resolvable DOI/arXiv id. All demographic figures, the PRISMA funnel, the coverage matrix, and the synthesis-table S-IDs were re-derived from this set.

**Metadata corrected to match the on-disk PDF (cite key kept for citation stability):**
- `Li2024CloudNativeSurvey` → Dong, Zhang, Li, Zhang, "Cloud-Native Databases: A Survey", IEEE TKDE 36(12), 2024, [10.1109/TKDE.2024.3397508](https://doi.org/10.1109/TKDE.2024.3397508) (previous authors/DOI did not match the PDF).
- `Haas2024HTAPSurvey` → Chao Zhang et al., "HTAP Databases: A Survey", [arXiv:2404.15670](https://arxiv.org/abs/2404.15670), 2024 (previous Haas/TKDE metadata unverifiable).
- `Harby2022Lakehouse` → Harby & Zulkernine, IEEE BigData 2022, [10.1109/BigData55660.2022.10020719](https://doi.org/10.1109/BigData55660.2022.10020719) (previous DOI `10.3390/bdcc6040111` points to an unrelated COVID paper).
- `Angles2020GraphDB` → year corrected 2018 → 2017 (ACM CSUR 50(5)).
- `Woltmann2023DNNIndex` → Sun, Zhou & Li, "Learned Index: A Comprehensive Experimental Evaluation", PVLDB 16(8), 2023, [10.14778/3594512.3594528](https://doi.org/10.14778/3594512.3594528) (the on-file PDF is this paper, not the previously listed one).
- Already-corrected re-keys retained: `Gomes2024EdgeFog`→Ferreira et al. ([10.1145/3666001](https://doi.org/10.1145/3666001)); `Kaur2021NoSQLReview`→Kpekpassi & Faye ([10.46298/arima.13970](https://doi.org/10.46298/arima.13970)); `Mathew2021CloudMigration`→Gholami et al. ([10.1016/j.jss.2016.06.068](https://doi.org/10.1016/j.jss.2016.06.068)); `Sanka2022CloudSecSurvey`→Alouffi et al. ([10.1109/ACCESS.2021.3073203](https://doi.org/10.1109/ACCESS.2021.3073203)).

**New catalog entry added:** `Bhatti2017CloudDBReview` (Bhatti & Rad, "Databases in Cloud Computing: A Literature Review", IJITCS 2017, [10.5815/ijitcs.2017.04.02](https://doi.org/10.5815/ijitcs.2017.04.02)).

**Removed from the bibliography (fabricated / unverifiable):** `Jainaga2023Lakehouse` (its DOI `10.1186/s40537-023-00808-2` resolves to Rahul et al.'s big-data/healthcare review, not a lakehouse survey) and `Thirumuruganathan2024DBLLMSurvey` (`arXiv:2404.06234` resolves to an astronomy paper). Both were dropped; lakehouse and LLM--DB coverage is carried by `Harby2022Lakehouse`/`Pohl2024LakehouseTS` and `Affolter2019NLIDB`/`Gao2024RAGSurvey` respectively. **2026-07-05:** their orphan PDFs (whose content matched neither the fabricated citations nor their filenames) have been deleted from this folder.

**Content-mismatched PDF files — resolved 2026-07-05.** The previously flagged files whose content did not match their filenames have been deleted: `Li2023LLMQueryOpt.pdf` (a statistics paper), `Zhou2023LLM4DB.pdf` (ML-theory), `Zhu2023Pilot.pdf` (differential privacy), `BDCC-06-00111-v2.pdf` (COVID review), and `Sun2019Learned.pdf` (a duplicate of `Abraham2019DataGovernance.pdf`) — none of these keys is cited in the manuscript. `Zhou2024DBot.pdf` has been **replaced with the real D-Bot paper** (arXiv:2312.01454v2, page-1 title verified). Note: the earlier claim that "the real D-Bot DOI in the bib is correct" was itself wrong — the bib carried `10.14778/3636218.3636230`, which resolves to "Multiple Time Series Forecasting with Dynamic Graph Modeling" (which is exactly why the downloader fetched a time-series paper). The bib entry has been corrected to the Crossref-verified record: PVLDB 17(10), pp.\ 2514--2527, DOI [10.14778/3675034.3675043](https://doi.org/10.14778/3675034.3675043).

**Supporting primary studies integrated (2026-07-05, per `plans/new-papers-v1.md` §1c):** nine previously unnamed PDFs were renamed to `<CitationKey>.pdf`, their metadata verified against Crossref, bib entries added, and in-text citations placed: `Tan2019iBTune` (PVLDB 12(10), [10.14778/3339490.3339503](https://doi.org/10.14778/3339490.3339503)), `Ma2020SlowQuery` (PVLDB 13(8), [10.14778/3389133.3389136](https://doi.org/10.14778/3389133.3389136)), `Hilprecht2020Partitioning` (SIGMOD 2020, [10.1145/3318464.3389704](https://doi.org/10.1145/3318464.3389704)), `Ferretti2014Encrypted` (IEEE TPDS 25(2), [10.1109/TPDS.2013.154](https://doi.org/10.1109/TPDS.2013.154)), `Cuzzocrea2016PrivateDB` (IEEE BigData 2016, [10.1109/BigData.2016.7841032](https://doi.org/10.1109/BigData.2016.7841032)), `Dory2011Elasticity` (IARIA CLOUD COMPUTING 2011, no DOI), `Phan2014IoTCloudDB` (IEEE iThings 2014, [10.1109/iThings.2014.26](https://doi.org/10.1109/iThings.2014.26)), `Jain2016HighVariety` (IEEE ICDEW 2016, [10.1109/ICDEW.2016.7495609](https://doi.org/10.1109/ICDEW.2016.7495609); note the new-papers plan guessed 2014 — Crossref says 2016), and `Ramanathan2011SimpleDBBigtable` (IEEE ReTIS 2011, [10.1109/ReTIS.2011.6146861](https://doi.org/10.1109/ReTIS.2011.6146861)). The 21 MB PVLDB proceedings dump `010086183.pdf` (a duplicate flagged in §1a of the plan) was deleted.

## Summary

- **Total tracked references:** 101
- **✅ Verified (PDF on disk):** 98
- **⚠️ Missing (no PDF, but real & cited):** 3
- **➕ Additional sources (not among the 166):** 43

## Cited references

| Key | Title | Status | Local PDF | DOI / source |
|-----|-------|--------|-----------|--------------|
| `Abadi2012PACELC` | Consistency Tradeoffs in Modern Distributed Database System Design: CAP is Only Part of the Story | ✅ Verified | [Abadi2012PACELC.pdf](Abadi2012PACELC.pdf) | [10.1109/MC.2012.33](https://doi.org/10.1109/MC.2012.33) |
| `Abraham2019DataGovernance` | Data governance: A conceptual framework, structured review, and research agenda | ✅ Verified | [Abraham2019DataGovernance.pdf](Abraham2019DataGovernance.pdf) | [10.1016/j.ijinfomgt.2019.07.008](https://doi.org/10.1016/j.ijinfomgt.2019.07.008) |
| `Acar2018HE` | A Survey on Homomorphic Encryption Schemes: Theory and Implementation | ✅ Verified | [Acar2018HE.pdf](Acar2018HE.pdf) | [10.1145/3214303](https://doi.org/10.1145/3214303) |
| `Akidau2015Dataflow` | — | ✅ Verified | [Akidau2015Dataflow.pdf](Akidau2015Dataflow.pdf) | [10.14778/2824032.2824076](https://doi.org/10.14778/2824032.2824076) |
| `AmazonAurora2023` | Amazon Aurora Documentation | ⚠️ Missing | — | [link](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/) |
| `Angles2020GraphDB` | Foundations of Modern Query Languages for Graph Databases | ✅ Verified | [Angles2020GraphDB.pdf](Angles2020GraphDB.pdf) | [10.1145/3104031](https://doi.org/10.1145/3104031) |
| `Antonopoulos2019` | Socrates: The New SQL Server in the Cloud | ✅ Verified | [Antonopoulos2019.pdf](Antonopoulos2019.pdf) | [10.1145/3299869.3314047](https://doi.org/10.1145/3299869.3314047) |
| `Arenas2022MultiModelBenchmark` | — | ✅ Verified | [Arenas2022MultiModelBenchmark.pdf](Arenas2022MultiModelBenchmark.pdf) | [PDF](https://link.springer.com/content/pdf/10.1007/s41019-019-00110-3.pdf) |
| `Armbrust2020DeltaLake` | — | ✅ Verified | [Armbrust2020DeltaLake.pdf](Armbrust2020DeltaLake.pdf) | [PDF](https://ir.cwi.nl/pub/32924/32924.pdf) |
| `Armbrust2021Lakehouse` | Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics | ✅ Verified | [Armbrust2021Lakehouse.pdf](Armbrust2021Lakehouse.pdf) | — |
| `Barker2014Empirical` | — | ✅ Verified | [Barker2014Empirical.pdf](Barker2014Empirical.pdf) | [arXiv:1406.4974](https://arxiv.org/pdf/1406.4974.pdf) |
| `Bermbach2017Fog` | — | ✅ Verified | [Bermbach2017Fog.pdf](Bermbach2017Fog.pdf) | [arXiv:1912.06096](https://arxiv.org/pdf/1912.06096) |
| `Brewer2012CAP` | CAP Twelve Years Later: How the ``Rules'' Have Changed | ✅ Verified | [Brewer2012CAP.pdf](Brewer2012CAP.pdf) | [10.1109/MC.2012.37](https://doi.org/10.1109/MC.2012.37) |
| `Cao2021PolarDB` | PolarDB Serverless: A Cloud Native Database for Disaggregated Data Centers | ✅ Verified | [Cao2021PolarDB.pdf](Cao2021PolarDB.pdf) | [10.1145/3448016.3457560](https://doi.org/10.1145/3448016.3457560) |
| `Cattell2011Scalable` | — | ✅ Verified | [Cattell2011Scalable.pdf](Cattell2011Scalable.pdf) | [PDF](http://www.cattell.net/datastores/Datastores.pdf) |
| `Chang2008Bigtable` | — | ✅ Verified | [Chang2008Bigtable.pdf](Chang2008Bigtable.pdf) | [10.1145/1365815.1365816](https://doi.org/10.1145/1365815.1365816) |
| `Cooper2010YCSB` | — | ✅ Verified | [Cooper2010YCSB.pdf](Cooper2010YCSB.pdf) | [10.1145/1807128.1807152](https://doi.org/10.1145/1807128.1807152) |
| `Corbett2013Spanner` | Spanner: Google's Globally Distributed Database | ✅ Verified | [Corbett2013Spanner.pdf](Corbett2013Spanner.pdf) | [10.1145/2491245](https://doi.org/10.1145/2491245) |
| `Curino2011DBaaS` | Relational Cloud: A Database-as-a-Service for the Cloud | ✅ Verified | [Curino2011DBaaS.pdf](Curino2011DBaaS.pdf) | — |
| `Cuzzocrea2016PrivateDB` | Private Databases on the Cloud: Models, Issues and Research Perspectives | ✅ Verified | [Cuzzocrea2016PrivateDB.pdf](Cuzzocrea2016PrivateDB.pdf) | [10.1109/BigData.2016.7841032](https://doi.org/10.1109/BigData.2016.7841032) |
| `Dageville2016` | The Snowflake Elastic Data Warehouse | ✅ Verified | [Dageville2016.pdf](Dageville2016.pdf) | [10.1145/2882903.2903741](https://doi.org/10.1145/2882903.2903741) |
| `Davoudian2018NoSQL` | A Survey on NoSQL Stores | ✅ Verified | [Davoudian2018NoSQL.pdf](Davoudian2018NoSQL.pdf) | [10.1145/3158661](https://doi.org/10.1145/3158661) |
| `DeCandia2007Dynamo` | — | ✅ Verified | [DeCandia2007Dynamo.pdf](DeCandia2007Dynamo.pdf) | [10.1145/1323293.1294281](https://doi.org/10.1145/1323293.1294281) |
| `Depoutovitch2020Taurus` | — | ✅ Verified | [Depoutovitch2020Taurus.pdf](Depoutovitch2020Taurus.pdf) | [arXiv:2412.02792](http://arxiv.org/pdf/2412.02792) |
| `Deutsch2022GQL` | Graph Pattern Matching in GQL and SQL/PGQ | ✅ Verified | [Deutsch2022GQL.pdf](Deutsch2022GQL.pdf) | [10.1145/3514221.3526057](https://doi.org/10.1145/3514221.3526057) |
| `Dory2011Elasticity` | Measuring Elasticity for Cloud Databases | ✅ Verified | [Dory2011Elasticity.pdf](Dory2011Elasticity.pdf) | IARIA CLOUD COMPUTING 2011 (no DOI) |
| `Farber2012` | SAP HANA Database: Data Management for Modern Business Applications | ✅ Verified | [Farber2012.pdf](Farber2012.pdf) | [10.1145/2094114.2094126](https://doi.org/10.1145/2094114.2094126) |
| `Fernandez2023DataMarketplace` | — | ✅ Verified | [Fernandez2023DataMarketplace.pdf](Fernandez2023DataMarketplace.pdf) | [arXiv:2002.01047](https://arxiv.org/pdf/2002.01047.pdf) |
| `Ferretti2014Encrypted` | Distributed, Concurrent, and Independent Access to Encrypted Cloud Databases | ✅ Verified | [Ferretti2014Encrypted.pdf](Ferretti2014Encrypted.pdf) | [10.1109/TPDS.2013.154](https://doi.org/10.1109/TPDS.2013.154) |
| `Francis2018GQL` | — | ✅ Verified | [Francis2018GQL.pdf](Francis2018GQL.pdf) | [PDF](https://hal.archives-ouvertes.fr/hal-01803524/file/paper.pdf) |
| `Fuhrt2010CloudSecurity` | Handbook of Cloud Computing | ✅ Verified | [Fuhrt2010CloudSecurity.pdf](Fuhrt2010CloudSecurity.pdf) | [10.1007/978-1-4419-6524-0](https://doi.org/10.1007/978-1-4419-6524-0) |
| `Gao2023DAILSQL` | Text-to-SQL Empowered by Large Language Models: A Benchmark Evaluation | ✅ Verified | [Gao2023DAILSQL.pdf](Gao2023DAILSQL.pdf) | [10.14778/3641204.3641221](https://doi.org/10.14778/3641204.3641221) |
| `Gao2024RAGSurvey` | Retrieval-Augmented Generation for Large Language Models: A Survey | ✅ Verified | [Gao2024RAGSurvey.pdf](Gao2024RAGSurvey.pdf) | [arXiv:2312.10997](https://arxiv.org/abs/2312.10997) |
| `gartner2024dbms` | Magic Quadrant for Cloud Database Management Systems | ⚠️ Missing | — | — |
| `GDPR2016` | Regulation (EU) 2016/679 of the European Parliament and of the Council (General Data Protection Regulation) | ✅ Verified | [GDPR2016.pdf](GDPR2016.pdf) | — |
| `Gomes2024EdgeFog` | Databases in Edge and Fog Environments: A Survey | ✅ Verified | [Gomes2024EdgeFog.pdf](Gomes2024EdgeFog.pdf) | [10.1145/3666001](https://doi.org/10.1145/3666001) |
| `Graefe1993QueryOptSurvey` | — | ✅ Verified | [Graefe1993QueryOptSurvey.pdf](Graefe1993QueryOptSurvey.pdf) | [10.1145/152610.152611](https://doi.org/10.1145/152610.152611) |
| `Haas2024HTAPSurvey` | HTAP Databases: A Survey | ✅ Verified | [Haas2024HTAPSurvey.pdf](Haas2024HTAPSurvey.pdf) | [10.1109/TKDE.2023.3298514](https://doi.org/10.1109/TKDE.2023.3298514) |
| `Halevy2016Goods` | Goods: Organizing Google's Datasets | ✅ Verified | [Halevy2016Goods.pdf](Halevy2016Goods.pdf) | [10.1145/2882903.2903730](https://doi.org/10.1145/2882903.2903730) |
| `Harby2022Lakehouse` | From Data Warehouse to Lakehouse: A Comparative Review | ✅ Verified | [Harby2022Lakehouse.pdf](Harby2022Lakehouse.pdf) | [10.1109/BigData55660.2022.10020719](https://doi.org/10.1109/BigData55660.2022.10020719) |
| `Hilprecht2020Partitioning` | Learning a Partitioning Advisor for Cloud Databases | ✅ Verified | [Hilprecht2020Partitioning.pdf](Hilprecht2020Partitioning.pdf) | [10.1145/3318464.3389704](https://doi.org/10.1145/3318464.3389704) |
| `Hilprecht2022CardinalityEstimation` | DeepDB: Learn from Data, not from Queries! | ✅ Verified | [Hilprecht2022CardinalityEstimation.pdf](Hilprecht2022CardinalityEstimation.pdf) | [10.14778/3384345.3384349](https://doi.org/10.14778/3384345.3384349) |
| `Hilprecht2022Zero` | — | ✅ Verified | [Hilprecht2022Zero.pdf](Hilprecht2022Zero.pdf) | [arXiv:2201.00561](http://arxiv.org/pdf/2201.00561) |
| `Hogan2021KGSurvey` | — | ✅ Verified | [Hogan2021KGSurvey.pdf](Hogan2021KGSurvey.pdf) | [arXiv:2003.02320](https://arxiv.org/pdf/2003.02320.pdf) |
| `Huang2020TiDB` | TiDB: A Raft-Based HTAP Database | ✅ Verified | [Huang2020TiDB.pdf](Huang2020TiDB.pdf) | [10.14778/3415478.3415535](https://doi.org/10.14778/3415478.3415535) |
| `IEA2024DataCenters` | Data Centres and Data Transmission Networks | ⚠️ Missing | — | [link](https://www.iea.org/energy-system/buildings/data-centres-and-data-transmission-networks) |
| `Jain2016HighVariety` | High Variety Cloud Databases | ✅ Verified | [Jain2016HighVariety.pdf](Jain2016HighVariety.pdf) | [10.1109/ICDEW.2016.7495609](https://doi.org/10.1109/ICDEW.2016.7495609) |
| `Johnson2021FAISS` | — | ✅ Verified | [Johnson2021FAISS.pdf](Johnson2021FAISS.pdf) | [arXiv:1702.08734](https://arxiv.org/pdf/1702.08734) |
| `Kaur2021NoSQLReview` | NoSQL Databases: A Survey | ✅ Verified | [Kaur2021NoSQLReview.pdf](Kaur2021NoSQLReview.pdf) | [10.46298/arima.13970](https://doi.org/10.46298/arima.13970) |
| `Kipf2019LearnedCardinality` | — | ✅ Verified | [Kipf2019LearnedCardinality.pdf](Kipf2019LearnedCardinality.pdf) | [arXiv:1809.00677](https://arxiv.org/pdf/1809.00677.pdf) |
| `Kitchenham2007` | Guidelines for Performing Systematic Literature Reviews in Software Engineering | ✅ Verified | [Kitchenham2007.pdf](Kitchenham2007.pdf) | — |
| `Kraska2018LearnedIndex` | The Case for Learned Index Structures | ✅ Verified | [Kraska2018LearnedIndex.pdf](Kraska2018LearnedIndex.pdf) | [10.1145/3183713.3196909](https://doi.org/10.1145/3183713.3196909) |
| `Lakshman2010Cassandra` | — | ✅ Verified | [Lakshman2010Cassandra.pdf](Lakshman2010Cassandra.pdf) | [10.1145/1773912.1773922](https://doi.org/10.1145/1773912.1773922) |
| `Lamb2012Vertica` | — | ✅ Verified | [Lamb2012Vertica.pdf](Lamb2012Vertica.pdf) | [arXiv:1208.4173](https://arxiv.org/pdf/1208.4173.pdf) |
| `Lamport1998Paxos` | — | ✅ Verified | [Lamport1998Paxos.pdf](Lamport1998Paxos.pdf) | [10.1145/279227.279229](https://doi.org/10.1145/279227.279229) |
| `Lao2024GPTuner` | GPTuner: A Manual-Reading Database Tuning System via GPT-Guided Bayesian Optimization | ✅ Verified | [Lao2024GPTuner.pdf](Lao2024GPTuner.pdf) | [10.14778/3659437.3659449](https://doi.org/10.14778/3659437.3659449) |
| `Leis2023CloudPricing` | Towards Cost-Optimal Query Processing in the Cloud | ✅ Verified | [Leis2023CloudPricing.pdf](Leis2023CloudPricing.pdf) | [10.14778/3461535.3461549](https://doi.org/10.14778/3461535.3461549) |
| `Li2024CloudNativeSurvey` | Cloud-Native Database Systems: A Survey and Future Directions | ✅ Verified | [Li2024CloudNativeSurvey.pdf](Li2024CloudNativeSurvey.pdf) | [10.1109/TKDE.2023.3313441](https://doi.org/10.1109/TKDE.2023.3313441) |
| `Lu2019MultiModel` | Multi-Model Databases: A New Journey to Handle the Variety of Data | ✅ Verified | [Lu2019MultiModel.pdf](Lu2019MultiModel.pdf) | [10.1145/3323214](https://doi.org/10.1145/3323214) |
| `Ma2020SlowQuery` | Diagnosing Root Causes of Intermittent Slow Queries in Cloud Databases | ✅ Verified | [Ma2020SlowQuery.pdf](Ma2020SlowQuery.pdf) | [10.14778/3389133.3389136](https://doi.org/10.14778/3389133.3389136) |
| `Ma2021LearnedWorkload` | Query-based Workload Forecasting for Self-Driving Database Management Systems | ✅ Verified | [Ma2021LearnedWorkload.pdf](Ma2021LearnedWorkload.pdf) | [10.1145/3183713.3196908](https://doi.org/10.1145/3183713.3196908) |
| `Ma2022MBAQO` | — | ✅ Verified | [Ma2022MBAQO.pdf](Ma2022MBAQO.pdf) | [10.1145/3514221.3517869](https://doi.org/10.1145/3514221.3517869) |
| `Malkov2020HNSW` | — | ✅ Verified | [Malkov2020HNSW.pdf](Malkov2020HNSW.pdf) | [arXiv:1603.09320](http://arxiv.org/pdf/1603.09320) |
| `Marcus2021Bao` | Bao: Making Learned Query Optimization Practical | ✅ Verified | [Marcus2021Bao.pdf](Marcus2021Bao.pdf) | [10.1145/3448016.3452838](https://doi.org/10.1145/3448016.3452838) |
| `Mathew2021CloudMigration` | Cloud Migration Process—A Survey, Evaluation Framework, and Open Challenges | ✅ Verified | [Mathew2021CloudMigration.pdf](Mathew2021CloudMigration.pdf) | [10.1016/j.jss.2016.06.068](https://doi.org/10.1016/j.jss.2016.06.068) |
| `Melnik2020Dremel` | Dremel: A Decade of Interactive SQL Analysis at Web Scale | ✅ Verified | [Melnik2020Dremel.pdf](Melnik2020Dremel.pdf) | [10.14778/3415478.3415568](https://doi.org/10.14778/3415478.3415568) |
| `Moher2009PRISMA` | — | ✅ Verified | [Moher2009PRISMA.pdf](Moher2009PRISMA.pdf) | [PDF](https://journals.plos.org/plosmedicine/article/file?id=10.1371/journal.pmed.1000097&type=printable) |
| `Muller2020Serverless` | Lambada: Interactive Data Analytics on Cold Data Using Serverless Cloud Infrastructure | ✅ Verified | [Muller2020Serverless.pdf](Muller2020Serverless.pdf) | [10.1145/3318464.3389758](https://doi.org/10.1145/3318464.3389758) |
| `Narasayya2015MultiTenant` | SQLVM: Performance Isolation in Multi-Tenant Relational Database-as-a-Service | ✅ Verified | [Narasayya2015MultiTenant.pdf](Narasayya2015MultiTenant.pdf) | — |
| `Noy2019KGSurvey` | — | ✅ Verified | [Noy2019KGSurvey.pdf](Noy2019KGSurvey.pdf) | [10.1145/3331166](https://doi.org/10.1145/3331166) |
| `Opara2017LockIn` | Architectural Principles for Cloud Software | ✅ Verified | [Opara2017LockIn.pdf](Opara2017LockIn.pdf) | [10.1145/3104028](https://doi.org/10.1145/3104028) |
| `Pan2024VectorDB` | Survey of Vector Database Management Systems | ✅ Verified | [Pan2024VectorDB.pdf](Pan2024VectorDB.pdf) | [10.1007/s00778-024-00864-x](https://doi.org/10.1007/s00778-024-00864-x) |
| `Patterson2022CarbonAI` | — | ✅ Verified | [Patterson2022CarbonAI.pdf](Patterson2022CarbonAI.pdf) | [10.1109/MC.2022.3148714](https://doi.org/10.1109/MC.2022.3148714) |
| `Pavlo2017SelfDriving` | Self-Driving Database Management Systems | ✅ Verified | [Pavlo2017SelfDriving.pdf](Pavlo2017SelfDriving.pdf) | — |
| `Phan2014IoTCloudDB` | Cloud Databases for Internet-of-Things Data | ✅ Verified | [Phan2014IoTCloudDB.pdf](Phan2014IoTCloudDB.pdf) | [10.1109/iThings.2014.26](https://doi.org/10.1109/iThings.2014.26) |
| `Politou2018GDPR` | Forgetting Personal Data and Revoking Consent Under the GDPR: Challenges and Proposed Solutions | ✅ Verified | [Politou2018GDPR.pdf](Politou2018GDPR.pdf) | [10.1093/cybsec/tyy001](https://doi.org/10.1093/cybsec/tyy001) |
| `Pourreza2023DINSQL` | DIN-SQL: Decomposed In-Context Learning of Text-to-SQL with Self-Correction | ✅ Verified | [Pourreza2023DINSQL.pdf](Pourreza2023DINSQL.pdf) | — |
| `Rabl2019BenchmarkSurvey` | Just Can't Get Enough---Synthesizing Big Data Benchmarks | ✅ Verified | [Rabl2019BenchmarkSurvey.pdf](Rabl2019BenchmarkSurvey.pdf) | — |
| `Rahm2001SchemaMatching` | — | ✅ Verified | [Rahm2001SchemaMatching.pdf](Rahm2001SchemaMatching.pdf) | [PDF](https://ul.qucosa.de/api/qucosa%3A31968/attachment/ATT-0/) |
| `Ramanathan2011SimpleDBBigtable` | Comparison of Cloud Database: Amazon's SimpleDB and Google's Bigtable | ✅ Verified | [Ramanathan2011SimpleDBBigtable.pdf](Ramanathan2011SimpleDBBigtable.pdf) | [10.1109/ReTIS.2011.6146861](https://doi.org/10.1109/ReTIS.2011.6146861) |
| `Saeed2023XAI` | Explainable AI (XAI): A Systematic Meta-Survey of Current Challenges and Future Opportunities | ✅ Verified | [Saeed2023XAI.pdf](Saeed2023XAI.pdf) | [10.1016/j.knosys.2023.110273](https://doi.org/10.1016/j.knosys.2023.110273) |
| `Sanka2022CloudSecSurvey` | A Systematic Literature Review on Cloud Computing Security: Threats and Mitigation Strategies | ✅ Verified | [Sanka2022CloudSecSurvey.pdf](Sanka2022CloudSecSurvey.pdf) | [10.1109/ACCESS.2021.3073203](https://doi.org/10.1109/ACCESS.2021.3073203) |
| `Strubell2019Energy` | — | ✅ Verified | [Strubell2019Energy.pdf](Strubell2019Energy.pdf) | [PDF](https://www.aclweb.org/anthology/P19-1355.pdf) |
| `Taft2020Cockroach` | CockroachDB: The Resilient Geo-Distributed SQL Database | ✅ Verified | [Taft2020Cockroach.pdf](Taft2020Cockroach.pdf) | [10.1145/3318464.3386134](https://doi.org/10.1145/3318464.3386134) |
| `Tan2019iBTune` | iBTune: Individualized Buffer Tuning for Large-scale Cloud Databases | ✅ Verified | [Tan2019iBTune.pdf](Tan2019iBTune.pdf) | [10.14778/3339490.3339503](https://doi.org/10.14778/3339490.3339503) |
| `Tomarchio2020CloudOrchestration` | — | ✅ Verified | [Tomarchio2020CloudOrchestration.pdf](Tomarchio2020CloudOrchestration.pdf) | [PDF](https://journalofcloudcomputing.springeropen.com/track/pdf/10.1186/s13677-020-00194-7) |
| `Verbitski2017` | Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases | ✅ Verified | [Verbitski2017.pdf](Verbitski2017.pdf) | [10.1145/3035918.3056101](https://doi.org/10.1145/3035918.3056101) |
| `Viotti2016Consistency` | Consistency in Non-Transactional Distributed Storage Systems | ✅ Verified | [Viotti2016Consistency.pdf](Viotti2016Consistency.pdf) | [10.1145/2926965](https://doi.org/10.1145/2926965) |
| `Wang2024MACSQL` | MAC-SQL: A Multi-Agent Collaborative Framework for Text-to-SQL | ✅ Verified | [Wang2024MACSQL.pdf](Wang2024MACSQL.pdf) | [arXiv:2312.11242](https://arxiv.org/abs/2312.11242) |
| `Woltmann2023DNNIndex` | Learned Indexes: A Comprehensive Experimental Evaluation | ✅ Verified | [Woltmann2023DNNIndex.pdf](Woltmann2023DNNIndex.pdf) | — |
| `Wu2022FactorJoin` | — | ✅ Verified | [Wu2022FactorJoin.pdf](Wu2022FactorJoin.pdf) | [arXiv:2212.05526](https://arxiv.org/pdf/2212.05526.pdf) |
| `Xiao2018OBDA` | Ontology-Based Data Access: A Survey | ✅ Verified | [Xiao2018OBDA.pdf](Xiao2018OBDA.pdf) | [PDF](https://www.ijcai.org/proceedings/2018/0777.pdf) |
| `Xue2024DBGPT` | DB-GPT: Empowering Database Interactions with Private Large Language Models | ✅ Verified | [Xue2024DBGPT.pdf](Xue2024DBGPT.pdf) | [arXiv:2312.17449](https://arxiv.org/abs/2312.17449) |
| `Yang2020NeuroCard` | — | ✅ Verified | [Yang2020NeuroCard.pdf](Yang2020NeuroCard.pdf) | [arXiv:2006.08109](https://arxiv.org/pdf/2006.08109.pdf) |
| `Yang2022OceanBase` | OceanBase: A 707 Million tpmC Distributed Relational Database System | ✅ Verified | [Yang2022OceanBase.pdf](Yang2022OceanBase.pdf) | [10.14778/3554821.3554830](https://doi.org/10.14778/3554821.3554830) |
| `Yu2018Spider` | Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Database Semantic Parsing and Text-to-SQL Task | ✅ Verified | [Yu2018Spider.pdf](Yu2018Spider.pdf) | [10.18653/v1/D18-1425](https://doi.org/10.18653/v1/D18-1425) |
| `Zaharia2016Spark` | — | ✅ Verified | [Zaharia2016Spark.pdf](Zaharia2016Spark.pdf) | [10.1145/2934664](https://doi.org/10.1145/2934664) |
| `Zamanian2017Chiller` | — | ✅ Verified | [Zamanian2017Chiller.pdf](Zamanian2017Chiller.pdf) | [10.14778/3055330.3055335](https://doi.org/10.14778/3055330.3055335) |
| `Zhang2022CDBTune` | An End-to-End Automatic Cloud Database Tuning System Using Deep Reinforcement Learning | ✅ Verified | [Zhang2022CDBTune.pdf](Zhang2022CDBTune.pdf) | [10.1145/3299869.3300085](https://doi.org/10.1145/3299869.3300085) |
| `Zhou2022AI4DB` | Database Meets Artificial Intelligence: A Survey | ✅ Verified | [Zhou2022AI4DB.pdf](Zhou2022AI4DB.pdf) | [10.1109/TKDE.2020.2994641](https://doi.org/10.1109/TKDE.2020.2994641) |
| `Zhou2024DBot` | D-Bot: Database Diagnosis System using Large Language Models | ✅ Verified | [Zhou2024DBot.pdf](Zhou2024DBot.pdf) | [10.14778/3675034.3675043](https://doi.org/10.14778/3675034.3675043) |

## Missing references (cited, no local PDF)

The 3 references below are cited in the manuscript but still lack a local PDF. All three are **legitimate non-article sources** (vendor documentation, an agency web report, and a proprietary analyst report), not downloadable papers — so no PDF is expected. The four previously-flagged incorrect/fabricated citations (`Gomes2024EdgeFog`, `Kaur2021NoSQLReview`, `Mathew2021CloudMigration`, `Sanka2022CloudSecSurvey`) have been **corrected in the bibliography to their real papers** and are now ✅ Verified above; the inclusion window was relaxed to 2016–2025 to accommodate them.

| Key | Title (as cited) | Why no PDF | Where to get it |
|-----|------------------|-----------|-----------------|
| `AmazonAurora2023` | Amazon Aurora Documentation | Web documentation, not a paper | [AWS Aurora User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/) |
| `IEA2024DataCenters` | Data Centres and Data Transmission Networks | IEA web report, no article PDF | [iea.org](https://www.iea.org/energy-system/buildings/data-centres-and-data-transmission-networks) |
| `gartner2024dbms` | Magic Quadrant for Cloud Database Management Systems | Gartner reprint is bot-protected (Cloudflare 403); can't be fetched programmatically, but is viewable in a browser | [Gartner reprint 1-2MC14I3H](https://www.gartner.com/doc/reprints?id=1-2MC14I3H&ct=251121&st=sb) — open in browser, then Print → Save as PDF to `references/gartner2024dbms.pdf` |

## Additional sources (not in original 166)

Real, verified papers downloaded during the search that are **not** among the 166 cited keys (broader DBaaS/NoSQL/cloud-survey collection). Left under their downloaded filenames.

| File | Title | DOI |
|------|-------|-----|
| [s00778-019-00567-8.pdf](s00778-019-00567-8.pdf) | A comparative survey of recent natural language interfaces for databases | [10.1007/s00778-019-00567-8](https://doi.org/10.1007/s00778-019-00567-8) |
| [A_comparison_between_several_NoSQL_databases_with_comments_and_notes.pdf](A_comparison_between_several_NoSQL_databases_with_comments_and_notes.pdf) | A comparison between several NoSQL databases with comments and notes | — |
| [1-s2.0-S0950705125005490-main.pdf](1-s2.0-S0950705125005490-main.pdf) | A comprehensive survey on integrating large language models with knowledge-based methods | [10.1016/j.knosys.2025.113503](https://doi.org/10.1016/j.knosys.2025.113503) |
| [A_Survey_of_Cloud_Database_Systems.pdf](A_Survey_of_Cloud_Database_Systems.pdf) | A Survey of Cloud Database Systems | — |
| [A_Survey_on_Querying_Encrypted_Data_for_Database_as_a_Service.pdf](A_Survey_on_Querying_Encrypted_Data_for_Database_as_a_Service.pdf) | A Survey on Querying Encrypted Data for Database as a Service | [10.1109/CyberC.2013.12](https://doi.org/10.1109/CyberC.2013.12) |
| [A_survey_on_RDBMS_and_NoSQL_Databases_MySQL_vs_MongoDB.pdf](A_survey_on_RDBMS_and_NoSQL_Databases_MySQL_vs_MongoDB.pdf) | A survey on RDBMS and NoSQL Databases MySQL vs MongoDB | — |
| [2000824.2000829.pdf](2000824.2000829.pdf) | A survey on representation, composition and application of preferences in database systems | [10.1145/2000824.2000829](https://doi.org/10.1145/2000824.2000829) |
| [1-s2.0-S0022437526000800-main.pdf](1-s2.0-S0022437526000800-main.pdf) | A systematic review of traffic safety data collection methods and challenges: From crash databases to AI-augmented sensors | [10.1016/j.jsr.2026.05.005](https://doi.org/10.1016/j.jsr.2026.05.005) |
| [Transactions on Emerging Telecommunications Technologies - 2019 - Khan - An analytic study of architecture  security .pdf](Transactions%20on%20Emerging%20Telecommunications%20Technologies%20-%202019%20-%20Khan%20-%20An%20analytic%20study%20of%20architecture%20%20security%20.pdf) | An analytic study of architecture, security, privacy, query processing, and performance evaluation of database‐as‐a‐service | [10.1002/ett.3814](https://doi.org/10.1002/ett.3814) |
| [1-s2.0-S0950584926001060-main.pdf](1-s2.0-S0950584926001060-main.pdf) | An empirically-driven clustering framework for NoSQL data warehouse conversion: Optimizing column family design from relational big data using HDBSCAN | [10.1016/j.infsof.2026.108117](https://doi.org/10.1016/j.infsof.2026.108117) |
| [Approach_to_Enhancing_Concurrent_and_Self-Reliant_Access_to_Cloud_Database_A_Review.pdf](Approach_to_Enhancing_Concurrent_and_Self-Reliant_Access_to_Cloud_Database_A_Review.pdf) | Approach to Enhancing Concurrent and Self-Reliant Access to Cloud Database: A Review | [10.1109/CICN.2015.158](https://doi.org/10.1109/CICN.2015.158) |
| [Cassandra_vs._MongoDB_A_Systematic_Review_of_Two_NoSQL_Data_Stores_in_Their_Industry_Uses.pdf](Cassandra_vs._MongoDB_A_Systematic_Review_of_Two_NoSQL_Data_Stores_in_Their_Industry_Uses.pdf) | Cassandra vs. MongoDB: A Systematic Review of Two NoSQL Data Stores in Their Industry Uses | [10.1109/BDAI62182.2024.10692676](https://doi.org/10.1109/BDAI62182.2024.10692676) |
| [Cloud_Database-as-a-Service_DaaS_-_ROI.pdf](Cloud_Database-as-a-Service_DaaS_-_ROI.pdf) | Cloud Database-as-a-Service (DaaS) - ROI | — |
| [Comparison_of_NoSQL_Datastores_for_Large_Scale_Data_Stream_Log_Analytics.pdf](Comparison_of_NoSQL_Datastores_for_Large_Scale_Data_Stream_Log_Analytics.pdf) | Comparison of NoSQL Datastores for Large Scale Data Stream Log Analytics | [10.1109/SMARTCOMP.2019.00093](https://doi.org/10.1109/SMARTCOMP.2019.00093) |
| [206476.206480.pdf](206476.206480.pdf) | A Survey of Current Object-Oriented Databases | [10.1145/206476.206480](https://doi.org/10.1145/206476.206480) |
| [Data_Lakehouse_for_Time_Series_Data_A_Systematic_Literature_Review.pdf](Data_Lakehouse_for_Time_Series_Data_A_Systematic_Literature_Review.pdf) | Data Lakehouse for Time Series Data: A Systematic Literature Review | [10.1109/BigData62323.2024.10825961](https://doi.org/10.1109/BigData62323.2024.10825961) |
| [Database_as_a_service_DBaaS.pdf](Database_as_a_service_DBaaS.pdf) | Database as a service (DBaaS) | — |
| [Database_as_a_Service_Challenges_and_solutions_for_privacy_and_security.pdf](Database_as_a_Service_Challenges_and_solutions_for_privacy_and_security.pdf) | Database as a Service: Challenges and solutions for privacy and security | — |
| [1-s2.0-S0164121223002674-main.pdf](1-s2.0-S0164121223002674-main.pdf) | Database management system performance comparisons: A systematic literature review | [10.1016/j.jss.2023.111872](https://doi.org/10.1016/j.jss.2023.111872) |
| [Databases_in_Cloud_Computing_A_Literatur.pdf](Databases_in_Cloud_Computing_A_Literatur.pdf) | Databases in Cloud Computing: A Literature Review | [10.5815/ijitcs.2017.04.02](https://doi.org/10.5815/ijitcs.2017.04.02) |
| [1-s2.0-S0306437925000900-main.pdf](1-s2.0-S0306437925000900-main.pdf) | Density based learned spatial index for clustered data | [10.1016/j.is.2025.102606](https://doi.org/10.1016/j.is.2025.102606) |
| [Evaluating_Performance_and_User_Perceptions_of_Multi-Cloud_Database-as-a-Service_Solutions_A_Mixed-Methods_Study.pdf](Evaluating_Performance_and_User_Perceptions_of_Multi-Cloud_Database-as-a-Service_Solutions_A_Mixed-Methods_Study.pdf) | Evaluating Performance and User Perceptions of Multi-Cloud Database-as-a-Service Solutions: A Mixed-Methods Study | [10.1109/ICAC69156.2025.11361452](https://doi.org/10.1109/ICAC69156.2025.11361452) |
| [Exploring_the_Landscape_of_Tourism_Knowledge_Graphs_A_Systematic_Literature_Review.pdf](Exploring_the_Landscape_of_Tourism_Knowledge_Graphs_A_Systematic_Literature_Review.pdf) | Exploring the Landscape of Tourism Knowledge Graphs: A Systematic Literature Review | [10.1109/ICITDA64560.2024.10809644](https://doi.org/10.1109/ICITDA64560.2024.10809644) |
| [2192-113x-2-22.pdf](2192-113x-2-22.pdf) | Data management in cloud environments: NoSQL and NewSQL data stores | [10.1186/2192-113X-2-22](https://doi.org/10.1186/2192-113X-2-22) |
| [Large-scale_ontology_storage_and_query_using_graph_database-oriented_approach_The_case_of_Freebase.pdf](Large-scale_ontology_storage_and_query_using_graph_database-oriented_approach_The_case_of_Freebase.pdf) | Large-scale ontology storage and query using graph database-oriented approach: The case of Freebase | — |
| [paper31.pdf](paper31.pdf) | BTW 2017 workshop paper (title not reliably extractable from PDF) | — |
| [1-s2.0-S0952197626005063-main.pdf](1-s2.0-S0952197626005063-main.pdf) | Machine learning in modern database systems: Techniques, architectures, and deployment challenges | [10.1016/j.engappai.2026.114225](https://doi.org/10.1016/j.engappai.2026.114225) |
| [1-s2.0-S0306457325000433-main.pdf](1-s2.0-S0306457325000433-main.pdf) | MQRLD: A multimodal data retrieval platform with query-aware feature representation and learned index based on data lake | [10.1016/j.ipm.2025.104101](https://doi.org/10.1016/j.ipm.2025.104101) |
| [Multidimensional_Modelling_in_NoSQL_Database__A_Systematic_Review.pdf](Multidimensional_Modelling_in_NoSQL_Database__A_Systematic_Review.pdf) | Multidimensional Modelling in NoSQL Database : A Systematic Review | — |
| [1-s2.0-S2214579625000188-main.pdf](1-s2.0-S2214579625000188-main.pdf) | NoSQL data warehouse optimizing models: A comparative study of column-oriented approaches | [10.1016/j.bdr.2025.100523](https://doi.org/10.1016/j.bdr.2025.100523) |
| [1-s2.0-S0164121225000597-main.pdf](1-s2.0-S0164121225000597-main.pdf) | NoSQL database education: A review of models, tools and teaching methods | [10.1016/j.jss.2025.112391](https://doi.org/10.1016/j.jss.2025.112391) |
| [wingerath-2016-csrd-nosql-toolbox.pdf](wingerath-2016-csrd-nosql-toolbox.pdf) | NoSQL database systems: a survey and decision guidance | [10.1007/s00450-016-0334-3](https://doi.org/10.1007/s00450-016-0334-3) |
| [On_distributed_database_security_aspects.pdf](On_distributed_database_security_aspects.pdf) | On distributed database security aspects | — |
| [Optimizing_the_performance_of_Database_as_a_Service_DaaS_model__A_distributed_approach.pdf](Optimizing_the_performance_of_Database_as_a_Service_DaaS_model__A_distributed_approach.pdf) | Optimizing the performance of Database as a Service (DaaS) model &#x2014; A distributed approach | — |
| [Review_of_NoSQL_Data_Stores_Using_a_reactive_three-tier_application_for_software_developers_to_achieve_a_high_availability_application_design_architecture.pdf](Review_of_NoSQL_Data_Stores_Using_a_reactive_three-tier_application_for_software_developers_to_achieve_a_high_availability_application_design_architecture.pdf) | Review of NoSQL Data Stores: Using a reactive three-tier application for software developers to achieve a high availability application design architecture | — |
| [Security_model_for_cloud_database_as_a_service_DBaaS.pdf](Security_model_for_cloud_database_as_a_service_DBaaS.pdf) | Security model for cloud database as a service (DBaaS) | — |
| [SQL_versus_NoSQL_databases_for_geospatial_applications.pdf](SQL_versus_NoSQL_databases_for_geospatial_applications.pdf) | SQL versus NoSQL Databases for Geospatial Applications | — |
| [SQL_NewSQL_and_NOSQL_Databases_A_Comparative_Survey.pdf](SQL_NewSQL_and_NOSQL_Databases_A_Comparative_Survey.pdf) | SQL, NewSQL, and NOSQL Databases: A Comparative Survey | [10.1109/ICICS49469.2020.239513](https://doi.org/10.1109/ICICS49469.2020.239513) |
| [Survey_on_NoSQL_database.pdf](Survey_on_NoSQL_database.pdf) | Survey on NoSQL database | — |
| [2505.24758v3.pdf](2505.24758v3.pdf) | Survey: Graph Databases | — |
| [Systematic_Literature_Review_and_Comparative_Performance_Analysis_of_SQL_and_NoSQL_Databases_in_Big_Data_Applications.pdf](Systematic_Literature_Review_and_Comparative_Performance_Analysis_of_SQL_and_NoSQL_Databases_in_Big_Data_Applications.pdf) | Systematic Literature Review and Comparative Performance Analysis of SQL and NoSQL Databases in Big Data Applications | [10.1109/ICIMCIS63449.2024.10957463](https://doi.org/10.1109/ICIMCIS63449.2024.10957463) |
| [Temporal_and_real-time_databases_a_survey.pdf](Temporal_and_real-time_databases_a_survey.pdf) | Temporal and real-time databases: a survey | — |
| [CLOUD_DATABASE_DATABASE_AS_A_SERVICE.pdf](CLOUD_DATABASE_DATABASE_AS_A_SERVICE.pdf) | Cloud Database — Database as a Service | [10.5121/ijdms.2013.5201](https://doi.org/10.5121/ijdms.2013.5201) |
