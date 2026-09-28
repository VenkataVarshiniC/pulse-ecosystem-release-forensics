# M2.3 dbt reconciliation and reproducibility

`scripts/reconcile_dbt.py` queries the actual dbt views and writes the
deterministic [37-check result](../../../data/validation/m2-3-dbt-reconciliation.json).
All 37 checks passed against the M2.2 trusted frozen baseline; PASS is
calculated from actual versus expected values, not stored in advance. The
largest model was `stg_pulse__artifacts` at 72 rows.

| Check | dbt actual | M2.2 expected |
| --- | ---: | ---: |
| Versioned cases; cohort members | 2; 8 | 2; 8 |
| Planned release tasks; retries | 54; 0 | 54; 0 |
| pytest required succeeded / required; optional not_found / optional | 11/11; 1/4 | 11/11; 1/4 |
| urllib3 required succeeded / required; optional not_found / optional | 27/27; 5/12 | 27/27; 5/12 |
| Historical PAIRED; AFTER_ONLY; UNRESOLVED | 1; 6; 9 | 1; 6; 9 |
| Paired members: pytest; urllib3 | 1/2; 0/6 | 1/2; 0/6 |
| Candidates; candidate-emitting repositories; shared candidate artifacts | 2; 1; 1 | 2; 1; 1 |
| Selected ACCEPT; REJECT reviews | 0; 2 | 0; 2 |
| SUFFICIENT; LEGACY_UNCLASSIFIED assessments | 2; 38 | 2; 38 |
| Findings total; UNKNOWN; bounded NO | 40; 38; 2 | 40; 38; 2 |
| Adoption UNKNOWN; recovery UNKNOWN members | 8; 8 | 8; 8 |
| DRAFT snapshots; chosen artifact digest mismatches | 2; 0 | 2; 0 |
| Fixture; noncollector source captures | 0; 0 | 0; 0 |

The source fixture/capture counts describe **this frozen PostgreSQL input**, not
an assertion that all PULSE evidence was collected unattended. Capture method
remains typed throughout staging. The 38 UNKNOWN findings and two bounded
NO findings are different evidence outcomes. No unknown adoption or recovery
member is scored as zero adoption or a failed recovery. Collection completion
means required tasks succeeded; it does not establish complete historical
coverage or a positive lifecycle event.

The clean-build exercise first fingerprinted all 30 ingestion/core tables,
removed only dbt-owned schemas, and ran `dbt build`, `dbt test` and
reconciliation against unchanged `pulse_dev` source data. The clean build
created **19 views** and passed **108 tests** (57 source, 39 model generic,
12 custom SQL) with **0 warnings and 0 failures**. dbt reported 15.95 seconds
elapsed for that clean build. A second build produced identical 19 model row
sets byte for byte and the same 37/37 reconciliation. The source table
fingerprints remained identical in all 30 tables. The separate `dbt test`
also passed all 108 tests. `dbt docs generate` completed successfully.

The fingerprints sort each table's `to_jsonb` row representation before
hashing, so row retrieval order cannot create a false difference. The
comparison establishes reproducibility for these frozen inputs and model
versions; it does not forecast behavior under new evidence. Generated dbt
runtime files and local fingerprint baselines remain ignored. No source
database reset was used for this clean dbt rebuild.
