# Phase 2 Milestone 5 — End-to-end validation

**Result: PASS for report integration.** Both frozen cases replay through the same manifest-verified workflow without recollection or analyst-entered completeness flags. Most lifecycle findings remain unknown because historical context or source types are missing. This is not a final Phase 2 decision.

| Case | Frozen cohort | Core collection | Historical declaration evidence | Candidates / accepted / rejected | Zero-candidate repositories |
| --- | ---: | --- | --- | --- | ---: |
| [pytest-8.0.0](generated/pytest-8.0.0-forensics.md) | 2 | 2/2 (complete) | 1/2 | 0 / 0 / 0 | 2 |
| [urllib3-2.0.0](generated/urllib3-2.0.0-forensics.md) | 6 | 6/6 (complete) | 1/6 | 2 / 0 / 2 | 5 |

The two cohorts are convenience validation sets. Their counts are not pooled into an ecosystem incidence statistic. Historical declaration evidence is not target-version adoption.

## Stage sufficiency and reportability

### pytest-8.0.0

- `adoption_readiness`: sufficient 0/2; YES 0, NO QUALIFYING EVIDENCE 0, UNKNOWN 2.
- `observed_adoption`: sufficient 0/2; YES 0, NO QUALIFYING EVIDENCE 0, UNKNOWN 2.
- `migration_friction`: sufficient 1/2; YES 0, NO QUALIFYING EVIDENCE 1, UNKNOWN 1.
- `remediation`: sufficient 1/2; YES 0, NO QUALIFYING EVIDENCE 1, UNKNOWN 1.
- `recovery_signal`: sufficient 0/2; YES 0, NO QUALIFYING EVIDENCE 0, UNKNOWN 2.
- Accepted evidence timeline: empty; no candidate passed review.
- Zero-candidate repositories: `bsc-wdc/qdislib`, `planetlabs/cosmolog`.
- Missing sources: Downstream release collection was not planned; text.support_release had no input. Target-version lockfile selection and runtime/CI resolution were not collected. Path-scoped historical manifest reconstruction is incomplete for some repositories.
- Unavailable metrics:
  - observed_adoption_rate: no target-version installation or runtime denominator
  - remediation_coverage: no accepted qualifying friction denominator
  - recovery_rate: downstream releases not collected and recovery-eligible set undefined

### urllib3-2.0.0

- `adoption_readiness`: sufficient 0/6; YES 0, NO QUALIFYING EVIDENCE 0, UNKNOWN 6.
- `observed_adoption`: sufficient 0/6; YES 0, NO QUALIFYING EVIDENCE 0, UNKNOWN 6.
- `migration_friction`: sufficient 0/6; YES 0, NO QUALIFYING EVIDENCE 0, UNKNOWN 6.
- `remediation`: sufficient 0/6; YES 0, NO QUALIFYING EVIDENCE 0, UNKNOWN 6.
- `recovery_signal`: sufficient 0/6; YES 0, NO QUALIFYING EVIDENCE 0, UNKNOWN 6.
- Accepted evidence timeline: empty; no candidate passed review.
- Zero-candidate repositories: `atenreiro/opensquat`, `wimglenn/advent-of-code-data`, `Aiven-Open/pghoard`, `facundoolano/feedi`, `enzet/map-machine`.
- Missing sources: Downstream release collection was not planned; text.support_release had no input. Target-version lockfile selection and runtime/CI resolution were not collected. Path-scoped historical manifest reconstruction is incomplete for some repositories.
- Unavailable metrics:
  - observed_adoption_rate: no target-version installation or runtime denominator
  - remediation_coverage: no accepted qualifying friction denominator
  - recovery_rate: downstream releases not collected and recovery-eligible set undefined
  - bounded_friction_finding_coverage: no repository has sufficient stage evidence

## Reproduction and interpretation

Run `uv run python scripts/reproduce_phase2_forensics.py` from the repository root while the Milestone 4 external collector roots are available. The script verifies the case fingerprint, exact task plan, run IDs, windows, snapshot hashes, baseline hash, and review-to-candidate identity, then rewrites deterministic reports. It makes no API calls. The committed baseline manifests contain the external paths.

A verified optional current-file 404 completes that probe but provides no dependency declaration. Historical path gaps remain unknown; current declarations do not prove historical target-version use. The planner collected upstream releases but no downstream releases, so recovery is unknown and `text.support_release` had no input. No target-version lockfile selection or runtime resolution was collected.

`NO QUALIFYING EVIDENCE` means complete required stage sources and review found no accepted event under this bounded method. It does not prove the event did not occur. Zero emitted candidates likewise does not establish no impact or detector recall. The two urllib3 rule firings from one Dependabot PR remain rejected detector output, not accepted lifecycle events.

See [evidence sufficiency](evidence-sufficiency.md) and the [machine-readable summary](evaluation-data/end-to-end-validation.json).
