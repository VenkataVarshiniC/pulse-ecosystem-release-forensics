# ADR-004 — PostgreSQL as preferred structured store (proposed)

**Status:** design preference only; Phase 3 HOLD prohibits installation, database creation, loading or migration. The exact physical schema and deployment choice are not locked.

## Decision context and rationale

PULSE joins declared case/release/repository membership to planned tasks, immutable artifact references, historical observations, candidate/review decisions, sufficiency and versioned findings. Its current demonstrated scale is **two cases/eight repositories**, not a warehouse-scale event stream. The central risks are identity integrity, missing-data semantics and auditable many-to-many evidence links, rather than raw volume. PostgreSQL is the preferred **primary structured database** because relational keys/constraints can enforce identity and references, SQL can express bounded analytical joins/windows, and it is a practical common source for Python, dbt and Power BI and a possible future FastAPI app. PostgreSQL [documents foreign-key integrity](https://www.postgresql.org/docs/current/tutorial-fk.html); Microsoft [documents a PostgreSQL Power Query connector](https://learn.microsoft.com/en-us/power-query/connectors/postgresql); dbt [documents source/model data tests](https://docs.getdbt.com/docs/build/data-tests). Compatibility does not itself justify building this stack before user/source gates are met.

| Option | Fit to PULSE now | Revisit condition |
| --- | --- | --- |
| **PostgreSQL — preferred** | Strong relational model, constraints and SQL for small/medium bounded analytical workloads; one coherent operational/analytical store is a reasonable first design. | Reassess size, concurrency, security, hosting and actual workloads after authorization. |
| BigQuery | Strong potential for much larger warehouse/event workloads; demonstrated PULSE volume does not require that complexity. | Large history scans, separate warehouse team or measured performance/cost need. |
| SQLite | Useful local replay/test store, but less suitable as primary shared flagship analytics/application store with concurrent governed users and schema layers. | Single-user embedded/offline product becomes the real requirement. |
| MongoDB | Raw documents could be stored, but PULSE's case/member/task/artifact/review/finding relationships and metric joins favor relational constraints. | Product evidence model becomes predominantly document retrieval rather than governed joins. |
| Snowflake | Capable analytical warehouse; service/cost/governance overhead is not justified by the current two-case validation. | Material multi-team warehouse scale or an existing organizational platform changes economics. |

This is a **fit decision**, not a universal vendor ranking or performance claim. Do not introduce BigQuery/Snowflake merely for résumé breadth.

## Evidence and schema boundaries

```text
GitHub / PyPI / preserved evidence
  → immutable raw forensic snapshots (URI/ref, digest, query, capture method)
  → versioned collection/provenance metadata
  → proposed PostgreSQL ingestion + normalized core
  → proposed dbt staging/intermediate/analytics marts
  → SQL / Python / Power BI (and possible future application)
```

Raw snapshots remain the audit source; PostgreSQL stores identifiers, typed records, and links, **not a silently rewritten copy of raw truth**. A connector-assisted snapshot and a fixture can never be counted as a successful unattended collector artifact. Each load would verify hash/ref and preserve source event time separately from capture/load time.

| Proposed schema | Conceptual entities | Boundary |
| --- | --- | --- |
| `ingestion` | `collection_run`, `collection_task`, `source_registry`, `load_audit`, raw snapshot pointer/hash. | Operational provenance and idempotent loading; one task may have no artifact. |
| `core` | `investigation_case`, `dependency_release`, `repository`, `cohort_membership`, `evidence_artifact`, `dependency_observation`, `target_version_observation`, `candidate`, `analyst_review`, `sufficiency_assessment`, `lifecycle_finding`, `investigation_disposition`. | Normalized business concepts and identity rules from [Phase 3](../phase-3/data-requirements.md); absent future sources remain absent. |
| `analytics` | `dim_case`, `dim_repository`, `dim_release`, `dim_evidence_source`, `bridge_case_repository`, `fct_collection_task`, `fct_repository_investigation`, `fct_candidate_review`, `fct_lifecycle_finding`, `fct_evidence_observation`, `bridge_finding_evidence`. | One explicit analytical snapshot and [grain](analytical-grain.md) per published view; dbt transformations proposed, not built. |

No DDL, database, migration, server, or dbt project is created by this ADR. Security roles, retention, backup, availability, deployment, and performance remain later requirements and baseline questions; no SLA is invented.
