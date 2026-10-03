# Phase 7 preregistered evaluation plan

Status: **FROZEN BEFORE IMPLEMENTATION** under [the experiment charter](experiment-charter.md).

## Comparison design

The comparison holds population, lifecycle questions, core collection status, candidate baseline, reviews, and published findings constant. The intended treatment difference is the historical reconstruction and availability/prerequisite method described by `p7-boundary-anchor-depth-v1`.

The unit of historical comparison is one declared member × one approved manifest path (`n = 16`). The finding unit is one declared member × one of the five existing lifecycle categories (`n = 40`). Candidate/review comparisons use candidate IDs and distinct artifact IDs separately. No denominator is pooled with the separate public PR research.

## Frozen baseline values

| Measure | Baseline |
| --- | ---: |
| Declared members | 8 |
| Core-collected members | 8 |
| Historical context records | 16 |
| `PAIRED` | 1 |
| `AFTER_ONLY` | 6 |
| `UNRESOLVED` | 9 |
| Eligible lifecycle assessments | 40 |
| `SUFFICIENT` | 2 |
| `INSUFFICIENT` | 38 |
| `UNKNOWN` findings | 38 |
| Bounded NO findings | 2 |
| Positive supported findings | 0 |
| Finding support links | 0 |
| Candidate IDs | 2 |
| Accepted / rejected candidates | 0 / 2 |
| Distinct candidate artifacts | 1 |

The baseline source-availability taxonomy was not fully explicit, so baseline availability is reconstructed only from preserved statuses and reported as `BASELINE_LEGACY_MAPPING`; it is not silently relabeled as a treatment observation.

## Historical state rules

- `PAIRED`: both exact-ref approved-path states are retrieved, parsed, and comparable. Target declaration may be present or absent; target qualification is a separate prerequisite.
- `AFTER_ONLY`: the after state is retrieved and parsed, while the before path is exact-ref `NOT_FOUND`. It does not establish historical absence outside that path/ref.
- `UNRESOLVED`: anchors are missing, a required response is unavailable/incomplete, parsing prevents comparison, or source states conflict.

A baseline state can change only when a treatment source record supports the new state. No inferred or latest-state substitution is allowed.

## Experimental measures

### P7-M01 — Prerequisite coverage

- **Population:** 40 frozen member-question assessments.
- **Numerator:** Assessments for which every `p7-question-prerequisites-v1` required prerequisite is satisfied.
- **Denominator:** All 40 assessments, reported by case and lifecycle question.
- **Eligibility:** Declared member and existing lifecycle category.
- **Missingness:** Missing, unavailable, incomplete, conflicting, or not-planned prerequisites remain uncovered with a reason; no UNKNOWN becomes NO.
- **Interpretation:** Coverage of declared evidence prerequisites under the treatment.
- **Limitation:** Coverage does not establish finding correctness, utility, or a positive event.

### P7-M02 — Paired historical-context availability

- **Population:** 16 frozen member-path records.
- **Numerator:** Records classified `PAIRED` under the treatment rules.
- **Denominator:** All 16 records.
- **Eligibility:** One of the two approved paths for a declared member.
- **Missingness:** AFTER_ONLY and UNRESOLVED remain in the denominator; a failed full run makes the metric unavailable.
- **Interpretation:** Exact-ref before/after path-state availability.
- **Limitation:** A pair is not installation, adoption, compatibility, or exact transition timing.

### P7-M03 — Lifecycle-question sufficiency

- **Population:** 40 frozen member-question assessments.
- **Numerator:** Assessments classified `SUFFICIENT` by the frozen question contract.
- **Denominator:** All 40 assessments, with lifecycle breakdown.
- **Eligibility:** Existing category; no new question added.
- **Missingness:** Unmet prerequisites stay `INSUFFICIENT`; missing contract makes the run invalid rather than defaulting a result.
- **Interpretation:** Questions eligible for a bounded answer.
- **Limitation:** Sufficiency may produce bounded NO and does not establish usefulness.

### P7-M04 — Bounded decision availability

- **Population:** 40 frozen findings.
- **Numerator:** Supported positive or bounded NO findings produced under satisfied prerequisites.
- **Denominator:** All 40 findings, with state distribution shown.
- **Eligibility:** Integrity and method-version checks pass.
- **Missingness:** UNKNOWN remains denominator and retains a controlled reason.
- **Interpretation:** Availability of an evidence-bounded answer.
- **Limitation:** A higher value can be entirely bounded negative and is not outcome incidence.

### P7-M05 — Support-link completeness

