# Versioned endpoint and response contract

Base path: `/api/v1`. Path IDs are UUIDs. `{case_version_id}` identifies a frozen case version, and every detail/read request requires exact `snapshot_id` as a query parameter. Approved snapshots are pytest `08852d5f-9843-5406-a69b-7039ea2ddaa4` and urllib3 `bd3a02a5-0c2d-5eec-84fd-8e9b93a238a3`. List mode shows only these `PUBLISHED_VALIDATION` snapshots; it never chooses a latest DRAFT.

| Method and path suffix | Response schema | Behavior |
|---|---|---|
| `GET /health` | status, `api_version`, `database_reachable` | Reachability, no secrets. |
| `GET /investigations` | `InvestigationList` | Case/release/window, declared count and versioned scope; no risk score. |
| `GET /investigations/{case_version_id}` | `InvestigationDetail` | All declared members and literal selected candidate/finding counts. |
| `GET .../repositories/{repository_id}` | `RepositoryDetail` | Identity, source states, observations, pairs, findings and candidate count. |
| `GET .../repositories/{repository_id}/evidence` | `EvidencePage` | Selected captures and observations; optional exact `source_type`, `ref`, `path`, `cursor`, `limit`. |
| `GET .../repositories/{repository_id}/artifacts/{artifact_id}` | `Provenance` | Selected capture, allowed public locator, method, digest, clocks, task/run and links. |
| `GET .../repositories/{repository_id}/findings` | `FindingsResponse` | Literal finding, assessment, source reasons and recorded support IDs. |
| `GET .../repositories/{repository_id}/findings/{finding_id}` | `Finding` | One scoped finding. |
| `GET .../repositories/{repository_id}/candidates` | `CandidatesResponse` | Tentative emissions and selected direct/inherited review lineage. |
| `GET .../repositories/{repository_id}/candidates/{candidate_id}` | `Candidate` | One scoped candidate; published `review_write_enabled=false`. |
| `POST .../repositories/{repository_id}/candidates/{candidate_id}/reviews` | `ReviewReceipt` only for isolated test DRAFT | Reasoned decision, expected review ID and idempotency key; production/current published writes rejected. |

The ellipsis means `/investigations/{case_version_id}`. Artifact/finding/candidate detail is deliberately below the selected repository, enforcing case + snapshot + membership; there is no unscoped `/artifacts/{id}`. OpenAPI has the full paths.

`Scope` carries `case_id`, `case_version_id`, `case_version`, `analysis_snapshot_id`, `snapshot_state`, `rule_version`, `metric_definition_version` and `model_version`. Collection, candidate, review, sufficiency and finding are distinct typed states. `UNKNOWN` is a present finding with reason and sufficiency; no candidate is an empty candidate list, not a negative finding. No adoption/recovery rate or false denominator is calculated. Legacy `LEGACY_UNCLASSIFIED` assessments are outside the published allowlist.

Evidence pagination is **keyset by immutable `artifact_id` UUID ascending**. Default `limit=25`, allowed 1–100; `next_cursor` is the last returned ID only when another row exists. Carry the same snapshot, member and filters to the next request. UUID order is stable but **not event chronology**. Event time may be null and is never replaced with retrieval time. Published snapshots are immutable, preventing in-place page drift.
