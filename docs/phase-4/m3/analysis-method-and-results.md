# M3 analysis method and descriptive results

These are **validation analytical outputs** from two DRAFT forensic snapshots and an existing frozen public-PR research sample. They are not a published governed BI dataset. `scripts/analyze_product_patterns.py` reads the M2.5 SQL-derived baseline/diagnostics, queries selected marts read-only for finding reasons and candidate origin, and consumes the frozen Phase 3 PR observations plus their existing workflow baseline. The generated [JSON](../../../data/analysis/m3-product-analytics-results.json), CSVs, and four exploratory SVGs retain input hashes. No new evidence was collected.

| Population | Unit and size | Selection | Permitted use | Prohibited inference |
|---|---|---|---|---|
| A: forensic validation | Case × declared repository: pytest 8.0.0 = 2, urllib3 2.0.0 = 6; eight member investigations | Predeclared Phase 2 validation cases, selected snapshots DRAFT | Bounded evidence, collection, candidate and finding diagnostics | Ecosystem incidence, package effect, adoption or recovery prevalence |
| B: public workflow base | One selected Dependabot PR: 20 | Convenience, title/first-page-biased Phase 3 base sample | Within-sample workflow descriptions and elapsed open-to-terminal time | All dependency-update workflows, private review or engineering effort |
| B: purposive discussion | Seven additional Dependabot PRs | Deliberately selected for visible interaction | Named qualitative examples only | Pooled rates with the base 20, prevalence comparison |

No rate combines A and B. The 20/7 PR samples are kept separate even within B. Case percentages below use their own frozen 2/6 denominator. Candidate percentages use candidate IDs, never member counts.

## Q1 — Where does certainty break down?

| Evidence pathway | Numerator / denominator | Share | Grain | Interpretation and limit |
|---|---:|---:|---|---|
| Declared and core collected | 8/8 | 100% | Member | Planned required collection completed, not decision sufficiency |
| Exact-ref historical declaration | 2/8 | 25% | Member | A historical declaration exists, not observed adoption |
| Paired pre-release history | 1/8 | 12.5% | Member | Stronger comparison path; a subset, not a new mandatory funnel transition |
| Category-specific sufficient assessment | 2/40 | 5% observed records | Member × category | Only migration friction and remediation, each 1/8; governed MET-005 rate remains PARTIAL because 38 assessments are legacy |
| Bounded non-UNKNOWN finding | 2/40 | 5% observed records | Member × category | Two bounded NO; 38 UNKNOWN; no repository-level completion conclusion |
| Candidate-emitting members | 1/8 | 12.5% | Member | Optional branch; zero candidate does not mean no event |
| Candidate IDs emitted | 2 IDs | n/a | Candidate | Both from one artifact and one repository |
| Terminally reviewed IDs | 2/2 | 100% | Candidate | Both REJECT; no accepted finding is implied |
| Accepted IDs | 0/2 | 0% | Reviewed candidate | Pytest alone has 0/0 and unavailable acceptance |
| Repository-level outcome | unavailable / 8 | n/a | Member | Approved required question set is absent |

These are **parallel evidence-processing branches**, not a single conversion sequence. Collection, historical context, candidate review and lifecycle categories do not imply chronology or causality. Category denominators are 8 each: UNKNOWN is 8/8 adoption readiness, 8/8 observed adoption, 8/8 recovery, 7/8 migration friction, and 7/8 remediation. The two bounded NO findings occur in the latter categories of one pytest member. There is no YES finding.

## Q2 — Historical context

Exact-ref declaration evidence is 1/2 pytest and 1/6 urllib3. Paired pre-release history is 1/2 and 0/6. An AFTER_ONLY path occurs for one pytest and four urllib3 members; six AFTER_ONLY **path records** occur across those five members. Unresolved paths occur for seven members, with nine unresolved path records. These indicators overlap: a member can have more than one path status. AFTER_ONLY is context, not a pre-release comparison or negative release-window observation. The scarcity of paired evidence limits before/after interpretation even where collection tasks succeeded.

## Q3–Q4 — Candidate generation and human review

Pytest emitted zero candidates from two members. Urllib3 emitted two candidate IDs from one of six members and one artifact. Both candidate rows have `source_origin=COPIED_UPSTREAM`; independent terminal reviews rejected one as `generic_dependency_mention` and one as `bot_or_dependency_update_noise`. The firings are dependent and do not estimate detector precision or recall. Review is the documented qualification boundary: a detector firing did not become an accepted downstream event. Urllib3 acceptance is the valid 0/2; pytest acceptance is unavailable at 0/0, not 0%. No-candidate members remain in the declared denominator.

## Q5 — UNKNOWN and evidence gaps

