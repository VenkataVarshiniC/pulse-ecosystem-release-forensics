# Pilot observation rubric

## Outcome definitions

- `PASS` — The participant independently demonstrates the dimension using the interface and gives a materially correct explanation. Ordinary exploration is allowed; no semantic teaching or targeted navigation prompt was needed.
- `PARTIAL` — The participant demonstrates part of the dimension but omits a material boundary, remains uncertain, or needs a neutral navigation prompt. The moderator does not supply the semantic answer.
- `FAIL` — The participant states a materially unsafe or contradictory interpretation after the relevant information is available, cannot complete the dimension because of comprehension, or requires semantic teaching.
- `NOT_OBSERVED` — The case, data, system, time, or session flow did not provide a fair opportunity. This is not a pass or failure.

Do not convert these categories into a numerical score or average. Record the observed action, evidence, prompt, direct statement, and analyst interpretation separately.

| Dimension | Observable `PASS` evidence | Material partial/failure signals |
| --- | --- | --- |
| A. Investigation-scope comprehension | Identifies the selected case, exact two pytest members, and that counts apply only to this snapshot/cohort. | Treats the cohort as all repositories or loses snapshot context. |
| B. UNKNOWN vs bounded NO comprehension | Explains that UNKNOWN lacks sufficient qualifying evidence while bounded NO is a scoped negative within a sufficient method and is not universal absence. | Treats either as proof no event occurred or treats both as identical. |
| C. Evidence-sufficiency comprehension | Uses status, sufficiency, reason, and source requirements to explain why a conclusion is or is not permitted. | Uses candidate count, declaration, or collection completion alone as sufficiency. |
| D. Provenance navigation | Reaches evidence/artifact provenance, identifies source/ref/capture context, and notices whether a finding-specific support edge exists. | Treats any nearby artifact as direct support or cannot distinguish source identity from conclusion. |
| E. Candidate/review interpretation | Describes a candidate as a detector firing, inherited REJECT as a prior governed review, and shared artifact as one source incident. | Treats firing as accepted finding, REJECT as no friction, or two firings as two incidents. |
| F. Missing-prerequisite identification | Names a case-relevant missing input such as resolved target version, complete history, downstream release/recovery eligibility, or explicit support edge. | Requests unrelated evidence or claims nothing is missing. |
| G. Next investigation step | Proposes a plausible evidence-seeking or owner-confirmation action connected to the observed gap. | Proposes closing or remediating solely from UNKNOWN, candidate, or declaration. |
| H. Trust calibration | States which evidence is trustworthy, which is insufficient, and what would change trust without demanding certainty the method cannot provide. | Unqualified trust or blanket rejection with no evidence basis. |
| I. Review burden | Gives a grounded view of whether candidate/review detail helps or burdens the task and what routing/volume would be acceptable. | No opportunity to assess is `NOT_OBSERVED`; positive sentiment is not required for PASS. |
| J. Workflow clarity | Explains where the workflow could fit, who would investigate/review/decide, or why it would not fit. | Collapses all roles without explanation or cannot place the workflow after completing the task. |

A severe failure in B or E must be highlighted separately because it can invert the governed meaning even if other dimensions pass.
