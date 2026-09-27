# Human and automation boundary — provisional

PULSE supports a release investigation; it does not make operational or causal judgments on a person's behalf. The boundary uses [Phase 2 architecture](../phase-2/phase-2-findings.md), [current gaps](gap-analysis.md), and the [proposed process](to-be-process.md). `Automate` below means a defensible proposed responsibility, not a claim that every input is currently collected. Organizational ownership is pending stakeholder research.

| Activity | Boundary | Why and present evidence | Unresolved validation |
| --- | --- | --- | --- |
| Define release, repository cohort, window, and selection rationale | **Human-owned**; PULSE records and validates a typed case | Phase 2 cases are bounded; its convenience cohorts are not an organization's population. | Actual decision owner and trigger. |
| Collect planned public evidence, record queries, task outcomes, capture method, immutable raw data, and resume | **Automate** | Phase 2 live validated bounded collection, provenance, and verified resume. | Access and relevance of any new source. |
| Normalize source identity and reconstruct exact-ref states | **Automate**, with visible unresolved states | Current path-scoped history works at exact refs but missed older unchanged declarations. | Which historical state matters and method coverage. |
| Evaluate declared source/stage sufficiency and denominators | **Automate** for explicit rules; **human-owned** for contested interpretation | Current UNKNOWN and negative-finding guards prevent missing data from becoming NO. | Whether added sources justify revised thresholds. |
| Generate friction/remediation/adoption/recovery candidates | **Automate** only as candidate discovery | Two Phase 2 bot-text firings were rejected; recall is unmeasured. | Precision, recall, and acceptable review volume. |
| Distinguish copied upstream context and flag conflicts | **Decision support** | Upstream release notes in PR bodies do not prove local impact; manifests and lockfiles can answer different questions. | Evidence needed to resolve a conflict. |
| Suggest which repositories/candidates warrant attention, with reasons and override | **Decision support** | The public sample shows many PRs without visible human interaction, but not a validated triage need. | Whether cross-repository prioritization exists; acceptable false alarms. |
| Accept, reject, or request more evidence for a candidate | **Human-owned** | Independent Phase 2 review kept both rejected firings out of accepted events. | Reviewer identity, authority, and burden. |
| Derive and render bounded repository/cohort findings from reviewed evidence | **Automate** within approved evidence rules | Deterministic reports and explicit UNKNOWN worked in frozen cases. | User comprehension and decision usefulness. |
| Interpret ambiguous causality or decide remediation priority and operational risk | **Human-owned** | No current data proves causality, production state, or business priority. | Who is accountable and what evidence they require. |
| Declare investigation complete or production recovered | **Human-owned / currently unresolved criterion** | PR merge, declaration, and CI status are distinct from deployment/recovery. | Completion definition and evidence source. |

No automated rank, detector emission, or elapsed time alone authorizes a lifecycle finding or organizational action. `Needs more evidence` keeps the review open or returns an explicit UNKNOWN. This boundary is a design hypothesis until primary research tests who reviews, which evidence they trust, and how much review work is acceptable.
