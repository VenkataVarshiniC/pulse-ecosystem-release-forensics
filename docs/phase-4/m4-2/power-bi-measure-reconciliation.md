# M4.2 measure and fanout reconciliation

Status: **PASS**. PostgreSQL source reconciliation, live semantic-model queries, and Power BI Desktop validation agree for both approved published snapshots. Cross-case totals remain descriptive only; no pooled rate is reported.

| Check | pytest | urllib3 | Both, descriptive only |
|---|---:|---:|---:|
| Declared members | 2 | 6 | 8 |
| Core complete | 2/2 | 6/6 | — |
| Historical declaration members | 1/2 | 1/6 | — |
| Paired pre-release members | 1/2 | 0/6 | — |
| Candidate-emitting members | 0/2 | 1/6 | — |
| Required tasks succeeded | 11/11 | 27/27 | — |
| Candidate IDs | 0 | 2 | 2 |
| Distinct candidate artifacts | 0 | 1 | 1 |
| Accepted / terminally reviewed | 0/0 → Unavailable (0 eligible observations) | 0/2 → Inherited review · 0% (0/2) | no pooled rate |
| Rejected / terminally reviewed | 0/0 → Unavailable (0 eligible observations) | 2/2 → Inherited review · 100% (2/2) | no pooled rate |
| Findings | 10 | 30 | 40 |
| UNKNOWN findings | 8 | 30 | 38 |
| Bounded NO findings | 2 | 0 | 2 |
| Positive findings | 0 | 0 | 0 |
| SUFFICIENT | 2 | 0 | 2 |
| INSUFFICIENT | 8 | 30 | 38 |

The repository virtual environment's scripts/reconcile_m4_1b.py --check passed with two cases, eight members, two candidates, one artifact, two inherited REJECT reviews, 40 findings, 38 UNKNOWN, two bounded NO, 46 metric outputs, and zero bridge_finding_evidence rows. The replay has 54 task rows, including shared upstream tasks with NULL repository. Separate read-only SQL checks found one bridge match per each of the eight member-investigation rows, two candidate rows, 40 finding rows, and 11 observation rows; task counts were preserved under direct snapshot scope. The composite bridge key was unique for all eight members.

The two urllib3 candidates share one artifact and inherit two REJECT dispositions. Desktop validation preserved this 2-to-1 grouping and made the inherited-review wording explicit. They are not two independent incidents, and REJECT does not establish absence of migration friction. The zero-edge finding bridge means “No explicit finding-support edge recorded,” not “no supporting evidence exists.”

The 35 DAX measures aggregate governed flags/IDs and guard presentation against multi-snapshot rate pooling. Scope Selected requires one snapshot and one case. Acceptance Display and Rejection Display test the terminally reviewed denominator before formatting a percentage. Finding Cell surfaces finding status and sufficiency while returning blank for out-of-scope empty combinations. No DAX formula recreates the SQL/dbt eligibility contract. Desktop validation confirmed the expected candidate and review values for both snapshots and that the repaired cards preserve complete denominator text without truncation.
