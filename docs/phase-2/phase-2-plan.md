# Phase 2 plan — Collection Reliability & Multi-Cohort Validation

Phase 1 demonstrated reproducible forensic processing, but its committed HTTPX validation snapshots were obtained with connector assistance. They establish downstream replay and review behavior, not unattended collection. Phase 2 must establish collection reliability before using the system to make broader multi-cohort observations. The Phase 1 **PIVOT** decision remains in force.

## Milestone 1 — Collection Reliability Foundation

Harden the existing authenticated GitHub collector and retain auditable per-task collection observations. The scope is pagination for issues, pull requests, commits, and releases; bounded retries and rate-limit handling; explicit task outcomes; immutable run and attempt records; and resume of verified successful tasks. Ordinary CI uses simulated HTTP responses and requires no live token. The acceptance gate asks whether authenticated, paginated tasks can preserve completed pages through transient failures and resume without replacing prior snapshots or duplicating logical evidence. See [collection reliability](collection-reliability.md) for the implemented contract and limitations.

An initial authenticated HTTPX smoke run retrieved 8 of 11 planned task payloads and correctly recorded three candidate file paths as `not_found`. It demonstrated live pagination, provenance, and safe resume, while exposing that optional 404 probes made the run operationally incomplete. Milestone 1 now separates operational completion from current artifact availability and later analytical sufficiency. A fresh authenticated run on 2026-09-26 completed operationally with 8 `succeeded`, 3 optional `not_found`, and 0 required failures. Resume reused all 11 terminal tasks without new requests or changed snapshots. The disposable live artifacts remain outside the repository. Access scope and source completeness still constrain any interpretation of absent evidence.

The Milestone 1 result is **PASS — LIVE VALIDATED** for bounded collection and resume mechanics.

## Milestone 2 — Historical Dependency Reconstruction

Implemented path-scoped historical commit discovery, exact-ref manifest retrieval, typed refs and pairs, raw collector provenance, and conservative dependency comparison. Live validation on 2026-09-26 automatically reconstructed stable HTTPX declarations in `openai/openai-python` and stable SQLAlchemy optional-dependency declarations in `pandas-dev/pandas`. `pallets-eco/flask-sqlalchemy` exposed incomplete complementary histories across packaging paths; PULSE left its transition unknown. The milestone result is **PARTIAL**. See [historical dependency reconstruction](historical-dependency-reconstruction.md) for anchor rules, raw evidence, live refs, Phase 0 comparison, and limitations.

## Milestone 3 — Predeclared validation cohorts

Milestone 3 froze two new Python/PyPI validation cases using predeclared release eligibility, bounded GitHub code-search candidate frames, direct dependency checks, deterministic SHA-256 ranking, and a complete exclusion ledger. The urllib3 cohort has six repositories; the pytest frame yielded only two under the predeclared root-manifest rule. The result is **PARTIAL**. See [cohort selection](cohort-selection.md) and its machine-readable ledger. No release-specific forensic outcome was inspected for selection; full cohort collection began only in Milestone 4.

## Milestone 4 — Detector quality evaluation

Milestone 4 preregistered detector review before live collection, collected both frozen cohorts, reconstructed historical manifest context for all eight repositories, and preserved the unchanged first-pass candidate set. Analyst review rejected both candidates from one bot PR, yielding reviewed-candidate precision **0/2**; pytest emitted none, and seven repositories emitted none. No detector rule was changed. The result is **PARTIAL** because candidate volume and historical context remain too limited for broad rule assessment. See [detector evaluation](detector-evaluation.md) and its machine-readable baseline, review ledger, and metrics.

## Milestone 5 — End-to-end multi-cohort forensics and completeness

Milestone 5 connected the frozen case definitions, verified live collection journals, historical reconstruction, first-pass detector baselines, and independent review ledger into a deterministic report workflow. Both pytest 8.0.0 and urllib3 2.0.0 now have structured and Markdown Release Forensics Reports, an accepted evidence ledger, repository source-availability and stage findings, denominator-aware cohort metrics, and a cross-case validation summary. No new collection or detector tuning was performed. The result is **PASS for end-to-end report integration**: source sufficiency is derived from the machine-readable artifacts, rejected candidates cannot become accepted events, and missing inputs remain visible as UNKNOWN or unavailable metrics. This milestone does not resolve the partial findings from Milestones 2–4 or determine the final Phase 2 decision. See [validation results](validation-results.md) and [evidence sufficiency](evidence-sufficiency.md).

## Milestone 6 — Final Phase 2 Decision

The final decision is **PIVOT**. Live collection and deterministic reporting are validated for the bounded cases, but historical release-boundary context, candidate yield, observed-adoption inputs, and recovery eligibility remain too weak for product scaling. The closure audit tightened negative stage findings so an after-only historical declaration cannot stand in for a release-boundary declaration. See [Phase 2 findings](phase-2-findings.md) for the evidence, limitations, and decision rationale.

## Later work — deferred

Any later work requires separate evidence, design, and authorization. Phase 0 and Phase 1 artifacts and their interpretations remain preserved.
