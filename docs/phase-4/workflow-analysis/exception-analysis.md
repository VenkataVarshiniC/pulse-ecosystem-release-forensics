# Explicit workflow exception taxonomy

Labels are derived from frozen `concerns`, `additional_work`, and close reason in the [analysis helper](compute_workflow_baseline.py). They are **multi-label**, and an empty label set means no exception coded in accessible evidence, not that nothing happened privately. “Exception” includes administrative PR lifecycle handling and must not be renamed “friction severity.”

| Label / source | Base PR count (D=20) | Purposive example count (N=7) |
| --- | ---: | ---: |
| Test failure (`concerns`) | 0 | 1 |
| Compatibility concern (`concerns`) | 0 | 1 |
| Retained older version (`version_constraint`) | 1 | 0 |
| Source-code modification | 0 | 1 |
| Test modification | 0 | 0 |
| Configuration change | 0 | 0 |
| Completed rebase/recreation coded | 0 | 0 |
| Explicit supersession close | 8 | 0 |
| Rebase request plus up-to-date/no-longer-needed reply | 1 | 3 |
| Other explicit bot close | 2 | 0 |

Base case label count: **8/20 zero**, **12/20 one**, **0/20 multiple**. Discussion case label count: three of seven zero, three one, one three; these are examples, not prevalence. The three-label case is [baseplate.py#1054](https://github.com/reddit/baseplate.py/pull/1054): test failure, compatibility concern and library-code modification. [uvicorn#2549](https://github.com/Kludex/uvicorn/pull/2549) retained an older `websockets` pin. Eight base closures were explicitly superseded; that does not establish failed migration or wasted work. In four command cases (one base, three discussion), a human asked for rebase and Dependabot replied that the dependency was already up to date; the code does not assert rebase completion. The two other base bot closes are one no-longer-needed reason without a visible command and one ignored-release response. Labels represent different types and can overlap in a future dataset; their sum is never treated as a severity score.
