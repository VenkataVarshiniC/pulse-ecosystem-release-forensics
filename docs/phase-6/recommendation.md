# Phase 6 recommendation

## Recommendation statement

Adopt a **sequenced, evidence-depth-first strategy**. Authorize only a bounded validation of question-specific evidence depth as the next investment: improve and test historical context reconstruction, source-availability classification, prerequisite/reason semantics, and explicit finding-support linkage on a prespecified scope. Do not broaden cohorts or expand the investigator/review product until that validation demonstrates greater bounded answerability or documents that the required evidence is inaccessible.

This is Option D from the [alternatives analysis](alternatives-analysis.md), with Option A as its immediate and only authorized horizon. It is a recommendation for the next decision sequence, not an implementation authorization in Phase 6.

## Decision rationale

1. Planned core collection is already complete for 8/8 declared members, so repeating the current collection plan is not the clearest route to better answers.
2. Only 2/40 lifecycle findings are sufficient, 38/40 remain `UNKNOWN`, and no positive finding exists. The largest observed gap lies between collected artifacts and question-specific qualifying evidence.
3. Only 1/8 members has paired pre-release historical context; fixed-window path-change selection and cross-file history are documented method limits.
4. Observed adoption and recovery lack qualified inputs and eligible denominators. They cannot be repaired by larger cohorts or interface changes.
5. Candidate/review provenance is strong, but the two rejected firings share one copied-upstream artifact. Origin-aware grouping and human review must remain.
6. PostgreSQL/dbt publication, API/UI integration, and Power BI isolation are technically validated. Another major presentation subsystem would not address the current analytical constraint.
7. G8 remains open. Workflow expansion and prioritization claims would depend heavily on unvalidated users, authority, and value.

## Primary evidence

- [Phase 2 findings](../phase-2/phase-2-findings.md): reliable bounded collection, sparse history, no accepted lifecycle events, and unavailable adoption/recovery.
- [Phase 3 root-cause analysis](../phase-3/root-cause-analysis.md): history, installed-version, recovery-source, and copied-text limitations with causal boundaries.
- [M3 decision memo](../phase-4/m3/product-analytics-decision-memo.md): 8/8 collection versus 38/40 UNKNOWN and 1/8 paired pre-release context.
- [M4.1B governed release](../phase-4/milestone-4-1b-findings.md): 40 versioned findings, 38 UNKNOWN, two bounded NO, and governed publication.
- [M4.2 validation](../phase-4/m4-2/power-bi-dashboard-validation.md): dynamic scope and denominator semantics work in Desktop.
- [M5.4 acceptance](../phase-5/m5-4/product-acceptance-results.md): technical workflow passes with explicit partial conditions for missing support edges, source states, and review operation.

The separate [public PR analysis](../phase-3/secondary-research/github-workflow-analysis.md) supports source-fragmentation and copied-origin hypotheses only. Its counts do not enter the governed finding population.

## Capabilities prioritized

1. **Question-specific evidence prerequisites** — map each lifecycle question to acceptable source types, eligibility rules, sufficiency states, and controlled unresolved reasons.
2. **Historical context depth** — test older-anchor discovery and cross-file manifest transitions against a prespecified validation set while keeping `AFTER_ONLY` distinct from `PAIRED`.
3. **Source availability** — distinguish not planned, not accessible, not found, incomplete, conflicting, and structurally unavailable inputs.
4. **Support linkage** — require every future supported positive finding to trace to qualifying evidence through an intact source/review chain.
5. **Incremental replay comparison** — publish side-by-side method results without overwriting frozen or published snapshots.
6. **Stop criteria** — record when evidence cannot be obtained or does not improve sufficiency, instead of expanding scope indefinitely.

## Capabilities explicitly deferred

- broad cohort and release expansion;
- production-scale monitoring or deployment;
- portfolio risk or attention scoring;
- observed-adoption or recovery rates without eligible inputs;
- detector optimization based on two dependent rejected firings;
- active reviewer queue/write workflow without authority and a legitimate DRAFT case;
- new dashboards or major interface subsystems;
- private-source acquisition without source policy and authorization;
- AI, LLM, RAG, embedding, or probabilistic classification work;
- final portfolio packaging.

## Why the alternatives are not first priority

**Cohort breadth first** would apply the same insufficient method to more repositories. It might increase examples, but it cannot establish better decision coverage and would increase the risk of pooled or ecosystem-generalized interpretation.

**Workflow first** would improve interaction around an already technically functional read path. It cannot create missing historical, resolved-version, or recovery evidence, and its intended user and reviewer authority remain unvalidated.

**Evidence depth without sequence gates** is directionally correct but risks open-ended source accumulation. The selected sequence constrains it to explicit questions, acceptance criteria, and stop decisions.

## Tradeoffs

- The recommendation favors evidence quality over visible feature growth and near-term cohort size.
- A deeper method may return an honest infeasibility result rather than more supported findings.
- Focusing on existing cases limits representativeness, but it isolates method change from population change.
- Delaying workflow and breadth reduces immediate demonstrability while protecting analytical validity.
- Some source questions cannot be resolved without stakeholder input or authorized nonpublic evidence.

## Residual risks

- Historical anchors or resolved-version evidence may remain unavailable after additional method work.
- A method tuned to the two validation cases may not transfer to another release or packaging layout.
- Typed prerequisite maps may become complex to maintain or drift from metric/report language.
- More evidence can increase review burden and false-positive opportunities.
- A technically stronger result may still have no validated decision owner or workflow value.

These risks are expanded in [risks, assumptions, and dependencies](risks-assumptions-dependencies.md).

## Stakeholder-dependent assumptions

- A bounded release-forensics question matters to an identifiable decision owner.
- At least one lifecycle question has an acceptable evidence threshold.
- An authorized source set can be defined and accessed.
- Honest UNKNOWN and evidence-gap explanations can support a decision rather than merely document uncertainty.
- A reviewer can be authorized if candidate qualification proceeds.

None is treated as validated. `G8 = NOT_YET_VALIDATED`.

## Conditions that would change the recommendation

The recommendation should change if any of these occurs:

- A prespecified evidence-depth experiment shows no meaningful improvement and identifies inaccessible prerequisites; consider HOLD, PIVOT to a narrower evidence-audit use case, or STOP.
- Stakeholders demonstrate that current tools already answer the decision adequately; stop or narrow PULSE rather than duplicate them.
- Stakeholders identify a workflow problem whose value does not depend on deeper lifecycle evidence; reassess Option C with explicit acceptance criteria.
- A validated decision requires breadth before depth, with an approved question whose current sources are already sufficient; authorize a bounded cohort experiment, not ecosystem inference.
- A new governed source-backed case supplies positive findings or recovery eligibility; update support-link and metric validation before changing claims.
- Source policy prevents acquisition of the evidence needed for the intended claim; remove or narrow that claim.

## Classification

**Phase 6: PASS_WITH_STAKEHOLDER_HOLD.**

The technical and analytical recommendation is complete, bounded, traceable, and compatible with existing governance. Stakeholder validation, user value, reviewer authority, and organizational source/decision thresholds remain unresolved. G8 stays `NOT_YET_VALIDATED`.
