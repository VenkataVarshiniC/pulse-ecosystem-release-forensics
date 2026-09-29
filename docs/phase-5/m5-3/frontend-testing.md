# Frontend testing and validation

The deterministic component suite uses Vitest, jsdom and Testing Library. Fixture objects include the M5.2 schema fields for scope, investigation, member, observation, finding, candidate, evidence page and provenance. The tests exercise two API-provided investigations, snapshot-preserving navigation, a zero-candidate member, declaration versus resolution, AFTER_ONLY, UNKNOWN versus bounded NO, unavailable source, null event time, server cursor plus filters, inherited REJECT, a shared artifact, published read-only controls, API failure/invalid snapshot, and safe/unsafe public locator handling. No current golden count is hard-coded into application components.

From `frontend/` run:

```text
npm ci
npm run typecheck
npm run lint
npm run test
npm run build
```

The browser smoke check on 2026-09-29 used the live local M5.2 API and PostgreSQL. It verified the two-case list, pytest overview (two declared members), a real repository (declaration, historical states and five findings), one bounded finding, urllib3 candidate with inherited REJECT and shared artifact, artifact provenance and the evidence explorer. API health returned `database_reachable=true`. This is a bounded read-only smoke check, not full end-to-end acceptance. Visual inspection was performed in the local browser; repository screenshot files are deferred to M5.4 because the available browser capture did not provide a reliable supported path to save them as repository artifacts.

Final M5.3 validation: `npm run typecheck` passed; `npm run lint` passed; `npm run test` passed (11 tests in 1 file); `npm run build` passed (38 modules transformed). The unchanged Python API contract and published-read regression subset passed (19 tests) with one existing Starlette/httpx deprecation warning. M5.4 should add cross-browser and narrow-screen visual QA, keyboard navigation review, full API interaction tracing, and review of wording with actual stakeholders. G8 remains `NOT_YET_VALIDATED`.
