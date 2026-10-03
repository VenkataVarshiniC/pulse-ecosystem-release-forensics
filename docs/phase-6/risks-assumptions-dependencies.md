# Phase 6 risks, assumptions, dependencies, and open questions

The categories below are intentionally separate. A risk is a possible adverse outcome; an assumption is an unvalidated proposition used to plan; a dependency is a condition outside the recommendation artifact that must exist; an open question requires evidence before resolution.

## Risks

| ID | Risk | Evidence / trigger | Consequence | Control or response |
| --- | --- | --- | --- | --- |
| R-01 | Public-source evidence limitations | Current plans lack installed-version, some CI/private review, and recovery evidence. | Evidence-depth work may leave lifecycle questions UNKNOWN. | Define source availability and stop criteria; narrow claims when evidence is inaccessible. |
| R-02 | Historical-source availability | Only 1/8 members currently has paired pre-release context. | Older anchors or cross-file states may remain unresolved. | Prespecify the history experiment; retain exact refs and unresolved reasons; do not infer past state. |
| R-03 | Source-policy constraints | Nonpublic/sensitive-source policy and retention are not approved. | A relevant source may be unusable even if technically accessible. | Require authorization, minimization, provenance, and retention rules before collection. |
| R-04 | Cohort representativeness misuse | Two convenience validation cases contain 8 members. | Readers may generalize bounded rates or outcomes to an ecosystem. | Name populations on every measure; prohibit pooled incidence and representative language. |
| R-05 | Stakeholder validation remains absent | G8 is `NOT_YET_VALIDATED`. | Technical priorities may not match a real decision or workflow. | Keep value/workflow claims provisional; execute the reconciliation framework only when authorized. |
| R-06 | Reviewer authority is undefined | Published review is read-only and current decisions are inherited. | A future review action could lack legitimacy or auditability. | Keep write paths gated; require named authority, DRAFT scope, identity, and reason policy. |
| R-07 | Evidence quality varies | Declarations, copied notes, bot replies, and PR states answer different questions. | Ineligible artifacts may be mistaken for adoption, friction, or recovery. | Use question/source eligibility and human qualification; preserve source origin. |
| R-08 | False-positive qualification | Two rules fired on one copied-upstream artifact and both were rejected. | More sources may increase review noise and unsupported event candidates. | Group by artifact/origin, freeze baselines, and evaluate against independently reviewed material. |
| R-09 | Scaling before sufficiency | Current findings are 38/40 UNKNOWN. | Broader cohorts may multiply uncertainty, cost, and misleading counts. | Block breadth until evidence-depth and selection gates pass. |
| R-10 | Maintenance complexity | Additional prerequisite maps, reason codes, source types, and versions add governance overhead. | Semantic inconsistency or brittle replay may increase. | Add only question-justified elements; version contracts; test side-by-side; retire unused paths deliberately. |
| R-11 | Semantic drift | UI, Power BI, metrics, and findings could diverge from source contracts. | UNKNOWN could be shown as NO, or evidence coverage as adoption. | Centralize governed definitions, run reconciliation, and audit forbidden interpretations. |
| R-12 | Metric misuse | Capability measures may be presented as business KPIs or success outcomes. | Coverage improvements could be mistaken for value, ROI, adoption, or compatibility. | Label all Phase 6 measures PROPOSED; require numerator/denominator/population/limits. |
| R-13 | Provenance loss | New transformations or source trials may omit identity, clocks, method, digest, or support links. | Findings become unauditable or irreproducible. | Fail closed on missing provenance and positive support linkage; never overwrite published records. |
| R-14 | Method overfitting | History/source rules may be tuned to pytest and urllib3 outcomes. | Apparent improvement may not transfer. | Freeze the experiment, separate method from population changes, then run a later outcome-blind transfer test. |
| R-15 | Sunk-cost continuation | The breadth of existing implementation may bias the next decision toward more building. | PULSE could continue without validated need or obtainable evidence. | Keep existing tools/do-nothing as a valid alternative and define stop conditions. |

## Assumptions

| ID | Assumption | Status | If false |
| --- | --- | --- | --- |
| A-01 | At least one bounded lifecycle question can be defined with observable, auditable prerequisites. | Unvalidated outside current technical contracts | Narrow the product to evidence inventory/audit or stop the affected claim. |
| A-02 | Deeper historical search can recover some context missed by the current in-window path-change method. | Plausible; not demonstrated | Record infeasibility and avoid history expansion as a default. |
| A-03 | Existing identity, provenance, replay, and publication architecture can represent the proposed method without a new major subsystem. | Supported by current modular/versioned design | Reassess scope and cost before implementation; do not force-fit. |
| A-04 | A fixed-population comparison can isolate method effects sufficiently for a bounded decision. | Methodological planning assumption | Redesign the experiment before interpreting deltas. |
| A-05 | Honest unresolved-reason detail may help an investigator choose a next evidence action. | Stakeholder-dependent | Do not expand the interface solely for reason taxonomy presentation. |
| A-06 | A future authorized stakeholder or reviewer can be identified. | `NOT_YET_VALIDATED` | Keep G8 open and review workflow read-only; consider HOLD/STOP. |
| A-07 | Existing tools remain a credible substitute and may be sufficient. | Supported as a technical possibility; cost/value unmeasured | If stakeholders show a concrete unmet decision, compare rather than dismiss substitutes. |

## Dependencies

| ID | Dependency | Needed for | Current state |
| --- | --- | --- | --- |
| D-01 | Frozen case, source, rule, and published snapshot identities | Side-by-side replay and audit | Available; must remain immutable. |
| D-02 | Approved lifecycle question and source/prerequisite contract | Evidence-depth implementation and P6 measures | Technical starting points exist; stakeholder-required set is unapproved. |
| D-03 | Source access and policy authorization | Any new source trial | Not established beyond current public sources. |
| D-04 | Versioned reason taxonomy and method manifest | Comparable sufficiency and unresolved analysis | Proposed; not implemented. |
| D-05 | Reconciliation and publication controls | Any analytical release | Existing architecture available. |
| D-06 | Legitimate source-backed positive or governed fixture | Positive support-link validation | Absent in current published population. |
| D-07 | Named reviewer authority and eligible DRAFT case | Live review-write validation | Absent. |
| D-08 | Genuine stakeholder participants and evidence-handling plan | G8 reconciliation | Absent; outside Phase 6 completion. |
| D-09 | Outcome-blind selection frame | Later cohort transfer test | Existing method exists; future frame not selected. |

## Open questions

| ID | Open question | Evidence required |
| --- | --- | --- |
| Q-01 | Which lifecycle question must a real decision answer? | Recent decision walkthrough and accountable owner. |
| Q-02 | What source and historical boundary is acceptable for that question? | Source policy plus stakeholder/analytical threshold. |
| Q-03 | Can deeper public history materially improve paired context on a frozen test? | Prespecified side-by-side experiment. |
| Q-04 | Is qualified resolved-version evidence accessible and relevant? | Authorized source trial with grain and eligibility contract. |
| Q-05 | What constitutes bounded completion versus production recovery? | Decision-owner definition and observable source. |
| Q-06 | Does an UNKNOWN explanation change a next action? | Stakeholder task test using a real incomplete case. |
| Q-07 | Who may review candidates, and what burden is acceptable? | Named authority, representative queue, and observed review exercise. |
| Q-08 | When should breadth follow depth? | Evidence-depth results, transfer question, and prespecified progression threshold. |
| Q-09 | Are current tools sufficient? | Side-by-side recent case reconstruction and changed-decision evidence. |

No assumption or open question is recorded as a validated fact.
