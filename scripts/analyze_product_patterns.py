"""Reproduce bounded M3 analysis from frozen metric, mart, and PR evidence."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median, pstdev
from uuid import UUID
from xml.sax.saxutils import escape

from psycopg.rows import dict_row

from pulse.phase2_postgres.loader import connect

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/analysis"
FIGURES = ROOT / "docs/phase-4/m3/figures"
M25 = ROOT / "data/validation/m2-5-metric-baseline.json"
DIAGNOSTICS = ROOT / "data/validation/m2-5-sql-diagnostics.json"
MANIFEST = ROOT / "data/manifests/analytics-release-manifest.json"
PR_SOURCE = ROOT / "docs/phase-3/secondary-research/github-pr-observations.jsonl"
PR_METRICS = ROOT / "docs/phase-4/workflow-analysis/workflow-metrics.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def query(path: Path) -> list[dict]:
    with connect("pulse_dev") as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(path.read_text(encoding="utf-8"))
        return [{key: str(value) if isinstance(value, UUID) else value
                 for key, value in row.items()} for row in cur.fetchall()]


def ratio(numerator: int | None, denominator: int | None) -> float | None:
    return round(numerator / denominator, 6) if numerator is not None and denominator else None


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def bar_figure(path: Path, title: str, rows: list[tuple[str, int, str]],
               note: str, maximum: int) -> None:
    """Render a deterministic, labeled exploratory count chart without a dashboard runtime."""
    height = 125 + 42 * len(rows)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" '
        'viewBox="0 0 900 ' + str(height) + '">',
        '<rect width="900" height="100%" fill="white"/>',
        f'<text x="28" y="34" font-size="20" font-family="Arial" fill="#182438">'
        f'{escape(title)}</text>',
        f'<text x="28" y="57" font-size="12" font-family="Arial" fill="#42536d">'
        f'{escape(note)}</text>',
    ]
    for index, (label, count, color) in enumerate(rows):
        y = 78 + index * 42
        width = 520 * count / maximum if maximum else 0
        lines.extend([
            f'<text x="28" y="{y + 17}" font-size="13" font-family="Arial" '
            f'fill="#182438">{escape(label)}</text>',
            f'<rect x="300" y="{y}" width="{width:.1f}" height="24" fill="{color}"/>',
            f'<text x="{310 + width:.1f}" y="{y + 17}" font-size="13" '
            f'font-family="Arial" fill="#182438">{count}</text>',
        ])
    lines.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def duration_figure(path: Path, rows: list[dict], upper_fence: float) -> None:
    """Plot every base PR elapsed duration on a log(1+h) axis; retain outliers."""
    ordered = sorted(rows, key=lambda r: (r["hours"], r["repository"],
                                         r["pr_number"]))
    max_hours = max(r["hours"] for r in ordered)
    height = 118 + 22 * len(ordered)
    left, span = 260, 585
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" '
        f'viewBox="0 0 900 {height}">',
        '<rect width="900" height="100%" fill="white"/>',
        '<text x="26" y="32" font-size="20" font-family="Arial" fill="#182438">'
        'Base Dependabot PR open-to-terminal duration</text>',
        '<text x="26" y="54" font-size="12" font-family="Arial" fill="#42536d">'
        '20 selected PRs; log(1 + hours) axis; orange exceeds the 1.5 x IQR upper fence'
        '</text>',
    ]
    for tick in (0, 1, 10, 100, 1000, 6000):
        x = left + span * math.log1p(tick) / math.log1p(max(max_hours, 6000))
        lines.extend([
            f'<line x1="{x:.1f}" y1="72" x2="{x:.1f}" y2="{height - 35}" '
            'stroke="#e3e8ee"/>',
            f'<text x="{x:.1f}" y="{height - 15}" text-anchor="middle" '
            f'font-size="11" font-family="Arial" fill="#42536d">{tick}</text>',
        ])
    for index, row in enumerate(ordered):
        hours = row["hours"]
        x = left + span * math.log1p(hours) / math.log1p(max(max_hours, 6000))
        y = 87 + index * 22
        label = f'{row["repository"]}#{row["pr_number"]}'
        color = "#ce6b27" if hours > upper_fence else "#277da8"
        lines.extend([
            f'<text x="26" y="{y + 4}" font-size="10" font-family="Arial" '
            f'fill="#182438">{escape(label)}</text>',
            f'<circle cx="{x:.1f}" cy="{y}" r="5" fill="{color}"/>',
        ])
    lines.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def population_a(baseline: dict, diagnostics: dict, manifest: dict) -> tuple[dict, list[dict]]:
    assert manifest["publication_decision"] == "HOLD_DRAFT"
    assert all(s["state"] == "DRAFT" for s in manifest["snapshots"])
    expected = {s["case_name"]: s["analysis_snapshot_id"] for s in manifest["snapshots"]}
    metric_rows = baseline["results"]
    assert len(metric_rows) == 46
    assert all(row["analysis_snapshot_id"] == expected[row["case"]] for row in metric_rows)
    comparisons = diagnostics["case_comparison"]
    members = [*diagnostics["pytest/evidence_gaps"],
               *diagnostics["urllib3/evidence_gaps"]]
    assert sum(row["members"] for row in comparisons) == len(members) == 8
    findings = query(ROOT / "analytics/sql/diagnostics/m3_finding_context.sql")
    candidates = query(ROOT / "analytics/sql/diagnostics/m3_candidate_origin.sql")
    assert sum(row["finding_count"] for row in findings) == 40
    assert len(candidates) == 2
    assert {row["analysis_snapshot_id"] for row in findings + candidates} <= set(
        expected.values()
    )
    reason_counts: Counter[str] = Counter()
    category_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in findings:
        count = row["finding_count"]
        category_counts[row["lifecycle_category"]][row["finding_status"]] += count
        if row["finding_status"] == "UNKNOWN":
            reason_counts[row["reason_code"] or "UNRECORDED_REASON"] += count
    by_case = {}
    funnel_csv = []
    for case in ("pytest", "urllib3"):
        case_members = [r for r in members if r["case_name"].startswith(case + "-")]
        case_metrics = {r["metric_id"]: r for r in metric_rows if r["case"] == case}
        funnel = diagnostics[f"{case}/investigation_funnel"]
        for row in funnel:
            funnel_csv.append({
                "population": "A_validation", "case": case, "step": row["step"],
                "category": row["category"] or "", "grain": row["unit"],
                "numerator": row["numerator"], "denominator": row["denominator"],
                "share": ratio(row["numerator"], row["denominator"]),
            })
        by_case[case] = {
            "member_count": len(case_members),
            "metrics": {mid: case_metrics[mid] for mid in (
                "MET-001", "MET-002", "MET-008", "MET-009", "MET-010", "MET-011",
                "MET-016", "MET-017", "MET-018", "MET-022",
            )},
            "historical_member_indicators": {
                "exact_ref_declaration": sum(r["has_historical_declaration"]
                                             for r in case_members),
                "paired_pre_release": sum(r["has_paired_pre_release_history"]
                                          for r in case_members),
                "after_only_present": sum(r["after_only_path_count"] > 0
                                          for r in case_members),
                "unresolved_path_present": sum(r["unresolved_path_count"] > 0
                                               for r in case_members),
            },
            "cooccurring_evidence_indicators": {
                "no_exact_ref_declaration": sum(not r["has_historical_declaration"]
                                                for r in case_members),
                "zero_candidates": sum(r["candidate_count"] == 0 for r in case_members),
                "any_unknown_finding": sum(r["unknown_finding_count"] > 0
                                           for r in case_members),
                "any_legacy_sufficiency": sum(r["legacy_unclassified_count"] > 0
                                               for r in case_members),
            },
            "funnel": funnel,
            "source_usage": diagnostics[f"{case}/source_coverage"],
        }
    readiness = Counter(row["contract_status"] for row in metric_rows if row["case"] == "pytest")
    assert readiness == {
        "READY": 10, "PARTIAL_EVIDENCE": 6, "PARTIAL_PLATFORM": 1,
        "UNAVAILABLE_EVIDENCE": 5, "BLOCKED_STAKEHOLDER": 1,
    }
    assert len({row["artifact_id"] for row in candidates}) == 1
    assert {row["terminal_review_status"] for row in candidates} == {"REJECT"}
    cohort_summary = {
        "declared_members": 8,
        "exact_ref_declaration_present": sum(r["has_historical_declaration"] for r in members),
        "exact_ref_declaration_absent": sum(not r["has_historical_declaration"]
                                                 for r in members),
        "paired_pre_release_present": sum(r["has_paired_pre_release_history"]
                                           for r in members),
        "after_only_path_present": sum(r["after_only_path_count"] > 0 for r in members),
        "unresolved_path_present": sum(r["unresolved_path_count"] > 0 for r in members),
        "candidate_emitting_member": sum(r["candidate_count"] > 0 for r in members),
        "zero_candidate_member": sum(r["candidate_count"] == 0 for r in members),
        "cohort_overlap_note": (
            "Historical path indicators can co-occur within a member; these counts are "
            "descriptive, not a mutually exclusive transition funnel."
        ),
    }
    return {
        "population": "A_frozen_forensic_validation", "members": 8, "cases": by_case,
        "case_comparison": comparisons,
        "cohort_summary": cohort_summary,
        "candidate_origin_and_review": candidates,
        "finding_context": findings,
        "finding_status_by_category": {k: dict(sorted(v.items()))
                                       for k, v in sorted(category_counts.items())},
        "unknown_reason_codes": dict(sorted(reason_counts.items())),
        "metric_contract_availability": dict(sorted(readiness.items())),
        "segment_inventory": diagnostics["segment_inventory"],
        "segment_readiness": [
            {"segment": "case/release", "status": "USABLE",
             "reason": "Two named validation cases support descriptive side-by-side counts only."},
            {"segment": "exact-ref declaration present/absent", "status": "USABLE",
             "reason": "2/8 versus 6/8 supports evidence-gap counts, not outcome comparison."},
            {"segment": "paired pre-release history", "status": "SPARSE",
             "reason": "Only one member has paired history."},
            {"segment": "after-only and unresolved paths", "status": "SPARSE",
             "reason": "Path statuses overlap within members and do not prove release effects."},
            {"segment": "candidate emission/rule/origin/review", "status": "SPARSE",
             "reason": "Two dependent candidates come from one artifact and one repository."},
            {"segment": "evidence source/capture method", "status": "USABLE",
             "reason": "Selected captures diagnose acquisition, not source utility."},
            {"segment": "repository provider and core collection", "status": "INVARIANT",
             "reason": "All eight members are GitHub and core-collected."},
            {"segment": "adoption/recovery/business outcome/role/value", "status": "UNAVAILABLE",
             "reason": "Qualified outcomes or stakeholder research are absent."},
        ],
        "limitation": (
            "Two purposively validated release cases; overlapping evidence indicators are not "
            "causes or independent cohorts; DRAFT validation output only."
        ),
    }, funnel_csv


def population_b() -> tuple[dict, list[dict]]:
    workflow = read_json(PR_METRICS)
    assert workflow["source_sha256"] == sha(PR_SOURCE)
    rows = [json.loads(line) for line in PR_SOURCE.read_text(encoding="utf-8").splitlines()
            if line.strip()]
    base = [row for row in rows if row["sample_type"] == "base"]
    discussion = [row for row in rows if row["sample_type"] == "discussion"]
    assert (len(base), len(discussion)) == (20, 7)
    assert all(r["update_mechanism"] == "dependabot" for r in rows)
    assert all(r["outcome"] in {"merged", "closed_without_merge"} for r in base)
    summary = workflow["samples"]["base"]["duration_hours"]
    values = [row["pr_resolution_duration_hours"] for row in base]
    assert len(values) == summary["n"] == 20
    assert round(median(values), 2) == summary["median"]
    lower = round(summary["q1"] - 1.5 * summary["iqr"], 2)
    upper = round(summary["q3"] + 1.5 * summary["iqr"], 2)
    outliers = sorted([
        {"repository": row["repository"], "pr_number": row["pr_number"],
         "url": row["url"], "hours": row["pr_resolution_duration_hours"]}
        for row in base if row["pr_resolution_duration_hours"] < lower
        or row["pr_resolution_duration_hours"] > upper
    ], key=lambda r: (r["hours"], r["repository"]))
    crosstab = Counter((r["human_interaction_present"], r["outcome"]) for r in base)
    durations = [
        {"sample": "base", "repository": r["repository"], "pr_number": r["pr_number"],
         "url": r["url"], "hours": r["pr_resolution_duration_hours"],
         "outcome": r["outcome"], "visible_human_interaction": r["human_interaction_present"],
         "outlier_1_5_iqr": r["pr_resolution_duration_hours"] < lower
         or r["pr_resolution_duration_hours"] > upper}
        for r in sorted(base, key=lambda x: (x["repository"], x["pr_number"]))
    ]
    return {
        "population": "B_selected_public_dependabot_prs",
        "base_n": 20, "purposive_discussion_n": 7,
        "base_workflow_metrics": workflow["metrics"],
        "base_observations": workflow["samples"]["base"],
        "discussion_observations_separate": workflow["samples"]["discussion"],
        "base_duration_hours": {
            **summary, "mean": round(mean(values), 2),
            "population_std_dev": round(pstdev(values), 2),
            "iqr_lower_fence": lower, "iqr_upper_fence": upper,
            "outliers_1_5_iqr": outliers,
        },
        "base_human_interaction_by_disposition": [
            {"visible_human_interaction": human, "outcome": outcome,
             "count": crosstab[human, outcome]}
            for human in (False, True) for outcome in ("merged", "closed_without_merge")
        ],
        "limitation": (
            "Convenience, title/first-page-biased base sample; seven discussion PRs were "
            "purposively chosen and excluded from every base rate. Duration is open-to-terminal "
            "elapsed time, not engineering work."
        ),
    }, durations


def main() -> int:
    baseline, diagnostics, manifest = read_json(M25), read_json(DIAGNOSTICS), read_json(MANIFEST)
    assert manifest["metric_baseline_sha256"] == sha(M25)
    assert manifest["sql_diagnostics_sha256"] == sha(DIAGNOSTICS)
    a, funnel = population_a(baseline, diagnostics, manifest)
    b, durations = population_b()
    assert sum(v["finding_count"] for v in a["finding_context"]
               if v["finding_status"] == "UNKNOWN") == 38
    output = {
        "analysis_version": "m3-bounded-product-analysis-v1",
        "publication_state": "validation analytical outputs; two DRAFT snapshots; BI blocked",
        "input_sha256": {
            "m2_5_metric_baseline": sha(M25), "m2_5_diagnostics": sha(DIAGNOSTICS),
            "analytics_release_manifest": sha(MANIFEST), "pr_observations": sha(PR_SOURCE),
            "pr_workflow_metrics": sha(PR_METRICS),
        },
        "population_boundary": (
            "A has 8 declared forensic members in 2 cases; B has 20 base and 7 separate "
            "purposive Dependabot PRs. No cross-population rates."
        ),
        "population_a": a, "population_b": b,
        "analytical_questions": {
            "Q1_investigative_certainty": ["population_a.cases.*.funnel",
                                         "population_a.finding_status_by_category"],
            "Q2_historical_context": ["population_a.cohort_summary"],
            "Q3_candidate_generation": ["population_a.candidate_origin_and_review"],
            "Q4_human_review": ["population_a.cases.*.metrics.MET-009",
                                 "population_a.candidate_origin_and_review"],
            "Q5_unknown_findings": ["population_a.unknown_reason_codes",
                                    "population_a.cases.*.cooccurring_evidence_indicators"],
            "Q6_evidence_sources": ["population_a.cases.*.source_usage"],
            "Q7_case_comparison": ["population_a.case_comparison"],
            "Q8_public_pr_workflow": ["population_b.base_observations",
                                      "population_b.base_duration_hours"],
            "Q9_metric_availability": ["population_a.metric_contract_availability"],
            "Q10_unsupported_decisions": ["population_a.segment_readiness",
                                           "formal_inference"],
        },
        "formal_inference": "FORMAL INFERENCE NOT JUSTIFIED",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "m3-product-analytics-results.json").write_text(
        json.dumps(output, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    write_csv(OUT / "m3-investigation-funnel.csv",
              ["population", "case", "step", "category", "grain", "numerator",
               "denominator", "share"], funnel)
    write_csv(OUT / "m3-case-comparison.csv", list(a["case_comparison"][0]),
              a["case_comparison"])
    write_csv(OUT / "m3-base-pr-durations.csv", list(durations[0]), durations)
    unknown = a["finding_status_by_category"]
    bar_figure(FIGURES / "unknown-by-category.svg", "UNKNOWN lifecycle findings by category",
               [(key.replace("_", " "), counts.get("UNKNOWN", 0), "#586bb3")
                for key, counts in unknown.items()],
               "Population A: 40 member-category findings; UNKNOWN is an evidence state",
               max(counts.get("UNKNOWN", 0) for counts in unknown.values()))
    bar_figure(FIGURES / "member-evidence-path.svg", "Declared-member evidence path",
               [("Declared members", 8, "#277da8"),
                ("Core collected", 8, "#277da8"),
                ("Exact-ref declaration", 2, "#277da8"),
                ("Paired pre-release history", 1, "#277da8")],
               "Population A: all bars count distinct members; denominator 8", 8)
    bar_figure(FIGURES / "candidate-review-path.svg", "Candidate review path",
               [("Emitted candidate IDs", 2, "#8f5fa8"),
                ("Terminally reviewed IDs", 2, "#8f5fa8"),
                ("Accepted IDs", 0, "#8f5fa8"),
                ("Rejected IDs", 2, "#8f5fa8")],
               "Population A: candidate IDs; 2 emitted in urllib3, none in pytest", 2)
    duration_figure(FIGURES / "base-pr-duration.svg", durations,
                    b["base_duration_hours"]["iqr_upper_fence"])
    print("PASS: M3 bounded analysis; A=8 members, B=20 base + 7 purposive PRs")
    print(f"Analysis SHA-256: {sha(OUT / 'm3-product-analytics-results.json')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
