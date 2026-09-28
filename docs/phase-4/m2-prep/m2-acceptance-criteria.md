# Future Milestone 2 acceptance and review gates

The eventual implementation can PASS only after authorization and all checks below, with source file IDs and query/test outputs attached. A documented source limitation may keep an individual metric unavailable; it cannot be masked as a test pass for that metric.

1. PostgreSQL environment/schema/migrations are reproducible in an isolated environment, with pinned versions and no committed secret.
2. Phase 2 frozen evidence loads with verified raw URI/digest/capture method, original source/ref/event/retrieval times and load audit. Repeated load is idempotent; conflicting key quarantines.
3. Eight frozen members reconcile exactly (2 pytest, 6 urllib3), including rows without qualifying evidence. No cohort member disappears from a join.
4. All 54 planned tasks reconcile (15 and 39), with 11/11 and 27/27 required, optional not_found 1/4 and 5/12, retries 0/15 and 0/39. Required failure and optional 404 stay distinct.
5. Historical declaration 1/2 and 1/6, paired pre-release 1/2 and 0/6. After-only cannot qualify release-window bounded NO.
6. Two urllib3 candidate IDs from one artifact, one emitting repository and two rejected reviews remain distinct; pytest has zero candidates. No accepted evidence is derived from a candidate alone.
7. Finding/assessment/status chains preserve UNKNOWN, explicit reason and selected version; neither adoption nor recovery becomes 0% or a bounded NO because evidence is absent.
8. dbt generic and [20 custom integrity themes](dbt-test-matrix.md) pass on governed fixtures and frozen data where observable. Positive YES support receives a controlled fixture because frozen cases have none.
9. Every mart meets exact grain, snapshot and FK contract; pre/post-join distinct counts match. Power BI cannot inflate counts through support bridges.
10. All 23 metric contracts have N/D lineage and explicit computability/unavailable reason. Currently computable values match [golden values](golden-validation-values.md); method changes get new metric/snapshot version and side-by-side comparison.
11. Replays 2/2 per case match canonical output under frozen inputs; a new live capture is labeled a new run. SQL analyses retain version, denominator and source lineage.
12. Schema, loader, model, runbook and quality documentation is current; an independent reviewer can trace sample finding to original raw evidence and review, and inspect quarantined failures.

Schema review checklist: [ ] normalized identities and typed observations; [ ] explicit grain/key on every table; [ ] PK/FK/unique/check valid; [ ] raw provenance and event/capture clocks separate; [ ] UNKNOWN and frozen membership intact; [ ] extension by provider refs rather than vendor copy; [ ] no premature generic framework; [ ] indexes justified by access pattern.

dbt review checklist: [ ] source contracts and provenance present; [ ] staging performs no business inference; [ ] intermediate versions rules and chooses snapshot; [ ] mart grains match metric grains; [ ] generic/custom tests pass and failures retained; [ ] no BI-only eligibility logic; [ ] unavailable metrics remain unavailable; [ ] snapshot reproducibility shown.
