# Phase 4 Milestone 1B — frozen public PR workflow analysis

## Classification

**PARTIAL.** The frozen evidence supports useful, reproducible descriptive Product Analytics and a distinct workflow research stream. It is too small, bot-centered, earliest-page biased and publicly incomplete for broader workflow conclusions. This is an acceptable partial analytical result, not a product implementation gate.

## Dataset

Population B consists of **20 base + seven purposive discussion** public Python dependency-update PRs, one sample × repository × PR row each. The seven discussion PRs are examples, never pooled with base prevalence. All 27 were Dependabot proposals. The [dataset contract](workflow-analysis/workflow-dataset-contract.md), [quality audit](workflow-analysis/workflow-data-quality.md) and [deterministic metrics](workflow-analysis/workflow-metrics.json) preserve the source and denominators. Population A remains the separate eight-member Phase 2 forensic cohort.

## Base metrics

In the frozen base sample: visible human interaction **6/20** (WF-MET-001), explicit approval **4/20** (002), merged **9/20 terminal** (003), explicit supersession **8/20** (004), coded source/test/config modification **0/20 checked diffs** (005), copied upstream text **13/20** (006), at least one explicit workflow exception **12/20** (007), and compatibility badge/link **16/20** (008). WF-MET-009 is median elapsed PR resolution **167.25 hours** among 20/20 terminal base PRs. These are not population, labor or success measures. [Contracts](workflow-analysis/workflow-metrics-framework.md).

## Workflow funnel

All 20 selected base PRs opened and showed a Python dependency-file diff. Automated context, human interaction, exception coding, approval and disposition form overlapping **branches**, not mandatory chronological conversion steps. Nine merged and 11 closed. The [workflow funnel](workflow-analysis/workflow-funnel.md) is separate from the forensic evidence funnel.

## Human review findings

Four of nine merged base PRs and ten of 11 non-merge closures had no visible human interaction. Four base approvals were visible. One base PR contained a substantive technical comment. The seven purposive discussion PRs all had visible interaction by selection; four had approval, six had bot commands and one had a substantive technical comment. None proves private review absence. [Human review analysis](workflow-analysis/human-review-analysis.md).

## Exception findings

Eight base PRs have no coded exception and 12 have one; none has multiple labels. Eight of the 12 labels are supersession. One base PR retained an older version; one has a rebase request/up-to-date bot reply; two have other explicit bot closes. The discussion sample separately includes one multi-label test/compatibility/source-code case and three rebase-request/up-to-date replies. Administrative closures are not “friction severity.” [Exception analysis](workflow-analysis/exception-analysis.md).

## Evidence-source findings

Base PRs show manifest/requirements diff **14/20**, lockfile diff **6/20**, release notes **10/20**, changelog **9/20**, copied upstream text **13/20**, compatibility badge/link **16/20**, substantive downstream comment **1/20**. Sources overlap. Upstream issue links embedded in copied text occur in 13/20, not as downstream issues. No systematic check-run history was audited. [Evidence-source analysis](workflow-analysis/evidence-source-analysis.md).

## Disposition findings

All 20 base PRs have terminal disposition: nine merged and 11 closed without merge. Closure reasons are eight superseded, two no longer needed per bot and one ignored per bot. Merge does not prove compatibility; closure does not prove failure. [Disposition analysis](workflow-analysis/disposition-analysis.md).

## Duration findings

Base elapsed PR time: N=20, min **0.0h**, Q1 **136.3h**, median **167.25h**, Q3 **744.0h**, max **5823.4h**, IQR **607.7h**. Merged median is 136.3h (N=9); closed median 334.6h (N=11). These small, clustered segments are descriptive only and do not measure engineering time or causes. [Full distribution](workflow-analysis/resolution-time-analysis.md).

## Useful segments

Base manifest/requirements versus lockfile (**14/6**), grouped versus single dependency (**4/16**), human interaction (**6/14**), any coded exception (**12/8**), and disposition (**9/11**) are interpretable descriptive splits. Avoid repository-level or multi-way rate charts with tiny cells.

## Cross-evidence conclusions

Phase 2 shows that copied upstream text can produce false detector candidates and that historical release-boundary coverage is incomplete. Phase 3 PRs show copied context is common in selected automated proposals and expose current/proposed versions, but do not provide release-time organizational state. An exception-focused human review layer is a **hypothesis**, not a validated feature. No populations are pooled. [Comparison](workflow-analysis/cross-evidence-comparison.md).

## Product implications

Explore explicit evidence-origin labels, close-reason handling and local concern-to-evidence links as stakeholder questions. Do not treat copied upstream text, merge, duration or bot commands as product success. [Product Analytics findings](workflow-analysis/product-analytics-findings.md) separate observation, denominator, interpretation, implication, limitation and stakeholder question.

## Consulting diagnostic

The public workflow reveals upstream-context and local-decision evidence in different PR surfaces, plus heterogeneous administrative and technical exceptions. This suggests a discovery agenda, not final recommendations or quantified value. [Diagnostic](workflow-analysis/consulting-diagnostic.md).

## Dashboard implications

Base disposition, human-interaction split, exception taxonomy, evidence-source presence and elapsed-time distribution are feasible **with limitations** as secondary-workflow visuals. Purposive cases belong in a separate case ledger; adoption, recovery, detector precision and time-saved visuals remain blocked. Audience and use remain stakeholder-gated. [Prototype readiness](workflow-analysis/workflow-dashboard-readiness.md).

## Statistical limits

**Descriptive analysis only.** N=20 base, repeated repositories, search-frame/date/title bias, no manual/Renovate comparison and private-activity blindness do not support inferential tests or ecosystem estimates. No significance tests were run.

## PostgreSQL implications

The PR grain could inform a future fact design, but the frozen sample remains a secondary research dataset. A `fct_dependency_update_pr` is **not** added to PULSE's long-term operational model based solely on this evidence. [Readiness decision](baseline-analysis/postgresql-readiness.md#milestone-1b-pr-workflow-dataset-decision).

## Stakeholder questions

Which signals prompt review? What local tests, installed-version records or private channels affect a decision? Which supersession/rebase cases create meaningful work? What timestamps represent decision effort? Which exception paths deserve prioritization, and for whom? What output would change a real decision?

## Implementation gate

**Phase 3 HOLD remains binding.** This milestone adds analysis-only files and no database, dbt, Power BI, collector, detector or product implementation. Phase 4 Milestone 2 has not begun.

## Validation

The analysis-only helper reads the frozen JSONL and produced the same `workflow-metrics.json` SHA-256 (`767dd3e64560757f0a0157803ae7375c3bb047b72a63f3ca4a10e84ec0781a2a`) on two runs. The source JSONL SHA-256 remained `fa56ed46a7a8269046c92e0100740d9d5b8028908046943169a0925847968972`. A separate read-only candidate-frame comparison matched 27/27 selected IDs and found zero UTC-duration discrepancies. Repository checks: `uv run ruff check .` passed and `uv run pytest -p no:cacheprovider` passed **134 tests**.
