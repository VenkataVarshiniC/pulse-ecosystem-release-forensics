# Phase 6 proposed success measures

## Status and use

Every measure in this document is **PROPOSED**. None is an established business KPI, target, or authorization to change the [governed metric registry](../../analytics/metrics/metric_registry.yml). A future implementation must version, review, and publish contracts through the existing metric-governance process.

Rates must be reported with numerator, denominator, case/population, eligibility, and missingness status. A zero denominator is `UNAVAILABLE_ZERO_DENOMINATOR`, never 0%. Missing evidence may reduce eligibility or produce `UNKNOWN`; it must not become a negative outcome.

## PROPOSED P6-01 — Evidence prerequisite coverage

- **Numerator:** Eligible member-question assessments for which every predeclared required evidence prerequisite has a qualifying observation or an explicitly permitted terminal state.
- **Denominator:** All eligible member-question assessments in the frozen experiment population.
- **Population:** One named case/method version, or separately reported named cases; never an ecosystem pool.
- **Eligibility:** Question is included in the experiment contract and has a versioned prerequisite map.
- **Missingness behavior:** Missing, inaccessible, incomplete, or conflicting required evidence leaves the assessment uncovered and retains its typed reason; an undefined prerequisite map makes the measure unavailable.
- **Interpretation:** Coverage of declared evidence prerequisites under a bounded method, not truth, compatibility, adoption, or recovery.
- **Limitation:** Full prerequisite coverage can still yield bounded NO or no positive event; stakeholder relevance of the question may remain unvalidated.

## PROPOSED P6-02 — Paired historical-context availability

- **Numerator:** Eligible members with parsed pre-release and post-release target-dependency observations forming a valid `PAIRED` comparison under the versioned history contract.
- **Denominator:** Eligible declared members in the frozen experiment population.
- **Population:** Named case and history-method version.
- **Eligibility:** Repository is a declared member and the target dependency/path search policy is defined before reconstruction.
- **Missingness behavior:** `AFTER_ONLY`, `BEFORE_ONLY`, `UNRESOLVED`, missing path, parse failure, or inaccessible history does not enter the numerator and retains its state; zero eligible members makes the rate unavailable.
- **Interpretation:** Availability of bounded before/after declaration context.
- **Limitation:** A paired declaration does not prove installation, target-version adoption, runtime compatibility, or causation. Current reference baseline is 1/8 across the two named validation cases, not a target.

## PROPOSED P6-03 — Lifecycle-question sufficiency

- **Numerator:** Member-question assessments classified `SUFFICIENT` under the versioned source/prerequisite contract.
- **Denominator:** All eligible member-question assessments for the same named case and method version.
- **Population:** Frozen case members × predeclared lifecycle questions.
- **Eligibility:** Question and required-source contract are approved for the experiment.
- **Missingness behavior:** Incomplete, unavailable, or conflicting prerequisites remain in the denominator as insufficient only when the contract explicitly defines them; absent question contracts make the measure unavailable.
- **Interpretation:** Share of bounded questions for which the system can issue a contract-valid finding state.
- **Limitation:** Sufficiency is not correctness or usefulness, and does not imply a positive outcome. The current 2/40 component is diagnostic and not an established KPI.

## PROPOSED P6-04 — Bounded decision availability

- **Numerator:** Eligible member-question findings with a supported `YES` or contract-valid `NO_QUALIFYING_EVIDENCE_FOUND` outcome.
- **Denominator:** All eligible member-question findings under the same versioned question/source contract.
- **Population:** One frozen case/method version, reported separately by lifecycle question and finding state.
- **Eligibility:** Required question set and sufficiency contract are defined; finding passed integrity checks.
- **Missingness behavior:** `UNKNOWN` stays in the denominator with its reason when the question is eligible; an undefined required-question set makes the measure unavailable.
- **Interpretation:** Availability of a bounded evidence-backed answer, not ecosystem outcome incidence or business completion.
- **Limitation:** A higher value can reflect more bounded negative findings rather than more observed events; state distribution must accompany the measure.

## PROPOSED P6-05 — Positive support-link completeness

- **Numerator:** Eligible supported positive findings with at least one intact, qualifying evidence path to source artifact, collection context, and review or direct-evidence qualification.
- **Denominator:** All eligible supported positive findings.
- **Population:** Published findings for one named analytical snapshot and rule/method version.
- **Eligibility:** Finding state is a supported positive and its source type is permitted by the question contract.
- **Missingness behavior:** Missing or broken support paths fail integrity and block publication; zero positive findings yields `UNAVAILABLE_ZERO_DENOMINATOR`.
- **Interpretation:** Provenance completeness of positive findings.
- **Limitation:** It measures traceability, not whether the finding is representative or useful. Current population is 0/0 and unavailable.

## PROPOSED P6-06 — Candidate reviewability and provenance completeness

- **Numerator:** Eligible candidate records with stable candidate ID, rule/version, source artifact, supporting span/field, origin classification, emission reason, and terminal review provenance where review is required.
- **Denominator:** All eligible candidates emitted by the versioned method.
- **Population:** One frozen baseline/rule version; shared artifacts and emitting members reported separately.
- **Eligibility:** Candidate belongs to the governed experiment and its rule requires human qualification.
- **Missingness behavior:** Missing identity, source, origin, or required review field fails completeness; zero candidates makes the rate unavailable rather than perfect.
- **Interpretation:** Whether candidates can be audited and reviewed under the declared process.
- **Limitation:** Complete candidates may all be rejected; candidate rows sharing an artifact are not independent incidents.

## PROPOSED P6-07 — Unresolved reason-code distribution

- **Numerator:** Count of eligible `UNKNOWN` member-question assessments assigned to each controlled unresolved reason code.
- **Denominator:** All eligible `UNKNOWN` member-question assessments in the same named case/method version.
- **Population:** Frozen case and question set; distributions remain case/question specific.
- **Eligibility:** Assessment is `UNKNOWN` and the controlled reason taxonomy version is recorded.
- **Missingness behavior:** Missing reason is reported as an explicit data-quality defect, not silently assigned to another category; zero UNKNOWN findings makes the distribution unavailable.
- **Interpretation:** Composition of why bounded questions remain unresolved, used to choose the next evidence-method test.
- **Limitation:** Reason counts do not prove root causes in repository teams or measure business impact.

## PROPOSED P6-08 — Evidence-depth method delta

- **Numerator:** Count of eligible member-question records whose prerequisite coverage, history state, or sufficiency improves under the proposed method without relaxing the outcome contract.
- **Denominator:** All eligible member-question records evaluated under both the baseline and proposed method.
- **Population:** Identical frozen inputs, population, question set, and comparison window; method version is the only intended change.
- **Eligibility:** Record identities reconcile one-to-one and both methods complete integrity checks.
- **Missingness behavior:** Unmatched, failed, or noncomparable records are reported separately and excluded only with a reason; zero comparable records makes the measure unavailable.
- **Interpretation:** Incremental capability attributable to the method change within the experiment.
- **Limitation:** Improvement on the fixed population does not establish transferability, user value, or ecosystem impact. A decrease can be correct if the new method finds an earlier false sufficiency classification.

## Decision use

No single measure determines success. A future gate should review P6-01 through P6-08 with state distributions, source availability, integrity defects, effort, and disconfirming evidence. The acceptable threshold must be prespecified for the experiment or left as an explicit decision, not chosen after seeing results.
