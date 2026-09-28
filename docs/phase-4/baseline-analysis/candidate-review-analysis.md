# Candidate and review baseline

| Case | Emitted | Distinct repository | Distinct source artifact | Accepted | Rejected | Needs review | Reviewed acceptance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| pytest 8.0.0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/0, **unavailable** |
| urllib3 2.0.0 | 2 | 1 (`jamesturk/scrapelib`) | 1 (Dependabot PR #226) | 0 | 2 | 0 | 0/2 (0%) within reviewed emissions |

The urllib3 rules `text.version_specific_remediation` and `text.version_specific_friction` fired once each on the **same PR body and content digest**. Candidate IDs differ, so there is no duplicate candidate identity; the shared artifact creates **dependent rule firings**, not two independent event observations. Both terminal reviews rejected the candidates: one `bot_or_dependency_update_noise`, one `generic_dependency_mention`. The copied upstream release notes describe urllib3, not a demonstrated downstream scrapelib breakage or remediation. The PR's proposed range does not show target-version installation. No candidate entered the accepted ledger.

Candidate density is 0/2 for pytest and 2/6 for urllib3; emission coverage is 0/2 and 1/6 members respectively. Neither rate measures release impact. `0/2` is **not** a population detector-precision estimate; recall lacks independently labeled non-emitted records. Review `reviewed_at` exists, but baseline candidate `occurred_at` is the source PR event, **not** emission/availability time, so MET-023 review duration is unavailable. See [baseline metrics](baseline-metrics.md) and preserved [review ledger](../../phase-2/evaluation-data/review-ledger.jsonl).
