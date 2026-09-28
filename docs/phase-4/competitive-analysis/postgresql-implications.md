# PostgreSQL/data-model implications — design note only

The [Milestone 1A readiness audit](../baseline-analysis/postgresql-readiness.md) remains provisional and Phase 3 HOLD applies. Market research suggests **source references and identity contracts**, not a new competitive-feature schema or a database build.

| Possible future contract decision | Evidence and reason | Gate |
| --- | --- | --- |
| External source registry with provider, product/edition, endpoint, access method, capture time, license/retention, raw artifact hash and immutable source URL | Package metadata, SCM, CI and SCA tools are separate authoritative systems [S06,S07,S13,S15,S16,S18]. | Authorized access and governance. |
| Source-specific observation reference, exact ref/commit, environment and provider object ID | Organization scans and PR/CI histories are tied to differing grains [S06,S07,S18,S22]. | No silent join between current scan and historical release case. |
| Case-to-evidence bridge with origin, copied-upstream flag, reviewer decision and sufficiency reason | PULSE Phase 2 false candidates and Phase 3 copied text require origin distinction; adjacent tools provide partial provenance. | Validated human review workflow and versioned reason codes. |
| Qualified resolved-version observation | Generic deps.dev graph and registry release metadata are not repository usage [S15,S16]. | Source/ref/environment/time rule before adoption KPI. |
| Optional external-risk reference | Existing SCA vendors already own vulnerability/policy risk [S12,S13,S17,S19,S22]. | Include only when a case decision needs it; do not mirror a full risk platform. |

Do **not** add a generic organization dependency inventory mart simply to compete with established dashboards. Do **not** add a competitive-market data warehouse or `fct_dependency_update_pr` from the small Phase 3 secondary sample. No PostgreSQL, DDL, migration, dbt or Power BI files are created.
