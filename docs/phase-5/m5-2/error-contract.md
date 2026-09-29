# API error and unavailable-state contract

Errors are JSON objects `{ "code": "...", "message": "..." }`, never empty result sets. Messages contain no SQL, credentials or internal paths. Invalid UUIDs/body fields use HTTP 422 `INVALID_REQUEST`; connection/configuration failures use HTTP 503 `DATABASE_UNAVAILABLE`. Network failure is a separate frontend state.

| Code | HTTP | Meaning / frontend action |
|---|---:|---|
| `INVALID_SNAPSHOT` | 404 or 409 on ineligible write state | Wrong-case, legacy DRAFT or otherwise unapproved selection; return to published list. |
| `NOT_FOUND_IN_SELECTED_COHORT` | 404 | Member/candidate/finding absent from exact scope; retain scope, do not show zero. |
| `PROVENANCE_MISMATCH` | 404/409 | Artifact outside selected scope or finding support that does not resolve within it. |
| `PUBLISHED_IMMUTABLE` | 409 | Review requested against a published candidate; keep read-only. |
| `REVIEWER_NOT_AUTHORIZED` | 403 | No trusted human authority plus eligible isolated DRAFT policy; no write attempted. |
| `INVALID_DECISION_REASON` | 422 | Blank reason in a typed review request. |
| `STALE_REVIEW` | 409 | Expected review ID differs or terminal review exists; reload. |
| `IDEMPOTENCY_CONFLICT` | 409 | Retry key reused with different payload or identity. |
| `DATABASE_UNAVAILABLE` | 503 | Local PostgreSQL/configuration error; retry later. |
| `DATABASE_ERROR` | 500 | Database operation failed; do not infer an empty investigation. |

`SOURCE_UNAVAILABLE` is a **governed sufficiency/source state**, not an HTTP error when collection failed. A successful read can return `UNKNOWN` finding plus `SOURCE_UNAVAILABLE` sufficiency. HTTP 404/503 never implies `NO_QUALIFYING_EVIDENCE_FOUND`. Only a selected finding with a sufficient bounded method may carry that negative status. Current replay has 38 UNKNOWN, two bounded NO and zero positive findings.
