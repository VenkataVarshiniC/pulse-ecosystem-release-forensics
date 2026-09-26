"""Minimal reproducible command-line workflow for PULSE."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pulse.analysis.forensics import ReleaseForensics, build_forensics
from pulse.collection.collectors import GitHubCollector, PyPICollector
from pulse.collection.journal import RunJournal
from pulse.collection.planner import plan_collection
from pulse.collection.raw import CaptureMethod, RawSnapshotStore
from pulse.collection.runner import CollectionRunner
from pulse.config.cases import load_case
from pulse.config.settings import Settings
from pulse.evidence.review_ledger import load_review_ledger
from pulse.github.client import GitHubClient
from pulse.github.errors import GitHubAuthenticationError
from pulse.packages.pypi import PyPIClient
from pulse.reporting import write_forensics_json, write_forensics_markdown


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pulse")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("plan", "collect"):
        command = subparsers.add_parser(name)
        command.add_argument("case", type=Path)
        if name == "collect":
            command.add_argument("--resume", action="store_true")
            command.add_argument("--output-root", type=Path, default=Path("."))
            command.add_argument("--max-pages", type=int, default=1000)
            command.add_argument("--max-retries", type=int, default=3)
    analyze = subparsers.add_parser("analyze")
    analyze.add_argument("case", type=Path)
    analyze.add_argument("review_ledger", type=Path)
    analyze.add_argument("--complete-repository", action="append", default=[])
    analyze.add_argument("--recovery-eligible", action="append")
    analyze.add_argument("--output-root", type=Path, default=Path("."))
    report = subparsers.add_parser("report")
    report.add_argument("forensics", type=Path)
    report.add_argument("output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "plan":
        print(plan_collection(load_case(args.case)).model_dump_json(indent=2))
        return 0
    if args.command == "collect":
        try:
            return _collect(
                args.case, resume=args.resume, output_root=args.output_root,
                max_pages=args.max_pages, max_retries=args.max_retries,
            )
        except (GitHubAuthenticationError, ValueError) as exc:
            print(f"Collection configuration error: {exc}", file=sys.stderr)
            return 2
    if args.command == "analyze":
        return _analyze(args)
    forensics = ReleaseForensics.model_validate_json(args.forensics.read_text(encoding="utf-8"))
    write_forensics_markdown(forensics, args.output)
    return 0


def _collect(
    case_path: Path, *, resume: bool = False, output_root: Path = Path("."),
    max_pages: int = 1000, max_retries: int = 3,
) -> int:
    definition = load_case(case_path)
    settings = Settings.from_env()
    plan = plan_collection(definition)
    journal = RunJournal(output_root / "data/interim")
    with GitHubClient(
        settings.github_token, base_url=settings.github_api_url,
        max_pages=max_pages, max_retries=max_retries,
    ) as github_client, PyPIClient(base_url=settings.pypi_api_url) as pypi_client:
        runner = CollectionRunner(
            [GitHubCollector(github_client), PyPICollector(pypi_client)],
            RawSnapshotStore(
                output_root / "data/raw", capture_method=CaptureMethod.COLLECTOR
            ),
            journal=journal,
        )
        manifest = runner.run(definition, plan, resume=resume)
    path = journal.directory(definition.case.case_id, manifest.run_id) / "manifest.json"
    print(path)
    return 0 if manifest.status == "complete" else 2


def _analyze(args: argparse.Namespace) -> int:
    definition = load_case(args.case)
    candidates = load_review_ledger(args.review_ledger)
    forensics = build_forensics(
        definition,
        candidates,
        repositories_with_sufficient_collection=set(args.complete_repository),
        recovery_eligible_repositories=(
            set(args.recovery_eligible) if args.recovery_eligible is not None else None
        ),
    )
    json_path = (
        args.output_root / "data" / "processed" / forensics.case_id / "forensics.json"
    )
    markdown_path = (
        args.output_root / "docs" / "generated" / f"{forensics.case_id}-forensics.md"
    )
    write_forensics_json(forensics, json_path)
    write_forensics_markdown(forensics, markdown_path)
    print(json.dumps({"json": str(json_path), "markdown": str(markdown_path)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
