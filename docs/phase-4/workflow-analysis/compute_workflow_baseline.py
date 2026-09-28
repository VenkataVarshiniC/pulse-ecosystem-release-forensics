"""Reproduce bounded descriptive metrics from the frozen Phase 3 PR observations."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import median
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "docs/phase-3/secondary-research/github-pr-observations.jsonl"
OUTPUT = Path(__file__).with_name("workflow-metrics.json")
SAMPLES = {"base": 20, "discussion": 7}


def percentile(values: list[float], fraction: float) -> float:
    """Return an interpolated (n-1) percentile, including endpoints."""
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = int(position)
    return round(
        ordered[lower]
        + (ordered[min(lower + 1, len(ordered) - 1)] - ordered[lower]) * (position - lower),
        2,
    )


def exception_labels(row: dict[str, Any]) -> list[str]:
    """Use only explicit frozen codes; labels may co-occur on one PR."""
    concerns = row["concerns"]
    work = row["additional_work"]
    labels: list[str] = []
    if "test_failure" in concerns:
        labels.append("test_failure")
    if "compatibility" in concerns:
        labels.append("compatibility_concern")
    if "version_constraint" in concerns:
        labels.append("retained_older_version")
    for key, label in (
        ("production_code_modification", "source_code_modification"),
        ("test_modification", "test_modification"),
        ("configuration_modification", "configuration_change"),
        ("rebase_recreation", "rebase_completed"),
    ):
        if work[key] is True:
            labels.append(label)
    if row["reason_for_close"] == "superseded":
        labels.append("superseded")
    if row["reason_for_close"] == "no_longer_needed_per_bot":
        if row["bot_command_usage"] is True:
            labels.append("rebase_requested_already_up_to_date_reply")
        else:
            labels.append("other_explicit_bot_close")
    if row["reason_for_close"] == "ignored_per_bot":
        labels.append("other_explicit_bot_close")
    return labels


def duration_summary(rows: list[dict[str, Any]]) -> dict[str, float | int | None]:
    values = [
        float(row["pr_resolution_duration_hours"])
        for row in rows
        if row["outcome"] in {"merged", "closed_without_merge"}
        and row["pr_resolution_duration_hours"] is not None
    ]
    if not values:
        return {
            "n": 0,
            "min": None,
            "q1": None,
            "median": None,
            "q3": None,
            "max": None,
            "iqr": None,
        }
    q1, q3 = percentile(values, 0.25), percentile(values, 0.75)
    return {
        "n": len(values),
        "min": min(values),
        "q1": q1,
        "median": round(median(values), 2),
        "q3": q3,
        "max": max(values),
        "iqr": round(q3 - q1, 2),
    }


def metric(
    metric_id: str, sample: str, numerator: int, denominator: int, interpretation: str
) -> dict[str, Any]:
    return {
        "metric_id": metric_id,
        "sample": sample,
        "n": numerator,
        "d": denominator,
        "value": round(numerator / denominator, 4) if denominator else None,
        "unit": "share_of_frozen_base_prs",
        "interpretation": interpretation,
        "limitation": (
            "Descriptive within the frozen, title/first-page-biased Dependabot base sample; "
            "not a population estimate or measure of private work."
        ),
    }


def validate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    assert len(rows) == 27
    assert Counter(row["sample_type"] for row in rows) == SAMPLES
    keys = {(row["sample_type"], row["repository"].lower(), row["pr_number"]) for row in rows}
    assert len(keys) == 27
    missing: Counter[str] = Counter()
    for row in rows:
        assert row["url"].lower() == (
            f"https://github.com/{row['repository']}/pull/{row['pr_number']}".lower()
        )
        assert row["sample_type"] in SAMPLES
        assert row["initiator"] in {"bot", "human", "unclear"}
        assert row["update_mechanism"] in {"dependabot", "renovate", "manual", "other", "unknown"}
        assert row["outcome"] in {"merged", "closed_without_merge", "open_at_cutoff"}
        assert isinstance(row["evidence_present"], dict)
        assert isinstance(row["additional_work"], dict)
        assert all(isinstance(value, bool) for value in row["evidence_present"].values())
        assert row["copied_upstream_release_text"] in {True, False}
        assert row["downstream_statement_present"] in {True, False}
        assert row["downstream_statement_present"] == (row["downstream_statement_kind"] is not None)
        assert row["approval"] in {True, False}
        assert row["human_interaction_present"] in {True, False}
        assert row["human_interaction_present"] == (row["visible_human_interaction_count"] > 0)
        assert not row["approval"] or row["human_interaction_present"]
        assert not row["copied_upstream_release_text"] or (
            row["evidence_present"]["release_notes"] or row["evidence_present"]["changelog"]
        )
        assert row["outcome"] != "merged" or row["reason_for_close"] is None
        assert row["outcome"] != "closed_without_merge" or row["reason_for_close"] is not None
        assert (
            row["pr_resolution_duration_hours"] is None or row["pr_resolution_duration_hours"] >= 0
        )
        assert row["observed_on"] == "2026-09-27"
        for name in ("previous_version", "proposed_version", "downstream_statement_kind"):
            if row[name] is None:
                missing[name] += 1
        if row["additional_work"]["lockfile_regeneration"] is None:
            missing["lockfile_regeneration"] += 1
    return {
        "rows": len(rows),
        "sample_counts": dict(Counter(row["sample_type"] for row in rows)),
        "unique_sample_repository_pr_keys": len(keys),
        "null_field_counts": dict(sorted(missing.items())),
    }


def main() -> None:
    source_bytes = SOURCE.read_bytes()
    rows = [json.loads(line) for line in source_bytes.decode("utf-8").splitlines() if line.strip()]
    audit = validate(rows)
    base = [row for row in rows if row["sample_type"] == "base"]
    discussion = [row for row in rows if row["sample_type"] == "discussion"]
    metrics = [
        metric(
            "WF-MET-001",
            "base",
            sum(r["human_interaction_present"] for r in base),
            20,
            "Visible public human interaction.",
        ),
        metric(
            "WF-MET-002", "base", sum(r["approval"] for r in base), 20, "Explicit visible approval."
        ),
        metric(
            "WF-MET-003",
            "base",
            sum(r["outcome"] == "merged" for r in base),
            sum(r["outcome"] != "open_at_cutoff" for r in base),
            "Merged terminal PR disposition, not successful migration.",
        ),
        metric(
            "WF-MET-004",
            "base",
            sum(r["reason_for_close"] == "superseded" for r in base),
            20,
            "Explicit supersession, not wasted work.",
        ),
        metric(
            "WF-MET-005",
            "base",
            sum(
                any(
                    r["additional_work"][k] is True
                    for k in (
                        "production_code_modification",
                        "test_modification",
                        "configuration_modification",
                    )
                )
                for r in base
            ),
            20,
            "Coded source, test, or configuration modification beyond dependency files.",
        ),
        metric(
            "WF-MET-006",
            "base",
            sum(r["copied_upstream_release_text"] for r in base),
            20,
            "Copied upstream notes/changelog in PR body.",
        ),
        metric(
            "WF-MET-007",
            "base",
            sum(bool(exception_labels(r)) for r in base),
            20,
            "At least one explicitly coded workflow exception; multi-label, not severity.",
        ),
        metric(
            "WF-MET-008",
            "base",
            sum(r["evidence_present"]["compatibility_score"] for r in base),
            20,
            "Compatibility badge/link present, score unverified.",
        ),
    ]
    base_duration = duration_summary(base)
    metrics.append(
        {
            "metric_id": "WF-MET-009",
            "sample": "base",
            "n": base_duration["n"],
            "d": len(base),
            "value": base_duration["median"],
            "unit": "elapsed_hours_median",
            "interpretation": (
                "Elapsed creation-to-terminal time; distribution and quartile method required."
            ),
            "limitation": "Not engineering time, productivity, delay cause, or time saved.",
        }
    )
    by_sample = {}
    for name, sample_rows in (("base", base), ("discussion", discussion)):
        labels = [exception_labels(row) for row in sample_rows]
        by_sample[name] = {
            "count": len(sample_rows),
            "outcomes": dict(sorted(Counter(row["outcome"] for row in sample_rows).items())),
            "close_reasons": dict(
                sorted(
                    Counter(
                        row["reason_for_close"] for row in sample_rows if row["reason_for_close"]
                    ).items()
                )
            ),
            "human_interaction": sum(row["human_interaction_present"] for row in sample_rows),
            "human_review": sum(row["human_review_present"] for row in sample_rows),
            "approval": sum(row["approval"] for row in sample_rows),
            "bot_command": sum(row["bot_command_usage"] for row in sample_rows),
            "substantive_comment": sum(
                row["downstream_statement_kind"] == "substantive_review_comment"
                for row in sample_rows
            ),
            "zero_visible_interaction": sum(
                not row["human_interaction_present"] for row in sample_rows
            ),
            "evidence": dict(
                sorted(
                    (key, sum(row["evidence_present"][key] for row in sample_rows))
                    for key in sample_rows[0]["evidence_present"]
                )
            ),
            "copied_upstream_text": sum(row["copied_upstream_release_text"] for row in sample_rows),
            "exception_labels": dict(
                sorted(Counter(label for case in labels for label in case).items())
            ),
            "exception_label_count_per_pr": dict(
                sorted(Counter(len(case) for case in labels).items())
            ),
            "duration_hours": duration_summary(sample_rows),
        }
    output = {
        "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "method": (
            "Frozen Phase 3 observations; descriptive only; base and purposive "
            "discussion samples never pooled for rates."
        ),
        "audit": audit,
        "metrics": metrics,
        "samples": by_sample,
        "base_duration_segments_hours": {
            "merged": duration_summary([r for r in base if r["outcome"] == "merged"]),
            "closed_without_merge": duration_summary(
                [r for r in base if r["outcome"] == "closed_without_merge"]
            ),
            "visible_human_interaction": duration_summary(
                [r for r in base if r["human_interaction_present"]]
            ),
            "no_visible_human_interaction": duration_summary(
                [r for r in base if not r["human_interaction_present"]]
            ),
            "coded_exception": duration_summary([r for r in base if exception_labels(r)]),
            "no_coded_exception": duration_summary([r for r in base if not exception_labels(r)]),
        },
        "base_segments": {
            "manifest_diff": sum(r["evidence_present"]["manifest_diff"] for r in base),
            "lockfile_diff": sum(r["evidence_present"]["lockfile_diff"] for r in base),
            "grouped_update": sum(r["dependency"] == "multiple" for r in base),
            "single_update": sum(r["dependency"] != "multiple" for r in base),
        },
    }
    OUTPUT.write_text(
        json.dumps(output, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
