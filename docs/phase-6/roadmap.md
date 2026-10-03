# Phase 6 recommendation roadmap

## Roadmap rule

This roadmap sequences decisions rather than promising features. Each horizon begins only when its prerequisites and acceptance gate are satisfied. A failed evidence gate may produce a HOLD, PIVOT, or STOP decision; it must not trigger automatic scope expansion.

## NOW — validate evidence depth

### N1. Freeze an evidence-depth experiment contract

- **Objective:** Define the exact lifecycle question, fixed population, permitted source classes, historical horizon, pairing semantics, and comparison method before implementation or collection.
- **Problem addressed:** Current source/question eligibility is incomplete, making it difficult to distinguish acquisition failure from qualification failure.
- **Evidence dependency:** Phase 2 cases, Phase 3 FR-004/FR-006/FR-009, M2.5 metric contracts, and current source-policy rules.
- **Expected analytical capability:** A reproducible comparison between the current method and one bounded evidence-depth method.
- **Acceptance criteria:** Case and population are frozen; required/optional sources and source policy are explicit; `PAIRED`, `AFTER_ONLY`, `UNRESOLVED`, `UNKNOWN`, bounded NO, and positive-support rules are predeclared; no current/present declaration can stand in for historical use.
- **Prerequisite:** Named technical owner and approval that the experiment does not alter published snapshots.
- **Risk:** Designing eligibility around known case outcomes.
- **Explicit non-goal:** Proving ecosystem coverage or stakeholder value.

### N2. Specify historical reconstruction improvements

- **Objective:** Design a bounded test of older-anchor discovery and cross-file manifest transitions for the fixed experiment population.
- **Problem addressed:** Only 1/8 current members has paired pre-release context; path-changing commits inside the window can miss older unchanged declarations.
- **Evidence dependency:** Existing exact-ref observations and unresolved reasons.
- **Expected analytical capability:** More precise classification of whether a pre-release and post-release dependency state can be compared.
- **Acceptance criteria:** Every attempted member/path produces a typed state and reason; refs, paths, parser version, and clocks are retained; after-only evidence never counts as paired; missing anchors remain unresolved.
- **Prerequisite:** N1 contract and source-access feasibility.
- **Risk:** Repository layouts and rewritten/deleted paths may remain unresolved.
- **Explicit non-goal:** Inferring installed target versions or compatibility from declarations.

### N3. Define source-availability and prerequisite reason taxonomy

- **Objective:** Replace generic insufficiency with controlled question-specific prerequisite and availability reasons.
- **Problem addressed:** `unknown_insufficient_data` cannot identify which approved input is absent or inaccessible.
- **Evidence dependency:** Existing task outcomes, assessment model, and Phase 3 FR-002/FR-006/NFR-004.
- **Expected analytical capability:** Explain whether a question is blocked by not-planned, not-found, inaccessible, incomplete, conflicting, ineligible, or unavailable evidence.
- **Acceptance criteria:** Reasons are mutually interpretable, source/question linked, versioned, and mapped to `UNKNOWN` without creating bounded NO; optional-not-found remains distinct from required-source failure.
- **Prerequisite:** N1 question/source map.
- **Risk:** Excessive taxonomy detail may become difficult to apply consistently.
- **Explicit non-goal:** Assigning blame or a causal reason for why evidence is absent.

### N4. Define side-by-side replay and stop gates

- **Objective:** Compare the existing method with the proposed evidence-depth method while preserving old results.
- **Problem addressed:** A method change could silently rewrite published conclusions or be judged by anecdote.
- **Evidence dependency:** M4.1B immutable publication, rule/version lineage, and reproducibility checks.
- **Expected analytical capability:** Attribute changes in history state, sufficiency, findings, and unresolved reasons to a versioned method.
- **Acceptance criteria:** Frozen inputs remain unchanged; new outputs receive distinct version/snapshot identity; changes are reconciled at member-question grain; no published row is overwritten; progression and stop conditions are reported even if sufficiency does not improve.
- **Prerequisite:** N1–N3 specifications.
- **Risk:** A result may appear improved because eligibility was relaxed.
- **Explicit non-goal:** Maximizing positive or negative finding counts.

## NEXT — qualify sources and linkage only after the NOW gate

### X1. Run one authorized evidence-source trial

- **Objective:** Test one source type tied to a predeclared unresolved prerequisite.
- **Problem addressed:** Some lifecycle questions lack qualified resolved-version or recovery inputs.
- **Evidence dependency:** A passed N1–N4 design gate and explicit source authorization.
- **Expected analytical capability:** Determine whether that source can provide eligible evidence, not whether the outcome is favorable.
- **Acceptance criteria:** Access policy, capture method, grain, event/retrieval clocks, provenance, eligibility, missingness, and stop condition are defined; results remain bounded to the trial.
- **Prerequisite:** Source owner/policy approval; stakeholder input if the source threshold reflects an organizational decision.
- **Risk:** The source may be inaccessible, noncomparable, or too sparse.
- **Explicit non-goal:** Broad source harvesting or private-data collection by default.

