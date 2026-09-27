# Assumptions, constraints, and risks

Assumptions are unvalidated propositions. Constraints are boundaries demonstrated by the current project record, not necessarily permanent limits. Risks are conditions that could defeat the proposed value. All should be revisited after discovery.

## Assumptions to test

| ID | Assumption | Validation approach |
| --- | --- | --- |
| A-01 | Some relevant users investigate releases across multiple repositories. | Recruit by actual responsibility; request a recent concrete case and repository set. |
| A-02 | Public or accessible development evidence influences their decisions. | Ask what sources they actually used and what was decisive. |
| A-03 | They need evidence tied to release-time state, not solely current declarations. | Examine the last investigation's timeline and decision threshold. |
| A-04 | Human review is acceptable for consequential candidate findings. | Elicit review volume, ownership, and tolerance from recent work. |
| A-05 | A bounded, honest UNKNOWN output can guide a next action. | Ask what they would do when a needed state cannot be established. |

## Current constraints

| ID | Constraint from existing work | Consequence for analysis |
| --- | --- | --- |
| C-01 | Public evidence can be incomplete; Phase 2 coverage was bounded to a frozen cohort and specified paths. | Do not generalize observed coverage or infer absence outside the collection boundary. |
| C-02 | Historical target-package declaration evidence was established for 2/8 frozen repositories. | Treat this as collection evidence coverage, never an adoption percentage. |
| C-03 | A current dependency declaration does not prove release-time use or installed target version; ordinary runtime/CI resolution was not established. | Ask which exposure state the decision actually requires. |
| C-04 | No downstream release collection or recovery-eligible denominator was established. | Recovery cannot be quantified from the present validation. |
| C-05 | Two candidate events were rejected; no accepted events allow recall measurement. | Do not claim detector effectiveness or tune to these cases without a decision criterion. |
| C-06 | Provenance varies: Phase 1 HTTPX snapshots were connector-assisted, while Phase 2 used bounded live API collection. | Communicate collection method and completeness with conclusions. |

## Risks and responses

| ID | Risk | What would reveal it / response |
| --- | --- | --- |
| R-01 | The proposed primary user does not own a recurring decision. | Interview alternative roles; revise or stop the use case rather than inventing demand. |
| R-02 | Evidence required for action is inaccessible or cannot be reconstructed reliably. | Elicit minimum evidence threshold; identify source access before specifying a feature. |
| R-03 | Trustworthy UNKNOWN outputs remain too inconclusive to change action. | Test realistic unknown-heavy examples in discovery; document a no-go outcome if needed. |
| R-04 | Analyst review burden exceeds the value of surfaced candidates. | Measure current and proposed review steps; include rejected and missed signals. |
| R-05 | Existing tools or practices sufficiently solve the problem. | Ask participants to demonstrate their actual workflow and compare gaps without pitching PULSE first. |
| R-06 | Narrow frozen cohorts or public repositories misrepresent an organization's owned set. | Define the population with users before claiming generality. |

Risk ownership and ratings should be agreed with genuine stakeholders later; none are assigned to fictional roles here.
