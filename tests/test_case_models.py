from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from pulse.config.cases import load_case
from pulse.models.case import CohortRepository, RepositoryCohort
from pulse.models.evidence import (
    Confidence,
    DownstreamEventType,
    EvidenceReference,
    LifecycleStage,
)
from pulse.models.review import EvidenceStatus, ReviewableEvidence

CASES = Path(__file__).parents[1] / "cases"


def test_existing_case_configuration_loads() -> None:
    definition = load_case(CASES / "sqlalchemy-2.0.0.yaml")

    assert definition.case.target_package == "SQLAlchemy"
    assert len(definition.cohort.repositories) == 2
    assert definition.case.case_id == definition.cohort.case_id


def test_cohort_rejects_duplicate_repositories() -> None:
    repository = CohortRepository(
        repository="example/project",
        project_name="Example",
        inclusion_reason="Explicitly supplied for the investigation.",
        selection_confidence=Confidence.HIGH,
    )
    with pytest.raises(ValidationError, match="must be unique"):
        RepositoryCohort(
            cohort_id="duplicates",
            case_id="example-2.0",
            selection_method="explicit",
            selection_rationale="A deliberately invalid duplicate cohort for validation.",
            repositories=(repository, repository),
            created_at=datetime(2026, 9, 24, tzinfo=UTC),
        )


def test_evidence_review_transition_is_explicit_and_terminal() -> None:
    candidate = ReviewableEvidence(
        candidate_id="candidate-123456",
        case_id="example-2.0",
        repository="https://github.com/example/project",
        occurred_at=datetime(2024, 1, 2, tzinfo=UTC),
        lifecycle_stage=LifecycleStage.REMEDIATION,
        event_type=DownstreamEventType.VERSION_PIN,
        title="Constrain example below version 2",
        target_package="example",
        target_release="2.0",
        evidence=(
            EvidenceReference(
                url="https://github.com/example/project/pull/1",
                observed_at=datetime(2026, 9, 24, tzinfo=UTC),
            ),
        ),
        classification_rule="dependency_upper_bound",
        classification_reason="The dependency change adds an upper bound excluding version 2.",
        confidence=Confidence.HIGH,
    )

    accepted = candidate.transition(
        EvidenceStatus.ACCEPTED,
        note="Manifest diff directly supports the classification.",
        reviewed_at=datetime(2026, 9, 24, tzinfo=UTC),
    )

    assert accepted.status is EvidenceStatus.ACCEPTED
    with pytest.raises(ValueError, match="invalid evidence transition"):
        accepted.transition(EvidenceStatus.REJECTED, note="Changed mind")
