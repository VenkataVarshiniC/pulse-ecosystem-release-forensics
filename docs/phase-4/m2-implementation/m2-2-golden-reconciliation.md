# M2.2 golden reconciliation

Run `python -m uv run python -m pulse.phase2_postgres reconcile` against `pulse_dev`. The command compares live SQL values with the predeclared [M2-PREP golden values](../m2-prep/golden-validation-values.md), writes [machine-readable results](../../../data/validation/m2-2-golden-reconciliation.json), and exits nonzero on any mismatch. The current frozen load passes **66/66** checks, including integrity and population checks. This is direct SQL validation; it is not the later dbt metric layer.

| Check | pytest 8.0.0 | urllib3 2.0.0 |
| --- | ---: | ---: |
| Members / core collection | 2/2 / 2/2 | 6/6 / 6/6 |
| Required succeeded | 11/11 | 27/27 |
| Optional `not_found` | 1/4 | 5/12 |
| Tasks / attempts / retries | 15 / 15 / 0 | 39 / 39 / 0 |
| Exact-ref declaration members | 1/2 | 1/6 |
| Paired pre-release members | 1/2 | 0/6 |
| Captures / parsed observations / pair decisions | 21 / 5 / 4 | 51 / 6 / 12 |
| Candidates / emitting members | 0 / 0 | 2 / 1 |
| Accepted / rejected reviews | 0 / 0; denominator 0, rate UNAVAILABLE | 0 / 2 |
| Matched replay attempts | 2/2 | 2/2 |
| Assessments / findings | 10 / 10 | 30 / 30 |

The 40 findings match the report's source grain: five stage categories for each of eight members. All eight observed-adoption and all eight recovery findings are UNKNOWN. The 38 UNKNOWN findings never become zeros. Two pytest stage findings are bounded NO; neither implies an event could not have occurred. The two urllib3 candidates share one capture and both independent reviews reject copied-upstream text. Their review acceptance rate is 0/2; pytest's 0/0 rate is **UNAVAILABLE**, not 0%.

The extra capture and parsed-observation splits (21/51 and 5/6) were counted from the frozen per-case manifests and reconstruction results; they are not a correction to a prior golden requirement. The SQL audit also verifies two cases, eight members, no fixtures, no non-collector captures, no published snapshots, no positive findings, no invented support edges, no duplicate task/candidate business keys and no listed orphans. PostgreSQL foreign keys enforce the remainder of the parent relationships.

The reproducible [lineage sample](../../../data/validation/m2-2-lineage.json) verifies a member alias, task capture, raw artifact digest, one historical observation, both urllib3 candidate/review rows and an UNKNOWN finding attached to a draft snapshot. All sampled logical capture paths and SHA-256 values match the frozen manifest. A second complete load returns `reused` for both cases and leaves the same analytical row counts.
