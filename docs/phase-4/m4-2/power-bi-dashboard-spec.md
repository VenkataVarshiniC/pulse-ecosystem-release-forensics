# Frozen three-page dashboard specification

All pages use the [published snapshot selector and relationships](power-bi-data-model.md), show the selected case/release and snapshot/version, and carry the label **PROVISIONAL — STAKEHOLDER VALIDATION PENDING** for audience, terminology, priority, and usefulness. The original questions come from [M3](../m3/power-bi-analysis-requirements.md); the later [M4.1B release](../milestone-4-1b-findings.md) removes the old technical publication hold. This is a future build specification, not evidence that a visual or `.pbix` exists.

Use a restrained layout: roughly four to six primary visuals per page, consistent titles, visible N/D on every rate, accessible text labels, explicit UNKNOWN/unavailable styling without implying good/bad, no 3D charts, and bars instead of pies where comparison matters. Keep stable IDs and digests in tooltips/drill pages rather than primary tiles. Show “Declared two-case validation cohort; not ecosystem-representative” and the current limitation near every page title.

## Page 1 — Release Investigation Overview

**Decision question:** Which declared repositories have enough evidence for a bounded investigation answer, and which need more work? **Audience hypothesis:** release investigator or dependency maintainer.

| Visual / type | Bound fields and metric | Filter or interaction | Required label / limit |
|---|---|---|---|
| Context band | `dim_case.case_name`, `dim_release.package_name/version/release_time`, selected snapshot ID, rule and metric versions from manifest | Single case/release and published-snapshot selectors | “Validation snapshot; declared cohort only.” |
| Declared member and core collection cards | Distinct bridge members; MET-001 N/D from published output or verified member fact | Exact selected snapshot | Counts 2 pytest or 6 urllib3; core 2/2 or 6/6. |
| Historical context and candidate-emission cards | MET-002 and MET-008 N/D; separate candidate path | Exact selected snapshot | Declaration coverage is not adoption; candidate emission is detector activity, not incidents. |
| Finding-state bars | `fct_lifecycle_finding.lifecycle_category`, `finding_status`, distinct `finding_id` | Repository/category selection | UNKNOWN visible; bounded NO only as literal finding state; no positive finding. |
| Member investigation table | Bridge member/repository label plus `core_collection_complete`, declaration/paired/after-only counts, `candidate_count`, `unknown_finding_count`, `bounded_no_finding_count` | Repository selection; choose member for drill | Preserve zero-evidence members; show candidate and member evidence paths in separate columns. |
| Historical path summary | Member-level paired / AFTER_ONLY / unresolved counts from `fct_repository_investigation` | Member drill | Counts describe path state; AFTER_ONLY never means a pre-release pair or absence. |

Page slicers: case/release and one published snapshot are mandatory; repository and lifecycle category are optional contextual filters. Drill: repository → selected member/category finding → selected observation/ref and recorded support edge *if one exists*. Current `bridge_finding_evidence` is empty, so the drill must say “No explicit finding-support edge recorded” rather than asserting a supporting artifact. Tooltip: case, snapshot ID, member, stage, status, sufficiency, numerator/denominator where applicable, source/rule version and limitation. Do not show confirmed adoption, recovery, ecosystem impact, generic risk score, or stakeholder outcome KPI.

## Page 2 — Evidence & Uncertainty Diagnostics

**Decision question:** What prerequisite is missing, and why does PULSE remain uncertain? **Audience hypothesis:** evidence-method analyst or investigator.

| Visual / type | Bound fields and metric | Filter or interaction | Required label / limit |
|---|---|---|---|
| Finding-state matrix | Member × `lifecycle_category`; `finding_status`, `source_sufficiency_status`, reason | Category and repository | UNKNOWN, INSUFFICIENT, and bounded NO have distinct text and accessible patterns. |
| Historical-state bars/table | `paired_path_count`, `after_only_path_count`, `unresolved_path_count`, `ambiguous_path_count`; declaration indicator | Selected member and snapshot | Aggregate path counts only; no invented path-level pairing record. |
| Exact-ref observation table | `observation_type`, `repository_ref`, `path_ref`, `historical_position`, `declared_constraint`/`resolved_version`, event/retrieval times, quality and capture method | Member/source type | A declaration is not installed/resolved adoption evidence. |
| Selected source/task inventory | `fct_collection_task` required/optional, terminal status, source label, capture/retry counts; captured observation method where present | Source/capture type | Do not use global `dim_evidence_source` method counts as selected-snapshot denominators. |
| Evidence-gap diagnostic | Member finding/task/observation components plus MET-004/005/012/013/015 partial statuses | Member/category/source drill | Display observed components and unavailable reason; never label a partial component as its full governed metric rate. |

