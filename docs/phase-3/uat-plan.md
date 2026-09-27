# Milestone 5 validation and future UAT plan

**Purpose:** check existing PULSE behavior against applicable [requirements](requirements-specification.md) and [rules](business-rules.md), then prepare testable future acceptance scenarios. The current evidence is **existing system acceptance evidence**, primarily automated engineering tests and frozen report replay. It is **not stakeholder UAT, signoff, or acceptance of a finished future product**. [The validation matrix](requirement-validation-matrix.md) keeps the modes separate.

## Scope and roles

**In scope now:** declared cases/cohorts, bounded collection, provenance/capture method, optional versus required source outcomes, immutable snapshot identity and resume, exact-ref uncertainty, candidate/review separation, rejected exclusion, stage sufficiency, UNKNOWN, frozen cohort denominator, unavailable recovery, and deterministic report replay. Evidence is the full 134-test suite plus `python -m uv run python scripts/reproduce_phase2_forensics.py`, which regenerated both Phase 2 frozen reports with no Git diff. Existing tests are reused by exact test name in [cases](uat-test-cases.md); no redundant manual execution is claimed.

**Future-state only:** comprehensive resolved/installed target-version evidence, stronger release-boundary acquisition, provenance-sensitive copied-text origin, explicit source-conflict status, attention/portfolio views, downstream recovery eligibility, fuller unresolved-candidate display, rule-version impact, private-source authorization policy, and human case closure. These receive planned cases but **no PASS for an unimplemented capability**.

**Out of scope:** invented participant acceptance, production-scale tests, future UI, performance SLA without baseline, warehouse/dashboard/frontend work, and actual implementation. Phase 2 convenience cohorts do not support population claims.

| Role | Current responsibility | Boundary |
| --- | --- | --- |
| BA / test analyst (this milestone) | Map requirements, execute repository checks, inspect frozen artifacts, record results and gaps. | Technical/document validation, not stakeholder proxy. |
| Current PULSE system | Execute already implemented Phases 0–2 code and deterministic replay. | No new product behavior added to make an AC pass. |
| Future stakeholder participant — TBD | Later validate decision, language, workflow, priority, burden, and closure criteria. | No participant or approval is asserted now. |

## Entry and exit gates

**Entry:** Milestone 4 baseline, AC, rules, and RTM are present; branch starts clean at `898a4059fdaa5a896538465941187b08bff33a7c`; Phase 2 reports, tests, and four external replay manifests are accessible; frozen inputs are not edited by the validation plan. Source access is local; no live API collection is implied.

**Milestone 5 exit (BA preparation, not stakeholder signoff):** every BR/SR/FR/NFR has one mode and result; every current-system-testable Must maps to a named existing test or replay check; actual checks and any blockers are logged; future Must/Should ACs have planned scenarios; 14 business rules are assessed; zero proposed capability is marked PASS solely for good documentation; respondent-dependent items stay pending; coverage, defects/gaps, and change control are recorded. **Final Phase 3 exit remains blocked** until genuine primary research and reconciliation.

## Execution and status conventions

- `PASS`: the current, bounded behavior named in the UAT case was observed in this run. It does not validate future user value.
- `FAIL`: actual existing behavior contradicted an applicable expected result. None recorded in this run.
- `BLOCKED`: full current-system acceptance cannot be determined because a required artifact, policy, or accepted-event example is absent, or existing behavior is only partial.
- `NOT_IMPLEMENTED`: future capability is intentionally absent; this is a design gap, **not a software defect**.
- `PENDING_STAKEHOLDER`: a real user/owner decision or exercise is necessary.

An individual UAT case can PASS a narrow integrity guard while the corresponding whole requirement remains blocked or stakeholder-dependent. [Validation coverage](validation-coverage.md) reports those denominators separately; no single misleading completion percentage is used. Requirements with multiple concerns retain a full-requirement result in the matrix, not the best result among their individual tests.

## Future execution protocol

After implementation and stakeholder reconciliation, freeze the requirement/AC/RTM version; identify authorized users and representative declared cases; capture preconditions and source access; execute each case against that version; preserve actual output and defect IDs; separate test analyst observations from participant statements; seek explicit signoff only from a real accountable stakeholder. Re-run technical regression after any product change. No future execution or signoff is recorded here.
