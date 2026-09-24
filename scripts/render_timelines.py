"""Render the processed evidence ledger as deterministic Markdown."""

from pathlib import Path

from pulse.analysis.timeline import build_timelines, render_markdown
from pulse.evidence.ledger import load_jsonl


def main() -> None:
    ledger = Path("data/processed/evidence-ledger.jsonl")
    print(render_markdown(build_timelines(load_jsonl(ledger))))


if __name__ == "__main__":
    main()
