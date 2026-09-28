# PR workflow metric contracts

These are **Population B** metrics at PR grain. `N/D` always means a count of frozen **base** PRs, except WF-MET-003, whose denominator is terminal base PRs (20 at this cutoff). Values are descriptive of the selected records only. The seven purposive discussion PRs are never added to a prevalence denominator. All rates retain zero as a coded public-observation result, never a statement about unobserved behavior.

| ID | Metric | Numerator | Denominator | Frozen result | Interpretation limit |
| --- | --- | --- | --- | --- | --- |
| WF-MET-001 | Human interaction share | Visible public human interaction | All base PRs | 6/20, 30% | No private review inference. |
| WF-MET-002 | Visible approval share | Explicit approval | All base PRs | 4/20, 20% | No test-pass inference. |
| WF-MET-003 | Merge share | Merged | Terminal base PRs | 9/20, 45% | Disposition, not successful migration. |
| WF-MET-004 | Supersession share | Explicit `superseded` close reason | All base PRs | 8/20, 40% | Not wasted work. |
| WF-MET-005 | Additional-code-change share | Source, test or config modification coded true | Base PRs with checked diff coding | 0/20, 0% | Public checked diff only; discussion case has code change. |
| WF-MET-006 | Copied-upstream-context share | Copied notes/changelog present | All base PRs | 13/20, 65% | Not downstream-specific evidence. |
| WF-MET-007 | Visible exception share | At least one [explicit taxonomy](exception-analysis.md) label | All base PRs | 12/20, 60% | Includes routine lifecycle closures; not “friction” rate. |
| WF-MET-008 | Compatibility badge/link share | Link/badge present | All base PRs | 16/20, 80% | Underlying score unverified. |

WF-MET-009 is PR resolution duration: `N=20` eligible terminal base PRs, `D=20` base PRs, median **167.25 hours**, Q1 **136.3**, Q3 **744**, IQR **607.7** hours. Its value unit is **elapsed hours**, not a share; the distribution, not just one point estimate, belongs in any display. [Machine results](workflow-metrics.json) preserve all nine contracts; [resolution-time analysis](resolution-time-analysis.md) carries WF-MET-009's full descriptive contract and groups. There is no labor, productivity or time-saved KPI.
