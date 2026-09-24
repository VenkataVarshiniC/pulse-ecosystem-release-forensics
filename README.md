# PULSE — Ecosystem Release Forensics

PULSE is a post-release intelligence project for reconstructing how major open-source changes propagate through downstream ecosystems:

```text
release → downstream adoption → migration or breakage → remediation → recovery
```

Phase 0 tests whether public evidence can support that reconstruction. It deliberately stays small: an authenticated GitHub client, a PyPI metadata client, typed evidence records, a configurable human-guided scorecard, and one evidence-backed NumPy 2.0 case study.

## Development

Requirements: Python 3.12+ and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync --all-groups
copy .env.example .env  # Windows; then add a GitHub token
uv run ruff check .
uv run pytest
uv run python scripts/score_candidates.py
```

`GITHUB_TOKEN` needs read access to the public repositories being studied. Never commit `.env` or tokens.

Start with [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md), then read the Phase 0 [research plan](docs/phase-0/research-plan.md), [candidate scorecard](docs/phase-0/candidate-releases.md), [feasibility report](docs/phase-0/data-feasibility.md), and [decision](docs/phase-0/phase-0-findings.md).

## Current conclusion

Phase 0 reaches a qualified **GO** for curated, evidence-backed release case studies. Public evidence supports the lifecycle for NumPy 2.0, but repository discovery and causal attribution remain human-reviewed steps. See the findings for the limits of that claim.
