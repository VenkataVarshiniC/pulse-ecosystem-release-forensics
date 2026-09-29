# M5.3 frontend architecture

The operational application lives in [`frontend/`](../../../frontend). It is a React 19 + TypeScript 6 single-page application built by Vite 8. It reads the M5.2 FastAPI boundary; it has no direct database connection, write workflow, BI dashboard, or authentication layer. The UI is **PROVISIONAL — STAKEHOLDER VALIDATION PENDING** (G8 `NOT_YET_VALIDATED`).

## Run locally

Start the existing backend on `127.0.0.1:8000` with its configured PostgreSQL environment. In `frontend/`, run `npm ci` and `npm run dev`. The frontend serves `127.0.0.1:5173`. `VITE_PULSE_API_BASE_URL` defaults to `http://127.0.0.1:8000/api/v1`; copy `.env.example` to `.env.local` only if a different local API origin is needed. The M5.2 CORS allowlist covers `127.0.0.1:5173` and `localhost:5173`.

`src/api/types.ts` contains explicit TypeScript interfaces matching the committed M5.2 OpenAPI read schemas. This avoids a generated-code dependency while retaining nullable event time, literal UNKNOWN/NO states, source reasons, capture method, review origin, and snapshot scope. `src/api/client.ts` owns every network request, base URL, query construction and structured error parsing. A future API schema change requires a deliberate comparison with `data/validation/m5-2-openapi.json` and contract tests; compile-time types alone do not validate arbitrary network JSON at runtime.

React Router owns seven case-scoped screens. Route helpers in `src/utils/routes.ts` carry the selected `snapshot_id` in every detail URL and breadcrumb. `useScope` rejects missing/malformed UUIDs. `useApiData` aborts obsolete requests, preserves the current request key on retry, and checks returned case/snapshot scope for envelope responses. Detail endpoints for a finding or candidate return the entity directly; their case/repository/snapshot boundary is enforced by M5.2 and the scoped URL.

CSS is local to `src/styles/app.css` with restrained status tokens, table/record patterns, visible focus, and narrow-screen reflow. No external font or UI component service is required. API data is never copied into a client global store; each screen requests its own selected resource. The Evidence Explorer alone holds local filter and cursor history, using API-provided `next_cursor` rather than slicing client data.

No Python, PostgreSQL, frozen source, dbt, analytics or Power BI files were changed for M5.3.
