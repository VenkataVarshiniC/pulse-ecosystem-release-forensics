# Cohort and segmentation feasibility

The unit is a **frozen case membership**, not all dependent repositories. No cohort here estimates ecosystem prevalence. See [Phase 4 cohort definitions](../cohort-framework.md) and [segments](../segmentation-framework.md).

| Proposed cohort | Feasibility | Current assignment and variation | Decision limitation |
| --- | --- | --- | --- |
| Release | **Constructible** | pytest 2, urllib3 6. | Two purposive/rule-based validation cases differ in source context; descriptive only. |
| Package family | **Constructible** | One package per case. | Confounded with case; no within-case variation. |
| Evidence coverage high/partial/insufficient | **Partially constructible** | Core coverage and stage sufficiency available. | No frozen general “high” source-set threshold; stage-specific labels only. |
| Historical pre-release paired / after-only / unresolved | **Constructible** | pytest 1/0/1; urllib3 0/1/5. | After-only contextual support is not a negative finding denominator. |
| Candidate path | **Constructible** | pytest 0 emitted; urllib3 1 member with 2 emitted, both rejected; no accepted/unresolved. | Sparse and one artifact; no impact or recall interpretation. |
| Source availability | **Constructible for planned classes** | Core complete for all; optional 404 varies 1 vs 5 tasks; downstream releases not planned. | “Not collected” is not source absence. |
| Selection method | **Constructible but invariant** | Both `rule_based` convenience frames. | No useful within-baseline segmentation or representativeness. |
| Actual adoption / recovered vs not recovered | **Invalid with current data** | No qualified target-version or eligible recovery evidence. | Do not create from declarations, PR merge, or UNKNOWN. |

## Segmentation-dimension audit

| Dimension | Classification | Variation / value now |
| --- | --- | --- |
| Dependency/release | Usable now | Two values but exactly one per case; case effects inseparable. |
| Repository | Usable now | Eight case-member identities; useful for drill-through, not inference. |
| Evidence source / capture method | Source usable; capture method **invariant** in Phase 2 | Source classes vary. All analyzed live attempts are `collector`; no connector-vs-collector outcome comparison. |
| Historical-support status | Derived/usable | Paired, after-only, unresolved variation; strongest evidence-gap segment. |
| Candidate rule | Sparse | Two rule firings from one PR, one per rule. |
| Review disposition/reason | Sparse | Two rejected; no accepted or unresolved; reason codes differ. |
| Lifecycle category | Usable now | Five report categories × eight members; outcomes heavily UNKNOWN. |
| Collection status | Usable now | Required success and optional not-found; no retry/failure variation in these runs. |
| UNKNOWN reason | Partly derived | Generic stage text plus multi-label repository missing sources; no stage-specific coded taxonomy. |
| Cohort-selection case | Usable but narrow | Both frozen convenience `rule_based`; no organizational cohort. |
| Resolved version, downstream release, human disposition | Future | Missing source/role; no valid segment. |
| Stakeholder role, trust, burden or value | Stakeholder-dependent | No primary research; cannot segment. |

Structurally present but invariant dimensions can still validate joins; they cannot explain outcome variation in this baseline.
