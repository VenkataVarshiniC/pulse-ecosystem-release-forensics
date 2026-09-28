# Neutral operational capability taxonomy

The unit and qualifying evidence matter more than feature labels. IDs are used in the [competitive matrix](competitive-capability-matrix.md). Capabilities C09–C16 are **not** presumed unique to PULSE.

| ID | Capability | Operational test |
| --- | --- | --- |
| C01 | Dependency inventory | Show direct/transitive package and version for a named repository/ref, with source coverage. |
| C02 | Package intelligence | Show registry release metadata, dependency graph or advisories for a named package/version. |
| C03 | Automated update proposal | Create/update a dependency PR with proposed version and changed files. |
| C04 | Update policy/grouping | Configure schedule, grouping, ignore/defer and approval rules. |
| C05 | Upstream context | Surface release notes/changelog with clear upstream origin. |
| C06 | Vulnerability/license/package risk | Detect or explain known security, license or behavior signals. |
| C07 | Pre-merge dependency review | Compare proposed dependency state and report policy/security findings before merge. |
| C08 | CI/test evidence | Expose test/check results tied to exact run, ref and environment. |
| C09 | Historical release-boundary reconstruction | Pair repository evidence at declared pre/post target-release refs; preserve unresolved state. |
| C10 | Qualified target-version observation | Identify resolved/installed/used version with ref, environment, time and provenance; distinguish a proposed specifier. |
| C11 | Downstream event correlation | Link issue/PR/comment/commit to a release case and distinguish downstream statement from copied upstream text. |
| C12 | Declared-cohort release comparison | Compare one target release across explicit member set/window and denominator, not a generic inventory. |
| C13 | Remediation/workaround trace | Link a local code/test/config/doc response to its evidence without asserting causality. |
| C14 | Bounded recovery evidence | Apply explicit eligible set, qualifying signal and window; missing evidence is not recovery failure. |
| C15 | Provenance/sufficiency/UNKNOWN | Trace finding to source, capture method and required evidence, retaining unknown/conflict. |
| C16 | Human forensic review/report | Separate machine candidate from human acceptance and produce auditable bounded case report. |

Cross-repository view (C12) is intentionally defined more narrowly than organization inventory. “Unknown” in C15 is outcome/evidence uncertainty, not an unknown component identity. C10 and C14 are demanding by design because version constraints and PR merge do not establish actual use or recovery.
