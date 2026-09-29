# M5.2 validation record

Validation used the existing isolated PostgreSQL 16 cluster (`pulse_dev` for read-only published checks; `pulse_test` for a transaction-rolled-back fixture). Commands were run with the installed `python -m uv` wrapper because `uv.exe` is not on this shell's PATH; this is the project's `uv` tool.

| Check | Result |
|---|---|
| `uv sync --locked --all-groups` | PASS; 72 packages checked against `uv.lock`. |
| `uv run ruff check .` | PASS; all checks passed. |
| Focused API tests | **20 passed** across contract, published-data and isolated review-fixture tests. |
| `uv run pytest -p no:cacheprovider` | **194 passed**, one upstream Starlette TestClient/httpx deprecation warning. No test failure. |
| `uv run python scripts/export_m5_2_openapi.py --check` | PASS; committed JSON exactly matches generated OpenAPI. |
| `uv run python scripts/reconcile_m4_1b.py --check` | PASS; live governed replay matches frozen reconciliation. |
| Uvicorn loopback smoke | PASS; health returned `ok` with database reachable, and investigation list returned two items. Server stopped afterward. |

The API golden tests read **two** published case snapshots, with **2 pytest + 6 urllib3** declared members. They observe **2** replay candidates sharing one artifact, **2 inherited REJECT** reviews, **40** findings (38 UNKNOWN, two bounded NO, zero positive), and **40** sufficiency assessments (38 INSUFFICIENT, two SUFFICIENT). Seven members have zero candidates yet remain in their cohorts. The existing replay reconciliation also reports `false_outcomes=0`, 72 selected artifact links and unchanged metric/mart output. These are bounded validation cases, not ecosystem rates or stakeholder UAT.

Tests exercise health, list/detail, all repository read paths, finding/candidate detail, artifact provenance, keyset pagination, invalid snapshot, wrong-case snapshot, out-of-cohort member, cross-snapshot artifact rejection, literal UNKNOWN/NO, nullable event time, read-only published POST, review-gate failure states, and a valid fixture DRAFT review with idempotent retry, stale/collision/authority/provenance rejection and full rollback. Published candidates are queried again after rejected POSTs. The fixture connects only to `pulse_test`; no test writes to `pulse_dev` or the two published snapshots.

Database regression is covered by the existing database tests in the full pytest run and the read-only replay reconciliation. dbt was **not rerun**: no migration, model, metric registry or analytical materialization changed. Git diff inspection confirms no frozen source capture, publication manifest or Power BI file changed. The sole generated artifact is deterministic OpenAPI JSON. The loopback smoke check supplements in-process HTTP tests; M5.3 should repeat browser-to-API checks during integration.
