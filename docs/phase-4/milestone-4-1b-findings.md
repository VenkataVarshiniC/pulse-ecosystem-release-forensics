# M4.1B — governed replay analytics and publication decision

**Classification: PASS_WITH_STAKEHOLDER_HOLD.** Technical gates G1–G7 pass for the bounded two-case replay release. G8 is **NOT_YET_VALIDATED**; overall Power BI eligibility is **TECHNICALLY_READY_STAKEHOLDER_HOLD**. This is a controlled analytical release, not permission to claim market fit, ecosystem representativeness, adoption, recovery, or dashboard utility. No Power BI work was done.

## Governed replay lineage

The committed M4.1 artifact SHA-256 is `b3be08da423c5c988be9151178b0da137a6d5bd1aedd300afbfc2c825cc48f13`; its rule release is `rule-replay-b2b638bb97c8-e10fb03f467e267f`, rule manifest hash `b9f09c03b5e72aa44cbb334e71261b4c72c966e899c0e9b962ddb97d1d858896`, and 142-file input manifest hash `09d66f72862cfaa1a664cb1fc5c42a5b8fe28dbaeb35bd7f42364bdbff50a743`. The loader refuses drift. Source commit `a85bbab9d222b924b6e7d6ea85a74da984df801d` pins its implementation and dbt model bytes. The M2.5 metric registry remains `m2-5-metric-registry-v1`; the model version is derived from the dbt model hash in the publication manifest.

The existing snapshot schema is case-scoped, so this release contains **two new physical snapshots** under one release ID: pytest `08852d5f-9843-5406-a69b-7039ea2ddaa4` and urllib3 `bd3a02a5-0c2d-5eec-84fd-8e9b93a238a3`. Both began DRAFT and were promoted only by `scripts/publish_m4_1b.py` after all checks. The original snapshots `2cecea1d-7b8f-5843-b4c1-39b7d99a9393` and `5a9b4836-44a1-5419-bd95-679a3877ed11` remain DRAFT with their unrecorded legacy rule. Neither old snapshot, candidate, review, assessment, nor finding row was edited.

Migration V005 adds replay snapshot/candidate lineage, an explicit `INHERITED` review origin and original-review reference, a separate immutable publication record, and guarded `PUBLISHED_VALIDATION` state. The additive loader made two replay candidate IDs linked to their original candidate IDs, one shared artifact digest, exact normalized fingerprints and the replay rule. Both source reviews were REJECT. Their original review UUIDs and timestamps remain linked; the replay review rows are provenance records, **not new reviewer actions**. It created 40 version-2 assessments (2 SUFFICIENT, 38 INSUFFICIENT) and 40 version-2 findings (38 UNKNOWN, two bounded NO, zero positive). Legacy `LEGACY_UNCLASSIFIED` remains separate. The two bounded NO findings are limited to pytest friction and remediation with paired pre-release context. Adoption and recovery remain UNKNOWN. Lifecycle categories are evidence classes, not a required chronology or causal chain.

dbt materializes 30 models and passes 173 tests across staging, intermediate, and marts with legacy and replay side by side. Candidate/member aggregation and tests now honor explicit snapshot selection; replay rows do not leak into legacy snapshot facts. Seven snapshot-scoped analytical marts reconcile, including eight member rows, 54 collection-task rows, 11 observation rows, two candidate rows, 40 finding rows, and no accepted finding-evidence bridge rows. The selected artifact links total 72 across the two snapshots; this is a link count, not 72 distinct new captures. All 23 metrics were executed per replay snapshot and rerun byte-identically (46 outputs; SHA-256 `febd43d2586d421a1f9ef64ae1b710db9484794ab9bf1a684e92a78eeabb595f`). See the [per-contract comparison](m4-1/replay-metric-comparison.md). The 46 governed status/numerator/denominator/value tuples match legacy: 31 IDENTICAL, 15 UNAVAILABLE_BOTH. Explicit replay sufficiency vocabulary changed without changing the v1 metric rate contract.

## Stability, gates, and limits

