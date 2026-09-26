from pathlib import Path

from pulse.analysis.forensics import EvidenceState, build_forensics
from pulse.collection.raw import CaptureMethod, RawSnapshot
from pulse.config.cases import load_case
from pulse.models.evidence import LifecycleStage
from pulse.models.review import CollectionObservation, EvidenceStatus
from pulse.pipeline import apply_review_decisions, detect_raw_candidates, load_review_decisions
from pulse.reporting import render_forensics_markdown


def test_preserved_validation_snapshots_produce_reviewed_candidates() -> None:
    definition = load_case(Path("cases/httpx-0.28.0.yaml"))
    candidates = detect_raw_candidates(definition, Path("data/raw/httpx-0.28.0"))

    assert {item.classification_rule for item in candidates} == {
        "text.version_specific_friction",
        "text.version_specific_remediation",
    }

    reviewed = apply_review_decisions(
        candidates,
        load_review_decisions(Path("data/interim/httpx-0.28.0/review-decisions.json")),
    )
    assert sum(item.status is EvidenceStatus.ACCEPTED for item in reviewed) == 2
    assert sum(item.status is EvidenceStatus.REJECTED for item in reviewed) == 1

    result = build_forensics(
        definition, reviewed, repositories_with_sufficient_collection=set()
    )
    assert [item.lifecycle_stage for item in result.accepted_events] == [
        LifecycleStage.REMEDIATION, LifecycleStage.MIGRATION_FRICTION
    ]
    assert result.accepted_events[0].occurred_at < result.accepted_events[1].occurred_at
    assert result.repositories[0].observed_adoption.state is EvidenceState.UNKNOWN
    report = render_forensics_markdown(result)
    assert "observed_adoption_evidence_coverage" in report
    assert "not an adoption rate" in report
    assert "not a required chronological or causal sequence" in report


def test_httpx_capture_provenance_is_connector_assisted() -> None:
    paths = sorted(Path("data/raw/httpx-0.28.0").rglob("*.json"))
    assert len(paths) == 3
    for path in paths:
        snapshot = RawSnapshot.model_validate_json(path.read_text(encoding="utf-8"))
        assert snapshot.capture_method is CaptureMethod.CONNECTOR_ASSISTED


def test_validation_search_observations_are_typed_and_bounded() -> None:
    path = Path("data/interim/httpx-0.28.0/collection-observations.jsonl")
    observations = [
        CollectionObservation.model_validate_json(line)
        for line in path.read_text(encoding="utf-8").splitlines()
    ]

    assert len(observations) == 3
    assert all(item.completed_at >= item.started_at for item in observations)
    assert all(item.matching_records <= item.records_examined for item in observations)
