# Vendor-neutral jobs to be done

Jobs describe a decision or evidence need, independent of a proposed PULSE feature. “Well documented” identifies examples in the [source ledger](source-ledger.md), not universal availability. A person can also do many jobs manually with existing tools.

| ID | Job and observable completion question | Documented coverage / unresolved boundary |
| --- | --- | --- |
| JTBD-01 | Identify current direct and transitive dependencies in a repository. | GitHub graph, Snyk, deps.dev generic graph [S03,S13,S15]; environment-specific completeness varies. |
| JTBD-02 | Learn that a newer dependency version exists. | Dependabot, Renovate, registries [S01,S08,S16]. |
| JTBD-03 | Propose an upgrade and manage update policy/grouping. | Dependabot and Renovate [S01,S02,S08,S09]. |
| JTBD-04 | Detect known vulnerabilities, license or package-risk signals. | GitHub, Snyk, Mend, Socket, Sonatype [S03,S04,S12,S13,S17,S19]. |
| JTBD-05 | Evaluate a proposed change before merge. | GitHub dependency review, security checks, CI and human review [S04,S06,S14,S17,S20]. |
| JTBD-06 | Inspect release notes and upstream changelog context. | Dependabot and Renovate attach/fetch it [S01,S10]; relevance to local behavior remains a question. |
| JTBD-07 | Recover dependency declaration at a chosen historical commit/ref. | Git history and APIs enable manual/configured reconstruction [S07]; complete release-boundary pairing was not shown as a native reviewed workflow. |
| JTBD-08 | Establish actual resolved/used target version for a repository at a defined time. | Current or submitted inventory can help [S03,S13,S18]; generic registry graph is insufficient [S15]. Historical runtime proof not verified. |
| JTBD-09 | Find release-associated downstream issues/PRs and separate copied upstream text. | Repository search/API enables manual work [S07]; cross-source origin-aware case assembly not verified natively. |
| JTBD-10 | Trace local code, test, config, workaround or documentation response. | PR/commit/review histories are inputs [S07]; linking them to one release case requires interpretation. |
| JTBD-11 | Determine whether bounded recovery evidence exists for an eligible set/window. | Existing security dashboards show vulnerability/policy remediation [S19,S20]; broader compatibility recovery remains unverified and needs a valid denominator. |
| JTBD-12 | Compare a declared cohort after one target release. | GitHub, Socket and Sonatype offer cross-repository/application views [S05,S18,S19]; target-release forensic cohort comparison not verified in reviewed docs. |
| JTBD-13 | Explain source, capture method, sufficiency and contradictory evidence behind a finding. | Native risk/identity provenance exists in adjacent tools [S18,S21]; full PULSE-style evidence chain not verified. |
| JTBD-14 | Preserve UNKNOWN and a next evidence request when a conclusion is unsupported. | Sonatype has “Unknown” component identity [S21], a different semantics; post-release outcome UNKNOWN not verified. |
| JTBD-15 | Decide whether another investigation is worth doing. | Real owner, frequency, consequence and acceptable manual effort are **stakeholder-dependent**, not vendor features. |

No job presumes that PULSE should own it. The sequence can branch: compatibility work may precede a later public friction report, and merge is not proof of adoption or recovery.
