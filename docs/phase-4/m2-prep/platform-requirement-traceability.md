# Phase 3 requirement → platform contract

This is technical traceability to the [provisional requirements](../../phase-3/requirements-specification.md) and [rules](../../phase-3/business-rules.md), not stakeholder approval. Requirements still need the Phase 3 reconciliation gate. Test IDs refer to the [dbt matrix](dbt-test-matrix.md); the full Phase 3 RTM remains [here](../../phase-3/requirements-traceability-matrix.md).

| Requirement | Rule | PostgreSQL component | dbt component / test | Metric or output |
| --- | --- | --- | --- | --- |
| BR-001, SR-001, FR-001 | RULE-011 | case version, release, membership | int_case_repository; T01/T17 | Frozen case/cohort denominator |
| BR-002, SR-004, FR-006, FR-009 | RULE-003/006/009/010/013 | assessment, source reason, finding, historical pair | int_stage_sufficiency; T04–06/T09–11 | MET-005/012/013/015; UNKNOWN |
| BR-003, SR-002, FR-003, NFR-001 | RULE-014 | artifact, source, run/task, typed support | int_finding_evidence; T03/T12/T14 | MET-021/source drill-through |
| BR-004, SR-005, FR-011 | RULE-011 | frozen membership only; human priority gated | member mart; T01 | Case-local comparison, no risk score |
| SR-003, FR-007, FR-008 | RULE-004/005/007 | candidate, review event, artifact | int_candidate_terminal_review; T07/08/15 | MET-008–011/022 |
| SR-006, FR-012 | RULE-012 | future disposition/recovery refs gated | future eligibility model; T13 | MET-007 unavailable |
| FR-002, NFR-004 | RULE-001/010 | run/task/attempt and source plan | task staging/member aggregate; T02/T20 | MET-001/016–019 |
| FR-004 | RULE-002/009 | typed observation/historical pair | int_repository_evidence; T05/06 | MET-002, paired breakdown |
| FR-005 | RULE-003 | qualified resolution observation distinct from declaration | observation staging; T04 | MET-003 unavailable |
| FR-010, NFR-002 | RULE-011/013/014 | snapshot manifest and selected versions | int_analysis_snapshot; T17/18 | Reproducible report/MET-020 |
| NFR-003 | RULE-005/014 | unique keys, FK and terminal-review index | T14/15/17/18 | Publication blocker |
| NFR-005 | RULE-014 | provenance refs/access class, least-privilege roles | source test T03; security review | No secret in marts |
| NFR-006 | RULE-014 | case/rule/parser/model/metric versions | snapshot and all marts; T17 | Change impact/replay |

RULE-008 is applied through nonchronological category modeling and T10. Every Phase 3 formal requirement is represented directly or in a grouped row above, but BR-004/SR-005/FR-011, SR-006/FR-012 and user workflow choices are deliberately gated. This map does not relabel a proposed requirement as validated.