Page slicers: mandatory case/snapshot; repository and category; source type/capture method and historical state as contextual filters. Route: UNKNOWN/evidence gap → member/category → exact-ref observation or path summary → approved artifact locator/source. The current published marts expose member-level historical-state counts and observation refs, **not** a complete path-level paired/AFTER_ONLY/unresolved record or every selected artifact locator. Before promising a row-level path/artifact drill, M4.2 must validate a governed, publication-scoped detail projection or show the honest summary/ref with a documented gap. Distinguish actual bounded NO, unavailable source, INSUFFICIENT prerequisites, UNKNOWN, and any future explicit conflict; do not equate zero coded conflicts with no conflict. Do not rank source usefulness by capture volume. Tooltip includes snapshot, stage/question, source/capture method, ref/path, event versus retrieval time where present, and the missing prerequisite.

## Page 3 — Candidate & Review Quality

**Decision question:** Which detector outputs required qualification, what evidence produced them, and what was the review result? **Audience hypothesis:** reviewer or rule owner.

| Visual / type | Bound fields and metric | Filter or interaction | Required label / limit |
|---|---|---|---|
| Candidate/review summary | MET-008/009/010/011/022 from governed outputs; counts of distinct candidate and artifact IDs | Exact case/snapshot | urllib3: two candidates, one artifact, two inherited REJECT; pytest: zero candidates and 0/0 review rates unavailable. |
| Candidate table | One row per `candidate_id`; repository, category, `candidate_rule_id/version`, `source_origin`, `capture_method`, terminal status/reason | Rule, origin, disposition, repository | Two rows are two detector firings, **not** two independent incidents. |
| Artifact grouping | Distinct `artifact_id` with candidate count | Select artifact then candidate | One shared artifact for both urllib3 firings; do not multiply evidence count. |
| Review provenance detail | Candidate → original candidate/review, EXACT_EQUIVALENT basis, original timestamp, inheritance policy | Candidate drill only | Must use a governed publication-scoped lineage projection; current candidate mart does **not** expose this complete detail. Label “Inherited review evidence; no new reviewer action.” |

Page slicers: mandatory case/snapshot; repository, lifecycle category, rule ID/version, source origin, and review status/reason where relevant. Route: candidate → shared artifact → rule/source-origin span → inherited review → original review provenance. `fct_candidate_review` supports the first-level result, but full inheritance and artifact-locator detail require the controlled projection identified in the [data contract](power-bi-data-model.md). Do not silently substitute raw ingestion or claim a complete drill when unavailable. Tooltip shows snapshot, rule, source origin, terminal decision, capture method, evidence locator if approved, original review time, and limitations; original reviewer identity and personal information are unnecessary. REJECT means the candidate was not qualified as a positive event; it does not assert that no friction happened.

## Shared display rules

| State | Display |
|---|---|
| `UNKNOWN` | Visible literal state with missing-evidence context; never blank, zero, or “no issue.” |
| Metric `UNAVAILABLE_*` or `BLOCKED_STAKEHOLDER` | “Unavailable”/“Pending stakeholder validation” plus governed reason; no percentage. |
| `0/N` with N > 0 and READY | Show `0%` and `0/N`; describe the exact eligible population. |
| `0/0` | “Unavailable (0 eligible observations)”, not `0%`. |
| No candidate emitted | “No candidate emitted in selected snapshot”; keep finding status separate. |
| `REJECT` | Review disposition on an emitted candidate; inherited provenance flagged. |
| `INSUFFICIENT` | Required evidence incomplete; no conversion to bounded NO. |
| `NO_QUALIFYING_EVIDENCE_FOUND` | Bounded selected-stage NO with sufficient prerequisite context, not global absence. |

All rate visuals must show case, snapshot, metric ID/version, N/D, status, and unavailable reason. The five lifecycle categories are forensic evidence classes; dashboard ordering must not imply chronology or causality. Preserve the final accessibility/formatting and portfolio screenshot requirements for M4.2.
