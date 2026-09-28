# Workflow data-quality audit

The [analysis helper](compute_workflow_baseline.py) reads **only the frozen JSONL** and validates its row-level contracts before computing metrics. Its machine-readable audit is in [workflow-metrics.json](workflow-metrics.json). A separate read-only comparison with the frozen Phase 3 candidate frame verified selected IDs and UTC durations; it does not feed metric computation.

| Check | Result |
| --- | --- |
| Expected observations and sample labels | 27/27; 20 `base`, seven `discussion`; no other labels. |
| Composite PR identity | 27 unique sample × repository × PR keys; canonical URLs match row identities. Separate frame comparison: all 27 selected IDs match. |
| Required coded fields / enums | Identity, status, mechanism, evidence, work and human fields present; allowed initiator, mechanism and outcome values checked. |
| Disposition consistency | 13 merges have null close reason; 14 non-merge closures have explicit reason; all 27 terminal at cutoff. |
| Human and provenance consistency | Interaction flag agrees with positive comment/review count; approvals imply visible interaction; nine downstream statements have a coded kind; copied upstream text has release-note/changelog presence. |
| Timestamp and duration | Helper checks all 27 durations nonnegative; separate frame audit confirms creation and terminal UTC timestamps and 27/27 elapsed-time agreement within 0.11 hour (rounding tolerance). |
| Missingness | Scalar previous/proposed versions null in four grouped PRs; their `dependency_changes` lists preserve component versions. Downstream statement kind null in 18/27 because no downstream statement was coded. `lockfile_regeneration` null in 27/27: changed lockfile does not establish regeneration method. |

**Coding ambiguities, retained rather than recoded:** `reason_for_close=no_longer_needed_per_bot` appears in five PRs, but only four include a visible human bot command (one base, three discussion); the other base PR is kept as “other explicit bot close.” The four command cases show a rebase request and up-to-date reply, **not** completed rebase. `test_results` and `ci_check_discussion` are not a systematic check-run history. Zero coded base code/test/config changes means none in the reviewed public diffs, not none in private work. `downstream_statement_kind=substantive_review_comment` captures one base and one discussion PR; approvals and commands are not automatically substantive technical discussion.

The source SHA-256 is `fa56ed46a7a8269046c92e0100740d9d5b8028908046943169a0925847968972` and is saved in the machine result. The frame comparison returned `selected_match=True`, `selected_count=27`, `duration_mismatch=0`. The frozen Phase 3 records are read-only for this milestone.
