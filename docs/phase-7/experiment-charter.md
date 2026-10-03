# Phase 7 evidence-depth experiment charter

Status: **FROZEN BEFORE IMPLEMENTATION**. This charter fixes the experiment boundary. Changes after treatment execution require a new method version and an explicit deviation record; they cannot be used to improve the apparent result.

## 1. Research question

Can a stronger, explicitly governed evidence-acquisition and historical-reconstruction method improve bounded analytical sufficiency on the existing frozen validation cases without weakening provenance, reproducibility, false-positive controls, or uncertainty semantics?

The experiment tests a method, not ecosystem outcomes, product value, or stakeholder demand.

## 2. Frozen population

The population is unchanged from the two published validation investigations:

| Case | Declared members | Approved manifest paths per member | Member-path records |
| --- | ---: | ---: | ---: |
| pytest 8.0.0 | 2 | 2 | 4 |
| urllib3 2.0.0 | 6 | 2 | 12 |
| **Total** | **8** | — | **16** |

The only paths are `pyproject.toml` and `requirements.txt`, already declared in both case files. No repository, release, path, dependency, branch, issue, pull request, or source class may be added after treatment results are observed.

The published baseline remains 2 investigations, 8/8 core-collected members, 40 findings, 38 `UNKNOWN`, 2 bounded NO, 0 supported positive findings, 2 inherited `REJECT` candidates, and 1 shared artifact. Historical context is 1 `PAIRED`, 6 `AFTER_ONLY`, and 9 `UNRESOLVED` member-path records.

## 3. Baseline method

`BASELINE_METHOD = m4-1b-published-validation`

The baseline is the existing path-change method and governed replay:

- historical pairing strategy `manifest_path_first_change`;
- path-history commits restricted to the case observation window;
- latest path change at or before release paired with earliest path change after release;
- published pytest snapshot `08852d5f-9843-5406-a69b-7039ea2ddaa4`;
- published urllib3 snapshot `bd3a02a5-0c2d-5eec-84fd-8e9b93a238a3`;
- rule release `rule-replay-b2b638bb97c8-e10fb03f467e267f`;
- unchanged frozen source evidence, candidates, reviews, findings, and metric outputs.

Baseline results are read-only inputs. Phase 7 will record their file digests before and after the experiment.

## 4. Treatment method

`TREATMENT_METHOD = p7-boundary-anchor-depth-v1`

`RECONSTRUCTION_VERSION = repository-boundary-pair-v1`

`PREREQUISITE_VERSION = p7-question-prerequisites-v1`

For each declared member:

1. Retrieve the latest repository commit at or before the release timestamp using one bounded GitHub REST query.
2. Retrieve the latest repository commit at or before the observation-window end using one bounded GitHub REST query.
3. Require the second anchor to be strictly after release; otherwise the after anchor is structurally unavailable.
4. Retrieve only `pyproject.toml` and `requirements.txt` at both exact refs.
5. Parse each retrieved state with the existing non-executing dependency parsers.
6. Classify each of the 16 member-path records as `PAIRED`, `AFTER_ONLY`, or `UNRESOLVED` from exact-ref source states.
7. Evaluate question-specific prerequisites without changing candidate or review inputs.

The treatment observes repository state at two bounded reference points. It does not claim the path changed at either anchor, determine the exact transition time, infer installation, or infer compatibility. Cross-file declarations may supply repository-level context, but no cross-file transition is inferred unless the evidence contract explicitly supports it; conflicting declarations remain unresolved.

## 5. Allowed source types

- Existing frozen case definitions, Phase 2 history manifests, Phase 2 processed reports, M4.1B replay/publication manifests, and candidate/review evidence, read only.
- Public GitHub REST repository commit metadata for two exact boundary-anchor queries per member.
- Public `raw.githubusercontent.com` file-content responses for two approved paths at no more than two exact refs per member.

Issues, pull requests, releases, check runs, actions logs, package indexes, downstream releases, runtime environments, private sources, repository clones, and general code search are not Phase 7 treatment sources.

## 6. Source policy

- GitHub access uses a Phase 7-bounded public REST collector and records `collector` capture method. A bearer token may be supplied through the existing environment setting, but the frozen workstation has no configured GitHub token; anonymous execution is permitted and must expose any rate-limit stop rather than bypass it.
- Raw responses are immutable, content-addressed in the manifest, and stored separately under `data/raw/phase-7/`.
- Authentication headers and tokens are never persisted.
- Event time is the commit timestamp. Retrieval time is recorded separately and never substituted.
- Exact repository, ref, path, query, method version, run ID, task identity, content digest, outcome, and failure state are required.
- HTTP 404 means the approved path was not found at that exact ref; it does not prove the dependency or repository was absent elsewhere.
- No private or unapproved source may be consulted.

