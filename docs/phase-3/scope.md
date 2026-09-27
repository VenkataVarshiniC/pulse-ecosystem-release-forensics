# Phase 3 investigation scope

The analytical unit is an upstream software release and a **declared, bounded set of downstream repositories**, consistent with the Phase 0–2 PULSE boundary. The investigation asks what decision, if any, people make about those repositories and what evidence they need. It does not presume that every lifecycle category occurs or follows a fixed sequence.

## In scope for business analysis

- The release-impact investigation workflow: trigger, decision owner, repository set, evidence threshold, handoffs, and communication.
- Evidence acquisition and review, including source provenance, collection completeness, historical point-in-time state, candidate quality, and human judgment.
- Repository prioritization, evidence sufficiency, useful treatment of UNKNOWN, and report consumption.
- Stakeholder and business-problem discovery; later As-Is/To-Be analysis, requirements, data traceability, and UAT within the planned Phase 3 milestones.

Milestone 1 is limited to hypotheses, context, and a discovery protocol. The later analysis is listed only as phase scope, not performed now.

## Out of scope for now

- Ecosystem-wide monitoring or prevalence claims from the frozen cohort.
- Vulnerability management unless genuine discovery establishes a direct connection to this release-impact decision.
- Generic dependency updating, code remediation automation, or automatic causal attribution.
- Production deployment, a final analytics dashboard, Phase 4 analytics, and product architecture expansion.
- Treating current declarations as historical adoption, or absence of qualifying collected evidence as absence of real-world events.

If discovery finds that the useful decision requires a different population, inaccessible data, or an unrelated workflow, document the scope change and revisit the product hypothesis before drafting requirements.
