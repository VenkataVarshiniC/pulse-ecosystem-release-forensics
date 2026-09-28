# Readiness of all twelve planned Power BI visuals

This is a **visual feasibility audit**, not a Power BI build. Classification considers metric, denominator, data, variation and misleading risk together. Even a READY view remains implementation-gated by Phase 3 HOLD and needs audience testing. The visual names map to [Milestone 1 plan](../power-bi-dashboard-plan.md).

| Dashboard / visual | Metric and denominator | Data / variation | Misleading risk | Readiness |
| --- | --- | --- | --- | --- |
| 1 Declared cohort/outcome cards | Cohort count valid; MET-006 definition unvalidated | 2/6 members, outcome N unavailable | Could depict “complete” without user-approved question set | **BLOCKED_STAKEHOLDER** for outcome card; cohort count READY_WITH_LIMITATION. |
| 1 Split investigation pathway | F0–F4/B1–B3 bounded, F5 unavailable | Stage and candidate counts available but mostly 0/UNKNOWN | Linear conversion/branch-grain confusion | **READY_WITH_LIMITATION** if F5 unavailable and branches labeled. |
| 1 Finding-status mosaic | MET-012 per reported category, not completion-wide | 40 rows; UNKNOWN vs two bounded NO | Could read bounded NO as no real-world event | **READY_WITH_LIMITATION**. |
| 1 Repositories needing evidence | MET-005/UNKNOWN reason; no validated priority | Member status exists, stage-specific reason sparse | Implies impact/attention ranking | **BLOCKED_STAKEHOLDER** for ranking; evidence table could be diagnostic only. |
| 2 Source-coverage matrix | MET-004 required-set rate not yet valid | Source statuses exist, but no frozen stage→source map | Complete collection falsely read as sufficiency | **BLOCKED_DATA** for metric view; descriptive task-status matrix possible. |
| 2 Historical-context partition | MET-002 1/2 and 1/6; subcounts | Paired/after-only/unresolved vary | After-only conflated with release-boundary proof | **READY_WITH_LIMITATION**. |
| 2 UNKNOWN-reason bars | MET-013/015 denominators not linked to stage reasons | Generic text, repository labels only | Overlapping reasons shown as exclusive causes | **BLOCKED_DATA**. |
| 2 Stage sufficiency/conflict | MET-005 valid per category; MET-014 unavailable | Sufficiency varies only in pytest friction/remediation; conflicts uncoded | Zero conflict code mistaken for no conflict | **READY_WITH_LIMITATION** for sufficiency; **BLOCKED_DATA** for conflict. |
| 3 Emission/disposition cards | MET-008–011/022; pytest reviewed D=0 | Two urllib3 firings, one artifact | 0/0 rendered as 0%; 0/2 generalized | **READY_WITH_LIMITATION** with case-specific unavailable state. |
| 3 Rule × source-origin matrix | MET-009/010 by rule/origin | One firing per rule; both one copied-source PR | Looks like rule ranking from dependent N=2 | **DEFER** until broader coded artifact variation. |
| 3 Rejection reasons | Two terminal rejects, different reasons | N=2; no repeated reason | Percent bars imply stable distribution | **READY_WITH_LIMITATION** as two-case annotations, not rate ranking. |
| 3 Review queue/provenance | MET-011 current; MET-021 D=0, MET-023 time absent | Rejected records traceable; no accepted support chain | Implies accepted provenance/time metric exists | **READY_WITH_LIMITATION** for review ledger; positive-provenance and duration **BLOCKED_DATA**. |

No observed-adoption or recovery rate card is ready. Dashboard audience, visual order, detail level and decision use remain **BLOCKED_STAKEHOLDER** globally. The current dataset could support a truthful case diagnostic, but most “executive” comparisons would be visually polished and analytically weak.
