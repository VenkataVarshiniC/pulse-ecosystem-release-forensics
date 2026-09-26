from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest

from pulse.collection.collectors.github import GitHubCollector
from pulse.collection.journal import AttemptRecord, RunJournal
from pulse.collection.manifest import TaskOutcomeStatus
from pulse.collection.planner import CollectionPlan, TaskKind, plan_collection
from pulse.collection.raw import CaptureMethod, RawSnapshot, RawSnapshotStore
from pulse.collection.runner import CollectionRunner
from pulse.config.cases import load_case
from pulse.github.client import GitHubClient
from pulse.pipeline import detect_raw_candidates

NOW = datetime(2026, 9, 26, tzinfo=UTC)
CASE = Path(__file__).parents[1] / "cases/httpx-0.28.0.yaml"


def issue(number=1):
    return {
        "id": number, "number": number,
        "html_url": f"https://github.com/openai/openai-python/issues/{number}",
        "title": "httpx 0.28.0 error", "body": "Reported exception",
        "created_at": "2024-12-01T00:00:00Z",
    }


def setup_runner(tmp_path, handler, *, two_tasks=False, max_pages=1000):
    definition = load_case(CASE)
    tasks = plan_collection(definition).tasks
    selected = [next(task for task in tasks if task.kind is TaskKind.GITHUB_ISSUES)]
    if two_tasks:
        selected.insert(0, next(
            task for task in tasks if task.kind is TaskKind.GITHUB_REPOSITORY
        ))
    plan = CollectionPlan(case_id=definition.case.case_id, tasks=tuple(selected))
    http = httpx.Client(base_url="https://api.github.test", transport=httpx.MockTransport(handler))
    client = GitHubClient(
        "fixture-token", http_client=http, max_retries=0, max_pages=max_pages,
    )
    journal = RunJournal(tmp_path / "interim")
    runner = CollectionRunner(
        [GitHubCollector(client)],
        RawSnapshotStore(tmp_path / "raw", capture_method=CaptureMethod.COLLECTOR),
        journal=journal, clock=lambda: NOW,
    )
    return definition, plan, runner, journal, http


def attempts(tmp_path):
    return [
        AttemptRecord.model_validate_json(path.read_text(encoding="utf-8"))
        for path in (tmp_path / "interim").rglob("*.attempt.json")
    ]


def test_partial_failure_resume_preserves_success_and_all_previous_attempts(tmp_path):
    state = {"fail": True, "repo_calls": 0}

    def handler(request):
        if not request.url.path.endswith("/issues"):
            state["repo_calls"] += 1
            return httpx.Response(200, json={"id": 123})
        if request.url.params.get("page") == "2":
            return httpx.Response(503) if state["fail"] else httpx.Response(200, json=[issue()])
        return httpx.Response(
            200, json=[issue()],
            headers={"Link": f'<{request.url.copy_set_param("page", "2")}>; rel="next"'},
        )

    definition, plan, runner, journal, http = setup_runner(tmp_path, handler, two_tasks=True)
    with http:
        first = runner.run(definition, plan)
        original_bytes = {
            path: path.read_bytes() for path in tmp_path.rglob("*.json")
        }
        assert first.status == "incomplete"
        assert first.outcomes[1].status is TaskOutcomeStatus.PARTIAL
        partial = next(item for item in attempts(tmp_path) if item.failure_kind)
        assert partial.stats.pages_requested == 2
        assert partial.stats.pages_completed == 1
        assert partial.matching_records == 1
        assert partial.failure_kind == "failed"
        state["fail"] = False
        second = runner.run(definition, plan, resume=True)
        third = runner.run(definition, plan, resume=True)

    assert second.status == third.status == "complete"
    assert len({first.run_id, second.run_id, third.run_id}) == 3
    assert state["repo_calls"] == 1
    assert all(path.read_bytes() == original for path, original in original_bytes.items())
    records = attempts(tmp_path)
    assert len(records) == 6
    assert len({item.attempt_id for item in records}) == 6
    assert sum(item.reused_from_attempt is not None for item in records) == 3
    assert all(
        record.matching_records == 1
        for record in records
        if record.task.kind is TaskKind.GITHUB_ISSUES
        and record.outcome.status is TaskOutcomeStatus.SUCCEEDED
    )
    snapshots = list((tmp_path / "raw").rglob("*.json"))
    assert len(snapshots) == 3
    for path in snapshots:
        snapshot = RawSnapshot.model_validate_json(path.read_bytes())
        assert snapshot.capture_method is CaptureMethod.COLLECTOR
        assert snapshot.attempt_id and snapshot.run_id
    assert len(detect_raw_candidates(definition, tmp_path / "raw")) == 1
    assert journal.successful(definition).keys() == {task.task_id for task in plan.tasks}


