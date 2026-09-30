# Phase 5 M5.4 — integrated product validation findings

**Classification: PASS for bounded technical/product QA.** This is not stakeholder UAT or overall project closure. G8 remains `NOT_YET_VALIDATED`; M4.2 Power BI remains `DEFERRED`. The [acceptance table](m5-4/product-acceptance-results.md) records six PASS and four PARTIAL checks because the published cohort cannot demonstrate a positive support edge, live source-unavailable/conflict/0/0 examples or an authorized DRAFT review flow. Those limits do not justify inventing data or weakening current guardrails.

## Integrated architecture and method

The actual local React/TypeScript app on `127.0.0.1:5173` called FastAPI on `127.0.0.1:8000`, which read the existing governed PostgreSQL published validation rows. Browser navigation and screenshots used real API responses. [The focused validator](../../scripts/validate_m5_4_live.py) issued **131 GETs**, cross-checked API identities/states against PostgreSQL in a read-only transaction, exercised keyset pagination/filtering and scoped errors, and made no review or collection request. The database service was already running; a controlled API instance with deliberately invalid database credentials exercised `DATABASE_UNAVAILABLE` without stopping or changing the database. Normal API service was restored afterward.

## Workflow and golden reconciliation

The browser reached list → pytest/urllib3 overview → repository → evidence → finding, and the urllib3 candidate → artifact/provenance route, then returned through breadcrumbs. Direct entry, refresh and back/forward retained the exact case version, repository and `snapshot_id`; no route chose a latest DRAFT. List exposed only two `PUBLISHED_VALIDATION` snapshots: pytest `08852d5f-9843-5406-a69b-7039ea2ddaa4` and urllib3 `bd3a02a5-0c2d-5eec-84fd-8e9b93a238a3`. Their member counts were 2 and 6, including seven members with zero candidates.

| Reconciliation target | Live result |
| --- | ---: |
| Investigations / declared members | 2 / 8 |
| Findings / UNKNOWN / bounded NO / positive | 40 / 38 / 2 / 0 |
| Sufficiency: SUFFICIENT / INSUFFICIENT | 2 / 38 |
| Candidates / inherited REJECT / distinct candidate artifacts | 2 / 2 / 1 |
| Historical context records: PAIRED / AFTER_ONLY / UNRESOLVED | 1 / 6 / 9 |
| Members with no candidate / live SOURCE_UNAVAILABLE tasks | 7 / 0 |

The two bounded NO findings were individually checked; each is supported only within its selected evidence method and sufficient prerequisite state. Representative UNKNOWN findings matched API and database status/reason/sufficiency, and the UI says insufficient qualifying evidence rather than “no issue,” zero adoption or successful compatibility. No positive finding or adoption/recovery result is inferred. A current finding with no explicit support edge says so; source artifacts are still inspectable through the evidence explorer. Lifecycle categories are forensic questions, not required chronological stages or causal claims.

Both candidate firings are from the same copied-upstream GitHub pull request capture. They are separate rule emissions, **not** independent incidents, and show inherited REJECT plus the original candidate/review IDs and notes. No active published review control appears. The candidate → artifact path exposes source type, public reference, capture method (`collector` for this artifact), content SHA-256, task/run context, unavailable source event time and a separate retrieval time. Other evidence records had event time present; the live reconciliation counted eight with event time and 58 without. Retrieval time was never substituted. This source capture's method does not prove all other collection was unattended; method must be read per artifact.

## History, pagination and state safety

`AFTER_ONLY` is displayed as after-only context, never before/after proof; unresolved does not mean historical absence. The repository's total was relabeled “context records” after QA found that “pairs” overstated the six AFTER_ONLY and nine UNRESOLVED records. Evidence pagination was exercised with API `limit=2` and every `next_cursor`, plus a filtered `limit=1` traversal: 28 unfiltered page transitions, no duplicate or skipped artifact IDs, matching filtered and unfiltered totals, and stable case/snapshot/repository/filter scope. UUID keyset order is not called event chronology.

A legitimate zero-candidate member displayed an explanatory empty state. The current published data have **no live SOURCE_UNAVAILABLE task**, so that state was not manufactured; its distinct frontend treatment is covered by deterministic tests. An invalid snapshot produced `INVALID_SNAPSHOT` with no cross-snapshot fallback, and a cross-cohort repository produced `NOT_FOUND_IN_SELECTED_COHORT`. With the API stopped, the browser displayed `NETWORK_ERROR` and a retry control, not zero evidence. With a separate API process using invalid database credentials, `/health` returned HTTP 503 `DATABASE_UNAVAILABLE`; the frontend displayed the database error. Restoring normal API and clicking retry loaded the same route/snapshot. No stale success was presented as a current response.

## Usability and visual QA

Keyboard-only tabbing exposed a visible skip-link focus ring, reached navigation, breadcrumbs and the evidence filter, and Return applied a source-type filter. Headings, labels, table headers, status text and error messaging were inspected on the seven routes. This supports **baseline accessibility validated** for the checked interactions, not WCAG certification or a full assistive-technology audit. Desktop and a true 390px viewport were reviewed. After constraining intrinsic mobile grid widths and wrapping the context strip, the narrow repository had `innerWidth=390`, document `scrollWidth=375` and no page-level horizontal overflow. At 390px, evidence tables had 310px visible containers with 660–722px internal scroll widths while the document remained 375px wide, so table overflow stayed inside its scroll area. No overlapping control or clipped status text was observed in the final capture. The [developer/product friction log](m5-4/ux-friction-log.md) records changes and honest deferred gaps. Product copy was checked against [terminology](m5-1/product-terminology.md); no causal, adoption, safety or value claim was added.

Ten [actual product screenshots](m5-4/screenshots/README.md) cover all seven routes plus bounded NO, invalid snapshot and narrow layout. They have no mock data, Power BI substitution, browser debug overlay or credentials. Screenshot review found readable hierarchy, distinct status treatment and restrained version/hash context. Their presence supports portfolio preparation, not finished portfolio selection.

## Regression and local responsiveness

Ruff passed; the full Python suite passed **194 tests** (one upstream Starlette deprecation warning); frontend ESLint and TypeScript typecheck passed; Vitest passed **11 tests**; and the production build succeeded. The Python suite includes the M5.2 API contract and published review-write guard. A repeat live validator run returned median **101 ms** and maximum **215 ms** across 131 local GETs; an earlier run reached about **1.26 s** maximum, so timing varies with the local host. This is a basic responsiveness sanity check, not a latency SLA, production throughput measurement or scalability claim. No obviously blocking page/query was observed in the browser walkthrough.

## Acceptance, scope and next work

The implementation preserves repository-bounded investigation, explicit provenance and uncertainty and avoids generic SaaS expansion, causal claims and unsupported value claims. It presents a traceable BA → Product Analytics → governed data → API → UI story, while demand and actor assumptions remain provisional. [End-to-end traceability](m5-4/end-to-end-traceability.md) maps all 28 Phase 3 requirements; [consulting synthesis inputs](m5-4/consulting-synthesis-inputs.md) collect evidence without issuing the final recommendation; the [portfolio inventory](m5-4/portfolio-evidence-inventory.md) points to concrete proof.

Remaining work: genuine stakeholder responses and reconciliation (G8), manual M4.2 Power BI, final consulting recommendation, final README/case study, final résumé/interview package, and selected final portfolio screenshots/package. A future governed cohort or approved DRAFT setup is needed to exercise positive support, live source-unavailable/conflicting/0/0 conditions and authorized review writes. M5.4 made no schema change, collector run, external evidence retrieval, published data edit or real candidate review submission.
