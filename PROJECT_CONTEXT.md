# PULSE product context

## Product definition

PULSE is a repository-bounded release-forensics system that reconstructs how a software dependency release affects a declared cohort of downstream repositories using auditable public evidence. The release has already happened; PULSE explains the public record afterward.

## Core lifecycle

```text
Release
   ↓
Downstream adoption
   ↓
Migration / breakage signals
   ↓
Human remediation
   ↓
Patch / workaround / documentation response
   ↓
Ecosystem recovery
```

## Possible evidence

- package releases and metadata
- dependency manifests and lockfiles
- GitHub releases, issues, pull requests, and commits
- version upgrades, downgrades, and pins
- migration pull requests and compatibility fixes
- workarounds, changelogs, and migration guides

## Analytical rules

- Never fabricate data or metrics.
- Preserve source evidence and retrieval context.
- Keep raw observations, normalized records, and analytical conclusions separate.
- Temporal association does not establish causality.
- Say **release-associated**, **observed after release**, **migration-related evidence**, or **temporally associated** unless stronger evidence supports a causal claim.
- Make confidence and the reason for confidence explicit.
- Prefer reproducible rules and human review before probabilistic classification.

## Product boundary

PULSE is not a generic release dashboard, vulnerability scanner, dependency graph viewer, pre-release predictor, chatbot, or GitHub analytics dashboard. It does not claim ecosystem representation from an explicit or purposive cohort. Phase 1 uses deterministic rules and human review; it does not use AI or ML classification.

## Current phase decision

Phase 0 remains the historical feasibility record. Phase 1 implements the file-based forensic engine and validates it on HTTPX 0.28.0 with an explicit one-repository cohort. The Phase 1 decision is **PIVOT**: retain the evidence model and pipeline, then harden live, comprehensive collection and historical manifest comparison before scaling the architecture.
