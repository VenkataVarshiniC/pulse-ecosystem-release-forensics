# Wave 1 quantitative response summary

All denominators are the Wave 1 convenience sample, **n = 9**, unless stated otherwise. Multi-select percentages may sum above 100%. No inferential statistics or significance tests are used.

## Upgrade context

- 7/9 (78%) reported direct dependency-upgrade experience; 2/9 (22%) reported none.
- Recent scopes were one repository for 3/9, two to five for 4/9, six to ten for 1/9, and unsure for 1/9.
- The most selected triggers were new feature requirement 5/9, security vulnerability 3/9, compatibility requirement 3/9, CI/build failure 3/9, and end-of-support/deprecation 3/9.

## Evidence and investigation

| Selected evidence source | Count |
| --- | ---: |
| GitHub/GitLab issues | 9/9 |
| Commit history | 5/9 |
| Application/runtime logs | 5/9 |
| Pull requests | 4/9 |
| CI/CD results | 4/9 |
| Test results | 3/9 |
| Manifest | 2/9 |
| Lockfile | 2/9 |
| Package documentation | 2/9 |

Seven respondents selected at least two evidence sources. Their single most-confidence source varied: package documentation 3/9, tests 2/9, CI 1/9, PRs 1/9, issues 1/9, and context-dependent 1/9.

Affected-repository methods were also distributed: CI/build failures 6/9, repository knowledge/documentation 5/9, automated update tools 4/9, and dependency graphs, manual search, manifest search, lockfile search, and central inventory each 3/9.

## Manual effort and uncertainty

| Manual-effort selection | Count |
| --- | ---: |
| Find version actually used | 5/9 |
| Search issues/PRs/commits | 4/9 |
| Determine remediation completion | 4/9 |
| Identify affected repositories | 3/9 |
| Understand breaking changes | 3/9 |
| Determine whether failure is upgrade-related | 3/9 |

Historical-version difficulty had mean **3.22/5** and median **3/5**: 7/9 selected 3 and 2/9 selected 4. Six respondents encountered insufficient causal evidence “Sometimes” and three “Rarely”; none selected a stronger or weaker category in this export.

When evidence was incomplete, 6/9 investigated additional sources, 5/9 reproduced locally, 4/9 treated the issue as potentially related until ruled out, and 3/9 ran more tests. One assumed it unrelated unless proven otherwise and one delayed the decision.

## Current tools and problems

Current-tool support had mean **3.33/5** and median **3/5**: 6/9 selected 3 and 3/9 selected 4. Tool use was fragmented across CI platforms, internal tools, scripts, source hosts, package managers, search tools, update bots, and one security tool.

Top personally encountered problems were irrelevant dependency alerts 5/9, unclear upgrade causality 5/9, too much manual investigation 4/9, historical-state difficulty 3/9, and uncertainty about which repositories need attention 3/9. Two selected evidence spread across systems. One selected that existing tools already solve most problems.

## Trust, uncertainty, and usefulness

Before trusting an automated result, respondents selected CI/test evidence 5/9, dependency-version information 5/9, historical state 5/9, explanation 4/9, original evidence link 3/9, missing-evidence indication 3/9, and human review 2/9.

Insufficient-evidence output preference was split:

- likely answer plus explicit uncertainty: 4/9;
- most likely answer with confidence score: 2/9;
- would not rely on automated conclusions: 2/9;
- explicit “insufficient evidence / unknown”: 1/9.

Traceability importance had mean **4.11/5**, median **4/5**, and 7/9 ratings of 4 or 5. Usefulness had mean **3.89/5**, median **4/5**, with ratings: 2 (1/9), 3 (3/9), 4 (1/9), and 5 (4/9).

Most useful capability was affected-repository identification for 5/9, centralized evidence for 2/9, historical reconstruction for 1/9, and highlighting uncertainty for 1/9.

## Barriers

Lack of trust and integration effort were each selected by 5/9. False positives and security/privacy concerns were each selected by 4/9. Human-review burden was 3/9; private-data limitations, existing-tool sufficiency, and results not affecting decisions were each 2/9. One respondent selected low problem frequency.

Follow-up willingness was Yes 1/9, Maybe 4/9, and No 4/9.