- **Population:** Supported positive findings only.
- **Numerator:** Positive findings with an intact finding → qualifying evidence → source/provenance path.
- **Denominator:** All supported positive findings.
- **Eligibility:** Positive state under the treatment contract.
- **Missingness:** Zero positive findings yields unavailable `0/0`, never 100%; missing edge blocks the positive finding.
- **Interpretation:** Positive-finding provenance integrity.
- **Limitation:** It cannot be live-validated if the positive denominator remains zero.

### P7-M06 — Unresolved reason distribution

- **Population:** Treatment `UNKNOWN` assessments and `UNRESOLVED` history records, reported separately.
- **Numerator:** Count in each controlled unresolved reason.
- **Denominator:** All UNKNOWN assessments or all UNRESOLVED records in the corresponding distribution.
- **Eligibility:** Treatment method and reason-taxonomy version present.
- **Missingness:** Missing reason is a validation failure; zero unresolved records makes the distribution unavailable.
- **Interpretation:** Why the bounded method cannot answer.
- **Limitation:** Reasons describe evidence state, not repository-team causation.

### P7-M07 — Method delta

- **Population:** The 16 historical records and 40 findings with exact baseline/treatment identity matches.
- **Numerator:** Records whose history state, prerequisite coverage, sufficiency, or support-link status changes with valid treatment evidence.
- **Denominator:** Comparable records in the corresponding grain.
- **Eligibility:** Same case/member/path or case/member/question; baseline digests match.
- **Missingness:** Unmatched identities invalidate the comparison; treatment failures are reported, not dropped.
- **Interpretation:** Change associated with the method on this frozen population.
- **Limitation:** It does not establish transferability or causality beyond the controlled method comparison.

### P7-M08 — Provenance completeness

- **Population:** All Phase 7 treatment source attempts and derived historical records.
- **Numerator:** Records with method/run/task identity, repository, query, exact ref/path where applicable, outcome, retrieval time, event time where available, content digest for retrieved content, and raw reference.
- **Denominator:** All treatment attempts/records.
- **Eligibility:** Record belongs to the frozen evaluation run.
- **Missingness:** Missing required provenance is an integrity failure; no partial percentage authorizes publication.
- **Interpretation:** Auditability of the treatment evidence chain.
- **Limitation:** Complete provenance does not make the underlying evidence sufficient.

## Source-availability distribution

Every treatment attempt must use exactly one state from the versioned taxonomy: `NOT_PLANNED`, `AVAILABLE`, `NOT_FOUND`, `INCOMPLETE`, `SOURCE_UNAVAILABLE`, `STRUCTURALLY_UNAVAILABLE`, or `CONFLICTING`. Counts are reported by case, repository, path, anchor role, and source type where applicable. These states describe evidence access/fitness and do not themselves determine a finding.

## Question-specific finding evaluation

- `migration_friction` and `remediation` may become sufficient only when core collection/review remains complete and a qualifying pre-release target declaration exists in a valid exact-ref treatment pair. With no accepted qualifying event, the output may be bounded NO under the existing bounded method.
- `adoption_readiness` and `observed_adoption` remain UNKNOWN because Phase 7 collects no qualified installed/resolved-version evidence.
- `recovery_signal` remains UNKNOWN because Phase 7 collects no downstream recovery source or eligible denominator.
- A positive finding requires accepted qualifying evidence and an intact support link; no rule is relaxed.

## Candidate and review evaluation

Candidate IDs, decisions, and artifact identities are inputs, not treatment targets. Expected delta is zero. Any new candidate, changed review, or split of the shared artifact is an experiment-integrity failure.

## Success and decision rules

- **GO_BOUNDED:** At least one evidence-depth improvement from the charter is observed, all integrity checks pass, and remaining work is a separately bounded method validation rather than breadth/product expansion.
- **GO:** Reserved for a complete evidence-depth method with transfer evidence; the frozen two-case experiment alone is unlikely to justify it.
- **HOLD:** Execution is valid but access or evidence is insufficient to decide whether further method work is warranted.
- **PIVOT:** Execution shows the proposed depth path is weak and a narrower evidence-audit or different approved method is more defensible.
- **STOP:** Required evidence is structurally inaccessible or the method adds no defensible capability relative to cost/risk.

Phase classification concerns rigor: a valid negative result may still be `PASS` or `PASS_WITH_LIMITATIONS`.

## Validation outputs

The evaluator must produce exact JSON values, a member-level change log, baseline/treatment digests, source-attempt and stop-reason counts, candidate identity comparison, support-link status, and a deterministic rerun check from committed raw evidence. Every documentation number must be regenerated or checked against those outputs.

`G8 = NOT_YET_VALIDATED` and no stakeholder or portfolio claim is evaluated.
