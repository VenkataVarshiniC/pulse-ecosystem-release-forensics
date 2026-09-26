"""GitHub collection adapter for planned tasks."""

from __future__ import annotations

from datetime import date
from typing import Any

from pulse.collection.manifest import TaskOutcomeStatus
from pulse.collection.planner import CollectionTask, TaskKind
from pulse.collection.result import CollectionResult
from pulse.github.client import GitHubClient
from pulse.github.errors import GitHubApiError

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

    def collect(self, task: CollectionTask) -> CollectionResult:
        self.client.reset_stats()
        result = CollectionResult(stats=self.client.stats)
        try:
            if task.kind in {TaskKind.GITHUB_REPOSITORY, TaskKind.GITHUB_FILE}:
                result.payload = self._records(task)
            else:
                result.payload = []
                for record in self._records(task):
                    if task.kind in {
                        TaskKind.GITHUB_ISSUES, TaskKind.GITHUB_PULL_REQUESTS
                    } and not _within_window(
                        [record], task.parameters["since"], task.parameters["until"]
                    ):
                        continue
                    result.payload.append(record)
        except GitHubApiError as exc:
            result.failure_kind = exc.failure_kind
            result.error = exc.message
            result.status = (
                TaskOutcomeStatus.PARTIAL if result.stats.pages_completed
                else TaskOutcomeStatus(exc.failure_kind)
            )
        if result.stats.termination is None:
            result.stats.termination = result.failure_kind or "complete"
        return result

    def _records(self, task: CollectionTask) -> Any:
        repository = task.repository
        if repository is None:
            raise ValueError("GitHub task requires a repository")
        if task.kind is TaskKind.GITHUB_REPOSITORY:
            return self.client.repository(repository)
        if task.kind is TaskKind.GITHUB_RELEASES:
            return self.client.releases(repository)
        if task.kind is TaskKind.GITHUB_COMMITS:
            return self.client.commits(
                    repository,
                    since=f"{task.parameters['since']}T00:00:00Z",
                    until=f"{task.parameters['until']}T23:59:59Z",
            )
        if task.kind is TaskKind.GITHUB_FILE:
            return self.client.contents(repository, task.parameters["path"])
        if task.kind is TaskKind.GITHUB_ISSUES:
            return self.client.issues(
                repository, state="all", since=task.parameters["since"],
                sort="created", direction="asc",
            )
        return self.client.pull_requests(
            repository, state="all", sort="created", direction="asc"
        )


def _within_window(records: Any, since: str, until: str) -> list[dict[str, Any]]:
    start = date.fromisoformat(since)
    end = date.fromisoformat(until)
    accepted = []
    for record in records:
        raw = record.get("created_at") or record.get("updated_at")
        if raw and start <= date.fromisoformat(raw[:10]) <= end:
            accepted.append(record)
    return accepted
