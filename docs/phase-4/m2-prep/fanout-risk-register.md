# Fan-out risk register

Every published rate declares its numerator and denominator grain before a join. Build a distinct-key CTE at that grain, aggregate lower-grain rows there, then join to the frozen membership spine. Bridges are for lineage/drill-through and must not be placed on the denominator path. Power BI uses one-way dimension-to-fact filters and governed measures, not automatic many-to-many inference.

| Risk | Demonstrated or possible mechanism | Protection and gate |
| --- | --- | --- |
| One PR artifact → two candidate firings | Observed in urllib3 baseline; naive artifact join counts two artifacts or two members. | Candidate count uses distinct candidate_id; artifact count distinct artifact_id; member count distinct case-version/repository. Golden 2 candidates, 1 artifact, 1 emitting repository. |
| One member → many tasks | Task join multiplies member denominator and stage rows. | Aggregate required core outcomes per member; left join once to membership; assert 2/6 members. |
| One candidate → several review events/cycles | Candidate acceptance rate duplicates one emission. | Snapshot selects one terminal cycle/decision per candidate; unique test and duplicate-terminal blocker. |
| One finding → multiple support edges | YES count or provenance rate inflated. | Count finding_id once after EXISTS qualified support; support bridge isolated. |
| One artifact → several observations | Historical before/after and path state could duplicate content coverage. | Count distinct member with qualifying observation; paired status separate from after-only. |
| One member → five stage categories | Member coverage inflated by category join. | Stage metrics at member-stage/question grain; member metrics reduced to member first. |
| Reused task → multiple snapshots | Fact task row could duplicate operational task count. | Task fact keyed by original run/task; snapshot-use bridge only for explicit per-snapshot filtering. |
| Overlapping UNKNOWN reasons | Reason percentages can exceed 100% if multi-label. | Denominator distinct UNKNOWN member-stage/question; label overlap and no sum of reason percentages. |
| Two case versions of one member | Silent pooling changes denominator. | Snapshot binds one case_version_id; cross-version comparison is explicit. |
| Connector-assisted/fixture captures | A source join might label validation as unattended success. | Filter by actual artifact.capture_method and verified collector task identity; separate displayed classes. |

Tests compare pre-join and post-join distinct key counts, assert mart unique grain and reconcile [golden values](golden-validation-values.md). One bad join blocks affected publication; DISTINCT at the final SELECT alone is insufficient when sums or statuses were already corrupted.
