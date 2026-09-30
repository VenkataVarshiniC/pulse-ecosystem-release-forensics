# Phase 3 → M5.4 implementation trace

The [Phase 3 requirement baseline](../../phase-3/requirements-specification.md) and [M5.1 product mapping](../m5-1/requirements-to-product-traceability.md) remain authoritative. This is an **implementation evidence extension**, not a change to requirement priority or a stakeholder sign-off. Every detail endpoint below is under `GET /api/v1/investigations/{case_version_id}` and requires exact `snapshot_id`; repository descendants also require `{repository_id}`. `L/O/R/E/F/C/P` mean list, overview, repository, evidence, finding, candidate and provenance screens. `Live` means the published-stack walkthrough plus [read-only API/DB reconciliation](../../../scripts/validate_m5_4_live.py); `regression` means existing deterministic contract tests. G8 remains `NOT_YET_VALIDATED` for all rows.

| Phase 3 requirement | M5.1 capability / check | M5.2 read or guard | M5.3 screen | M5.4 evidence / boundary |
| --- | --- | --- | --- | --- |
| BR-001 bounded release/cohort | P-01 | investigations list/detail | L/O | Live 2 cases, 8 declared members; PASS |
| BR-002 distinguish answer states | P-05/06 | repository/findings | O/R/F | Live 38 UNKNOWN, 2 bounded NO, 0 positive; PASS for current states |
| BR-003 source/human chain | P-04/07 | candidate/artifact/finding | F/C/P | Candidate lineage live; no supported positive finding edge; PARTIAL |
| BR-004 compare declared members | P-01 | investigation detail | O | Literal 2/6 members live; decision value unvalidated |
| SR-001 show release context | P-01 | investigations list/detail | L/O | Release/window/snapshot and stable breadcrumb live |
| SR-002 inspect provenance | P-03/04 | evidence/artifact | E/P | Method, ref, clocks, digest, task/run live |
| SR-003 reasoned human review | P-08 | guarded candidate review POST | C | Published read-only live; eligible authorized DRAFT write deferred |
| SR-004 explain UNKNOWN | P-05/06 | finding/repository | R/F | Incomplete sufficiency/reason live; detailed missing-source taxonomy partial |
| SR-005 attention/override | deferred | none | none | Should; no validated owner/factors; not implemented |
| SR-006 bounded closure | P-05 | finding | F | No completion/merge equivalence; owner/closure test deferred |
| FR-001 case/window/membership | P-01 | investigations list/detail | L/O | Existing published scope live; case creation outside current UI |
| FR-002 planned tasks/outcomes | P-02/03 | repository/evidence | R/E | Task outcomes live; source-unavailable absent in current data |
| FR-003 raw capture identity | P-03/04 | artifact | E/P | Method/digest/task/run live; raw immutability from prior regression |
| FR-004 exact-ref history | P-02 | repository | R | 1 PAIRED, 6 AFTER_ONLY, 9 UNRESOLVED records live; correct distinction |
| FR-005 declaration vs resolution | P-02 | repository | R | Separate fields and unavailable resolved version live |
| FR-006 question sufficiency | P-05/06 | finding | F | 2 sufficient/38 insufficient live; conflict case not present |
| FR-007 tentative candidate/origin | P-07 | candidate/artifact | C/P | Two copied-upstream firings from one artifact live |
| FR-008 review/accepted finding separation | P-07/08 | candidate; review POST guard | C/F | Inherited REJECT visible; no ACCEPT; DRAFT write deferred |
| FR-009 YES/NO/UNKNOWN guard | P-05/06 | finding | O/R/F | UNKNOWN and bounded NO live; positive case unavailable |
| FR-010 reproducible report/gaps | P-01/05 | investigation/repository/finding | O/R/F | API/DB reconciliation and version context live; report replay prior evidence |
| FR-011 attention override | deferred | none | none | Should; no current product control |
| FR-012 recovery evidence/window | deferred | finding | F | Should; eligible recovery source/denominator absent, so no rate claim |
| NFR-001 navigable chain | P-04 | artifact/candidate/finding | E/F/C/P | Candidate → artifact complete; positive finding edge untestable |
| NFR-002 reproducibility | P-09 | versioned scope | O/F/P | Frozen IDs stable across 131 GETs; deterministic replay prior evidence |
| NFR-003 integrity/single review | P-08/09 | review guard + typed reads | C/F | Published write disabled; no live mutation; regression guards |
| NFR-004 failure transparency | P-06/10 | repository/finding/error contract | R/E/F | Scoped errors and outage/retry live; source-unavailable fixture only |
| NFR-005 safe source handling | P-03/04 | artifact locator policy | E/P | Public reference/method shown; no credential in captured screens; broader private-source policy pending |
| NFR-006 rule traceability | P-05/07 | scope/finding/candidate | O/F/C | Rule/version visible; change-impact exercise deferred |

Technical navigation evidence cannot validate the intended actor, utility, decision ownership, or acceptance wording. The four partial M5.4 checks and future-data conditions are listed in [acceptance results](product-acceptance-results.md); stakeholder reconciliation remains a separate gate.
