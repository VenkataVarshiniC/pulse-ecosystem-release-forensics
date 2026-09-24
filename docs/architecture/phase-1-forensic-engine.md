# Phase 1 forensic engine

```text
YAML case + declared cohort
            ↓
deterministic collection plan
            ↓
modular GitHub / PyPI collectors
            ↓
immutable raw JSON envelopes + run manifest
            ↓
dependency parsing / transparent text rules
            ↓
candidate evidence JSONL
            ↓
explicit review decisions
            ↓
accepted typed evidence events
            ↓
repository lifecycle summaries + cohort metrics
            ↓
forensics JSON → generated Markdown report
```

## Boundaries

Configuration owns release-specific facts. Collectors only retrieve and preserve source records. Parsers and detectors normalize raw artifacts into candidates but cannot accept them. The forensic engine reads accepted evidence and treats collection completeness as an independent input, which prevents missing artifacts from becoming negative claims. Reporting is a deterministic projection of the structured result.

## Failure and idempotency

The runner catches task failures independently and returns an incomplete manifest when at least one task succeeds. Raw files use exclusive creation with task ID and retrieval timestamp, so an existing snapshot is never silently replaced. Candidate IDs hash logical identity; accepted events deduplicate on that ID. Re-running analysis over the same snapshots and decisions produces the same ledger and report.

## Tradeoffs

Local JSON and JSONL keep provenance inspectable and versionable at Phase 1 volume. Search remains API-dependent, and files are less suitable for concurrent large-scale analysis. Rule-based detection is explainable and testable but deliberately leaves ambiguous context for human review. The architecture reserves no AI-only step; a future classifier would have to emit the same reviewable evidence contract.
