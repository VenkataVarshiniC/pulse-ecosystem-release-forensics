# Milestone 5 validation coverage and rule assessment

These denominators answer different questions and must **not** be merged into a single completion percentage. [The matrix](requirement-validation-matrix.md) holds full-requirement results; [UAT cases](uat-test-cases.md) hold narrower scenario results. Current full pytest: **134 passed**. Frozen Phase 2 replay regenerated both reports and summary with **no Git diff**. Neither is stakeholder UAT.

| Coverage dimension | Result | Boundary |
| --- | --- | --- |
| Structural AC | **28/28** formal requirements have at least one AC; [M4 audit](requirements-quality-review.md). | AC presence is not implementation. |
| Structural RTM | **28/28** requirements, **22/22 Must** end-to-end, **14/14** rules referenced; [RTM](requirements-traceability-matrix.md). | Stakeholder need links are hypotheses. |
| Validation-mode partition | 10 current-system-testable; 5 current-system-partially-testable; 2 document-review-testable; 3 future-implementation-required; 8 stakeholder-validation-required. | 28 total, mutually exclusive primary modes. |
| Full-requirement result partition | **10 PASS, 0 FAIL, 5 BLOCKED, 5 NOT_IMPLEMENTED, 8 PENDING_STAKEHOLDER**. | A narrow passing guard may coexist with a blocked whole requirement. |
| Current implementation/evidence | 10 fully testable bounded requirements have current acceptance evidence; 5 have only partial current evidence; 5 are wholly proposed/future; 8 require user validation though some underlying technical behavior exists. | This partition is validation maturity, not a product-completion score. |
| Current-system acceptance cases | **15 PASS, 0 FAIL, 2 BLOCKED** among existing/partial scenarios. | 15 narrow PASS cases include guards for future requirements, not whole-function implementation. |
| Future-state case design | **8 NOT_IMPLEMENTED** cases and **5 PENDING_STAKEHOLDER** cases specified. | No future case was executed or passed. |
| Wholly unimplemented formal requirements with future scenario | **5/5** (FR-005/007/011/012, NFR-006). | Their AC/requirements remain NOT_IMPLEMENTED. |
| Partially testable formal requirements with blocker and planned scenario | **5/5** (BR-003, FR-006/010, NFR-001/005). | Missing accepted event, conflict/detail method, or policy remains explicit. |
| Stakeholder validation | **0/28** formal requirements stakeholder-validated. | Google Form/interviews pending; no participant signoff. |

## Business-rule validation (all 14)

`Validated` below means a bounded existing safeguard has direct tests/artifacts, **not** universal source coverage or user approval. Partial rows have a current guard but need future evidence-method or presentation work. Rule IDs link to [definitions](business-rules.md).

| Rule | Current classification | Current evidence and remaining boundary |
| --- | --- | --- |
| RULE-001 optional not-found | **Validated by existing behavior** | `test_optional_missing_files_keep_outcomes_but_complete_run`; required failures separate in UAT-002. |
| RULE-002 current absence ≠ historical | **Validated by existing behavior** | `test_paginated_history_and_historical_file_after_current_404`, `test_missing_or_uncertain_exact_ref_never_proves_absence`. |
| RULE-003 declaration ≠ use/adoption | **Validated by existing behavior** | P2 report unavailable adoption and `test_incomplete_collection_measures_evidence_coverage_without_asserting_no_adoption`; comprehensive installed source still future. |
| RULE-004 candidate ≠ accepted event | **Validated by existing behavior** | `test_frozen_baseline_and_review_ledger_replay`, UAT-005. |
| RULE-005 rejected/unresolved excluded | **Validated by existing behavior** | `test_rejected_candidates_never_enter_accepted_ledger`, `test_precision_excludes_unresolved_and_handles_zero_denominator`. |
| RULE-006 zero candidates ≠ no event | **Validated by existing behavior** | `test_zero_candidates_require_stage_sufficiency_for_negative_finding`, UAT-008. |
| RULE-007 copied upstream text | **Partially validated** | Frozen two candidates rejected; automatic text-origin classification absent (CAPG-002). |
| RULE-008 nonchronological categories | **Validated by existing report behavior** | [Phase 1 methodology](../phase-1/methodology.md), `test_preserved_validation_snapshots_produce_reviewed_candidates` checks report wording. |
| RULE-009 after-only not negative | **Validated by existing behavior** | `test_committed_after_only_case_remains_unknown_with_no_friction_denominator`, UAT-004. |
| RULE-010 collection ≠ sufficiency | **Validated by existing behavior** | `test_optional_404_is_complete_but_historical_unknown_remains_unknown`, UAT-009. |
| RULE-011 frozen cohort retained | **Validated by existing behavior** | `test_bounded_summary_has_no_pooled_incidence` plus frozen 2/6 reports; no silent exclusion. |
| RULE-012 recovery eligibility | **Partially validated** | Current report correctly leaves rate unavailable; qualifying downstream source/eligible set not yet implemented (DATA-002/CAPG-005). |
| RULE-013 no temporal causality | **Partially validated** | Report/method wording rejects causal interpretation, but no universal automated prose guard is claimed. |
| RULE-014 identity chain | **Validated by existing behavior** | `test_case_artifact_mismatch_fails_explicitly`, `test_duplicate_or_missing_decisions_fail_closed`; full accepted Phase 2 chain remains blocked (DATA-003). |

**Rule summary:** 11 bounded existing safeguards validated, 3 partially validated, 0 rules treated as overturned by a stakeholder preference. Future research may change wording or source priorities, but any proposed weakening of an integrity rule requires explicit evidence and change review. Rule validation is not the same as full requirement or stakeholder validation.
