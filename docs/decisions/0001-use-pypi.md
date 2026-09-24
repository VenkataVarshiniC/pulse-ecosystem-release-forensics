# ADR 0001: Use PyPI for Phase 0

**Status:** Accepted

## Context

Phase 0 needs exact release files and upload timestamps, package metadata, source links, Python requirement metadata, and a small client surface. Both npm and PyPI expose useful public metadata, but implementing both would dilute the feasibility test.

## Decision

Use PyPI. Its unauthenticated JSON endpoints provide project and version records in a compact, stable shape, while candidate Python projects have rich GitHub issue and pull-request histories. NumPy 2.0 also provides an unusually clear ABI transition across compiled downstream packages.

## Consequences

The result demonstrates feasibility for the Python ecosystem only. npm lockfile conventions, monorepos, scoped packages, and registry behavior require a separate study before claiming portability.
