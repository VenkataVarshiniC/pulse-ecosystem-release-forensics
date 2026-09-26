"""Operational completion is separate from artifact availability."""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest
from pydantic import ValidationError

from pulse.collection.collectors.github import GitHubCollector
from pulse.collection.journal import AttemptRecord, RunJournal
from pulse.collection.manifest import (
    FileProbeAvailability,
    LiveCollectionManifest,
    TaskOutcomeStatus,
)
from pulse.collection.planner import (
    CollectionPlan,
    TaskKind,
    TaskRequirement,
    plan_collection,
)
from pulse.collection.raw import CaptureMethod, RawSnapshotStore
from pulse.collection.runner import CollectionRunner
from pulse.config.cases import load_case
from pulse.github.client import GitHubClient

CASE = Path(__file__).parents[1] / "cases/httpx-0.28.0.yaml"


def setup_run(tmp_path, file_statuses, *, repo_status=200):
    definition = load_case(CASE)
    tasks = plan_collection(definition).tasks
    repo = next(
        task for task in tasks
        if task.kind is TaskKind.GITHUB_REPOSITORY and task.repository == "encode/httpx"
    )
    files = [task for task in tasks if task.kind is TaskKind.GITHUB_FILE]
    selected = [repo, *(task for task in files if task.parameters["path"] in file_statuses)]
    plan = CollectionPlan(case_id=definition.case.case_id, tasks=tuple(selected))
    calls = []

    def handler(request):
        calls.append(request)
        if "/contents/" in request.url.path:
            path = request.url.path.split("/contents/", 1)[1]
            status = file_statuses[path]
        else:
            status = repo_status
        if status == 200:
            return httpx.Response(200, json={"id": len(calls)})
        return httpx.Response(status, json={"message": "fixture response"})

    http = httpx.Client(
        base_url="https://api.github.test", transport=httpx.MockTransport(handler)
    )
    client = GitHubClient("fixture-token", http_client=http, max_retries=0)
    journal = RunJournal(tmp_path / "interim")
    runner = CollectionRunner(
        [GitHubCollector(client)],
        RawSnapshotStore(tmp_path / "raw", capture_method=CaptureMethod.COLLECTOR),
        journal=journal,
    )
    return definition, plan, runner, journal, calls, http


def records(journal, case_id, run_id):
    return [
        AttemptRecord.model_validate_json(path.read_bytes())
        for path in journal.directory(case_id, run_id).glob("*.attempt.json")
    ]


def test_only_file_tasks_can_be_optional():
    definition = load_case(CASE)
    repository = next(
        task for task in plan_collection(definition).tasks
        if task.kind is TaskKind.GITHUB_REPOSITORY
    )
    with pytest.raises(ValidationError, match="Only configured file probes"):
        repository.__class__.model_validate({
            **repository.model_dump(), "requirement": "optional_probe",
        })


def test_optional_missing_files_keep_outcomes_but_complete_run(tmp_path):
    statuses = {
        "pyproject.toml": 200, "requirements.txt": 404,
        "setup.cfg": 404, "setup.py": 404,
    }
    definition, plan, runner, journal, _, http = setup_run(tmp_path, statuses)
    with http:
        manifest = runner.run(definition, plan)
    assert all(task.requirement is TaskRequirement.OPTIONAL_PROBE for task in plan.tasks[1:])
    assert manifest.status == "complete"
    assert manifest.outcome_breakdown["succeeded"] == 2
    assert manifest.outcome_breakdown["not_found"] == 3
    assert manifest.outcome_breakdown["optional_not_found"] == 3
    assert manifest.outcome_breakdown["required_failures"] == 0
    assert manifest.file_probe_availability is FileProbeAvailability.AVAILABLE
    assert manifest.dependency_analysis_sufficiency == "not_assessed"
    missing = [
        item for item in records(journal, definition.case.case_id, manifest.run_id)
        if item.outcome.status is TaskOutcomeStatus.NOT_FOUND
    ]
    assert len(missing) == 3
    assert all(item.task.parameters["path"] in statuses for item in missing)
    assert all(item.capture_method is CaptureMethod.COLLECTOR for item in missing)
    assert all(item.stats.requests[0].status_code == 404 for item in missing)
    assert all(item.outcome.snapshot_path is None for item in missing)
    assert len(list((tmp_path / "raw").rglob("*.json"))) == 2
    serialized = manifest.model_dump(mode="json")
    assert serialized["status"] == "complete"
    assert serialized["outcome_breakdown"]["optional_not_found"] == 3


def test_required_repository_404_prevents_completion(tmp_path):
    definition, plan, runner, _, _, http = setup_run(
        tmp_path, {"pyproject.toml": 404}, repo_status=404
    )
    with http:
        manifest = runner.run(definition, plan)
    assert manifest.status == "failed"
    assert manifest.outcomes[0].status is TaskOutcomeStatus.NOT_FOUND
    assert manifest.outcomes[0].task_id == plan.tasks[0].task_id
    assert manifest.outcome_breakdown["required_failures"] == 1
    assert manifest.outcome_breakdown["optional_not_found"] == 1


