# Market research source ledger

Research/access date: **2026-09-27**. All 22 sources below are official product, API or vendor documentation opened for this analysis. They establish **documented capabilities as of that date**, not measured performance or proof that an undocumented feature is absent. The [JSON ledger](source-ledger.json) carries each source's claim reference, type, confidence and limitation. `Sxx` IDs are used in the matrices. No search-result snippet is final evidence.

| ID | Product and official document | Capability read from source | Confidence / material limit |
| --- | --- | --- | --- |
| S01 | [GitHub Dependabot version updates](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-version-updates) | Manifest-based version checks and update PRs | High; configuration/ecosystem dependent. |
| S02 | [GitHub Dependabot PR optimization](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/optimizing-pr-creation-version-updates) | Grouping and update policies | High; optional configuration. |
| S03 | [GitHub dependency graph](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-graph) | Repository inventory, versions, licenses, transitive paths and SBOM | High; parsed/submitted source coverage varies. |
| S04 | [GitHub dependency review](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-dependency-changes-in-a-pull-request) | PR dependency diff and vulnerability context | High; unparsed changes can be missed. |
| S05 | [GitHub organization dependency insights](https://docs.github.com/en/enterprise-cloud%40latest/organizations/collaborating-with-groups-in-organizations/viewing-insights-for-dependencies-in-your-organization) | Cross-repository dependency/risk view | High; Enterprise Cloud, maintenance mode and incomplete-data caveats. |
| S06 | [GitHub Actions workflow run history](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/monitoring-workflows/viewing-workflow-run-history) | Run, job and step logs | High; access and retention vary. |
| S07 | [GitHub PR REST API](https://docs.github.com/en/rest/pulls) | PR, reviews, commits and changed-file source | High; raw endpoints require interpretation. |
| S08 | [Mend Renovate overview](https://docs.mend.io/renovate/latest) | Dependency updates and PRs | High; edition boundaries matter. |
| S09 | [Renovate Dependency Dashboard](https://docs.renovatebot.com/key-concepts/dashboard/) | Pending/ignored updates and approval workflow | High; repository issue, not cohort forensics. |
| S10 | [Renovate configuration](https://docs.renovatebot.com/configuration-options/) | Changelog/release-note fetching | High; upstream text alone is not downstream evidence. |
| S11 | [Mend Remediate and Renovate](https://docs.mend.io/integrations/latest/mend-remediate-and-renovate) | Vulnerability fix PRs and available changelog annotation | Medium; Classic integration/legacy screenshot context. |
| S12 | [Mend SCA risk factors](https://docs.mend.io/platform/latest/risk-factors-in-mend-sca) | Reachability/exploitability/maliciousness prioritization | High; security-risk lens. |
| S13 | [Snyk CLI for Open Source](https://docs.snyk.io/developer-tools/snyk-cli/scan-and-maintain-projects-using-the-cli/snyk-cli-for-open-source) | Direct/transitive tree and known vulnerabilities | High; some builds needed for complete resolution. |
| S14 | [Snyk developer tools overview](https://docs.snyk.io/developer-tools/overview) | SCM PR checks, fix/upgrade PRs, CI integration | High; exact ecosystem/edition availability not established here. |
| S15 | [deps.dev API v3](https://docs.deps.dev/api/v3/) | Package versions, advisories and generic resolved graph | High; graph is not the target repository's historic environment. |
| S16 | [PyPI JSON API](https://docs.pypi.org/api/json/) | Python project/release metadata | High; registry listing is not downstream adoption. |
| S17 | [Socket for GitHub](https://docs.socket.dev/docs/socket-for-github) | PR package-behavior and supply-chain alerts | High; security-oriented and configuration dependent. |
| S18 | [Socket Scans](https://docs.socket.dev/docs/scans) | Organization-wide scans linked to repo, branch, PR and commit | High; strong multi-repo overlap, risk-scan scope. |
| S19 | [Sonatype Lifecycle Dashboard](https://help.sonatype.com/en/lifecycle-dashboard.html) | Cross-application risk/component views and export | High; undermines generic multi-repo novelty. |
| S20 | [Sonatype Lifecycle SCM evaluation](https://help.sonatype.com/en/policy-evaluation-in-source-control-management.html) | PR policy feedback and remediation PRs | High; policy/security-oriented. |
| S21 | [Sonatype component identification](https://help.sonatype.com/en/component-identification.html) | Exact/similar/unknown component match and source | High; identity UNKNOWN differs from forensic outcome UNKNOWN. |
| S22 | [Mend organization dashboard](https://docs.mend.io/platform/latest/view-the-overall-state-of-your-organization) | Organization/application scans, findings and security remediation trends | High; security-specific, not named-release compatibility cohort. |

The search was **representative, not exhaustive**. Public documentation may omit private, enterprise, experimental or configurable features. Product testing, license/edition verification and customer workflow research remain pending. “Not found in reviewed documentation” is the maximum absence claim.
