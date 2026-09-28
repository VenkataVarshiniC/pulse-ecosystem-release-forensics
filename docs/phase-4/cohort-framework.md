# Cohort definitions and comparison discipline

A **case cohort** is the frozen set of declared `(case_id, repository_id)` memberships; it is never reduced because collection failed. Phase 2's pytest 8.0.0 and urllib3 2.0.0 cohorts were selected for validation and cannot support population estimates. Any cross-cohort comparison must show selection rule, source plan, window, case version and denominator.

| Cohort | Assignment rule | Decision use | Guard |
| --- | --- | --- | --- |
| Release | All declared memberships under one release case. | Case-level sufficiency and attention map. | Do not pool release effects as ecosystem incidence. |
| Package family | Case's declared target package; compare only like evidence methods. | Identify package-specific acquisition gaps. | No general package ranking from convenience cases. |
| Evidence coverage | High = all preregistered question-specific sources complete; partial = some but not all; insufficient = no defensible stage basis. | Choose source-method test. | Define source set per question; labels are not adoption strata. |
| Historical context | Pre-release paired-path declaration; after-only exact-ref declaration; unresolved/no qualifying ref. | Test release-boundary context gap. | After-only counts as context coverage, not a negative release-window denominator. |
| Candidate path | None emitted; emitted-unreviewed; accepted; rejected; needs more evidence. | Diagnose review/rule path. | A repository may have multiple candidates/dispositions; use distinct member counts for repository comparisons. No-candidate is not no event. |
| Source availability | Complete, optional verified not-found, partial/failed, not planned by source class. | Locate missing evidence. | Optional not-found means probe completed, not source fact absent historically. |
| Selection method | Rule-based convenience, purposive, or later stakeholder-declared owned set, with frame/version. | Assess transportability. | Never relabel research cohort as owned portfolio. |

Cohort comparisons show raw counts, exact denominators and missingness. Segment membership can overlap; do not sum overlapping strata. Historical status and source coverage are measured per case, not enduring repository traits.
