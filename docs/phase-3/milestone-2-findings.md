# Phase 3 Milestone 2 findings — provisional As-Is and root causes

## Classification

**PARTIAL.** The current public, bot-initiated PR artifact path and PULSE's system evidence limits can be modeled with provenance. The broader organizational dependency-release investigation, its owner, cross-repository priority decision, evidence threshold, and completion criterion remain unobserved while Google Form/interview evidence is pending. That is too much of the stakeholder As-Is workflow to call validated or to use as a firm basis for a To-Be design.

## Evidence basis

1. **Phase 2 system evidence:** [final PIVOT findings](../phase-2/phase-2-findings.md), historical and evidence-sufficiency methods. Bounded live collection/reporting worked, while exact-ref declaration evidence covered 2/8 repositories, two bot-text candidates were rejected, and adoption/recovery inputs were insufficient.
2. **Milestone 1 hypotheses:** [primary user](primary-user-hypothesis.md), [business problem](business-problem.md), stakeholder/needs registers. These provide questions and possible roles, not validated behavior.
3. **Milestone 1A secondary evidence:** [frozen sample](secondary-research/github-pr-candidate-frame-summary.md) and [coded observations](secondary-research/github-pr-observations.jsonl): 20 base and 7 purposive discussion PRs, all Dependabot-initiated and all from the first day of their half-year slice. No ecosystem prevalence or general Python workflow claim follows.
4. **Primary stakeholder evidence:** still pending. No survey result or interview is claimed here.

## Provisional As-Is process

In the bounded public sample, Dependabot opened a package-update PR with a dependency-file diff and sometimes copied upstream context. Optional visible review or test discussion could lead to approval, a retained version, code change, command, or bot status; the PR then merged or closed. These are branches, not a required linear sequence. [The process narrative](as-is-process.md), [swimlane](as-is-swimlane.md), and [BPMN-style artifact model](as-is-bpmn.md) show this limited path. Separately, PULSE can collect and report bounded evidence with explicit UNKNOWN, but there is no evidence it participated in the sampled repositories' workflow.

## Strongly supported process elements

Within **PULSE's frozen Phase 2 cases**, authenticated planned-source collection, exact-ref path-scoped history attempts, independent candidate review, provenance checks, and deterministic reporting are demonstrated. Their limits are also demonstrated: declaration evidence 2/8 is not adoption, target-version installation was not established, zero lifecycle events were accepted, and no recovery denominator was available. [The capability matrix](current-state-capability-matrix.md) distinguishes supported from partial and unsupported capabilities.

## Secondary-evidence-supported elements

Within the **public PR frame**, proposal/diff, attached upstream text, occasional human review, visible exception responses, and merge/closure are supported. Base sample: 6/20 showed public human interaction; 9 merged and 11 closed. Discussion sample: 7/7 had human interaction by purposive selection; 4 merged and 3 closed. [baseplate.py#1054](https://github.com/reddit/baseplate.py/pull/1054) showed a reported test failure and code change; [uvicorn#2549](https://github.com/Kludex/uvicorn/pull/2549) retained an older package pin. These examples do not estimate frequency outside the frame or prove stakeholder needs.

## Hypothesized and not-observable elements

An organizational release-investigation trigger, owner, repository selection, portfolio comparison, priority/escalation rule, trust threshold, and migration-completion decision are `hypothesized` or `not observable`. The primary-user hypothesis is **unchanged and unvalidated**: a cross-repository dependency/platform engineer is plausible, but no sampled PR identifies that role or its decision process.

## Main observable workflow friction and root causes

The [friction analysis](workflow-friction-analysis.md) separates distributed evidence, upstream/downstream text ambiguity, historical and installed-version uncertainty, visible exception paths, and completion semantics from unmeasured human burden. [Root-cause analysis](root-cause-analysis.md) identifies documented PULSE causes: the in-window, path-scoped historical anchor method; missing installed/runtime inputs; copied upstream text behind the two rejected candidates; and uncollected downstream releases/undefined recovery eligibility. It stops where further organizational explanation would be speculation.

## Current capability gaps

The [gap analysis](gap-analysis.md) identifies release-boundary state, installed target-version evidence, qualifying local event signals, recovery evidence, and actionability of UNKNOWN as open decision prerequisites. Portfolio scope and the user value of deterministic reports are unvalidated. None is converted to a final functional requirement.

## Questions stakeholder research must resolve

[The question catalogue](milestone-2-primary-research-questions.md) asks who scopes repositories, whether cross-repository priority is real, what triggers work, which sources/CI results change a decision, when historical versus installed state matters, what bot noise costs, how UNKNOWN is used, what provenance is trusted, and what counts as completion. Genuine responses may confirm, refine, contradict, or replace this process account.

## Impact on primary-user hypothesis

No promotion or change. Public PR reviewers are visible, but their organizational role and portfolio responsibility are not. The broader [primary-user hypothesis](primary-user-hypothesis.md) remains a recruiting hypothesis.

## Readiness for Milestone 3 and later reconciliation

**Not ready to lock a To-Be workflow.** The proposed future process would depend critically on unanswered ownership, decision, source-threshold, UNKNOWN-utility, and completion questions. When genuine Google Form/interview evidence is available, a separate **Milestone 2A — Stakeholder Evidence Reconciliation** checkpoint should compare it with the frozen public analysis and this provisional model, recording confirmations, refinements, contradictions, and replacements before locking As-Is or deriving formal requirements. That checkpoint is planned only; it has not been performed. No To-Be design, BR/FR/NFR catalogue, user-story backlog, RTM, or UAT plan was created in Milestone 2.
