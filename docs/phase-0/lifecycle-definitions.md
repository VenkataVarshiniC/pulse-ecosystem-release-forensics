# Lifecycle definitions

These definitions are operational labels for source-backed events. A label describes what the cited artifact demonstrates. It does not imply that one event caused another.

| Stage | Qualifying evidence | Does not qualify by itself |
|---|---|---|
| Release | An authoritative package index, upstream release record, or signed/tagged release with an occurrence time. | A planned milestone or an undated documentation page. |
| Adoption readiness | A downstream compatibility declaration, merged compatibility change, or passing test job against the target release. | Evidence that the target version was selected in ordinary downstream use. |
| Observed adoption | A manifest or lockfile selects the target version, or an ordinary downstream CI/runtime environment resolves it. | A compatibility claim, migration PR, or optional pre-release test matrix alone. |
| Migration friction | A version-specific failure, incompatibility, deprecation break, or migration task with a reproducible environment or concrete code surface. | A release mention with no demonstrated impact. |
| Remediation | A pin, workaround, revert, code change, test change, or downstream release intended to address release-associated friction. | Proof that the affected population recovered. |
| Recovery signal | A qualifying event within a declared cohort and time window, such as a downstream release explicitly shipping support or a previously failing ordinary CI path passing with the target version. | An upstream patch release, issue closure, or passage of time alone. |

## Adoption and readiness

Readiness describes capability before or independent of ordinary use. Adoption requires evidence that a repository, build, or runtime actually selected the target release. A project can be ready before a release exists, and a project can adopt a release before it is fully ready.

## Recovery claims

Every recovery statement must declare:

1. the population or named cohort;
2. the start and end of the observation window;
3. the qualifying recovery event; and
4. the denominator and projects with no qualifying event.

Phase 0B uses a purposive SQLAlchemy cohort of pandas and Flask-SQLAlchemy, observed from 2023-01-26 through 2023-09-11. Both have downstream releases that explicitly state SQLAlchemy 2.0 support. That supports recovery for this two-project cohort only. NumPy and Pydantic have remediation evidence, but the ledger does not claim cohort recovery for them.

## Confidence

- **High:** the primary artifact directly records the version, event, and repository relationship.
- **Medium:** the event is direct but incomplete, or the interpretation depends on a bounded analyst choice such as cohort selection.
- **Low:** the relationship is plausible but indirect, incomplete, or based mainly on temporal proximity.

Confidence applies to the observation, not to a causal claim. PULSE uses “release-associated” when evidence links an event to a release without proving causality.

In the ledger, `repository` identifies the downstream repository for readiness, adoption, friction, remediation, and recovery-signal events. It identifies the upstream repository only for the release event, where no downstream repository exists.
