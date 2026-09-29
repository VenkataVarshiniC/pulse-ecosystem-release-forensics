# M4.1B governed metric replay versus historical DRAFT baseline

The comparison joins each metric by case and contract ID. The left side is the original M2.5 result from two historical **DRAFT** snapshots; the right side is a fresh execution of all 23 unchanged `m2-5-metric-registry-v1` contracts against two new, case-scoped replay snapshots. There is no pooled cross-case snapshot: `core.analysis_snapshot` has one case foreign key, so the shared release ID groups two physical snapshots. The replay output is [`m4-1b-replay-metrics.json`](../../../data/validation/m4-1b-replay-metrics.json), SHA-256 `febd43d2586d421a1f9ef64ae1b710db9484794ab9bf1a684e92a78eeabb595f`.

`IDENTICAL` means status, numerator, denominator, and governed value are equal. `UNAVAILABLE_BOTH` means neither result has a governed value; it does **not** mean a zero observation. No metric is VALUE_CHANGED, STATUS_CHANGED, LEGACY_ONLY, or REPLAY_ONLY. The two explanatory component labels for MET-005 and MET-020 were clarified for the new replay output; the v1 contract, status, counts, and unavailable reason did not change.

| Contract | Pytest comparison | urllib3 comparison | Explanation |
|---|---|---|---|
| MET-001 Core collection coverage | IDENTICAL | IDENTICAL | The same verified selected tasks and member population are used. |
| MET-002 Historical context coverage | IDENTICAL | IDENTICAL | The same exact-ref captures and paired-path evidence are selected. |
| MET-003 Target-version evidence coverage | UNAVAILABLE_BOTH | UNAVAILABLE_BOTH | Eligible resolved-version provenance is absent; adoption remains UNKNOWN. |
| MET-004 Stage source completeness | IDENTICAL | IDENTICAL | Partial components describe overall tasks; a category-to-source map is absent. |
| MET-005 Stage evidence sufficiency | IDENTICAL | IDENTICAL | The replay has explicit 2 SUFFICIENT / 38 INSUFFICIENT assessments, whereas legacy has 38 LEGACY_UNCLASSIFIED. The numerical partial component remains 2/40; it is **not** an approved rate. |
| MET-006 Investigation outcome coverage | UNAVAILABLE_BOTH | UNAVAILABLE_BOTH | Outcome criteria still require stakeholder agreement. |
| MET-007 Recovery eligibility coverage | UNAVAILABLE_BOTH | UNAVAILABLE_BOTH | Recovery-eligible evidence is absent. |
| MET-008 Candidate emission coverage | IDENTICAL | IDENTICAL | Zero pytest candidates and two urllib3 candidates from one artifact. |
| MET-009 Reviewed candidate acceptance | UNAVAILABLE_BOTH | IDENTICAL | Pytest has a zero denominator; urllib3 has two inherited REJECT decisions. |
| MET-010 Reviewed candidate rejection | UNAVAILABLE_BOTH | IDENTICAL | Pytest has a zero denominator; urllib3's two decisions are inherited, not new reviews. |
| MET-011 Unresolved candidate share | UNAVAILABLE_BOTH | IDENTICAL | Pytest has a zero denominator; urllib3 has no unresolved candidate. |
| MET-012 UNKNOWN finding rate | IDENTICAL | IDENTICAL | Component counts remain 38/40; stakeholder question interpretation is pending. |
| MET-013 UNKNOWN reason distribution | IDENTICAL | IDENTICAL | UNKNOWN counts exist; controlled reason numerator is unavailable. |
| MET-014 Conflicting evidence rate | UNAVAILABLE_BOTH | UNAVAILABLE_BOTH | No governed conflict population exists. |
| MET-015 Missing-source contribution | IDENTICAL | IDENTICAL | UNKNOWN counts exist; per-source contribution is unavailable. |
| MET-016 Required-task completion | IDENTICAL | IDENTICAL | Frozen selected collection tasks are unchanged. |
| MET-017 Optional not-found share | IDENTICAL | IDENTICAL | Frozen selected collection tasks are unchanged. |
| MET-018 Retry incidence | IDENTICAL | IDENTICAL | Frozen selected collection attempts are unchanged. |
| MET-019 Verified resume reuse | IDENTICAL | IDENTICAL | Partial component remains unavailable as a governed rate. |
| MET-020 Deterministic replay success | IDENTICAL | IDENTICAL | Source replay audit exists; the metric's required governed replay audit mart does not. |
| MET-021 Accepted-finding provenance | UNAVAILABLE_BOTH | UNAVAILABLE_BOTH | There are no accepted positive findings. |
| MET-022 Candidate density | IDENTICAL | IDENTICAL | The replay retained two exact-equivalent firings in urllib3. |
| MET-023 Review resolution duration | UNAVAILABLE_BOTH | UNAVAILABLE_BOTH | Timestamp/eligible review population contract is unmet. |

Across 46 case-contract comparisons: **31 IDENTICAL, 15 UNAVAILABLE_BOTH, 0 other**. The replay has 17 READY outputs, 12 PARTIAL_EVIDENCE, 2 PARTIAL_PLATFORM, 10 UNAVAILABLE_EVIDENCE, 3 UNAVAILABLE_ZERO_DENOMINATOR, and 2 BLOCKED_STAKEHOLDER. These are output counts across two cases; the unchanged registry contains 10 READY, seven PARTIAL, five evidence-unavailable, and one stakeholder-blocked *contract definitions*. The three zero-denominator outputs are the pytest candidate ratios and remain NULL, never 0%. No apparent value stability licenses an adoption, recovery, or population claim.
