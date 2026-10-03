# M4.2 Checkpoint 1 — PostgreSQL source preflight

> Historical checkpoint: this preflight preceded implementation. Final PBIP import, semantic behavior, rendered case isolation, KPI displays, and drill-through behavior subsequently passed Power BI Desktop validation; see `power-bi-dashboard-validation.md`.

**Status: SOURCE VERIFIED; POWER BI IMPORT NOT YET VERIFIED.** Checked on 2026-10-02 against the existing isolated `127.0.0.1:55432` / `pulse_dev` cluster. The governed replay reconciliation passed against the committed publication artifact. This check used SELECT statements inside a read-only transaction; it did not connect Power BI Desktop, create a PBIX, or load Power Query data.

Approved analytical release: `m4-1b-9979f0a7b15d6e70b90f`; metric contract: `m2-5-metric-registry-v1`. The exact allowlist is pytest `08852d5f-9843-5406-a69b-7039ea2ddaa4` and urllib3 `bd3a02a5-0c2d-5eec-84fd-8e9b93a238a3`, both `PUBLISHED_VALIDATION`.

| Approved `analytics` table | pytest published | urllib3 published | Other/DRAFT rows present in mart |
| --- | ---: | ---: | ---: |
| `bridge_case_repository` | 2 | 6 | 8 |
| `bridge_finding_evidence` | 0 | 0 | 0 |
| `fct_repository_investigation` | 2 | 6 | 8 |
| `fct_collection_task` | 15 | 39 | 54 |
| `fct_candidate_review` | 0 | 2 | 2 |
| `fct_lifecycle_finding` | 10 | 30 | 40 |
| `fct_evidence_observation` | 5 | 6 | 11 |

The four approved dimension tables have no snapshot key: `dim_case` 2 rows, `dim_repository` 8, `dim_release` 2, and `dim_evidence_source` 9. Their source methods/counts are descriptive; they are not selected-snapshot rates. The snapshot-bearing marts contain older DRAFT rows with different IDs, so **Power Query must filter them before loading the model**. A report-level or slicer-only filter is insufficient.

The required filter on each of the seven snapshot-bearing tables is:

```powerquery
[snapshot_state] = "PUBLISHED_VALIDATION"
and List.Contains(
  {"08852d5f-9843-5406-a69b-7039ea2ddaa4", "bd3a02a5-0c2d-5eec-84fd-8e9b93a238a3"},
  Text.Lower(Text.From([analysis_snapshot_id]))
)
```

This is a proposed Power Query filter expression, **not a verified loaded query**. At the Desktop checkpoint, select only the 11 approved marts in Import mode, apply this filter to the seven snapshot-bearing queries before Close & Apply, inspect the query previews and loaded row counts, and verify the two exact case-to-snapshot pairings. Power BI must request its own database credentials from the user if needed; no credential is recorded here. Do not proceed to semantic relationships or DAX until the actual Desktop import proves that no DRAFT row was loaded.
