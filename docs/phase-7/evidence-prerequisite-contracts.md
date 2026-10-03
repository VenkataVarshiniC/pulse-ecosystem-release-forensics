# Phase 7 evidence-prerequisite contracts

Contract version: `p7-question-prerequisites-v1`

These experimental contracts apply only to the frozen eight-member Phase 7 population. A question is `SUFFICIENT` only when every required prerequisite is satisfied. An unmet, unavailable, incomplete, conflicting, structurally unavailable, or not-planned prerequisite yields `INSUFFICIENT` and preserves `UNKNOWN`. Evidence absence may produce bounded NO only after the full question contract is satisfied.

| Lifecycle question | Required evidence | Eligible sources | Time relationship | Sufficiency rule | UNKNOWN reasons | Bounded NO eligibility |
| --- | --- | --- | --- | --- | --- | --- |
| Adoption readiness | Qualified resolved or installed target version | Lockfile/resolver/runtime evidence; not collected | Must represent the governed post-release member state | Required source exists and establishes target-version readiness | `RESOLVED_VERSION_SOURCE_NOT_PLANNED` | Ineligible in v1 |
| Observed adoption | Qualified resolved or installed target version | Lockfile/resolver/runtime evidence; not collected | Must be after release and inside the governed window | Required source establishes actual target use | `RESOLVED_VERSION_SOURCE_NOT_PLANNED` | Ineligible in v1 |
| Migration friction | Complete frozen core/review inputs plus a paired pre-release target declaration | Existing Phase 2 core/review evidence; exact-ref repository manifests | Before declaration is at the latest repository anchor at/before release; comparison anchor is after release and at/before window end | Core/review coverage complete and at least one approved path is a valid pair containing a pre-release target declaration | `CORE_OR_REVIEW_INCOMPLETE`; `PRE_RELEASE_TARGET_DECLARATION_UNAVAILABLE`; source-state reason | Eligible only when both prerequisites are satisfied and no accepted qualifying event exists |
| Remediation | Complete frozen core/review inputs plus a paired pre-release target declaration | Existing Phase 2 core/review evidence; exact-ref repository manifests | Same bounded anchor relationship; lifecycle categories need not be chronological | Same two prerequisites as migration friction | Same controlled reasons | Eligible only when both prerequisites are satisfied and no accepted qualifying event exists |
| Recovery signal | Eligible downstream recovery source and denominator | Downstream release/runtime evidence; not collected | Must establish recovery after an eligible friction/remediation state | Required source and denominator exist | `RECOVERY_SOURCE_NOT_PLANNED` | Ineligible in v1 |

## Positive findings and support

A positive finding additionally requires an accepted qualifying observation or artifact and an intact chain:

`finding → qualifying observation/artifact/review → source identity → repository/ref/path → raw collection provenance`

The frozen population contains zero accepted candidates and therefore zero supported positive findings. Phase 7 does not fabricate support edges. `P7-M05` is unavailable at `0/0`; it is not reported as 100%.

## Semantics retained

- `UNKNOWN != NO`.
- Missing evidence is not negative evidence.
- A permissive dependency declaration does not prove compatibility, installation, or adoption.
- A repository boundary pair does not identify the exact change time.
- `REJECT` means the detector firing was not accepted under governed review; it does not prove absence of migration friction.
- The two inherited candidate firings remain two candidate IDs attached to one shared artifact, not two incidents.

No contract is relaxed after treatment results are observed.
