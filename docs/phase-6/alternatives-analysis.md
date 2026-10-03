# Phase 6 strategic alternatives analysis

## Evaluation method

Alternatives are compared qualitatively. No weights or synthetic totals are used because stakeholder priorities, source access, and acceptable effort are not validated. Ratings mean:

- **Strong advantage** — directly addresses an observed gap with existing architectural support.
- **Moderate advantage** — likely helps a documented gap but has a material dependency or limit.
- **Neutral/mixed** — benefit and disadvantage are both material.
- **Moderate disadvantage** — weak fit or meaningful risk under current evidence.
- **Strong disadvantage** — conflicts with the observed constraint or creates a high integrity risk.
- **Unknown / stakeholder-dependent** — cannot be resolved from repository evidence.

## Alternatives

### Option A — Evidence depth first

Strengthen qualifying evidence acquisition and historical reconstruction for the existing bounded investigation model. The supported scope includes prespecified historical manifest reconstruction, explicit source-availability classification, question-specific prerequisite maps and reason codes, stronger finding-support linkage, and a bounded test of approved evidence sources. It does not assume that every missing source should be added.

### Option B — Cohort breadth first

Increase releases and repositories while retaining the current evidence method. This could test operational throughput and surface more examples, but it uses a method that currently yields 38/40 `UNKNOWN` findings and only 1/8 paired pre-release members. Larger N does not by itself create eligible evidence.

### Option C — Investigator workflow first

Prioritize triage, review, qualification, provenance navigation, evidence-gap explanation, and review productivity. PULSE already has a technically validated read workflow and strong uncertainty communication. Reviewer authority, workflow value, and acceptable burden remain unvalidated; only two dependent rejected firings exist.

### Option D — Sequenced, gated approach

Authorize evidence-depth validation first; require a measured sufficiency improvement or a documented infeasibility result; then test bounded workflow refinements with stakeholders or authorized reviewers; expand cohorts selectively only after the evidence method and decision question pass their gates. This is a sequence, not parallel feature expansion.

## Tradeoff matrix

| Criterion | A — Evidence depth | B — Cohort breadth | C — Workflow first | D — Sequenced/gated |
| --- | --- | --- | --- | --- |
| Improvement in evidence sufficiency | **Strong advantage** — targets paired history, prerequisites, sources, and support linkage. | **Strong disadvantage** — repeats the current method across more members. | **Moderate disadvantage** — can explain gaps but does not supply missing inputs. | **Strong advantage** — A is the first gate; later work depends on demonstrated improvement. |
| Decision usefulness | **Moderate advantage** — more bounded answers may be possible, but usefulness remains unvalidated. | **Moderate disadvantage** — more UNKNOWN may add volume without answers. | **Unknown / stakeholder-dependent** — workflow value requires users. | **Moderate advantage** — links technical improvement to later stakeholder and breadth gates. |
| Preservation of provenance | **Strong advantage** — existing lineage can govern new observations and links. | **Moderate advantage** — current architecture preserves scope, but volume adds audit burden. | **Strong advantage** — provenance navigation is already central. | **Strong advantage** — provenance is a gate throughout the sequence. |
| Analytical validity | **Strong advantage** — keeps question/source eligibility explicit. | **Strong disadvantage** — creates temptation to interpret counts as prevalence. | **Moderate advantage** — can preserve uncertainty if no prioritization score is invented. | **Strong advantage** — prevents progression when validity gates fail. |
| Implementation effort | **Neutral/mixed** — focused experiments can be bounded, but source/history methods may be difficult. | **Moderate disadvantage** — collection/storage/review volume grows without fixing the method. | **Neutral/mixed** — UI exists, but write/review policy is unresolved. | **Moderate disadvantage** — requires disciplined gates and more than one decision point. |
| Technical risk | **Neutral/mixed** — historical/source acquisition can expose edge cases; core architecture is reusable. | **Moderate disadvantage** — operational surface expands before need is shown. | **Moderate advantage** for read refinements; write flow remains risky. | **Moderate advantage** — isolates experiments and stops failed paths. |
| Governance risk | **Moderate advantage** — explicit source policy and sufficiency rules can improve control. | **Strong disadvantage** — higher risk of pooled or generalized claims. | **Neutral/mixed** — guardrails exist, but reviewer authority is absent. | **Strong advantage** — publication and stakeholder gates stay explicit. |
| Reproducibility | **Strong advantage** — prespecified inputs and side-by-side replay fit current architecture. | **Moderate advantage** technically, with higher artifact volume. | **Moderate advantage** for read-only behavior; review actions need governed identity. | **Strong advantage** — each step requires frozen comparison evidence. |
| Compatibility with architecture | **Strong advantage** — uses existing cases, observations, sufficiency, lineage, and replay. | **Moderate advantage** — collectors and storage can accept more cases, but scale is unproven. | **Moderate advantage** — API/UI paths exist; new write behavior is gated. | **Strong advantage** — reuses all existing layers without authorizing a new subsystem. |
| Incremental validation | **Strong advantage** — a prespecified bounded history/source experiment is possible. | **Moderate disadvantage** — larger cohorts confound method and population changes. | **Moderate advantage** for small usability tests; current stakeholders absent. | **Strong advantage** — incremental evidence, workflow, and breadth gates are explicit. |
| Dependency on stakeholder input | **Moderate advantage** for history-method testing; source relevance still needs approval. | **Unknown / stakeholder-dependent** — cohort meaning and owner are unvalidated. | **Strong disadvantage** — reviewer and workflow questions are central. | **Neutral/mixed** — first gate can proceed analytically; later gates wait for stakeholders. |
| Portfolio/demonstrability value | **Moderate advantage** — demonstrates disciplined hypothesis testing and honest failure. | **Moderate advantage** visually, but larger counts could mislead. | **Moderate advantage** if a real workflow is validated; otherwise cosmetic. | **Strong advantage** — demonstrates evidence-based sequencing and governance without feature inflation. |

## Alternative decision

**Select Option D, with Option A as the only authorized near-term investment.**

Option D earns selection because sequencing is necessary to prevent the unresolved dependencies in A, C, and B from being treated as simultaneous build commitments. Its first gate is not a compromise: it is the evidence-depth experiment directly supported by the observed primary gap. Workflow work waits for reviewer/decision evidence. Cohort expansion waits for a method that improves answerability or produces a documented stop decision.

## Why the other alternatives are not first priority

- **A alone** correctly identifies the immediate priority, but without explicit stop and progression gates it could become open-ended source accumulation. It is retained as the first horizon inside D.
- **B** risks scaling UNKNOWN, review volume, and nonrepresentative counts. It is deferred until evidence-depth performance can be evaluated on a prespecified population.
- **C** would optimize a technically working interface around an unvalidated user, review authority, and workload. Limited evidence-explanation changes may accompany a later validated test, but workflow expansion is not first.

The current status quo and existing tools remain a valid fallback. If deeper evidence is inaccessible or stakeholders later find no useful decision, the sequence should stop rather than manufacture a product rationale.
