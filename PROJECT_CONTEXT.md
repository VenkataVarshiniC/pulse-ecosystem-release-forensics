# PULSE product context

## Product thesis

PULSE reconstructs the lifecycle of significant open-source software changes using real public evidence. The release has already happened; PULSE explains what happened afterward.

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

PULSE is not a generic release dashboard, vulnerability scanner, dependency graph viewer, pre-release predictor, chatbot, or GitHub analytics dashboard. Phase 0 establishes data feasibility only; later product architecture must follow a fresh decision.
