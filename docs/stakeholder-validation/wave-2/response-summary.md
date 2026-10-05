# Wave 2 quantitative response summary

Wave 2 contains **5 new responses** and **14 cumulative responses**. Counts below use the stated denominator. Multi-select percentages may sum above 100%. No inferential statistics or significance tests are used.

## Experience and scope

Direct dependency-upgrade experience was 3/5 among additions and 10/14 (71%) cumulatively. Explicit multi-repository scope was 2/5 among additions and 7/14 (50%) cumulatively; 3/14 were unsure.

The cumulative leading upgrade triggers were new feature requirements and CI/build failures at 6/14 each, security vulnerabilities 5/14, and compatibility, outdated dependencies, automated updates, and end-of-support/deprecation at 4/14 each.

## Evidence and investigation

| Evidence source | New n = 5 | Cumulative n = 14 |
| --- | ---: | ---: |
| GitHub/GitLab issues | 2/5 | 11/14 (79%) |
| Application/runtime logs | 3/5 | 8/14 (57%) |
| Test results | 4/5 | 7/14 (50%) |
| Commit history | 1/5 | 6/14 (43%) |
| CI/CD results | 1/5 | 5/14 (36%) |
| Pull requests | 1/5 | 5/14 (36%) |
| Manifest | 2/5 | 4/14 (29%) |
| Package documentation | 2/5 | 4/14 (29%) |

Eleven of fourteen respondents selected at least two evidence sources. Most-confidence sources remain heterogeneous: package documentation and tests 3/14 each, commit history 2/14, and six other answers 1/14 each.

The leading cumulative affected-repository methods were CI/build failures 9/14, automated update tools, repository knowledge, manual search, and manifest search 5/14 each, and lockfile search or central inventory 4/14 each.

## Manual work and uncertainty

Cumulative manual-effort selections were actual-version discovery 7/14, documentation and issue/PR/commit search 6/14 each, reproduction, breaking-change understanding, and completion determination 5/14 each, and causality or affected-repository identification 4/14 each.

Historical-version difficulty was mean **3.21/5**, median **3/5**: 11/14 selected 3 and 3/14 selected 4. Insufficient causal evidence was “Sometimes” for 9/14, “Rarely” for 3/14, and “Not sure” for 2/14.

When evidence was incomplete, 8/14 investigated more sources, 8/14 reproduced locally, 7/14 ran more tests, and 5/14 treated the issue as potentially related until ruled out.

## Current tools and recurring problems

Current-tool support was mean **3.36/5**, median **3/5**: 9/14 selected 3 and 5/14 selected 4. No respondent selected either endpoint.

| Encountered problem | Cumulative count |
| --- | ---: |
| Irrelevant dependency alerts | 8/14 (57%) |
| Unclear upgrade causality | 8/14 (57%) |
| Too much manual investigation | 7/14 (50%) |
| Historical-state difficulty | 6/14 (43%) |
| Unclear affected repository set | 6/14 (43%) |
| Evidence spread across systems | 3/14 (21%) |
| Installed/resolved-version difficulty | 3/14 (21%) |
| Completion difficulty | 3/14 (21%) |

## Trust, output, and usefulness

Trust inputs were CI/test evidence 8/14, version information, historical state, and explanation 7/14 each, original links 6/14, and missing-evidence indication or related issue/PR 5/14 each.

Insufficient-evidence preferences were likely answer plus explicit uncertainty 4/14, confidence score 3/14, explicit UNKNOWN 3/14, and non-reliance on automated conclusions 4/14. The five additions contained no likely-answer-plus-uncertainty selection: two chose explicit UNKNOWN, two non-reliance, and one confidence score.

Traceability importance was mean **4.07/5**, median **4/5**; 10/14 (71%) rated it 4 or 5. Usefulness was mean **3.86/5**, median **4/5**, with ratings 2 (1/14), 3 (5/14), 4 (3/14), and 5 (5/14).

Most useful capability was affected-repository identification 5/14, centralized evidence 4/14, missing/uncertain evidence 3/14, historical reconstruction 1/14, and an investigation report 1/14. None of the five additions selected affected-repository identification as the single most useful capability.

## Barriers and follow-up

Lack of trust led at 9/14 (64%). Integration effort, false positives, and security/privacy were 5/14 each; review burden 4/14; private-data limitations and existing-tool sufficiency 3/14 each; decision non-impact and low frequency 2/14 each.

Follow-up willingness was Yes 3/14, Maybe 4/14, and No 7/14.
