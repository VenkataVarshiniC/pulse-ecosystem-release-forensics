# Proposed dbt transformation and testing architecture

**Design only.** If a later decision authorizes PostgreSQL implementation, dbt would express repeatable SQL transformations and assertions over **verified structured records**. It would not retrieve GitHub/PyPI data, replace immutable snapshots, conduct human review, or manufacture missing observations. [dbt's documentation](https://docs.getdbt.com/docs/build/data-tests) supports generic unique/not-null/relationship/accepted-value tests; the PULSE-specific rules below would need custom data tests and source-level audit.

```text
PostgreSQL ingestion/core sources
  → staging (typed, renamed, provenance preserved)
  → intermediate (one verified snapshot, member/task/candidate/stage logic)
  → analytical dimensions/facts/marts
  → metric contracts / BI exposure
```

| Layer | Planned models | Responsibility |
| --- | --- | --- |
| Sources | `ingestion.*`, `core.*` declared with source metadata | Point to loaded, hash-verified records; publish capture method and load/run identity. |
| Staging | `stg_pulse__cases`, `stg_pulse__memberships`, `stg_pulse__tasks`, `stg_pulse__reviews`, `stg_github__artifacts`, `stg_pypi__releases` | Normalize names/statuses only; preserve null/UNKNOWN and source event vs capture time. No inference of adoption. |
| Intermediate | `int_repository_evidence`, `int_candidate_reviews`, `int_stage_sufficiency`, `int_analysis_snapshot` | Resolve case/run/version identity, source prerequisites, terminal review and reason-coded uncertainty; materialize at documented grain. |
| Marts | `dim_case`, `dim_repository`, `dim_release`, `dim_evidence_source`, `fct_collection_task`, `fct_repository_investigation`, `fct_candidate_review`, `fct_lifecycle_finding`, `fct_evidence_observation` plus bridges | Stable facts for metrics and drill-through with numerator/denominator metadata. |

## Future test contract

Generic: non-null keys and required status fields; unique IDs/composite grains; relationships from every fact to its declared case/member/source; accepted values for capture method, task, review, assessment and finding statuses. Custom: one member per frozen case/repository; no missing cohort member after joins; one terminal decision per candidate/snapshot; rejected or unresolved candidate never linked to accepted finding; YES has intact provenance; UNKNOWN never encoded as bounded NO; after-only history cannot qualify a negative release-window finding; recovery has eligible event/set/window; source event time is not substituted by capture time; case/repository/snapshot grain stays unique; all denominators reconcile to frozen cohort or explicit eligible set. Fixture and connector-assisted records are segregated from unattended collector metrics. Store failing rows for investigation and block affected marts rather than silently filter.

Model version, source/run IDs, input hashes and test results would accompany each published analytical snapshot. Actual package/adapter versions and execution settings are deferred. No dbt files or transformations are created in Milestone 1.
