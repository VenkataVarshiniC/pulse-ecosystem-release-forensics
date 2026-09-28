# Future Milestone 2 build backlog and sequence

**Not authorized.** Work packages are technical sequencing, not permission, estimates or separate product milestones. Any actual build remains under Phase 3 HOLD until stakeholder reconciliation and an explicit implementation decision. Each package must retain the [golden values](golden-validation-values.md) and [acceptance gate](m2-acceptance-criteria.md).

| Package | Objective and dependencies | Inputs → outputs; acceptance and main risk |
| --- | --- | --- |
| WP1 Environment/schemas | Authorized local PostgreSQL foundation; none | Pinned runtime/config → reproducible isolated schemas/roles. Accept repeat setup and no secrets. Risk environment drift. |
| WP2 Core identity/provenance | Stable keys, source/run/task/artifact; WP1 | Frozen manifests + raw refs → constrained identity/provenance relations. Accept digest/rename/capture-method checks. Risk raw path governance. |
| WP3 Frozen data loader | Idempotent Phase 2 load; WP2 | Verified external files → audit/quarantine/id mapping. Accept replay no-op, conflict quarantine. Risk missing external roots. |
| WP4 Normalized observations/reviews/findings | Typed evidence chain; WP2–3 | Historical pairs, baseline, ledger, reports → versioned core rows/bridges. Accept no UNKNOWN conversion, no candidate→fact shortcut. Risk positive YES path unobserved. |
| WP5 dbt project/staging | Trusted source contracts; WP3–4 | Core/ingestion → typed staging models. Accept status/provenance parity with source. Risk parser drift. |
| WP6 Intermediate evidence/sufficiency | One-snapshot business logic; WP5 | Staging + methods → member spine, terminal review, stage sufficiency. Accept after-only and missing-source controls. Risk unresolved method questions. |
| WP7 Analytics facts/dimensions | Explicit grains; WP6 | Intermediate + manifest → dimensions/facts/bridges. Accept unique grains and frozen member count. Risk join fan-out. |
| WP8 dbt integrity tests | Enforce rules; WP5–7 | Test matrix → generic/custom tests and failing-row diagnostics. Accept all blocking tests and negative fixtures. Risk no real positive YES example. |
| WP9 Metric SQL/analysis | Governed eligible metrics; WP7–8 | Marts + metric definitions → versioned N/D views and query backlog. Accept all computable baseline values; unavailable stays unavailable. Risk false inference. |
| WP10 Reconciliation/documentation | End-to-end signoff; WP1–9 | Frozen inputs + audit → golden comparison, replay, lineage review, operator docs. Accept 8 members/54 tasks/2 candidate identity and snapshot reproducibility. Risk source files unavailable or permission. |

Execution in five controlled steps: **M2.1** WP1–2 (environment/base schema); **M2.2** WP3–4 (loading/core normalized model); **M2.3** WP5–6 (dbt staging/intermediate); **M2.4** WP7–8 (marts/data quality); **M2.5** WP9–10 (metrics/advanced SQL/reconciliation). These are substeps of one Milestone 2, not permission to begin M2.1. Do not add target-version/recovery sources, an update bot, generic PR fact or BI deployment just to complete the sequence.
