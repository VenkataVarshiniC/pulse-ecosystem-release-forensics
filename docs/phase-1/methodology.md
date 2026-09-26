# Phase 1 methodology

## Unit of analysis

The unit is a release, repository, artifact, or evidence event. PULSE does not profile people. A case declares the target package and version, release time, bounded observation window, collection rules, and repository cohort before analysis.

## Collection and provenance

The planner expands a case into stable task IDs for PyPI metadata, GitHub repository metadata, releases, issues, pull requests, commits, and selected dependency files. Collectors run independently; one failure does not discard successful tasks. Each success is stored in a new raw envelope containing the source, query, retrieval time, identifier, and payload. The run manifest retains successes, failures, record counts, and paths.

Every raw envelope also requires a controlled `capture_method`: `collector` for PULSE collector retrieval, `connector_assisted` for evidence obtained with connector assistance, or `fixture` for test data. There is no implicit default when parsing an envelope or constructing a snapshot store. The live CLI explicitly selects `collector`; tests use `fixture`. Existing envelopes must be labeled from known provenance rather than assumed to be collector output. The three committed HTTPX snapshots are `connector_assisted`; replaying them validates downstream processing, not unattended collection. Their payloads and recorded retrieval times are preserved by this metadata correction.

The source registry states supported artifacts. GitHub issue, pull-request, and commit queries use the case window where the API permits it. Historical file contents can be requested at a ref through the GitHub client. Phase 1 parsers support `requirements.txt`, PEP 621 and Poetry sections in `pyproject.toml`, `setup.cfg`, and literal `install_requires` in `setup.py`; repository code is never executed.

## Detection and review

Rules create candidates and record why they fired. Text rules require the exact target package and version plus stage terms. Dependency rules compare typed constraints and can identify an explicit target exclusion or acceptance. Direct constraint transitions may receive high confidence; keyword candidates receive medium confidence and require review.

Candidate, needs-review, accepted, and rejected states are distinct. Terminal decisions require a timestamp and note. Only accepted records become lifecycle events. Candidate IDs hash the case, repository, source, and rule; accepted-event projection deduplicates by that stable ID.

## Interpretation

Repository findings use `yes`, `no_qualifying_evidence_found`, and `unknown_insufficient_data`. Incomplete collection yields unknown rather than no. Every cohort metric publishes its numerator, denominator, window, and qualification rule. Friction is divided by repositories with accepted adoption evidence; remediation by repositories with accepted friction; recovery is omitted unless an eligible denominator is explicitly supplied.

`observed_adoption_evidence_coverage` is the fraction of declared repositories with accepted observed-adoption evidence. It measures the investigation's evidence coverage, not an adoption rate. A value of 0/1 means no accepted adoption evidence for the one declared repository; it does not mean that repository did not adopt. Unknown findings remain unknown. Even sufficient collection with no qualifying evidence is not proof of absence. See [ADR 0006](../decisions/0006-adoption-evidence-coverage.md).

Lifecycle stages are forensic evidence categories, not mandatory steps in a chronological or causal sequence. Timelines sort by evidence timestamps without reordering categories. Compatibility work may anticipate a release, and users of an older downstream version may report friction after a fix ships. For HTTPX 0.28.0, the upstream release and openai-python 1.55.3 compatibility response occurred on 2024-11-28; the later 2024-12-02 issue concerned openai-python 1.54.4. The later report does not cause the earlier fix, and the fix does not establish universal recovery.

Temporal association is not causality. Explicit cohorts describe only their members, and a missing public artifact never proves that no event occurred.
