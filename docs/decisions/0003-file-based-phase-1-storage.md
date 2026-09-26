# ADR 0003: Use file-based storage in Phase 1

## Status

Accepted

## Decision

Store source envelopes as JSON, reviewable evidence as JSONL, and forensic outputs as JSON plus generated Markdown. Use exclusive raw writes and stable logical identifiers.

## Consequences

Investigations remain easy to audit, diff, and reproduce without database operations. Concurrent high-volume analytics are deferred until measured volume or query needs justify a warehouse.
