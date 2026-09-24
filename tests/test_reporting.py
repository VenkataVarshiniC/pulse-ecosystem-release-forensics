from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from pulse.analysis.forensics import build_forensics
from pulse.config.cases import load_case
from pulse.models.evidence import (
    Confidence,
    DownstreamEventType,
    EvidenceReference,
    LifecycleStage,
)
from pulse.models.review import EvidenceStatus, ReviewableEvidence
from pulse.reporting import render_forensics_markdown

CASES = Path(__file__).parents[1] / "cases"


def test_generated_report_is_deterministic_and_exposes_trust_boundaries() -> None:
    now = datetime(2026, 9, 24, tzinfo=UTC)
    candidate = ReviewableEvidence(
        candidate_id="report-event-1234",
        case_id="sqlalchemy-2.0.0",
        repository="https://github.com/pandas-dev/pandas",
        occurred_at=datetime(2023, 1, 27, tzinfo=UTC),
        lifecycle_stage=LifecycleStage.MIGRATION_FRICTION,
        event_type=DownstreamEventType.COMPATIBILITY_ISSUE,
        title="SQLAlchemy 2.0 compatibility failure",
        target_package="SQLAlchemy",
        target_release="2.0.0",
        evidence=(
            EvidenceReference(
                url="https://github.com/pandas-dev/pandas/issues/51015",
                observed_at=now,
                source_type="issue",
            ),
        ),
        classification_rule="text.version_specific_friction",
        classification_reason="The source contains exact versions and a reproducible failure.",
        confidence=Confidence.HIGH,
        status=EvidenceStatus.ACCEPTED,
        reviewer_note="Exact versions and stack trace verified.",
        reviewed_at=now,
    )
    result = build_forensics(
        load_case(CASES / "sqlalchemy-2.0.0.yaml"),
        (candidate,),
        repositories_with_sufficient_collection={"pandas-dev/pandas"},
    )

    first = render_forensics_markdown(result)
    second = render_forensics_markdown(result)

    assert first == second
    assert "1 of 2 cohort repositories" in first
    assert "no_qualifying_evidence_found" in first
    assert "unknown_insufficient_data" in first
    assert "0/2" in first
    assert "## Observed adoption" in first
    assert "## Bounded recovery" in first
    assert "https://github.com/pandas-dev/pandas/issues/51015" in first
