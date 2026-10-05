# Moderator-only ground-truth reference

**Do not provide this document to participants before or during the task.** It records the governed published-baseline interpretation and is not a script for coaching.

## Selected population

### Primary pytest case

- Case: pytest 8.0.0; published snapshot `08852d5f-9843-5406-a69b-7039ea2ddaa4`.
- Observation window: 2023-12-28 through 2024-05-26.
- Declared population: `bsc-wdc/qdislib` and `planetlabs/cosmolog` only.
- Findings: 10 total; 8 UNKNOWN; 2 bounded NO; 0 positive.
- Candidates: 0.
- `bsc-wdc/qdislib`: five UNKNOWN findings. Historical context is unresolved; downstream releases were not collected.
- `planetlabs/cosmolog`: UNKNOWN for adoption readiness, observed adoption, and recovery signal; bounded NO for migration friction and remediation. Its `pyproject.toml` has a qualifying exact-ref pair, while other evidence remains incomplete.

### Focused urllib3 candidate extension

- Case: urllib3 2.0.0; published snapshot `bd3a02a5-0c2d-5eec-84fd-8e9b93a238a3`.
- Observation window: 2023-03-27 through 2023-08-24.
- Declared population: `atenreiro/opensquat`, `jamesturk/scrapelib`, `wimglenn/advent-of-code-data`, `Aiven-Open/pghoard`, `facundoolano/feedi`, and `enzet/map-machine`.
- Findings: 30 UNKNOWN; 0 bounded NO; 0 positive.
- `jamesturk/scrapelib`: two detector candidates, two inherited REJECT decisions, zero accepted evidence. Both firings reference one captured Dependabot pull-request artifact containing copied upstream text.

## Allowed interpretations

- UNKNOWN means the question remains unanswered because qualifying prerequisites are incomplete.
- Bounded NO means that, within the declared evidence scope and sufficient method for that question, no qualifying evidence was found. It does not establish real-world absence.
- The pytest bounded NO findings apply only to migration friction and remediation for `planetlabs/cosmolog` in the published baseline.
- Complete core collection can coexist with incomplete analytical sufficiency.
- A paired declaration establishes historical declaration context, not installed target version, adoption, compatibility, remediation completion, or recovery.
- Lifecycle categories are evidence questions and need not occur in chronological or causal order.

## Provenance expectations

The participant can inspect source type/provider, repository ref, capture method, content digest, task/run context, source event time, and retrieval time. Current findings have no explicit support edge; the interface says not to infer one from category or status. Available evidence remains inspectable, but it cannot be silently promoted to finding support.

For the selected urllib3 artifact, capture method is `collector`, source event time is unavailable, and retrieval time is recorded. Retrieval time is not event time. One artifact’s collector method does not establish unattended collection for every other artifact.

## Candidate and review semantics

- Candidate firing != accepted finding.
- Two candidate firings from one artifact != two independent source incidents.
- `INHERITED REJECT` means a prior governed decision is reused; it is not a new decision by the participant or current snapshot.
- REJECT excludes the candidate from accepted evidence under the review rule. It does not prove that no migration friction occurred.
- The published snapshot is immutable and review write is disabled.

## Known evidence gaps

- No qualified installed/resolved target-version source or runtime denominator.
- Incomplete exact-ref history for several paths and repositories.
- Downstream release evidence was not collected and recovery eligibility is undefined.
- No positive finding with a complete finding-specific support chain.
- No accepted urllib3 candidate and no product-observed decision outcome.

## Prohibited conclusions

The cases do not support claims that:

- adoption occurred or did not occur;
- compatibility succeeded;
- migration friction was absent in reality;
- remediation or recovery completed;
- a declaration proves installation;
- a rejected candidate proves no event;
- retrieval time is event time;
- the cohorts represent an ecosystem;
- PULSE changes decisions, saves time, or is adopted.

Phase 7 treatment adds experimental historical depth and bounded decisions for some urllib3 members. It is not the authoritative published result in this pilot and must not be presented as such.
