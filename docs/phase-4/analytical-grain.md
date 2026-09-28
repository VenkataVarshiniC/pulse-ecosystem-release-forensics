# Grain and key contract for proposed analytical objects

These are future **logical analytical grains**, not implemented tables. A frozen case can have multiple runs and reports; every published mart must select and record one verified analytical snapshot (`analysis_snapshot_id`: case fingerprint + chosen run/history/baseline/review/report/method versions) so replays and later revisions never double count. Immutable artifact identity is retained separately.

| Object | Exact row grain and candidate key | Expected use / duplicate risk |
| --- | --- | --- |
| `dim_case` | One row per case definition version (`case_id`, `case_version`). | Window, target release, selection frame; do not overwrite a revised case. |
| `dim_repository` | One row per canonical repository identity (`repository_id`). | Stable label/host; rename aliases tracked separately if needed. |
| `dim_release` | One row per upstream package + release version + source identity (`release_id`). | Release boundary reference; unresolved time is not fabricated. |
| `dim_evidence_source` | One row per controlled source class and capture method (`source_key`). | Collector/connector-assisted/fixture separation; source access class. |
| `bridge_case_repository` | One row per (`case_id`, `case_version`, `repository_id`). | Frozen denominator and selection rationale; never inner-join away. |
| `fct_collection_task` | One row per (`run_id`, `task_id`) in frozen plan. | Required/optional, terminal status, attempts; tasks without artifact remain. |
| `fct_repository_investigation` | One row per (`analysis_snapshot_id`, `case_id`, `repository_id`). | Member-level coverage/outcome flags and reasons. No candidate/artifact row duplicated here. |
| `fct_candidate_review` | One row per (`analysis_snapshot_id`, `candidate_id`) with at most one terminal decision. | Reviewed-emitted denominator; retain unreviewed/NEEDS_REVIEW. If full review history becomes needed, a separate event fact has grain (`candidate_id`, `review_event_id`). |
| `fct_lifecycle_finding` | One row per (`analysis_snapshot_id`, `case_id`, `repository_id`, `lifecycle_category`, `finding_version`). | Stage sufficiency/UNKNOWN/YES/bounded NO. Snapshot selects an explicitly published version; never assume stage order. |
| `fct_evidence_observation` | One row per (`analysis_snapshot_id`, `observation_id`) scoped to case × repository × immutable artifact/ref/path. | Historical/target-version observations; type and context distinguish declaration from resolved use. Multiple observations can cite one artifact. |
| `bridge_finding_evidence` | One row per (`finding_version_key`, `artifact_id`, `observation_id_or_review_id`) support link. | Many-to-many provenance; never use this bridge to count findings without `DISTINCT` at finding grain. |

No SCD Type 2 is proposed for ordinary observations: explicit case versions, exact refs, capture timestamps and finding versions already carry relevant history. If mutable repository metadata later matters for a decision, version it deliberately rather than quietly overwriting analytical labels. See [star proposal](analytical-data-model.md).
