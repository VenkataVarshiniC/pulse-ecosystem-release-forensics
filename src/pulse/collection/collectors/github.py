"""GitHub collection adapter for planned tasks."""

from __future__ import annotations

from datetime import date
from typing import Any

from pulse.collection.planner import CollectionTask, TaskKind
from pulse.github.client import GitHubClient

_KINDS = {
    TaskKind.GITHUB_REPOSITORY,
    TaskKind.GITHUB_RELEASES,
    TaskKind.GITHUB_ISSUES,
    TaskKind.GITHUB_PULL_REQUESTS,
    TaskKind.GITHUB_COMMITS,
    TaskKind.GITHUB_FILE,
}


class GitHubCollector:
    def __init__(self, client: GitHubClient) -> None:
        self.client = client

    def supports(self, kind: TaskKind) -> bool:
        return kind in _KINDS

    def collect(self, task: CollectionTask) -> Any:
        repository = task.repository
        if repository is None:
            raise ValueError("GitHub task requires a repository")
        if task.kind is TaskKind.GITHUB_REPOSITORY:
            return self.client.repository(repository)
        if task.kind is TaskKind.GITHUB_RELEASES:
            return list(self.client.releases(repository))
        if task.kind is TaskKind.GITHUB_COMMITS:
            return list(
                self.client.commits(
                    repository,
                    since=f"{task.parameters['since']}T00:00:00Z",
                    until=f"{task.parameters['until']}T23:59:59Z",
                )
            )
        if task.kind is TaskKind.GITHUB_FILE:
            return self.client.contents(repository, task.parameters["path"])
        if task.kind is TaskKind.GITHUB_ISSUES:
            records = self.client.issues(repository, state="all", since=task.parameters["since"])
            return _within_window(records, task.parameters["since"], task.parameters["until"])
        records = self.client.pull_requests(
            repository, state="all", sort="updated", direction="asc"
        )
        return _within_window(records, task.parameters["since"], task.parameters["until"])


def _within_window(records: Any, since: str, until: str) -> list[dict[str, Any]]:
    start = date.fromisoformat(since)
    end = date.fromisoformat(until)
    accepted = []
    for record in records:
        raw = record.get("created_at") or record.get("updated_at")
        if raw and start <= date.fromisoformat(raw[:10]) <= end:
            accepted.append(record)
    return accepted
