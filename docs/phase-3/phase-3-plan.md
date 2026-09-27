# Business Analysis & Requirements Engineering

## Purpose and boundary

Phase 3 translates the validated findings, constraints, failures, stakeholder needs, evidence gaps, and business rules discovered during PULSE Phases 0–2 into a traceable business-process and requirements specification for the next version of PULSE. The Phase 2 decision was **PIVOT**: preserve the repository-bounded forensic engine and reconsider the evidence acquisition and decision workflow before expanding the product.

PULSE's product boundary remains: given a software release and a declared set of downstream repositories, reconstruct evidence-backed signals of adoption, migration friction, remediation, and bounded recovery while preserving provenance, confidence, review boundaries, and missing-data semantics. Phases 0–2 tested technical and evidentiary feasibility. Phase 3 investigates who makes the decision, how they currently work, and what the next version must support. The stakeholder and problem statements in Milestone 1 are hypotheses, not research findings.

| Milestone | Planned focus | Gate/output |
| --- | --- | --- |
| 1. Business Context, Stakeholders & Discovery Foundation | Translate the historical record into a charter, provisional stakeholder and problem hypotheses, scope, and a usable discovery protocol. | Evidence-grounded discovery foundation; no interviews claimed. |
| 2. As-Is Process & Root-Cause Analysis | Investigate and model actual release-impact investigation workflows using genuine discovery evidence. | Validated or explicitly uncertain process and root-cause account. |
| 3. To-Be Process & Solution Boundary | Compare workflow options and define where PULSE would help, with human review and evidence limits. | Provisional process and solution boundary pending stakeholder reconciliation. |
| 4. Formal Requirements Engineering | Derive and prioritize provisional business, stakeholder, functional, and nonfunctional requirements from existing evidence and explicit hypotheses. | Traceable baseline and acceptance criteria pending stakeholder reconciliation. |
| 5. Data Requirements & Traceability | Specify information, provenance, completeness, and trace links needed for the workflow. | Traceability from evidence and stakeholder needs to requirements. |
| 6. UAT & BA Validation | Define and perform stakeholder-facing acceptance against the agreed decision workflow. | Documented acceptance evidence and unresolved gaps. |

Milestone 1 and the bounded public-research Milestone 1A are complete. [Milestone 2 findings](milestone-2-findings.md) classify the provisional As-Is and root-cause analysis as **PARTIAL** because stakeholder evidence is pending. [Milestone 3 findings](milestone-3-findings.md) classify the provisional To-Be and capability prioritization as **PARTIAL** for the same unresolved decision ownership and completion questions. [Milestone 4 findings](milestone-4-findings.md) classify the traceable formal requirements baseline as **PARTIAL** pending primary research. A future Milestone 2A reconciliation is proposed, not performed. Milestones 5–6 remain planning only; no product implementation or UAT execution has begun.

## Working method

Keep observations, interpretations, and open questions separate. Preserve the Phase 0–2 distinction between missing evidence and evidence of absence; a current dependency declaration does not establish release-time use, and a candidate detector event does not establish friction. Record provenance and review status for every later conclusion. Test the primary-user and business-problem hypotheses with genuine stakeholders before promoting them to validated needs or requirements.

See [the Phase 3 charter](phase-3-charter.md), [Phase 2 inputs](phase-2-ba-inputs.md), and [discovery plan](discovery-plan.md).