## 7. Evaluation metrics

The experiment uses the definitions in [evaluation-plan.md](evaluation-plan.md): declared/core members, historical state distribution, prerequisite coverage, lifecycle sufficiency, bounded decision availability, finding states, support-link completeness, availability distribution, candidate/review counts, provenance completeness, unresolved reasons, and baseline-to-treatment method delta.

All Phase 7 measures are `EXPERIMENTAL`. No measure is added to the production metric registry in this phase.

## 8. Success criteria

Experimental execution passes only if the frozen method runs on all eight members, applies stop states, produces member-level provenance, preserves baseline artifacts, and supports exact comparison.

The treatment demonstrates a defensible evidence-depth improvement if one or more of these occurs without relaxing a prerequisite or integrity rule:

- an `AFTER_ONLY` or `UNRESOLVED` member-path record becomes a valid exact-ref `PAIRED` record;
- a previously unresolved member obtains a qualifying pre-release target declaration;
- a lifecycle assessment becomes `SUFFICIENT` from newly qualifying evidence;
- an explicit support link can be created for a genuinely supported finding;
- every unresolved record receives a more specific source-availability and stop reason;
- the treatment proves a required source structurally unavailable within the frozen method.

Positive findings, more candidates, and a lower UNKNOWN count are not required. UNKNOWN may decrease only when the treatment supplies qualifying evidence.

## 9. Stop criteria

Evidence acquisition stops for a member/path when the following fixed work is complete or blocked:

- one pre-release boundary-anchor query and one observation-end anchor query;
- at most four exact-ref file requests: two approved paths × two anchors;
- maximum of 3 retries, a 30-second request timeout, and no retry that exceeds a 60-second wait budget;
- no pagination because each anchor query requests one latest commit;
- no alternate branch, tag, parent traversal, path discovery, repository clone, or wider time range;
- a source-policy or authentication failure stops the affected run;
- missing repository anchor yields `STRUCTURALLY_UNAVAILABLE`;
- exact-ref 404 yields `NOT_FOUND` for that file state;
- incomplete or failed API response yields `INCOMPLETE` or `SOURCE_UNAVAILABLE`;
- parser ambiguity or incompatible cross-file declarations yields `CONFLICTING` or `UNRESOLVED`;
- any next step needing private sources or exceeding the two-path/two-anchor boundary is `NOT_PLANNED`.

Repeated searches after these states are prohibited in this method version.

## 10. Publication boundary

Phase 7 writes only separate experimental raw, validation, and processed outputs. It creates no PostgreSQL migration or analytical snapshot, changes no dbt mart, and writes no `PUBLISHED_VALIDATION` or DRAFT row. The baseline database and committed Phase 2/M4.1B artifacts remain unchanged.

Treatment results may be committed as experimental validation evidence with their manifest and hashes. They are not production metrics or replacements for published findings.

## 11. Non-goals

- New cohorts, paths, source classes, candidates, detector rules, UI/API/Power BI work, production monitoring, or cloud deployment.
- Installed-version adoption, runtime compatibility, causal migration, recovery, prevalence, ecosystem impact, ROI, demand, or stakeholder value.
- Exact transition-time reconstruction from boundary snapshots.
- Making the treatment look successful by loosening bounded NO or positive-finding rules.
- Final Portfolio Release.

## 12. Risks

- Boundary commits may not contain either approved path even when another path carried the dependency.
- Repository default-branch history may have changed or become inaccessible.
- A later observation-end snapshot may hide intermediate changes.
- Same-path pairs may increase while target-declaration coverage remains unchanged.
- The two existing cases may favor or disadvantage the treatment and cannot establish transferability.
- More bounded NO findings could be misread as evidence of real-world absence.
- Raw public responses may be larger than expected; the request boundary limits volume.

## 13. Expected outputs

- A versioned treatment implementation and focused regression tests.
- Immutable raw response envelopes and an evaluation run manifest.
- Exact baseline and treatment JSON results with source/stop/provenance fields.
- Required Phase 7 contracts, implementation record, comparison, member log, findings, decision memo, and closure record.
- A final `GO`, `GO_BOUNDED`, `HOLD`, `PIVOT`, or `STOP` decision grounded in the observed treatment result.

`G8 = NOT_YET_VALIDATED` throughout.
