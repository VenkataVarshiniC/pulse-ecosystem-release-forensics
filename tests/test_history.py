"""Historical pairing and exact-ref collection behavior."""

from __future__ import annotations

import base64
from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest

from pulse.config.cases import load_case
from pulse.dependencies.parsers import parse_dependency_file_with_diagnostics
from pulse.github.client import GitHubClient
from pulse.github.errors import GitHubApiError
from pulse.history.models import ChangeStatus, FileStateStatus, PairStatus
from pulse.history.pairing import select_ref_pair
from pulse.history.runner import HistoricalRunner

CASE = load_case(Path("cases/httpx-0.28.0.yaml"))
BEFORE = "a" * 40
AFTER = "b" * 40


def commit(sha: str, when: str) -> dict:
    return {"sha": sha, "commit": {"committer": {"date": when}}}


def content(value: str) -> dict:
    data = value.encode()
    return {
        "type": "file", "encoding": "base64",
        "content": base64.b64encode(data).decode(), "size": len(data),
    }


def client(handler) -> GitHubClient:
    transport = httpx.MockTransport(handler)
    http = httpx.Client(base_url="https://api.github.com", transport=transport)
    return GitHubClient("fixture-token", http_client=http, backoff_seconds=0)


def test_pairing_boundaries_and_uncertainty() -> None:
    repo, path = "openai/openai-python", "pyproject.toml"
    records = [
        commit("c" * 40, "2024-10-27T00:00:00Z"),
        commit(BEFORE, "2024-11-28T14:53:00Z"),
        commit(AFTER, "2024-11-29T00:00:00Z"),
        commit("d" * 40, "2025-03-01T00:00:00Z"),
    ]
    pair = select_ref_pair(CASE, repo, path, records)
    assert pair.status is PairStatus.PAIRED
    assert pair.before.commit_sha == BEFORE
    assert pair.after.commit_sha == AFTER
    assert select_ref_pair(CASE, repo, path, records[:2]).status is PairStatus.MISSING_AFTER
    assert select_ref_pair(CASE, repo, path, records[2:3]).status is PairStatus.MISSING_BEFORE
    assert select_ref_pair(CASE, repo, path, records[:1]).status is PairStatus.INSUFFICIENT_HISTORY
    tied = [*records, commit("e" * 40, "2024-11-29T00:00:00Z")]
    assert select_ref_pair(CASE, repo, path, tied).status is PairStatus.AMBIGUOUS
    malformed = [*records, {"sha": "bad"}]
    assert select_ref_pair(CASE, repo, path, malformed).status is PairStatus.AMBIGUOUS


@pytest.mark.parametrize(
    ("path", "text"),
    [
        ("requirements.txt", "HTTPX >=0.27,<1"),
        ("pyproject.toml", '[project]\ndependencies = ["HTTPX >=0.27,<1"]'),
        ("setup.cfg", "[options]\ninstall_requires =\n    HTTPX >=0.27,<1"),
        ("setup.py", 'setup(install_requires=["HTTPX >=0.27,<1"])'),
    ],
)
def test_historical_parser_provenance_without_execution(path: str, text: str) -> None:
    observations, unparsed = parse_dependency_file_with_diagnostics(
        repository="example/repo", file_path=path, content=text,
        commit_reference=BEFORE, observed_at=datetime.now(UTC),
        source=f"https://github.com/example/repo/blob/{BEFORE}/{path}",
    )
    assert not unparsed
    assert len(observations) == 1
    assert observations[0].package == "httpx"
    assert observations[0].raw_requirement == "HTTPX >=0.27,<1"
    assert observations[0].declared_package == "HTTPX"


