# M3 reproducibility runbook

Run from the repository root with the isolated local PostgreSQL database containing the validated M2 marts:

```powershell
uv run python scripts/analyze_product_patterns.py
uv run ruff check .
uv run pytest -p no:cacheprovider
uv run python scripts/run_dbt.py test
uv run python scripts/fingerprint_dbt_sources.py compare
uv run python scripts/fingerprint_dbt_models.py compare
```

The analysis script performs read-only queries in `analytics/sql/diagnostics/m3_finding_context.sql` and `m3_candidate_origin.sql`; it reads the existing M2.5 baseline/diagnostics/manifest and frozen Phase 3 PR JSONL plus its workflow-metrics derivative. It verifies input hashes, DRAFT states, case/snapshot scope, 20/7 sample separation, candidate/finding counts and core duration median before writing. SQL remains canonical for MET-001–023; Python does not recompute those metric definitions. The script adds descriptive cohort, reason, cross-tab and duration-outlier summaries.

Outputs are [structured JSON](../../../data/analysis/m3-product-analytics-results.json), [funnel CSV](../../../data/analysis/m3-investigation-funnel.csv), [case CSV](../../../data/analysis/m3-case-comparison.csv), [base-duration CSV](../../../data/analysis/m3-base-pr-durations.csv), and four deterministic SVGs in `figures/`. The JSON records all input SHA-256 values and Q1–Q10 result paths. CSVs and SVGs are **validation analytical outputs**, not published BI extracts. A rerun with unchanged inputs must reproduce byte-identical files. Do not modify source JSONL, core tables, snapshot state or M2.5 baseline to make an analysis pass.
