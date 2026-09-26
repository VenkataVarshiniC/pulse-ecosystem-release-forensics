# Validation case: HTTPX 0.28.0

## Selection

HTTPX 0.28.0 was not used in Phase 0. It was selected before downstream classification because the upstream release removed previously deprecated client arguments, creating a clear version boundary in a widely used pure-Python library. The case tests whether the Phase 1 rules can process a new API-compatibility event without package-specific code.

The explicit cohort contains `openai/openai-python`, a public Python client with a direct HTTPX dependency and active public history in the window. A one-repository validation cohort is intentionally narrow and is not statistically representative.

## Collection result

All three committed HTTPX snapshots were obtained through connector-assisted retrieval and are explicitly typed `capture_method: connector_assisted`. They contain the preserved validation evidence and do not demonstrate a complete unattended PULSE collector run. Unattended collection remains unvalidated.

The window is 2024-10-28 through 2025-02-28. Three primary-source snapshots were preserved: the [HTTPX 0.28.0 release](https://github.com/encode/httpx/releases/tag/0.28.0), [openai-python issue #1915](https://github.com/openai/openai-python/issues/1915), and [openai-python PR #1905](https://github.com/openai/openai-python/pull/1905). Search observations record queries, counts, and the limits of negative evidence. Three of eleven planned tasks have snapshots. The manifest is therefore `incomplete`; uncollected repository metadata, commits, and dependency files remain explicit failures.

## Candidate and accepted evidence

The rules produced three candidates. Review accepted the issue as medium-confidence migration friction because it names HTTPX 0.28.0, the removed `proxies` argument, the exact `TypeError`, and the affected downstream version. Review accepted the merged release PR as medium-confidence remediation because it explicitly states compatibility with HTTPX 0.28.0 and links its implementing commit.

The issue also triggered the remediation keyword rule because its text linked to a fix. Review rejected that candidate: the issue was contextual evidence, while PR #1905 was the direct remediation artifact. This false positive demonstrates why deterministic detection and accepted evidence remain separate.

## Result

The generated report records friction and remediation as `yes`. Adoption and recovery remain `unknown_insufficient_data` because collection was incomplete and no accepted evidence established those stages. Observed adoption **evidence coverage** is 0/1: no accepted adoption evidence, not zero adoption. Friction incidence is unavailable at 0/0 under its declared denominator; remediation coverage is 1/1. These are cohort results, not ecosystem rates.

The timeline places the 2024-11-28 compatibility response in openai-python 1.55.3 before the 2024-12-02 friction report involving the older 1.54.4 release. Both follow the HTTPX 0.28.0 release, which was also on 2024-11-28. Lifecycle stages are evidence categories; they need not appear in stage order and do not imply that the later issue prompted the earlier fix.

Run `uv run python scripts/reproduce_validation.py` to regenerate the manifest, review ledger, structured forensics, and Markdown report from the committed snapshots and decisions.
