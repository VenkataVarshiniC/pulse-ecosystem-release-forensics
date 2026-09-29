"""Protect population boundaries and generated M3 descriptive outputs."""

import csv
import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "data/analysis/m3-product-analytics-results.json"
SOURCE = ROOT / "docs/phase-3/secondary-research/github-pr-observations.jsonl"


def load():
    return json.loads(ANALYSIS.read_text(encoding="utf-8"))


def test_population_separation_and_question_coverage():
    result = load()
    assert result["population_a"]["members"] == 8
    assert {case: value["member_count"] for case, value in
            result["population_a"]["cases"].items()} == {"pytest": 2, "urllib3": 6}
    assert result["population_b"]["base_n"] == 20
    assert result["population_b"]["purposive_discussion_n"] == 7
    assert len(result["analytical_questions"]) == 10
    assert result["input_sha256"]["pr_observations"] == hashlib.sha256(
        SOURCE.read_bytes()
    ).hexdigest()
    assert result["formal_inference"] == "FORMAL INFERENCE NOT JUSTIFIED"
    assert "DRAFT" in result["publication_state"]


def test_unknown_and_candidate_grains():
    population = load()["population_a"]
    assert sum(states.get("UNKNOWN", 0) for states in
               population["finding_status_by_category"].values()) == 38
    assert population["unknown_reason_codes"] == {"unknown_insufficient_data": 38}
    candidates = population["candidate_origin_and_review"]
    assert len(candidates) == 2
    assert len({row["artifact_id"] for row in candidates}) == 1
    assert len({row["repository_id"] for row in candidates}) == 1
    assert {row["source_origin"] for row in candidates} == {"COPIED_UPSTREAM"}
    assert {row["terminal_review_status"] for row in candidates} == {"REJECT"}
    assert population["cohort_summary"]["paired_pre_release_present"] == 1


def test_base_duration_outliers_and_no_purposive_pooling():
    population = load()["population_b"]
    duration = population["base_duration_hours"]
    assert (duration["n"], duration["median"], duration["q1"],
            duration["q3"], duration["iqr"]) == (20, 167.25, 136.3, 744.0, 607.7)
    assert duration["iqr_upper_fence"] == 1655.55
    assert [row["hours"] for row in duration["outliers_1_5_iqr"]] == [2032.5, 5823.4]
    with (ROOT / "data/analysis/m3-base-pr-durations.csv").open(
        encoding="utf-8", newline=""
    ) as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 20
    assert {row["sample"] for row in rows} == {"base"}


def test_exploratory_figures_are_valid_svg():
    figure_dir = ROOT / "docs/phase-4/m3/figures"
    assert {path.name for path in figure_dir.glob("*.svg")} == {
        "unknown-by-category.svg", "member-evidence-path.svg",
        "candidate-review-path.svg", "base-pr-duration.svg",
    }
    for path in figure_dir.glob("*.svg"):
        assert ElementTree.parse(path).getroot().tag.endswith("svg")
