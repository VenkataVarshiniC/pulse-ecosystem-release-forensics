# Phase 6 decision context

## Decision to make

PULSE must decide where to invest next to improve evidence-backed decision usefulness while preserving bounded, auditable release-forensics semantics. The decision is not how to scale PULSE fastest. The current record does not establish that system throughput, cohort size, or interface breadth is the primary constraint.

The governing question is:

> Where should PULSE invest next to improve evidence-backed decision usefulness while preserving bounded, auditable release-forensics semantics?

Phase 6 answers that question from the existing repository record. It does not authorize implementation, collect new external evidence, change frozen inputs, modify published validation data, or complete stakeholder validation.

## Why the decision exists

The system has progressed beyond a collection prototype. Bounded authenticated collection, immutable provenance, exact-ref observations, candidate/review separation, deterministic replay, PostgreSQL and dbt analytical models, governed metrics, FastAPI and React investigation paths, and Power BI reporting have all been implemented and technically validated. The [Phase 5 integration record](../phase-5/milestone-5-4-findings.md) and [M4.2 closure](../phase-4/m4-2/power-bi-dashboard-validation.md) show that PULSE can carry the two published validation investigations through governed storage and decision interfaces without losing scope or uncertainty semantics.

That technical capability has not produced broad answerability. Across the bounded published validation population, core collection completed for all 8 declared members, while 38 of 40 lifecycle findings remain `UNKNOWN`, 2 are bounded `NO_QUALIFYING_EVIDENCE_FOUND`, and none is a supported positive finding. Only 1 of 8 members has paired pre-release historical context. The two detector candidates are inherited `REJECT` decisions from one copied-upstream artifact. Observed adoption and recovery remain unavailable. These facts come from the [Phase 2 findings](../phase-2/phase-2-findings.md), [governed M2.5 results](../phase-4/m2-implementation/m2-5-metric-results.md), [M4.1B release](../phase-4/milestone-4-1b-findings.md), and [Power BI reconciliation](../phase-4/m4-2/power-bi-measure-reconciliation.md).

The decision therefore concerns the gap between reliable collection/governance and qualifying evidence sufficiency. It does not assume that every `UNKNOWN` can be resolved from public sources.

## Governed evidence baseline

These values describe only the two published validation investigations. They are not an ecosystem sample or population estimate.

| Baseline fact | Governed value | Interpretation boundary |
| --- | ---: | --- |
| Published validation investigations | 2 | pytest 8.0.0 and urllib3 2.0.0 only. |
| Declared repository members | 8 | pytest 2; urllib3 6. |
| Core-collected members | 8/8 | Planned core-source completion, not analytical sufficiency. |
| Lifecycle findings | 40 | Five evidence categories per declared member. |
| `UNKNOWN` findings | 38 | Missing or insufficient qualifying evidence, not NO. |
| Bounded NO findings | 2 | Both limited to the declared sufficient method; not proof of real-world absence. |
| Supported positive findings | 0 | No positive support chain exists in the governed population. |
| Detector candidates | 2 | Two rule emissions, not two incidents. |
| Candidate dispositions | 2 inherited `REJECT` | Provenance records, not new reviewer actions or proof of absent friction. |
| Distinct candidate artifacts | 1 | One shared copied-upstream artifact. |
| Historical context | 1 `PAIRED`; 6 `AFTER_ONLY`; 9 `UNRESOLVED` | Context records, not 16 independent members; after-only is not a release-boundary pair. |
| Power BI validation | PASS at `92e0e7e5c87284d49a79a6a481e978637026fa8f` | Technical Desktop validation; no stakeholder approval. |

Collection reliability is materially stronger than analytical evidence sufficiency in this bounded record. That statement is a comparison of validated system capabilities, not a quantified business conclusion.

## Current technical capability

Within the two published cases, PULSE can:

- preserve a declared release, cohort, window, case version, and analytical snapshot;
- execute bounded public-source collection with typed task outcomes and verified resume;
- retain source, capture method, retrieval context, digest, task/run identity, and exact-ref observations;
- separate declarations, historical context, candidates, reviews, sufficiency assessments, and findings;
- prevent rejected candidates and missing evidence from becoming accepted findings;
- reproduce governed metrics and findings through PostgreSQL/dbt publication;
- expose exact case/snapshot scope through API, React, and Power BI;
- communicate `UNKNOWN`, bounded `NO`, zero denominators, copied-upstream origin, and missing support links without inventing an answer.

