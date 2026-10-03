# Phase 7 source-availability model

Taxonomy version: `p7-question-prerequisites-v1`

Availability is recorded independently from finding state. These states describe whether a source was planned, reachable, complete, and fit for the bounded comparison. They never silently supply negative evidence.

| State | Meaning | Permitted effect |
| --- | --- | --- |
| `NOT_PLANNED` | The source class is outside the frozen treatment, such as installed-version or recovery evidence. | Prerequisite remains unmet and the finding remains `UNKNOWN`. |
| `AVAILABLE` | The approved source was retrieved, parsed, and is fit for the declared comparison. | It may satisfy a prerequisite; content still determines qualification. |
| `NOT_FOUND` | An approved path returned 404 at one exact ref. | It describes that ref/path only. It does not prove repository-wide or dependency absence. |
| `INCOMPLETE` | A response, encoding, parser result, indirection, or dynamic manifest prevents exhaustive use. | Comparison remains unresolved; absence cannot be inferred. |
| `SOURCE_UNAVAILABLE` | Access failed because of a bounded transport, server, policy, authorization, or rate-limit stop. | The attempt and failure are preserved; no fallback or negative finding is allowed. |
| `STRUCTURALLY_UNAVAILABLE` | No eligible repository anchor exists at the prescribed boundary, or the observation-end anchor is not after release. | Dependent exact-ref requests become virtual stopped attempts and the history record is unresolved. |
| `CONFLICTING` | Multiple target declarations within the same parser declaration group yield incompatible states. | The history record is unresolved; a declaration is not selected opportunistically. |

## Mapping to history states

- `PAIRED`: both approved path states are `AVAILABLE` at eligible exact refs.
- `AFTER_ONLY`: the pre-release path state is `NOT_FOUND` and the after state is `AVAILABLE`.
- `UNRESOLVED`: every other combination, including both `NOT_FOUND`, any incomplete/unavailable/structural/conflicting state, or an ineligible anchor.

Target presence is evaluated separately. A `PAIRED` record can contain no target declaration and still be a valid path-state pair; it cannot satisfy the paired pre-release target prerequisite in that case.

## Stop reasons

Each attempt or derived history record carries one controlled stop reason:

- `BOUNDED_REQUESTS_COMPLETE`
- `ANCHOR_NOT_FOUND`
- `AFTER_ANCHOR_NOT_AFTER_RELEASE`
- `PATH_NOT_FOUND_AT_REF`
- `BOTH_PATH_STATES_NOT_FOUND`
- `SOURCE_ACCESS_STOP`
- `RESPONSE_INCOMPLETE`
- `PARSE_INCOMPLETE`
- `CONFLICTING_DECLARATIONS`
- `SOURCE_NOT_PLANNED`

The live collector performs 16 anchor attempts and exactly 32 file attempts, including virtual stopped attempts when an anchor is unavailable. It does not paginate, discover alternate paths, traverse parents, switch branches or tags, clone repositories, or consult private sources.

## Provenance

Every attempt records case, repository, source type, anchor role, optional path/ref, event time when available, retrieval time, raw path and digest, content digest for retrieved files, retry count, availability, reason, stop reason, run ID, task ID, treatment method, and collector capture method. Authentication material and response headers are excluded.
