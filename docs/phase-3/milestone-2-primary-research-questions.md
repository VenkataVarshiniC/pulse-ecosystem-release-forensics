# Milestone 2 unresolved primary-research questions

Use these questions to reconcile the provisional [As-Is model](as-is-process.md) with future qualified Google Form responses and genuine interviews. They are **questions**, not observed needs or final requirements. Ask for a recent actual case before presenting the public-PR or PULSE interpretation; capture counterexamples and “not applicable” answers. The [integration plan](secondary-research/primary-research-integration-plan.md) keeps primary and secondary evidence separate.

| ID | Question for a qualified participant | Current uncertainty / linked analysis |
| --- | --- | --- |
| Q01 | What most recently triggered a dependency-release investigation or upgrade in your work? Was it a bot PR, upstream release, incident, security notice, or something else? | Bot PR initiation is observed; broader investigation trigger is not. [ASIS-01](as-is-process-catalogue.md). |
| Q02 | Who decides which repositories or services are in scope, and who owns the resulting decision? | Portfolio owner and intake are hypothetical. [DP-06](as-is-decision-points.md). |
| Q03 | Do you actually compare or prioritize multiple repositories? If so, what determines the order and who acts on it? | Cross-repository prioritization is not observable in public PRs. [GAP-07](gap-analysis.md). |
| Q04 | In your last case, which concrete sources did you inspect, and which one changed your decision? | Diffs, notes, comments, issues, and checks are distributed; required source set is unknown. [Friction analysis](workflow-friction-analysis.md). |
| Q05 | Was passing CI sufficient to accept the upgrade? If not, what further test, review, or production evidence was needed? | Public check histories were not systematically audited; approval does not prove test success. [ASIS-03](as-is-process-catalogue.md). |
| Q06 | When did you need the dependency declaration as it existed at a past release boundary, rather than its current value? How did you establish it? | Phase 2 path-scoped history often lacked a pre-release anchor. [GAP-02](gap-analysis.md). |
| Q07 | Did the installed or resolved package version matter more than a declaration or constraint? What evidence showed the version actually in use? | Phase 2 had no comprehensive target-version resolution evidence. [GAP-03](gap-analysis.md). |
| Q08 | Which PR candidates or review steps consumed meaningful attention in the last case, and what volume of review would be acceptable? | Visible comment count is not effort; burden is unmeasured. [Friction analysis](workflow-friction-analysis.md). |
| Q09 | Are bot upgrade PRs, copied upstream notes, supersession, or rebase replies useful signals, routine noise, or both in your workflow? | The frozen public sample is all Dependabot; PULSE had two copied-text false candidates. [Root causes](root-cause-analysis.md). |
| Q10 | What did “complete” mean in your last migration: PR merge, version installed, deployment, a downstream release, or something else? Who verified it? | PR disposition, migration, and recovery are distinct; recovery evidence was not collected. [DP-08](as-is-decision-points.md). |
| Q11 | If an investigation returns UNKNOWN because evidence is missing, what is your next action? When is that result useful versus blocking? | PULSE propagates UNKNOWN correctly; operational utility is unvalidated. [GAP-05](gap-analysis.md). |
| Q12 | Which provenance details—source URL, capture method, date, completeness, review decision—do you need before trusting or sharing a conclusion? | PULSE preserves provenance, but user trust standard is unknown. [Capability matrix](current-state-capability-matrix.md). |
| Q13 | When an upgrade needs code changes or escalation, who receives the work and how is the handoff recorded? | One public PR showed a code change; organizational handoffs are not visible. [ASIS-04](as-is-process-catalogue.md). |
| Q14 | Which existing tools already answer this decision well, and which gaps remain after using them? | The value of PULSE versus existing practice is an untested business hypothesis. [Business problem](business-problem.md). |

Future evidence should classify each question as confirmed, refined, contradicted, or still unknown with an anonymized source. Do not fill answers from the public PR sample or fabricate Google Form responses.
