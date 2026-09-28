# Power BI decision-view specifications (proposed, not built)

Audience and priority are **PENDING STAKEHOLDER / FUTURE PRODUCT VALIDATION**. The provisional user is an investigator/reviewer of a declared release case, with a possible product/evidence-method owner for aggregated diagnostics. Every visual shows case, cohort definition, observation window, source-plan/report version, numerator/denominator (or unavailable reason), and capture-method caveat. Drill-through reaches the preserved source link and assessment/review rationale. RLS, permissions, refresh and deployment are later requirements; no Power BI file exists now.

## Dashboard 1 — Release Investigation Overview

| Visual | Question; user/decision | Metric; grain; filter | Drill-down; interpretation; misuse risk |
| --- | --- | --- | --- |
| Declared cohort and outcome cards | Investigator: how many repositories are in scope and have defensible answers? Decide where further evidence is needed. | F0 count, MET-006; case × repository; case/release/window. | Member list → stage findings; outcome coverage is not impact rate or human completion. |
| Split investigation pathway | Evidence-method owner: where does collection/context/sufficiency/review stop? Choose source experiment. | F0–F5 with optional B1–B3; member, member-stage and candidate grains labeled separately; case/source plan. | Branch stage → member/task/candidate; do not read as linear user conversion or multiply branch percentages. |
| Finding-status mosaic | Investigator: which evidence categories are YES, bounded NO, UNKNOWN? Choose review queue. | Stage finding count/MET-012; case × repository × category × version; case/category. | Category → assessment/evidence; bounded NO does not mean event impossible; categories have no required chronology. |
| Repositories needing evidence table | Investigator: which member's next evidence question is specific? | MET-005/006 and UNKNOWN reasons; member-stage; case, category. | Member → missing task/ref/review; a suggested attention order is not a validated impact priority. |

## Dashboard 2 — Evidence & Uncertainty Diagnostics

| Visual | Question; user/decision | Metric; grain; filter | Drill-down; interpretation; misuse risk |
| --- | --- | --- | --- |
| Source-coverage matrix | Evidence-method owner: which source class is incomplete? Select acquisition test. | MET-004 with required/optional status; member × stage × source; case/source. | Cell → planned task/query/outcome; complete API query is not all relevant evidence. |
| Historical-context partition | Investigator: who has paired pre-release, after-only or unresolved context? | MET-002 plus subcounts; member; case/release. | Member → exact ref/path raw snapshot; after-only not release-time proof or negative denominator. |
| UNKNOWN-reason bars | Method owner: which missing prerequisites recur? | MET-013; member × stage × reason; case/category/source. | Reason → assessment/task/artifact; reasons may overlap, bars must not be summed as unique people/repos. |
| Stage sufficiency and conflict view | Investigator: which bounded answers are eligible, and which need conflict review? | MET-005/014; member-stage; case/category. | Assessment → source links; sufficient ≠ YES; conflict count unavailable if taxonomy absent. |

## Dashboard 3 — Candidate & Review Quality

| Visual | Question; user/decision | Metric; grain; filter | Drill-down; interpretation; misuse risk |
| --- | --- | --- | --- |
| Emission and disposition cards | Rule reviewer: how much candidate material and what terminal state? | MET-008/009/010/011/022; candidate and distinct-member grains labeled; case/rule. | Candidate → rule/version/review; acceptance is reviewed-emitted only, no recall claim. |
| Rule × source-origin matrix | Rule reviewer: is copied-upstream text driving rejected signals? | MET-009/010 by rule and coded text origin; candidate; rule/source/case. | Cell → artifact span and rationale; unresolved origin stays separate; one PR can cause two firings. |
| Rejection-reason distribution | Rule reviewer: what nonqualifying mechanisms recur? | Rejected candidate count/reason (MET-010 breakdown); candidate; case/rule. | Reason → review ledger; do not extrapolate from two Phase 2 emissions. |
| Review queue and provenance table | Investigator: what needs review and what evidence backs accepted items? | MET-011/021/023 where time valid; candidate/finding version; case/disposition. | Candidate/finding → artifact digest/source URI; duration is elapsed process time, not labor. |

No adoption or recovery rate card appears until its eligible population and qualifying source exist. “0 accepted in this reviewed set” may be displayed with denominator and limitation; “0 affected” may not. Comparative visuals default to within-case; cross-case mode explicitly shows selection and source-plan differences. Accessibility, usability and audience ordering require actual stakeholder feedback.
