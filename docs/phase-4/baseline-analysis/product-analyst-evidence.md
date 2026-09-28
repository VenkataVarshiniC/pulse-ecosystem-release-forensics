# Internal Product Analyst evidence inventory — no résumé claims

| Capability demonstrated | Reviewable artifact and observed work | Boundary |
| --- | --- | --- |
| Business-question framing | [Decision tree](../analytics-question-framework.md) and [decision insights](decision-insights.md). | Stakeholder decision hypothesis remains unvalidated. |
| KPI and metric contracts | [KPI hierarchy](../kpi-hierarchy.md), 23 [definitions](../metrics-framework.md), [computability audit](metric-computability.md). | Technical computability is not product value. |
| Numerator/denominator discipline | [Machine baseline](baseline-metrics.json) exposes N/D, unavailable reasons and 0/0 separately. | Convenience cohorts remain case-specific. |
| Investigation funnel | [Split-path baseline](funnel-baseline.md) keeps optional candidate branch separate. | Not user conversion. |
| Cohort/segmentation | [Feasibility audit](cohort-feasibility.md) distinguishes constructible from invalid adoption/recovery cohorts. | Sparse/invariant dimensions have little explanatory power. |
| Missing-data semantics | [UNKNOWN audit](unknown-analysis.md) separates correct unresolved evidence from missing analytical rows. | Stage-specific reason attribution is incomplete. |
| Data quality and grain | [Quality audit](data-quality-audit.md), [grain validation](grain-validation.md), [model readiness](model-feasibility.md). | Multi-run and positive-finding links need design review. |
| Source feasibility | [Gap matrix](source-gap-matrix.md) compares public source options and claim boundaries. | No new outcome collection or feasibility experiment. |
| Descriptive analysis | [Case findings](descriptive-findings.md), [candidate review](candidate-review-analysis.md), [reliability](collection-reliability-analysis.md). | No population/business effect. |
| Statistical judgment | [Readiness audit](statistical-readiness.md) declines unjustified inference. | No significant difference or ML claim. |
| Dashboard decision mapping | [Visual audit](dashboard-readiness.md) blocks misleading visuals before build. | Audience and product use unvalidated. |

The reproducible helper is explicitly **analysis-only/non-production**. It reads frozen files, validates identities/hashes and emits descriptive results; it is not an ETL platform, collector, or product API.
