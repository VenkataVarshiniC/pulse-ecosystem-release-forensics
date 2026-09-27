"""Execute the predeclared Phase 2 Milestone 3 cohort-selection protocol.

Only package metadata, code-search hits, current manifests, repository metadata,
and commit counts are read. No issue, PR, or commit content is inspected.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import os
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
import yaml
from packaging.utils import canonicalize_name
from packaging.version import InvalidVersion, Version

from pulse.dependencies.parsers import parse_dependency_file_with_diagnostics
from pulse.github.client import GitHubClient
from pulse.github.errors import GitHubApiError
from pulse.models.case import CaseDefinition

SEEDS = ("click", "pytest", "urllib3")
RELEASE_START = date(2023, 1, 1)
RELEASE_END = date(2024, 12, 31)
SEARCH_PATHS = ("pyproject.toml", "requirements.txt")
SEARCH_PAGE_SIZE = 30
COHORT_SIZE = 6
MAX_REPOSITORY_KB = 500_000


def _timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def observation_window(released_at: datetime) -> tuple[date, date]:
    day = released_at.astimezone(UTC).date()
    return day - timedelta(days=30), day + timedelta(days=120)


def rank(case_id: str, repository: str) -> str:
    key = f"{case_id}/{repository.lower()}".encode()
    return hashlib.sha256(key).hexdigest()


def _github_repository(info: dict[str, Any]) -> str | None:
    urls = info.get("project_urls") or {}
    candidates = [
        urls[key] for key in ("Source", "Repository", "Code", "Homepage")
        if isinstance(urls.get(key), str)
    ]
    candidates += [
        value for key, value in sorted(urls.items())
        if key not in {"Source", "Repository", "Code", "Homepage"}
        and isinstance(value, str)
    ]
    for value in candidates:
        parsed = urlparse(value)
        parts = parsed.path.strip("/").removesuffix(".git").split("/")
        if parsed.hostname == "github.com" and len(parts) == 2 and all(parts):
            return "/".join(parts)
    return None


def select_targets(pypi: httpx.Client) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    pool = []
    for package in SEEDS:
        response = pypi.get(f"/pypi/{package}/json")
        response.raise_for_status()
        payload = response.json()
        upstream = _github_repository(payload["info"])
        eligible = []
        for version_text, files in payload["releases"].items():
            try:
                version = Version(version_text)
            except InvalidVersion:
                continue
            if (
                version.is_prerelease or version.is_postrelease or version.is_devrelease
                or version.local is not None or len(version.release) != 3
                or version.release[0] < 2 or version.release[1:] != (0, 0)
            ):
                continue
            uploaded = [
                _timestamp(item["upload_time_iso_8601"])
                for item in files if item.get("upload_time_iso_8601")
            ]
            if not uploaded:
                continue
            first = min(uploaded)
            if RELEASE_START <= first.date() <= RELEASE_END:
                eligible.append((first, version_text))
        latest = max(eligible, default=None)
        record = {
            "package": package, "pypi_url": f"https://pypi.org/pypi/{package}/json",
            "upstream_repository": upstream,
            "qualifying_release": latest[1] if latest else None,
            "released_at": latest[0].isoformat() if latest else None,
            "eligible": bool(latest and upstream),
            "exclusion_reason": None if latest and upstream else (
                "no_public_github_upstream" if not upstream else "no_release_in_range"
            ),
        }
        pool.append(record)
    chosen = sorted(
        (record for record in pool if record["eligible"]),
        key=lambda item: (item["released_at"], item["package"]), reverse=True,
    )[:2]
    if len(chosen) != 2:
        raise RuntimeError("The predeclared package pool yielded fewer than two releases")
    return pool, chosen


def discover_candidates(github: GitHubClient, package: str) -> tuple[list[dict], list[dict]]:
    searches = []
    by_repository: dict[str, dict[str, Any]] = {}
    for path in SEARCH_PATHS:
        query = f"{package} in:file filename:{path}"
        response = github.get_json(
            "/search/code", params={"q": query, "per_page": SEARCH_PAGE_SIZE, "page": 1}
        )
        if response.get("incomplete_results") or not isinstance(response.get("items"), list):
            raise RuntimeError(f"Code search was incomplete for {query}")
        searches.append({
            "query": query, "retrieved_at": datetime.now(UTC).isoformat(),
            "total_count": response["total_count"],
            "returned_count": len(response["items"]),
            "ordered_results": [
                {"repository": item["repository"]["full_name"],
                 "path": item["path"], "html_url": item["html_url"]}
                for item in response["items"]
            ],
        })
        for index, item in enumerate(response["items"], start=1):
            name = item["repository"]["full_name"]
            key = name.lower()
            candidate = by_repository.setdefault(key, {
                "repository": name, "search_hits": [],
            })
            candidate["search_hits"].append({
                "query": query, "rank": index, "path": item["path"],
                "html_url": item["html_url"],
            })
    return searches, list(by_repository.values())


def _manifest_content(payload: Any) -> tuple[str, str]:
    if not isinstance(payload, dict) or payload.get("type") != "file":
        raise ValueError("Not a regular file")
    if payload.get("encoding") != "base64" or not isinstance(payload.get("content"), str):
        raise ValueError("No inline base64 content")
    binary = base64.b64decode("".join(payload["content"].split()), validate=True)
    if len(binary) > 1_000_000:
        raise ValueError("Manifest exceeds 1 MB")
    return binary.decode("utf-8"), hashlib.sha256(binary).hexdigest()


def evaluate_candidate(
    github: GitHubClient, candidate: dict[str, Any], target: dict[str, Any],
    *, checked_at: datetime,
) -> dict[str, Any]:
    repository = candidate["repository"]
    row = {
        **candidate,
        "rank_hash": rank(f"{target['package']}-{target['qualifying_release']}", repository),
        "eligible": False, "selected": False, "exclusion_reasons": [],
        "metadata": None, "dependency": None, "activity": None,
    }
    reasons = row["exclusion_reasons"]
    roots = [hit for hit in candidate["search_hits"] if hit["path"] in SEARCH_PATHS]
    if not roots:
        reasons.append("non_root_manifest")
        return row
    try:
        metadata = github.repository(repository)
    except GitHubApiError as exc:
        if exc.failure_kind == "not_found":
            reasons.append("repository_unavailable")
            return row
        raise
    row["metadata"] = {
        "description": metadata.get("description"),
        "language": metadata.get("language"),
        "size_kb": metadata.get("size"),
        "archived": metadata.get("archived"),
        "fork": metadata.get("fork"),
        "private": metadata.get("private"),
        "default_branch": metadata.get("default_branch"),
        "html_url": metadata.get("html_url"),
    }
    if metadata.get("private"):
        reasons.append("private")
    if metadata.get("archived"):
        reasons.append("archived")
    if metadata.get("fork"):
        reasons.append("fork")
    if metadata.get("language") != "Python":
        reasons.append("not_primary_python")
    if not isinstance(metadata.get("size"), int) or metadata["size"] > MAX_REPOSITORY_KB:
        reasons.append("repository_too_large_or_unknown")
    upstream = target["upstream_repository"].lower()
    if repository.lower() == upstream:
        reasons.append("upstream_repository")
    if repository.split("/")[0].lower() == upstream.split("/")[0]:
        reasons.append("upstream_owner")
    if reasons:
        return row
    for path in SEARCH_PATHS:
        if not any(hit["path"] == path for hit in roots):
            continue
        try:
            payload = github.contents(repository, path, ref=metadata["default_branch"])
            content, digest = _manifest_content(payload)
            observations, _ = parse_dependency_file_with_diagnostics(
                repository=repository, file_path=path, content=content,
                commit_reference=payload.get("sha", metadata["default_branch"]),
                observed_at=checked_at,
                source=payload.get("html_url") or f"https://github.com/{repository}",
            )
        except (GitHubApiError, ValueError, TypeError, UnicodeError, binascii.Error):
            continue
        matches = [
            item for item in observations
            if item.package == canonicalize_name(target["package"])
        ]
        if matches:
            row["dependency"] = {
                "path": path, "source_url": payload.get("html_url"),
                "content_sha256": digest, "observed_at": checked_at.isoformat(),
                "declarations": [
                    {"raw": item.raw_requirement, "group": item.declaration_group}
                    for item in matches
                ],
            }
            break
    if row["dependency"] is None:
        reasons.append("no_direct_dependency_declaration")
        return row
    start, end = observation_window(_timestamp(target["released_at"]))
    until = end + timedelta(days=1)
    try:
        commits = github.get_json(
            f"/repos/{repository}/commits",
            params={"since": f"{start.isoformat()}T00:00:00Z",
                    "until": f"{until.isoformat()}T00:00:00Z", "per_page": 2},
        )
    except GitHubApiError as exc:
        if exc.failure_kind == "not_found":
            reasons.append("activity_unavailable")
            return row
        raise
    if not isinstance(commits, list):
        raise RuntimeError(f"Unexpected activity response for {repository}")
    row["activity"] = {
        "at_least_two_commits": len(commits) >= 2,
        "sample_committer_dates": [
            item.get("commit", {}).get("committer", {}).get("date")
            for item in commits
        ],
    }
    if len(commits) < 2:
        reasons.append("inactive_in_window")
        return row
    row["eligible"] = True
    return row


def _case_payload(
    target: dict[str, Any], selected: list[dict[str, Any]], created_at: datetime,
) -> dict[str, Any]:
    package, version = target["package"], target["qualifying_release"]
    case_id = f"{package}-{version}"
    start, end = observation_window(_timestamp(target["released_at"]))
    return {
        "case": {
            "case_id": case_id, "target_package": package, "target_version": version,
            "upstream_repository": target["upstream_repository"],
            "release_timestamp": target["released_at"], "ecosystem": "pypi",
            "observation_window_start": start.isoformat(),
            "observation_window_end": end.isoformat(),
            "collection_rules": [
                {"source": "pypi", "artifact_types": ["package_version"]},
                {"source": "github", "artifact_types": [
                    "repository", "releases", "issues", "pull_requests", "commits", "files",
                ], "file_paths": list(SEARCH_PATHS)},
            ],
            "created_at": created_at.isoformat(),
        },
        "cohort": {
            "cohort_id": f"{case_id}-rule-based", "case_id": case_id,
            "selection_method": "rule_based",
            "selection_rationale": (
                "First six eligible repositories by the predeclared SHA-256 ranking "
                "of a bounded GitHub code-search candidate frame; no release outcomes inspected."
            ),
            "created_at": created_at.isoformat(),
            "repositories": [
                {
                    "repository": row["repository"],
                    "project_name": row["repository"].split("/")[1],
                    "inclusion_reason": (
                        f"Direct {package} declaration in root {row['dependency']['path']} "
                        "and at least two public commits in the declared window."
                    ),
                    "dependency_evidence": {
                        "url": row["dependency"]["source_url"],
                        "observed_at": row["dependency"]["observed_at"],
                        "excerpt": row["dependency"]["declarations"][0]["raw"],
                        "content_sha256": row["dependency"]["content_sha256"],
                        "source_type": "repository_file",
                        "source_identifier": (
                            f"{row['repository']}:{row['dependency']['path']}"
                        ),
                    },
                    "selection_confidence": "high",
                }
                for row in selected
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=Path("."))
    args = parser.parse_args()
    checked_at = datetime.now(UTC)
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required for authenticated code search")
    with httpx.Client(base_url="https://pypi.org", timeout=30) as pypi:
        pool, targets = select_targets(pypi)
    ledger: dict[str, Any] = {
        "protocol_commit": "7f3c495", "checked_at": checked_at.isoformat(),
        "target_seed_pool": pool, "cases": [], "outcome_evidence_inspected": False,
    }
    definitions = []
    with GitHubClient(token, max_retries=2, max_pages=1) as github:
        for target in targets:
            searches, candidates = discover_candidates(github, target["package"])
            rows = [
                evaluate_candidate(github, item, target, checked_at=checked_at)
                for item in candidates
            ]
            eligible = sorted(
                (row for row in rows if row["eligible"]),
                key=lambda row: (row["rank_hash"], row["repository"].lower()),
            )
            selected = eligible[:COHORT_SIZE]
            for row in selected:
                row["selected"] = True
            case = _case_payload(target, selected, checked_at) if selected else None
            if case:
                CaseDefinition.model_validate(case)
                definitions.append((f"{target['package']}-{target['qualifying_release']}", case))
            ledger["cases"].append({
                "target": target, "searches": searches,
                "candidates_considered": len(rows), "eligible_count": len(eligible),
                "selected_count": len(selected), "candidates": rows,
                "eligible_ranked": [row["repository"] for row in eligible],
            })
            print(
                f"{target['package']} {target['qualifying_release']}: "
                f"considered={len(rows)} eligible={len(eligible)} selected={len(selected)}"
            )
    directory = args.output_root / "docs/phase-2"
    directory.mkdir(parents=True, exist_ok=True)
    ledger_path = directory / "cohort-selection-ledger.json"
    with ledger_path.open("x", encoding="utf-8") as handle:
        json.dump(ledger, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    for case_id, payload in definitions:
        path = args.output_root / "cases" / f"{case_id}.yaml"
        with path.open("x", encoding="utf-8") as handle:
            yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=True)
    print(ledger_path)
    return 0 if len(definitions) == 2 and all(
        item["selected_count"] >= 5 for item in ledger["cases"]
    ) else 2


if __name__ == "__main__":
    raise SystemExit(main())
