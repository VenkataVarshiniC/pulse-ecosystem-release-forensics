# M3 analytical findings log

All observations below are from **validation analytical outputs**, not a published governed BI dataset. Population A is the two DRAFT forensic cases (eight members); Population B's base is 20 selected Dependabot PRs, with seven purposive discussion PRs kept separate. Strength describes support *within the named frozen population*, not external validity. Interpretation and possible implication are deliberately separated from observation.

## M3-F01 — Collection versus decision coverage

- **Question / population:** Q1 and Q10; A.
- **Evidence:** MET-001, MET-016, selected findings and F5 funnel.
- **Observation:** Core collection 8/8 and required task success 38/38, yet only 2/40 reported member-category findings are bounded; 38 are UNKNOWN. Repository-level outcome is unavailable.
- **Interpretation:** Completing planned retrieval is not equivalent to answering lifecycle questions. The 2/40 diagnostic is not a governed overall decision-coverage KPI because the required question set is unapproved.
- **Strength / limitation:** High for recorded counts; low for underlying reason. Two selected cases and legacy classifications.
- **Possible product implication:** Test question-specific evidence prerequisites and answer eligibility before expanding generic collection.

## M3-F02 — Historical comparison scarcity

- **Question / population:** Q2; A.
- **Evidence:** MET-002 and member-level historical path diagnostics.
- **Observation:** Exact-ref declarations exist for 2/8 members; paired pre-release history for 1/8. Five members have an AFTER_ONLY path, and seven have an unresolved path; indicators overlap.
- **Interpretation:** Most selected member investigations lack the stronger before/after basis. AFTER_ONLY is context, not negative pre-release evidence.
- **Strength / limitation:** High for recorded paths; no release-effect estimate or claim that missing paths never existed.
- **Possible product implication:** Evaluate historical reconstruction quality on prespecified cases before broadening comparisons.

## M3-F03 — Candidate concentration and origin

- **Question / population:** Q3; A.
- **Evidence:** MET-008, MET-022, candidate-origin SQL.
- **Observation:** Two urllib3 candidate IDs came from one COPIED_UPSTREAM artifact in one repository; pytest emitted none.
- **Interpretation:** Candidate count is not artifact or repository count. The two firings are dependent.
- **Strength / limitation:** High for this frozen baseline; too few independent examples for detector precision or recall.
- **Possible product implication:** Preserve source-origin and artifact-level grouping in candidate review.

## M3-F04 — Human qualification boundary

- **Question / population:** Q4; A.
- **Evidence:** MET-009–011 and frozen review ledger.
- **Observation:** Both emitted urllib3 candidates were terminally REJECTED; acceptance is 0/2. Pytest acceptance is unavailable at 0/0.
- **Interpretation:** Human review prevented these firings from being treated as qualifying downstream evidence; a zero candidate denominator cannot be a zero acceptance rate.
- **Strength / limitation:** High for ledger outcomes; review reasoning does not prove global rule error rate.
- **Possible product implication:** Keep a transparent review gate and distinguish unavailable rates in every display.

## M3-F05 — UNKNOWN is broad, reasons are coarse

- **Question / population:** Q5; A.
- **Evidence:** Finding-context SQL, MET-012/013/015 components.
- **Observation:** 38/40 findings are UNKNOWN, and all 38 carry `unknown_insufficient_data`; two bounded NO remain separate. Six members lack exact-ref declarations and all eight have at least one legacy assessment.
- **Interpretation:** The reason code identifies insufficient recorded data but cannot attribute each UNKNOWN to a particular source, historical path, or conflict. Co-occurrence is not causation.
- **Strength / limitation:** High for counts; low for finer cause attribution because no controlled reason partition or stage-source map exists.
- **Possible product implication:** Test a governed, question-specific missing-prerequisite taxonomy.

## M3-F06 — Source presence versus source utility