These are bounded technical capabilities, not evidence of production scalability, market demand, or stakeholder utility.

## Current analytical limitation

Collection completeness and analytical sufficiency answer different questions:

- **Collection completeness** asks whether the tasks required by the declared plan completed under the plan's source policy.
- **Analytical sufficiency** asks whether the collected evidence satisfies the prerequisites for a particular lifecycle question and finding state.

The current population has 8/8 core collection but only 2/40 sufficient member-question assessments. Successful completion of metadata, issue, pull-request, and commit tasks does not supply missing release-boundary history, qualified resolved-version evidence, a recovery-eligible denominator, or accepted local lifecycle evidence. The [Phase 3 root-cause analysis](../phase-3/root-cause-analysis.md) identifies those source and method limits; it does not claim organizational causation.

## Stakeholder-validation dependency

`G8 = NOT_YET_VALIDATED`.

No repository evidence establishes a validated primary user, decision owner, workflow value, tolerable review burden, required question set, source threshold, completion definition, demand, or return on investment. The [Phase 3 closure](../phase-3/phase-3-closure-assessment.md) and [stakeholder reconciliation framework](../phase-3/stakeholder-reconciliation-framework.md) remain authoritative. Phase 6 may recommend technical and analytical priorities supported by the observed system gaps. Any claim about usefulness, priority for a real organization, reviewer authority, or acceptable evidence source remains stakeholder-dependent.

Stakeholder validation is outside Phase 6 completion criteria. Its absence constrains the recommendation; it does not prevent an auditable recommendation about the next evidence-method investment.

## Recommendation boundary

Inside the boundary:

- prioritize among evidence depth, cohort breadth, investigator workflow, and a gated sequence;
- identify the evidence-method capabilities most directly connected to current `UNKNOWN` results;
- define acceptance gates and proposed capability measures;
- preserve provenance, frozen evidence, governed publication, and bounded finding semantics;
- identify stakeholder-dependent decisions without resolving them by assumption.

Outside the boundary:

- a new collector, source integration, historical-lineage implementation, detector retuning, major subsystem, or production deployment;
- new external collection or modification of frozen/published data;
- stakeholder UAT, persona validation, market sizing, ROI, demand, or value claims;
- ecosystem inference from the 2-case, 8-member population;
- adoption, compatibility, causal migration, or recovery claims unsupported by qualifying evidence;
- final portfolio and recruiting materials.

## Evidence sufficient for this recommendation

The recommendation can be made because the repository contains:

1. two outcome-blind frozen validation cases with explicit population limits;
2. live collection and deterministic replay evidence;
3. stable governed counts through PostgreSQL, dbt, API, React, and Power BI;
4. explicit requirement, metric, sufficiency, provenance, and missingness contracts;
5. observed gaps in historical context, target-version evidence, recovery eligibility, and finding-support linkage;
6. a separate public PR study that illustrates source fragmentation and copied upstream text without being mixed into the governed validation cohort;
7. documented technical acceptance limits and stakeholder gates.

This evidence is sufficient to choose the next bounded analytical priority. It is not sufficient to predict how much sufficiency will improve, whether additional approved sources are accessible, or whether a stakeholder will value the resulting workflow.

## What remains unknown

- Whether the intended decision exists frequently enough to justify continued product investment.
- Which lifecycle questions are required by an actual decision owner.
- Which public or authorized nonpublic sources are acceptable and obtainable.
- Whether deeper history can materially increase qualifying paired context in a prespecified test.
- Whether qualified resolved-version or recovery evidence can be acquired at useful coverage.
- Whether current `UNKNOWN` explanations guide action.
- Who may review candidates and what review burden is acceptable.
- Whether a broader cohort would improve learning after evidence-method gates pass.
- Whether existing tools and a competent investigator already solve the relevant decision adequately.

No absence above is converted into a negative conclusion.
