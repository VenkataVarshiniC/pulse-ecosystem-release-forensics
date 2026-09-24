# ADR 0002: Model PyPI response URLs as artifacts

**Status:** Accepted

## Context

PyPI’s project and version JSON responses use `urls` for the distribution files attached to the selected version. The initial adapter exposed those files as `PackageMetadata.releases`, which incorrectly suggested that the collection represented package release history.

## Decision

Rename `PackageRelease` to `DistributionArtifact`, `PackageMetadata.releases` to `artifacts`, and `latest_version` to `version`. The `version` field is the version returned by the selected endpoint; each artifact repeats that version and records its own upload timestamp, URL, and Python constraint.

Release history would require parsing the separate `releases` mapping from the unversioned project response and is outside the current adapter contract.

## Consequences

The type names now match PyPI semantics, and callers cannot mistake wheels and source distributions for distinct releases. Existing callers must adopt the new field names.
