"""Deterministic dependency-transition classification."""

from __future__ import annotations

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import Version

from pulse.dependencies.models import (
    DependencyObservation,
    DependencyTransition,
    TransitionKind,
)


def detect_transition(
    before: DependencyObservation | None,
    after: DependencyObservation | None,
    *,
    target_version: str,
) -> DependencyTransition | None:
    if before is None and after is None:
        return None
    observed = after or before
    if observed is None:  # pragma: no cover - narrowed above
        raise AssertionError("unreachable")
    if before is None:
        kind = TransitionKind.INTRODUCED
        reason = "The dependency appears in the later inspected manifest."
    elif after is None:
        kind = TransitionKind.REMOVED
        reason = "The dependency is absent from the later inspected manifest."
    elif before.constraint == after.constraint:
        return None
    else:
        accepted_before = _accepts(before.constraint, target_version)
        accepted_after = _accepts(after.constraint, target_version)
        if accepted_before and not accepted_after:
            kind = TransitionKind.TARGET_EXCLUDED
            reason = (
                "The later constraint excludes the target release after previously accepting it."
            )
        elif not accepted_before and accepted_after:
            kind = TransitionKind.TARGET_ACCEPTED
            reason = (
                "The later constraint accepts the target release after previously excluding it."
            )
        else:
            kind = TransitionKind.CONSTRAINT_CHANGED
            reason = (
                "The dependency constraint changed without changing target-release eligibility."
            )
    return DependencyTransition(
        repository=observed.repository,
        package=observed.package,
        before=before,
        after=after,
        target_version=target_version,
        kind=kind,
        reason=reason,
    )


def _accepts(constraint: str, target_version: str) -> bool:
    if not constraint:
        return True
    try:
        return SpecifierSet(constraint).contains(Version(target_version), prereleases=True)
    except InvalidSpecifier:
        return False
