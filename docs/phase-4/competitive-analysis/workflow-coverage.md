# Workflow coverage and temporal boundary

The path below is a **conceptual investigation map**, not a universal process, conversion funnel or causal chain. A compatibility response can precede a later public friction report. “Post-release” here means a release has occurred and is being investigated; proposed PR and pre-merge checks may happen after that release. Cells reference the [capability matrix](competitive-capability-matrix.md) and [official sources](source-ledger.md).

| Workflow question | Documented tools and overlap | What still requires assembly or verification |
| --- | --- | --- |
| Does a repository depend on the package? | GitHub graph, Snyk, Socket, Sonatype and deps.dev expose inventory/graphs [S03,S13,S15,S18,S19]. | Historical ref and environment may differ from current view. |
| Is a new release available? | Dependabot, Renovate, PyPI and deps.dev [S01,S08,S15,S16]. | Registry publication does not prove downstream use. |
| Was an upgrade proposed? | Dependabot, Renovate, Mend/Snyk/Sonatype fixes [S01,S08,S11,S14,S20]. | Proposal state differs from merge or installed version. |
| What did pre-merge validation show? | GitHub dependency review, Actions logs, Snyk/Socket/Sonatype checks [S04,S06,S14,S17,S20]. | Check history/ref/retention and relevance to a later release case. |
| Was target version actually resolved/used? | GitHub submitted snapshots and scan inventories can provide version evidence [S03,S13,S18]. | Qualified release-boundary source, exact ref/environment/time and denominator; neither PR merge nor generic deps.dev graph suffices. |
| What later public problem appeared? | GitHub issues, PRs, commits and reviews are accessible as raw evidence [S07]. | Relevance to the named release, copied-upstream filtering and negative/UNKNOWN semantics. |
| What investigation/remediation followed? | GitHub PR history and security remediation workflows [S07,S11,S20]. | Link local response to evidence without imposing causal order. |
| What recovery signal exists? | Security policy/vulnerability remediation views exist [S12,S19,S20]. | General compatibility recovery across a declared eligible set/window is **not verified**. |
| What can be learned across repositories? | GitHub organization insights, Socket scans and Sonatype dashboard already aggregate cross-repo/app data [S05,S18,S19]. | A single-target-release cohort narrative with explicit missing evidence was not found in reviewed docs. |

Existing products are not simply “pre-release”: several provide ongoing monitoring, organization views and post-merge scans. The defensible distinction is the **question and evidence contract**: release-bounded reconstruction of a declared cohort, versus dependency inventory, risk/policy monitoring or update PR handling. Whether that distinction improves a real decision remains stakeholder-dependent.
