# PULSE — Ecosystem Release Forensics

PULSE is a post-release intelligence project for reconstructing how major open-source changes propagate through downstream ecosystems:

```text
release → downstream adoption → migration or breakage → remediation → recovery
```

Phase 0 will test whether public evidence can support that reconstruction before any product architecture is built.

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

Start with [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) and the [project charter](docs/project-charter.md). Phase 0 findings will be proposed through a review branch.
