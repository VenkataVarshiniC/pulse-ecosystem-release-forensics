from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from pulse.config.cases import load_case
from pulse.dependencies.parsers import parse_dependency_file
from pulse.dependencies.transitions import detect_transition
from pulse.evidence.detectors import (
    ArtifactType,
    TextArtifact,
    detect_text_candidates,
    detect_transition_candidate,
)
from pulse.models.evidence import Confidence, LifecycleStage
from pulse.models.review import EvidenceStatus

CASES = Path(__file__).parents[1] / "cases"
NOW = datetime(2026, 9, 24, tzinfo=UTC)


def test_issue_detection_requires_package_version_and_explains_rule() -> None:
    case = load_case(CASES / "sqlalchemy-2.0.0.yaml").case
    artifact = TextArtifact(
        repository="pandas-dev/pandas",
        artifact_type=ArtifactType.ISSUE,
        source_url="https://github.com/pandas-dev/pandas/issues/51015",
        source_identifier="issue:51015",
        title="SQLAlchemy 2.0.0 compatibility failure",
        body="read_sql raises an error after the migration.",
        occurred_at=datetime(2023, 1, 27, tzinfo=UTC),
        observed_at=NOW,
    )

    candidates = detect_text_candidates(case, artifact)

    friction = next(
        item for item in candidates if item.lifecycle_stage is LifecycleStage.MIGRATION_FRICTION
    )
    assert friction.status is EvidenceStatus.NEEDS_REVIEW
    assert friction.confidence is Confidence.MEDIUM
    assert friction.classification_rule == "text.version_specific_friction"


def test_keyword_match_without_exact_version_is_not_candidate_evidence() -> None:
    case = load_case(CASES / "sqlalchemy-2.0.0.yaml").case
    artifact = TextArtifact(
        repository="example/project",
        artifact_type=ArtifactType.ISSUE,
        source_url="https://github.com/example/project/issues/1",
        source_identifier="issue:1",
        title="SQLAlchemy compatibility failure",
        occurred_at=NOW,
        observed_at=NOW,
    )

    assert detect_text_candidates(case, artifact) == ()


def test_direct_constraint_transition_can_be_high_confidence_candidate() -> None:
    case = load_case(CASES / "pydantic-2.0.yaml").case
    before = parse_dependency_file(
        repository="PrefectHQ/prefect",
        file_path="requirements.txt",
        content="pydantic>=1.10",
        commit_reference="before",
        observed_at=NOW,
        source="https://github.com/PrefectHQ/prefect/blob/before/requirements.txt",
    )[0]
    after = parse_dependency_file(
        repository="PrefectHQ/prefect",
        file_path="requirements.txt",
        content="pydantic>=1.10,<2",
        commit_reference="after",
        observed_at=NOW,
        source="https://github.com/PrefectHQ/prefect/blob/after/requirements.txt",
    )[0]
    transition = detect_transition(before, after, target_version="2.0")
    assert transition is not None

    candidate = detect_transition_candidate(case, transition)

    assert candidate is not None
    assert candidate.confidence is Confidence.HIGH
    assert candidate.evidence[0].source_type == "repository_file"
