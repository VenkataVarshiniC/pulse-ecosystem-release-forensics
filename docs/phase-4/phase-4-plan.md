# Phase 4 — Product Analytics & Decision Intelligence

## Objective and boundary

Transform PULSE's bounded forensic evidence, investigation workflow, and provisional requirements into a governed analytical design for evidence coverage, investigation progression, signal quality, uncertainty, repository differences, review behavior, and decision-relevant patterns. The product remains release forensics for **declared downstream cohorts**, not general GitHub, vulnerability, or DevOps analytics. Lifecycle stages are evidence categories, not a required temporal or causal sequence.

This milestone is **design only**. [Phase 3's HOLD](../phase-3/phase-3-closure-assessment.md) blocks product/data-platform implementation until primary stakeholder reconciliation changes the decision. No stakeholder has approved a product user, completion definition, portfolio prioritization, dashboard audience, or value target. Technical integrity rules in [Phase 3](../phase-3/business-rules.md) remain binding.

## Evidence baseline and analytical thesis

[Phase 2](../phase-2/phase-2-findings.md) froze two convenience cases with 2 and 6 repositories. Core planned-source collection completed for 8/8; exact-ref target-package declaration evidence appeared for 2/8, but only one had stronger pre-release paired-path context. Two candidate firings from one bot PR were reviewed and rejected; zero lifecycle events were accepted. Adoption and recovery rates are unavailable. These are **method diagnostics**, not population outcomes or a business-value baseline. Phase 3 has 0 stakeholder-validated formal requirements and a HOLD decision.

The analytical strategy asks, “Can a declared case produce a defensible, traceable repository-level answer, and where does its evidence method stop?” Product value remains a hypothesis until user research tests whether that answer changes a real decision.

## Milestones and gate

| Milestone | Scope | Current authorization |
| --- | --- | --- |
| 1 — Analytics strategy & PostgreSQL architecture | Question tree, metric contracts, funnel/cohorts, logical-to-analytical design, dbt/SQL/statistical/dashboard plans, quality and lineage. | **This milestone: documentation only.** |
| 2 — Analytics data platform | PostgreSQL, ingestion, dbt, tests, marts, SQL. | Future; blocked by Phase 3 HOLD. |
| 3 — Product and statistical analysis | Run funnel, cohort, signal, uncertainty, time and reliability analyses on validated data. | Future; blocked. |
| 4 — Decision intelligence & Power BI | Build decision views and evidence-backed recommendations. | Future; blocked. |

Primary research may occur independently. A later decision must reconcile [Phase 3 stakeholder questions](../phase-3/stakeholder-reconciliation-framework.md) before prioritizing any build. This design does not authorize Milestones 2–4.

## Design navigation

[Questions](analytics-question-framework.md) → [metric contracts](metrics-framework.md) → [KPI hierarchy](kpi-hierarchy.md), [funnel](investigation-funnel.md), [cohorts](cohort-framework.md), [segments](segmentation-framework.md) → [PostgreSQL ADR](postgresql-architecture.md), [grains](analytical-grain.md), [model](analytical-data-model.md), [dbt](dbt-design.md), [lineage](data-lineage.md), [quality](analytics-data-quality.md) → [SQL](sql-analysis-plan.md), [product analyses](product-analysis-plan.md), [statistics/Python](statistical-analysis-plan.md), [Power BI](power-bi-dashboard-plan.md), [decision intelligence](decision-intelligence-framework.md), and [milestone findings](milestone-1-findings.md).
