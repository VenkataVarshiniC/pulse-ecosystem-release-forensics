# Stakeholder validation Wave 1 synthesis

## 1. Wave scope

Wave 1 is a frozen interim convenience sample of 9 responses collected by 2026-10-04. Additional responses are expected. Raw identity and contact data remain local and ignored.

## 2. Sample

Seven respondents reported direct dependency-upgrade work. Roles span software, full-stack, data/AI, and security/supply-chain engineering. Experience is evenly split among less than one, one to two, and three to five years. Five reported a recent multi-repository scope.

## 3. Strongest supported findings

Affected-repository identification, historical/version evidence, CI/test/runtime evidence, explanation, provenance, and qualified automation receive the strongest direct support. Traceability averaged 4.11/5, and affected-repository identification was most useful for 5/9.

## 4. Mixed findings

Respondents differ on insufficient-evidence output, human-review need, current-tool adequacy, centralization, and desired automation. Historical reconstruction is supported but was the top capability for only 1/9.

## 5. Contradictions

The hypothesis of one stable final decision owner is contradicted by five owner categories. Two respondents say existing tools are sufficient, two would not rely on automated conclusions, two say results may not affect decisions, and one reports insufficient problem frequency.

## 6. Unanswered questions

Actual upgrade frequency, time spent, decision delay, cost, acceptable false-positive volume, PULSE comprehension, integration path, private-source authorization, installed-version source, recovery definition, and observed decision impact remain unresolved.

## 7. Requirements implications

Strengthen affected-set scope, provenance, missing-prerequisite display, historical/version/eligible CI evidence, completion criteria, security/privacy, and explainable triage. Reword singular owner/reviewer assumptions. Defer recovery. Add workflow integration only as a candidate pending observation.

## 8. Persona implications

The engineer-investigator is partially confirmed; a dedicated platform/dependency manager is not. Investigator, reviewer, repository owner, and final decision owner must remain separable.

## 9. Trust and uncertainty implications

Explicit provenance and missingness align with respondent preferences. UNKNOWN semantics must remain intact. A separately governed presentation study may test labeled tentative guidance without changing the finding state.

## 10. Value signal

Wave 1 shows **SUPPORTED INTEREST**, not validated demand. Usefulness averaged 3.89/5, while trust and integration barriers each reached 5/9.

## 11. Impact on Phase 6 recommendation

The sequenced evidence-depth-first strategy is `PARTIALLY_SUPPORTED`: evidence depth, history, uncertainty, and provenance align; automation, review burden, integration, and frequency remain constrained.

## 12. Impact on Phase 7 result

`GO_BOUNDED` is `PARTIALLY_SUPPORTED`. Phase 7’s method aligns with evidence preferences but has not been shown to change a stakeholder decision and should remain experimental.

## 13. G8 assessment

G8 becomes `PARTIALLY_VALIDATED`. Genuine evidence now supports core needs, but sample size/status, mixed counter-evidence, incomplete persona/owner validation, and absent task-based use block a stronger gate.

## 14. What additional responses should test

Recruit more experienced upgrade owners, platform/dependency engineers, technical leads, managers, and security reviewers. Test recent incident frequency, actual repository selection, decision authority, evidence that changed action, acceptable review volume, integration constraints, private-source policy, completion/recovery criteria, and whether a PULSE case changes next action.

## 15. What should not change yet

Do not weaken UNKNOWN or bounded-NO rules, replace Phase 7’s baseline, infer adoption/recovery, broaden evidence collection, automate remediation, claim ROI/demand, collapse roles, begin Phase 8, or rewrite the frozen Phase 3 requirements in place.
