# Phase 0B cross-case comparison

Phase 0B tests the same evidence rules on three contrasting Python releases. The cases are purposive feasibility tests, not a representative sample of Python packages.

| Criterion | NumPy 2.0.0 | Pydantic 2.0 | SQLAlchemy 2.0.0 |
|---|---|---|---|
| Release evidence quality | High: official news, package record, detailed ABI/API notes | High: official announcement, package record, migration guide | High: official changelog, package record, staged migration guide |
| Discovery difficulty | Low to medium because an upstream compatibility tracker seeds downstreams | Medium; downstreams found through repository-specific version and failure searches | High; evidence required separate searches in plausible downstream repositories |
| Adoption observability | Strong in Arrow CI; pandas pre-release support is readiness only | Weak to medium; compatibility releases and failures are visible, ordinary selection is sparsely recorded | Weak to medium; failures show installed use, but broad adoption cannot be enumerated |
| Friction observability | Strong for binary incompatibility with exact versions | Strong for API/import failures and migration tasks | Strong for removed execution APIs with exact versions |
| Remediation observability | Strong for pins, upgrade guidance, CI changes | Strong for version constraints, downstream fixes, dual-version support | Strong for compatibility PRs and downstream releases |
| Recovery observability | Insufficient for a declared cohort in this ledger | Insufficient for a declared cohort in this ledger | Medium for the declared pandas and Flask-SQLAlchemy cohort; not ecosystem-wide |
| Tracker dependency | High for efficient discovery and broad context | None; repository-local evidence used | None; deliberately selected as the tracker-free case |
| Reproducibility | High for named tracker entries; tracker state can change | Medium; search terms and repository choices must be recorded | Medium; repository selection dominates what is found |
| Main biases | Tracker inclusion, compiled-package visibility, public GitHub projects | High-profile framework selection and public issue reporting | Purposive downstream selection and a long 1.4-to-2.0 migration period |

## What generalizes

Across all three cases, primary sources establish release boundaries, and repository-local issues, pull requests, dependency constraints, and downstream release notes reveal migration friction and remediation. The structured ledger and deterministic timeline work without ecosystem-specific machine learning.

Observed adoption remains harder than compatibility readiness. Public evidence also does not provide an unbiased downstream denominator. Recovery becomes defensible only after declaring a cohort, a time window, and a qualifying event.

## What was NumPy-specific

NumPy’s centralized compatibility tracker makes discovery faster and gives broad context that the other cases lack. Its ABI break also creates unusually explicit failure signatures. Those advantages cannot be assumed for pure-Python API migrations or tracker-free ecosystems.

## Decision: PIVOT

The original broad ecosystem-monitoring concept should pivot to **curated, repository-bounded release forensics for declared downstream cohorts**. Phase 0B validates repeatable reconstruction of releases, friction, and remediation, but it does not validate exhaustive discovery, population-level adoption, or ecosystem-wide recovery.

Any Phase 1 proposal must use this narrower scope, publish repository selection rules, preserve negative searches, and prohibit an ecosystem recovery metric unless its denominator is declared. Phase 0B does not begin Phase 1 or authorize a product build.
