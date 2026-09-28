# Market category map and competitive role

Research date **2026-09-27**; categories reflect [documented capabilities](source-ledger.md), not exclusive vendor identities or a complete market census. A “direct competitor” would have to document an end-to-end release-bounded, declared-cohort, downstream evidence investigation with explicit missing-evidence semantics. That combined workflow was **not verified** in this review; absence from reviewed documentation is not proof no product provides it.

| Tool / scope | Primary and overlapping jobs | Relationship to PULSE thesis | Why |
| --- | --- | --- | --- |
| GitHub Dependabot | Version/security update automation, grouped PRs, upstream notes | Partially overlapping | Creates and enriches update PRs; surrounding workflow already strong [S01,S02]. |
| Mend Renovate | Update automation, policy, dashboard, changelog enrichment | Partially overlapping | Tracks pending/ignored updates and review approval in a repository [S08–S10]. |
| Mend Remediate + SCA | Vulnerability/SCA, fix PRs, risk prioritization | Partially overlapping | Targeted security remediation and risk context, not documented as general compatibility forensics [S11,S12]. |
| Snyk Open Source | SCA, dependency tree, PR checks, fix/upgrade integration | Partially overlapping | Security/dependency workflow and CI overlap [S13,S14]. |
| GitHub dependency graph/review/Actions/API | Inventory, pre-merge review, CI, repository history, organization insights | Infrastructure/data source **and** partial substitute | A motivated analyst can assemble much of a case manually; organization inventory already exists [S03–S07]. |
| deps.dev | Package/version/dependency/advisory intelligence | Infrastructure/data source | Useful metadata and generic graph, not a downstream repository decision record [S15]. |
| PyPI | Package release metadata | Infrastructure/data source | Release facts, not adoption proof [S16]. |
| Socket | Supply-chain risk, PR alerts, organization scan history | Partially overlapping | Cross-repository, PR/commit-linked evidence materially challenges any generic “multi-repo evidence” novelty [S17,S18]. |
| Sonatype Lifecycle | SCA policy, remediation PRs, application/component risk dashboard | Partially overlapping | Organization-wide component and application views already exist [S19–S21]. |

Dependency observability and post-release investigation are **jobs**, not automatically new product categories. GitHub APIs, scripts and human review can form a powerful substitute even without a dedicated product. No vendor receives a “winner” score.
