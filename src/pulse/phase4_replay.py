"""Bounded, offline M4.1 replay over the verified Phase 2 evidence freeze."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from packaging.utils import canonicalize_name

from pulse.collection.manifest import LiveCollectionManifest, TaskOutcomeStatus
from pulse.collection.raw import RawSnapshot
from pulse.config.cases import load_case
from pulse.dependencies.parsers import parse_dependency_file_with_diagnostics
from pulse.detector_evaluation import load_verified_baseline
from pulse.evidence.detectors import detect_transition_candidate
from pulse.history.models import FileStateStatus, HistoricalRun, PairStatus
from pulse.history.pairing import select_ref_pair
from pulse.history.runner import _decode_content
from pulse.models.review import ReviewableEvidence
from pulse.phase2_forensics import build_phase2_report
from pulse.phase2_postgres.loader import identity
from pulse.phase2_postgres.manifest import (
    ROOT,
    VerifiedInputs,
    canonical_digest,
    sha256,
    verify_inputs,
)
from pulse.pipeline import detect_raw_candidates

MANIFEST = ROOT / "data/manifests/m4-1-rule-manifest.json"
CASES = ("pytest-8.0.0", "urllib3-2.0.0")
REVIEW_POLICY = "exact-candidate-v1"


def read_rule_manifest(path: Path = MANIFEST) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    body = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    if canonical_digest(body) != manifest["manifest_sha256"]:
        raise ValueError("Rule manifest fingerprint mismatch")
    for name, digest in manifest["source_files"].items():
        if sha256(ROOT / name) != digest:
            raise ValueError(f"Rule source drift: {name}")
    return manifest


def normalized(candidate: ReviewableEvidence) -> dict[str, Any]:
    """Exact comparison includes source span/payload and all rule-produced fields."""
    return candidate.model_dump(
        mode="json", exclude={"candidate_id", "status", "reviewer_note", "reviewed_at"}
    )


def source_origin(candidate: ReviewableEvidence) -> str:
    # This is a bounded span classification, not an assertion about the entire PR.
    excerpt = candidate.evidence[0].excerpt or ""
    if candidate.evidence[0].source_type == "pull_request" and "<em>Sourced from" in excerpt:
        return "COPIED_UPSTREAM"
    return "UNRESOLVED"


def replay_id(rule_release: str, candidate: ReviewableEvidence) -> str:
    return (
        "m41-"
        + canonical_digest({"rule_release": rule_release, "candidate": normalized(candidate)})[:32]
    )


def exact_legacy_match(
    candidate: ReviewableEvidence, legacy_by_fingerprint: dict[str, ReviewableEvidence]
) -> ReviewableEvidence | None:
    return legacy_by_fingerprint.get(canonical_digest(normalized(candidate)))


def verify_history(
    inputs: VerifiedInputs, case: str, definition: Any, history: HistoricalRun
) -> int:
    """Recheck every frozen query pairing and every captured exact-ref file parse."""
    verified = 0
    for result in history.results:
        item, capture_path = inputs.by_absolute_path(result.history_snapshot_path)
        if item["role"] != "historical_query_capture":
            raise ValueError("Historical query is not a frozen capture")
        capture = RawSnapshot.model_validate_json(capture_path.read_text(encoding="utf-8"))
        if capture.query.get("path") != result.pair.manifest_path:
            raise ValueError("Historical query path mismatch")
        if result.history_stats.termination == "complete":
            paired = select_ref_pair(
                definition, result.pair.repository, result.pair.manifest_path, capture.payload
            )
            if paired.before != result.pair.before or paired.after != result.pair.after:
                raise ValueError("Historical exact-ref pairing changed")
            if result.pair.status not in {
                paired.status,
                PairStatus.FILE_UNAVAILABLE,
                PairStatus.MALFORMED,
                PairStatus.AMBIGUOUS,
            }:
                raise ValueError("Historical pair status changed")
        for state in (result.before_state, result.after_state):
            if state is None or not state.raw_snapshot_path:
                continue
            file_item, file_path = inputs.by_absolute_path(state.raw_snapshot_path)
            if file_item["role"] != "historical_file_capture":
                raise ValueError("Historical file is not a frozen capture")
            file_capture = RawSnapshot.model_validate_json(file_path.read_text(encoding="utf-8"))
            if file_capture.query.get("ref") != state.commit_sha:
                raise ValueError("Historical file ref mismatch")
            content = _decode_content(file_capture.payload)
            if hashlib.sha256(content.encode()).hexdigest() != state.content_sha256:
                raise ValueError("Historical file content digest changed")
            observations, _ = parse_dependency_file_with_diagnostics(
                repository=state.repository,
                file_path=state.path,
                content=content,
                commit_reference=state.commit_sha,
                observed_at=state.commit_timestamp,
                source=state.source_url,
            )
            selected = tuple(
                obs
                for obs in observations
                if obs.package == canonicalize_name(definition.case.target_package)
            )
            if state.status is FileStateStatus.PARSED and selected != state.target_observations:
                raise ValueError("Historical parsed observations changed")
            verified += 1
        verified += 1
    return verified


def _write_temporary_replay(
    directory: Path,
    case: str,
    candidates: list[ReviewableEvidence],
    reviews: list[dict[str, Any]],
    collection: LiveCollectionManifest,
    history: HistoricalRun,
) -> tuple[Path, Path, Path]:
    baseline = directory / f"{case}.jsonl"
    baseline.write_text("".join(c.model_dump_json() + "\n" for c in candidates), encoding="utf-8")
    manifest = directory / f"{case}.manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "case_id": case,
                "collection_run_id": collection.run_id,
                "history_run_id": history.run_id,
                "candidate_count": len(candidates),
                "candidate_ids": [c.candidate_id for c in candidates],
                "baseline_sha256": sha256(baseline),
            }
        ),
        encoding="utf-8",
    )
    ledger = directory / f"{case}.reviews.jsonl"
    ledger.write_text(
        "".join(json.dumps(r, sort_keys=True) + "\n" for r in reviews), encoding="utf-8"
    )
    return baseline, manifest, ledger


def replay() -> dict[str, Any]:
    inputs = verify_inputs()
    if len(inputs.files) != 142:
        raise ValueError("Frozen file population changed")
    rules = read_rule_manifest()
    old_reviews = {
        row["candidate"]["candidate_id"]: row
        for line in inputs.one(CASES[0], "review_ledger")[1]
        .read_text(encoding="utf-8")
        .splitlines()
        if (row := json.loads(line))
    }
    results: dict[str, Any] = {}
    with TemporaryDirectory(prefix="pulse-m41-") as temporary:
        temp = Path(temporary)
        for case in CASES:
            definition = load_case(inputs.one(case, "case_definition")[1])
            collection_path = inputs.one(case, "collection_manifest")[1]
            history_path = inputs.one(case, "history_manifest")[1]
            collection = LiveCollectionManifest.model_validate_json(
                collection_path.read_text(encoding="utf-8")
            )
            history = HistoricalRun.model_validate_json(history_path.read_text(encoding="utf-8"))
            historical_checks = verify_history(inputs, case, definition, history)
            snapshots = {
                Path(o.snapshot_path).resolve()
                for o in collection.outcomes
                if o.status in {TaskOutcomeStatus.SUCCEEDED, TaskOutcomeStatus.PARTIAL}
                and o.snapshot_path
            }
            frozen_snapshots = {path.resolve() for _, path in inputs.entries(case, "raw_capture")}
            raw_root = collection_path.parents[4] / "raw" / case
            if snapshots != frozen_snapshots or set(raw_root.rglob("*.json")) != snapshots:
                raise ValueError("Detector input root differs from frozen collector captures")
            current = {c.candidate_id: c for c in detect_raw_candidates(definition, raw_root)}
            for item in history.results:
                if item.pair.status is PairStatus.PAIRED and item.transition is not None:
                    candidate = detect_transition_candidate(definition.case, item.transition)
                    if candidate is not None:
                        if (
                            candidate.candidate_id in current
                            and current[candidate.candidate_id] != candidate
                        ):
                            raise ValueError("Candidate identity collision")
                        current[candidate.candidate_id] = candidate
            legacy = load_verified_baseline(
                inputs.one(case, "candidate_baseline")[1],
                inputs.one(case, "candidate_baseline_manifest")[1],
            )
            old_by_fp = {canonical_digest(normalized(c)): c for c in legacy}
            if len(old_by_fp) != len(legacy):
                raise ValueError("Duplicate legacy normalized candidate")
            candidate_rows = []
            replay_candidates = []
            inherited_reviews = []
            exact_ids = set()
            for candidate in sorted(current.values(), key=lambda c: c.candidate_id):
                fingerprint = canonical_digest(normalized(candidate))
                old = exact_legacy_match(candidate, old_by_fp)
                classification = "EXACT_EQUIVALENT" if old else "NEW"
                identifier = replay_id(rules["rule_release_id"], candidate)
                replay_candidate = candidate.model_copy(update={"candidate_id": identifier})
                replay_candidates.append(replay_candidate)
                source = source_origin(candidate)
                candidate_rows.append(
                    {
                        "candidate_id": identifier,
                        "legacy_candidate_id": old.candidate_id if old else None,
                        "case_id": case,
                        "repository": str(candidate.repository),
                        "artifact": str(candidate.evidence[0].url),
                        "artifact_digest": candidate.evidence[0].content_sha256,
                        "evidence_span": candidate.evidence[0].model_dump(mode="json"),
                        "rule_id": candidate.classification_rule,
                        "rule_version": rules["rule_release_id"],
                        "lifecycle_category": candidate.lifecycle_stage.value,
                        "source_origin": source,
                        "normalized_candidate_fingerprint": fingerprint,
                        "emitted_reason": candidate.classification_reason,
                        "equivalence": classification,
                        "review_state": "INHERITED_REVIEW_EVIDENCE" if old else "REVIEW_REQUIRED",
                    }
                )
                if old:
                    exact_ids.add(old.candidate_id)
                    old_review = old_reviews[old.candidate_id]
                    if (
                        "copied upstream" in old_review["candidate"]["reviewer_note"].casefold()
                        and source != "COPIED_UPSTREAM"
                    ):
                        raise ValueError(
                            "Replay source-origin classification disagrees with frozen review"
                        )
                    copied = dict(old_review)
                    copied["candidate"] = {
                        **old_review["candidate"],
                        "candidate_id": identifier,
                    }
                    inherited_reviews.append(copied)
            missing = sorted(set(c.candidate_id for c in legacy) - exact_ids)
            report = None
            if not missing and len(inherited_reviews) == len(replay_candidates):
                baseline, baseline_manifest, ledger = _write_temporary_replay(
                    temp, case, replay_candidates, inherited_reviews, collection, history
                )
                report = build_phase2_report(
                    definition, collection_path, history_path, baseline, baseline_manifest, ledger
                )
            results[case] = {
                "legacy_candidate_count": len(legacy),
                "replay_candidate_count": len(replay_candidates),
                "historical_checks": historical_checks,
                "candidates": candidate_rows,
                "missing_legacy_candidate_ids": missing,
                "review_provenance": [
                    {
                        "original_review_id": str(
                            identity("review", case, r["candidate"]["candidate_id"], 1, 1)
                        ),
                        "original_candidate_id": r["candidate"]["candidate_id"],
                        "replay_candidate_id": next(
                            c["candidate_id"]
                            for c in candidate_rows
                            if c["legacy_candidate_id"] == r["candidate"]["candidate_id"]
                        ),
                        "equivalence_basis": "EXACT_EQUIVALENT: normalized full candidate payload",
                        "original_review_decision": r["candidate"]["status"],
                        "reuse_policy": REVIEW_POLICY,
                    }
                    for r in (old_reviews[old_id] for old_id in sorted(exact_ids))
                ],
                "finding_status_counts": dict(
                    sorted(
                        Counter(
                            finding.state.value
                            for repo in report.repositories
                            for finding in repo.stage_findings.values()
                        ).items()
                    )
                )
                if report
                else None,
                "replay_sufficiency_counts": dict(
                    sorted(
                        Counter(
                            "SUFFICIENT" if value else "INSUFFICIENT"
                            for repo in report.repositories
                            for value in repo.stage_sufficiency.values()
                        ).items()
                    )
                )
                if report
                else None,
                "report_fingerprint": canonical_digest(report.model_dump(mode="json"))
                if report
                else None,
                "report": report.model_dump(mode="json") if report else None,
            }
    return {
        "input_manifest_sha256": inputs.manifest["manifest_sha256"],
        "frozen_file_count": len(inputs.files),
        "rule_release_id": rules["rule_release_id"],
        "rule_manifest_sha256": rules["manifest_sha256"],
        "review_policy": REVIEW_POLICY,
        "cases": results,
    }
