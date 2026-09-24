from __future__ import annotations

import httpx

from pulse.packages.pypi import PyPIClient


def test_package_normalizes_version_files_and_repository() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "info": {
                    "name": "example",
                    "version": "2.0.0",
                    "package_url": "https://pypi.org/project/example/",
                    "project_urls": {"Source": "https://github.com/example/example"},
                },
                "urls": [
                    {
                        "url": "https://files.pythonhosted.org/example.whl",
                        "upload_time_iso_8601": "2024-06-16T12:00:00Z",
                        "requires_python": ">=3.9",
                    }
                ],
            },
        )

    http_client = httpx.Client(
        base_url="https://pypi.test/pypi",
        transport=httpx.MockTransport(handler),
    )
    package = PyPIClient(http_client=http_client).package("example", version="2.0.0")

    assert package.version == "2.0.0"
    assert str(package.repository_url) == "https://github.com/example/example"
    assert package.artifacts[0].python_requires == ">=3.9"
    assert package.artifacts[0].version == package.version
