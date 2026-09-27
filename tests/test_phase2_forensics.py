"""Stage sufficiency and replay checks using a local synthetic collector journal."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from pulse.analysis.forensics import EvidenceState
from pulse.collection.journal import AttemptRecord, case_fingerprint
from pulse.collection.manifest import LiveCollectionManifest, TaskOutcome, TaskOutcomeStatus
from pulse.collection.planner import TaskKind, plan_collection
from pulse.collection.raw import CaptureMethod, RawSnapshotStore
from pulse.collection.telemetry import CollectionStats, RequestRecord
from pulse.config.cases import load_case
from pulse.history.models import (
    HistoricalPathResult,
    HistoricalRefPair,
    HistoricalRun,
    PairStatus,
)
from pulse.models.case import SourceSystem
from pulse.models.evidence import Confidence, LifecycleStage
from pulse.phase2_forensics import (
    Availability,
    _finding,
    _read_collection,
    build_phase2_report,
    render_phase2_markdown,
    validation_summary,
    write_phase2_report,
)

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 1, 1, tzinfo=UTC)


def _artifacts(
    tmp_path: Path,
    case_id: str = "pytest-8.0.0",
    *,
    missing_kind: TaskKind | None = None,
    optional_404: bool = True,
) -> tuple:
    definition = load_case(ROOT / "cases" / f"{case_id}.yaml")
    plan = plan_collection(definition)
    directory = tmp_path / "run"
    directory.mkdir()
    fingerprint = case_fingerprint(definition)
    (directory / "run.json").write_text(
        json.dumps(
            {
                "run_id": "test-run",
                "case_fingerprint": fingerprint,
                "definition": definition.model_dump(mode="json"),
                "plan": plan.model_dump(mode="json"),
            }
        ),
        encoding="utf-8",
    )
    store = RawSnapshotStore(tmp_path / "raw", capture_method=CaptureMethod.COLLECTOR)
    outcomes = []
    used_404 = False
    used_failure = False
    for task in plan.tasks:
        is_404 = optional_404 and task.kind is TaskKind.GITHUB_FILE and not used_404
        is_failure = missing_kind is task.kind and task.repository is not None and not used_failure
        used_404 |= is_404
        used_failure |= is_failure
        status = (
            TaskOutcomeStatus.NOT_FOUND
            if is_404
            else TaskOutcomeStatus.FAILED
            if is_failure
            else TaskOutcomeStatus.SUCCEEDED
        )
        stats = CollectionStats(
            pages_requested=1,
            pages_completed=0 if is_404 or is_failure else 1,
            requests=[RequestRecord(status_code=404 if is_404 else 500 if is_failure else 200)],
            termination="not_found" if is_404 else "failed" if is_failure else "complete",
        )
        attempt_id = f"attempt-{task.task_id}"
        snapshot_path = None
        digest = None
        if status is TaskOutcomeStatus.SUCCEEDED:
            snapshot_path = store.save(
                task, [], NOW, run_id="test-run", attempt_id=attempt_id, stats=stats
            )
            digest = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()
        outcome = TaskOutcome(
            task_id=task.task_id,
            status=status,
            started_at=NOW,
            completed_at=NOW,
            record_count=0,
            snapshot_path=str(snapshot_path) if snapshot_path else None,
        )
        outcomes.append(outcome)
        attempt = AttemptRecord(
            run_id="test-run",
            attempt_id=attempt_id,
            case_fingerprint=fingerprint,
            task=task,
            capture_method=CaptureMethod.COLLECTOR,
            observation_window_start=str(definition.case.observation_window_start),
            observation_window_end=str(definition.case.observation_window_end),
            outcome=outcome,
            stats=stats,
            matching_records=0,
            failure_kind="not_found" if is_404 else "failed" if is_failure else None,
            snapshot_sha256=digest,
        )
        (directory / f"{attempt_id}.attempt.json").write_text(
            attempt.model_dump_json(), encoding="utf-8"
        )
    collection = LiveCollectionManifest(
        run_id="test-run",
        case_id=case_id,
        started_at=NOW,
        completed_at=NOW,
        observation_window_start=str(definition.case.observation_window_start),
        observation_window_end=str(definition.case.observation_window_end),
        planned_tasks=plan.tasks,
        outcomes=tuple(outcomes),
    )
    collection_path = directory / "manifest.json"
    collection_path.write_text(collection.model_dump_json(), encoding="utf-8")
    paths = sorted(
        {
            path
            for rule in definition.case.collection_rules
            if rule.source in {SourceSystem.GITHUB, SourceSystem.REPOSITORY_FILE}
            for path in rule.file_paths
        }
    )
    results = tuple(
        HistoricalPathResult(
            pair=HistoricalRefPair(
                case_id=case_id,
                repository=member.repository,
                manifest_path=path,
                before=None,
                after=None,
                pairing_strategy="test",
                release_timestamp=definition.case.release_timestamp,
                observation_window_start=definition.case.observation_window_start,
                observation_window_end=definition.case.observation_window_end,
                confidence=Confidence.LOW,
                reason="Insufficient path history in fixture.",
                status=PairStatus.INSUFFICIENT_HISTORY,
            ),
            history_stats=CollectionStats(),
        )
        for member in definition.cohort.repositories
        for path in paths
    )
    history = HistoricalRun(
        run_id="test-history",
        case_id=case_id,
        started_at=NOW,
        completed_at=NOW,
        results=results,
    )
    history_path = tmp_path / "history.json"
    history_path.write_text(history.model_dump_json(), encoding="utf-8")
    source_dir = ROOT / "docs/phase-2/evaluation-data"
    baseline = tmp_path / "baseline.jsonl"
    baseline.write_bytes((source_dir / f"baseline-{case_id}.jsonl").read_bytes())
    source_metadata = json.loads(
        (source_dir / f"baseline-{case_id}.manifest.json").read_text(encoding="utf-8")
    )
    source_metadata.update(
        collection_run_id="test-run",
        history_run_id="test-history",
        baseline_sha256=hashlib.sha256(baseline.read_bytes()).hexdigest(),
    )
    baseline_manifest = tmp_path / "baseline.manifest.json"
    baseline_manifest.write_text(json.dumps(source_metadata), encoding="utf-8")
    ledger = tmp_path / "review-ledger.jsonl"
    ledger.write_text(
        "\n".join(
            line
            for line in (source_dir / "review-ledger.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if json.loads(line)["candidate"]["case_id"] == case_id
        ),
        encoding="utf-8",
    )
    return definition, collection_path, history_path, baseline, baseline_manifest, ledger


def test_optional_404_is_complete_but_historical_unknown_remains_unknown(tmp_path: Path) -> None:
    inputs = _artifacts(tmp_path)
    report = build_phase2_report(*inputs)
    assert report.collection_operational_status == "complete"
    assert (
        report.repositories[0].collection_coverage["current_manifest_probes"].state
        is Availability.COMPLETE
    )
    assert (
        sum(
            item.collection_coverage["current_manifest_probes"].optional_not_found
            for item in report.repositories
        )
        == 1
    )
    assert all(
        item.stage_findings[LifecycleStage.MIGRATION_FRICTION.value].state is EvidenceState.UNKNOWN
        for item in report.repositories
    )
    assert report.accepted_events == ()
    assert "No candidate event" in render_phase2_markdown(report)
    assert "remediation_coverage" in " ".join(report.unavailable_metrics)
    assert "bounded_friction_finding_coverage" not in {item.name for item in report.metrics}


def test_zero_candidates_require_stage_sufficiency_for_negative_finding() -> None:
    stage = LifecycleStage.MIGRATION_FRICTION
    assert _finding(stage, (), True).state is EvidenceState.NO_QUALIFYING_EVIDENCE
    assert _finding(stage, (), False).state is EvidenceState.UNKNOWN


def test_required_failure_prevents_negative_finding(tmp_path: Path) -> None:
    inputs = _artifacts(tmp_path, missing_kind=TaskKind.GITHUB_ISSUES)
    report = build_phase2_report(*inputs)
    assert report.collection_operational_status == "incomplete"
    assert report.repositories[0].collection_coverage["issues"].state is Availability.UNAVAILABLE
    assert (
        report.repositories[0].stage_findings[LifecycleStage.MIGRATION_FRICTION.value].state
        is EvidenceState.UNKNOWN
    )


def test_rejected_candidates_never_enter_accepted_ledger(tmp_path: Path) -> None:
    inputs = _artifacts(tmp_path, "urllib3-2.0.0")
    report = build_phase2_report(*inputs)
    assert report.emitted_candidate_count == 2
    assert report.rejected_candidate_count == 2
    assert report.accepted_events == ()
    assert len(report.rejected_candidates) == 2
    assert "Dependabot" in render_phase2_markdown(report)
    json_path, markdown_path = write_phase2_report(report, tmp_path)
    assert json_path.with_name("accepted-evidence.jsonl").read_text(encoding="utf-8") == ""
    before = (json_path.read_bytes(), markdown_path.read_bytes())
    write_phase2_report(build_phase2_report(*inputs), tmp_path)
    assert (json_path.read_bytes(), markdown_path.read_bytes()) == before


def test_case_artifact_mismatch_fails_explicitly(tmp_path: Path) -> None:
    inputs = _artifacts(tmp_path)
    definition, collection_path, history_path, baseline, baseline_manifest, ledger = inputs
    payload = json.loads(history_path.read_text(encoding="utf-8"))
    payload["case_id"] = "urllib3-2.0.0"
    history_path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="history case"):
        build_phase2_report(
            definition, collection_path, history_path, baseline, baseline_manifest, ledger
        )


def test_fingerprint_and_review_identity_are_enforced(tmp_path: Path) -> None:
    inputs = _artifacts(tmp_path, "urllib3-2.0.0")
    definition, collection_path, history_path, baseline, baseline_manifest, ledger = inputs
    run_path = collection_path.parent / "run.json"
    run = json.loads(run_path.read_text(encoding="utf-8"))
    run["case_fingerprint"] = "wrong"
    run_path.write_text(json.dumps(run), encoding="utf-8")
    with pytest.raises(ValueError, match="fingerprint"):
        _read_collection(definition, collection_path)
    run["case_fingerprint"] = case_fingerprint(definition)
    run_path.write_text(json.dumps(run), encoding="utf-8")
    rows = ledger.read_text(encoding="utf-8").splitlines()
    ledger.write_text(rows[0], encoding="utf-8")
    with pytest.raises(ValueError, match="review ledger"):
        build_phase2_report(
            definition, collection_path, history_path, baseline, baseline_manifest, ledger
        )


def test_bounded_summary_has_no_pooled_incidence(tmp_path: Path) -> None:
    pytest_root = tmp_path / "pytest"
    urllib_root = tmp_path / "urllib"
    pytest_root.mkdir()
    urllib_root.mkdir()
    reports = (
        build_phase2_report(*_artifacts(pytest_root)),
        build_phase2_report(*_artifacts(urllib_root, "urllib3-2.0.0")),
    )
    summary = validation_summary(reports)
    assert set(summary["cases"]) == {"pytest-8.0.0", "urllib3-2.0.0"}
    assert "pooled incidence" in summary["scope"]
    assert summary["cases"]["pytest-8.0.0"]["cohort_size"] == 2
    assert summary["cases"]["urllib3-2.0.0"]["cohort_size"] == 6