def test_manifest_cannot_report_complete_with_a_missing_task_outcome(tmp_path):
    definition, plan, runner, _, _, http = setup_run(
        tmp_path, {"pyproject.toml": 404}
    )
    with http:
        manifest = runner.run(definition, plan)
    payload = manifest.model_dump(mode="json")
    payload["outcomes"] = payload["outcomes"][:1]
    with pytest.raises(ValidationError, match="one outcome per planned task"):
        LiveCollectionManifest.model_validate(payload)


@pytest.mark.parametrize("status,expected", [(429, "rate_limited"), (503, "failed")])
def test_optional_operational_failure_stays_incomplete(tmp_path, status, expected):
    definition, plan, runner, _, _, http = setup_run(
        tmp_path, {"pyproject.toml": status}
    )
    with http:
        manifest = runner.run(definition, plan)
    assert manifest.status == "incomplete"
    assert manifest.outcomes[1].status.value == expected
    assert manifest.outcome_breakdown["required_failures"] == 0
    assert manifest.file_probe_availability is FileProbeAvailability.INCOMPLETE


def test_all_file_probes_404_means_no_current_file_evidence(tmp_path):
    statuses = {path: 404 for path in (
        "pyproject.toml", "requirements.txt", "setup.cfg", "setup.py"
    )}
    definition, plan, runner, _, _, http = setup_run(tmp_path, statuses)
    with http:
        manifest = runner.run(definition, plan)
    assert manifest.status == "complete"
    assert manifest.outcome_breakdown["optional_not_found"] == 4
    assert manifest.file_probe_availability is FileProbeAvailability.NONE_FOUND
    assert manifest.dependency_analysis_sufficiency == "not_assessed"


def test_resume_reuses_verified_optional_404_but_fresh_run_reprobes(tmp_path):
    definition, plan, runner, journal, calls, http = setup_run(
        tmp_path, {"pyproject.toml": 404}
    )
    with http:
        first = runner.run(definition, plan)
        raw = list((tmp_path / "raw").rglob("*.json"))
        original_bytes = {path: path.read_bytes() for path in raw}
        second = runner.run(definition, plan, resume=True)
        assert len(calls) == 2
        third = runner.run(definition, plan)
    assert first.status == second.status == third.status == "complete"
    assert len(calls) == 4
    assert all(path.read_bytes() == data for path, data in original_bytes.items())
    reused = records(journal, definition.case.case_id, second.run_id)
    assert len(reused) == 2
    assert all(item.reused_from_attempt for item in reused)
    assert all(item.stats.requests == [] for item in reused)
    file_attempt = next(item for item in reused if item.task.kind is TaskKind.GITHUB_FILE)
    assert file_attempt.outcome.status is TaskOutcomeStatus.NOT_FOUND
    assert len({first.run_id, second.run_id, third.run_id}) == 3


def test_changing_requirement_keeps_id_but_forces_new_attempt(tmp_path):
    definition, plan, runner, journal, calls, http = setup_run(
        tmp_path, {"pyproject.toml": 404}
    )
    with http:
        first = runner.run(definition, plan)
        required_file = plan.tasks[1].model_copy(update={
            "requirement": TaskRequirement.REQUIRED,
        })
        changed = CollectionPlan(case_id=plan.case_id, tasks=(plan.tasks[0], required_file))
        second = runner.run(definition, changed, resume=True)
    assert first.outcomes[1].task_id == second.outcomes[1].task_id
    assert len(calls) == 3  # The repository was reused; the changed file task was re-probed.
    assert second.status == "incomplete"
    assert second.outcome_breakdown["required_failures"] == 1
    new_file_attempt = next(
        item for item in records(journal, definition.case.case_id, second.run_id)
        if item.task.kind is TaskKind.GITHUB_FILE
    )
    assert new_file_attempt.reused_from_attempt is None
    assert new_file_attempt.stats.requests[0].status_code == 404


def test_modified_optional_404_telemetry_is_not_reused(tmp_path):
    definition, plan, runner, journal, calls, http = setup_run(
        tmp_path, {"pyproject.toml": 404}
    )
    with http:
        first = runner.run(definition, plan)
        record_path = next(
            path for path in journal.directory(definition.case.case_id, first.run_id).glob(
                "*.attempt.json"
            ) if '"status": "not_found"' in path.read_text(encoding="utf-8")
        )
        original = record_path.read_text(encoding="utf-8")
        record_path.write_text(original.replace('"status_code": 404', '"status_code": 200'))
        second = runner.run(definition, plan, resume=True)
    assert second.status == "complete"
    assert len(calls) == 3
    new_file_attempt = next(
        item for item in records(journal, definition.case.case_id, second.run_id)
        if item.task.kind is TaskKind.GITHUB_FILE
    )
    assert new_file_attempt.reused_from_attempt is None
