# Phase 2 Findings

## Executive Decision

**PIVOT.** Preserve the validated collector, provenance, review, and reporting architecture. The current evidence-acquisition and historical-context method does not yet support scaling the lifecycle claims.

## Original Question

Can PULSE perform comprehensive enough unattended evidence collection across multiple predeclared downstream cohorts to produce useful, auditable release-forensics results without manually locating relevant issues, PRs, commits, or historical SHAs first?

## Final Answer

**Not yet for substantive multi-repository lifecycle reconstruction.** PULSE collected the planned public GitHub and PyPI sources and generated auditable reports for both frozen cases without hand-selected issue/PR URLs or historical SHAs. The reports are useful as an honest account of what was collected and what remains unknown. They contain **zero accepted lifecycle events**, however, and cannot measure observed adoption or recovery. Successful unattended collection of the planned sources is narrower than acquisition of enough relevant evidence to explain release effects.

## Milestone Summary

| Milestone | Classification | Evidence |
| --- | --- | --- |
| 1 — Collection Reliability | **PASS — LIVE VALIDATED** | Authenticated pagination, bounded retry/rate-limit outcomes, collector provenance, immutable checkpoints, verified zero-request resume, and required-versus-optional task semantics were exercised live. |
| 2 — Historical Dependency Reconstruction | **PARTIAL** | Automatic path-scoped ref discovery and exact-ref parsing worked in live cases; missing in-window anchors and cross-file history remain unresolved. |
| 3 — Predeclared Multi-Repository Cohorts | **PARTIAL** | Outcome-blind cases and a complete exclusion ledger were frozen before forensic collection; the pytest frame yielded only two repositories. |
| 4 — Detector Quality Evaluation | **PARTIAL** | The first-pass baseline and independent analyst decisions were preserved; only two rule firings from one artifact were reviewable, both rejected. |
| 5 — End-to-End Reporting | **PASS for end-to-end report integration** | Both frozen cases replay through one verified, deterministic workflow with machine-derived source sufficiency, UNKNOWN propagation, and rejected output excluded from accepted evidence. |

## What Phase 2 Proved

Authenticated PULSE collectors can retrieve bounded, paginated public evidence, preserve provenance and partial failures, and safely resume verified whole tasks. The live validation runs completed operationally for both frozen cases. The path-scoped historical engine can select refs automatically and retrieve and parse files at exact SHAs. A predeclared, outcome-blind selection process can freeze auditable convenience cohorts. Candidate rules and analyst review remain separate. The Phase 2 report pipeline verifies the case fingerprint, task plan, collection snapshots, history identity, frozen baseline, and reviewed candidate identity before producing deterministic JSON and Markdown. It correctly renders an empty accepted timeline and unavailable metrics.

## What Phase 2 Did Not Prove

It did not prove unbiased downstream discovery, representative adoption or friction rates, comprehensive historical dependency state, target-version installation, runtime compatibility, detector recall, broadly useful detector precision, causal impact, production-scale monitoring, or automated recovery measurement. Complete collection of a planned API query does not establish that all relevant public evidence was discoverable by the current rules. The two convenience cohorts are not an ecosystem sample.

## Quantitative Evidence

| Measure | pytest 8.0.0 | urllib3 2.0.0 |
| --- | ---: | ---: |
| Frozen repositories | 2 | 6 |
| Core metadata/issues/PRs/commits collection complete | 2/2 | 6/6 |
| Exact-ref target-package declaration observed | 1/2 | 1/6 |
| Baseline candidates emitted | 0 | 2 |
| Accepted / rejected / unresolved candidates | 0 / 0 / 0 | 0 / 2 / 0 |
| Accepted lifecycle events | 0 | 0 |
| Repositories with zero emitted candidates | 2 | 5 |
| Friction and remediation repositories supporting a bounded negative finding | 1/2 | 0/6 |

Across eight repositories, two rule firings from one Dependabot PR were reviewed: **0 accepted, 2 rejected, 0 unresolved**, giving **0/2 reviewed-candidate precision** for this emitted set. That fraction is not a population precision estimate. No recall denominator exists. Historical target-package declaration evidence totals **2/8**, but only the pytest declaration has a parsed pre-release anchor in a paired path. The urllib3 declaration is after-only. Neither count measures adoption or target-version eligibility. The live case runs had 15 planned tasks (14 succeeded, one optional 404) for pytest and 39 (34 succeeded, five optional 404s) for urllib3, with no required failures. Milestone 5 core collection covers all eight repositories under its explicit metadata/issues/PRs/commits threshold.

## Main Product Finding

The release-forensics thesis remains plausible, but the present automated path often returns a defensible inventory of missing evidence rather than a substantive release narrative. Conservative UNKNOWN findings build trust only if the acquisition layer can eventually reduce them. The two frozen reports have no accepted timeline events; adoption and recovery remain unknown throughout, and the urllib3 case cannot support even a bounded negative friction finding after the release-boundary audit. Product scaling would amplify uncertainty, not solve it.

## Main Technical Finding

Collection reliability and deterministic report integration are no longer the primary engineering blockers for these bounded cases. PULSE can preserve exact queries, raw snapshots, run outcomes, reviewer decisions, and stable analytical output. The remaining challenge is methodological: whether the selected sources, historical anchor strategy, cohort frame, and candidate rules can reliably surface qualifying evidence without unsupported inference.

## Evidence Acquisition Gaps

