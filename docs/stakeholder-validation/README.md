# PULSE stakeholder-validation waves

Stakeholder evidence is additive and versioned. Raw survey exports remain local and ignored; committed artifacts contain only digests, anonymized response IDs, coded evidence, and aggregate analysis.

| Evidence stage | Population | Status | Boundary |
| --- | ---: | --- | --- |
| Wave 1 | n = 9 | Complete; frozen baseline wave | Findings remain unchanged except for a documented analytical correction. |
| Wave 2 | cumulative n = 14; new n = 5 | Complete; frozen additive interim wave | Uses R10–R14 and cumulative comparison without rewriting Wave 1. |
| Task-based validation | Target 1–3 participants | `PREPARED_NOT_EXECUTED` | Study materials only; no participant results or success rates. |
| Wave 3 | Future | Not started | Requires a separately frozen export and additive analysis. |

**G8 remains `PARTIALLY_VALIDATED`.** Preparing or running a pilot does not change the gate automatically. **Phase 8 remains `NOT_STARTED`.**

The [bounded task-pilot package](task-pilot/README.md) separates participant materials, moderator-only ground truth, observation coding, decision-effect recording, privacy controls, gate criteria, and the later analysis plan.

When another survey wave arrives:

1. Freeze the new cumulative raw export and record its digest and response count.
2. Verify that previously frozen substantive rows match and identify only newly added respondents.
3. Assign new stable anonymized IDs and create a separate wave dataset and analysis.
4. Compare prior waves with the additions and cumulative result without editing earlier conclusions.
5. Rerun cumulative hypothesis, persona, requirements, strategy, counter-evidence, and value reconciliation.
6. Reassess G8 under the same governance definitions.

A frozen wave may be corrected only for a documented analytical error. New evidence produces a new wave result rather than a retrospective rewrite.
