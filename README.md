# PULSE — Ecosystem Release Forensics

PULSE is a repository-bounded release-forensics system. It reconstructs how a software dependency release affects a declared cohort of downstream repositories using auditable public evidence:

```text
release → downstream adoption → migration or breakage → remediation → recovery
```

Phase 0 established feasibility and narrowed the product claim. Phase 1 adds declarative cases, deterministic collection plans, modular GitHub and PyPI collectors, immutable raw snapshots, dependency parsers, transparent candidate rules, explicit human review, repository summaries, defensible cohort metrics, and generated reports.

Lifecycle stages are evidence categories, not a required chronological or causal sequence. Adoption evidence coverage measures accepted evidence, not adoption prevalence; unknown findings remain unknown.

## Development

Requirements: Python 3.12+ and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync --all-groups
copy .env.example .env  # Windows; then add a GitHub token
uv run ruff check .
uv run pytest -p no:cacheprovider
uv run python scripts/score_candidates.py
uv run python scripts/render_timelines.py
uv run pulse plan cases/sqlalchemy-2.0.0.yaml
uv run python scripts/reproduce_validation.py
```

`GITHUB_TOKEN` needs read access to the public repositories being studied. Never commit `.env` or tokens.

GitHub Actions runs `uv sync --locked --all-groups`, Ruff, and the full pytest suite on pull requests and pushes to `main`, using Python 3.12 and the [official uv action](https://docs.astral.sh/uv/guides/integration/github/). CI uses local fixtures and does not require a GitHub collection token or validate live collection.

For live collection, set `GITHUB_TOKEN`, then run:

```bash
uv run pulse collect cases/httpx-0.28.0.yaml
uv run pulse analyze cases/httpx-0.28.0.yaml data/interim/httpx-0.28.0/review-ledger.jsonl
uv run pulse report data/processed/httpx-0.28.0/forensics.json docs/generated/httpx-0.28.0-forensics.md
```

`collect` records every planned task as succeeded or failed and returns a nonzero status for an incomplete run. Raw snapshot filenames are append-only and include the stable task ID and retrieval time. `analyze` consumes reviewed evidence; it never promotes candidates implicitly.

Raw envelopes require `capture_method` (`collector`, `connector_assisted`, or `fixture`). The committed HTTPX validation snapshots are connector-assisted; replaying them does not establish unattended collection. That remains unvalidated.

Start with [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md), the Phase 0 [decision](docs/phase-0/phase-0-findings.md), and the Phase 1 [methodology](docs/phase-1/methodology.md), [validation case](docs/phase-1/validation-case.md), and [findings](docs/phase-1/phase-1-findings.md).

## Current conclusion

Phase 1 reaches **PIVOT**. The forensic pipeline and report are reproducible from preserved evidence, while comprehensive live discovery and collection still require hardening before analytical scale-up. The system makes no ecosystem-wide claim.
