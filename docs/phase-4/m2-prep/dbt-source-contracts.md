# Proposed dbt source contracts

No dbt YAML, project, model or adapter is created. Sources represent hash-verified PostgreSQL rows, never live GitHub/PyPI endpoints. Source freshness is meaningful for operational load monitoring, not for judging historical evidence completeness: a frozen case can be old and valid.

| Source group | Grain/primary identity | Required lineage columns and source checks | Freshness |
| --- | --- | --- | --- |
| ingestion.source_registry | definition version/source_id | provider, type, version, access class; unique/not-null/accepted provider class | Registry change audit only |
| ingestion.collection_run | run/run_id | case_version_id, plan/collector version, timestamps/status, resume ref; relationships | Recent-run monitor only |
| ingestion.collection_task | run × plan task/task_id | run, repo, source, required, status, attempts; unique plan key, enum, relationship | Recent-run monitor only |
| ingestion.task_attempt | task × attempt number | status/time/digest; unique composite, nonnegative sequence | Recent-run monitor only |
| ingestion.load_audit | load attempt/load_id | input digest, target, loader/result, counts; successful-key uniqueness | Active load monitor |
| core.dependency_release | package release/release_id | ecosystem, package, exact version, nullable sourced release time; natural-key unique | No generic freshness SLA |
| core.repository and repository_alias | canonical identity/repository_id; alias event/alias_id | provider ID when known, provisional flag, original label/source; unique stable provider ID | No generic SLA |
| core.investigation_case and cohort_membership | case version/case_version_id; case version × repo | window, release, plan/rule/question versions, selection; unique member, FK | Frozen definitions do not stale |
| core.evidence_artifact and external_evidence_reference | capture/artifact_id; artifact × provider ref | URI, digest, method, source/ref, event/retrieval time, run/task nullable by method; hash/method/FK | Capture monitoring only |
| core.dependency_observation and historical_pair | observation_id; pair_id | artifact, case/member, type, constraint/resolution, exact ref/time, pair endpoints/status; semantic tests | No generic SLA |
| core.candidate and analyst_review | firing/candidate_id; event/review_id | artifact, rule/version, origin, emission time nullable; decision/cycle/sequence; terminal uniqueness | Review backlog monitor if authorized |
| core.sufficiency_assessment and assessment_source_reason | assessment_id; assessment × source/reason | category/question/version/status/reason/rule and required source version; enum/relationships | Snapshot-scoped |
| core.lifecycle_finding and typed support bridges | finding_id; typed support edge | assessment, category/question/version/status, support FKs; provenance/UNKNOWN tests | Snapshot-scoped |
| core.analysis_snapshot manifest and members | snapshot ID; snapshot × chosen input | versions, input digest/ref, state, fingerprint; published-only selection | Publication monitor |

The snapshot manifest relations are specified in [snapshot contract](analytical-snapshot-contract.md) even though they are not loaded now. Source tests: not_null on keys and required provenance; unique at each documented grain; relationships to parent/case member; accepted_values on controlled statuses/method; custom hash/ref/semantic tests in [test matrix](dbt-test-matrix.md). Source warnings cannot convert missing raw bytes into a passing metric. dbt should refuse unpublished manifests.
