from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from pulse.analysis.forensics import EvidenceState, build_forensics
from pulse.config.cases import load_case
from pulse.models.evidence import (
    Confidence,
    DownstreamEventType,
    EvidenceReference,
    LifecycleStage,
)
from pulse.models.review import EvidenceStatus, ReviewableEvidence

CASES = Path(__file__).parents[1] / "cases"
NOW = datetime(2026, 9, 24, tzinfo=UTC)


def accepted_candidate(
    candidate_id: str, repository: str, stage: LifecycleStage
) -> ReviewableEvidence:
    return ReviewableEvidence(
        candidate_id=candidate_id,
        case_id="sqlalchemy-2.0.0",
        repository=f"https://github.com/{repository}",
        occurred_at=datetime(2023, 2, 1, tzinfo=UTC),
        lifecycle_stage=stage,
        event_type=DownstreamEventType.COMPATIBILITY_ISSUE,
        title=f"Accepted {stage.value} evidence",
        target_package="SQLAlchemy",
        target_release="2.0.0",
        evidence=(
            EvidenceReference(
                url=f"https://github.com/{repository}/issues/1",
                observed_at=NOW,
                source_type="issue",
            ),
        ),
        classification_rule="fixture.direct_evidence",
        classification_reason="The fixture represents direct version-specific primary evidence.",
        confidence=Confidence.HIGH,
        status=EvidenceStatus.ACCEPTED,
        reviewer_note="Accepted for the engine behavior test.",
        reviewed_at=NOW,
    )


def test_forensics_uses_only_accepted_evidence_and_exposes_denominators() -> None:
    definition = load_case(CASES / "sqlalchemy-2.0.0.yaml")
    events = (
        accepted_candidate(
            "adoption-123456", "pandas-dev/pandas", LifecycleStage.OBSERVED_ADOPTION
        ),
        accepted_candidate(
            "friction-123456", "pandas-dev/pandas", LifecycleStage.MIGRATION_FRICTION
        ),
        accepted_candidate("remediate-12345", "pandas-dev/pandas", LifecycleStage.REMEDIATION),
    )

    result = build_forensics(
        definition,
        events,
        repositories_with_sufficient_collection={"pandas-dev/pandas"},
    )

    metrics = {item.name: item for item in result.metrics}
    assert metrics["observed_adoption_coverage"].numerator == 1
    assert metrics["observed_adoption_coverage"].denominator == 2
    assert metrics["friction_incidence"].denominator == 1
    assert "bounded_recovery_coverage" not in metrics


def test_repository_summary_distinguishes_no_evidence_from_unknown() -> None:
    definition = load_case(CASES / "sqlalchemy-2.0.0.yaml")

    result = build_forensics(
        definition,
        (),
        repositories_with_sufficient_collection={"pandas-dev/pandas"},
    )

    summaries = {item.repository: item for item in result.repositories}
    assert (
        summaries["pandas-dev/pandas"].migration_friction.state
        is EvidenceState.NO_QUALIFYING_EVIDENCE
    )
    assert (
        summaries["pallets-eco/flask-sqlalchemy"].migration_friction.state
        is EvidenceState.UNKNOWN
    )


def test_accepted_event_projection_deduplicates_stable_candidate_ids() -> None:
    definition = load_case(CASES / "sqlalchemy-2.0.0.yaml")
    candidate = accepted_candidate(
        "duplicate-123456", "pandas-dev/pandas", LifecycleStage.MIGRATION_FRICTION
    )

    result = build_forensics(
        definition,
        (candidate, candidate),
        repositories_with_sufficient_collection={"pandas-dev/pandas"},
    )

    assert len(result.accepted_events) == 1
