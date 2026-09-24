from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from pulse.models.evidence import (
    Confidence,
    DownstreamEvent,
    DownstreamEventType,
    EvidenceReference,
)


def reference() -> EvidenceReference:
    return EvidenceReference(
        url="https://github.com/example/project/pull/1",
        observed_at=datetime(2026, 9, 24, tzinfo=UTC),
    )


def test_high_confidence_requires_a_specific_reason() -> None:
    with pytest.raises(ValidationError, match="specific rationale"):
        DownstreamEvent(
            repository="https://github.com/example/project",
            occurred_at=datetime(2024, 6, 17, tzinfo=UTC),
            event_type=DownstreamEventType.DEPENDENCY_UPGRADE,
            title="Upgrade dependency",
            target_package="numpy",
            target_release="2.0.0",
            evidence=(reference(),),
            confidence=Confidence.HIGH,
            evidence_reason="Exact diff.",
        )


def test_event_preserves_evidence_and_reason() -> None:
    event = DownstreamEvent(
        repository="https://github.com/example/project",
        occurred_at=datetime(2024, 6, 17, tzinfo=UTC),
        event_type=DownstreamEventType.DEPENDENCY_UPGRADE,
        title="Upgrade dependency",
        target_package="numpy",
        target_release="2.0.0",
        evidence=(reference(),),
        confidence=Confidence.HIGH,
        evidence_reason="The dependency manifest changes from NumPy 1.x to 2.0.0.",
    )

    assert event.evidence[0].url.host == "github.com"
    assert event.confidence is Confidence.HIGH
