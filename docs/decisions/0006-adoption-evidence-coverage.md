# ADR 0006: Measure observed-adoption evidence coverage explicitly

## Status

Accepted

## Context

The HTTPX report paired unknown adoption with `observed_adoption_coverage: 0/1 (0.0%)`. Although the numerator counted accepted evidence, the name could imply a measured absence of adoption.

## Decision

Rename the metric to `observed_adoption_evidence_coverage`. Its numerator counts repositories with accepted observed-adoption evidence; its denominator remains the declared cohort. Keep it available during incomplete collection because it describes evidence in hand. Its qualification rule in both structured and Markdown output explicitly states that zero evidence coverage is not zero adoption.

Repository findings remain independently three-state: yes, no qualifying evidence found, or unknown/insufficient data. Neither unknown nor no qualifying evidence is proof that adoption did not occur. Collection coverage remains separately visible. The old metric name is removed from generated outputs; consumers must use the new name.

## Consequences

The metric remains useful for measuring investigation coverage without estimating adoption prevalence. Tests cover a wholly incomplete cohort with zero evidence and a mixed cohort with accepted adoption in one member and unknown adoption in another. The Phase 1 PIVOT decision remains unchanged.