The 38 UNKNOWN findings are 8 pytest and 30 urllib3, across the category counts above. Every UNKNOWN has the generic recorded reason `unknown_insufficient_data`. That code does not partition missing sources, historical context, conflict, or question-specific causes. Co-occurring member indicators are: no exact-ref declaration 6/8; zero candidates 7/8; at least one legacy sufficiency assessment 8/8; at least one UNKNOWN finding 8/8. These overlap, and none can be assigned as the cause of a particular UNKNOWN without a governed reason/source mapping. `LEGACY_UNCLASSIFIED` is not recoded as insufficient. The two bounded NO findings remain distinct from UNKNOWN.

## Q6–Q7 — Source usage and case comparison

The selected-capture SQL joins actual snapshot artifacts, not just source registry rows: nine source types occur in each case, with 21 pytest and 51 urllib3 selected captures. All selected Phase 2 captures are recorded as collector; zero fixtures are included. A source's frequency says nothing about its sufficiency for adoption or recovery. For both cases, required tasks completed (11/11 and 27/27), while exact-ref declaration coverage was 1/2 and 1/6. Candidate-emitting members were 0/2 and 1/6; UNKNOWN findings were 8/10 and 30/30 reported categories. The cases differ in selection frame and size; none of these contrasts is a package effect.

## Q8 — Public PR workflow sample

Among the **20 selected base PRs**, visible human interaction occurred in 6/20, explicit approval in 4/20, merging in 9/20, closing without merge in 11/20, explicit supersession in 8/20, copied upstream text in 13/20, any coded exception in 12/20, and a compatibility badge/link in 16/20. One PR had a substantive downstream review comment; 14/20 had no visible human interaction. The visible interaction × disposition cross-tab is: interacted 5 merged/1 closed; no visible interaction 4 merged/10 closed. This is a selected-sample association, not evidence that interaction causes merging. Manifest diffs appear in 14/20, lockfile diffs 6/20, upstream issue links 13/20, and no coded downstream issue links or test-results evidence appear. A badge/link is not a verified score. The seven purposive discussion PRs are retained separately as examples.

The seven purposive examples were selected for visible discussion: all seven have visible interaction, six include bot-command usage, and the coded examples include a test-failure concern and a compatibility concern. Four were merged and three closed without merge. These are case descriptions, not a second prevalence estimate or a comparison rate against the base sample.

For 20/20 base terminal PRs, observable **PR open-to-terminal duration** (hours) is min 0, Q1 136.3, median 167.25, Q3 744, max 5823.4, IQR 607.7, mean 708.79, population standard deviation 1290.29. Quartiles use `(n−1)×p` linear interpolation inherited from the workflow baseline. The 1.5×IQR fences are −775.25 and 1655.55 hours. Two high observations exceed the upper fence: `delphix/virtualization-sdk#605` (2032.5h) and `gugarosa/statys#39` (5823.4h). Neither is removed. The high mean relative to the median and long upper tail show skew; they do not measure labor, bottleneck cause, or time saved.

## Q9–Q10 — Analytical product boundary

The 23 metric contracts comprise 10 READY, six PARTIAL_EVIDENCE, one PARTIAL_PLATFORM, five UNAVAILABLE_EVIDENCE, and one BLOCKED_STAKEHOLDER. Technical SQL can calculate collection, declaration, candidate and review measures. It cannot turn absent qualified version evidence into adoption, absent event/window evidence into recovery, missing question approval into business completion, or public PR observations into user value or organizational priority. Metric availability is itself a diagnostic: the immediate bottleneck is **decision-grade evidence and interpretation**, despite complete planned core collection in these two cases. This is an analytical boundary, not a claim that additional collection alone would solve it.

| Planned segment | Readiness | Bounded use or reason |
|---|---|---|
| Case/release; exact-ref declaration present versus absent | USABLE | Counts and missingness only; 2/8 have declaration, so no stable outcome comparison |
| Evidence source and capture method | USABLE | Actual selected-capture inventory; no source-utility ranking |
| Paired history; AFTER_ONLY/unresolved path | SPARSE | Only one paired member; path indicators overlap |
| Candidate rule, origin, review | SPARSE | Two dependent candidates from one artifact/repository |
| Provider and core collection | INVARIANT | All eight GitHub; all eight core-collected |
| Adoption, recovery, business outcome, role and value | UNAVAILABLE | No qualified outcome or primary stakeholder evidence |

**Should formal inferential statistics be used here? FORMAL INFERENCE NOT JUSTIFIED.** Population A has two deliberately validated cases, eight nonrandom members, one candidate artifact, and no YES/adoption/recovery outcome. Population B is a 20-PR convenience sample clustered by repository/time and biased by first-page/title selection; the seven discussion PRs were chosen for interaction. Sampling independence and representativeness are not established, many cells are sparse, and the desired product outcomes are unavailable. No p-values, regressions, confidence intervals, or causal claims are generated. Descriptive statistics and explicit missingness are the defensible output.

The four exploratory figures show the [member evidence path](figures/member-evidence-path.svg), [candidate review path](figures/candidate-review-path.svg), [UNKNOWN category composition](figures/unknown-by-category.svg), and [base PR duration distribution](figures/base-pr-duration.svg). They are static validation-analysis aids, not Power BI dashboards.
