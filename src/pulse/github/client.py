"""Small, testable GitHub REST client for forensic collection."""

from __future__ import annotations

import logging
import time
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import httpx

from pulse.github.errors import GitHubApiError, GitHubAuthenticationError

LOGGER = logging.getLogger(__name__)
_TRANSIENT_STATUS = {429, 500, 502, 503, 504}


@dataclass(frozen=True, slots=True)
class RateLimit:
    limit: int | None
    remaining: int | None
    reset_at: datetime | None
    resource: str | None


class GitHubClient:
    """Authenticated GitHub REST access with pagination and bounded retries."""

    def __init__(
        self,
        token: str | None,
        *,
        base_url: str = "https://api.github.com",
        timeout_seconds: float = 30.0,
        max_retries: int = 3,
        backoff_seconds: float = 0.5,
        http_client: httpx.Client | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        if not token:
            raise GitHubAuthenticationError("GITHUB_TOKEN is required")
        self._max_retries = max_retries
        self._backoff_seconds = backoff_seconds
        self._sleep = sleep
        self._owns_client = http_client is None
        self._client = http_client or httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=timeout_seconds,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "pulse-release-forensics/0.1",
            },
        )
        self.rate_limit = RateLimit(None, None, None, None)

    def __enter__(self) -> GitHubClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def _update_rate_limit(self, response: httpx.Response) -> None:
        headers = response.headers
        reset_raw = headers.get("X-RateLimit-Reset")
        reset_at = None
        if reset_raw and reset_raw.isdigit():
            reset_at = datetime.fromtimestamp(int(reset_raw), tz=UTC)

        def as_int(name: str) -> int | None:
            value = headers.get(name)
            return int(value) if value and value.isdigit() else None

        self.rate_limit = RateLimit(
            limit=as_int("X-RateLimit-Limit"),
            remaining=as_int("X-RateLimit-Remaining"),
            reset_at=reset_at,
            resource=headers.get("X-RateLimit-Resource"),
        )

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> httpx.Response:
        last_error: httpx.HTTPError | None = None
        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.request(method, endpoint, **kwargs)
                self._update_rate_limit(response)
            except httpx.HTTPError as exc:
                last_error = exc
                if attempt == self._max_retries:
                    break
                delay = self._backoff_seconds * (2**attempt)
                LOGGER.warning("GitHub request failed; retrying", extra={"delay": delay})
                self._sleep(delay)
                continue

            if response.status_code not in _TRANSIENT_STATUS:
                break
            if attempt == self._max_retries:
                break
            retry_after = response.headers.get("Retry-After")
            delay = float(retry_after) if retry_after else self._backoff_seconds * (2**attempt)
            LOGGER.warning(
                "GitHub returned a transient response; retrying",
                extra={"status": response.status_code, "delay": delay},
            )
            self._sleep(delay)
        else:  # pragma: no cover - loop is bounded and always exits via return/break
            raise AssertionError("unreachable")

        if last_error is not None and "response" not in locals():
            raise GitHubApiError("GitHub request failed", endpoint=endpoint) from last_error
        if response.status_code in {401, 403}:
            raise GitHubAuthenticationError(
                "GitHub authentication or permission check failed",
                status_code=response.status_code,
                endpoint=endpoint,
                response_body=_safe_json(response),
            )
        if response.is_error:
            raise GitHubApiError(
                "GitHub API returned an error",
                status_code=response.status_code,
                endpoint=endpoint,
                response_body=_safe_json(response),
            )
        LOGGER.debug(
            "GitHub request complete",
            extra={"endpoint": endpoint, "remaining": self.rate_limit.remaining},
        )
        return response

    def get_json(self, endpoint: str, *, params: dict[str, Any] | None = None) -> Any:
        return self._request("GET", endpoint, params=params).json()

    def paginate(
        self,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Iterator[dict[str, Any]]:
        query = {**(params or {}), "per_page": 100}
        next_endpoint: str | None = endpoint
        while next_endpoint:
            response = self._request("GET", next_endpoint, params=query or None)
            payload = response.json()
            if not isinstance(payload, list):
                raise GitHubApiError(
                    "Expected a paginated list",
                    status_code=response.status_code,
                    endpoint=next_endpoint,
                    response_body=payload,
                )
            yield from payload
            next_endpoint = response.links.get("next", {}).get("url")
            query = {}

    def repository(self, full_name: str) -> dict[str, Any]:
        return self.get_json(f"/repos/{full_name}")

    def releases(self, full_name: str) -> Iterator[dict[str, Any]]:
        return self.paginate(f"/repos/{full_name}/releases")

    def issues(self, full_name: str, **filters: Any) -> Iterator[dict[str, Any]]:
        for item in self.paginate(f"/repos/{full_name}/issues", params=filters):
            # GitHub's issues endpoint includes pull requests. Analytical issue
            # counts must never treat those records as issues.
            if "pull_request" not in item:
                yield item

    def pull_requests(self, full_name: str, **filters: Any) -> Iterator[dict[str, Any]]:
        return self.paginate(f"/repos/{full_name}/pulls", params=filters)

    def commits(self, full_name: str, **filters: Any) -> Iterator[dict[str, Any]]:
        return self.paginate(f"/repos/{full_name}/commits", params=filters)

    def contents(self, full_name: str, path: str, *, ref: str | None = None) -> dict[str, Any]:
        params = {"ref": ref} if ref else None
        return self.get_json(f"/repos/{full_name}/contents/{path}", params=params)


def _safe_json(response: httpx.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return response.text[:1000]
