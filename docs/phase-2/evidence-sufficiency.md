# Milestone 5 evidence sufficiency

The Phase 2 `pulse forensics` path reads the frozen case definition, a live collection run, a historical run, a SHA-256-verified first-pass candidate baseline, and the independent analyst review ledger. It never asks an analyst to mark a repository complete. The legacy Phase 1 `pulse analyze --complete-repository` path remains available for its historical replay; Phase 2 reports do not use that flag.

## Input identity and provenance

The collection `run.json` must contain the exact case definition, SHA-256 case fingerprint, and collection plan regenerated from the case. Its manifest must match the case ID, window, run ID, and ordered tasks. Each task outcome must have exactly one attempt record in that run. Successful snapshots must pass the journal's SHA-256, collector provenance, task/query, attempt, and run checks. Verified optional current-file 404s count as completed probes, not discovered dependencies. The historical run must contain exactly the configured repository/path pairs, with matching case, release boundary, and window. Historical file-state provenance is checked by the Milestone 4 contextual model. The baseline hash and candidate IDs are verified; its recorded collection and historical run IDs must match. Review rows must cover each baseline candidate exactly once without altering its detector fields, target package/version, cohort repository, or event window. A mismatch fails the command.

`pulse forensics cases/pytest-8.0.0.yaml --baseline-manifest docs/phase-2/evaluation-data/baseline-pytest-8.0.0.manifest.json --review-ledger docs/phase-2/evaluation-data/review-ledger.jsonl` generates one report. The urllib3 case uses its corresponding case and baseline manifest. `uv run python scripts/reproduce_phase2_forensics.py` generates both reports and the cross-case summary in one command, without network calls. The frozen baseline manifests refer to external Milestone 4 collector roots; those roots must be present for re-analysis. Committed analytical JSON and Markdown remain readable if the disposable roots are unavailable later.

## Typed source availability

Each repository has separate coverage for metadata, issues, pull requests, commits, current manifest probes, historical reconstruction, reviewed candidates, and downstream releases. `complete` means all planned collection tasks for that category succeeded, or optional current-file probes returned a verified 404. It does **not** mean an event or dependency exists. `partial` means some evidence exists but a required path or task is incomplete. `unavailable` means planned tasks yielded no completed evidence. `not_collected` means no task was planned. Downstream repository releases are `not_collected` because the planner only collected upstream releases.

Historical context is distinct from path completeness. `historically_supported` means at least one parsed exact-ref manifest declares the target package. Other configured paths can still be partial. This does not establish installation or use of the target version. `historically_unknown` preserves missing anchors, invalid file states, and incomplete path history. A current 404 cannot resolve history. Path-scoped history may miss a declaration last changed before the window, and PULSE does not infer cross-file migration.

Reviewed-candidate coverage is `complete` when every **emitted** candidate has a terminal analyst outcome, including when the detector emitted zero. It is `partial` if one remains unresolved. This category does not measure detector recall. Rejected candidates remain in detector-quality output and never enter the accepted evidence ledger.

## Stage decisions

Accepted qualifying evidence gives `YES` for its stage, regardless of a separate historical manifest gap. With no accepted event, the current bounded rules are:

| Stage | Negative-finding prerequisite | Otherwise |
| --- | --- | --- |
| Adoption readiness | No negative rule: compatible declarations, tests, and CI are not comprehensively collected. | `UNKNOWN` |
| Observed adoption | No negative rule: target-version lockfile selection and ordinary runtime/CI resolution are not comprehensively collected. | `UNKNOWN` |
| Migration friction | Complete repository metadata, issues, PRs, commits, and emitted-candidate review, plus at least one direct exact-ref historical package declaration. | `UNKNOWN` |
| Remediation | Same bounded public-artifact and historical support threshold as friction. | `UNKNOWN` |
| Recovery signal | No negative rule: downstream releases were not collected and no recovery-eligible set is defined. | `UNKNOWN` |

When a friction or remediation negative prerequisite is met, the finding is `NO QUALIFYING EVIDENCE FOUND`: PULSE completed those stage sources in the declared window and found no **accepted** event. It does not prove the event did not happen, that the target version was installed, or that the detector found every relevant artifact. An unresolved historical context makes a negative finding `UNKNOWN` even if issue/PR/commit collection succeeded. A required collection failure also makes it `UNKNOWN`. A verified optional current-file 404 does not by itself cause a required-source failure.

## Denominators

Core collection coverage, historical declaration evidence coverage, candidate emission coverage, and accepted evidence coverage use the frozen case cohort as denominator and state exactly what their numerators count. None is an adoption or impact rate. A bounded friction finding metric is emitted only for repositories meeting the friction stage sufficiency threshold; it is not ecosystem incidence. Observed-adoption rate, remediation coverage without accepted friction, and recovery rate are explicitly unavailable. No zero denominator is rendered as 0%. The two convenience cohorts are reported separately and are not pooled into an ecosystem statistic.

The accepted evidence ledger is written to `data/processed/phase-2/<case>/accepted-evidence.jsonl`; it is valid and empty for both Milestone 4 cases. Generated JSON and Markdown retain stable ordering and omit runtime generation timestamps. Their lifecycle timeline can be empty without hiding zero candidates, rejected candidates, or uncollected sources.
