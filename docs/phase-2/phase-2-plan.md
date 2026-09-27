# Phase 2 plan — Collection Reliability & Multi-Cohort Validation

Phase 1 demonstrated reproducible forensic processing, but its committed HTTPX validation snapshots were obtained with connector assistance. They establish downstream replay and review behavior, not unattended collection. Phase 2 must establish collection reliability before using the system to make broader multi-cohort observations. The Phase 1 **PIVOT** decision remains in force.

## Milestone 1 — Collection Reliability Foundation

Harden the existing authenticated GitHub collector and retain auditable per-task collection observations. The scope is pagination for issues, pull requests, commits, and releases; bounded retries and rate-limit handling; explicit task outcomes; immutable run and attempt records; and resume of verified successful tasks. Ordinary CI uses simulated HTTP responses and requires no live token. The acceptance gate asks whether authenticated, paginated tasks can preserve completed pages through transient failures and resume without replacing prior snapshots or duplicating logical evidence. See [collection reliability](collection-reliability.md) for the implemented contract and limitations.

An initial authenticated HTTPX smoke run retrieved 8 of 11 planned task payloads and correctly recorded three candidate file paths as `not_found`. It demonstrated live pagination, provenance, and safe resume, while exposing that optional 404 probes made the run operationally incomplete. Milestone 1 now separates operational completion from current artifact availability and later analytical sufficiency. A fresh authenticated run on 2026-09-26 completed operationally with 8 `succeeded`, 3 optional `not_found`, and 0 required failures. Resume reused all 11 terminal tasks without new requests or changed snapshots. The disposable live artifacts remain outside the repository. Access scope and source completeness still constrain any interpretation of absent evidence.

## Milestone 2 — Historical Dependency Reconstruction

Implemented path-scoped historical commit discovery, exact-ref manifest retrieval, typed refs and pairs, raw collector provenance, and conservative dependency comparison. Live validation on 2026-09-26 automatically reconstructed stable HTTPX declarations in `openai/openai-python` and stable SQLAlchemy optional-dependency declarations in `pandas-dev/pandas`. `pallets-eco/flask-sqlalchemy` exposed incomplete complementary histories across packaging paths; PULSE left its transition unknown. The milestone result is **PARTIAL**. See [historical dependency reconstruction](historical-dependency-reconstruction.md) for anchor rules, raw evidence, live refs, Phase 0 comparison, and limitations.

## Later Phase 2 work — deferred

Later milestones may evaluate detector precision and cohort-level completeness. Each requires its own evidence, tests, and review. No Phase 2 final decision follows from Milestones 1–2. Phase 0 and Phase 1 artifacts and their interpretations remain preserved.
