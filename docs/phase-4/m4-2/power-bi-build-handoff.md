# M4.2 Power BI build freeze and future handoff

`M4.2_STATUS = DEFERRED` · `TECHNICAL_BI_STATUS = TECHNICALLY_READY` · `G8 = NOT_YET_VALIDATED` · `OVERALL_BI_STATUS = TECHNICALLY_READY_STAKEHOLDER_HOLD`

Manual Power BI dashboard construction is intentionally postponed for scheduling reasons. Scope, quality, analytical requirements, and final deliverables are unchanged. **DEFERRED does not mean cancelled, skipped, complete, or out of scope.** No Power BI connection, semantic model, DAX measure, dashboard, screenshot, or `.pbix` is claimed here.

This is the current-state handoff for a later **manual M4.2**. It supersedes only the obsolete *technical publication gate* sentences in the original [M3 Power BI requirements](../m3/power-bi-analysis-requirements.md), [M2.4 join guide](../m2-implementation/m2-4-join-guide.md), and [M4.1 stakeholder gate](../m4-1/dashboard-stakeholder-gate.md): M4.1B subsequently passed G1–G7 and published governed replay snapshots. Those earlier records are preserved as written. Their audience, question, uncertainty, denominator, and drill-through requirements remain hypotheses until G8. No stakeholder response has established final audience, usefulness, priority, wording, decision workflow, or completion criteria; mark such choices **PROVISIONAL — STAKEHOLDER VALIDATION PENDING**.

The technical source of truth is release `m4-1b-9979f0a7b15d6e70b90f` in the [publication manifest](../../../data/validation/m4-1b-publication-manifest.json), with pytest snapshot `08852d5f-9843-5406-a69b-7039ea2ddaa4` and urllib3 snapshot `bd3a02a5-0c2d-5eec-84fd-8e9b93a238a3`, both `PUBLISHED_VALIDATION`. The two older snapshots are DRAFT and must never enter normal Power BI consumption. The explicit case-and-snapshot selector, immutable fingerprint validation, and `m2-5-metric-registry-v1` are mandatory. `PUBLISHED_VALIDATION` means controlled, bounded analytical consumption; it does not confer stakeholder approval, ecosystem representativeness, adoption, recovery, or product success.

Use these frozen build documents together:

- [Data model and relationship contract](power-bi-data-model.md): the 11 dbt marts, snapshot filter, safe keys, semantic relationships, governed measures, and provenance gaps.
- [Three-page dashboard specification](power-bi-dashboard-spec.md): visual fields, slicers, labels, tooltips, drill-through, and limitations.
- [Validation checklist](power-bi-validation-checklist.md): per-case golden counts, metric semantics, fanout tests, publication and accessibility checks.
- [Resume checkpoint](power-bi-resume-checkpoint.md): manual build sequence, DAX boundary, stakeholder questions, and deferred-work register.

The retained authority chain is the original [M3 requirements](../m3/power-bi-analysis-requirements.md), [M2 semantic proposal](../m2-prep/power-bi-semantic-model.md), [M2.4 analytical model](../m2-implementation/m2-4-analytical-model.md), [join guide](../m2-implementation/m2-4-join-guide.md), [metric readiness](../m2-implementation/m2-4-metric-readiness.md), [M2.5 results](../m2-implementation/m2-5-metric-results.md), [SQL catalog](../m2-implementation/m2-5-sql-catalog.md), [M4.1 stakeholder gate](../m4-1/dashboard-stakeholder-gate.md), and the later [M4.1B decision](../milestone-4-1b-findings.md). The [replay metric output](../../../data/validation/m4-1b-replay-metrics.json), [metric comparison](../m4-1/replay-metric-comparison.md), and publication manifest resolve numerical or version questions; older DRAFT metric files remain historical baselines, not BI inputs.

The manual Power BI build is deferred for scheduling reasons only. **No planned dashboard, metric, drill-through, analytical requirement, validation requirement, or portfolio deliverable has been removed.** No schema, metric, source evidence, or published result is changed by this freeze.

PULSE may proceed to **Phase 5.1 Product Workflow Specification** while M4.2 remains deferred. Phase 5 work must not claim Power BI implementation is complete. **M5.5 Final Portfolio Release cannot be considered complete until deferred M4.2 Power BI implementation and required final analytical/consulting closure are completed.**
