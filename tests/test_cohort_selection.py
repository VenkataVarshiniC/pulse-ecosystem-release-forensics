"""Validate the frozen Milestone 3 population against its prior selection rules."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from runpy import run_path

import pytest
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

from pulse.config.cases import load_case
from pulse.models.case import CohortSelectionMethod

SELECTION = run_path("scripts/select_cohorts.py")
COHORT_SIZE = SELECTION["COHORT_SIZE"]
observation_window = SELECTION["observation_window"]
rank = SELECTION["rank"]

LEDGER = json.loads(
    Path("docs/phase-2/cohort-selection-ledger.json").read_text(encoding="utf-8")
)


def test_target_pool_and_case_policy_are_frozen() -> None:
    assert [item["package"] for item in LEDGER["target_seed_pool"]] == [
        "click", "pytest", "urllib3"
    ]
    assert not LEDGER["outcome_evidence_inspected"]
    assert {item["target"]["package"] for item in LEDGER["cases"]} == {
        "pytest", "urllib3"
    }
    for record in LEDGER["cases"]:
        target = record["target"]
        case_id = f"{target['package']}-{target['qualifying_release']}"
        definition = load_case(Path("cases") / f"{case_id}.yaml")
        case = definition.case
        cohort = definition.cohort
        assert cohort.selection_method is CohortSelectionMethod.RULE_BASED
        assert case.ecosystem == "pypi"
        assert case.release_timestamp == datetime.fromisoformat(target["released_at"])
        assert (
            case.observation_window_start, case.observation_window_end
        ) == observation_window(case.release_timestamp)
        assert {rule.source.value for rule in case.collection_rules} == {"pypi", "github"}
        assert len(cohort.repositories) == record["selected_count"]
        assert len(cohort.repositories) <= COHORT_SIZE
        assert len({item.repository.lower() for item in cohort.repositories}) == len(
            cohort.repositories
        )
        assert all(
            item.repository.lower() != case.upstream_repository.lower()
            and item.repository.split("/")[0].lower()
            != case.upstream_repository.split("/")[0].lower()
            for item in cohort.repositories
        )


def test_every_code_search_hit_is_accounted_for_and_exclusions_are_explicit() -> None:
    for record in LEDGER["cases"]:
        hits = {
            item["repository"].lower()
            for search in record["searches"]
            for item in search["ordered_results"]
        }
        rows = record["candidates"]
        assert len(hits) == record["candidates_considered"] == len(rows)
        assert {item["repository"].lower() for item in rows} == hits
        assert sum(item["eligible"] for item in rows) == record["eligible_count"]
        assert sum(item["selected"] for item in rows) == record["selected_count"]
        assert all(item["exclusion_reasons"] for item in rows if not item["eligible"])
        assert all(not item["exclusion_reasons"] for item in rows if item["eligible"])
        assert all(item["eligible"] for item in rows if item["selected"])


def test_hash_ranking_and_case_membership_replay_exactly() -> None:
    assert rank("example-1.0.0", "Owner/Repo") == rank("example-1.0.0", "owner/repo")
    for record in LEDGER["cases"]:
        target = record["target"]
        case_id = f"{target['package']}-{target['qualifying_release']}"
        rows = record["candidates"]
        assert all(
            item["rank_hash"] == rank(case_id, item["repository"])
            for item in rows
        )
        eligible = sorted(
            (item for item in rows if item["eligible"]),
            key=lambda item: (item["rank_hash"], item["repository"].lower()),
        )
        selected = eligible[:COHORT_SIZE]
        assert [item["repository"] for item in eligible] == record["eligible_ranked"]
        assert {item["repository"] for item in selected} == {
            item["repository"] for item in rows if item["selected"]
        }
        definition = load_case(Path("cases") / f"{case_id}.yaml")
        assert [item.repository for item in definition.cohort.repositories] == [
            item["repository"] for item in selected
        ]


@pytest.mark.parametrize("case_id", ["pytest-8.0.0", "urllib3-2.0.0"])
def test_direct_dependency_evidence_is_present_for_every_member(case_id: str) -> None:
    definition = load_case(Path("cases") / f"{case_id}.yaml")
    record = next(
        item for item in LEDGER["cases"]
        if f"{item['target']['package']}-{item['target']['qualifying_release']}" == case_id
    )
    selected = {item["repository"]: item for item in record["candidates"] if item["selected"]}
    for member in definition.cohort.repositories:
        row = selected[member.repository]
        evidence = member.dependency_evidence
        assert evidence is not None
        assert evidence.content_sha256 == row["dependency"]["content_sha256"]
        assert evidence.observed_at == datetime.fromisoformat(
            row["dependency"]["observed_at"]
        )
        assert evidence.observed_at > definition.case.release_timestamp
        assert row["dependency"]["path"] in {"pyproject.toml", "requirements.txt"}
        assert any(
            canonicalize_name(Requirement(item["raw"]).name)
            == canonicalize_name(definition.case.target_package)
            for item in row["dependency"]["declarations"]
        )
        assert row["activity"]["at_least_two_commits"]
        assert len(row["activity"]["sample_committer_dates"]) == 2
        assert row["metadata"]["language"] == "Python"
        assert not row["metadata"]["archived"]
        assert not row["metadata"]["fork"]
        assert not row["metadata"]["private"]


def test_short_cohort_is_reported_instead_of_backfilled() -> None:
    pytest_case = next(
        item for item in LEDGER["cases"] if item["target"]["package"] == "pytest"
    )
    assert pytest_case["selected_count"] == pytest_case["eligible_count"] == 2
    assert pytest_case["selected_count"] < 5
    documentation = Path("docs/phase-2/cohort-selection.md").read_text(encoding="utf-8")
    assert "Milestone 3 is **PARTIAL**" in documentation
    assert "no additional candidates were added" in documentation.lower()


def test_selection_timestamp_precedes_no_forensic_collection() -> None:
    assert datetime.fromisoformat(LEDGER["checked_at"]).tzinfo is not None
    assert datetime.fromisoformat(LEDGER["checked_at"]).astimezone(UTC).year == 2026