def test_zero_matches_are_persisted_with_window_counts_and_query(tmp_path):
    definition, plan, runner, _, http = setup_runner(
        tmp_path, lambda _: httpx.Response(200, json=[
            {**issue(), "created_at": "2020-01-01T00:00:00Z"},
            {**issue(2), "pull_request": {}},
        ])
    )
    with http:
        manifest = runner.run(definition, plan)
    record = attempts(tmp_path)[0]
    assert record.stats.records_examined == 2
    assert record.matching_records == 0
    assert record.stats.pages_completed == 1
    assert record.outcome.status is TaskOutcomeStatus.SUCCEEDED
    assert record.task.repository == "openai/openai-python"
    assert record.task.parameters["since"] == "2024-10-28"
    assert record.observation_window_end == "2025-02-28"
    assert RawSnapshot.model_validate_json(
        Path(manifest.outcomes[0].snapshot_path).read_bytes()
    ).payload == []


@pytest.mark.parametrize("status,kind", [
    (401, "unauthorized"), (404, "not_found"), (429, "rate_limited"), (500, "failed"),
])
def test_task_failure_taxonomy_is_persisted_without_secrets(tmp_path, status, kind):
    definition, plan, runner, _, http = setup_runner(
        tmp_path, lambda _: httpx.Response(
            status, headers={"X-RateLimit-Remaining": "0"},
            json={"message": "fixture-token"},
        )
    )
    with http:
        result = runner.run(definition, plan)
    record = attempts(tmp_path)[0]
    assert result.status == "failed"
    assert record.outcome.status.value == kind
    assert record.failure_kind == kind
    assert record.stats.requests[0].remaining == 0
    assert record.outcome.snapshot_path is None
    assert "fixture-token" not in record.model_dump_json()


@pytest.mark.parametrize("damage", ["deleted", "modified"])
def test_resume_does_not_reuse_missing_or_modified_snapshot(tmp_path, damage):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(200, json=[issue()])

    definition, plan, runner, _, http = setup_runner(tmp_path, handler)
    with http:
        first = runner.run(definition, plan)
        path = Path(first.outcomes[0].snapshot_path)
        if damage == "deleted":
            path.unlink()
        else:
            path.write_text("{}", encoding="utf-8")
        assert runner.run(definition, plan, resume=True).status == "complete"
    assert len(calls) == 2


def test_repeated_fresh_runs_do_not_duplicate_logical_evidence(tmp_path):
    definition, plan, runner, _, http = setup_runner(
        tmp_path, lambda _: httpx.Response(200, json=[issue()])
    )
    with http:
        first = runner.run(definition, plan)
        second = runner.run(definition, plan)
    assert first.outcomes[0].task_id == second.outcomes[0].task_id
    assert first.outcomes[0].snapshot_path != second.outcomes[0].snapshot_path
    assert len(list((tmp_path / "raw").rglob("*.json"))) == 2
    assert len(detect_raw_candidates(definition, tmp_path / "raw")) == 1


def test_resume_uses_checkpoint_even_without_completed_run_manifest(tmp_path):
    definition, plan, runner, journal, http = setup_runner(
        tmp_path, lambda _: httpx.Response(200, json=[issue()])
    )
    with http:
        first = runner.run(definition, plan)
        journal.directory(definition.case.case_id, first.run_id).joinpath("manifest.json").unlink()
        second = runner.run(definition, plan, resume=True)
    assert first.outcomes[0].snapshot_path == second.outcomes[0].snapshot_path
    assert attempts(tmp_path)[-1].outcome.status is TaskOutcomeStatus.SUCCEEDED


def test_changed_case_definition_does_not_reuse_prior_success(tmp_path):
    definition, plan, runner, _, http = setup_runner(
        tmp_path, lambda _: httpx.Response(200, json=[issue()])
    )
    with http:
        first = runner.run(definition, plan)
        changed_cohort = definition.cohort.model_copy(update={
            "selection_rationale": "A changed rationale must invalidate prior case reuse.",
        })
        changed = definition.model_copy(update={"cohort": changed_cohort})
        second = runner.run(changed, plan, resume=True)
    assert first.outcomes[0].snapshot_path != second.outcomes[0].snapshot_path


def test_partial_zero_record_page_is_retained_and_retried(tmp_path):
    definition, plan, runner, _, http = setup_runner(
        tmp_path, lambda request: httpx.Response(
            200, json=[],
            headers={"Link": f'<{request.url.copy_set_param("page", "2")}>; rel="next"'},
        ), max_pages=1,
    )
    with http:
        first = runner.run(definition, plan)
        second = runner.run(definition, plan, resume=True)
    assert first.status == second.status == "incomplete"
    assert first.outcomes[0].status is TaskOutcomeStatus.PARTIAL
    assert first.outcomes[0].record_count == 0
    assert len(list((tmp_path / "raw").rglob("*.json"))) == 2
    assert all(item.stats.termination == "page_limit" for item in attempts(tmp_path))


def test_raw_hash_in_checkpoint_matches_snapshot(tmp_path):
    definition, plan, runner, _, http = setup_runner(
        tmp_path, lambda _: httpx.Response(200, json=[])
    )
    with http:
        runner.run(definition, plan)
    record = attempts(tmp_path)[0]
    assert record.snapshot_sha256 == hashlib.sha256(
        Path(record.outcome.snapshot_path).read_bytes()
    ).hexdigest()
