# PULSE M3 product analytics decision memo

## Executive analytical summary

The frozen validation shows a clear operational distinction: planned core collection completed for all eight declared members, yet most lifecycle findings remain UNKNOWN and repository-level outcome is not defined. Historical comparison evidence is scarce, and candidate review matters because the only two emitted candidates were rejected. This supports prioritizing **question-specific evidence qualification and historical-context validation** as product hypotheses, while keeping publication and Power BI blocked. It does not establish ecosystem prevalence, customer value, or return on investment.

## What we analyzed

Population A comprises pytest 8.0.0 (two member investigations) and urllib3 2.0.0 (six), using M2.5 SQL metrics and DRAFT dbt marts. Population B comprises a separate frozen Phase 3 public workflow sample: 20 convenience-selected Dependabot PRs for descriptive rates and seven purposively selected discussion PRs as examples. No numerator or denominator crosses the population boundary.

## Populations and limitations

The two release cases were selected for forensic validation, not ecosystem representation. The PR base sample is title/first-page-biased, bot-centered, and public-only. Its 7 discussion PRs are excluded from base rates. Candidate firings share an artifact, so their outcomes are dependent. Most sufficiency records are legacy-classified, and all UNKNOWN reason codes are generic. Both analytical snapshots remain DRAFT; these are **validation analytical outputs**, not a published governed BI dataset.

## Major findings

1. Core collection was 8/8, but only two of 40 recorded member-category findings were bounded; 38 were UNKNOWN. The 2/40 ratio is a diagnostic count, not an approved decision-coverage KPI.
2. Exact-ref historical declarations were present for 2/8 members; only 1/8 had paired pre-release history. AFTER_ONLY does not establish a before/after comparison.
3. Urllib3 produced two copied-upstream candidate firings from one artifact and one repository; both were reviewed and rejected. Pytest had no acceptance denominator.
4. In the separate 20-PR base sample, copied upstream text appeared in 13, visible human interaction in six, and a substantive downstream review comment in one. Observable open-to-terminal duration was highly skewed (median 167.25h; two high 1.5×IQR outliers). These are workflow visibility diagnostics, not engineering effort or impact.

## Evidence gaps

The current reason code `unknown_insufficient_data` does not identify a specific missing source or causal mechanism. Qualified resolved-version, recovery-event/window, and approved required-question evidence are absent. All eight observed-adoption and recovery statuses remain UNKNOWN. Collection coverage therefore cannot substitute for decision coverage.

## Product implications

- Evaluate a category-specific prerequisite and reason taxonomy so an investigator sees *which evidence is needed* for a bounded answer; validate it before treating it as a metric.
- Test historical ref pairing and exact-ref declaration methods on a prespecified validation set. Do not count AFTER_ONLY as pre-release coverage.
- Retain origin-aware grouping and human review. Compare any origin-aware detector change against independently reviewed artifacts; two rejected firings do not establish global precision.
- Ask where human decisions happen when public PRs have little visible discussion. A merged PR is not proof of compatibility, adoption or recovery.

## What PULSE can currently support

It can reproduce bounded case/member collection, historical declaration, candidate, review, selected-source and finding-state diagnostics. Ten metric contracts are READY; seven are partial, five evidence-unavailable, and one stakeholder-blocked. It can surface uncertainty without converting UNKNOWN to NO.

## What it cannot support

It cannot currently claim confirmed adoption, recovery, business completion, customer value, organizational priority, ecosystem incidence, detector recall, or a broadly applicable precision estimate. Formal inference is **not justified** by the small purposive and convenience samples, sparse dependent events, and missing outcomes.

## Questions for stakeholder validation

1. Which lifecycle questions must an investigation answer before it is useful, and what constitutes a bounded completion?
2. Which source classes and historical windows are acceptable evidence for adoption and recovery in the intended workflow?
3. Where are compatibility decisions actually made—public PRs, CI, private review, issue trackers, release processes, or elsewhere?
4. How should an investigator see missing prerequisites and copied-upstream origin without mistaking them for negative evidence?
5. Who is the intended dashboard audience, what decision will each view support, and what evidence threshold permits publication?

## Recommended next analytical priorities

Prespecify question/source eligibility and reason codes; test historical pairing and origin-aware review on additional independent validation material **in a separately authorized milestone**; seek stakeholder definitions of useful outcome and decision workflow; then revisit rule provenance and the publication gate. The [dashboard requirements](power-bi-analysis-requirements.md) are specifications only. No Power BI work has begun.
