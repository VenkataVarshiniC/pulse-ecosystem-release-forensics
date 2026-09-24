from __future__ import annotations

from pathlib import Path

import pytest

from pulse.analysis.timeline import build_timelines, render_markdown
from pulse.evidence.ledger import LedgerValidationError, load_jsonl

FIXTURES = Path(__file__).parent / "fixtures"
PROJECT_ROOT = Path(__file__).parents[1]


def test_ledger_validates_and_timeline_orders_events() -> None:
    timelines = build_timelines(load_jsonl(FIXTURES / "valid-ledger.jsonl"))

    assert [event.title for event in timelines[0].events] == [
        "Version 2.0 released",
        "Failure after upgrade",
    ]
    rendered = render_markdown(timelines)
    assert "migration_friction" in rendered
    assert "https://github.com/org/downstream/issues/1" in rendered


def test_ledger_reports_invalid_line_number() -> None:
    with pytest.raises(LedgerValidationError, match="line 1"):
        load_jsonl(FIXTURES / "invalid-ledger.jsonl")


def test_processed_ledger_validates_and_reproduces_committed_timeline() -> None:
    ledger = PROJECT_ROOT / "data" / "processed" / "evidence-ledger.jsonl"
    events = load_jsonl(ledger)

    assert len(events) == 17
    assert {event.case_id for event in events} == {
        "numpy-2.0.0",
        "pydantic-2.0",
        "sqlalchemy-2.0.0",
    }
    expected = (PROJECT_ROOT / "docs" / "phase-0" / "forensic-timelines.md").read_text(
        encoding="utf-8"
    )
    assert render_markdown(build_timelines(events)).strip() == expected.strip()
