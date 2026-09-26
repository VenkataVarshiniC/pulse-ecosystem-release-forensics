from __future__ import annotations

import httpx
import pytest

from pulse.github.client import GitHubClient
from pulse.github.errors import GitHubApiError


@pytest.fixture
def make_client():
    clients = []

    def make(handler, **kwargs):
        transport = httpx.Client(
            base_url="https://api.github.test", transport=httpx.MockTransport(handler)
        )
        clients.append(transport)
        return GitHubClient("fixture-token", http_client=transport, **kwargs)

    yield make
    for client in clients:
        client.close()


@pytest.mark.parametrize("method", ["issues", "pull_requests", "commits", "releases"])
def test_all_list_endpoints_follow_pages_and_deduplicate(make_client, method):
    seen = []

    def handler(request):
        seen.append(request)
        assert request.headers["Authorization"] == "Bearer fixture-token"
        if request.url.params.get("page") == "2":
            return httpx.Response(200, json=[{"id": 1}, {"id": 2}])
        return httpx.Response(
            200, json=[{"id": 1}],
            headers={"Link": f'<{request.url.copy_set_param("page", "2")}>; rel="next"'},
        )

    client = make_client(handler)
    assert list(getattr(client, method)("org/repo")) == [{"id": 1}, {"id": 2}]
    assert len(seen) == 2
    assert client.stats.pages_requested == client.stats.pages_completed == 2
    assert client.stats.records_examined == 3
    assert client.stats.duplicate_records == 1
    assert client.stats.termination == "complete"


@pytest.mark.parametrize("limit,cycle,reason", [
    (1, False, "page_limit"), (10, True, "pagination_cycle"),
])
def test_pagination_stops_explicitly_at_limit_or_cycle(make_client, limit, cycle, reason):
    calls = []

    def handler(request):
        calls.append(request)
        link = request.url if cycle else request.url.copy_set_param("page", "2")
        return httpx.Response(
            200, json=[{"id": 1}], headers={"Link": f'<{link}>; rel="next"'}
        )

    client = make_client(handler, max_pages=limit)
    records = []
    with pytest.raises(GitHubApiError, match="safety limit"):
        records.extend(client.issues("org/repo"))
    assert records == [{"id": 1}]
    assert len(calls) == 1
    assert client.stats.termination == reason


def test_cross_origin_link_is_not_followed_with_credentials(make_client):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(
            200, json=[], headers={"Link": '<https://elsewhere.test/items>; rel="next"'}
        )

    client = make_client(handler)
    with pytest.raises(GitHubApiError, match="origin"):
        list(client.releases("org/repo"))
    assert len(calls) == 1


@pytest.mark.parametrize("first", ["network", 429, 503])
def test_transient_failure_then_success_records_retry(make_client, first):
    calls = []
    delays = []

    def handler(request):
        calls.append(request)
        if len(calls) == 1:
            if first == "network":
                raise httpx.ConnectError("a private diagnostic", request=request)
            return httpx.Response(first, headers={"Retry-After": "2"})
        return httpx.Response(200, json={"id": 1})

    client = make_client(handler, sleep=delays.append)
    assert client.repository("org/repo") == {"id": 1}
    assert len(calls) == 2
    assert client.stats.retry_count == 1
    assert len(client.stats.requests) == 2
    assert delays == ([0.5] if first == "network" else [2.0])


@pytest.mark.parametrize("statuses", [[503, 503, 503], [503, "network", "network"]])
def test_retry_exhaustion_never_returns_a_stale_response(make_client, statuses):
    pending = iter(statuses)
    delays = []

    def handler(request):
        status = next(pending)
        if status == "network":
            raise httpx.ReadTimeout("fixture-token", request=request)
        return httpx.Response(status, json={"message": "fixture-token"})

    client = make_client(handler, max_retries=2, sleep=delays.append)
    with pytest.raises(GitHubApiError) as caught:
        client.repository("org/repo")
    assert "fixture-token" not in str(caught.value)
    assert "fixture-token" not in client.stats.model_dump_json()
    assert delays == [0.5, 1.0]
    assert client.stats.retry_count == 2
    assert client.stats.pages_completed == 0


@pytest.mark.parametrize("status,kind", [
    (401, "unauthorized"), (403, "unauthorized"), (404, "not_found"), (422, "failed"),
])
def test_nonretryable_status_has_explicit_failure_kind(make_client, status, kind):
    delays = []
    client = make_client(
        lambda _: httpx.Response(status, json={"message": "fixture-token"}),
        sleep=delays.append,
    )
    with pytest.raises(GitHubApiError) as caught:
        client.repository("org/repo")
    assert caught.value.failure_kind == kind
    assert delays == []
    assert len(client.stats.requests) == 1


@pytest.mark.parametrize("status", [403, 429])
def test_long_rate_limit_is_preserved_without_early_retry(make_client, status):
    delays = []
    client = make_client(
        lambda _: httpx.Response(status, headers={
            "X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "2000000000",
        }),
        clock=lambda: 1999999000.0, sleep=delays.append,
    )
    with pytest.raises(GitHubApiError) as caught:
        client.repository("org/repo")
    assert caught.value.failure_kind == "rate_limited"
    assert client.stats.requests[0].remaining == 0
    assert client.stats.requests[0].reset_at is not None
    assert delays == []


def test_secondary_rate_limit_exhaustion_is_not_authentication_failure(make_client):
    delays = []
    client = make_client(
        lambda _: httpx.Response(403, json={"message": "secondary rate limit"}),
        max_retries=1, sleep=delays.append,
    )
    with pytest.raises(GitHubApiError) as caught:
        client.repository("org/repo")
    assert caught.value.failure_kind == "rate_limited"
    assert delays == [60.0]


def test_empty_page_is_a_successful_negative_observation(make_client):
    client = make_client(lambda _: httpx.Response(200, json=[]))
    assert list(client.issues("org/repo")) == []
    assert client.stats.pages_completed == 1
    assert client.stats.records_examined == 0
    assert client.stats.termination == "complete"


def test_invalid_json_is_a_typed_failure_without_echoing_body(make_client):
    client = make_client(lambda _: httpx.Response(200, text="fixture-token"))
    with pytest.raises(GitHubApiError, match="invalid JSON"):
        list(client.releases("org/repo"))
    assert client.stats.pages_completed == 0


def test_retry_after_http_date_is_respected(make_client):
    calls = []
    delays = []

    def handler(request):
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(429, headers={"Retry-After": "Thu, 01 Jan 1970 00:00:05 GMT"})
        return httpx.Response(200, json={})

    client = make_client(handler, clock=lambda: 0, sleep=delays.append)
    assert client.repository("org/repo") == {}
    assert delays == [5.0]
