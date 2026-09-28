# Statistical and Python analysis plan

Phase 2's 2- and 6-member convenience cohorts, two dependent candidate firings and no accepted events do **not** justify inferential claims, significance tests, broad confidence intervals or machine learning. Descriptive case-level counts and complete uncertainty reporting are the current defensible choice.

| Possible technique | Preconditions before use | Intended question and interpretation limit |
| --- | --- | --- |
| Descriptive distribution | Verified grain, denominator, selection frame, missingness; enough observed values to show distribution. | Compare coverage/review-reason patterns; no population generalization. |
| Binomial/proportion interval | A meaningful sampled population or repeated independent eligible units, stable method and adequate denominator. | Quantify uncertainty of a defined rate; frozen convenience repositories do not meet representativeness. |
| Proportion comparison | Comparable cohorts/source plans, independent or appropriately clustered units, adequate events; prespecified question. | Explore coverage-method difference, never causal effect of release or product. |
| Nonparametric comparison | Trustworthy continuous measure (e.g., review elapsed time), enough independent cases and prespecified grouping. | Compare distributions when shape is unsuitable for parametric assumptions; elapsed time ≠ work hours. |
| Bootstrap interval | Resampling unit matches dependence structure (likely artifact/repository/case cluster), enough clusters and measured variable. | Sensitivity interval, not a cure for convenience selection or zero events. |
| Correlation/exploratory association | Multiple comparable cases, measured variables, missingness audit and alternative mechanisms. | Generate hypothesis about source coverage vs UNKNOWN; no causal attribution. |

**Python's complementary role:** reproducible scripts/notebooks for distribution exploration, interval/sensitivity calculations when preconditions hold, anomaly and data-quality diagnostics, and investigation plots that are awkward in SQL. SQL owns canonical cohort, join, denominator and metric extraction; Python consumes a versioned, read-only analytical extract with method metadata. No model classifier, RAG, embeddings or ML is justified now. Every analysis plan records unit of analysis, selection mechanism, missingness, clustering, assumptions, alternative explanations and whether results are exploratory. No statistics or Python analysis code is executed in Milestone 1.
