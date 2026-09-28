# M2.1 PostgreSQL relational foundation

This document describes the **M2.1 starting schema**. M2.2 subsequently applied V002–V004 and loaded the two frozen Phase 2 cases. The current schema and load mapping are documented in [the M2.2 mapping](phase2-to-postgres-mapping.md), with operational commands in the [runbook](migration-runbook.md). Statements below that no real evidence is loaded describe the M2.1 checkpoint, not the current database.

Migration [V001](../../../infra/postgres/migrations/V001__base_relational_foundation.sql) implements the stable [M2-PREP physical contract](../m2-prep/postgresql-physical-model.md) in PostgreSQL 16.14. The database is an index and typed interpretation of external immutable raw evidence, not the original forensic source. No frozen Phase 2 evidence, dbt marts, Power BI objects or stakeholder disposition tables are loaded or built.

| Schema | Table(s) | Grain and key |
| --- | --- | --- |
| public | schema_migrations | One applied migration version; integer PK |
| ingestion | source_registry | One provider/source definition version; source_id UUID PK, provider/type/version unique |
| ingestion | collection_run | One execution; run ID UUID PK, case-version FK |
| ingestion | collection_task | One planned task in a run; task ID UUID PK, run/plan task key unique; run/case and frozen member composite FKs |
| ingestion | task_attempt | One task attempt; task/attempt-number composite PK |
| ingestion | load_audit | One load attempt; load UUID PK; one successful idempotency key per target |
| core | dependency_release | One ecosystem/package/version; release UUID PK and natural unique key |
| core | repository, repository_alias | Stable provider identity and observed names; provider ID unique when known; alias UUID PK |
| core | investigation_case, cohort_membership | One immutable case definition version and one member per case version/repository; UUID and composite PKs |
| core | evidence_artifact, external_evidence_reference | One captured payload reference and one artifact/provider-object ref; independent UUID keys |
| core | dependency_observation, historical_pair | One typed parsed claim and one versioned before/after pairing decision; UUID keys |
| core | candidate, analyst_review | One rule firing and one review event; independent UUID keys, candidate fingerprint unique, terminal review unique per cycle |
| core | sufficiency_assessment, assessment_source_reason | One versioned member/question assessment and one coded source reason edge |
| core | lifecycle_finding | One versioned member/category/question finding; UUID PK and scoped version unique |
| core | finding_artifact_support, finding_observation_support, finding_review_support | One typed finding/support edge with real FKs and composite PK |
| core | analysis_snapshot, snapshot_run, snapshot_artifact, snapshot_candidate, snapshot_review, snapshot_assessment, snapshot_finding | One manifest and typed chosen-input edges; UUID PK/fingerprint unique and composite edge PKs |

Case and membership triggers prevent updates/deletes after FROZEN and prevent moving a member into a frozen case. The freeze transition requires at least one member. Artifact provenance rows reject updates/deletes. Observation fingerprints are unique. Composite FKs tie candidate/observation repository to the cited artifact and tie findings to an assessment for the same case, member, category and question. Status CHECKs preserve task required/optional outcomes, collector/connector-assisted/fixture capture, declaration versus resolution, historical pair status, review NEEDS_EVIDENCE versus REJECT, sufficiency SUFFICIENT/INSUFFICIENT/SOURCE_UNAVAILABLE/CONFLICTING, and findings QUALIFYING_EVIDENCE/NO_QUALIFYING_EVIDENCE_FOUND/UNKNOWN. No NO_EVENT_OCCURRED value exists.

Collector artifacts require a task, repository, and matching task/source/repository composite FK. Connector-assisted and fixture captures cannot masquerade as task-linked collector artifacts. Content digest is indexed but not unique; capture fingerprint is unique, so identical bytes captured in different contexts remain separate artifacts. The known one-artifact/two-candidate shape is supported. Source event and retrieval time are independent nullable/required timestamptz fields respectively. Semantic versions, refs and URLs are text; SHA-256 fields require lowercase 64-hex. No JSONB is used.

The migration adds eight targeted lookup indexes beyond PK/unique indexes: task run/repository; artifact digest and task; observation case/repository/package; candidate case/repository and artifact; review candidate/cycle/sequence; finding case/repository/category. Query plans should drive any later index expansion.

Cross-row qualification remains an application/dbt/human-review concern under [M2-PREP's integrity contract](../m2-prep/database-integrity-contract.md): matching before/after ref/path/time, sufficiency prerequisites for a bounded NO, and accepted provenance for a YES. The typed FK support chain is implemented and tested, but a positive finding's semantic qualification is not asserted solely by a database CHECK. Snapshot metadata and typed input links are implemented; publication and dbt mart validation come later.

Stakeholder-dependent disposition, portfolio priority, business completion and recovery tables are intentionally absent. Analysis snapshot metadata is structural and has no current published analytic dataset. The only substantive contract adjustment is an extra composite collector task/source/repository FK and a trigger protecting moves into frozen cohorts; both strengthen the documented identity rules.

M2.3 adds dbt-managed views in `dbt_staging` and `dbt_intermediate`, plus a
test-audit schema, without altering the source schemas. See the
[transformation lineage](m2-3-dbt-lineage.md) for each view's grain and
source-to-future-mart mapping.

M2.4 adds 11 dbt-managed validation tables in `analytics`: four dimensions,
five facts and two bridges. Their two input snapshots remain DRAFT, so the
tables are not published analytical results. See the [analytical model](m2-4-analytical-model.md)
for exact grains, relationships and publication blockers.
