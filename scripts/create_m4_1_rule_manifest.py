"""Freeze the exact pre-replay rule sources; run once at the M4.1 base commit."""

from __future__ import annotations

import json

from pulse.phase2_postgres.manifest import ROOT, canonical_digest
from pulse.phase4_replay import source_sha256

BASE_COMMIT = "b2b638bb97c8b6a136a8f9f3f19334547219ec19"
RULE_FILES = (
    "src/pulse/analysis/forensics.py",
    "src/pulse/collection/journal.py",
    "src/pulse/collection/planner.py",
    "src/pulse/config/cases.py",
    "src/pulse/dependencies/models.py",
    "src/pulse/dependencies/parsers.py",
    "src/pulse/dependencies/transitions.py",
    "src/pulse/detector_evaluation.py",
    "src/pulse/evidence/detectors.py",
    "src/pulse/history/models.py",
    "src/pulse/history/pairing.py",
    "src/pulse/history/runner.py",
    "src/pulse/models/review.py",
    "src/pulse/phase2_forensics.py",
    "src/pulse/phase2_postgres/loader.py",
    "src/pulse/phase4_replay.py",
    "src/pulse/pipeline.py",
    "scripts/run_m4_1_replay.py",
)


def build_manifest() -> dict:
    body = {
        "schema": "pulse.m4-1-rule-manifest.v1",
        "created_at": "2026-09-29T01:02:05Z",
        "source_git_commit": BASE_COMMIT,
        "scope": (
            "Offline replay of the two frozen Phase 2 cases; current rules, "
            "not historical attribution"
        ),
        "source_hash_encoding": "sha256-of-file-bytes-with-CRLF-normalized-to-LF",
        "source_files": {name: source_sha256(ROOT / name) for name in RULE_FILES},
        "candidate_rules": [
            "text.version_specific_friction",
            "text.version_specific_remediation",
            "text.support_release",
            "dependency.target_excluded",
            "dependency.target_accepted",
        ],
        "evaluation_components": [
            "manifest_path_first_change",
            "parse_dependency_file_with_diagnostics",
            "detect_transition",
            "historical_context",
            "_coverage",
            "_release_boundary_dependency_supported",
            "_finding",
            "accepted_to_events",
            "exact-candidate-v1",
        ],
        "parser_evaluation_version": "source-file-sha256-bound",
        "python_runtime": "CPython 3.14; packaging and Pydantic versions locked by uv.lock",
        "known_limitations": [
            "The source commit identifies current replay rules, not historical Phase 2 execution.",
            "No new source collection; unobserved adoption and recovery remain unavailable.",
            "Historical capture replay verifies pairing and parsed observations "
            "but retains frozen collection attempt metadata.",
        ],
    }
    body["rule_release_id"] = f"rule-replay-{BASE_COMMIT[:12]}-{canonical_digest(body)[:16]}"
    return {**body, "manifest_sha256": canonical_digest(body)}


def main() -> None:
    output = ROOT / "data/manifests/m4-1-rule-manifest.json"
    candidate = build_manifest()
    if output.exists():
        existing = json.loads(output.read_text(encoding="utf-8"))
        if existing != candidate:
            raise SystemExit("Frozen M4.1 rule manifest differs; do not overwrite")
    else:
        output.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(candidate["rule_release_id"], candidate["manifest_sha256"])


if __name__ == "__main__":
    main()
