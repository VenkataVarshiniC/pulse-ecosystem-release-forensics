# Native PostgreSQL 16.14 development runbook

The host used for M2.1 has native PostgreSQL 16.14 tools and no Docker CLI. PostgreSQL **16** is a [supported major version](https://www.postgresql.org/support/versioning/); 16.14 is pinned to the exact locally tested toolchain. The current 16.15 minor update should be evaluated as a separate documented pin change rather than silently substituted. Use the PostgreSQL 16.14 Windows installer/tools or set PULSE_PG_BIN to a directory with the matching binaries. No cloud or default postgres database holds PULSE project state.

Run from the repository root in PowerShell:

~~~powershell
./infra/postgres/db.ps1 -Action init
./infra/postgres/db.ps1 -Action start
./infra/postgres/db.ps1 -Action migrate -Database pulse_dev
./infra/postgres/db.ps1 -Action reset -Database pulse_test
$env:PULSE_REQUIRE_DB_TESTS = '1'
python -m uv run pytest tests/database -p no:cacheprovider
python -m uv run pytest -p no:cacheprovider
./infra/postgres/db.ps1 -Action status
~~~

The first command creates a fresh cluster under ignored .local/postgres and a generated 256-bit password in ignored root .env. It refuses to overwrite an existing cluster. The cluster listens only on 127.0.0.1:55432 with SCRAM password authentication. The existing system PostgreSQL service on 5432 is untouched. pulse_dev and pulse_test are separate databases. The script checks its own cluster is running before create, migrate or reset. .env.example in infra/postgres contains placeholders only. Do not commit or print .env, .local, passwords or API tokens.

The bootstrap pulse_local role is a superuser **inside this isolated development cluster** so it can initialize and migrate schemas; it is not an application or BI account. Before any shared or production deployment, define separate least-privilege loader, transformation and read-only roles and upgrade to the current supported PostgreSQL minor release. This local setup makes no enterprise-security claim.

The migration runner applies ordered VNNN__description.sql files. Each file must wrap DDL and its schema_migrations insertion in one transaction. Applied versions are skipped on repeat; a failing migration rolls back. Current revision: **4**. V002 adds frozen upstream/historical capture scope and the legacy sufficiency mapping; V003 preserves absent interpretation times and replay audits; V004 retains historical raw task/attempt source keys. Future schema changes require a new numbered migration, tested on empty and already migrated test databases. Do not edit applied migrations. No second migration framework is used.

For M2.2, set the four frozen-root environment variables documented in the [input manifest guide](m2-2-input-manifest.md). Verify all 142 file hashes **before** loading. Then run:

~~~powershell
python -m uv run python -m pulse.phase2_postgres verify
python -m uv run python -m pulse.phase2_postgres load --all
python -m uv run python -m pulse.phase2_postgres reconcile
python -m uv run python -m pulse.phase2_postgres lineage
~~~

`load --all` loads pytest and urllib3 in separate transactions. An identical rerun reports `reused`; changed manifest identity on an existing key is rejected. `reconcile` writes `data/validation/m2-2-golden-reconciliation.json`; `lineage` writes `data/validation/m2-2-lineage.json`. These are deterministic validation artifacts. No external API is called and no analytical snapshot is published. Only `pulse_dev` receives real frozen evidence; integration tests use rolled-back `pulse_test` transactions.

To verify empty rebuild or deliberately destroy development state:

~~~powershell
./infra/postgres/db.ps1 -Action reset -Database pulse_dev
./infra/postgres/db.ps1 -Action reset -Database pulse_test
$env:PULSE_REQUIRE_DB_TESTS = '1'
python -m uv run pytest tests/database -p no:cacheprovider
./infra/postgres/db.ps1 -Action stop
~~~

Reset drops only the explicitly named pulse_dev or pulse_test database in the isolated cluster, recreates it, and reapplies migrations. It destroys rows in that selected local database; do not use it after real evidence loading without a backup. Database tests use fixture captures inside transactions that roll back; they never become source evidence or analytical metrics. In an environment without the local cluster, the general pytest suite skips these database probes. Setting PULSE_REQUIRE_DB_TESTS=1 makes missing database access a failure, which is the required database validation command and recommended future CI behavior when a PostgreSQL service is provisioned.

M2.3 dbt views live in separate dbt-owned schemas. For transformation setup,
clean rebuild and source-preserving validation, use the [dbt runbook](../../../analytics/dbt/README.md).
