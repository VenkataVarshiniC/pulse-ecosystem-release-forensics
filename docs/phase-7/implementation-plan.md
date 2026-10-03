# Phase 7 evidence-depth implementation plan

This plan implements the frozen [experiment charter](experiment-charter.md) and [evaluation plan](evaluation-plan.md). It was written before implementation code.

## Minimal architecture

Add one isolated Phase 7 module and one command script. Reuse the current case loader, immutable raw-envelope writer, dependency parsers, candidate/review baseline, and processed Phase 2 reports. Keep all Phase 7 source and derived outputs under Phase 7-specific paths.

No API, frontend, Power BI, PostgreSQL, dbt, published snapshot, or current Phase 2/M4.1B replay component needs modification.

## Model changes

Add Phase 7-local typed models for:

- method and evaluation-run identity;
- source availability and stop reason;
- boundary anchors and source attempts;
- exact-ref file states;
- member-path history comparison;
- question prerequisite evaluation;
- finding/support status;
- experimental metric result;
- aggregate experiment result and immutable run manifest.

Do not change the existing `PairStatus`, published finding enums, or database schema. The treatment output maps to published terminology without becoming a published record.

## Collector changes

Do not alter the general collection plan or add a broad collector. The Phase 7 module will reuse `RawSnapshotStore`, existing telemetry concepts, and retry/error semantics while adding a treatment-local public GitHub source client to execute exactly:

- two `per_page=1` GitHub REST repository-commit anchor requests per member;
- up to four `raw.githubusercontent.com` exact-ref file requests per member;
- only `pyproject.toml` and `requirements.txt`;
- existing retry, timeout, rate-limit, and origin controls.

The source client accepts an optional environment-backed bearer token for API anchors and otherwise runs anonymously within the same fixed request boundary. Each successful or failed/blocked attempt receives a stable task ID and immutable raw envelope. No token or response header is persisted; a rate-limit response stops rather than triggers a different acquisition method.

## Reconstruction changes

Implement a Phase 7-local `repository-boundary-pair-v1` strategy:

- latest commit at or before release;
- latest commit at or before observation-window end, required to be later than release;
- exact-ref retrieval and parsing for both allowed paths;
- `PAIRED`, `AFTER_ONLY`, or `UNRESOLVED` classification;
- explicit availability and stop reasons;
- no alternate branch, path search, or transition-time inference.

The existing Phase 2 history engine remains unchanged and is the baseline comparator.

## Rule and prerequisite changes

Add no detector rule and change no candidate/review rule. Add Phase 7 experimental prerequisite contracts for the five existing lifecycle questions:

- migration friction and remediation require complete existing core/review inputs plus a valid paired pre-release target declaration for bounded NO eligibility;
- positive findings still require accepted qualifying evidence and a support link;
- adoption readiness, observed adoption, and recovery remain UNKNOWN because Phase 7 does not collect their required source types.

The contracts will be represented in code and [evidence-prerequisite-contracts.md](evidence-prerequisite-contracts.md). They are not added to the production metric registry.

## Migrations

None. Phase 7 must not write the local PostgreSQL database or create an analytical snapshot.

## Analytics changes

Create a deterministic evaluator that:

- reads baseline states/findings from committed Phase 2/M4.1B artifacts;
- reads Phase 7 source attempts from an immutable run manifest;
- reconstructs treatment history and question assessments;
- verifies candidate/review/artifact invariance;
- computes the eight experimental measures;
- writes exact JSON to `data/processed/phase-7/` and a validation manifest to `data/validation/phase-7/`;
- supports an offline `replay MANIFEST --expected EVALUATION` mode with no network access;
- refuses baseline digest drift or out-of-population/member/path input.

Documentation values will be generated from or checked against this JSON.

## Tests

Add focused tests for:

- exact release/observation-end anchor selection;
- after anchor strictly later than release;
- fixed two-query/four-file boundary and no pagination;
- paired, after-only, unresolved, unavailable, incomplete, conflicting, and not-planned states;
- exact-ref parser and target declaration preservation;
- prerequisite evaluation and controlled reasons;
- UNKNOWN preservation for adoption/recovery and failed history;
- bounded NO eligibility only under complete prerequisites;
- positive finding blocked without accepted evidence/support;
- candidate/review identity invariance;
- baseline digest/population isolation;
- treatment method/run version isolation;
- deterministic offline replay;
- stop criteria and virtual attempts for structurally unavailable sources.

Run the full Python regression suite because the implementation adds executable core-package logic. Ruff must pass. No dbt or migration test is needed unless this plan changes; any such deviation must be documented before execution.

## Output safety

- Read and hash every baseline input before treatment.
- Write new files exclusively; never replace an existing run directory.
- Store live raw envelopes under `data/raw/phase-7/` and commit the bounded run used for evaluation.
- Store only Phase 7 experimental outputs under `data/processed/phase-7/` and `data/validation/phase-7/`.
- After execution, verify all baseline input digests and the two published snapshot identifiers remain unchanged.
- Scan committed files for credentials and unrelated changes.

## Planned implementation files

- `src/pulse/phase7_depth.py`
- `scripts/run_phase7_depth.py`
- `tests/test_phase7_depth.py`
- required Phase 7 documentation and generated experimental evidence paths

Any additional implementation file requires a documented reason. No major subsystem is authorized.
