# Release forensics: urllib3 2.0.0

Case `urllib3-2.0.0`; release boundary 2023-04-26T17:21:22.577020+00:00; observation window 2023-03-27 to 2023-08-24.

## Frozen cohort and selection

`urllib3-2.0.0-rule-based` (rule_based). First six eligible repositories by the predeclared SHA-256 ranking of a bounded GitHub code-search candidate frame; no release outcomes inspected.

- `atenreiro/opensquat`
- `jamesturk/scrapelib`
- `wimglenn/advent-of-code-data`
- `Aiven-Open/pghoard`
- `facundoolano/feedi`
- `enzet/map-machine`

## Collection and review

Collector run `5ba100d9629143f880ce8f5779d6d747`: complete; historical run `027bc3fc71334e138d8ec73bedde28a1`.
Collection tasks: planned=39, succeeded=34, partial=0, rate_limited=0, not_found=5, unauthorized=0, failed=0, optional_not_found=5, required_failures=0.
Upstream sources: pypi_version=`complete`, upstream_repository=`complete`, upstream_releases=`complete`.
Detector candidates: 2; accepted: 0; rejected: 2; needs review: 0.
Rejected candidate output is detector-quality evidence, not accepted lifecycle evidence.

## Historical dependency context and repository findings

### atenreiro/opensquat

Historical context: `historically_unknown`. A declaration does not establish target-version installation or adoption.
Historical paths: `pyproject.toml` insufficient_history (before unavailable; after unavailable; transition unknown); `requirements.txt` missing_before (before unavailable; after unavailable; transition unknown).
Candidates emitted/rejected/unresolved: 0/0/0.
Accepted-event confidence: `unavailable`.
Source coverage: repository_metadata=`complete` (1/1 succeeded, 0 optional 404), issues=`complete` (1/1 succeeded, 0 optional 404), pull_requests=`complete` (1/1 succeeded, 0 optional 404), commits=`complete` (1/1 succeeded, 0 optional 404), current_manifest_probes=`complete` (2/2 succeeded, 0 optional 404), historical_dependency=`partial` (0/2 succeeded, 0 optional 404), reviewed_candidates=`complete` (0/0 succeeded, 0 optional 404), downstream_releases=`not_collected` (0/0 succeeded, 0 optional 404).
- adoption_readiness: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- observed_adoption: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- migration_friction: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- remediation: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- recovery_signal: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
Missing sources: historical_dependency, downstream_releases.
Unknown stages: adoption_readiness, observed_adoption, migration_friction, remediation, recovery_signal.

### jamesturk/scrapelib

Historical context: `historically_unknown`. A declaration does not establish target-version installation or adoption.
Historical paths: `pyproject.toml` missing_before (before unavailable; after unavailable; transition unknown); `requirements.txt` insufficient_history (before unavailable; after unavailable; transition unknown).
Candidates emitted/rejected/unresolved: 2/2/0.
Accepted-event confidence: `unavailable`.
Source coverage: repository_metadata=`complete` (1/1 succeeded, 0 optional 404), issues=`complete` (1/1 succeeded, 0 optional 404), pull_requests=`complete` (1/1 succeeded, 0 optional 404), commits=`complete` (1/1 succeeded, 0 optional 404), current_manifest_probes=`complete` (1/2 succeeded, 1 optional 404), historical_dependency=`partial` (0/2 succeeded, 0 optional 404), reviewed_candidates=`complete` (2/2 succeeded, 0 optional 404), downstream_releases=`not_collected` (0/0 succeeded, 0 optional 404).
- adoption_readiness: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- observed_adoption: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- migration_friction: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- remediation: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- recovery_signal: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
Missing sources: historical_dependency, downstream_releases.
Unknown stages: adoption_readiness, observed_adoption, migration_friction, remediation, recovery_signal.

### wimglenn/advent-of-code-data

