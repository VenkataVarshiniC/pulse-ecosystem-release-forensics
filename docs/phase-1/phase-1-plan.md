# Phase 1 plan

## Objective

Turn Phase 0's researcher-driven method into a repeatable, repository-bounded evidence pipeline while preserving its ledgers and conclusions unchanged.

## Milestones

1. Model release cases, explicit or rule-based cohorts, collection observations, and review state.
2. Plan and run modular GitHub and PyPI collection into immutable raw envelopes and a manifest that retains failures.
3. Parse high-value Python dependency formats and classify target-version constraint transitions.
4. Detect explainable adoption, friction, remediation, and recovery candidates without assigning keyword-only high confidence.
5. Convert accepted evidence into timelines, three-state repository findings, cohort metrics, and missing-evidence records.
6. Generate deterministic JSON and Markdown reports through a CLI.
7. Validate the unchanged architecture on HTTPX 0.28.0 and publish a decision.

## Acceptance checks

Ruff and the full test suite must pass. The SQLAlchemy Phase 0 case must load and produce a stable collection plan, the original Phase 0 timelines must still render, and `scripts/reproduce_validation.py` must recreate the committed HTTPX ledger, forensics JSON, manifest, and report byte for byte.
