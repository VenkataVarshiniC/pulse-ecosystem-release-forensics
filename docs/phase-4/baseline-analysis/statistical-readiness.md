# Statistical readiness for the Phase 4 analysis plan

The available population is two **convenience cases** with 2 and 6 members, plus two dependent rule firings from one PR. No inferential statistic can repair that selection or dependence. The [Milestone 1 preconditions](../statistical-analysis-plan.md) are audited below.

| Technique | Classification now | Reason / permissible use |
| --- | --- | --- |
| Descriptive distributions and exact counts | **Currently valid within these files** | Show per-case counts, full N/D and missingness; no ecosystem inference. |
| Confidence interval for a population proportion | **Biased sample / future only** | No probability sample or validated target population; 0/2 candidate acceptance is clustered in one artifact. |
| Proportion comparison | **Insufficient N and incomparable cases** | Different package/case context and tiny denominators; no comparative effect estimate. |
| Nonparametric review-time comparison | **Missing field / insufficient N** | Candidate emission time absent; only two terminal reviews from one PR. |
| Bootstrap interval | **Non-independent observations / insufficient clusters** | Candidate-level resampling would double count one artifact; two cases cannot support useful cluster bootstrap. |
| Correlation/exploratory association | **Descriptively usable only, no inferential analysis** | At most eight members, strong method/case confounding; may formulate source-gap hypotheses but no reliable association claim. |
| Machine learning/classification | **Future only, no present analytical need** | No labeled non-emitted universe or representative training data; not an authorized phase objective. |

**Conclusion:** current data supports descriptive analysis only. No significance tests, confidence bounds, bootstrap, causal estimate or ML model are run in Milestone 1A.
