# Frozen Phase 2 reconciliation values

These are the exact bounded values from [M1A baseline](../baseline-analysis/metric-computability.md) and [grain audit](../baseline-analysis/grain-validation.md). They are acceptance anchors for an **authorized future load**, not new database results. A governed metric/method version change must publish side-by-side differences with reason; never silently replace these anchors.

| Check | pytest 8.0.0 | urllib3 2.0.0 |
| --- | ---: | ---: |
| Frozen members | 2 | 6 |
| Core collection | 2/2 | 6/6 |
| Historical exact-ref target declarations | 1/2 | 1/6 |
| Stronger paired pre-release path | 1/2 | 0/6 |
| Candidate-emitting members | 0/2 | 1/6 |
| Candidate IDs | 0 | 2 |
| Accepted reviewed candidates | 0/0, rate unavailable | 0/2 |
| Rejected reviewed candidates | 0/0, rate unavailable | 2/2 |
| Required tasks complete | 11/11 | 27/27 |
| Optional verified not_found | 1/4 | 5/12 |
| Tasks with retries | 0/15 | 0/39 |
| Deterministic replay attempts matching | 2/2 | 2/2 |

Across both cases: 8 frozen members, 54 planned tasks, 40 reported member-category findings. The two urllib3 candidates cite **one PR artifact** and must remain two candidate rows but one artifact count and one emitting member. Observed adoption is **UNKNOWN/unavailable**, not 0%; recovery is **UNKNOWN/unavailable**, not 0%. The urllib3 after-only declaration is contextual evidence, not a negative release-window eligibility anchor. No positive YES support chain exists in these cases, so positive-link integrity needs a later governed fixture or source-backed case.
