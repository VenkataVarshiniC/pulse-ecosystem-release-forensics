# PULSE dbt transformation layer (M2.3)

This is the single `pulse_analytics` dbt project. It reads the governed, frozen
`pulse_dev.ingestion` and `pulse_dev.core` tables and creates **views** in
`dbt_staging` and `dbt_intermediate`. It does not write to source schemas or
create final marts. `dbt_test__audit` holds failing-test rows when needed;
`dbt_scratch` is the profile's default schema. All four are dbt-owned.

The analytics dependency group pins `dbt-core==1.11.15` and
`dbt-postgres==1.11.0` in `pyproject.toml` and `uv.lock`. The project selects
Python 3.12 through `.python-version` because the pinned dbt stack works there;
the host's Python 3.14 did not initialize dbt. The local cluster is PostgreSQL
17. These versions were selected for the supported Python/PostgreSQL adapter
combination and a reproducible lock, not for a claimed performance improvement.
No external dbt packages are required.

The committed `profiles.yml` uses `PGHOST`, `PGPORT`, `PGUSER` and
`PGPASSWORD`. `scripts/run_dbt.py` reads these from the process environment or
the ignored root `.env`, requires `127.0.0.1:55432` and `pulse_local`, and
connects only to `pulse_dev`. Never commit `.env` or credentials. Initialize
and start the isolated cluster as described in the PostgreSQL
[migration runbook](../../docs/phase-4/m2-implementation/migration-runbook.md),
then load the verified frozen evidence using the M2.2 runbook. Do not reset
`pulse_dev` after loading without preserving its evidence.

From the repository root, with the local cluster running:

```powershell
python -m uv sync --python 3.12 --locked --all-groups
python -m uv run --group analytics python scripts/run_dbt.py debug
python -m uv run --group analytics python scripts/run_dbt.py build
python -m uv run --group analytics python scripts/run_dbt.py test
python -m uv run --group analytics python scripts/run_dbt.py docs generate
python -m uv run --group analytics python scripts/reconcile_dbt.py
```

For a clean transformation rebuild, first record source fingerprints, then
drop **only** dbt-owned schemas and rebuild:

```powershell
python -m uv run --group analytics python scripts/fingerprint_dbt_sources.py record
python -m uv run --group analytics python scripts/reset_dbt_schemas.py --dbt-only
python -m uv run --group analytics python scripts/run_dbt.py build
python -m uv run --group analytics python scripts/run_dbt.py test
python -m uv run --group analytics python scripts/reconcile_dbt.py
python -m uv run --group analytics python scripts/fingerprint_dbt_sources.py compare
```

To compare two business-output builds, record and then compare the ignored
model fingerprints with `scripts/fingerprint_dbt_models.py record` and
`compare`, running `dbt build` between them. The reconciliation JSON is
committed at `data/validation/m2-3-dbt-reconciliation.json`; dbt `target/`,
logs, and fingerprint baselines in `.local/` are ignored.

The source declarations cover the 26 tables used by these models. They omit
`ingestion.load_audit` and `replay_attempt`, and `core.repository_alias` and
`external_evidence_reference`, because M2.3 does not transform their distinct
audit/name/reference purposes. Snapshot input bridges are declared and used.
No source freshness SLA is set: these are intentionally frozen cases, not a
stream. Source event time remains separate from retrieval time. All staged
statuses, NULLs, capture methods, and source IDs remain available. The seven
intermediate views expose evidence diagnostics, not final metrics or published
snapshot results.

The measured local clean build created 19 views and passed 108 tests in
15.95 seconds of dbt elapsed time. The largest view had 72 rows. This is an
engineering baseline for a tiny frozen dataset, not a performance claim.
See the [lineage](../../docs/phase-4/m2-implementation/m2-3-dbt-lineage.md),
[reconciliation](../../docs/phase-4/m2-implementation/m2-3-dbt-reconciliation.md),
and [data-quality record](../../docs/phase-4/m2-implementation/m2-3-data-quality.md).
