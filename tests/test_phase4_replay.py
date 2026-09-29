"""Review inheritance is limited to full candidate identity under pinned replay rules."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from pulse.detector_evaluation import load_verified_baseline
from pulse.phase2_postgres.manifest import ROOT, canonical_digest, sha256
from pulse.phase4_replay import (
    exact_legacy_match,
    normalized,
    read_rule_manifest,
    replay_id,
    source_origin,
)


def _legacy():
    root = ROOT / "docs/phase-2/evaluation-data"
    return load_verified_baseline(
        root / "baseline-urllib3-2.0.0.jsonl",
        root / "baseline-urllib3-2.0.0.manifest.json",
    )


def test_replay_candidate_is_exact_only_when_full_payload_matches() -> None:
    candidate = _legacy()[0]
    lookup = {canonical_digest(normalized(candidate)): candidate}
    assert exact_legacy_match(candidate, lookup) == candidate
    assert (
        exact_legacy_match(candidate.model_copy(update={"title": "Different context"}), lookup)
        is None
    )
    assert exact_legacy_match(candidate.model_copy(update={"evidence": tuple()}), lookup) is None


def test_replay_identity_and_copied_source_span() -> None:
    candidate = _legacy()[0]
    rules = read_rule_manifest()
    assert replay_id(rules["rule_release_id"], candidate).startswith("m41-")
    assert replay_id(rules["rule_release_id"], candidate) != candidate.candidate_id
    assert source_origin(candidate) == "COPIED_UPSTREAM"
    altered = candidate.model_copy(update={"title": "Other"})
    assert replay_id(rules["rule_release_id"], altered) != replay_id(
        rules["rule_release_id"], candidate
    )


def test_rule_manifest_is_pinned_to_existing_sources() -> None:
    rules = read_rule_manifest()
    assert len(rules["source_files"]) == 18
    assert rules["source_git_commit"] == "b2b638bb97c8b6a136a8f9f3f19334547219ec19"
    assert Path(ROOT / "data/manifests/m4-1-rule-manifest.json").is_file()
    for name, expected in rules["source_files"].items():
        source = subprocess.run(
            ["git", "show", f"{rules['source_git_commit']}:{name}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert hashlib.sha256(source.replace(b"\r\n", b"\n")).hexdigest() == expected


def test_bi_manifest_does_not_claim_a_published_replay_snapshot() -> None:
    release = json.loads(
        (ROOT / "data/manifests/m4-1-bi-release-manifest.json").read_text(encoding="utf-8")
    )
    assert release["rule_manifest_sha256"] == read_rule_manifest()["manifest_sha256"]
    assert release["offline_replay_sha256"] == sha256(ROOT / "data/processed/m4-1/replay.json")
    assert release["snapshot_id"] is None
    assert release["metric_baseline_fingerprint"] is None
    assert release["publication_state"] == "HOLD_NO_GOVERNED_SNAPSHOT"
