"""Focused semantics and replay tests for the frozen Phase 7 experiment."""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from pulse.collection.raw import CaptureMethod, RawSnapshot
from pulse.config.cases import load_case
from pulse.dependencies.parsers import parse_dependency_file_with_diagnostics
from pulse.phase7_depth import (
    ALLOWED_CASES,
    ALLOWED_PATHS,
    PREREQUISITE_VERSION,
    RECONSTRUCTION_VERSION,
    TREATMENT_METHOD,
    AnchorRole,
    ExactRefFileState,
    FindingState,
    HistoryState,
    Phase7RunManifest,
    SourceAvailability,
    StopReason,
    _history_state,
    _Response,
    _target_declarations,
    baseline_paths,
    collect_phase7,
    evaluate_phase7,
    verify_replay,
    write_evaluation,
)

ROOT = Path(__file__).resolve().parents[1]


class FrozenPublicSource:
    """A complete bounded public-source fixture with no extra discovery."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, str] | None]] = []

    def get(self, url: str, *, params: dict[str, str] | None = None) -> _Response:
        self.calls.append((url, params))
        if url.startswith("https://api.github.com/"):
            assert params is not None
            until = datetime.fromisoformat(params["until"])
            sha = hashlib.sha1(  # noqa: S324 - stable fixture identity, not security
                f"{url}|{params['until']}".encode()
            ).hexdigest()
            body = [{
                "sha": sha,
                "commit": {"committer": {"date": until.astimezone(UTC).isoformat()}},
            }]
            return _Response(200, json.dumps(body).encode(), 0)
        target = "pytest" if any(
            name in url for name in ("bsc-wdc/qdislib", "planetlabs/cosmolog")
        ) else "urllib3"
        content = (
            f'[project]\ndependencies = ["{target}>=1"]\n'.encode()
            if url.endswith("pyproject.toml")
            else b""
        )
        return _Response(200, content, 0)


def _copy_governed_inputs(destination: Path) -> None:
    for source in baseline_paths(ROOT):
        target = destination / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


@pytest.fixture
def completed_experiment(tmp_path: Path) -> tuple[Path, Path, FrozenPublicSource]:
    _copy_governed_inputs(tmp_path)
    source = FrozenPublicSource()
    manifest = collect_phase7(tmp_path, client=source)  # type: ignore[arg-type]
    evaluation = evaluate_phase7(manifest, root=tmp_path)
    output = write_evaluation(evaluation, root=tmp_path)
    return manifest, output, source


def _state(availability: SourceAvailability) -> ExactRefFileState:
    return ExactRefFileState(
        repository="example/repo",
        path="pyproject.toml",
        anchor_role=AnchorRole.PRE_RELEASE,
        ref=None,
        event_time=None,
        availability=availability,
        source_attempt_id="task",
    )


def test_historical_state_preserves_absence_and_unavailability() -> None:
    state, reason, stop = _history_state(
        _state(SourceAvailability.NOT_FOUND),
        _state(SourceAvailability.AVAILABLE),
    )
    assert state is HistoryState.AFTER_ONLY
    assert reason
    assert stop is StopReason.PATH_NOT_FOUND_AT_REF

    state, reason, stop = _history_state(
        _state(SourceAvailability.INCOMPLETE),
        _state(SourceAvailability.AVAILABLE),
    )
    assert state is HistoryState.UNRESOLVED
    assert reason
    assert stop is StopReason.PARSE_INCOMPLETE


def test_conflicting_declarations_are_explicit() -> None:
    definition = load_case(ROOT / "cases/pytest-8.0.0.yaml")
    observations, _ = parse_dependency_file_with_diagnostics(
        repository="example/repo",
        file_path="pyproject.toml",
        content=(
            '[project]\ndependencies = ["pytest<8"]\n'
            '[project.optional-dependencies]\ntest = ["pytest>=8"]\n'
        ),
        commit_reference="a" * 40,
        observed_at=definition.case.release_timestamp,
        source=f"https://github.com/example/repo/blob/{'a' * 40}/pyproject.toml",
    )
    declarations, conflicting = _target_declarations(
        observations, definition.case.target_package
    )
    assert len(declarations) == 2
    assert not conflicting  # Different declaration groups can coexist.

    duplicate = (observations[0], observations[0].model_copy(
        update={"constraint": ">=8", "raw_requirement": "pytest>=8"}
    ))
    _, conflicting = _target_declarations(duplicate, "pytest")
    assert conflicting


def test_collection_is_bounded_and_carries_collector_provenance(
    completed_experiment: tuple[Path, Path, FrozenPublicSource],
) -> None:
    manifest_path, _, source = completed_experiment
    manifest = Phase7RunManifest.model_validate_json(manifest_path.read_text())
    assert len(source.calls) == 48
    assert sum("api.github.com" in url for url, _ in source.calls) == 16
    assert sum("raw.githubusercontent.com" in url for url, _ in source.calls) == 32
    assert len(manifest.attempts) == 48
    assert {item.case_id for item in manifest.attempts} == set(ALLOWED_CASES)
    assert {item.path for item in manifest.attempts if item.path} == set(ALLOWED_PATHS)
    for attempt in manifest.attempts:
        snapshot = RawSnapshot.model_validate_json(
            (manifest_path.parents[4] / attempt.raw_path).read_text()
        )
        assert snapshot.capture_method is CaptureMethod.COLLECTOR


def test_treatment_version_and_population_are_isolated(
    completed_experiment: tuple[Path, Path, FrozenPublicSource],
) -> None:
    manifest_path, _, _ = completed_experiment
    payload: dict[str, Any] = json.loads(manifest_path.read_text())
    assert payload["treatment_method"] == TREATMENT_METHOD
    assert payload["reconstruction_version"] == RECONSTRUCTION_VERSION
    assert payload["prerequisite_version"] == PREREQUISITE_VERSION
    payload["treatment_method"] = "old-method"
    with pytest.raises(ValidationError, match="method version"):
        Phase7RunManifest.model_validate(payload)
    payload = json.loads(manifest_path.read_text())
    payload["attempts"].pop()
    with pytest.raises(ValidationError, match="exactly 48"):
        Phase7RunManifest.model_validate(payload)


def test_baseline_is_exact_and_treatment_only_changes_qualified_states(
    completed_experiment: tuple[Path, Path, FrozenPublicSource],
) -> None:
    _, output, _ = completed_experiment
    result = json.loads(output.read_text())
    assert result["baseline"]["declared_members"] == 8
    assert result["baseline"]["history_states"] == {
        "PAIRED": 1,
        "AFTER_ONLY": 6,
        "UNRESOLVED": 9,
    }
    assert result["baseline"]["sufficient"] == 2
    assert result["baseline"]["insufficient"] == 38
    assert result["baseline"]["findings"] == {
        "YES": 0,
        "NO_QUALIFYING_EVIDENCE_FOUND": 2,
        "UNKNOWN": 38,
    }
    assert result["treatment"]["history_states"] == {
        "PAIRED": 16,
        "AFTER_ONLY": 0,
        "UNRESOLVED": 0,
    }
    assert result["treatment"]["sufficient"] == 16
    assert result["treatment"]["insufficient"] == 24
    assert result["treatment"]["findings"] == {
        "YES": 0,
        "NO_QUALIFYING_EVIDENCE_FOUND": 16,
        "UNKNOWN": 24,
    }


def test_unknown_and_bounded_no_prerequisites_remain_distinct(
    completed_experiment: tuple[Path, Path, FrozenPublicSource],
) -> None:
    _, output, _ = completed_experiment
    result = json.loads(output.read_text())
    assessments = result["assessments"]
    adoption = [item for item in assessments if item["question"] == "observed_adoption"]
    friction = [item for item in assessments if item["question"] == "migration_friction"]
    assert {item["finding"] for item in adoption} == {FindingState.UNKNOWN.value}
    assert all(not item["prerequisites"][0]["satisfied"] for item in adoption)
    assert {item["finding"] for item in friction} == {
        FindingState.NO_QUALIFYING_EVIDENCE_FOUND.value
    }
    assert all(all(p["satisfied"] for p in item["prerequisites"]) for item in friction)


def test_positive_support_link_metric_is_unavailable_at_zero_denominator(
    completed_experiment: tuple[Path, Path, FrozenPublicSource],
) -> None:
    _, output, _ = completed_experiment
    result = json.loads(output.read_text())
    metric = next(item for item in result["metrics"] if item["metric_id"] == "P7-M05")
    assert metric["numerator"] is None
    assert metric["denominator"] == 0
    assert metric["value"] is None
    assert metric["status"] == "UNAVAILABLE_ZERO_DENOMINATOR"


def test_candidate_reviews_and_shared_artifact_are_invariant(
    completed_experiment: tuple[Path, Path, FrozenPublicSource],
) -> None:
    _, output, _ = completed_experiment
    result = json.loads(output.read_text())
    expected = {"candidates": 2, "accepted": 0, "rejected": 2, "distinct_artifacts": 1}
    assert result["baseline"]["candidates"] == expected
    assert result["treatment"]["candidates"] == expected
    assert result["candidate_invariant"] is True


def test_offline_replay_is_deterministic(
    completed_experiment: tuple[Path, Path, FrozenPublicSource],
) -> None:
    manifest, output, _ = completed_experiment
    verify_replay(manifest, output, root=manifest.parents[4])
    assert evaluate_phase7(manifest, root=manifest.parents[4]) == evaluate_phase7(
        manifest, root=manifest.parents[4]
    )


def test_baseline_digest_drift_stops_evaluation(
    completed_experiment: tuple[Path, Path, FrozenPublicSource],
) -> None:
    manifest, _, _ = completed_experiment
    root = manifest.parents[4]
    baseline = root / "data/processed/phase-2/pytest-8.0.0/forensics.json"
    baseline.write_text(baseline.read_text() + "\n")
    with pytest.raises(ValueError, match="baseline digest drift"):
        evaluate_phase7(manifest, root=root)
