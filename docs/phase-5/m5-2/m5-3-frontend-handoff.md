# M5.3 frontend handoff

Use base URL `http://127.0.0.1:8000/api/v1` for local development. Run the API on loopback. CORS permits only `http://localhost:5173` and `http://127.0.0.1:5173`, with GET/POST and `Content-Type`; there is no wildcard production policy. Generated [`OpenAPI JSON`](../../../data/validation/m5-2-openapi.json) is the machine-readable type contract; [endpoint details](endpoint-contract.md) and [errors](error-contract.md) state product semantics. Build React/TypeScript in M5.3 only.

| M5.1 screen | M5.2 read path | Key rendering rule |
|---|---|---|
| Investigation List | `GET /investigations` | Open exact `scope.case_version_id` and `scope.analysis_snapshot_id`; no implicit latest. |
| Investigation Overview | `GET /investigations/{case_version_id}?snapshot_id=...` | Keep all declared members, including zero candidates; show literal finding counts. |
| Repository Investigation | `GET .../repositories/{repository_id}?snapshot_id=...` | Separate declaration, resolved observation, historical pair, source task, finding and candidate. |
| Evidence Explorer | `GET .../evidence?limit=...&cursor=...&snapshot_id=...` | Group by source/ref; UUID pagination is not chronology. Keep null event time distinct from retrieval time. |
| Finding Detail | `GET .../findings` or `GET .../findings/{finding_id}` | `UNKNOWN`, bounded NO and future qualifying status use `finding_status`, `sufficiency_status`, `reason_code`, `source_reasons`, actual support IDs. |
| Candidate Review | `GET .../candidates` or `GET .../candidates/{candidate_id}` | Inherited review is labeled as reuse of original review; `review_write_enabled=false` on current published data. |
| Artifact/Provenance | `GET .../artifacts/{artifact_id}` | Show allowed `public_locator`/`external_public_locators`, capture method, digest and two clocks; a null public locator means no safe direct link. |

Every detail path is under `/investigations/{case_version_id}`; carry `snapshot_id` on every request. Use UUIDs returned by the API, never invent a repository from an unscoped search. Standard read responses carry `scope` on list/detail envelopes; individual `Finding`/`Candidate` detail uses the scope already present in the URL/query and parent navigation. Loading or network/backend failure must not display zero evidence. A 404 for wrong case/member/snapshot is not an empty cohort. `SOURCE_UNAVAILABLE` is data; HTTP 503 means the API/database failed. The API does not return a percentage for unavailable adoption/recovery or turn no candidate into bounded NO.

`EvidencePage.next_cursor` is null at end. Repeat the same filters and exact snapshot on each page; default limit 25, maximum 100. Filters are exact source type, repository ref or path. Current published review POSTs return `PUBLISHED_IMMUTABLE`. **Do not render an enabled review form for the two published snapshots.** A future form must require a distinct, authorized DRAFT workflow and server-trusted identity; sending a user-entered reviewer string does not authorize a decision. No case creation, attention override, closure, Power BI dashboard, authentication console or risk score is supplied by M5.2.

The frontend should honor [uncertainty UX](../m5-1/uncertainty-ux.md) and [product terminology](../m5-1/product-terminology.md). Screen order and utility remain **PROVISIONAL — STAKEHOLDER VALIDATION PENDING** (G8).
