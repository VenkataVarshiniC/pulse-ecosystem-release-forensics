# Phase 4 Milestone 1A — analytics feasibility and baseline findings

## Classification and input population

**PARTIAL.** The audit covers all 23 metric contracts, computes every defensible current metric, preserves unavailable/zero distinctions, tests grains against actual frozen artifacts, and reproduces the output. The present two convenience cases are too sparse for major Product Analyst inference, product-value metrics, observed adoption/recovery, and several proposed visuals. A PARTIAL classification reflects those evidence limits, not a failure of the audit.

Input: the frozen Phase 2 `pytest-8.0.0` case (2 repositories) and `urllib3-2.0.0` case (6 repositories), plus existing preserved task journals, candidate baselines, independent review ledger, history outputs and verified reports. The separate HTTPX live resume record is used only to assess MET-019 method feasibility, not added to either case cohort. [Manifest](baseline-analysis/input-manifest.md) records each source/identity/hash; [machine manifest](baseline-analysis/input-manifest.json) lists all 82 external journal/history origins and local inputs.

## Metric and descriptive results

| Audit result | Count / evidence |
| --- | --- |
| Metric contracts audited | **23/23** |
| Fully computable contracts | **12** (some have a case-specific zero denominator) |
| Partially computable contracts | **5** |
| Unavailable contracts | **6** |
| Core collection MET-001 | pytest **2/2**, urllib3 **6/6** |
| Historical declaration MET-002 | pytest **1/2**, urllib3 **1/6**; stronger paired pre-release **1/2**, **0/6** |
| Emission MET-008 | pytest **0/2**, urllib3 **1/6** repositories; candidate density MET-022 **0/2**, **2/6** candidates/member |
| Reviewed candidate MET-009/010 | pytest **0/0 unavailable**; urllib3 **0/2 accepted**, **2/2 rejected**, both one PR artifact |
| Required-task MET-016 | pytest **11/11**, urllib3 **27/27** |
| Optional not-found MET-017 | pytest **1/4**, urllib3 **5/12** |
| Retry incidence MET-018 | pytest **0/15**, urllib3 **0/39**, attempt logs verified |
| Replay MET-020 | **2/2 per case** exact frozen-output matches |

Every calculated row, including per-category MET-005 sufficiency and partial reported-category MET-012 UNKNOWN, is in [baseline-metrics.json](baseline-analysis/baseline-metrics.json) and the [human table](baseline-analysis/baseline-metrics.md). The [computability audit](baseline-analysis/metric-computability.md) explains missing fields and denominators. **Zero adoption/recovery is not asserted.** A 0/0 rate is unavailable, not 0%.

## Investigation, cohorts and model

The [funnel baseline](baseline-analysis/funnel-baseline.md) keeps the 2/6 declared-member spines and optional candidate branch separate. Core collection is complete; contextual history is sparse; only one pytest member supports bounded friction/remediation output; neither case has an approved repository-completion question set. The [candidate audit](baseline-analysis/candidate-review-analysis.md) confirms two rejected urllib3 firings from one copied-text PR artifact. [Evidence coverage](baseline-analysis/evidence-coverage-analysis.md) lists all eight members; [UNKNOWN analysis](baseline-analysis/unknown-analysis.md) distinguishes correct unresolved findings from missing analytical records. [Reliability](baseline-analysis/collection-reliability-analysis.md) separates operational completion from sufficiency and reports the external HTTPX 11/11 verified resume example without pooling it.

[Cohort/segment feasibility](baseline-analysis/cohort-feasibility.md) supports release, historical-status, candidate and planned-source splits, while actual adoption/recovery cohorts are invalid. Candidate rule/review dimensions are sparse; selection method and capture method are invariant in these Phase 2 cases. [Grain validation](baseline-analysis/grain-validation.md) finds unique current member/task/candidate/category rows but missing `analysis_snapshot_id`, stable observation ID and finding version; two candidate IDs share one artifact. [Fact/dimension audit](baseline-analysis/model-feasibility.md) finds a loadable bounded membership/task subset and partial finding/review/observation objects. [PostgreSQL readiness](baseline-analysis/postgresql-readiness.md) is **PARTIAL** because semantic identity, source coverage, positive finding lineage and stakeholder completion remain unresolved; no database was created.

## Gaps, quality, statistics and decisions

The [source gap matrix](baseline-analysis/source-gap-matrix.md) evaluates public exact-ref history, lockfiles, checks/Actions, downstream releases, PyPI and deps.dev **as potential future sources**, without collecting new outcome data. Major blockers are qualified target-version evidence, historical release boundary, downstream recovery eligibility, controlled conflict/UNKNOWN reasons, candidate emission time and an actual stakeholder completion rule. [Data-quality audit](baseline-analysis/data-quality-audit.md) found no current identity mismatch; the significant risks are method-limited evidence, missing stage-reason linkage and future join fan-out. [Statistical readiness](baseline-analysis/statistical-readiness.md): **descriptive only**; tiny convenience cases and dependent candidate firings do not support inference. [Dashboard audit](baseline-analysis/dashboard-readiness.md) identifies a few bounded diagnostic views and blocks/defer visuals requiring invalid denominators, source taxonomy or stakeholder decisions.

The [internal Product Analyst evidence inventory](baseline-analysis/product-analyst-evidence.md) documents question framing, contracts, denominator discipline, funnel/cohort/segment design, data-quality and model audits. [Conditional decision insights](baseline-analysis/decision-insights.md) identify next research questions, **not** final client recommendations. Product value, trust, workload tolerance, audience, priority and completion remain stakeholder-dependent. [Metric change log](metric-change-log.md): no version-1.0 definition changed; ambiguities are recorded for future governed revision.

## Reproducibility and implementation gate

The analysis-only [helper](baseline-analysis/compute_baseline.py) verifies input hashes, identities and frozen task snapshot digests. Two existing Phase 2 replays matched frozen report/summary hashes, and two baseline calculations are compared for byte-identical JSON/Markdown output in final validation. The full repository Ruff/pytest checks are run separately. No synthetic repository, candidate, accepted event, cherry-picked case or pooled ecosystem rate was introduced.

**Phase 4 implementation remains blocked by the Phase 3 HOLD.** This milestone did not install/start PostgreSQL, create tables/DDL, build dbt/Power BI, alter collectors/detectors, or start Milestone 2. A later authorized stakeholder reconciliation and evidence-source method decision are prerequisites to implementation.
