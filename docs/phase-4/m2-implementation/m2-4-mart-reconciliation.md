# M2.4 mart reconciliation

Run `python -m uv run --group analytics python scripts/reconcile_marts.py`
against the local frozen `pulse_dev` database. The script queries dbt tables,
compares each actual count with the M2.2/M2.3 baseline, and writes the
[deterministic machine result](../../../data/validation/m2-4-mart-reconciliation.json).
All **40/40** checks passed. The artifact records both DRAFT snapshot IDs,
their input manifest SHA-256 values and the measured publication blockers.

| Grain or source state | Actual | Expected |
| --- | ---: | ---: |
| Case, repository, release dimensions | 2, 8, 2 | 2, 8, 2 |
| Represented source definitions | 9 | 9 |
| Cohort bridge and repository investigation | 8, 8 | 8, 8 |
| Release collection tasks | 54 | 54 |
| pytest / urllib3 required successes | 11 / 27 | 11 / 27 |
| pytest / urllib3 optional not_found | 1 / 5 | 1 / 5 |
| PAIRED / AFTER_ONLY / UNRESOLVED historical paths | 1 / 6 / 9 | 1 / 6 / 9 |
| Candidate rows / emitting repositories / shared artifact | 2 / 1 / 1 | 2 / 1 / 1 |
| ACCEPT / REJECT selected reviews | 0 / 2 | 0 / 2 |
| SUFFICIENT / LEGACY_UNCLASSIFIED | 2 / 38 | 2 / 38 |
| Findings / UNKNOWN / bounded NO | 40 / 38 / 2 | 40 / 38 / 2 |
| Typed observations / actual support edges | 11 / 0 | 11 / 0 |
| Adoption UNKNOWN / recovery UNKNOWN members | 8 / 8 | 8 / 8 |
| DRAFT / PUBLISHED source snapshots | 2 / 0 | 2 / 0 |
| Snapshot artifact digest mismatches / fixture mart rows | 0 / 0 | 0 / 0 |

The two candidate rows share an artifact but remain distinct, with two
independent REJECT reviews. The pytest acceptance denominator is zero for both
members, and `reviewed_acceptance_available=false`; no 0/0 rate is emitted.
The 38 `LEGACY_UNCLASSIFIED` assessments and 38 UNKNOWN findings remain
literal. Adoption and recovery are UNKNOWN for every member. Cross-fact dbt
tests compare each lower-grain preaggregate with the repository fact to detect
join inflation. Key uniqueness, selected-input membership and dimension
relationships are separately tested.

The source fingerprints cover all 30 `ingestion`/`core` tables, including
the unchanged DRAFT snapshot and input-edge tables. A clean rebuild removes
only dbt-managed schemas, leaving evidence tables intact. Repeated model row
fingerprints and the reconciliation artifact must match. No core publication
write occurred. This reconciliation validates the small frozen population,
not completeness of all external repository history.

The committed frozen-input allowlist was reverified: **142/142 files** matched
manifest SHA-256 `09d66f72862cfaa1a664cb1fc5c42a5b8fe28dbaeb35bd7f42364bdbff50a743`.
The clean dbt build created **30 models** (19 views and 11 analytical tables)
and passed **173 tests**, with zero warnings/failures, in **20.55 seconds** of
dbt elapsed time. Standalone `dbt test` also passed all 173 tests. The largest
analytical mart is `fct_collection_task` at 54 rows. A second build produced
byte-identical row sets for all 30 models; all 30 source-table fingerprints
remained unchanged, and the 40-check reconciliation JSON retained SHA-256
`1f7c30e3ae80650f41543ecc8b62737296b9eb62a282eea6d13449e2c4cfa895`.
Generated dbt docs completed successfully. These times are a local engineering
baseline on a very small frozen dataset, not a scale claim.
