# Phase 0 findings

## Decision: GO

Public data can reconstruct a defensible release lifecycle for carefully selected cases. NumPy 2.0 supplies direct evidence for the upstream release, downstream compatibility preparation, post-release binary failure, pins and upgrade workarounds, remediation work, and broader recovery signals.

The decision is qualified. PULSE should begin as a curated forensic workflow with human review, not an exhaustive ecosystem monitor. It can state what its collected evidence shows; it cannot infer universal adoption or causality from search hits and timestamps.

## What survived contact with data

- Release identity and timing are strong when PyPI and upstream notes agree.
- Explicit manifest changes, binary errors, compatibility releases, and maintainer guidance can connect multiple lifecycle stages.
- A typed evidence model and transparent rules preserve uncertainty without blocking useful analysis.
- A compatibility tracker provides a practical seed set of downstream repositories.

## Unresolved risks

- Unbiased downstream discovery is the hardest problem.
- Search and API limits may make coverage difficult to reproduce at scale.
- Recovery needs a declared cohort and operational definition.
- Repository evidence can disappear or be rewritten.
- Different ecosystems will require different package and lockfile adapters.

## Next decision gate

Before a product build, run the same method on at least two contrasting releases: one pure-Python API migration and one release without an upstream compatibility tracker. Continue only if discovery and confidence rules remain useful without NumPy’s unusually rich evidence.
