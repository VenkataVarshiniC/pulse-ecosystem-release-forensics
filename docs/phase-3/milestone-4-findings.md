# Phase 3 Milestone 4 findings — traceable provisional baseline

## Classification

**PARTIAL.** The formal baseline is structurally complete and evidence-linked, but several stakeholder-facing priorities and even the identity/decision of the primary user remain unvalidated. The requirements are **provisional pending primary-research reconciliation**. This classification is driven by missing stakeholder evidence, not by a claim of product implementation or UAT approval. [Milestone 2](milestone-2-findings.md) and [Milestone 3](milestone-3-findings.md) remain PARTIAL.

## Counts and baseline

| Artifact | Count |
| --- | ---: |
| Business requirements (BR) | 4 |
| Stakeholder requirements (SR) | 6 |
| Functional requirements (FR) | 12 |
| Non-functional requirements (NFR) | 6 |
| Business rules | 14 |
| Primary acceptance criteria | 28 |
| Use cases | 6 |

The [specification](requirements-specification.md) uses strength A (direct system), B (integrity), C (public secondary), and D (design hypothesis); **Level E genuine stakeholder evidence is absent**. Status separates existing/partial from proposed; no stakeholder-facing item is labeled stakeholder-validated. The [backlog](requirements-backlog.md) applies provisional MoSCoW and marks proposed functionality **Not Implemented**.

## Must-Have groups

The 22 Must requirements cover bounded case/cohort identity, authenticated and provenance-bearing collection, exact-ref context with unresolved history, distinct declaration/resolved-version/compatibility meanings, tentative candidates with upstream/downstream origin, independent review, stage-specific sufficiency and UNKNOWN, bounded finding/report semantics, and audit/replay/failure/security integrity. “Must” is conditional on validating the PULSE investigation decision, not authorization to build every capability now. No target-version source, recovery source, or improved historical method is claimed as already working.

## Stakeholder-dependent requirements

BR-001/004, SR-001/003/005/006, FR-011/012 and associated case setup, review workload, attention factors, and completion semantics require direct user evidence. SR-002/004 and report presentation also require trust and comprehension testing even though their underlying provenance/UNKNOWN safeguards are integrity-backed. Future Milestone 2A may confirm, modify, reprioritize, split, remove, add, or leave them unresolved. The cross-repository engineer remains a [primary-user hypothesis](primary-user-hypothesis.md), not a validated persona.

## Integrity requirements and rules

BR-002/003, FR-002–010, and NFR-001–005 contain key evidence-correctness safeguards, though some technical acquisition methods are partial or proposed. [Rules 001–014](business-rules.md) preserve optional-versus-required source status, historical and adoption semantics, candidate/review separation, copied-upstream boundaries, nonchronological lifecycle, after-only UNKNOWN, collection-versus-sufficiency, cohort denominator integrity, recovery eligibility, causality limits, and artifact identity. User preferences cannot silently turn missing data into NO, copied upstream text into local friction, or PR merge into recovery.

## Logical data and data quality

The [logical model](logical-data-model.md) centers on Case/Release/Cohort Membership/Repository, Collection Run/Task/Source/Artifact, Historical and Target-Version Observations, Candidate/Review, Sufficiency/Finding, Report, and separate Human Disposition. These are concepts, not physical tables. [Data requirements](data-requirements.md) and the [dictionary](data-dictionary.md) define completeness, original-source provenance/capture method, enum validity, stable identity/consistency, source versus retrieval timestamps, and replay equivalence. Null source data does not become UNKNOWN automatically; an explicit assessment carries UNKNOWN with a reason. No timeliness or throughput SLA is fabricated.

## Source-to-target and traceability coverage

The [mapping](source-to-target-mapping.md) covers PyPI release metadata; GitHub repository metadata, manifests, lockfiles, exact-ref history, issues, PRs, comments/reviews, and commits; plus collector journals and candidate/review outputs. Downstream releases and ordinary CI/runtime resolution are explicitly **not collected/comprehensive in Phase 2** and remain candidate sources. Every mapping records interpretation, rule, quality hazard, and availability.

The [RTM](requirements-traceability-matrix.md) links **28/28 requirements**, including **22/22 Must** end to end, to objective/need, gap, capability, rule, AC, logical entity, and future verification. **14/14 rules** are referenced, **28/28 AC** resolve, and there are **0 orphan requirements, 0 orphan rules, 0 missing AC, and 0 missing structural Must links**. These are document-structure counts, not stakeholder validation or executed tests.

## Quality and change control

The [quality review](requirements-quality-review.md) found no critical structural defects or contradictory evidence semantics. NFR-005 is a singularity watch item because its security boundary combines secret exclusion and source authorization; policy review may split it. Open substantive links are the case owner/portfolio decision, review burden and trusted evidence, older-anchor and resolved-version methods, recovery criterion, source policy/retention, and user-facing presentation. Performance targets are **TBD — requires baseline measurement / stakeholder validation**.

[Change history](requirements-change-history.md) preserves CH-01–07 and adds explicit requirement/rule/AC links for each evidence-driven design correction. Later changes should record the primary source, decision authority, affected IDs, revised AC/RTM/backlog, and any integrity tradeoff rather than rewriting the original evidence.

## Readiness for Milestone 5

The baseline is ready for **future stakeholder reconciliation and validation planning**, not for declaring stakeholder approval or final Phase 3 closure. Genuine Google Form/interview evidence and a Milestone 2A comparison with As-Is/To-Be assumptions remain required. No Phase 3 product implementation, UAT execution result, user signoff, or Milestone 5 work is recorded here.
