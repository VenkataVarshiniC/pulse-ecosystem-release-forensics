# Phase 0 research plan

## Method

1. Record authoritative upstream release and migration sources.
2. Retrieve PyPI version metadata and file upload timestamps.
3. Identify downstream repositories from explicit compatibility trackers where present; otherwise record repository-selection rules and exact repository-local searches.
4. Collect issues, pull requests, commits, manifests, changelogs, and pins that name the target release.
5. Normalize evidence into typed records with source URL, observation time, confidence, and rationale.
6. Order records by event time and evaluate which lifecycle stages have direct evidence.
7. Require human review for repository identity, ambiguous text, and any causal conclusion.

Phase 0A tested this method on NumPy 2.0. Phase 0B repeats it on Pydantic 2.0, a pure-Python API migration, and SQLAlchemy 2.0.0, a case without a centralized compatibility tracker. The cross-case comparison is the final Phase 0 decision gate.

## Search protocol

- Start from upstream documentation and official release artifacts.
- Prefer exact version strings and package names in repository-local search.
- Treat dependency edits and released compatibility statements as stronger than issue prose.
- Record negative results and inaccessible evidence; absence of a public event is not evidence that no event occurred.
- Re-run retrieval with an authenticated token to reduce rate-limit and visibility failures.
- Treat GitHub issue-endpoint records containing a `pull_request` object as pull requests, never as issues.
- Preserve every accepted observation in `data/processed/evidence-ledger.jsonl`; render analysis from that ledger rather than from an uncited narrative.

## Candidate gate

A candidate advances when it has a stable timestamp, documented migration surface, public downstream repositories, and at least plausible adoption, friction, and remediation signals. The configurable scorecard ranks investigation value after this gate.
