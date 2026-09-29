# M3 stability and M4.1 gates

The replay verifies the same frozen forensic population only; M3's separate public PR workflow sample was not re-run or joined to the forensic cohort.

| M3 observation | Classification | Replay basis / limit |
|---|---|---|
| Collection versus decision coverage | STABLE | 8/8 selected core collections, but only 2/40 bounded findings; 38 UNKNOWN. |
| Historical-context limitation | STABLE | 16 path-scoped pairings and eight exact-ref file captures rechecked; 2/8 declaration evidence, only 1/8 paired pre-release member. |
| Candidate/review pattern | STABLE | Two new-ID candidate firings from one PR, exact-equivalent, both inherited REJECT; no accepted event. |
| UNKNOWN dominance | STABLE | 38/40 UNKNOWN, two bounded NO. Incomplete history or missing stage source never becomes NO. |
| Copied-upstream hypothesis | STABLE as a bounded hypothesis | Both candidate excerpts retain explicit copied-upstream marker; two firings are dependent. This does not establish detector recall or a population rate. |
| Metric availability | STILL_UNAVAILABLE for replay snapshot | Registry remains 10 READY/7 PARTIAL/5 evidence-unavailable/1 stakeholder-blocked, but those contract statuses are not replay metric results. No replay mart/snapshot or 23-contract execution. |

| Gate | Decision | Evidence and unresolved work |
|---|---|---|
| G1 frozen input integrity | PASS | 142/142 file hashes and canonical frozen manifest verified; source evidence table fingerprints unchanged. |
| G2 explicit rule provenance | PASS for offline replay | Current source commit, 18 rule/config/implementation file hashes, manifest digest, candidate/finding IDs recorded. This does not resolve legacy historical versions. |
| G3 deterministic replay | PASS for offline replay | Two full runs produced byte-identical JSON; pinned source parser/pairing and finding code verified. No database model replay is claimed. |
| G4 candidate/review lineage | PASS for offline replay | 2 EXACT_EQUIVALENT; original review UUIDs/decisions linked to new candidate IDs under `exact-candidate-v1`. |
| G5 finding lineage | PASS for offline replay | `build_phase2_report` reevaluated current rules from verified collection/history and inherited reviews: 38 UNKNOWN, 2 bounded NO. No DB finding version exists. |
| G6 metric/model versioning | FAIL | Existing M2.5/M2.4 versions are known, but no all-23 metric run or model fingerprint exists **for a replay snapshot**. |
| G7 governed snapshot publication | FAIL | No new PostgreSQL snapshot, dbt replay mart rows, immutable publication fingerprint or state transition. Both historical snapshots remain DRAFT. |
| G8 stakeholder/audience validation | HOLD | No genuine response export/interview evidence found in authorized repository material. |

**Publication decision: HOLD_NO_GOVERNED_SNAPSHOT. Power BI eligibility: PUBLICATION_HOLD.** G1–G5 establish a bounded replay artifact, but G6/G7 block publication. G8 independently blocks a dashboard build. A future additive replay loader/model integration would need snapshot-isolated candidate/review/finding rows, all 23 metric contracts executed and reconciled, and immutable release fingerprinting before reevaluating these gates. The existing frozen-specific loader must not be used to relabel old rows.
