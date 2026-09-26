# ADR 0005: Separate deterministic candidates from accepted evidence

## Status

Accepted

## Decision

Phase 1 uses transparent rules to create candidate evidence. Acceptance and rejection are explicit terminal transitions with notes and timestamps. Keyword matches cannot receive high confidence, and no ML or LLM classification is introduced.

## Consequences

False positives remain visible and every accepted event has a review trail. The baseline is slower than full automation but can later evaluate assisted classification against a stable, auditable contract.