@pytest.mark.parametrize(
    ("old", "new", "expected"),
    [
        ("httpx>=0.28", "httpx<0.28", ChangeStatus.TARGET_EXCLUDED),
        ("httpx<0.28", "httpx>=0.28", ChangeStatus.TARGET_ACCEPTED),
        ("httpx>=0.27", "httpx>=0.26", ChangeStatus.CONSTRAINT_CHANGED),
        ("httpx>=0.27", "httpx>=0.27", ChangeStatus.UNCHANGED),
        ("other>=1", "httpx>=0.27", ChangeStatus.INTRODUCED),
        ("httpx>=0.27", "other>=1", ChangeStatus.REMOVED),
    ],
)
def test_exact_ref_collection_classifies_manifest_changes(
    tmp_path: Path, old: str, new: str, expected: ChangeStatus,
) -> None:
    seen: list[tuple[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/commits"):
            assert request.url.params["path"] in {
                "requirements.txt", "pyproject.toml", "setup.py", "setup.cfg"
            }
            if request.url.params["path"] == "requirements.txt":
                return httpx.Response(200, json=[
                    commit(BEFORE, "2024-11-27T00:00:00Z"),
                    commit(AFTER, "2024-11-29T00:00:00Z"),
                ])
            return httpx.Response(200, json=[])
        sha = request.url.params["ref"]
        seen.append((request.url.path, sha))
        return httpx.Response(200, json=content(old if sha == BEFORE else new))

    run, manifest = HistoricalRunner(client(handler), tmp_path).run(CASE)
    result = next(item for item in run.results if item.pair.manifest_path == "requirements.txt")
    assert result.change_status is expected
    assert result.pair.status is PairStatus.PAIRED
    assert result.before_state.capture_method.value == "collector"
    assert result.before_state.content_sha256
    assert result.before_state.raw_snapshot_path
    assert {sha for _, sha in seen} == {BEFORE, AFTER}
    assert all("requirements.txt" in path for path, _ in seen)
    assert manifest.exists()


def test_paginated_history_and_historical_file_after_current_404(tmp_path: Path) -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(str(request.url))
        if request.url.path.endswith("/commits"):
            if request.url.params["path"] != "requirements.txt":
                return httpx.Response(200, json=[])
            if request.url.params.get("page") == "2":
                return httpx.Response(200, json=[commit(BEFORE, "2024-11-27T00:00:00Z")])
            next_url = str(request.url.copy_set_param("page", "2"))
            return httpx.Response(
                200, json=[commit(AFTER, "2024-11-29T00:00:00Z")],
                headers={"Link": f'<{next_url}>; rel="next"'},
            )
        if "ref" not in request.url.params:
            return httpx.Response(404)
        return httpx.Response(200, json=content("httpx>=0.27"))

    api = client(handler)
    with pytest.raises(GitHubApiError) as exc:
        api.contents("openai/openai-python", "requirements.txt")
    assert exc.value.failure_kind == "not_found"
    run, _ = HistoricalRunner(api, tmp_path).run(CASE)
    result = next(item for item in run.results if item.pair.manifest_path == "requirements.txt")
    assert result.pair.status is PairStatus.PAIRED
    assert result.history_stats.pages_completed == 2
    assert result.change_status is ChangeStatus.UNCHANGED
    content_urls = [url for url in seen if "/contents/" in url]
    assert sum("ref=" not in url for url in content_urls) == 1
    assert {sha for sha in (BEFORE, AFTER) if any(f"ref={sha}" in url for url in content_urls)} == {
        BEFORE, AFTER,
    }


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        (None, PairStatus.FILE_UNAVAILABLE),
        ({"type": "file", "encoding": "none"}, PairStatus.MALFORMED),
        (content("-r other.txt\nhttpx>=0.27"), PairStatus.MALFORMED),
        (content("httpx>=0.27\nhttpx<0.28"), PairStatus.AMBIGUOUS),
    ],
)
def test_missing_or_uncertain_exact_ref_never_proves_absence(
    tmp_path: Path, payload: dict | None, expected: PairStatus,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/commits"):
            if request.url.params["path"] != "requirements.txt":
                return httpx.Response(200, json=[])
            return httpx.Response(200, json=[
                commit(BEFORE, "2024-11-27T00:00:00Z"),
                commit(AFTER, "2024-11-29T00:00:00Z"),
            ])
        if request.url.params["ref"] == AFTER:
            return httpx.Response(404) if payload is None else httpx.Response(200, json=payload)
        return httpx.Response(200, json=content("httpx>=0.27"))

    run, _ = HistoricalRunner(client(handler), tmp_path).run(CASE)
    result = next(item for item in run.results if item.pair.manifest_path == "requirements.txt")
    assert result.pair.status is expected
    assert result.change_status is ChangeStatus.UNKNOWN
    assert result.transition is None
    if payload is None:
        assert result.after_state.status is FileStateStatus.NOT_FOUND


def test_incomplete_pagination_does_not_select_anchor(tmp_path: Path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.params.get("page") == "2":
            return httpx.Response(500)
        next_url = str(request.url.copy_set_param("page", "2"))
        return httpx.Response(
            200, json=[commit(BEFORE, "2024-11-27T00:00:00Z")],
            headers={"Link": f'<{next_url}>; rel="next"'},
        )

    api = client(handler)
    api._max_retries = 0
    run, _ = HistoricalRunner(api, tmp_path).run(CASE)
    assert all(result.pair.status is PairStatus.COLLECTION_FAILED for result in run.results)
    assert all(result.pair.before is None for result in run.results)
    assert all(result.history_snapshot_path for result in run.results)


def test_cross_file_path_migration_is_ambiguous(tmp_path: Path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/commits"):
            if request.url.params["path"] not in {"requirements.txt", "pyproject.toml"}:
                return httpx.Response(200, json=[])
            return httpx.Response(200, json=[
                commit(BEFORE, "2024-11-27T00:00:00Z"),
                commit(AFTER, "2024-11-29T00:00:00Z"),
            ])
        path = request.url.path
        before = request.url.params["ref"] == BEFORE
        if path.endswith("requirements.txt"):
            text = "httpx>=0.27" if before else "other>=1"
        else:
            dependencies = "other>=1" if before else "httpx>=0.27"
            text = f'[project]\ndependencies = ["{dependencies}"]'
        return httpx.Response(200, json=content(text))

    run, _ = HistoricalRunner(client(handler), tmp_path).run(CASE)
    paths = [
        item for item in run.results
        if item.pair.manifest_path in {"requirements.txt", "pyproject.toml"}
    ]
    assert len(paths) == 2
    assert all(item.pair.status is PairStatus.AMBIGUOUS for item in paths)
    assert all(item.change_status is ChangeStatus.UNKNOWN for item in paths)
    assert all(item.transition is None for item in paths)


def test_setup_py_is_parsed_without_running_repository_code(tmp_path: Path) -> None:
    marker = tmp_path / "executed"
    code = (
        f'open(r"{marker}", "w").write("bad")\n'
        'setup(install_requires=["httpx>=0.27"])'
    )
    observations, _ = parse_dependency_file_with_diagnostics(
        repository="example/repo", file_path="setup.py", content=code,
        commit_reference=BEFORE, observed_at=datetime.now(UTC),
        source=f"https://github.com/example/repo/blob/{BEFORE}/setup.py",
    )
    assert len(observations) == 1
    assert not marker.exists()


def test_marker_and_direct_reference_do_not_imply_target_acceptance(tmp_path: Path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/commits"):
            if request.url.params["path"] != "requirements.txt":
                return httpx.Response(200, json=[])
            return httpx.Response(200, json=[
                commit(BEFORE, "2024-11-27T00:00:00Z"),
                commit(AFTER, "2024-11-29T00:00:00Z"),
            ])
        text = (
            'httpx<0.28; python_version < "3.9"'
            if request.url.params["ref"] == BEFORE
            else "httpx @ https://example.org/httpx.whl"
        )
        return httpx.Response(200, json=content(text))

    run, _ = HistoricalRunner(client(handler), tmp_path).run(CASE)
    result = next(item for item in run.results if item.pair.manifest_path == "requirements.txt")
    assert result.change_status is ChangeStatus.CONSTRAINT_CHANGED
    assert result.before_state.target_observations[0].marker
    assert result.after_state.target_observations[0].direct_reference


def test_optional_groups_and_unrelated_dynamic_metadata() -> None:
    text = (
        '[project]\ndynamic = ["readme"]\n'
        '[project.optional-dependencies]\n'
        'database = ["SQLAlchemy>=1.4"]\n'
        'analytics = ["SQLAlchemy>=2"]\n'
    )
    observations, unparsed = parse_dependency_file_with_diagnostics(
        repository="example/repo", file_path="pyproject.toml", content=text,
        commit_reference=BEFORE, observed_at=datetime.now(UTC),
        source=f"https://github.com/example/repo/blob/{BEFORE}/pyproject.toml",
    )
    assert not unparsed
    assert {item.declaration_group for item in observations} == {
        "project.optional-dependencies.database",
        "project.optional-dependencies.analytics",
    }


def test_unchanged_optional_groups_are_reconciled_without_discarding_them(
    tmp_path: Path,
) -> None:
    manifest = (
        '[project]\ndynamic = ["readme"]\n'
        '[project.optional-dependencies]\n'
        'database = ["httpx>=0.27"]\n'
        'analytics = ["httpx>=0.27"]\n'
    )

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/commits"):
            if request.url.params["path"] != "pyproject.toml":
                return httpx.Response(200, json=[])
            return httpx.Response(200, json=[
                commit(BEFORE, "2024-11-27T00:00:00Z"),
                commit(AFTER, "2024-11-29T00:00:00Z"),
            ])
        return httpx.Response(200, json=content(manifest))

    run, _ = HistoricalRunner(client(handler), tmp_path).run(CASE)
    result = next(item for item in run.results if item.pair.manifest_path == "pyproject.toml")
    assert result.pair.status is PairStatus.PAIRED
    assert result.change_status is ChangeStatus.UNCHANGED
    assert len(result.before_state.target_observations) == 2
    assert len(result.after_state.target_observations) == 2


def test_single_available_ref_is_retrieved_but_not_compared(tmp_path: Path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/commits"):
            if request.url.params["path"] != "requirements.txt":
                return httpx.Response(200, json=[])
            return httpx.Response(200, json=[commit(AFTER, "2024-11-29T00:00:00Z")])
        assert request.url.params["ref"] == AFTER
        return httpx.Response(200, json=content("httpx>=0.27"))

    run, _ = HistoricalRunner(client(handler), tmp_path).run(CASE)
    result = next(item for item in run.results if item.pair.manifest_path == "requirements.txt")
    assert result.pair.status is PairStatus.MISSING_BEFORE
    assert result.before_state is None
    assert result.after_state.status is FileStateStatus.PARSED
    assert result.after_state.target_observations[0].package == "httpx"
    assert result.change_status is ChangeStatus.UNKNOWN
