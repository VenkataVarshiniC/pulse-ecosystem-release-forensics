from __future__ import annotations

import httpx
import pytest

from pulse.github.client import GitHubClient
from pulse.github.errors import GitHubAuthenticationError


def test_client_requires_authentication() -> None:
    with pytest.raises(GitHubAuthenticationError, match="GITHUB_TOKEN"):
        GitHubClient(None)


def test_pagination_follows_link_header_and_tracks_rate_limit() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.params.get("page") == "2":
            return httpx.Response(200, json=[{"id": 2}])
        return httpx.Response(
            200,
            json=[{"id": 1}],
            headers={
                "Link": '<https://api.github.test/items?page=2>; rel="next"',
                "X-RateLimit-Limit": "5000",
                "X-RateLimit-Remaining": "4999",
                "X-RateLimit-Reset": "2000000000",
                "X-RateLimit-Resource": "core",
            },
        )

    http_client = httpx.Client(
        base_url="https://api.github.test",
        transport=httpx.MockTransport(handler),
    )
    client = GitHubClient("test-token", http_client=http_client)

    assert list(client.paginate("/items")) == [{"id": 1}, {"id": 2}]
    assert client.rate_limit.limit is None  # Last response intentionally omitted headers.


def test_transient_response_is_retried() -> None:
    attempts = 0
    delays: list[float] = []

    def handler(_: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return httpx.Response(503, json={"message": "try again"})
        return httpx.Response(200, json={"full_name": "example/repo"})

    http_client = httpx.Client(
        base_url="https://api.github.test",
        transport=httpx.MockTransport(handler),
    )
    client = GitHubClient(
        "test-token",
        http_client=http_client,
        backoff_seconds=0.25,
        sleep=delays.append,
    )

    assert client.repository("example/repo")["full_name"] == "example/repo"
    assert attempts == 2
    assert delays == [0.25]


def test_issues_excludes_pull_requests_returned_by_github_issues_api() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json=[
                {"number": 10, "title": "A real issue"},
                {
                    "number": 11,
                    "title": "A pull request",
                    "pull_request": {"url": "https://api.github.test/repos/example/repo/pulls/11"},
                },
            ],
        )

    http_client = httpx.Client(
        base_url="https://api.github.test",
        transport=httpx.MockTransport(handler),
    )
    client = GitHubClient("test-token", http_client=http_client)

    assert list(client.issues("example/repo")) == [{"number": 10, "title": "A real issue"}]
