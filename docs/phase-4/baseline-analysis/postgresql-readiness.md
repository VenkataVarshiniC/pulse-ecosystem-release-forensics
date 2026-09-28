# PostgreSQL data-contract readiness, without a database

**Answer if authorized tomorrow:** only a bounded subset is load-ready. The Phase 2 inputs can support a first case/member/task/candidate/finding snapshot, but the proposed architecture is **PARTIAL**, not a complete release-forensics data platform. This audit creates no database, schema, DDL, migration or dbt project.

| Proposed layer | Readiness | What can be loaded from frozen evidence | Blocking fields / contract decisions |
| --- | --- | --- | --- |
| `ingestion` | **PARTIAL** | Two collector runs with 54 planned tasks/attempts, statuses, requirement, retry counts and digests; separate HTTPX resume audit; raw snapshot references. | Original Phase 2 journals/raw payloads reside in external local roots; durable governed location, access/retention, load audit and idempotent replay policy need design. Do not silently import fixtures/connector-assisted data as unattended runs. |
| `core` case/release/repository/membership | **Ready for frozen cases** | Two case definitions, release timestamps/windows, eight memberships. | Explicit versioned case definition and canonical rename identity for longitudinal data. |
| `core` artifact/observation | **PARTIAL** | Exact-ref path states, artifact refs/hashes and collector provenance. | Stable observation ID, before/after row semantics, complete historical anchor method, qualified resolved-version source. |
| `core` candidate/review/assessment/finding | **PARTIAL** | Two candidates/rejections, 40 status findings and stage sufficiency. | Candidate emission time, versioned stage-required source/reason schema, finding version and accepted YES support-chain test. |
| `core` human disposition/recovery | **BLOCKED** | No authorized organizational disposition or recovery-eligible evidence. | Decision owner/completion rule, downstream source, eligible event/set/window. |
| `analytics` member/task/review dimensions/facts | **PARTIAL** | Frozen member, task and terminal review counts support selected diagnostics. | `analysis_snapshot_id`, versioned source/review methods and bridge protection against fan-out. |
| `analytics` finding/observation/recovery marts | **PARTIAL/BLOCKED** | Per-category status diagnostic only; historical pair observations. | Stage reason linkage, observation key, positive provenance, target-version/recovery denominators. |

The main design surprise is not database performance; it is **semantic incompleteness**. A physically valid table could still calculate a false adoption/recovery rate if it coerces missing evidence to zero, merges after-only with pre-release context, or multiplies one artifact's two candidate firings. PostgreSQL preference remains provisional and implementation-gated by Phase 3 HOLD.

## Milestone 1B PR-workflow dataset decision

The frozen Phase 3 sample adds a **research PR observation** grain (sample × repository × PR), with explicit sample selection, origin of upstream text, human signal, close reason and elapsed PR duration. It does **not** justify a `fct_dependency_update_pr` in PULSE's operational analytics model. The 20 base and seven purposive discussion PRs are public secondary research selected through a title/earliest-page, bot-heavy protocol, not product-generated cases or a governed customer workflow feed. Keep this dataset and its [descriptive contracts](../workflow-analysis/workflow-dataset-contract.md) in the separate secondary-research layer. Reconsider a future PR fact only after stakeholder use case, stable acquisition/provenance, permissions, versioned sample/cohort membership, event timestamps, deduplication and decision-grain contracts are validated. No database or DDL is added.
