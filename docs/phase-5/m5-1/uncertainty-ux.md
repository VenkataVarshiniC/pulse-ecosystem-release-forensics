# Honest uncertainty and missing-evidence UX

Use neutral, accessible text plus an icon; color alone must not carry meaning. **Missing evidence must never visually become negative evidence.** Collection outcome, review decision, sufficiency, finding and metric availability are separate axes. The published replay contains 38 UNKNOWN, two bounded NO, zero positive findings, two inherited REJECT candidates, and no qualified adoption/recovery outcome. These are bounded case results, not population claims.

| State / technical source | User-facing label and explanation | Supported next action; forbidden reading |
|---|---|---|
| `core.lifecycle_finding.finding_status = UNKNOWN` | **Unanswered — evidence insufficient for this category.** Show `reason_code`, category, source sufficiency, and recorded missing prerequisite. | Inspect finding, source coverage, exact-ref history. Never blank, “no issue,” zero adoption/recovery or bounded NO. |
| `core.sufficiency_assessment.sufficiency_status = INSUFFICIENT` | **Required evidence incomplete.** Name a source only when recorded. | Inspect task/historical context. Never turn into negative finding or assume SOURCE_UNAVAILABLE. |
| `SOURCE_UNAVAILABLE` | **Required source unavailable.** Show actual selected source/task failure or not-collected reason. | Inspect provenance; a later retry needs a new run, not mutation of published evidence. Do not equate optional not-found with required failure. |
| `CONFLICTING` | **Evidence conflicts; no bounded conclusion.** Show both recorded claims, refs and clocks if a future assessment uses this state. | Human qualification; current replay has no demonstrated CONFLICTING finding. |
| `NO_QUALIFYING_EVIDENCE_FOUND` plus `SUFFICIENT` | **No qualifying evidence found under this bounded method.** Show stage, source set, window and reason. | Inspect method; never assert universal absence. |
| `QUALIFYING_EVIDENCE` | **Qualifying evidence recorded.** Show accepted review and support chain. | Follow provenance; current replay has zero positive findings. |
| No selected candidate row | **No candidate emitted in this selected snapshot.** | Inspect completeness and finding separately; not “no friction” or REJECT. |
| Review `REJECT` | **Candidate rejected by review**, or **Inherited REJECT from prior review** when `review_origin = INHERITED`. | Inspect original review/artifact; current published record is read-only. No real-world absence inferred. |
| `NEEDS_EVIDENCE` / no selected review | **Review unresolved** / **Not reviewed**, separately. | Inspect artifact; submit a reason only for authorized DRAFT target. Never auto-accept. |
| READY numerator `0`, denominator `N>0` | **0 of N eligible observations**, with exact question and case. | Valid numeric zero on that question only: zero emissions ≠ zero friction. |
| `0/0`, `UNAVAILABLE_ZERO_DENOMINATOR` | **Unavailable — no eligible observations (0/0).** | Inspect eligibility; never render 0%. |
| `UNAVAILABLE_EVIDENCE`, `PARTIAL_*`, `BLOCKED_STAKEHOLDER` | **Unavailable** or **Partial diagnostic only**, with governed `unavailable_reason`. | Follow stated dependency; do not compute a full rate from partial components. |
| Missing pair / `AFTER_ONLY` | **Release-time history unresolved; after-only observation retained.** | Inspect exact ref/path; never infer pre-release absence or installation. |

Collection statuses (success, failed required, optional not-found, not-collected, partial) remain visible with the required flag. A source can be collected while a question remains insufficient. Event and retrieval times have separate labels; unknown event time belongs in an “event time unavailable” group, not an invented timeline position. Lifecycle categories are evidence classes, not a forced chronology. Drill paths retain case, repository, snapshot, rule version and provenance without exposing secrets.

Future UI acceptance checks: failed required source plus no accepted event → UNKNOWN with reason (AC-BR-002-01); after-only context cannot support a negative (AC-FR-004-01); zero candidates and incomplete context → UNKNOWN (AC-FR-009-01); optional 404 differs from required failure (AC-FR-002-01); declaration differs from target-version installation (AC-FR-005-01); 0/0 acceptance is unavailable while valid 0/2 may show 0%. These are specifications, **not executed user tests**.
