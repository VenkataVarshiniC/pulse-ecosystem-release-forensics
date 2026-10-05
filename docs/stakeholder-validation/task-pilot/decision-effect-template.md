# Observed decision-effect template

Create one local working copy per real participant and commit only a privacy-reviewed anonymized result later.

| Field | Record |
| --- | --- |
| Participant ID | `T__` |
| Case and snapshot | |
| Initial intended action, before PULSE | |
| Evidence initially requested | |
| Post-task intended action | |
| Decision effect | `CHANGED` / `CLARIFIED` / `UNCHANGED` / `NOT_OBSERVED` |
| Participant’s reason | |
| PULSE evidence explicitly referenced | |
| Evidence ignored or distrusted | |
| Participant confidence, in their own terms | |
| Moderator interpretation | |
| Direct statement versus analyst inference | |
| Prompt or system limitation affecting observation | |

## Classification rules

- `CHANGED` — The participant explicitly states that the action they would take differs materially after reviewing PULSE. Record both actions and the evidence causing the change.
- `CLARIFIED` — The intended action remains materially the same, but the participant explicitly reports a clearer rationale, scope, sequence, evidence request, or owner.
- `UNCHANGED` — The participant reports the same action and no material clarification attributable to PULSE.
- `NOT_OBSERVED` — Initial action, post-task action, or a fair task opportunity is missing.

A clearer explanation is not `CHANGED` unless the participant says the action changed. Moderator inference cannot upgrade `UNCHANGED` or `CLARIFIED` to `CHANGED`. Negative or unchanged effects are retained as counter-evidence.
