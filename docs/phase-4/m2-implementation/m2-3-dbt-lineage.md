# M2.3 source-to-dbt lineage

The lineage below is for **frozen input evidence**, not a published analytical
snapshot. M2.3 materializes staging and intermediate views only. The rightmost
column names planned M2.4 consumers from the M2-PREP contract; none exists yet.
Every source identity remains traceable through the view or its documented
parent. dbt model descriptions and column semantics are also in `schema.yml`.

| PostgreSQL source | Staging model and grain/key | Intermediate consumer and grain/key | Planned mart consumer |
| --- | --- | --- | --- |
| `core.investigation_case`, `core.dependency_release` | `stg_pulse__cases`; `case_version_id` | `int_case_repository`; case version × repository | `dim_case`, `dim_release`, `bridge_case_repository` |
| `core.cohort_membership`, `core.repository` | `stg_pulse__memberships`; case version × repository | `int_case_repository`; case version × repository | `dim_repository`, `bridge_case_repository` |
| `ingestion.collection_run`, `collection_task`, `task_attempt` | `stg_pulse__collection_tasks`; `collection_task_id` | `int_collection_task_status`; `collection_task_id`, then `int_repository_evidence`; case version × repository | `fct_collection_task`, `fct_repository_investigation` |
| `ingestion.source_registry`, `core.evidence_artifact` | `stg_pulse__artifacts`; `artifact_id` | `int_collection_task_status` and `int_repository_evidence` use separately aggregated collector captures; `int_analysis_snapshot` checks chosen hashes | `dim_evidence_source`, `fct_repository_investigation` |
| `core.dependency_observation` | `stg_pulse__dependency_observations`; `observation_id` | `int_repository_evidence`; case version × repository | `fct_evidence_observation` |
| `core.historical_pair` | `stg_pulse__historical_pairs`; `historical_pair_id` | `int_repository_evidence`; case version × repository, with PAIRED and AFTER_ONLY separate | `fct_repository_investigation` |
| `core.candidate`, `analyst_review` | `stg_pulse__candidates`; `candidate_id`; `stg_pulse__reviews`; `review_id` | `int_candidate_terminal_review`; `candidate_id`; separate candidate aggregate feeds `int_repository_evidence` | `fct_candidate_review` |
| `core.sufficiency_assessment`, `assessment_source_reason` | `stg_pulse__sufficiency`; `assessment_id` | `int_stage_sufficiency`; `assessment_id`; finding join uses this identity | `fct_lifecycle_finding` |
| `core.lifecycle_finding`, three typed finding-support bridges | `stg_pulse__findings`; `finding_id`; `stg_pulse__finding_support`; finding × support type × support ID × role | `int_finding_evidence`; `finding_id` after support aggregation | `fct_lifecycle_finding`, `bridge_finding_evidence` |
| `core.analysis_snapshot`, six typed snapshot input bridges | `stg_pulse__snapshots`; `analysis_snapshot_id` | `int_analysis_snapshot`; `analysis_snapshot_id` | Future snapshot selection/manifest validation |

The 8-row `int_case_repository` spine starts with the frozen membership keys
and is never reduced by an inner join to sparse evidence. Task, capture,
history, observation and candidate relations aggregate at their own grain
before joining to that spine. One capture may emit two candidates and two
independent reviews without becoming two artifacts or four review rows.

`capture_method` identifies collector, connector-assisted and fixture
captures. Collector-only repository coverage counts do not promote the other
methods to unattended evidence. `source_event_time` and `retrieved_at` remain
independent, nullable and nonnullable clocks respectively. Historical PAIRED,
AFTER_ONLY, UNRESOLVED and CROSS_FILE_AMBIGUITY remain separate; a later
capture alone does not reconstruct a before state. Source sufficiency status
retains `LEGACY_UNCLASSIFIED`; `analytical_status_family` is an additional
label, never a replacement. Finding UNKNOWN remains distinct from bounded NO.

M2-PREP described some intermediate grains as snapshot-scoped and
`int_finding_evidence` as one row per support edge. The only current snapshots
are DRAFT, so these M2.3 views use original case/member, candidate, assessment
or finding identities and **do not** claim a published snapshot selection.
Typed support edges remain in `stg_pulse__finding_support`; they are aggregated
before joining into one finding row to make counts safe. Snapshot-scoped final
marts and publication checks remain M2.4 work. The implementation follows
the additive V002–V004 PostgreSQL schema, including legacy sufficiency and
historical source-key/clock fields, where that differs from older M2-PREP prose.
