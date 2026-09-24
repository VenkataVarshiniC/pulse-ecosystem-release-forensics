from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pulse.collection.planner import TaskKind, plan_collection
from pulse.collection.raw import RawSnapshotStore
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
