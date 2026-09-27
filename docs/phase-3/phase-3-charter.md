# Phase 3 charter

## Background

Phase 0 pivoted from ecosystem-wide inference to a curated, repository-bounded investigation because public evidence was uneven. Phase 1 produced a reproducible forensic engine, while its HTTPX validation snapshots were connector-assisted and did not prove unattended collection. Phase 2 validated bounded live collection and report reproduction, but historical target-package declaration evidence was established for only 2 of 8 frozen repositories. It could not establish installed target versions or ordinary runtime/CI resolution, collected no downstream releases for recovery, and produced two rejected candidates from one Dependabot PR with no accepted lifecycle events. Its final decision was **PIVOT**, preserving the architecture while reconsidering the evidence and evaluation method. These are technical findings, not proof of stakeholder need. See [Phase 2 findings](../phase-2/phase-2-findings.md).

## Business-analysis objective

Determine whether a real stakeholder has a recurring, consequential release-impact investigation decision that PULSE can improve within its evidence limits. Describe that stakeholder's current workflow, evidence threshold, review tolerance, and desired outcome before specifying the next version. A trustworthy report full of UNKNOWN findings may still be insufficient for the decision.

## Business question

What stakeholder decision should PULSE support, what current workflow creates the problem, and what business and system requirements must the next version satisfy to improve that workflow while maintaining trustworthy evidence boundaries?

## Scope

This phase includes stakeholder identification and discovery; decision and workflow analysis; a testable business-problem definition; assumptions, constraints, and risks; later As-Is and To-Be analysis; later requirements, data traceability, and UAT. Milestone 1 performs only the context and discovery-foundation work. [Scope](scope.md) defines the investigation boundary.

This phase excludes a SQL analytics warehouse, BigQuery/dbt, Power BI, a React product UI, major FastAPI expansion, LLMs/RAG, embeddings, ML ranking, production cloud work, Phase 4 analytics, and arbitrary detector tuning. It does not broaden PULSE to ecosystem-wide monitoring or claim causal attribution.

## Phase 3 success criteria

By the end of the phase, a reviewer should be able to trace the selected stakeholder, decision, observed workflow problem, and each proposed requirement back to genuine discovery or identified project evidence. The specification should state what evidence is sufficient for each decision, where uncertainty remains, what human review is required, and how acceptance will be evaluated. Stakeholders should be able to assess the proposed workflow and acceptance scenarios against their actual practice. Any unmet evidence prerequisite or disconfirming discovery result must remain visible. Quantitative improvement targets require a measured baseline and stakeholder agreement; none are asserted here.

## Milestone 1 gate

This milestone passes only if the historical findings are accurately carried into testable questions, every stakeholder and need is marked provisional, the discovery protocol is usable, and no interview, process validation, or formal requirement is invented.
