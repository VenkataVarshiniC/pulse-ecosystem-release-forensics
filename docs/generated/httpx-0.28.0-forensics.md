# Release forensics: httpx 0.28.0

## Release summary

- Case: `httpx-0.28.0`
- Observation window: 2024-10-28 to 2025-02-28
- Accepted evidence events: 2

## Declared cohort

Selection method: `explicit`. A deliberately narrow validation cohort selected before classification: one public Python client library that directly declared httpx and had active public development during the observation window. It is a product validation sample, not a representative population.

- `openai/openai-python`

## Collection coverage

0 of 1 cohort repositories had sufficient collection.

## Release timeline

- 2024-11-28 — **remediation** — release: 1.55.3 (medium; [source](https://github.com/openai/openai-python/pull/1905))
- 2024-12-02 — **migration_friction** — httpx 0.28.0 removed proxies in httpx.Client, result in error (medium; [source](https://github.com/openai/openai-python/issues/1915))

## Repository findings

### openai/openai-python

- Observed adoption: `unknown_insufficient_data`
- Migration friction: `yes`
- Remediation: `yes`
- Recovery signal: `unknown_insufficient_data`
- Overall confidence: `medium`

## Observed adoption

- `openai/openai-python`: `unknown_insufficient_data` — Collection was incomplete or unavailable, so the stage is unknown.

## Migration friction

- `openai/openai-python`: `yes` — 1 accepted migration_friction event(s).

## Remediation

- `openai/openai-python`: `yes` — 1 accepted remediation event(s).

## Bounded recovery

- `openai/openai-python`: `unknown_insufficient_data` — Collection was incomplete or unavailable, so the stage is unknown.

## Cohort metrics

- **observed_adoption_coverage:** 0/1 (0.0%). Accepted observed-adoption event / declared cohort repositories.
- **friction_incidence:** 0/0 (unavailable). Accepted friction event / repositories with observed adoption.
- **remediation_coverage:** 1/1 (100.0%). Accepted remediation event / repositories with accepted friction.

## Confidence

- medium: 2

## Missing evidence

- openai/openai-python: sufficient public artifacts were not collected
- openai/openai-python: no accepted observed_adoption evidence
- openai/openai-python: no accepted recovery_signal evidence

## Limitations

- Metrics describe only the declared cohort and observation window.
- No qualifying evidence found does not prove that no event occurred.
- Accepted evidence supports association unless a source demonstrates causality.

## Source references

- https://github.com/openai/openai-python/issues/1915
- https://github.com/openai/openai-python/pull/1905
