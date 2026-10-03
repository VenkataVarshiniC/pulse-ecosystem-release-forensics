# Phase 6 recommendation traceability

## Traceability statuses

- **SUPPORTED** — directly grounded in observed project evidence and existing contracts.
- **PARTIALLY_SUPPORTED** — grounded in a documented gap, but feasibility, transfer, or value remains unresolved.
- **STAKEHOLDER_DEPENDENT** — requires a real user, owner, authority, threshold, or usefulness decision.
- **NOT_SUPPORTED** — current evidence does not justify the recommendation or claim.

## Recommendation trace

| Recommendation or decision | Status | Observed project evidence | Analytical finding / requirement or gap | Risk or tradeoff | Proposed action |
| --- | --- | --- | --- | --- | --- |
| Use a sequenced, evidence-depth-first strategy. | **SUPPORTED** | 8/8 core collection versus 2/40 sufficient findings and 38/40 UNKNOWN; technical presentation is validated. | [Primary gap](capability-gap-analysis.md); Phase 3 GAP-02/03/05; FR-004/005/006/009. | Depth may still fail; sequence delays breadth/features. | Execute NOW gates before workflow or cohort expansion. |
| Freeze the question, population, source policy, and comparison contract before method work. | **SUPPORTED** | Existing frozen cases and immutable publication make outcome-blind comparison possible. | NFR-002/003/006; M4.1B version lineage. | Known outcomes could bias eligibility. | Prespecify contract and prevent published-row overwrite. |
| Test deeper historical reconstruction first. | **SUPPORTED** | 2/8 exact-ref declarations, 1/8 paired pre-release member; fixed-window/cross-file gaps documented. | GAP-02; FR-004; RC-01. | Older/cross-file anchors may remain inaccessible. | Compare an explicit older-anchor/cross-file method on fixed scope. |
| Add explicit source-availability and unresolved-reason semantics. | **SUPPORTED** | 38 UNKNOWN findings and generic insufficiency reasons; required source inputs absent for several questions. | FR-002/006; NFR-004; MET-013/015 partial. | Taxonomy complexity and inconsistent coding. | Version a controlled question/source reason map. |
| Require intact support linkage for future positive findings. | **SUPPORTED** | Current support bridge has zero rows and positive denominator is zero; lineage requirement exists. | BR-003; NFR-001; MET-021 unavailable. | No live positive case exists for validation. | Fail closed on missing links; use a clearly labeled fixture only for mechanics. |
| Run one authorized source trial only when tied to an explicit prerequisite. | **PARTIALLY_SUPPORTED** | Installed-version and recovery inputs are absent. | GAP-03/06; FR-005/012. | Source may be inaccessible or irrelevant; source policy pending. | Approve source, grain, eligibility, provenance, and stop condition before collection. |
| Preserve origin-aware grouping and human review. | **SUPPORTED** | Two candidate firings came from one copied-upstream artifact and both were rejected. | GAP-04; FR-007/008; RULE-004/005. | Two dependent firings do not establish general detector precision. | Keep artifact/member counts separate and review before findings. |
| Defer cohort breadth. | **SUPPORTED** | Current method leaves most questions UNKNOWN; current cohorts are convenience validation sets. | GAP-01/07; Phase 2 PIVOT. | Delays transfer learning and adds no new cases now. | Expand only after evidence-depth gate and outcome-blind selection plan. |
| Defer active review workflow and product expansion. | **STAKEHOLDER_DEPENDENT** | Read-only workflow works; reviewer authority, burden, and value are unvalidated. | SR-003/005; FR-008/011; G8. | May postpone useful workflow learning. | Require a legitimate DRAFT case, reviewer authority, and task acceptance criteria. |
| Reconcile with genuine stakeholders when authorized. | **STAKEHOLDER_DEPENDENT** | Phase 3 closure and M5.4 identify no primary responses. | G8; stakeholder reconciliation framework. | Participants may reject the need or require inaccessible sources. | Preserve response provenance and revise requirements/recommendation based on evidence. |
| Define capability measures with explicit missingness. | **SUPPORTED** | Existing metric governance prevents 0/0 and UNKNOWN from becoming zero outcomes. | FR-010; metric registry; Power BI validation. | Measures could be misused as KPIs. | Keep Phase 6 measures PROPOSED and version them before use. |
| Treat a failed evidence-depth experiment as a valid stop/pivot input. | **SUPPORTED** | Phase 2 and Phase 3 decisions already preserve uncertainty rather than manufacture progress. | NFR-002/004; decision governance. | Sunk-cost pressure may favor continued building. | Report infeasibility and reassess HOLD/PIVOT/STOP. |

## Explicitly unsupported actions or claims

| Action or claim | Status | Reason |
| --- | --- | --- |
| Scale to broad cohorts now because larger N improves validity. | **NOT_SUPPORTED** | Current answerability gap is methodological; larger N can scale UNKNOWN and selection bias. |
| Claim observed adoption from manifests or permissive constraints. | **NOT_SUPPORTED** | Qualified target-version installation/resolution evidence is absent. |
| Claim recovery from PR merge/closure or elapsed time. | **NOT_SUPPORTED** | Recovery source, window, and eligible denominator are absent. |
| Infer no friction from zero candidates or inherited REJECT. | **NOT_SUPPORTED** | Candidate generation/review is not a real-world absence test. |
| Treat two firings from one artifact as two incidents. | **NOT_SUPPORTED** | Shared copied-upstream artifact makes the observations dependent. |
| Claim ecosystem representativeness or population incidence. | **NOT_SUPPORTED** | Two convenience cases and eight members are not an ecosystem sample. |
| Claim validated user demand, value, ROI, or workflow utility. | **NOT_SUPPORTED** | G8 has no stakeholder evidence. |
| Build AI/LLM classification or another major subsystem. | **NOT_SUPPORTED** | No observed gap requires it; transparent evidence qualification remains the priority. |

## Traceability result

Every major Phase 6 recommendation is supported, partially supported with a named feasibility dependency, or explicitly stakeholder-dependent. No recommended action depends on an ecosystem, causal, adoption, recovery, demand, value, or ROI claim. The result is **PASS** for recommendation traceability, with G8 retained as `NOT_YET_VALIDATED`.
