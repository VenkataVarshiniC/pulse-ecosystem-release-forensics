# Phase 4 Milestone 1 — design findings and gate

## Classification and objective

**PARTIAL.** The requested decision-oriented analytics and architecture have reviewable contracts and preserve the Phase 3 implementation gate, but a primary health indicator (investigation outcome coverage) and all product-value success measures depend on an unvalidated stakeholder question/completion set. The classification does **not** mean the product value hypothesis, physical design or future analyses have been validated. The objective is to analyze PULSE's bounded forensic method and a possible investigation workflow without inventing business impact.

## Design outcome

| Area | Milestone 1 result | Critical boundary |
| --- | --- | --- |
| Core questions | Eight [decision domains](analytics-question-framework.md): coverage, investigation path, candidate/review quality, uncertainty, segmentation, effort proxies, reliability and provisional stakeholder value. | No observed user decision or manual effort baseline. |
| KPI hierarchy | [Value hypothesis → health indicators → diagnostics → integrity guardrails](kpi-hierarchy.md). | No invented North Star, target or productivity claim. |
| Metrics | [Versioned contracts](metrics-framework.md) define questions, N/D, grain, dimensions, sources, exclusions, UNKNOWN, interpretation, misuse, measurability and stakeholder dependency. | Adoption, recovery, recall and user-value measures remain unavailable. |
| Funnel | [Declared-member spine and optional candidate branch](investigation-funnel.md). | Candidate generation is not mandatory, and evidence stages need not be chronological. |
| Cohorts and segments | [Frozen release/package/evidence/history/candidate/source cohorts](cohort-framework.md) and [availability-classified dimensions](segmentation-framework.md). | Two Phase 2 convenience cases cannot support ecosystem estimates. |
| PostgreSQL | [ADR](postgresql-architecture.md) prefers relational structured store at demonstrated scale; raw snapshots stay independent; proposed ingestion/core/analytics layers. | Physical schema, deployment and access policy deferred. |
| Analytical model | [Exact grains](analytical-grain.md) and [star/bridge proposal](analytical-data-model.md) separate core records from versioned analytical facts/dimensions. | No flattened fan-out or silently overwritten evidence. |
| dbt | [Sources → staging → intermediate → marts](dbt-design.md), with generic and PULSE-specific tests. | No dbt project, model or executed test. |
| SQL and product analysis | [Question-led joins, CTEs, windows, conditional aggregation and cohort/funnel plans](sql-analysis-plan.md); [bounded analysis program](product-analysis-plan.md). | No production query or claimed analytical finding. |
| Statistics/Python | [Descriptive-first plan](statistical-analysis-plan.md) and preconditions for intervals/comparisons/bootstrap; Python complements canonical SQL. | Tiny dependent convenience sample cannot justify inferential claims or ML. |
| Dashboard | Three [decision-mapped Power BI views](power-bi-dashboard-plan.md), each visual tied to user, metric, grain, filter, drill, interpretation and misuse. | Audience and value unvalidated; no Power BI build. |
| Quality and lineage | [Quality tests](analytics-data-quality.md) for completeness/provenance/validity/grain/replay and [raw-to-mart lineage](data-lineage.md). | Correctly recorded UNKNOWN can be high-quality data despite insufficient evidence. |
| Decision intelligence | [Consulting-style diagnostic and option framework](decision-intelligence-framework.md) links observations to possible next investigations. | No prewritten recommendation or assigned action owner. |

## Evidence and stakeholder gaps

Phase 2 completed core collection for 8/8 frozen members but had exact-ref declaration evidence for only 2/8, only one stronger paired pre-release path, two rejected firings from one artifact, and no accepted events; observed adoption and recovery rates remain unavailable. [Phase 3](../phase-3/phase-3-closure-assessment.md) has no primary stakeholder evidence or approved requirements. The product-value KPI hierarchy, portfolio prioritization, completion, trust dimensions, review-burden measures, dashboard audience/order and success criteria are `PENDING STAKEHOLDER / FUTURE PRODUCT VALIDATION`. Actual source feasibility for target-version and recovery measures is also unresolved.

## Implementation gate

**Phase 4 implementation remains blocked by the Phase 3 HOLD unless a later authorized reconciliation changes that decision.** This milestone produced documentation only. No PostgreSQL installation/database/DDL/loading, dbt project/mart, Power BI file, API, new collector, or Phase 4 Milestone 2 work occurred. A later gate must reconcile real stakeholder evidence, evidence-source feasibility and the changed decision before implementation.
