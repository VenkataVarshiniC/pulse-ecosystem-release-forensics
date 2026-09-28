# Forensic-to-analytical lineage proposal

```text
GitHub / PyPI / preserved evidence
  → immutable raw snapshots + exact query/ref + digest + capture method
  → collection run/task and load audit
  → PostgreSQL normalized core (proposed)
  → dbt staging → intermediate → analytical marts (proposed)
  → SQL / Python → Power BI / possible future application (proposed)
```

Raw snapshots are the auditable evidence, including source URI, pagination/query, ref, captured time and method (`collector`, `connector_assisted`, `fixture`). Structured rows are interpretations/indices of that evidence; reviews and findings add explicit analytical judgment. New source content or changed method creates a new versioned run/snapshot rather than overwriting provenance. A generated report can remain reproducible from its frozen input identities even if the live source later changes.

| Major measure | Required lineage | Publication boundary |
| --- | --- | --- |
| MET-001/016 core/required collection | Frozen case membership → planned run/tasks → verified terminal status. | Operational completion only; optional 404 separate. |
| MET-002 historical context | Membership → exact Git ref/path raw content → parsed observation → paired/after-only context. | Declaration coverage, not adoption; no current-state substitution. |
| MET-003 target-version evidence | Membership → qualified lock/runtime/CI artifact → version/context observation. | Future source absent now; never infer from constraint. |
| MET-005/012 sufficiency/UNKNOWN | Case question set → source plan/tasks/history/reviews → versioned assessment/reasons → finding. | Preserve missing-source reason; never recode UNKNOWN as NO. |
| MET-009/010 candidate quality | Immutable baseline ID/rule/artifact span → independent review terminal decision. | Denominator is reviewed emitted candidates only; no recall. |
| MET-021 provenance | YES finding → qualifying accepted review or direct observation → artifact/ref/digest → task/run/source. | Broken chain blocks publication. |
| MET-020 replay | Frozen case/plan/raw/baseline/review/rule version → deterministic output fingerprint. | A live re-collection is a different run, not replay. |

An analytical extract should carry `analysis_snapshot_id`, case/cohort version, method/rule version, numerator/denominator definitions, source-class completeness and any unavailable reason. Drill-through must reach the preserved artifact without implying the analytical row is raw source text. No lineage tooling is installed in this milestone.
