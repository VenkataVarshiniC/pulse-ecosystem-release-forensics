# dbt staging, intermediate and mart contracts

**Future specification, no model files.** Staging renames/casts and preserves null/status/source IDs. It does not infer lifecycle, adoption, recovery or completion. Intermediate models apply versioned evidence rules at explicit grains. Marts publish only one VALIDATED/PUBLISHED snapshot and retain source IDs for drill-through.

| Layer/model | Grain; dependencies | Output/logic boundary |
| --- | --- | --- |
| stg_pulse__cases | case_version_id; core case/release | Case/window/plan/rule/question IDs, nullable release time; no cohort inference. |
| stg_pulse__memberships | case_version_id × repository_id; core membership/repository | Frozen denominator, selection metadata. |
| stg_pulse__collection_tasks | collection_task_id; ingestion run/task/attempt | Required/optional, terminal outcome, actual retry count with attempt evidence. |
| stg_pulse__artifacts | artifact_id; core artifact/source/ref | Digest, URI, locator, method, event and retrieval time preserved separately. |
| stg_pulse__dependency_observations | observation_id; core observation/pair | Declaration, resolution and path state remain separate types; exact ref/path. |
| stg_pulse__candidates | candidate_id; core candidate | Rule/version, artifact, span, origin and nullable emission time. |
| stg_pulse__reviews | review_id; core review | Event, cycle, sequence and controlled decision; no terminal coalescing here. |
| stg_pulse__sufficiency | assessment_id; core assessment/reasons | Status, reason and required-source version intact. |
| stg_pulse__findings | finding_id; core finding/typed support edges | Status/version/assessment identity; no YES inferred from candidate. |
| int_analysis_snapshot | analysis_snapshot_id; manifest/input tables | Validates exact chosen IDs, versions and fingerprint; one row per published manifest. |
| int_case_repository | snapshot × case-version × repository; membership + manifest | Left-preserved frozen spine; one row even with zero task/artifact/candidate. |
| int_repository_evidence | snapshot × case-version × repository; spine + task/observation pre-aggregates | Core collection flag, historical exact-ref/paired/after-only status, source gaps; no target-version inference from declaration. |
| int_candidate_terminal_review | snapshot × candidate; candidate + selected review cycle | One selected terminal outcome or unresolved; duplicates fail. Candidate remains distinct from shared artifact. |
| int_stage_sufficiency | snapshot × case-version × repository × category × question; assessment + source prerequisite map | Selected assessment and reason links; missing assessment blocks published rate, not converted to INSUFFICIENT. |
| int_finding_evidence | snapshot × finding × typed support edge; finding/bridges/artifact/review | Resolves chain and qualified role; many edges remain separate, no fact counting here. |

| Analytics object | Exact grain and primary use |
| --- | --- |
| dim_case | case_version_id; release/window/plan/selection metadata. |
| dim_repository | canonical repository_id; label and provisional-identity flag. |
| dim_release | release_id; package/version/sourced boundary. |
| dim_evidence_source | source definition × actual capture method; class, provider and provenance label; never assert universal authority. |
| bridge_case_repository | snapshot × case_version × repository; complete denominator and source selection frame. |
| fct_collection_task | one run × task (collection_task_id), with snapshot-use bridge when a task is reused across snapshots; task counts are not multiplied by snapshot selection. |
| fct_repository_investigation | snapshot × case version × repository; pre-aggregated collection/context/candidate coverage, questions and unavailable reasons. |
| fct_candidate_review | snapshot × candidate; one selected review state, rule, artifact ID and source origin. |
| fct_lifecycle_finding | snapshot × case version × repository × category × question × selected finding version; status, assessment, reason. |
| fct_evidence_observation | snapshot × observation; typed declaration/resolution/path state, exact ref and artifact. |
| bridge_finding_evidence | snapshot × finding × typed support edge; drill-through only, never fact denominator. |

No operational PR fact is built from the Phase 3 bot-heavy secondary sample. No general dependency inventory, CI execution or SCA risk fact is planned. Report MET-020 uses a distinct verified replay-audit input; absent audit keeps it unavailable, rather than manufacturing success from a stable dbt run. Human disposition and recovery marts remain gated. See [fan-out register](fanout-risk-register.md).
