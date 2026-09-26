"""Authenticated REST collection with bounded pagination and request retries."""

from __future__ import annotations

import json
import time
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from typing import Any

import httpx

from pulse.collection.telemetry import CollectionStats, RequestRecord
from pulse.github.errors import GitHubApiError, GitHubAuthenticationError

_TRANSIENT_STATUS = {500, 502, 503, 504}


@dataclass(frozen=True, slots=True)
class RateLimit:
    limit: int | None
    remaining: int | None
    reset_at: datetime | None
    resource: str | None


class GitHubClient:
    """Sequential client; reset telemetry at each logical task boundary."""

    def __init__(
        self, token: str | None, *,
        base_url: str = "https://api.github.com",
        timeout_seconds: float = 30.0,
        max_retries: int = 3,
        backoff_seconds: float = 0.5,
        max_pages: int = 1000,
        max_wait_seconds: float = 60.0,
        http_client: httpx.Client | None = None,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.time,
    ) -> None:
        if not token or not token.strip():
            raise GitHubAuthenticationError(
                "GITHUB_TOKEN is required", failure_kind="unauthorized"
            )
        if max_retries < 0 or max_pages < 1 or backoff_seconds < 0 or max_wait_seconds < 0:
            raise ValueError(
                "Retry and wait limits must be nonnegative; max_pages must be positive"
            )
        self._max_retries = max_retries
        self._max_pages = max_pages
        self._backoff_seconds = backoff_seconds
        self._max_wait_seconds = max_wait_seconds
        self._sleep = sleep
        self._clock = clock
        self._owns_client = http_client is None
        self._client = http_client or httpx.Client(
            base_url=base_url.rstrip("/"), timeout=timeout_seconds
        )
        # Injection changes transport, not the authentication contract.
        self._headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "pulse-release-forensics/0.2",
        }
        self.reset_stats()

    def reset_stats(self) -> None:
        self.stats = CollectionStats()
        self.rate_limit = RateLimit(None, None, None, None)

    def __enter__(self) -> GitHubClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def _update_rate_limit(self, response: httpx.Response) -> None:
        def as_int(name: str) -> int | None:
            value = response.headers.get(name)
            return int(value) if value and value.isdigit() else None

        reset = as_int("X-RateLimit-Reset")
        try:
            reset_at = datetime.fromtimestamp(reset, tz=UTC) if reset is not None else None
        except (OverflowError, OSError, ValueError):
            reset_at = None
        self.rate_limit = RateLimit(
            as_int("X-RateLimit-Limit"), as_int("X-RateLimit-Remaining"),
            reset_at, response.headers.get("X-RateLimit-Resource"),
        )
        self.stats.requests.append(RequestRecord(
            status_code=response.status_code,
            remaining=self.rate_limit.remaining,
            reset_at=reset_at.isoformat() if reset_at else None,
            retry_after=response.headers.get("Retry-After"),
        ))

    def _retry_delay(self, response: httpx.Response, attempt: int, limited: bool) -> float:
        delay = self._backoff_seconds * (2**attempt)
        hint = response.headers.get("Retry-After")
        supplied = False
        if hint:
            try:
                wait = float(hint)
            except ValueError:
                try:
                    wait = parsedate_to_datetime(hint).timestamp() - self._clock()
                except (ValueError, TypeError, OverflowError):
                    wait = None
            if wait is not None and wait >= 0:
                delay = max(delay, wait)
                supplied = True
        if limited and self.rate_limit.remaining == 0 and self.rate_limit.reset_at:
            delay = max(delay, self.rate_limit.reset_at.timestamp() - self._clock())
            supplied = True
        if limited and not supplied:
            delay = max(delay, 60.0 * (2**attempt))
        return delay

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> httpx.Response:
        self.stats.pages_requested += 1
        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.request(
                    method, endpoint, headers=self._headers, **kwargs
                )
            except httpx.TransportError as exc:
                self.stats.requests.append(RequestRecord(error_type=type(exc).__name__))
                if attempt == self._max_retries:
                    raise GitHubApiError("GitHub transport retries exhausted") from None
                delay = self._backoff_seconds * (2**attempt)
                if delay > self._max_wait_seconds:
                    raise GitHubApiError("GitHub retry delay exceeds wait budget") from None
            else:
                self._update_rate_limit(response)
                status = response.status_code
                limited = status == 429 or (
                    status == 403 and (
                        self.rate_limit.remaining == 0
                        or "Retry-After" in response.headers
                        or "rate limit" in response.text.casefold()
                    )
                )
                if status == 401 or (status == 403 and not limited):
                    raise GitHubAuthenticationError(
                        "GitHub authentication or permission check failed",
                        status_code=status, failure_kind="unauthorized",
                    )
                if status == 404:
                    raise GitHubApiError(
                        "GitHub resource unavailable (404)",
                        status_code=status, failure_kind="not_found",
                    )
                if not limited and status not in _TRANSIENT_STATUS:
                    if not 200 <= status < 300:
                        raise GitHubApiError("GitHub API returned an error", status_code=status)
                    return response
                delay = self._retry_delay(response, attempt, limited)
                if attempt == self._max_retries or delay > self._max_wait_seconds:
                    raise GitHubApiError(
                        "GitHub rate limit prevents continuation" if limited
                        else "GitHub transient retries exhausted or wait budget exceeded",
                        status_code=status, failure_kind="rate_limited" if limited else "failed",
                    )
            self.stats.retry_count += 1
            self._sleep(delay)
        raise AssertionError("unreachable")

    def _decode(self, response: httpx.Response) -> Any:
        try:
            return response.json()
        except ValueError:
            raise GitHubApiError("GitHub returned invalid JSON") from None

    def get_json(self, endpoint: str, *, params: dict[str, Any] | None = None) -> Any:
        payload = self._decode(self._request("GET", endpoint, params=params))
        self.stats.pages_completed += 1
        self.stats.records_examined += len(payload) if isinstance(payload, list) else 1
        self.stats.termination = "complete"
        return payload

    def paginate(
        self, endpoint: str, *, params: dict[str, Any] | None = None,
    ) -> Iterator[dict[str, Any]]:
        query = {**(params or {}), "per_page": 100}
        next_endpoint: str | None = endpoint
        visited: set[str] = set()
        identities: set[str] = set()
        origin = self._client.base_url
        page_count = 0
        while next_endpoint:
            url = origin.join(next_endpoint)
            if query:
                url = url.copy_merge_params(query)
            if (url.scheme, url.host, url.port) != (origin.scheme, origin.host, origin.port):
                self.stats.termination = "unsafe_next_link"
                raise GitHubApiError("GitHub next link left the configured API origin")
            key = str(url)
            if key in visited or page_count >= self._max_pages:
                self.stats.termination = "pagination_cycle" if key in visited else "page_limit"
                raise GitHubApiError("GitHub pagination safety limit reached")
            visited.add(key)
            response = self._request("GET", key)
            payload = self._decode(response)
            if not isinstance(payload, list) or any(not isinstance(item, dict) for item in payload):
                raise GitHubApiError("Expected a paginated list of records")
            self.stats.pages_completed += 1
            page_count += 1
            self.stats.records_examined += len(payload)
            for item in payload:
                identity = next(
                    (f"{field}:{item[field]}" for field in ("id", "node_id", "sha", "number")
                     if field in item),
                    json.dumps(item, sort_keys=True),
                )
                if identity in identities:
                    self.stats.duplicate_records += 1
                    continue
                identities.add(identity)
                yield item
            next_endpoint = response.links.get("next", {}).get("url")
            query = {}
        self.stats.termination = "complete"

    def repository(self, full_name: str) -> dict[str, Any]:
        return self.get_json(f"/repos/{full_name}")

    def releases(self, full_name: str) -> Iterator[dict[str, Any]]:
        return self.paginate(f"/repos/{full_name}/releases")

    def issues(self, full_name: str, **filters: Any) -> Iterator[dict[str, Any]]:
        for item in self.paginate(f"/repos/{full_name}/issues", params=filters):
            if "pull_request" not in item:
                yield item

    def pull_requests(self, full_name: str, **filters: Any) -> Iterator[dict[str, Any]]:
        return self.paginate(f"/repos/{full_name}/pulls", params=filters)

    def commits(self, full_name: str, **filters: Any) -> Iterator[dict[str, Any]]:
        return self.paginate(f"/repos/{full_name}/commits", params=filters)

    def contents(self, full_name: str, path: str, *, ref: str | None = None) -> dict[str, Any]:
        return self.get_json(
            f"/repos/{full_name}/contents/{path}", params={"ref": ref} if ref else None
        )