1. **Release-time dependency context:** path changes bounded to the observation window miss older unchanged declarations. A current declaration is membership evidence, not historical use. Cross-file migrations and incomplete pairs leave six of eight repositories historically unknown under the contextual Milestone 4 method.
2. **Observed adoption and recovery inputs:** no comprehensive target-version lockfile or ordinary runtime/CI resolution data was collected. Downstream releases were not planned, so `text.support_release` had no input and no recovery-eligible denominator exists.
3. **Candidate discovery:** exact-version text matching can miss version-implicit incidents. The two collected candidate firings came from one bot update with copied upstream notes, not qualifying downstream events. The non-emitted record universe was not independently labeled.
4. **Cohort frame:** first-page GitHub code search, current root manifests, and a two-member pytest cohort constrain validity outside these frozen cases.

These are prioritized evidence-method questions, not a claim that unobserved incidents exist in the frozen repositories.

## Detector Findings

The deterministic rules remain useful as **secondary candidate generators requiring review**, not validated central event classifiers. For pytest they emitted none. For urllib3, `text.version_specific_friction` and `text.version_specific_remediation` each fired on the same unmerged Dependabot PR; both were rejected after reviewing the preserved PR body. The failure pattern is copied upstream release-note language inside a bot dependency update. One distinct artifact did not meet the preregistered threshold for a general rule change, so no detector was retuned. Zero emissions do not establish no impact, and 0/2 does not establish universally zero precision.

## Historical Reconstruction Findings

The automatic exact-ref mechanism is worth preserving, but `historically_supported` is deliberately broad: any parsed exact-ref target-package declaration in the window qualifies for **evidence coverage**, including an after-only declaration. It does not prove release-time presence, target-version eligibility, installation, or compatibility. The closure audit corrected the stricter question of whether a repository can support a **negative release-window finding**: that now requires a parsed pre-release target declaration in a paired path as well as complete stage-source collection and review. `planetlabs/cosmolog` meets that bounded threshold; `wimglenn/advent-of-code-data` has only an after-side declaration and remains UNKNOWN. Thus historical evidence coverage remains 1/2 and 1/6, while urllib3's previously displayed bounded friction denominator is suppressed.

## Reporting and Trustworthiness

`YES` requires accepted qualifying evidence. `NO QUALIFYING EVIDENCE FOUND` means the declared stage sources were completely collected and reviewed under the bounded method, with no accepted event; it does **not** mean no event happened. `UNKNOWN` propagates incomplete required collection, unresolved release-boundary context, uncollected source types, or undefined denominators. Current declarations, permissive constraints, zero candidates, and elapsed time do not become observed adoption, absence, or recovery. The generated reports expose all eight repositories, source gaps, rejected candidates, empty accepted timelines, and metrics with explicit numerators and denominators. Their lifecycle stages are evidence categories, not an assumed chronology or causal sequence.

## Final Decision Rationale

**GO TO PHASE 3** as expansion or productization is unsupported: the validation cases provide no accepted lifecycle events, only two rejected rule firings, little release-boundary dependency context, and no measured observed adoption or recovery. **STOP** is also premature: earlier Phase 0/1 records show that public release-associated evidence can be useful, while Phase 2 demonstrates a working unattended collection and audit trail that can be retained. **PIVOT** best matches the record: preserve the functioning architecture, but require a deliberate evidence-method correction before scaling release-forensics claims. This is a Phase 2 product decision, not an implementation authorization for Phase 3.

## Architecture to Preserve

- Typed case and frozen cohort definitions with explicit windows and selection records.
- Authenticated paginated collectors, bounded failure/retry semantics, immutable raw snapshots, collector provenance, and verified resume.
- Typed exact-ref historical file states and explicit unresolved statuses.
- Immutable first-pass candidate baselines, independent structured review, and accepted-evidence separation.
- Artifact identity checks, stage-specific sufficiency, deterministic reports, and denominator-aware metrics.

## Work Explicitly Deferred

No new collectors, cohorts, detector rules, historical lineage system, adoption logic, downstream release source, lockfile/runtime source, frontend, warehouse, model classification, or deployment was added in this closure audit. None is authorized by this decision alone. The suitability and priority of such work belong to a separate future design.

## Claims Allowed After Phase 2

- PULSE performed authenticated bounded live collection and verified resume in declared cases.
- It automatically reconstructed some exact-ref dependency declarations and represented unresolved history explicitly.
- It froze two outcome-blind convenience cohorts and preserved an exclusion ledger.
- It reviewed all two emitted validation candidates independently; neither qualified.
- It reproducibly generated two auditable reports that preserve UNKNOWN, rejected evidence, and missing denominators.

## Claims Still Prohibited

- Ecosystem-wide monitoring, unbiased dependent discovery, or population adoption/friction statistics.
- Exhaustive release-impact discovery, detector recall, or broad detector precision.
- Target-version installation or runtime compatibility inferred from a permissive declaration.
- Causal attribution from temporal association or a required chronological lifecycle.
- Reliable observed-adoption or recovery rates, or production-scale readiness.
- Interpreting zero emitted/accepted events as proof of no release effect.

## Phase 3 Planning Inputs

A future design should decide what evidence would establish release-time dependency use, target-version adoption, and a bounded recovery-eligible set; whether publicly accessible sources can provide those observations at useful coverage; how to evaluate candidate discovery against independently labeled events; and how to preserve outcome-blind cohort selection while testing a more useful frame. It should state measurable gates before any product expansion. These are questions derived from Phase 2, **not** a Phase 3 architecture, milestone plan, branch, or implementation commitment.
