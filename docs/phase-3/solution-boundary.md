# Provisional PULSE solution boundary

**Product thesis:** Given a software release and a declared set of downstream repositories, PULSE reconstructs evidence-backed signals of adoption, migration friction, remediation, and bounded recovery while preserving provenance, confidence, review boundaries, and missing-data semantics. It is release-forensics investigation support, pending stakeholder validation of the actual decision and user. [Phase 2's PIVOT](../phase-2/phase-2-findings.md) preserves the proven audit path while challenging evidence acquisition; [Milestone 2](milestone-2-findings.md) has not validated an organizational workflow.

## PULSE must own within a selected investigation case

| Responsibility | Why it belongs in the boundary |
| --- | --- |
| Typed target-release case, declared repository cohort/window and denominator | A bounded case prevents silent ecosystem-wide scope or population claims; Phase 2 froze cases and exposed cohort limits. |
| Authenticated, bounded planned-source collection with resumability and required/optional task semantics | Phase 2 validated live pagination, retry/failure states, optional 404 handling, and verified resume. A collection failure remains visible. |
| Immutable raw evidence, capture-method and query provenance, artifact identity | Reviewable claims must point to what was actually retrieved and how; connector-assisted Phase 1 evidence is distinguishable from unattended Phase 2 collection. |
| Exact-ref historical observations where possible, with unresolved state | Point-in-time evidence matters, but current path-scoped coverage cannot be overclaimed. Preserve typed context while improving acquisition method when justified. |
| Explicit source/stage sufficiency, conflict and missing-data states | UNKNOWN must not turn into NO; negative findings need a bounded completeness rule and denominator. |
| Candidate generation distinct from acceptance and independent human review | The two rejected Phase 2 firings show why copied upstream text cannot become accepted downstream events automatically. |
| Deterministic repository/cohort forensic reporting with uncertainty and traceable rationale | Phase 2 reproduced audit-ready reports; users must be able to see gaps, rejected evidence, and what each finding means. |

These are core *solution responsibilities*, not claims that all are currently complete at useful coverage or validated as stakeholder needs.

## PULSE may support, subject to evidence and stakeholder value

| Proposed support | Evidence condition / current status |
| --- | --- |
| Explainable repository-attention suggestions and cohort comparison | Design hypothesis; no public PR establishes portfolio triage or its owner. |
| Downstream-release, resolved-version, and relevant CI/runtime evidence | Candidate acquisition improvements for adoption/recovery questions; access, coverage, and decision utility unknown. |
| Cross-source conflict highlighting and upstream/downstream text separation | Phase 2 false-positive mechanism supports investigation; exact method and recall need validation. |
| Analyst collaboration and review handoff | Independent review exists, but multi-user workflow, authority, and burden are not established. |
| Evidence-request checklist for UNKNOWN cases | Could make gaps actionable, but UNKNOWN's usefulness is untested. |

## PULSE explicitly does not own

- Creating routine dependency-update PRs or replacing Dependabot/Renovate.
- Generating code remediations, choosing an upgrade, running generic CI, or deploying to production.
- General vulnerability-management scanning; a security signal may be an investigation trigger only if a declared release case is in scope.
- Inferring ecosystem-wide impact, population adoption, or causal effects from bounded convenience cohorts.
- Treating current declarations, PR merge, passing tests, or elapsed time as installed target-version use, migration completion, or production recovery.
- Automatically deciding business priority, accepting ambiguous evidence, or certifying operational risk/closure.
- ML/LLM classification, a warehouse/dashboard, or cloud deployment as a Milestone 3 deliverable.

The boundary separates a future **case investigation** from an update mechanism. A future stakeholder may reject cross-repository triage or require different evidence; in that event the capability set must be revised before formal requirements. See [prioritization](capability-prioritization.md) and [human ownership](human-automation-boundary.md).