Historical context: `historically_supported`. A declaration does not establish target-version installation or adoption.
Historical paths: `pyproject.toml` missing_before (before unavailable; after urllib3; transition unknown); `requirements.txt` insufficient_history (before unavailable; after unavailable; transition unknown).
Candidates emitted/rejected/unresolved: 0/0/0.
Accepted-event confidence: `unavailable`.
Source coverage: repository_metadata=`complete` (1/1 succeeded, 0 optional 404), issues=`complete` (1/1 succeeded, 0 optional 404), pull_requests=`complete` (1/1 succeeded, 0 optional 404), commits=`complete` (1/1 succeeded, 0 optional 404), current_manifest_probes=`complete` (1/2 succeeded, 1 optional 404), historical_dependency=`partial` (0/2 succeeded, 0 optional 404), reviewed_candidates=`complete` (0/0 succeeded, 0 optional 404), downstream_releases=`not_collected` (0/0 succeeded, 0 optional 404).
- adoption_readiness: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- observed_adoption: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- migration_friction: **no_qualifying_evidence_found** — Required sources were completely collected and emitted candidates were reviewed; no accepted qualifying evidence was found. This does not prove the event did not happen.
- remediation: **no_qualifying_evidence_found** — Required sources were completely collected and emitted candidates were reviewed; no accepted qualifying evidence was found. This does not prove the event did not happen.
- recovery_signal: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
Missing sources: historical_dependency, downstream_releases.
Unknown stages: adoption_readiness, observed_adoption, recovery_signal.

### Aiven-Open/pghoard

Historical context: `historically_unknown`. A declaration does not establish target-version installation or adoption.
Historical paths: `pyproject.toml` insufficient_history (before unavailable; after unavailable; transition unknown); `requirements.txt` insufficient_history (before unavailable; after unavailable; transition unknown).
Candidates emitted/rejected/unresolved: 0/0/0.
Accepted-event confidence: `unavailable`.
Source coverage: repository_metadata=`complete` (1/1 succeeded, 0 optional 404), issues=`complete` (1/1 succeeded, 0 optional 404), pull_requests=`complete` (1/1 succeeded, 0 optional 404), commits=`complete` (1/1 succeeded, 0 optional 404), current_manifest_probes=`complete` (1/2 succeeded, 1 optional 404), historical_dependency=`partial` (0/2 succeeded, 0 optional 404), reviewed_candidates=`complete` (0/0 succeeded, 0 optional 404), downstream_releases=`not_collected` (0/0 succeeded, 0 optional 404).
- adoption_readiness: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- observed_adoption: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- migration_friction: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- remediation: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- recovery_signal: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
Missing sources: historical_dependency, downstream_releases.
Unknown stages: adoption_readiness, observed_adoption, migration_friction, remediation, recovery_signal.

### facundoolano/feedi

Historical context: `historically_unknown`. A declaration does not establish target-version installation or adoption.
Historical paths: `pyproject.toml` missing_before (before unavailable; after unavailable; transition unknown); `requirements.txt` missing_before (before unavailable; after unavailable; transition unknown).
Candidates emitted/rejected/unresolved: 0/0/0.
Accepted-event confidence: `unavailable`.
Source coverage: repository_metadata=`complete` (1/1 succeeded, 0 optional 404), issues=`complete` (1/1 succeeded, 0 optional 404), pull_requests=`complete` (1/1 succeeded, 0 optional 404), commits=`complete` (1/1 succeeded, 0 optional 404), current_manifest_probes=`complete` (1/2 succeeded, 1 optional 404), historical_dependency=`partial` (0/2 succeeded, 0 optional 404), reviewed_candidates=`complete` (0/0 succeeded, 0 optional 404), downstream_releases=`not_collected` (0/0 succeeded, 0 optional 404).
- adoption_readiness: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- observed_adoption: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- migration_friction: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- remediation: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- recovery_signal: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
Missing sources: historical_dependency, downstream_releases.
Unknown stages: adoption_readiness, observed_adoption, migration_friction, remediation, recovery_signal.

### enzet/map-machine

