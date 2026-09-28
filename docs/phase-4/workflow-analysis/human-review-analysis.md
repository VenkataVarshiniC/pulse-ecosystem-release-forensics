# Visible human review and judgment

| Public signal | Base (D=20) | Purposive discussion (N=7, example counts only) |
| --- | ---: | ---: |
| Any visible human interaction | 6 | 7 |
| Formal human review coded | 5 | 4 |
| Explicit approval | 4 | 4 |
| Human bot command | 1 | 6 |
| Substantive downstream review comment | 1 | 1 |
| No visible human interaction | 14 | 0 by selection |
| Changes requested | 0 | 0 |

In the base sample, 14/20 PRs reach terminal disposition without visible human interaction: four merged and ten closed without merge. Among the six with interaction, five merged and one closed. These are selected-case descriptions, not evidence that interaction caused merger. The approved cases demonstrate visible decisions but not check-run success, decision effort, or private discussion. The [uvicorn#2549](https://github.com/Kludex/uvicorn/pull/2549) comment is a substantive constraint/retained-version decision. The [baseplate.py#1054](https://github.com/reddit/baseplate.py/pull/1054) discussion case reports tests/type checking and adds library code. The Couchers discussion examples show approvals plus bot merge commands; Delphix shows rebase commands and bot replies. Command use is human interaction, but not equivalent to technical review.

This evidence raises a stakeholder question: which routine proposals are handled from automated context alone, and which exceptions require a person to reconcile local tests, version constraints and closure replies? The public record cannot answer how much private review occurred.