- **Question / population:** Q6; A.
- **Evidence:** Selected snapshot-artifact/source SQL, 21 pytest and 51 urllib3 captures across nine source types per case.
- **Observation:** All selected captures are recorded as collector and none as fixture; adoption and recovery remain UNKNOWN in every member.
- **Interpretation:** Actual source collection is visible, but source frequency does not establish question sufficiency or value.
- **Strength / limitation:** High for selected capture inventory; cannot compare source utility without a prerequisite map and qualified outcomes.
- **Possible product implication:** Evaluate evidence type against the decision it is meant to support, not capture volume alone.

## M3-F07 — Two-case contrast is descriptive

- **Question / population:** Q7; A.
- **Evidence:** Case comparison, 2 pytest versus 6 urllib3 members.
- **Observation:** Both cases completed required collection; historical declaration is 1/2 versus 1/6, candidate emitters 0/2 versus 1/6, and UNKNOWN findings 8/10 versus 30/30 reported categories.
- **Interpretation:** The two cases have different evidence patterns in their selected frames.
- **Strength / limitation:** High for observed counts; package, release, case window and cohort selection are confounded. No package-effect inference.
- **Possible product implication:** Use case-level diagnostics to choose next validation cases, not rank packages.

## M3-F08 — Public workflow visibility

- **Question / population:** Q8; B base only.
- **Evidence:** Frozen 20-PR workflow metrics and observations.
- **Observation:** Visible interaction 6/20, approval 4/20, merge 9/20, supersession 8/20, copied upstream text 13/20, coded exception 12/20; one substantive downstream comment.
- **Interpretation:** Public PR surfaces often show automated context and disposition but limited visible substantive downstream discussion in this sample.
- **Strength / limitation:** High for coded selected PRs; convenience, bot-centered, first-page sample and private activity unknown.
- **Possible product implication:** Validate with stakeholders where real compatibility decisions occur before using PR comments as a completion proxy.

## M3-F09 — Elapsed PR time is skewed

- **Question / population:** Q8; B base only.
- **Evidence:** 20/20 terminal PR durations, interpolated quartiles, 1.5×IQR diagnostic.
- **Observation:** Median 167.25h, IQR 607.7h, maximum 5823.4h; two observations exceed the 1655.55h upper fence.
- **Interpretation:** Open-to-terminal elapsed time has a long upper tail and should be shown as a distribution.
- **Strength / limitation:** High for coded intervals; neither duration nor outlier status measures engineering effort or delay cause.
- **Possible product implication:** If duration is displayed, retain full distribution and label its clock precisely.

## M3-F10 — Metric availability is a product boundary

- **Question / population:** Q9–Q10; A and contract registry, without pooling A/B rates.
- **Evidence:** 23 versioned metric contracts: 10 READY, 7 PARTIAL, 5 evidence-unavailable, 1 stakeholder-blocked.
- **Observation:** Collection and candidate/review diagnostics execute; confirmed adoption, recovery, business completion, user value and organizational priority do not.
- **Interpretation:** SQL correctness does not fill evidence or stakeholder-definition gaps.
- **Strength / limitation:** High for current contract readiness; future methods or research can change it.
- **Possible product implication:** Treat missing decisions as explicit roadmap questions and maintain the publication gate.

## M3-F11 — Origin-aware handling is a testable hypothesis

- **Question / population:** Q3/Q8; A and B described separately.
- **Evidence:** B base copied upstream text in 13/20 selected PRs; A's two rejected urllib3 candidates share one COPIED_UPSTREAM artifact.
- **Observation:** Copied material occurs in both bounded evidence sets, under different sampling and grains.
- **Interpretation:** Together they motivate scrutiny of text origin; they do **not** show that copied text generally causes false positives.
- **Strength / limitation:** Moderate as a hypothesis generator; two dependent A firings and a nonrepresentative B sample cannot estimate mechanism frequency.
- **Possible product implication:** Prespecify an origin-aware rule evaluation with independently reviewed artifacts and compare against a clear baseline.
