# Product Analytics traceability

| Analytical question | Metric contract | SQL/dbt logic | Replay validation | Dashboard consumption |
|---|---|---|---|---|
| Was the planned core source set collected? | MET-001, MET-016–018 | M2.5 `analytics/sql` and M2.4 source/coverage marts | Same frozen task and capture population, 142 hashes, 30 source table fingerprints unchanged | Withheld until a new replay snapshot reaches publication. |
| Is an exact-ref declaration visible? | MET-002 | Historical path/intermediate and member marts | 16 pairing checks and 8 exact-ref file reparses; 2/8 declaration evidence, 1/8 paired pre-release member | Prospective member/path drill, not adoption. |
| What was emitted and reviewed? | MET-008–011, MET-022 | Candidate/review marts and M2.5 numerator/denominator SQL | 2 exact-equivalent candidates, both inherited REJECT from one PR; pytest 0/0 precision remains unavailable | Prospective origin-aware candidate drill; current DRAFT mart is not a replay mart. |
| Which stage answer is supportable? | MET-004/005/012/013/015 partial | Assessment/finding marts and diagnostic SQL | Recomputed 2 SUFFICIENT/bounded NO, 38 INSUFFICIENT/UNKNOWN; reason taxonomy remains incomplete | Prospective uncertainty diagnostics with visible missing prerequisites. |
| Did adoption/recovery or useful completion happen? | MET-003/006/007 | Contract marks evidence unavailable or stakeholder blocked | No new qualifying source and no approval; replay does not infer zero | Suppress rate/outcome tiles. |

The 23-metric registry is unchanged at `m2-5-metric-registry-v1`: 10 READY, seven PARTIAL, five evidence-unavailable, one stakeholder-blocked **contract statuses**. There is no replay PostgreSQL snapshot, so no new 23-contract result, numerator/denominator set or replay metric baseline fingerprint exists. Existing M2.5 values refer only to the two historical DRAFT marts and cannot close this gap. The independent offline `Phase2Report` coverage metrics are forensic report values, not M2.5 mart metric execution.
