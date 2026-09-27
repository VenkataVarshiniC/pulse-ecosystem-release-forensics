"""Review outcomes and precision denominators for emitted candidates."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from pulse.detector_evaluation import (
    AnalystDecision,
    ReviewedCandidate,
    ReviewReason,
    apply_analyst_decisions,
    counts,
    grouped_counts,
    load_verified_baseline,
)
from pulse.models.evidence import LifecycleStage
from pulse.models.review import EvidenceStatus

DATA = Path("docs/phase-2/evaluation-data")
NOW = datetime(2026, 9, 27, 5, 3, tzinfo=UTC)


def _baseline(case_id: str):
    return load_verified_baseline(
        DATA / f"baseline-{case_id}.jsonl",
        DATA / f"baseline-{case_id}.manifest.json",
    )


def _decision(candidate_id: str, status: EvidenceStatus, reason: ReviewReason):
    return AnalystDecision(
        candidate_id=candidate_id, status=status, reason_code=reason,
        note="Independent analyst inspected the preserved source body.",
        reviewed_at=NOW, source_basis="Collector snapshot from a frozen run.",
    )


def test_frozen_baseline_and_review_ledger_replay() -> None:
    assert _baseline("pytest-8.0.0") == ()
    candidates = _baseline("urllib3-2.0.0")
    decisions = tuple(
        AnalystDecision.model_validate(item)
        for item in json.loads((DATA / "review-decisions.json").read_text(encoding="utf-8"))
    )
    reviewed = apply_analyst_decisions(candidates, decisions)
    ledger = tuple(
        ReviewedCandidate.model_validate_json(line)
        for line in (DATA / "review-ledger.jsonl").read_text(encoding="utf-8").splitlines()
    )
    assert reviewed == ledger
    assert counts(reviewed) == json.loads((DATA / "metrics.json").read_text(encoding="utf-8"))[
        "overall"
    ]
    assert all(item.candidate.status is EvidenceStatus.REJECTED for item in reviewed)
    assert {item.candidate.candidate_id for item in reviewed} == {
        item.candidate_id for item in candidates
    }


def test_precision_excludes_unresolved_and_handles_zero_denominator() -> None:
    base = _baseline("urllib3-2.0.0")[0]
    candidates = tuple(
        base.model_copy(update={"candidate_id": character * 24})
        for character in "abc"
    )
    decisions = (
        _decision("a" * 24, EvidenceStatus.ACCEPTED, ReviewReason.DIRECT_STAGE_EVIDENCE),
        _decision("b" * 24, EvidenceStatus.REJECTED, ReviewReason.GENERIC_DEPENDENCY_MENTION),
        _decision("c" * 24, EvidenceStatus.NEEDS_REVIEW, ReviewReason.SOURCE_UNAVAILABLE),
    )
    reviewed = apply_analyst_decisions(candidates, decisions)
    result = counts(reviewed)
    assert result == {
        "emitted": 3, "accepted": 1, "rejected": 1, "needs_review": 1,
        "reviewed": 2, "precision_numerator": 1, "precision_denominator": 2,
        "reviewed_candidate_precision": 0.5,
    }
    assert counts(())['reviewed_candidate_precision'] is None
    assert counts(reviewed[2:])["reviewed_candidate_precision"] is None


def test_rule_and_stage_aggregation_keeps_zero_rules_unavailable() -> None:
    records = tuple(
        ReviewedCandidate.model_validate_json(line)
        for line in (DATA / "review-ledger.jsonl").read_text(encoding="utf-8").splitlines()
    )
    stages, rules = grouped_counts(records)
    assert stages[LifecycleStage.MIGRATION_FRICTION.value]["precision_denominator"] == 1
    assert stages[LifecycleStage.REMEDIATION.value]["rejected"] == 1
    assert stages[LifecycleStage.OBSERVED_ADOPTION.value]["reviewed_candidate_precision"] is None
    assert rules["text.version_specific_friction"]["rejected"] == 1
    assert rules["text.version_specific_remediation"]["rejected"] == 1
    assert rules["dependency.target_accepted"]["reviewed_candidate_precision"] is None
    saved = json.loads((DATA / "metrics.json").read_text(encoding="utf-8"))
    assert stages == saved["by_lifecycle_stage"]
    assert rules == saved["by_rule"]


def test_duplicate_or_missing_decisions_fail_closed() -> None:
    candidates = _baseline("urllib3-2.0.0")
    decision = _decision(
        candidates[0].candidate_id, EvidenceStatus.REJECTED,
        ReviewReason.GENERIC_DEPENDENCY_MENTION,
    )
    with pytest.raises(ValueError, match="exactly one"):
        apply_analyst_decisions(candidates, (decision,))
    with pytest.raises(ValueError, match="duplicate"):
        apply_analyst_decisions(candidates, (decision, decision))
    with pytest.raises(ValueError, match="duplicate"):
        apply_analyst_decisions((candidates[0], candidates[0]), (decision,))


def test_invalid_status_reason_pair_is_rejected() -> None:
    with pytest.raises(ValidationError, match="direct stage evidence"):
        _decision("a" * 24, EvidenceStatus.ACCEPTED, ReviewReason.GENERIC_DEPENDENCY_MENTION)
    with pytest.raises(ValidationError, match="unresolved reason"):
        _decision("a" * 24, EvidenceStatus.NEEDS_REVIEW, ReviewReason.GENERIC_DEPENDENCY_MENTION)


def test_unreviewed_candidate_cannot_be_scored() -> None:
    base = _baseline("urllib3-2.0.0")[0]
    unreviewed = ReviewedCandidate(
        candidate=base.model_copy(update={"status": EvidenceStatus.CANDIDATE}),
        reason_code=ReviewReason.INSUFFICIENT_SOURCE_CONTEXT,
        source_basis="Collector snapshot from a frozen run.",
    )
    with pytest.raises(ValueError, match="unreviewed"):
        counts((unreviewed,))


def test_baseline_hash_guard_detects_modified_candidate(tmp_path: Path) -> None:
    source = DATA / "baseline-urllib3-2.0.0.jsonl"
    candidate_path = tmp_path / source.name
    candidate_path.write_bytes(source.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="digest mismatch"):
        load_verified_baseline(
            candidate_path, DATA / "baseline-urllib3-2.0.0.manifest.json"
        )