| M3 observation | Current classification | Bounded result |
|---|---|---|
| Collection versus decision coverage | STABLE | 8/8 core member collections; only 2/40 bounded stage findings. |
| Historical-context limitation | STABLE | Only 1/8 members has paired pre-release history; after-only paths do not prove absence. |
| Candidate/review result | STABLE | Two exact-equivalent candidates from one PR, both inherited REJECT. |
| UNKNOWN dominance | STABLE | 38/40 UNKNOWN, never converted to NO. |
| Copied-upstream origin | STABLE | The two candidate spans retain the copied-upstream marker; this is not a recall estimate. |
| Replay metric availability | CHANGED | All 23 v1 contracts were executed per new snapshot; five evidence-unavailable contract definitions and one stakeholder-blocked definition remain. |

| Gate | Result | Basis |
|---|---|---|
| G1 frozen input | PASS | 142 verified files and unchanged original source-row fingerprints across 30 ingestion/core tables. |
| G2 rule provenance | PASS | Explicit rule release and rule-manifest hash are bound in new snapshot lineage. |
| G3 deterministic replay | PASS | Committed replay hash verified; loader idempotent; metric output reproducible. |
| G4 candidate/review lineage | PASS | Two exact-equivalent candidate links and traceable original REJECT decisions. |
| G5 finding lineage | PASS | 40 new versioned assessments/findings; status and sufficiency reconciliation passed. |
| G6 metric/model governance | PASS | 23 v1 contracts per explicit snapshot; model and registry hashes; deterministic metric output. |
| G7 analytical publication | PASS | dbt tests, reconciliation, frozen source comparison, release manifest, database publication record and post-publication fingerprint validation passed. |
| G8 stakeholder validation | NOT_YET_VALIDATED | Authorized Phase 3/4 materials contain no actual survey or interview response validating audience, usefulness, wording, or dashboard priorities. |

The release ID is `m4-1b-9979f0a7b15d6e70b90f`. The [`publication manifest`](../../data/validation/m4-1b-publication-manifest.json) has canonical body digest `04a2b29767ab100748ced9a3d67a3272faf0b55abbf8700c3cdb67d6b279153d` and file SHA-256 `62de6ac5fd1e914740dbb651aa2c0ccfd0fc7295e0af1ee52ed44bf9dee6be8f`. It records the common publication timestamp, case-specific snapshot/metric/mart fingerprints, source commit, dbt 1.11.15, 30 model successes and 173 test passes. The database stores each case's metric output and mart-row fingerprints. Published snapshots and their selected result/lineage rows reject update/delete; publication records reject update/delete. `scripts/publish_m4_1b.py` rechecks the immutable manifest, live metrics, and mart row fingerprints and refuses drift. A future rule, dbt, or metric revision requires a new release and snapshot. `PUBLISHED_VALIDATION` means only that this bounded analytical snapshot is reproducible and versioned for controlled consumption. It does **not** imply stakeholder validation, ecosystem representativeness, product-market fit, confirmed adoption, or confirmed recovery.

The technical Power BI gate is **TECHNICALLY_READY**; the overall gate remains **TECHNICALLY_READY_STAKEHOLDER_HOLD**. No dashboard or connection was created. The three M3 dashboard themes remain prospective:

| Theme | Required metrics and drill | Replay technical status | Stakeholder status |
|---|---|---|---|
| Release Investigation Overview | MET-001/002/008; exact case/snapshot and member/path drill; visible UNKNOWN and eligible denominator. | TECHNICALLY_READY for bounded collection/context/candidate slices. Adoption, recovery, outcome tiles are unavailable or blocked. | NOT_YET_VALIDATED |
| Evidence & Uncertainty Diagnostics | MET-004/005/012/013/015; stage/member/source drill, UNKNOWN reason and missing prerequisite disclosure. | TECHNICALLY_READY for current partial components and selected evidence drill. Reason distribution, source attribution and denominator interpretation remain partial. | NOT_YET_VALIDATED |
| Candidate & Review Quality | MET-008/009/010/011/022; artifact-to-candidate/review lineage, rule and copied-upstream origin drill. | TECHNICALLY_READY for two inherited rejects on one artifact. Pytest candidate ratios are 0/0 and NULL, not zero percent. | NOT_YET_VALIDATED |

The evidence population stayed frozen; no external evidence was recollected. M4.2 and Power BI implementation have not begun.
