# Phase 4 metric change log

**Milestone 1A: no metric definitions changed; all 23 remain version 1.0.** The audit does not silently amend a contract when its inputs are absent. [Computability findings](baseline-analysis/metric-computability.md) are separate from definition changes.

| Contract | Observed issue and evidence | Current decision | Future change trigger / impact if revised |
| --- | --- | --- | --- |
| MET-004 | Source-class statuses exist, but the category→required-source map is not a frozen analytical field. | Partial; no numeric stage-source completeness rate. | Version a source-set registry before revising numerator logic; backfill affected cases and label method version. |
| MET-006/012 | Five reported categories exist; stakeholder-required completion question set is unvalidated. | MET-006 unavailable; MET-012 only a reported-category diagnostic. | Primary research defines required questions, exclusions and completion; version definitions and recompute denominators. |
| MET-013/015 | Repository missing-source labels are not linked to each UNKNOWN stage. | Partial; no cause/contribution percentages. | Add controlled reason→stage→required-source links; do not retroactively infer attribution. |
| MET-019 | Verified HTTPX resume exists, but the two release cases have no resumed run. | Separate 11/11 method example; no release-case rate. | Collect a genuine eligible resume run under a declared case; retain original eligibility rule. |
| MET-023 | Candidate `occurred_at` is source event time, not emission time. | Unavailable; no substitution. | Record explicit emission/availability timestamp and review-event identity before computing duration. |

Any later revision must append: old definition/version, exact observed problem and source, proposed definition/version, affected numerators/denominators/grains, backfill comparison, reviewer decision and date. No such revision is authorized or made in Milestone 1A.
