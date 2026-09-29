# M2.5 bounded validation observations

These statements describe only the frozen pytest 8.0.0 and urllib3 2.0.0 validation cases (two releases, eight declared repositories). They are inputs to later analysis, not causal, comparative-effect, or ecosystem claims.

- Required collection succeeded for 11/11 pytest and 27/27 urllib3 planned required tasks. Optional not-found outcomes were 1/4 and 5/12, respectively; no task retried. The task types have different denominators.
- Exact-ref historical target declarations occur in one member per case (2/8 combined). Stronger paired pre-release history occurs in one pytest member and no urllib3 member. Six path records are AFTER_ONLY, not paired comparisons; path counts are not repository counts.
- The urllib3 baseline emitted two candidate IDs from one repository and one artifact. Both received terminal REJECT reviews. Pytest emitted no candidates, so reviewed acceptance is undefined there.
- There are 40 lifecycle findings: 38 UNKNOWN and two bounded NO. The bounded NO findings belong to pytest's migration-friction and remediation categories. Thirty-eight sufficiency assessments retain LEGACY_UNCLASSIFIED; these are not retrospectively labeled insufficient.
- Observed adoption and recovery are UNKNOWN for every member. Missing evidence cannot be interpreted as zero adoption or zero recovery.
- Selected capture sources include nine source types per case, all with recorded `collector` method and zero fixtures in these Phase 2 snapshots. Source-type presence alone is not counted; the diagnostic joins selected captured artifacts. This does not repair unknown rule provenance.

No inferential statistics, cross-ecosystem comparison, product recommendation, or stakeholder acceptance conclusion is supported by two release cases.
