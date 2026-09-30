# M5.4 product acceptance results

These are technical implementation checks of the [M5.1 criteria](../m5-1/product-acceptance-criteria.md), using the actual local PostgreSQL → FastAPI → React stack and two allowlisted `PUBLISHED_VALIDATION` snapshots. They are **not stakeholder UAT**. `PARTIAL` means a specified aspect could not be demonstrated with the current published data or current read-only product.

| Check | Result | Observed result and limit |
| --- | --- | --- |
| P-01 Bounded investigation | PASS | List showed exactly two published cases; overviews showed pytest 2 and urllib3 6 declared members. Browser route, refresh and breadcrumb retained the selected snapshot. |
| P-02 Repository | PASS | Declaration, resolved observation, history state, task outcome, candidate count and five findings stayed distinct. `AFTER_ONLY` was not called a pair; an out-of-cohort ID returned `NOT_FOUND_IN_SELECTED_COHORT`. |
| P-03 Evidence | PASS | Explorer showed source grouping/filtering, ref/path, capture method, digest, task outcome and separate event/retrieval clocks. Missing event time remained unavailable. The API pagination cursor was exercised with limit 1. |
| P-04 Provenance | PARTIAL | Candidate → artifact → source/public reference → capture method/digest/clocks and return worked. Current UNKNOWN/NO findings have no recorded support edge; the UI says so. There is no current positive supported finding with which to test a complete finding-specific edge. |
| P-05 Bounded finding | PASS | API/DB reconciliation found 38 UNKNOWN, two sufficient bounded NO and zero positive across 40. UI displayed status, sufficiency, reason and rule separately; no positive support was fabricated. |
| P-06 Uncertainty and denominator | PARTIAL | UNKNOWN, incomplete history and no-candidate remained distinct; API failure did not become an empty result. No live `SOURCE_UNAVAILABLE`, `CONFLICTING` or eligible 0/0 metric is present in these published cases, so those live displays were not claimed as exercised. Existing frontend tests cover source-unavailable copy. |
| P-07 Review lineage | PASS | Both urllib3 firings came from one copied-upstream artifact, each showed inherited REJECT and original review/candidate IDs; no active review control appeared. |
| P-08 Guard review | PARTIAL | Published pages are read-only, `review_write_enabled=false`, and M5.2 regression covers the published write guard. The future authorized DRAFT review exercise is not testable in this published-only walkthrough. No real review was submitted. |
| P-09 Preserve frozen evidence | PASS | M5.4 live requests were GET-only; PostgreSQL reconciliation used a read-only transaction. Browser retry did not submit a review or run a collector. No evidence/schema/migration files changed. |
| P-10 Empty and error states | PARTIAL | Zero-candidate member, absent support link, invalid snapshot, out-of-cohort repository, database unavailable and network failure each had contextual treatment; retry preserved route. No live source-unavailable record exists, and the no-cases condition was not induced against published data. |

Six checks pass and four are partial; none fails. This supports the M5.4 technical integration decision, while the specified future-data and stakeholder conditions stay open. G8 remains `NOT_YET_VALIDATED`.
