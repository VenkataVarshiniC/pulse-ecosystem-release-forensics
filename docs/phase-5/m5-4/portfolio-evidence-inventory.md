# Portfolio evidence inventory after M5.4

This is a map to concrete artifacts, not résumé claims or a finished portfolio package. The [live screenshots](screenshots/README.md) show the implemented product; Power BI images do not exist because M4.2 is deferred.

## Business Analysis

| Proof | Artifact |
| --- | --- |
| Problem, as-is and to-be process | [Business problem](../../phase-3/business-problem.md), [as-is process](../../phase-3/as-is-process.md), [to-be process](../../phase-3/to-be-process.md) |
| Testable but provisional requirements | [Specification](../../phase-3/requirements-specification.md), [traceability](end-to-end-traceability.md), [product acceptance](product-acceptance-results.md) |
| UAT plan and stakeholder boundary | [UAT plan](../../phase-3/uat-plan.md), [Phase 3 closure](../../phase-3/phase-3-closure-assessment.md) |

## Product Analytics

| Proof | Artifact |
| --- | --- |
| Diagnostic findings and limits | [M3 analysis](../../phase-4/m3/analysis-method-and-results.md), [decision memo](../../phase-4/m3/product-analytics-decision-memo.md) |
| Governed metric definitions | [M2.5 SQL catalog](../../phase-4/m2-implementation/m2-5-sql-catalog.md), [metric results](../../phase-4/m2-implementation/m2-5-metric-results.md) |

## Consulting

| Proof | Artifact |
| --- | --- |
| Problem-to-capability synthesis inputs | [M5.4 synthesis inputs](consulting-synthesis-inputs.md), [Phase 3 executive summary](../../phase-3/phase-3-executive-summary.md) |
| Explicit boundaries and decision gates | [Solution boundary](../../phase-3/solution-boundary.md), [M5.4 findings](../milestone-5-4-findings.md) |

## Backend Engineering

| Proof | Artifact |
| --- | --- |
| Versioned scoped read contract | [Endpoint contract](../m5-2/endpoint-contract.md), [FastAPI implementation](../../../src/pulse/api/app.py) |
| Published review safety | [Review write safety](../m5-2/review-write-safety.md), [API tests](../../../tests/test_api_contract.py) |
| Real stack reconciliation | [M5.4 read-only validator](../../../scripts/validate_m5_4_live.py) |

## Frontend / Product

| Proof | Artifact |
| --- | --- |
| Seven operational routes and typed state handling | [Screen implementation](../m5-3/screen-implementation.md), [frontend source](../../../frontend/src/App.tsx) |
| Actual UI, mobile/error examples | [Ten live screenshots](screenshots/README.md), [developer UX log](ux-friction-log.md) |

## Data Engineering / Analytics Engineering

| Proof | Artifact |
| --- | --- |
| Relational/dbt analytical foundation | [Physical/SQL catalog](../../phase-4/m2-implementation/m2-5-sql-catalog.md), [governed versioning](../../phase-4/m2-implementation/m2-5-version-governance.md) |
| Rule/metric replay and publication | [Replay contract](../../phase-4/m4-1/replay-contract.md), [replay comparison](../../phase-4/m4-1/replay-metric-comparison.md) |

## Governance / Quality

| Proof | Artifact |
| --- | --- |
| Typed uncertainty and source provenance | [M5.1 terminology](../m5-1/product-terminology.md), [M5.2 error contract](../m5-2/error-contract.md) |
| Test and audit record | [M5.4 acceptance](product-acceptance-results.md), [findings](../milestone-5-4-findings.md), [traceability](end-to-end-traceability.md) |

M5.5 still needs stakeholder reconciliation, M4.2 manual Power BI work, a final consulting recommendation, README/case study, and a selected portfolio/resume/interview package. This inventory does not claim that any of those deliverables are complete.
