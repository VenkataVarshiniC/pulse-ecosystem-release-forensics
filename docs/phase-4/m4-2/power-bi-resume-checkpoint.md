# Deferred M4.2 resume checkpoint

`M4.2_STATUS = DEFERRED` for scheduling only. No connection, Power Query model, relationship, DAX, visual, `.pbix`, screenshot, or stakeholder-validated dashboard has been built. Start from the [main handoff](power-bi-build-handoff.md), [data contract](power-bi-data-model.md), [page specification](power-bi-dashboard-spec.md), and [acceptance checklist](power-bi-validation-checklist.md), not the old M3 technical publication hold. G8 remains `NOT_YET_VALIDATED`.

## Manual sequence when M4.2 is authorized to resume

1. [ ] Open Power BI Desktop and the handoff documents; confirm the active release manifest, snapshot IDs, v1 metric registry, and current stakeholder status.
2. [ ] Run the governed read-only publication/fingerprint verification; stop if published rows, metrics, model hash, or source scope drift.
3. [ ] Connect read-only to local PostgreSQL; load only approved `analytics` marts and an allowlisted published `SnapshotScope` semantic projection. Do not import raw ingestion or DRAFT rows.
4. [ ] Verify 2/6 declared members, exact case-to-snapshot pairing, and single-select case/release and snapshot behavior before relationships.
5. [ ] Build one-way dimensions, composite snapshot-member keys, and the separate route for NULL-repository upstream tasks. Inspect relationship cardinality and inactive/ambiguous paths.
6. [ ] Hide technical UUIDs/digests from primary visuals while retaining approved drill keys and a provenance panel.
7. [ ] Implement only presentation measures for READY contracts; use governed status/N/D and `DIVIDE`-style blank behavior. Label all proposed DAX **PROPOSED — NOT YET IMPLEMENTED** until built and checked.
8. [ ] Reconcile each measure for both cases with the published 46-row metric output, including pytest 0/0 and urllib3 0/2 acceptance.
9. [ ] Build Dashboard 1 from the frozen page specification; reconcile member, task, finding, and candidate counts.
10. [ ] Validate Dashboard 1 filters, case/snapshot context, UNKNOWN and unavailable labels, and member-to-category drill.
11. [ ] Build Dashboard 2; validate partial-component labeling, exact-ref observations, source/capture scope, and honest path-detail limits.
12. [ ] Validate Dashboard 2's missing-prerequisite explanation and no false absence/source-ranking claim.
13. [ ] Build Dashboard 3; validate candidate ID grain, one shared artifact, rule/origin, and inherited REJECT semantics.
14. [ ] Validate Dashboard 3 deep provenance through an approved publication-scoped projection; if unavailable, visibly withhold that drill rather than substitute raw data.
15. [ ] Add consistent case/release/snapshot, rule/metric version, capture method, source clock, and limitation tooltips or provenance panels.
16. [ ] Check `UNKNOWN`, `INSUFFICIENT`, `REJECT`, no candidate, bounded NO, zero numerator, `0/0`, and unavailable/blocked statuses on all pages.
17. [ ] Perform final formatting, accessibility, keyboard/reading-order, and source-label review; keep denominators visible and avoid unsupported red/green severity.
18. [ ] Save the actual `.pbix` and relationship configuration, then capture portfolio screenshots only after final validation.
19. [ ] Record measure-versus-SQL results, relationship/fanout tests, drill-through evidence, limitations, and reviewer sign-off.
20. [ ] Reconcile real stakeholder responses before calling a page or dashboard useful, approved, or complete. Close M4.2 only against its full agreed deliverables.

Expected DAX categories, **PROPOSED — NOT YET IMPLEMENTED**: simple counts/distinct counts at approved grain; selected-case/snapshot guards; `DIVIDE` or an equivalent blank result for zero denominator; display labels for governed status and unavailable reason. DAX must not infer eligibility, change `m2-5-metric-registry-v1`, create a partial contract rate, or replace SQL/dbt sufficiency. The published metric JSON is the comparison oracle. Actual Power BI DAX syntax and behavior must be tested during M4.2, not assumed from this document.

## Stakeholder reconciliation hook

When genuine Google Form or interview responses arrive, record respondent role/date/source, question wording, and dissent. Revisit the primary audience; most important decision; terminology for UNKNOWN, sufficiency, bounded NO and inherited review; page order and priority; whether uncertainty diagnostics are useful; acceptable evidence thresholds; investigation completion criteria; preferred drill depth; and whether all three pages are useful. Compare responses to original M3 hypotheses and current page specifications, change only what evidence warrants, and preserve the previous handoff version. Analyst assumptions and the public-PR workflow sample are not stakeholder validation. Until then every stakeholder-sensitive element remains **PROVISIONAL — STAKEHOLDER VALIDATION PENDING**.

| Item | Current state | Resume condition |
|---|---|---|
| Power BI Desktop connection | DEFERRED | Resume M4.2 and verify published source |
| Semantic model implementation | DEFERRED | Resume M4.2; validate one-way composite relationships |
| DAX implementation | DEFERRED | Resume M4.2; compare with governed SQL outputs |
| Dashboard 1 — Release Investigation Overview | DEFERRED | Resume M4.2; retain member and uncertainty rules |
| Dashboard 2 — Evidence & Uncertainty Diagnostics | DEFERRED | Resume M4.2; preserve partial-metric limits |
| Dashboard 3 — Candidate & Review Quality | DEFERRED | Resume M4.2; govern lineage detail projection |
| PBIX validation | DEFERRED | After actual build and metric/relationship tests |
| Portfolio screenshots | DEFERRED | After final formatting and accessibility checks |
| Stakeholder reconciliation | PENDING | Genuine survey/interview responses received |

The manual Power BI build is deferred for scheduling reasons only. No planned dashboard, metric, drill-through, analytical requirement, validation requirement, or portfolio deliverable has been removed. Phase 5.1 Product Workflow Specification may proceed; it must not claim Power BI is implemented. M5.5 Final Portfolio Release remains dependent on completion of deferred M4.2 and required analytical/consulting closure.
