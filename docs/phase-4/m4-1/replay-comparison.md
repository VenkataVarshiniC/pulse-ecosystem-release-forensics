# Legacy DRAFT versus current-rule replay

The two old PostgreSQL snapshots remain DRAFT with `unrecorded_in_frozen_report`; the replay is a **separate offline result**, not a third database snapshot. Its rule manifest identifies current source bytes only. The same 142 frozen files, two cases, eight declared members, selected tasks/artifacts and exact-ref captures were used. Sixteen historical queries and eight captured files were checked offline; no additional history was retrieved. Source-level replay output is [`replay.json`](../../../data/processed/m4-1/replay.json).

| Dimension | Legacy DRAFT | New replay | Explanation |
|---|---|---|---|
| Members/cases | 8 / 2 | 8 / 2 | Case definitions unchanged. |
| Collection tasks and artifacts | Frozen manifest | Same verified captures | Raw root is required to equal selected frozen snapshots exactly. |
| Historical context | 16 path results | 16 pair checks; 8 file reparse checks | Exact refs and parsed target observations matched; original attempt metadata retained. |
| Candidates / emitting members | 2 / 1 | 2 / 1 | Full candidate payload exact, but replay IDs newly qualified by rule release. Both firings share one PR artifact. |
| Candidate equivalence | Unavailable | 2 EXACT_EQUIVALENT; 0 changed/new/missing | Full normalized payload comparison, not forced count matching. |
| Reviews | 2 REJECT | 2 inherited REJECT, 0 REVIEW_REQUIRED | Original UUID, note, reason, time and source basis retained as inheritance, not new review. |
| Sufficiency | 2 SUFFICIENT; 38 LEGACY_UNCLASSIFIED | 2 SUFFICIENT; 38 INSUFFICIENT | New current-rule assessment vocabulary only; old rows not rewritten. |
| Findings | 2 bounded NO; 38 UNKNOWN | 2 bounded NO; 38 UNKNOWN | Recomputed from verified collection/history and inherited valid review evidence; agreement is observed, not a replay target. |
| Adoption / recovery | No qualified rate | No qualified rate | Target-version installation and recovery-eligible sources remain missing. UNKNOWN never becomes zero adoption. |
| Metrics | 23 contracts evaluated against old DRAFT marts | **Not evaluated against a replay snapshot** | M2.5 metric definition stays v1, but old result is not a new metric replay. See publication gate. |

The two bounded NO outcomes are pytest friction and remediation under paired pre-release path context. All adoption-readiness, observed-adoption and recovery stages remain UNKNOWN where evidence is insufficient. Lifecycle categories are not required to occur in order; a finding is not a causal sequence. Current rule execution produces no accepted event.

The replay has no new PostgreSQL `core.candidate`, `core.lifecycle_finding`, `core.analysis_snapshot` or dbt mart rows. Existing loader branches explicitly require the two frozen candidates, review notes, and historical IDs; simply relabeling them with a new rule version would falsify lineage. An additive governed replay loader/snapshot selection and dbt/metric execution are prerequisites before G6/G7 can pass. No metric numerator or denominator from legacy DRAFT marts is represented as a replay value.
