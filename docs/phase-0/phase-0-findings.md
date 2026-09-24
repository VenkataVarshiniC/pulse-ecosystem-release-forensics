# Phase 0 findings

## Final decision: PIVOT

Public evidence supports curated, repository-bounded release forensics for declared downstream cohorts. It does not support the original broader implication of exhaustive ecosystem monitoring. The work should pivot to that narrower analytical claim before any Phase 1 proposal.

The earlier NumPy result was a **qualified GO to Phase 0B**. It showed that one unusually well-documented release could be reconstructed and justified cross-case validation. It was not a general product GO.

## Cross-case result

NumPy 2.0, Pydantic 2.0, and SQLAlchemy 2.0 consistently expose strong release, migration-friction, and remediation evidence. Pydantic confirms that the method is useful for a pure-Python API migration. SQLAlchemy confirms that a defensible named-repository reconstruction is possible without a central compatibility tracker.

The method does not consistently observe ordinary adoption. Compatibility declarations usually show readiness, not use. Unbiased downstream discovery remains unresolved, and ecosystem recovery cannot be inferred from patch releases, closed issues, or selected success stories. The [comparison](cross-case-comparison.md) records the evidence and biases case by case.

## Validated scope

- Preserve accepted events in a typed, source-auditable ledger.
- Reconstruct timelines for named releases and explicitly selected downstream repositories.
- Distinguish release, readiness, observed adoption, friction, remediation, and bounded recovery signals.
- Publish confidence, repository-selection rules, time windows, and missing evidence.
- Make release-associated claims while reserving causal language for evidence that demonstrates a mechanism.

## Scope that remains unvalidated

- Exhaustive or unbiased discovery of downstream repositories.
- Population-level adoption rates from public repository or package metadata.
- Ecosystem-wide recovery without a declared denominator and qualifying event.
- Cross-ecosystem portability beyond the tested Python/PyPI cases.
- Automated causal attribution or fully automated lifecycle classification.

## Unresolved risks

- Search and API behavior can make historical discovery hard to reproduce.
- Public repositories overrepresent projects that expose issue and CI history.
- Analyst-selected cohorts can overrepresent successful migrations.
- Mutable or deleted source artifacts weaken future audits.
- Different dependency formats will require explicit adapters and validation.

## Gate for a future Phase 1 proposal

A future proposal must adopt the narrower scope, define repository inclusion before collection, retain negative searches, and declare cohort denominators before using recovery language. It should be rejected or revised if it again implies ecosystem-wide coverage from purposive public evidence.

Phase 0B ends with this decision. No Phase 1 product implementation is included.
