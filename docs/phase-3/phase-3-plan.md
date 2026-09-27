# Business Analysis & Requirements Engineering

## Purpose and boundary

Phase 3 translates the validated findings, constraints, failures, stakeholder needs, evidence gaps, and business rules discovered during PULSE Phases 0–2 into a traceable business-process and requirements specification for the next version of PULSE. The Phase 2 decision was **PIVOT**: preserve the repository-bounded forensic engine and reconsider the evidence acquisition and decision workflow before expanding the product.

PULSE's product boundary remains: given a software release and a declared set of downstream repositories, reconstruct evidence-backed signals of adoption, migration friction, remediation, and bounded recovery while preserving provenance, confidence, review boundaries, and missing-data semantics. Phases 0–2 tested technical and evidentiary feasibility. Phase 3 investigates who makes the decision, how they currently work, and what the next version must support. The stakeholder and problem statements in Milestone 1 are hypotheses, not research findings.

| Milestone | Planned focus | Gate/output |
| --- | --- | --- |
| 1. Business Context, Stakeholders & Discovery Foundation | Translate the historical record into a charter, provisional stakeholder and problem hypotheses, scope, and a usable discovery protocol. | Evidence-grounded discovery foundation; no interviews claimed. |
| 2. As-Is Process & Root-Cause Analysis | Investigate and model actual release-impact investigation workflows using genuine discovery evidence. | Validated or explicitly uncertain process and root-cause account. |
| 3. To-Be Process & Solution Boundary | Compare workflow options and define where PULSE would help, with human review and evidence limits. | Proposed process and agreed solution boundary. |
| 4. Formal Requirements Engineering | Derive and prioritize business, functional, and nonfunctional requirements from validated needs. | Reviewable requirements with sources and acceptance criteria. |
| 5. Data Requirements & Traceability | Specify information, provenance, completeness, and trace links needed for the workflow. | Traceability from evidence and stakeholder needs to requirements. |
| 6. UAT & BA Validation | Define and perform stakeholder-facing acceptance against the agreed decision workflow. | Documented acceptance evidence and unresolved gaps. |

Only Milestone 1 is active here. Later milestones are a plan, not completed analysis. No As-Is/To-Be model or formal FR/NFR/BR catalogue is created in this milestone.

## Working method

Keep observations, interpretations, and open questions separate. Preserve the Phase 0–2 distinction between missing evidence and evidence of absence; a current dependency declaration does not establish release-time use, and a candidate detector event does not establish friction. Record provenance and review status for every later conclusion. Test the primary-user and business-problem hypotheses with genuine stakeholders before promoting them to validated needs or requirements.

See [the Phase 3 charter](phase-3-charter.md), [Phase 2 inputs](phase-2-ba-inputs.md), and [discovery plan](discovery-plan.md).
