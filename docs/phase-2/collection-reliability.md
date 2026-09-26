# Collection reliability contract

## Running a collection

Set `GITHUB_TOKEN` in the process environment and run `uv run pulse collect cases/httpx-0.28.0.yaml`. Use `--resume` to reuse intact successful tasks from previous runs of that exact case definition. `--output-root PATH`, `--max-pages N` (default 1000), and `--max-retries N` (default 3) control the output location and safety limits. A missing or blank token produces a typed authentication/configuration error before the run creates files. The token is sent only as a bearer authorization header; PULSE does not persist it or copy response bodies into failure messages. Authentication is required even when resuming, because pending tasks may need collection.

The CLI prints the new run manifest path. It exits successfully only when every planned task succeeded or was safely reused. The run folder is `data/interim/<case-id>/runs/<run-id>/`; it contains the case and plan in `run.json`, one `.attempt.json` for every completed task attempt, and `manifest.json` when the run reaches its end. Raw envelopes are stored under `data/raw/<case-id>/<source>/<repository>/`. The CLI creates new run folders on every invocation and writes all records exclusively; it never updates a prior run or snapshot. The legacy Phase 1 `collection-manifest.json` writer remains available for historical replay, but new live runs use per-run manifests.

## Identity and observations

A *logical task ID* hashes case ID, source, query kind, repository, and query parameters. It is stable across repeated executions of the same plan. A *run ID* identifies one invocation. Each planned task receives a distinct *attempt ID* in that run, including an explicit reuse decision. Automatic HTTP retries stay within the same attempt and increment its retry count. A SHA-256 fingerprint of the full case definition prevents `--resume` from silently reusing data when the cohort, window, or rules change.

Each attempt record retains the task ID, source, repository, query kind and parameters, observation window, start and end times, status, matched record count, failure kind, and collection statistics. A reused success carries forward the prior matched count while its statistics show zero new requests. Statistics include pages requested/completed, raw records examined, duplicate records suppressed, retries, termination reason, and safe status or transport-error metadata for each HTTP request. Available rate-limit remaining, reset time, and Retry-After values are retained per response. A completed query with **zero matching records** is a successful observation with a raw envelope containing an empty list. A zero-match result from an incomplete query is `partial` or another failure, never evidence of absence.

The raw envelope includes `run_id`, `attempt_id`, query, capture metadata, retrieval time, source payload, and the task's statistics. Live PULSE runs label new envelopes `capture_method = collector`. The committed HTTPX validation snapshots retain `connector_assisted`; fixture envelopes remain `fixture`. No provenance label is inferred from data content.

## Pagination and filtering

The GitHub client requests up to 100 items per page and follows the API's `Link: rel="next"` header for issues, pull requests, commits, and releases. It does not assume a short page is final. It rejects a next link outside the configured API origin, detects repeated URLs, and stops with an explicit incomplete outcome when the configured page limit is reached. Duplicate records across pages are suppressed using GitHub identity fields (`id`, `node_id`, `sha`, or `number`, in that order), with a stable full-record fallback. Raw records examined and duplicates are counted separately from matches retained after filtering.

Issues returned from the issues endpoint that represent pull requests are excluded from the issue task. Issues and pull requests are filtered locally by creation date against the declared window, while commits use GitHub's `since` and `until` parameters. Releases are collected as an upstream release list. The GitHub issues `since` parameter concerns updates; the local creation-date filter defines the retained issue window. The PR endpoint is paginated without a server-side date bound. Consequently, a large historical repository may hit the page limit before complete PR coverage. Such a task is incomplete and cannot support a negative finding. Repository and file metadata requests are single-response queries.

## Failure and retry policy

Task outcomes are `succeeded`, `partial`, `rate_limited`, `not_found`, `unauthorized`, or `failed`:

| Outcome | Meaning |
| --- | --- |
| `succeeded` | The request or pagination chain completed, including a complete zero-match result. |
| `partial` | At least one page completed before a later API or pagination failure; the completed data is preserved. The attempt also records the underlying failure kind. |
| `rate_limited` | GitHub signaled a rate limit and no completed page is available; retry or wait budget prevented completion. |
| `not_found` | GitHub returned 404 before a page completed. This can also reflect inaccessible private resources. |
| `unauthorized` | Missing token, HTTP 401, or HTTP 403 without reliable rate-limit indicators. HTTP 403 can represent a permission denial. |
| `failed` | Other API, decoding, transport, or internal task failures. |

HTTP 429, recognizable rate-limit HTTP 403, selected 5xx responses (500, 502, 503, 504), and transport errors may be retried. The default is at most three retries after the first request. Backoff is exponential from 0.5 seconds. `Retry-After` (seconds or HTTP date) and the GitHub reset time are honored where supplied. An unhinted rate-limit response uses at least a 60-second wait. If a required delay exceeds the 60-second per-retry wait budget, the attempt stops as `rate_limited` rather than retrying early. Sleep and clock functions are injectable, so tests do not wait. Authentication failures, 404, and other nontransient API errors are not retried. The client records each response and retry count without persisting headers wholesale, request URLs, or error bodies. This is a bounded retry policy, not a rate-limit scheduler. It follows GitHub's [pagination](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api) and [retry/rate-limit guidance](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api).

## Resume and evidence use

`--resume` scans prior attempt checkpoints for the same case fingerprint and task definition. Only a `succeeded` attempt with an existing, SHA-256-matching `collector` snapshot and matching case, task, run, attempt, and query metadata is reused. An incomplete or failed attempt, including a `partial` one with an empty first page, is retried as a new attempt. Reuse writes a new attempt record that points to the earlier immutable snapshot; it makes no HTTP request for that task. Checkpoints can be reused even if an interrupted run never wrote its final manifest. Prior failures and partial snapshots remain available for audit. Candidate detection uses stable source and rule identities to collapse repeated evidence from retry and rerun snapshots into one logical candidate.

Resume is at the whole-task boundary. A crash during a task may require that task's already fetched pages to be requested again; completed task checkpoints remain reusable. Runs execute sequentially, with no concurrent-writer coordination. Snapshot paths are absolute, so moving a collection output directory invalidates automatic reuse until paths are reconciled. A changed case definition deliberately causes new collection. A completed response is an observation of public API data under the recorded query and access scope; it does not prove an event never occurred.

## Validation boundary

The ordinary test suite uses HTTP mock transports to cover pagination, deduplication, termination, retries, rate limits, failure kinds, partial snapshots, zero matches, missing credentials, tamper detection, reuse, and repeated-run candidate identity. It also runs Phase 0 and Phase 1 regression tests. These tests establish deterministic collector behavior under simulated responses. They do not establish live API availability, permission completeness, historical coverage, or a successful unattended HTTPX cohort collection. No new cohort, historical ref pairing, or detector precision claim is part of this milestone.
