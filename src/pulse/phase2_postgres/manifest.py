"""Verify the committed M2.2 input manifest before opening a database connection."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "data/manifests/phase2-postgres-load-manifest.json"
CASES = frozenset({"pytest-8.0.0", "urllib3-2.0.0"})


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class VerifiedInputs:
    manifest: dict[str, Any]
    files: dict[tuple[str, str], Path]

    def entries(self, case: str, role: str) -> list[tuple[dict[str, Any], Path]]:
        selected = []
        for item in self.manifest["inputs"]:
            if item["role"] == role and item["case"] in (case, "both"):
                selected.append((item, self.files[item["root"], item["path"]]))
        return selected

    def one(self, case: str, role: str) -> tuple[dict[str, Any], Path]:
        matches = self.entries(case, role)
        if len(matches) != 1:
            raise ValueError(f"Expected one {role} for {case}; found {len(matches)}")
        return matches[0]

    def by_absolute_path(self, path: str) -> tuple[dict[str, Any], Path]:
        resolved = Path(path).resolve(strict=True)
        for item in self.manifest["inputs"]:
            found = self.files[item["root"], item["path"]]
            if found == resolved:
                return item, found
        raise ValueError("Source file is not declared in the frozen M2.2 manifest")


def verify_inputs(manifest_path: Path = MANIFEST) -> VerifiedInputs:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = manifest.get("manifest_sha256")
    body = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    if canonical_digest(body) != expected:
        raise ValueError("Frozen input manifest fingerprint mismatch")
    if set(manifest["cases"]) != CASES:
        raise ValueError("Input manifest case population differs from the two authorized cases")
    dotenv = dotenv_values(ROOT / ".env")
    files: dict[tuple[str, str], Path] = {}
    seen: set[tuple[str, str]] = set()
    roots: dict[str, Path] = {"repo": ROOT.resolve()}
    for logical, env_name in manifest["root_environment"].items():
        value = os.environ.get(env_name) or dotenv.get(env_name)
        if not value:
            raise ValueError(f"Missing external frozen root setting {env_name}")
        roots[logical] = Path(value).resolve(strict=True)
    for item in manifest["inputs"]:
        key = (item["root"], item["path"])
        if key in seen:
            raise ValueError(f"Duplicate frozen input identity: {key}")
        seen.add(key)
        if item["case"] not in CASES | {"both"}:
            raise ValueError("Input outside declared frozen cases")
        collector_roles = {
            "collector_task_attempt", "raw_capture", "historical_query_capture",
            "historical_file_capture", "collection_manifest", "history_manifest",
        }
        method = "collector" if item["role"] in collector_roles else "derived_frozen"
        if item["capture_method"] != method or not item["interpretation"]:
            raise ValueError("Frozen input role/capture/interpretation mismatch")
        relative = Path(item["path"])
        if relative.is_absolute() or ".." in relative.parts or item["root"] not in roots:
            raise ValueError("Unsafe or unknown logical input path")
        root = roots[item["root"]]
        full = (root / relative).resolve(strict=True)
        if not full.is_relative_to(root) or not full.is_file():
            raise ValueError("Frozen input escapes its configured root or is not a file")
        actual = sha256(full)
        if actual != item["sha256"]:
            raise ValueError(f"Frozen input hash mismatch: {item['root']}/{item['path']}")
        files[key] = full
    return VerifiedInputs(manifest=manifest, files=files)
