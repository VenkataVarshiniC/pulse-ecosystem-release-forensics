# Proposed analytical fact/dimension feasibility

Statuses assess **population from current artifacts**, not permission to create tables. Source identities are in [input manifest](input-manifest.json). Keys and grains follow [Milestone 1](../analytical-grain.md); the two reports are not themselves a star schema.

| Model | Status | Source; natural/business key; grain | Essential available / missing fields; relationship hazard |
| --- | --- | --- | --- |
| `dim_case` | PARTIAL | Case YAML/report; `case_id`, one row per case definition. | Package/version/window available; explicit `case_version` and owned-cohort authority absent. |
| `dim_repository` | READY_FROM_EXISTING_DATA | Frozen cohort/report; canonical `owner/name`, one row per repository identity. | Labels exist; rename history/host-stable ID not audited. Distinct across cases before dedup. |
| `dim_release` | READY_FROM_EXISTING_DATA | Case/PyPI-bound report; package + target version + upstream source, one row per declared release. | Release timestamp present; source disagreement/versioning not modeled. |
| `dim_evidence_source` | PARTIAL | Task/source/class + `capture_method`, one row per controlled source/method. | Current collector classes exist; no complete future access/source registry. All Phase 2 analyzed attempts use collector. |
| `bridge_case_repository` | READY_FROM_EXISTING_DATA | Case YAML/report frozen membership; `(case_id, repository)`, one per member. | Eight memberships preserve denominator; explicit `case_version` absent. Never inner-join to task rows. |
| `fct_collection_task` | READY_FROM_EXISTING_DATA | Preserved manifests/attempts; `(run_id, task_id)`, 54 rows. | Requirement/status/retries/provenance available; not-found has no snapshot. External original journals require governed ingestion path later. |
| `fct_repository_investigation` | PARTIAL | Report; `(case_id, repository)` in each frozen report, eight rows. | Coverage flags available; `analysis_snapshot_id`, required completion question set and human disposition absent. |
| `fct_candidate_review` | PARTIAL | Frozen baseline + review ledger; candidate ID, two rows. | Terminal review/rule/reason available; no separate emission time, review-event ID for multiple actions. |
| `fct_lifecycle_finding` | PARTIAL | Report stage findings; `(case_id, repository, category)`, 40 rows today. | Status/sufficiency available; finding version, stage-specific coded reasons and full YES support chain untested. |
| `fct_evidence_observation` | DESIGN_REVIEW_REQUIRED | Report/history manifest; current path-pair natural composite. | Exact refs/path states available; no stable observation ID, unclear before/after vs pair row grain. Target-version observation requires future source. |
| `bridge_finding_evidence` | DESIGN_REVIEW_REQUIRED | Accepted event links if present; none here. | Zero YES findings, so positive support cardinality untested; candidate→artifact is many-to-one. |
| Qualified target-version/recovery facts | FUTURE_SOURCE_REQUIRED | No current qualifying installed version or downstream recovery population. | Source, context, eligibility and window absent; cannot populate from declarations/PR dispositions. |

“READY” means existing data can populate that bounded grain after authorized loading; it does not mean the broader product or database is ready. Positive-finding lineage, duplicate future runs, and source access need a separate contract test before build.
