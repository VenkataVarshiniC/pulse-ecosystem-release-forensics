from __future__ import annotations

from pathlib import Path

import httpx

from pulse import cli
from pulse.collection.journal import AttemptRecord
from pulse.collection.planner import CollectionPlan, TaskKind, plan_collection
from pulse.collection.raw import CaptureMethod, RawSnapshot
from pulse.config.cases import load_case
from pulse.config.settings import Settings
from pulse.github.client import GitHubClient

CASE = Path(__file__).parents[1] / "cases/httpx-0.28.0.yaml"


def test_live_command_without_token_fails_before_creating_any_run(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setattr(cli.Settings, "from_env", lambda: Settings(github_token=None))
    result = cli.main(["collect", str(CASE), "--output-root", str(tmp_path)])
    assert result == 2
    assert "GITHUB_TOKEN is required" in capsys.readouterr().err
    assert not list(tmp_path.iterdir())


def test_cli_collect_and_resume_write_collector_provenance_without_historical_writes(
    tmp_path, monkeypatch,
):
    definition = load_case(CASE)
    task = next(
        task for task in plan_collection(definition).tasks if task.kind is TaskKind.GITHUB_ISSUES
    )
    monkeypatch.setattr(
        cli, "plan_collection",
        lambda _: CollectionPlan(case_id=definition.case.case_id, tasks=(task,)),
    )
    monkeypatch.setattr(cli.Settings, "from_env", lambda: Settings(github_token="fixture-token"))
    calls = []

    def handler(request):
        calls.append(request)
        assert request.headers["Authorization"] == "Bearer fixture-token"
        return httpx.Response(200, json=[])

    with httpx.Client(
        base_url="https://api.github.test", transport=httpx.MockTransport(handler)
    ) as http:
        monkeypatch.setattr(
            cli, "GitHubClient",
            lambda token, **kwargs: GitHubClient(
                token, http_client=http, **kwargs
            ),
        )
        command = ["collect", str(CASE), "--output-root", str(tmp_path)]
        assert cli.main(command) == 0
        assert cli.main([*command, "--resume"]) == 0
    assert len(calls) == 1
    snapshots = list((tmp_path / "data/raw").rglob("*.json"))
    assert len(snapshots) == 1
    snapshot = RawSnapshot.model_validate_json(snapshots[0].read_bytes())
    assert snapshot.capture_method is CaptureMethod.COLLECTOR
    records = [
        AttemptRecord.model_validate_json(path.read_bytes())
        for path in tmp_path.rglob("*.attempt.json")
    ]
    assert len(records) == 2
    assert sum(record.reused_from_attempt is not None for record in records) == 1
    assert all("fixture-token" not in record.model_dump_json() for record in records)
    assert not (tmp_path / "data/interim/httpx-0.28.0/collection-manifest.json").exists()


def test_invalid_collection_limits_fail_before_run_creation(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cli.Settings, "from_env", lambda: Settings(github_token="fixture-token"))
    assert cli.main([
        "collect", str(CASE), "--output-root", str(tmp_path), "--max-pages", "0",
    ]) == 2
    assert "max_pages must be positive" in capsys.readouterr().err
    assert not list(tmp_path.iterdir())
