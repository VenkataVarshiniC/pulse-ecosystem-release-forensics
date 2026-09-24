"""Deterministic, source-auditable lifecycle timelines."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from pydantic import BaseModel, ConfigDict

from pulse.models.evidence import EvidenceEvent, LifecycleStage

_STAGE_ORDER = {stage: index for index, stage in enumerate(LifecycleStage)}


class ReleaseTimeline(BaseModel):
    model_config = ConfigDict(frozen=True)

    case_id: str
    target_package: str
    target_release: str
    events: tuple[EvidenceEvent, ...]


def build_timelines(events: Iterable[EvidenceEvent]) -> tuple[ReleaseTimeline, ...]:
    groups: dict[tuple[str, str, str], list[EvidenceEvent]] = defaultdict(list)
    for event in events:
        groups[(event.case_id, event.target_package, event.target_release)].append(event)

    timelines = []
    for (case_id, package, release), grouped_events in sorted(groups.items()):
        ordered = tuple(
            sorted(
                grouped_events,
                key=lambda event: (
                    event.occurred_at,
                    _STAGE_ORDER[event.lifecycle_stage],
                    event.title.casefold(),
                ),
            )
        )
        timelines.append(
            ReleaseTimeline(
                case_id=case_id,
                target_package=package,
                target_release=release,
                events=ordered,
            )
        )
    return tuple(timelines)


def render_markdown(timelines: Iterable[ReleaseTimeline]) -> str:
    lines = [
        "# Forensic timelines",
        "",
        "Generated from `data/processed/evidence-ledger.jsonl`. "
        "Every entry links back to its source.",
        "",
    ]
    for timeline in timelines:
        lines.extend(
            [
                f"## {timeline.target_package} {timeline.target_release}",
                "",
            ]
        )
        for event in timeline.events:
            date = event.occurred_at.date().isoformat()
            sources = ", ".join(
                f"[source {index}]({reference.url})"
                for index, reference in enumerate(event.evidence, start=1)
            )
            lines.append(
                f"- **{date} - {event.lifecycle_stage.value}:** {event.title} "
                f"({event.confidence.value}; {sources})"
            )
        lines.append("")
    return "\n".join(lines)
