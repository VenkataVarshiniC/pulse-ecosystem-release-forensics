# Phase 3 Milestone 3 findings — provisional future state

## Classification

**PARTIAL.** The future-state workflow, boundaries, alternatives, and MoSCoW priorities are evidence-linked and keep missing-data and human-review safeguards. However, the identity of the decision-maker, existence of cross-repository triage, acceptable review burden, trusted evidence threshold, and completion criterion remain untested. These are major solution decisions, so the design is **provisional pending primary-research reconciliation**, not stakeholder-approved or ready to lock as formal requirements. The [Milestone 2 As-Is](milestone-2-findings.md) remains PARTIAL.

## Proposed To-Be workflow

A human declares a consequential target release, bounded repository cohort, window, and rationale. PULSE acquires planned evidence with provenance and task status, reconstructs available historical context, checks source/stage sufficiency, and emits explainable candidates. It may suggest which repositories need deeper review, while an analyst independently accepts, rejects, or requests evidence. Deterministic repository and declared-cohort reports distinguish bounded YES, `NO QUALIFYING EVIDENCE FOUND` under complete rules, and UNKNOWN. A human decides the next action or bounded investigation closure. [The process](to-be-process.md) and [model](to-be-process-model.md) show alternate paths for missing, conflicting, copied-upstream, rejected, and no-candidate cases. Lifecycle categories do not form a required chronology.

## Preferred solution design and alternatives

**Provisional Alternative B — human-review forensic workflow.** It retains the proven Phase 2 collection, provenance, exact-ref observations, sufficiency, review separation, and deterministic reporting, while proposing explainable attention support and evidence-method improvements. [Alternative A](as-is-to-be-comparison.md) (report-only) fits current architecture but may leave UNKNOWN-heavy outputs without a useful next step. Alternative C (highly automated classification) is unjustified by sparse accepted evidence, unknown recall, and absent adoption/recovery inputs. B is conditional on genuine user/decision validation; it is not implementation approval.

## Human versus automation boundary

PULSE may automate bounded source collection, normalization, provenance, explicit sufficiency rules, candidate generation, and report derivation. It provides decision support for source conflicts, missing inputs, evidence comparison, and proposed repository attention. Humans choose scope, review ambiguous candidates, interpret causality, set organizational priority/risk tolerance, and define/approve investigation completion. [The boundary table](human-automation-boundary.md) keeps owner identity and workload unresolved.

## MoSCoW capability summary

| Priority | Capability themes | Evidence and limit |
| --- | --- | --- |
| **Must Have** | CAP-01–08: declared case/cohort; reliable provenance-bearing collection; release-boundary context with unresolved state; separate declaration/resolution/compatibility meanings; provenance-sensitive candidates; independent review; sufficiency/UNKNOWN; deterministic denominator-aware reports. | These preserve Phase 2's validated trust architecture and address its demonstrated gaps; improved evidence coverage is not yet demonstrated. |
| **Should Have** | CAP-09–12: target-version evidence, downstream-release/recovery evidence, explainable attention suggestions, independent detector discovery evaluation. | Need source access, denominators, and stakeholder decision validation. |
| **Could Have** | CAP-13–14: actionable evidence-request/conflict views and analyst collaboration. | Useful only if actual reviewers need them. |
| **Won't Have — current boundary** | CAP-15–16: generic updater, automatic remediation/deployment/business closure, ecosystem/causal claims, and ML/LLM, warehouse, dashboard, or cloud work as prerequisites. | None is supported by the current forensic evidence or Phase 3 scope. |

The full [capability map](capability-prioritization.md) traces each theme to Milestone 2 gaps. These are not FR/NFR or acceptance criteria. The [solution boundary](solution-boundary.md) preserves PULSE as release forensics rather than a dependency manager.

## Major As-Is → To-Be changes

The current public PR artifact path exposes a proposal, diff, optional visible review, and merge/closure; it does not reveal an organizational portfolio decision or recovery. Current PULSE supplies bounded reports but historical declarations in only 2/8 frozen repositories, zero accepted Phase 2 lifecycle events, and no adoption/recovery rate. The [proposed comparison](as-is-to-be-comparison.md) adds explicit human-selected scope, stronger historical and version evidence methods, provenance-sensitive candidates, explainable review attention, and evidence-aware closure—without claiming the sampled PRs used PULSE or that these changes save time.

## Business outcome hypotheses

Potential outcomes are less avoidable evidence reconstruction, clearer missing evidence, stronger traceability and reproducibility, fewer irrelevant reviews, and more useful attention to cases needing investigation. Future measure *names* include investigation completion time, candidate acceptance rate, review burden, evidence coverage, UNKNOWN rate, additional-evidence cases, and analyst agreement. No baseline, target, improvement, or monetary benefit is asserted.

## Stakeholder assumptions and primary-user impact

Unknowns include who triggers and owns a case, whether an owned multi-repository decision exists, what source and provenance threshold is trusted, whether an UNKNOWN finding guides action, how much review work is acceptable, whether CI or resolved version is decisive, and what operational completion means. The all-Dependabot public sample cannot answer those questions; its 6/20 base PRs with visible human interaction cannot establish private work or triage demand. The [primary-user hypothesis](primary-user-hypothesis.md)—a cross-repository dependency/platform engineer—remains **unchanged, plausible, and unvalidated**. It must not be promoted to a validated persona.

## Readiness and next evidence gate

**Not ready to lock formal requirements engineering.** Milestone 3 provides a reviewable design hypothesis, but genuine Google Form/interview evidence and the planned **Milestone 2A stakeholder-evidence reconciliation** must test the decision owner, scope, attention value, trust and review thresholds, and completion criterion. Compare findings against both [Milestone 2 As-Is](milestone-2-findings.md) and this design; record confirmation, refinement, contradiction, or replacement in [change history](requirements-change-history.md). Primary stakeholder reconciliation is still required before final Phase 3 closure. No formal BR/FR/NFR catalogue, RTM, UAT plan, implementation, or Milestone 4 work is included here.
