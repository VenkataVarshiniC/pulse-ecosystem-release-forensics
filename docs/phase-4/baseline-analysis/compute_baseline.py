"""Analysis-only / non-production Phase 4 baseline over frozen local artifacts.

No network calls, collector changes, database writes, or synthetic observations.
The optional freeze step copies a compact audit of already-preserved live journals.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
CASES = ("pytest-8.0.0", "urllib3-2.0.0")
STAGES = (
    "adoption_readiness",
    "observed_adoption",
    "migration_friction",
    "remediation",
    "recovery_signal",
)
CORE = ("repository_metadata", "issues", "pull_requests", "commits")
AUDIT_VERSION = "1.0"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_record(path: Path, role: str, case: str) -> dict[str, str]:
    try:
        display_path = str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        display_path = str(path)
    return {"path": display_path, "sha256": digest(path), "role": role, "case": case}


def freeze_run(manifest_path: Path, external: list[dict[str, str]]) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    case = manifest["case_id"]
    external.append(source_record(manifest_path, "collection manifest", case))
    run_dir = manifest_path.parent
    planned = {task["task_id"]: task for task in manifest["planned_tasks"]}
    outcomes = {row["task_id"]: row for row in manifest["outcomes"]}
    assert len(planned) == len(outcomes) == len(manifest["planned_tasks"])
    attempts: dict[str, dict[str, Any]] = {}
    for path in sorted(run_dir.glob("*.attempt.json")):
        row = read_json(path)
        task_id = row["task"]["task_id"]
        assert task_id not in attempts and task_id in planned
        assert row["task"] == planned[task_id]
        assert row["outcome"] == outcomes[task_id]
        assert row["run_id"] == manifest["run_id"]
        assert row["capture_method"] == "collector"
        snapshot_path = row["outcome"].get("snapshot_path")
        if snapshot_path:
            assert digest(Path(snapshot_path)) == row["snapshot_sha256"]
        attempts[task_id] = {
            "attempt_id": row["attempt_id"],
            "task_id": task_id,
            "requirement": row["task"]["requirement"],
            "source": row["task"]["source"],
            "kind": row["task"]["kind"],
            "repository": row["task"]["repository"],
            "status": row["outcome"]["status"],
            "retry_count": row["stats"]["retry_count"],
            "request_count": len(row["stats"]["requests"]),
            "capture_method": row["capture_method"],
            "snapshot_sha256": row["snapshot_sha256"],
            "reused_from_attempt": row["reused_from_attempt"],
        }
        external.append(source_record(path, "collector task attempt", case))
    assert set(attempts) == set(planned)
    return {
        "case_id": case,
        "run_id": manifest["run_id"],
        "operational_status": manifest["status"],
        "tasks": [attempts[task_id] for task_id in sorted(attempts)],
    }


def freeze() -> None:
    external: list[dict[str, str]] = []
    runs: dict[str, Any] = {}
    for case in CASES:
        baseline_manifest = read_json(
            ROOT / f"docs/phase-2/evaluation-data/baseline-{case}.manifest.json"
        )
        runs[case] = freeze_run(Path(baseline_manifest["collection_manifest"]), external)
        external.append(
            source_record(Path(baseline_manifest["history_manifest"]), "history manifest", case)
        )

    # Separate Milestone 1 live HTTPX smoke/resume validation, never pooled into
    # the two Phase 2 frozen release-case cohort metrics.
    resume_root = Path(r"C:\Users\venka\pulse-phase2-m1-final-live\data\interim\httpx-0.28.0\runs")
    first = freeze_run(resume_root / "218a9c713b344d0cbc48f3fb20c91b48" / "manifest.json", external)
    resumed = freeze_run(
        resume_root / "ccae40970dac4573896892a9447bf2aa" / "manifest.json", external
    )
    assert len(first["tasks"]) == len(resumed["tasks"]) == 11
    first_ids = {task["attempt_id"] for task in first["tasks"]}
    assert all(task["reused_from_attempt"] in first_ids for task in resumed["tasks"])
    assert all(task["request_count"] == 0 for task in resumed["tasks"])
    write_json(
        OUT / "frozen-task-audit.json",
        {
            "version": AUDIT_VERSION,
            "release_cases": runs,
            "separate_httpx_resume_validation": {"first": first, "resumed": resumed},
            "external_source_files": sorted(external, key=lambda x: x["path"]),
            "boundary": (
                "Compact analysis-only extraction; raw snapshots are external and not copied."
            ),
        },
    )
    write_manifest()


def write_manifest() -> None:
    audit = read_json(OUT / "frozen-task-audit.json")
    files = []
    for case in CASES:
        for path, role in (
            (ROOT / f"cases/{case}.yaml", "frozen case definition"),
            (ROOT / f"data/processed/phase-2/{case}/forensics.json", "verified report"),
            (ROOT / f"data/processed/phase-2/{case}/accepted-evidence.jsonl", "accepted ledger"),
            (ROOT / f"docs/phase-2/generated/{case}-forensics.md", "human report"),
            (ROOT / f"docs/phase-2/evaluation-data/baseline-{case}.jsonl", "candidate baseline"),
            (
                ROOT / f"docs/phase-2/evaluation-data/baseline-{case}.manifest.json",
                "baseline identity",
            ),
        ):
            files.append(source_record(path, role, case))
    for rel, role in (
        ("docs/phase-2/evaluation-data/review-ledger.jsonl", "terminal review ledger"),
        ("docs/phase-2/evaluation-data/end-to-end-validation.json", "cross-case replay summary"),
        ("docs/phase-2/evaluation-data/metrics.json", "detector evaluation metrics"),
    ):
        files.append(source_record(ROOT / rel, role, "both"))
    files.append(source_record(OUT / "frozen-task-audit.json", "frozen task extraction", "both"))
    replay = OUT / "replay-audit.json"
    if replay.exists():
        files.append(source_record(replay, "new verified replay attempts", "both"))
    write_json(
        OUT / "input-manifest.json",
        {
            "version": AUDIT_VERSION,
            "local_files": sorted(files, key=lambda x: x["path"]),
            "external_origins": audit["external_source_files"],
            "boundary": "Only existing frozen PULSE evidence; no external outcome data added.",
        },
    )


def verify_replay() -> None:
    paths = [ROOT / f"data/processed/phase-2/{case}/forensics.json" for case in CASES] + [
        ROOT / "docs/phase-2/evaluation-data/end-to-end-validation.json"
    ]
    initial = {str(path.relative_to(ROOT)).replace("\\", "/"): digest(path) for path in paths}
    attempts = []
    command = [sys.executable, str(ROOT / "scripts/reproduce_phase2_forensics.py")]
    for number in (1, 2):
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
        observed = {str(path.relative_to(ROOT)).replace("\\", "/"): digest(path) for path in paths}
        attempts.append({"attempt": number, "matched_frozen_outputs": observed == initial})
        assert observed == initial, "Frozen Phase 2 replay changed committed analytical output"
    write_json(
        OUT / "replay-audit.json",
        {
            "version": AUDIT_VERSION,
            "command": "uv run python scripts/reproduce_phase2_forensics.py",
            "attempts": attempts,
            "output_sha256": initial,
        },
    )
    write_manifest()


def result(
    metric: str,
    case: str,
    numerator: int | None,
    denominator: int | None,
    *,
    grain: str,
    unit: str = "proportion",
    status: str = "COMPUTABLE",
    filters: str = "frozen declared case and report version",
    exclusions: str = "none beyond contract",
    unavailable_reason: str | None = None,
    interpretation_boundary: str,
) -> dict[str, Any]:
    if denominator == 0:
        status = "UNAVAILABLE_UNDEFINED_DENOMINATOR"
        unavailable_reason = "Eligible denominator is zero in this case."
    value = numerator / denominator if numerator is not None and denominator else None
    return {
        "metric_id": metric,
        "metric_version": AUDIT_VERSION,
        "case": case,
        "numerator": numerator,
        "denominator": denominator,
        "value": value,
        "unit": unit,
        "status": status,
        "grain": grain,
        "filters": filters,
        "exclusions": exclusions,
        "unavailable_reason": unavailable_reason,
        "interpretation_boundary": interpretation_boundary,
    }


def calculate() -> list[dict[str, Any]]:
    audit = read_json(OUT / "frozen-task-audit.json")
    replay = read_json(OUT / "replay-audit.json")
    assert all(row["matched_frozen_outputs"] for row in replay["attempts"])
    ledger = [
        json.loads(line)
        for line in (ROOT / "docs/phase-2/evaluation-data/review-ledger.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    reviews = {row["candidate"]["candidate_id"]: row for row in ledger}
    assert len(reviews) == len(ledger)
    results: list[dict[str, Any]] = []
    for case in CASES:
        report = read_json(ROOT / f"data/processed/phase-2/{case}/forensics.json")
        members = report["repositories"]
        member_names = [row["repository"] for row in members]
        assert len(set(member_names)) == len(members) == len(report["frozen_cohort"])
        assert set(member_names) == set(report["frozen_cohort"])
        tasks = audit["release_cases"][case]["tasks"]
        candidates = [
            json.loads(line)
            for line in (ROOT / f"docs/phase-2/evaluation-data/baseline-{case}.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        ]
        candidate_ids = [row["candidate_id"] for row in candidates]
        assert len(set(candidate_ids)) == len(candidates)
        assert all(row["case_id"] == case for row in candidates)
        assert all(row["capture_method"] == "collector" for row in tasks)
        assert len(tasks) == report["collection_task_counts"]["planned"]
        reviewed = [reviews[cid] for cid in candidate_ids if cid in reviews]
        accepted = sum(row["candidate"]["status"] == "accepted" for row in reviewed)
        rejected = sum(row["candidate"]["status"] == "rejected" for row in reviewed)
        terminal = accepted + rejected
        assert len(reviewed) == len(candidates) and terminal == len(candidates)
        assert report["emitted_candidate_count"] == len(candidates)
        assert report["accepted_candidate_count"] == accepted
        assert report["rejected_candidate_count"] == rejected

        def add(
            metric: str,
            n: int | None,
            d: int | None,
            grain: str,
            boundary: str,
            case_id: str = case,
            **kw: Any,
        ) -> None:
            results.append(
                result(
                    metric,
                    case_id,
                    n,
                    d,
                    grain=grain,
                    interpretation_boundary=boundary,
                    **kw,
                )
            )

        add(
            "MET-001",
            sum(
                all(row["collection_coverage"][src]["state"] == "complete" for src in CORE)
                for row in members
            ),
            len(members),
            "case × repository",
            "Planned core collection, not analytical sufficiency.",
        )
        add(
            "MET-002",
            sum(
                row["historical_dependency_context"] == "historically_supported" for row in members
            ),
            len(members),
            "case × repository",
            "Exact-ref declaration coverage, not adoption.",
        )
        add(
            "MET-008",
            sum(row["emitted_candidate_count"] > 0 for row in members),
            len(members),
            "case × repository",
            "Rule emissions, not impact incidence.",
        )
        add(
            "MET-009",
            accepted,
            terminal,
            "candidate",
            "Reviewed emitted set only; not recall or population precision.",
            exclusions="unreviewed/NEEDS_REVIEW",
        )
        add(
            "MET-010",
            rejected,
            terminal,
            "candidate",
            "Reviewed emitted set only; not labor burden.",
            exclusions="unreviewed/NEEDS_REVIEW",
        )
        add(
            "MET-011",
            len(candidates) - terminal,
            len(candidates),
            "candidate",
            "No emission does not imply no event.",
        )
        add(
            "MET-022",
            len(candidates),
            len(members),
            "candidate / case member",
            "Candidates per declared member, not event rate.",
            unit="candidates_per_member",
        )
        required = [row for row in tasks if row["requirement"] == "required"]
        optional = [row for row in tasks if row["requirement"] == "optional_probe"]
        add(
            "MET-016",
            sum(row["status"] == "succeeded" for row in required),
            len(required),
            "run × task",
            "Required operational task success, not stage sufficiency.",
        )
        add(
            "MET-017",
            sum(row["status"] == "not_found" for row in optional),
            len(optional),
            "run × optional task",
            "Verified optional 404, not historical absence.",
        )
        add(
            "MET-018",
            sum(row["retry_count"] > 0 for row in tasks),
            len(tasks),
            "run × attempted task",
            "Observed retries in preserved attempts only.",
        )
        add(
            "MET-020",
            len(replay["attempts"]),
            len(replay["attempts"]),
            "case × replay attempt",
            "Same frozen inputs/output; not live source stability.",
            filters=f"{case}; two verified replay attempts",
        )
        for stage in STAGES:
            assert all(stage in row["stage_findings"] for row in members)
            add(
                "MET-005",
                sum(row["stage_sufficiency"][stage] for row in members),
                len(members),
                "case × repository × category",
                "Current Phase 2 bounded stage rule only.",
                filters=f"{case}; category={stage}",
            )
            add(
                "MET-012",
                sum(
                    row["stage_findings"][stage]["state"] == "unknown_insufficient_data"
                    for row in members
                ),
                len(members),
                "case × repository × reported category",
                "Reported-category diagnostic; required completion question set unvalidated.",
                status="PARTIALLY_COMPUTABLE",
                filters=f"{case}; reported category={stage}",
            )
        # Partial and unavailable contracts retain null numeric results. They are
        # never silently represented as zero.
        gaps = {
            "MET-003": (
                "UNAVAILABLE_MISSING_SOURCE",
                "No qualified installed/resolved target-version source.",
            ),
            "MET-004": (
                "PARTIALLY_COMPUTABLE",
                "Source statuses exist; explicit versioned stage-required source "
                "map is not a frozen analytical field.",
            ),
            "MET-006": (
                "UNAVAILABLE_STAKEHOLDER_DEFINITION",
                "Required repository completion-question set is unvalidated.",
            ),
            "MET-007": (
                "UNAVAILABLE_UNDEFINED_DENOMINATOR",
                "Recovery-eligible set/window and downstream source are undefined.",
            ),
            "MET-013": (
                "PARTIALLY_COMPUTABLE",
                "Repository missing-source labels exist; not reason-coded per "
                "UNKNOWN member-stage.",
            ),
            "MET-014": (
                "UNAVAILABLE_MISSING_FIELD",
                "No complete explicit conflict taxonomy/assessment across member-stage pairs.",
            ),
            "MET-015": (
                "PARTIALLY_COMPUTABLE",
                "Missing-source labels are not linked to each UNKNOWN category "
                "or required-source set.",
            ),
            "MET-019": (
                "PARTIALLY_COMPUTABLE",
                "No resume run in either frozen release case; separate HTTPX "
                "smoke has verified reuse.",
            ),
            "MET-021": (
                "UNAVAILABLE_UNDEFINED_DENOMINATOR",
                "No YES finding exists; accepted-finding denominator is zero.",
            ),
            "MET-023": (
                "UNAVAILABLE_MISSING_FIELD",
                "Candidate emission timestamp is absent; occurred_at is source "
                "event time, not emission time.",
            ),
        }
        for metric, (status, reason) in gaps.items():
            add(
                metric,
                None,
                None,
                "see metric contract",
                "No numeric release-case value is asserted.",
                status=status,
                unavailable_reason=reason,
            )
    return sorted(results, key=lambda row: (row["case"], row["metric_id"], row["filters"]))


def write_results() -> None:
    manifest = read_json(OUT / "input-manifest.json")
    for item in manifest["local_files"]:
        assert digest(ROOT / item["path"]) == item["sha256"], item["path"]
    rows = calculate()
    write_json(
        OUT / "baseline-metrics.json",
        {
            "version": AUDIT_VERSION,
            "scope": "two separate frozen Phase 2 convenience cases",
            "results": rows,
        },
    )
    lines = [
        "# Phase 4 Milestone 1A — computed baseline",
        "",
        "Analysis-only, non-production. Percentages describe each frozen "
        "validation case, not the ecosystem. `—` means unavailable, not zero.",
        "",
        "| Case | Metric | Filter | N | D | Value | Status | Boundary / reason |",
        "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        value = (
            "—"
            if row["value"] is None
            else (
                f"{row['value']:.3f} candidates/member"
                if row["unit"] == "candidates_per_member"
                else f"{row['value'] * 100:.1f}%"
            )
        )
        detail = row["unavailable_reason"] or row["interpretation_boundary"]
        numerator = row["numerator"] if row["numerator"] is not None else "—"
        denominator = row["denominator"] if row["denominator"] is not None else "—"
        filters = row["filters"].replace("; ", ", ")
        lines.append(
            f"| {row['case']} | {row['metric_id']} | {filters} | {numerator} | "
            f"{denominator} | {value} | {row['status']} | {detail} |"
        )
    lines += [
        "",
        "Every row also has metric version, grain, unit, filters, exclusions "
        "and interpretation boundary in [baseline-metrics.json](baseline-metrics.json). "
        "`MET-012` is a reported-category diagnostic; its required-question-set "
        "contract remains partial. `MET-019` has separate HTTPX resume evidence, "
        "not a release-case rate.",
        "",
    ]
    (OUT / "baseline-metrics.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--freeze", action="store_true", help="Extract preserved external journals once"
    )
    parser.add_argument(
        "--verify-replay", action="store_true", help="Run frozen Phase 2 replay twice"
    )
    args = parser.parse_args()
    if args.freeze:
        freeze()
    if args.verify_replay:
        verify_replay()
    if not args.freeze and not args.verify_replay:
        write_results()


if __name__ == "__main__":
    main()