Historical context: `historically_unknown`. A declaration does not establish target-version installation or adoption.
Historical paths: `pyproject.toml` insufficient_history (before unavailable; after unavailable; transition unknown); `requirements.txt` insufficient_history (before unavailable; after unavailable; transition unknown).
Candidates emitted/rejected/unresolved: 0/0/0.
Accepted-event confidence: `unavailable`.
Source coverage: repository_metadata=`complete` (1/1 succeeded, 0 optional 404), issues=`complete` (1/1 succeeded, 0 optional 404), pull_requests=`complete` (1/1 succeeded, 0 optional 404), commits=`complete` (1/1 succeeded, 0 optional 404), current_manifest_probes=`complete` (1/2 succeeded, 1 optional 404), historical_dependency=`partial` (0/2 succeeded, 0 optional 404), reviewed_candidates=`complete` (0/0 succeeded, 0 optional 404), downstream_releases=`not_collected` (0/0 succeeded, 0 optional 404).
- adoption_readiness: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- observed_adoption: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- migration_friction: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- remediation: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
- recovery_signal: **unknown_insufficient_data** — Required evidence or historical context is incomplete; a negative finding is unsupported.
Missing sources: historical_dependency, downstream_releases.
Unknown stages: adoption_readiness, observed_adoption, migration_friction, remediation, recovery_signal.

## Accepted evidence timeline

Events are ordered by evidence timestamp. Stages are categories, not a required chronological or causal sequence.

No candidate event in this validation case passed the preregistered analyst review criteria. This is not evidence that no event occurred.

## Rejected detector candidates

- `bb4048c374b6b5c34d799903` / `text.version_specific_remediation` / `bot_or_dependency_update_noise`: Analyst review of the collected Dependabot PR #226: the bot proposed widening scrapelib's urllib3 requirement, but the PR was closed without merging and its body does not connect the proposal to a downstream friction event. Copied upstream release notes are not scrapelib remediation. [Collected source](https://github.com/jamesturk/scrapelib/pull/226).
- `e3aebd0869d43caa3aee8e22` / `text.version_specific_friction` / `generic_dependency_mention`: Analyst review of the collected Dependabot PR #226: the PR describes a proposed version-range update, not a concrete failure, incompatible environment, or migration task in scrapelib. The error/fix language belongs to copied upstream urllib3 release notes and does not establish downstream friction. [Collected source](https://github.com/jamesturk/scrapelib/pull/226).

## Denominator-aware cohort metrics

- **core_collection_coverage:** 6/6 (100.0%). Repositories with complete metadata, issues, PRs, and commits / frozen cohort.
- **historical_dependency_evidence_coverage:** 1/6 (16.7%). Repositories with an exact-ref target-package declaration / frozen cohort; not adoption.
- **candidate_emission_coverage:** 1/6 (16.7%). Repositories with at least one emitted candidate / frozen cohort; not impact incidence.
- **accepted_evidence_coverage:** 0/6 (0.0%). Repositories with accepted evidence / frozen cohort; not event incidence.
- **bounded_friction_finding_coverage:** 0/1 (0.0%). Accepted friction evidence / repositories sufficient for a stage-level finding; not ecosystem incidence.

## Unavailable metrics

- observed_adoption_rate: no target-version installation or runtime denominator
- remediation_coverage: no accepted qualifying friction denominator
- recovery_rate: downstream releases not collected and recovery-eligible set undefined

## Missing evidence

- Downstream release collection was not planned; text.support_release had no input.
- Target-version lockfile selection and runtime/CI resolution were not collected.
- Path-scoped historical manifest reconstruction is incomplete for some repositories.

## Limitations

- Cohort selection used current declarations, not proven historical target-version use.
- Path-scoped history can miss earlier declarations and cross-file migrations.
- No qualifying evidence found describes this bounded method, not proof no event occurred.
- Zero emitted candidates does not establish absence of release impact or detector recall.
- Lifecycle stages are evidence categories, not a required chronology or causal chain.
- These frozen convenience cohorts are not ecosystem-representative.
