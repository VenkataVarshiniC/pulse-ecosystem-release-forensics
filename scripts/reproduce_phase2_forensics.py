"""Rebuild both frozen Phase 2 reports and their cross-case validation summary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pulse.config.cases import load_case
from pulse.phase2_forensics import (
    Phase2Report,
    build_phase2_report,
    validation_summary,
    write_phase2_report,
)

CASE_IDS = ("pytest-8.0.0", "urllib3-2.0.0")


def reproduce(root: Path, data_dir: Path) -> tuple[Path, Path]:
    reports: list[Phase2Report] = []
    for case_id in CASE_IDS:
        manifest_path = data_dir / f"baseline-{case_id}.manifest.json"
        metadata = json.loads(manifest_path.read_text(encoding="utf-8"))
        report = build_phase2_report(
            load_case(root / "cases" / f"{case_id}.yaml"),
            Path(metadata["collection_manifest"]),
            Path(metadata["history_manifest"]),
            data_dir / f"baseline-{case_id}.jsonl",
            manifest_path,
            data_dir / "review-ledger.jsonl",
        )
        write_phase2_report(report, root)
        reports.append(report)
    summary = validation_summary(tuple(reports))
    json_path = data_dir / "end-to-end-validation.json"
    json_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    markdown_path = root / "docs/phase-2/validation-results.md"
    markdown_path.write_text(_render_summary(tuple(reports)), encoding="utf-8")
    return json_path, markdown_path


def _render_summary(reports: tuple[Phase2Report, ...]) -> str:
    lines = [
        "# Phase 2 Milestone 5 — End-to-end validation",
        "",
        "**Result: PASS for report integration.** Both frozen cases replay through the same "
        "manifest-verified workflow without recollection or analyst-entered completeness flags. "
        "Most lifecycle findings remain unknown because historical context or "
        "source types are missing. "
        "This is not a final Phase 2 decision.",
        "",
        "| Case | Frozen cohort | Core collection | Historical declaration evidence | "
        "Candidates / accepted / rejected | Zero-candidate repositories |",
        "| --- | ---: | --- | --- | --- | ---: |",
    ]
    for item in reports:
        metrics = {metric.name: metric for metric in item.metrics}
        core = metrics["core_collection_coverage"]
        history = metrics["historical_dependency_evidence_coverage"]
        zero = sum(repo.emitted_candidate_count == 0 for repo in item.repositories)
        lines.append(
            f"| [{item.case_id}](generated/{item.case_id}-forensics.md) | "
            f"{len(item.repositories)} | {core.numerator}/{core.denominator} "
            f"({item.collection_operational_status}) | {history.numerator}/{history.denominator} | "
            f"{item.emitted_candidate_count} / {item.accepted_candidate_count} / "
            f"{item.rejected_candidate_count} | {zero} |"
        )
    lines.extend(
        [
            "",
            "The two cohorts are convenience validation sets. Their counts are not pooled into an "
            "ecosystem incidence statistic. Historical declaration evidence is not "
            "target-version adoption.",
            "",
            "## Stage sufficiency and reportability",
            "",
        ]
    )
    for item in reports:
        lines.append(f"### {item.case_id}")
        lines.append("")
        for stage in item.repositories[0].stage_findings:
            states = {
                state: sum(
                    repo.stage_findings[stage].state.value == state for repo in item.repositories
                )
                for state in ("yes", "no_qualifying_evidence_found", "unknown_insufficient_data")
            }
            sufficient = sum(repo.stage_sufficiency[stage] for repo in item.repositories)
            lines.append(
                f"- `{stage}`: sufficient {sufficient}/{len(item.repositories)}; "
                f"YES {states['yes']}, NO QUALIFYING EVIDENCE "
                f"{states['no_qualifying_evidence_found']}, "
                f"UNKNOWN {states['unknown_insufficient_data']}."
            )
        lines.append("- Accepted evidence timeline: empty; no candidate passed review.")
        lines.append(
            "- Zero-candidate repositories: "
            + ", ".join(
                f"`{repo.repository}`"
                for repo in item.repositories
                if repo.emitted_candidate_count == 0
            )
            + "."
        )
        lines.append("- Missing sources: " + " ".join(item.missing_sources))
        lines.append("- Unavailable metrics:")
        lines.extend(f"  - {reason}" for reason in item.unavailable_metrics)
        lines.append("")
    lines.extend(
        [
            "## Reproduction and interpretation",
            "",
            "Run `uv run python scripts/reproduce_phase2_forensics.py` from the repository root "
            "while the Milestone 4 external collector roots are available. The script verifies the "
            "case fingerprint, exact task plan, run IDs, windows, snapshot hashes, baseline hash, "
            "and review-to-candidate identity, then rewrites deterministic reports. "
            "It makes no API calls. The committed baseline manifests contain the external paths.",
            "",
            "A verified optional current-file 404 completes that probe but provides no dependency "
            "declaration. Historical path gaps remain unknown; current declarations do not prove "
            "historical target-version use. The planner collected upstream releases "
            "but no downstream "
            "releases, so recovery is unknown and `text.support_release` had no input. "
            "No target-version lockfile selection or runtime resolution was collected.",
            "",
            "`NO QUALIFYING EVIDENCE` means complete required stage sources and review found no "
            "accepted event under this bounded method. It does not prove the event did not occur. "
            "Zero emitted candidates likewise does not establish no impact or detector recall. "
            "The two urllib3 rule firings from one Dependabot PR remain rejected detector output, "
            "not accepted lifecycle events.",
            "",
            "See [evidence sufficiency](evidence-sufficiency.md) and the "
            "[machine-readable summary](evaluation-data/end-to-end-validation.json).",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--data-dir", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    data_dir = args.data_dir or root / "docs/phase-2/evaluation-data"
    for item in reproduce(root, data_dir):
        print(item)


if __name__ == "__main__":
    main()
