# Provisional requirements traceability matrix

This matrix links each formal requirement to its motivating objective, hypothesized need, current gap, [To-Be capability](capability-prioritization.md), [rule](business-rules.md), [acceptance criterion](acceptance-criteria.md), logical [data entity](data-requirements.md), and **future** verification. There is no executed UAT or stakeholder-approved need. `OB-01–06` are trace aliases for the six rows, in order, of [business objectives](business-objectives.md): reconstruction, traceability, uncertainty, repository attention, candidate relevance, reproducibility. `N-01–08` retain the IDs in [needs hypotheses](stakeholder-needs-hypotheses.md). In a compact slash list, the prefix applies to each number: `RULE-003/010` means `RULE-003` and `RULE-010`, and the same convention applies to `OB`, `N`, `GAP`, and `CAP`. All future checks below are planned, not run.

| Objective → need/hypothesis | As-Is gap → To-Be capability | Requirement | Rule(s) | Acceptance criterion | Logical data entity | Future verification / current status |
| --- | --- | --- | --- | --- | --- | --- |
| OB-01 → N-01 | GAP-01 → CAP-01 | BR-001 | RULE-011 | AC-BR-001-01 | Case, Membership | Case-scope walkthrough; **Must, stakeholder-dependent**. |
| OB-03 → N-04 | GAP-05 → CAP-07 | BR-002 | RULE-003/010/013 | AC-BR-002-01 | Assessment, Finding | Incomplete-case comprehension/replay; **Must, integrity/system**. |
| OB-02 → N-03/N-08 | GAP-04/08 → CAP-02/06/08 | BR-003 | RULE-004/014 | AC-BR-003-01 | Artifact, Review, Finding | Source-to-finding audit; **Must, integrity/system**. |
| OB-04 → N-01/N-07 | GAP-07 → CAP-11 | BR-004 | RULE-011 | AC-BR-004-01 | Membership, Report | Portfolio decision interview; **Should, provisional**. |
| OB-01 → N-01 | GAP-01 → CAP-01 | SR-001 | RULE-011 | AC-SR-001-01 | Case, Membership | Case setup walkthrough; **Must, provisional role**. |
| OB-02 → N-03/N-08 | GAP-08 → CAP-02/08 | SR-002 | RULE-014 | AC-SR-002-01 | Source, Artifact | Provenance inspection; **Must, integrity**. |
| OB-05 → N-05 | GAP-04 → CAP-06 | SR-003 | RULE-004/005 | AC-SR-003-01 | Candidate, Review | Analyst review exercise; **Must, role unvalidated**. |
| OB-03 → N-04 | GAP-05 → CAP-07 | SR-004 | RULE-010 | AC-SR-004-01 | Assessment, Finding | UNKNOWN comprehension exercise; **Must, integrity**. |
| OB-04 → N-07 | GAP-07 → CAP-11 | SR-005 | RULE-011 | AC-SR-005-01 | Membership, Report | Triage exercise; **Should, provisional**. |
| OB-03 → N-06 | GAP-06 → CAP-10 | SR-006 | RULE-012 | AC-SR-006-01 | Finding, Disposition | Real completion reconstruction; **Should, provisional**. |
| OB-01 → N-01 | GAP-01 → CAP-01 | FR-001 | RULE-011 | AC-FR-001-01 | Case, Membership | Invalid/valid case tests; **Must, existing case basis**. |
| OB-01 → N-02/N-08 | GAP-05 → CAP-02 | FR-002 | RULE-001/010 | AC-FR-002-01 | Run, Task | Optional 404/required failure replay; **Must, existing**. |
| OB-02/06 → N-08 | GAP-08 → CAP-02 | FR-003 | RULE-014 | AC-FR-003-01 | Source, Task, Artifact | Tamper/resume replay; **Must, existing**. |
| OB-01 → N-02 | GAP-02 → CAP-03 | FR-004 | RULE-002/009 | AC-FR-004-01 | Historical Observation | Before/after-only cases; **Must, partial**. |
| OB-03 → N-02 | GAP-03 → CAP-04 | FR-005 | RULE-003 | AC-FR-005-01 | Target-Version Observation, Finding | Declaration-only counterexample; **Must, proposed method**. |
| OB-03 → N-04 | GAP-05 → CAP-07 | FR-006 | RULE-009/010 | AC-FR-006-01 | Assessment | Incomplete/conflict tests; **Must, partial**. |
| OB-05 → N-05 | GAP-04 → CAP-05 | FR-007 | RULE-004/006/007 | AC-FR-007-01 | Artifact, Candidate | Copied-note fixture; **Must, partial**. |
| OB-02/05 → N-03/N-05 | GAP-04 → CAP-06 | FR-008 | RULE-004/005/014 | AC-FR-008-01 | Candidate, Review | Three-decision review exercise; **Must, partial**. |
| OB-03 → N-04 | GAP-05/06 → CAP-07 | FR-009 | RULE-003/005/006/008/012/013 | AC-FR-009-01 | Assessment, Finding | Zero-candidate/unknown replay; **Must, existing bounded**. |
| OB-02/06 → N-03/N-08 | GAP-08 → CAP-08 | FR-010 | RULE-011/012/013 | AC-FR-010-01 | Report, Finding | Same-input report replay; **Must, partial**. |
| OB-04 → N-07 | GAP-07 → CAP-11 | FR-011 | RULE-011 | AC-FR-011-01 | Membership, Report | Owner triage exercise; **Should, provisional**. |
| OB-03 → N-06 | GAP-06 → CAP-10 | FR-012 | RULE-012 | AC-FR-012-01 | Finding, Disposition | Eligibility/PR merge counterexample; **Should, provisional**. |
| OB-02 → N-08 | GAP-08 → CAP-02/08 | NFR-001 | RULE-014 | AC-NFR-001-01 | Case, Artifact, Review, Finding | Chain audit; **Must, partial**. |
| OB-06 → N-08 | GAP-08 → CAP-08 | NFR-002 | RULE-014 | AC-NFR-002-01 | Report, Run | Frozen replay comparison; **Must, existing**. |
| OB-02 → N-03 | GAP-04/08 → CAP-06/07 | NFR-003 | RULE-005/014 | AC-NFR-003-01 | Candidate, Review, Finding | Duplicate/mismatch test; **Must, partial**. |
| OB-03 → N-04 | GAP-05 → CAP-02/07 | NFR-004 | RULE-001/010 | AC-NFR-004-01 | Task, Assessment | Mixed-status test; **Must, existing**. |
| OB-02 → N-08 | GAP-08 → CAP-02 | NFR-005 | RULE-014 | AC-NFR-005-01 | Source, Artifact | Credential/source-permission inspection; **Must, proposed safeguard**. |
| OB-06 → N-08 | GAP-08 → CAP-02/05/08 | NFR-006 | RULE-014 | AC-NFR-006-01 | Candidate, Report | Rule-change impact exercise; **Should, proposed**. |

**Trace coverage target and current audit:** every one of the 28 formal requirements has a source/gap/capability, at least one rule, exactly one primary AC reference, a logical entity, and a planned verification. All **22 Must** rows are linked end to end. All 14 rules are referenced by at least one row. There are no Level E sources or completed UAT links. The substantive open links are validation of N-01–08 and the organizational decision/role; these are explicitly pending rather than silently treated as trace completion in business terms. The [quality review](requirements-quality-review.md) audits structural coverage and unresolved evidence separately.
