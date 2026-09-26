# Phase 2 plan — Collection Reliability & Multi-Cohort Validation

Phase 1 demonstrated reproducible forensic processing, but its committed HTTPX validation snapshots were obtained with connector assistance. They establish downstream replay and review behavior, not unattended collection. Phase 2 must establish collection reliability before using the system to make broader multi-cohort observations. The Phase 1 **PIVOT** decision remains in force.

## Milestone 1 — Collection Reliability Foundation

Harden the existing authenticated GitHub collector and retain auditable per-task collection observations. The scope is pagination for issues, pull requests, commits, and releases; bounded retries and rate-limit handling; explicit task outcomes; immutable run and attempt records; and resume of verified successful tasks. Ordinary CI uses simulated HTTP responses and requires no live token. The acceptance gate asks whether authenticated, paginated tasks can preserve completed pages through transient failures and resume without replacing prior snapshots or duplicating logical evidence. See [collection reliability](collection-reliability.md) for the implemented contract and limitations.

The milestone makes no claim that an unattended HTTPX run or a full downstream cohort has succeeded. A real network run, its exact access scope, and the completeness of each source must be evaluated separately before interpreting absence of evidence.

## Later Phase 2 work — deferred

Later milestones may validate unattended collection against bounded public cohorts, investigate historical ref pairing, and evaluate detector precision and cohort-level completeness. Each requires its own evidence, tests, and review. No Phase 2 final decision follows from Milestone 1 alone. Phase 0 and Phase 1 artifacts and their interpretations remain preserved.