### X2. Validate positive support-link integrity when eligible evidence exists

- **Objective:** Demonstrate finding-to-evidence traceability for a genuine source-backed positive case or an explicitly governed validation fixture.
- **Problem addressed:** Current published findings have zero support-bridge rows and no positive finding.
- **Evidence dependency:** A qualifying positive event; fixtures may test mechanics but cannot establish real-world coverage.
- **Expected analytical capability:** Audit a YES finding through review/candidate or qualified direct evidence to source artifact and collection context.
- **Acceptance criteria:** Every YES has at least one intact qualifying support path; broken or absent paths block publication; fixture and real evidence remain distinguishable.
- **Prerequisite:** An eligible case or approved fixture contract.
- **Risk:** Fixture success could be misrepresented as live validation.
- **Explicit non-goal:** Manufacturing a positive outcome.

### X3. Reconcile with stakeholders when authorized

- **Objective:** Test the decision question, required evidence, usefulness of UNKNOWN, reviewer authority, and acceptable burden.
- **Problem addressed:** G8 remains open.
- **Evidence dependency:** Genuine responses from relevant decision participants using the existing reconciliation framework.
- **Expected analytical capability:** Distinguish technical sufficiency from workflow usefulness and revise priorities where evidence warrants.
- **Acceptance criteria:** Response provenance, role/authority, disconfirming evidence, unresolved disagreement, and requirement impacts are recorded; silence is not rejection or approval.
- **Prerequisite:** Authorized participants and data-handling plan.
- **Risk:** Participants may reject the need or require inaccessible evidence.
- **Explicit non-goal:** Seeking endorsement for a preselected product direction.

## LATER — conditional workflow and breadth

### L1. Refine investigator/review workflow

- **Objective:** Improve evidence-gap explanation, triage, or review only for an observed user task.
- **Problem addressed:** Current technical workflow may not match actual decision or review practice.
- **Evidence dependency:** X3 validates a user, task, and acceptance criterion; a legitimate DRAFT case and reviewer authority exist for write behavior.
- **Expected analytical capability:** More reliable human qualification without weakening immutable published data.
- **Acceptance criteria:** Task completion and comprehension are observed; review authority and audit fields are enforced; no attention score is labeled organizational risk.
- **Prerequisite:** G8 evidence relevant to the change.
- **Risk:** Interface changes may optimize an unrepresentative workflow.
- **Explicit non-goal:** Generic case management or collaboration SaaS.

### L2. Expand cohorts selectively

- **Objective:** Test transferability of the validated evidence method on a prespecified additional release/cohort.
- **Problem addressed:** Current results are limited to two convenience validation investigations.
- **Evidence dependency:** NOW/NEXT demonstrate a stable method and clear question; selection remains outcome-blind.
- **Expected analytical capability:** Evaluate method transfer without treating the new cohort as an ecosystem sample.
- **Acceptance criteria:** Inclusion/exclusion frame is frozen before forensics; no pooled incidence claim; method and population changes are separable; resource/review limits are explicit.
- **Prerequisite:** Evidence-depth gate passes or produces a deliberate revised method.
- **Risk:** Selection bias and sparse evidence persist.
- **Explicit non-goal:** Increasing N for a résumé metric or population claim.

### L3. Reassess product and production investment

- **Objective:** Decide whether to continue, narrow, pivot, hold, or stop after evidence and stakeholder gates.
- **Problem addressed:** Technical completeness does not establish value or production need.
- **Evidence dependency:** Results from N1–N4, any X1/X2 evidence, X3 stakeholder reconciliation, and L2 transfer test if authorized.
- **Expected analytical capability:** An evidence-backed investment decision with explicit residual uncertainty.
- **Acceptance criteria:** Alternatives include current tools/do-nothing; benefits are observed rather than invented; security, operations, and scale requirements are separately authorized.
- **Prerequisite:** Decision owner.
- **Risk:** Sunk-cost bias favors continued building.
- **Explicit non-goal:** Automatic cloud deployment or productionization.

## Progression gates

1. **NOW → NEXT:** The experiment contract is prespecified, source policy is valid, replay comparison is reproducible, and the result either improves a defined capability measure or establishes a documented infeasibility that justifies a new decision.
2. **NEXT → LATER workflow:** A real task, user, reviewer authority, and acceptance criterion are validated.
3. **NEXT → LATER breadth:** The evidence method is stable enough to test transfer and the added cohort answers a declared learning question.
4. **Stop/reconsider:** Required evidence is inaccessible, method changes do not improve bounded answerability, current tools are sufficient, or no stakeholder-owned decision is found.

No horizon has a date because the repository contains no legitimate delivery-time requirement.
