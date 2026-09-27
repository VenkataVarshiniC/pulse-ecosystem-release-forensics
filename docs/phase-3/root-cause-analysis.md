# Root-cause analysis of current evidence limits

**Provisional top-level problem:** determining what action a repository requires after a consequential dependency change may be difficult with the currently observable evidence. The *stakeholder difficulty* is a Milestone 1 hypothesis, not an observed complaint. This document analyzes causes of **PULSE's demonstrated inability to answer particular forensic questions** and visible PR exceptions; it does not infer organizational root causes from GitHub activity.

## Cause hierarchy

| Branch | Symptom | Supported underlying cause | Evidence/status | Limit of causal claim |
| --- | --- | --- | --- | --- |
| Information availability: history | Release-boundary exposure often UNKNOWN. | Path-filtered, in-window commit anchors can miss a declaration last changed before the window; missing paired states and cross-file history are unresolved. | [Phase 2 historical method](../phase-2/historical-dependency-reconstruction.md); 2/8 exact-ref declaration evidence and one pre-release paired-path anchor. `observed` PULSE method/output. | Does not prove no historical dependency or no adoption. |
| Information availability: installed version | Observed adoption cannot be measured. | Comprehensive target-version lockfile selection and ordinary runtime/CI resolution were not collected. | [Phase 2 findings](../phase-2/phase-2-findings.md), `observed` source gap. | A permissive/current declaration is not installed use. |
| Information availability: recovery | Recovery rate unavailable. | Downstream releases were not planned/collected, and no recovery-eligible denominator was established. | [Phase 2 evidence sufficiency](../phase-2/evidence-sufficiency.md), `observed` source/denominator gap. | PR merge is not production recovery. |
| Information fragmentation | Relevant facts sit in different PR fields and source categories. | Dependency diff, copied upstream notes, review comments, and bot status replies are separate artifacts; PULSE's own collection joins multiple categories. | [Public PR analysis](secondary-research/github-workflow-analysis.md), `secondary-evidence-supported` for source distribution. | Whether a stakeholder finds correlation difficult or costly is `pending stakeholder validation`. |
| Signal quality and provenance | Two Phase 2 candidates did not qualify. | Copied upstream release-note language in one Dependabot PR was treated as potential downstream friction/remediation by text rules; analyst review rejected both. | [Phase 2 detector evaluation](../phase-2/detector-evaluation.md), `observed` for this case; [public PR codebook](secondary-research/github-pr-codebook.md) preserves text origin. | One artifact does not estimate general precision or recall. |
| Completion semantics | A merged/closed PR is an observable endpoint, but adoption/recovery remain unresolved. | PR disposition answers an artifact-management question; installation, migration completion, and production recovery require different evidence/definitions. | [Public PR outcomes](secondary-research/github-pr-observations.jsonl) plus [Phase 2 findings](../phase-2/phase-2-findings.md); `secondary-evidence-supported` and `observed` boundary. | The stakeholder's own “done” criterion is unknown. |
| Process ownership and prioritization | Cross-repository priority cannot be described. | **No primary evidence yet**, rather than a demonstrated broken process. | [Milestone 1 hypothesis](primary-user-hypothesis.md), `hypothesized`/`not observable`. | Do not turn absence of observation into an organizational cause. |

The first, second, third, and fifth branches explain specific *PULSE output limitations*. The public PR branch shows where information resides, not that the distribution causes stakeholder pain. “UNKNOWN-heavy report” is a symptom of unmet evidence prerequisites, not itself a root cause.

## Bounded why-chains

### RC-01 — Historical release exposure remains UNKNOWN

1. **Why is release-boundary declaration evidence missing in many Phase 2 repositories?** Only 2/8 yielded parsed exact-ref target declarations, and only one had a parsed pre-release anchor in a paired path.
2. **Why can the current method miss a pre-release state?** It selects path-changing commits inside a fixed observation window. A declaration last changed before that window supplies no in-window before anchor; separate packaging paths are not combined into a cross-file transition.
3. **Stop:** These are documented acquisition-method limits. We cannot infer that the repository lacked the dependency, that a maintainer made an error, or that a stakeholder needs a different historical horizon until primary research defines the decision.

### RC-02 — Copied upstream text produced rejected event candidates

1. **Why did two Phase 2 candidate rules fire without accepted downstream evidence?** Both firings came from one Dependabot PR body containing copied upstream release notes; independent review rejected both.
2. **Why is that text misleading for PULSE's forensic question?** Upstream changelog statements describe the upstream package, while a downstream friction/remediation claim needs evidence about the consuming repository. The text rule's candidate output did not make that distinction sufficient for acceptance.
3. **Stop:** This identifies a provenance-sensitive false-positive mechanism in one artifact. It does not establish broad detector quality, analyst burden, or a specific replacement rule.

### RC-03 — Recovery cannot be stated as a measured result

1. **Why is the Phase 2 recovery rate unavailable?** The reports have no defined recovery-eligible denominator or qualifying downstream release evidence.
2. **Why are those inputs absent?** The Phase 2 collection plan did not collect downstream releases, and the accepted lifecycle ledger has no qualifying events from which to form a recovery set.
3. **Stop:** The current planned-source boundary explains the unavailable metric. Whether a downstream release is even the stakeholder's completion criterion remains unknown. Do not equate PR merge or elapsed time with recovery.

These are cause chains for documented system results. They intentionally stop before conjecture about budgets, team practices, or user motivation. See [gaps](gap-analysis.md) and [primary-research questions](milestone-2-primary-research-questions.md).
