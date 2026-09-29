# M2.5 executable SQL catalog

All queries live in `analytics/sql`. `scripts/run_metric_pack.py` executes them against the local PostgreSQL/dbt marts and records outputs under `data/validation`. Named `snapshot_id` parameters isolate the selected case. PostgreSQL CTEs, conditional aggregation with `FILTER`, `NULLIF` denominator guards, distinct candidate/artifact keys, and explicit member spines serve correctness; no window function or percentile is used merely for sophistication.

| Query | Decision question / grain | Mart or source / denominator | Key limitation |
|---|---|---|---|
| `metrics/member_coverage.sql` | Core, history, candidate-member coverage and density; case/member | `bridge_case_repository` joined to `fct_repository_investigation`; all declared members | History is declaration evidence, not adoption; density is candidates/member |
| `metrics/candidate_review.sql` | Acceptance, rejection, unresolved; case/candidate | `fct_candidate_review`; terminally reviewed or all emitted candidate IDs | 0/0 is NULL; two candidates can share one artifact |
| `metrics/collection_reliability.sql` | Required success, optional not-found, retries; case/task | `fct_collection_task`; separate required, optional terminal, attempted spines | No synthetic attempts or mixing optional with required |
| `metrics/partial_components.sql` | Observed counts for seven partial contracts; case/component | task and lifecycle facts; explicitly labeled observed denominator | Never yields a full contract rate |
| `diagnostics/investigation_funnel.sql` | Bounded evidence-processing stages; member, candidate, or member/category | repository, candidate and lifecycle facts; denominator per stage | F3/F4 are category-specific; F5 remains unavailable; no causal drop-off |
| `diagnostics/evidence_gaps.sql` | Which declared members lack context, candidates or bounded findings?; case/member | bridge, repository fact and dimensions; full declared cohort | Indicators are evidence states, not failure diagnoses |
| `diagnostics/source_coverage.sql` | Which source classes supplied selected captures?; case/source | selected `core.snapshot_artifact`, staged captures, source dimension; actual artifacts | Upstream release/PyPI captures have no member repository; dimension presence alone is excluded |
| `diagnostics/case_comparison.sql` | Side-by-side count/rate validation; case/snapshot | preaggregated repository, candidate, task facts; 2 and 6 members | Descriptive only; no normalized effects or generalization |
| `diagnostics/segment_inventory.sql` | Are planned segment cells populated?; dimension/cell | repository fact and dimensions; eight members | Sparse groups cannot support robust segment analysis |
| `validation/snapshot_scope.sql` | Select exactly the two frozen DRAFT case snapshots | core snapshot + case dimension | Blocks implicit latest-snapshot mixing |
| `validation/metric_assertions.sql` | Does the frozen golden evidence match?; case/snapshot | repository, candidate, task facts; explicit expected counts | Returns zero rows on pass; immutable frozen validation cases only |

The SQL assertions verify 2/6 member denominators; 1 paired member and six AFTER_ONLY paths; 2 candidate IDs from one artifact and one repository; 0/2 accepted versus undefined pytest acceptance; 38 UNKNOWN distinct from two bounded NO; 38 LEGACY_UNCLASSIFIED; zero fixture candidates; 54 tasks and zero retries. The Python result test also checks the generated metric statuses, values, snapshot isolation, and release-manifest hashes.
