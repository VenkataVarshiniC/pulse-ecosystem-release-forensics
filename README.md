# PULSE — Ecosystem Release Forensics

PULSE is a post-release intelligence project for reconstructing how major open-source changes propagate through downstream ecosystems:

```text
release → downstream adoption → migration or breakage → remediation → recovery
```

Phase 0 tests whether public evidence can support that reconstruction. It deliberately stays small: an authenticated GitHub client, a PyPI metadata client, a typed JSONL evidence ledger, a deterministic timeline layer, an auditable human-guided scorecard, and three evidence-backed case studies.

## Development

Requirements: Python 3.12+ and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync --all-groups
copy .env.example .env  # Windows; then add a GitHub token
uv run ruff check .
uv run pytest
uv run python scripts/score_candidates.py
uv run python scripts/render_timelines.py
```

`GITHUB_TOKEN` needs read access to the public repositories being studied. Never commit `.env` or tokens.

Start with [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md), then read the Phase 0 [research plan](docs/phase-0/research-plan.md), [candidate scorecard](docs/phase-0/candidate-releases.md), [feasibility report](docs/phase-0/data-feasibility.md), and [decision](docs/phase-0/phase-0-findings.md).

## Current conclusion

Phase 0 reaches **PIVOT**. Three cases support curated, repository-bounded reconstruction of release, friction, and remediation evidence. They do not validate exhaustive discovery, population-level adoption, or ecosystem-wide recovery. See the [cross-case comparison](docs/phase-0/cross-case-comparison.md) and [findings](docs/phase-0/phase-0-findings.md).
