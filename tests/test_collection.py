from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from pulse.collection.planner import TaskKind, plan_collection
from pulse.collection.raw import CaptureMethod, RawSnapshot, RawSnapshotStore
from pulse.collection.runner import CollectionRunner
from pulse.config.cases import load_case

CASES = Path(__file__).parents[1] / "cases"
PROJECT_ROOT = Path(__file__).parents[1]


class FakeCollector:
    def supports(self, kind: TaskKind) -> bool:
        return True

    def collect(self, task):  # type: ignore[no-untyped-def]
        if task.kind is TaskKind.GITHUB_RELEASES:
            raise RuntimeError("simulated unavailable source")
        return [{"task": task.task_id}]


class MemoryStore:
    def __init__(self) -> None:
        self.paths: list[Path] = []

    def save(self, task, payload: Any, retrieved_at: datetime) -> Path:  # type: ignore[no-untyped-def]
        path = Path(f"memory/{task.task_id}.json")
        self.paths.append(path)
        return path


def test_planner_is_deterministic_and_time_bounds_downstream_queries() -> None:
    definition = load_case(CASES / "sqlalchemy-2.0.0.yaml")

    first = plan_collection(definition)
    second = plan_collection(definition)

    assert first == second
    assert len(first.tasks) == 19
    issues = next(task for task in first.tasks if task.kind is TaskKind.GITHUB_ISSUES)
    assert issues.parameters == {"since": "2022-12-26", "until": "2023-09-30"}


def test_runner_preserves_successes_and_reports_partial_failure() -> None:
    definition = load_case(CASES / "sqlalchemy-2.0.0.yaml")
    plan = plan_collection(definition)
    now = datetime(2026, 9, 24, tzinfo=UTC)
    store = MemoryStore()
    runner = CollectionRunner([FakeCollector()], store, clock=lambda: now)

    manifest = runner.run(definition, plan)

    assert manifest.status == "incomplete"
    assert manifest.failures == 1
    assert manifest.successes == len(plan.tasks) - 1
    assert len(store.paths) == manifest.successes


def test_raw_snapshots_never_silently_overwrite() -> None:
    definition = load_case(CASES / "sqlalchemy-2.0.0.yaml")
    task = plan_collection(definition).tasks[0]
    now = datetime(2026, 9, 24, tzinfo=UTC)
    written: set[Path] = set()

    def write_exclusive(path: Path, _: str) -> None:
        if path in written:
            raise FileExistsError(path)
        written.add(path)

    store = RawSnapshotStore(
        Path("raw"),
        capture_method=CaptureMethod.FIXTURE,
        prepare_directory=lambda _: None,
        write_exclusive=write_exclusive,
    )
    store.save(task, {"version": "2.0.0"}, now)

    try:
        store.save(task, {"version": "2.0.0"}, now)
    except FileExistsError:
        pass
    else:
        raise AssertionError("a duplicate raw snapshot should not overwrite the first")


@pytest.mark.parametrize("method", list(CaptureMethod))
def test_raw_capture_method_survives_serialization(method: CaptureMethod) -> None:
    task = plan_collection(load_case(CASES / "sqlalchemy-2.0.0.yaml")).tasks[0]
    written: list[str] = []
    store = RawSnapshotStore(
        Path("raw"),
        capture_method=method,
        prepare_directory=lambda _: None,
        write_exclusive=lambda _, content: written.append(content),
    )
    store.save(task, {"version": "2.0.0"}, datetime(2026, 9, 24, tzinfo=UTC))

    snapshot = RawSnapshot.model_validate_json(written[0])
    assert snapshot.capture_method is method
    assert snapshot.model_dump(mode="json")["capture_method"] == method.value


@pytest.mark.parametrize("method", [None, "unspecified"])
def test_raw_capture_method_cannot_be_missing_or_uncontrolled(method: str | None) -> None:
    path = next((PROJECT_ROOT / "data/raw/httpx-0.28.0").rglob("*.json"))
    payload = RawSnapshot.model_validate_json(path.read_text(encoding="utf-8")).model_dump()
    if method is None:
        del payload["capture_method"]
    else:
        payload["capture_method"] = method
    with pytest.raises(ValidationError, match="capture_method"):
        RawSnapshot.model_validate(payload)
