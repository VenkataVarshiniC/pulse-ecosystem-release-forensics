"""PyPI JSON API adapter."""

from __future__ import annotations

from typing import Any

import httpx

from pulse.packages.base import DistributionArtifact, PackageMetadata


class PyPIClient:
    def __init__(
        self,
        *,
        base_url: str = "https://pypi.org/pypi",
        http_client: httpx.Client | None = None,
    ) -> None:
        self._owns_client = http_client is None
        self._client = http_client or httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=30,
            headers={"User-Agent": "pulse-release-forensics/0.1"},
        )

    def __enter__(self) -> PyPIClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def package(self, name: str, *, version: str | None = None) -> PackageMetadata:
        endpoint = f"/{name}/{version}/json" if version else f"/{name}/json"
        response = self._client.get(endpoint)
        response.raise_for_status()
        payload: dict[str, Any] = response.json()
        info = payload["info"]
        files = payload.get("urls", [])
        artifacts = tuple(
            DistributionArtifact(
                package=info["name"],
                version=info["version"],
                uploaded_at=item["upload_time_iso_8601"],
                artifact_url=item["url"],
                python_requires=item.get("requires_python"),
            )
            for item in files
        )
        project_urls = info.get("project_urls") or {}
        repository = _first_url(project_urls, "Source", "Repository", "Code")
        return PackageMetadata(
            name=info["name"],
            version=info["version"],
            project_url=info["package_url"],
            repository_url=repository,
            artifacts=artifacts,
        )


def _first_url(values: dict[str, str], *keys: str) -> str | None:
    normalized = {key.casefold(): value for key, value in values.items()}
    return next((normalized[key.casefold()] for key in keys if key.casefold() in normalized), None)
