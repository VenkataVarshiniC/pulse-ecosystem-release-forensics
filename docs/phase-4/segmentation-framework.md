# Segmentation framework

Segments explain method differences and point to a next investigation. They are not causal treatments or priority scores. Each view includes case/cohort selection, source plan, denominator and small-cell counts.

| Dimension | Availability | Grain/derivation | Decision use and caution |
| --- | --- | --- | --- |
| Package and release | Current | Declared case/release identity. | Compare cases descriptively; release cases have different windows and selection frames. |
| Repository | Current | Canonical identity within case membership. | Inspect traceable gaps; same repository in two cases is two investigations. |
| Evidence source and capture method | Current | Task/source/artifact; collector vs connector-assisted vs fixture. | Find acquisition gaps; exclude fixtures and label connector-assisted evidence separately from unattended performance. |
| Historical support | Current/derivable | Exact-ref observations: paired pre-release, after-only, unresolved. | Test context gap; `historically_supported` broad flag alone does not establish release-boundary sufficiency. |
| Collection status | Current | Planned task outcome, required flag, source class. | Diagnose reliability; optional 404 stays separate. |
| Candidate rule and source origin | Rule current; text-origin partly derivable with reviewed provenance | Candidate-level, rule version and artifact span. | Investigate copied-upstream mechanism; do not silently classify all uncoded text. |
| Review disposition/reason | Current | Terminal candidate review (or unresolved). | Find rule-specific review patterns; repeated firings in one PR are dependent. |
| Lifecycle category and UNKNOWN reason | Current/derivable | Case × repository × category assessment/finding. | Show missing prerequisites; categories need not be chronological. |
| Selection case | Current | Frozen cohort frame and rationale. | Expose convenience sampling; no population claims. |
| Resolved target version, downstream release, human disposition | Future, not comprehensively captured | Would require qualified source/context/window or actual user action. | Keep adoption/recovery/completion views unavailable until method and authority validated. |
| Role, trust, burden tolerance, business value | Stakeholder-dependent | Primary research / future product validation. | Do not infer from public PR authors or current reports. |
