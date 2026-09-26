"""Deterministic structured and Markdown forensic reports."""

from __future__ import annotations

from pathlib import Path

from pulse.analysis.forensics import ReleaseForensics


def write_forensics_json(forensics: ReleaseForensics, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(forensics.model_dump_json(indent=2), encoding="utf-8")
    return path


def render_forensics_markdown(forensics: ReleaseForensics) -> str:
    lines = [
        f"# Release forensics: {forensics.target_package} {forensics.target_version}",
        "",
        "## Release summary",
        "",
        f"- Case: `{forensics.case_id}`",
        f"- Observation window: {forensics.observation_window_start} to "
        f"{forensics.observation_window_end}",
        f"- Accepted evidence events: {len(forensics.accepted_events)}",
        "",
        "## Declared cohort",
        "",
        f"Selection method: `{forensics.cohort_selection_method}`. "
        f"{forensics.cohort_selection_rationale}",
        "",
    ]
    for repository in forensics.repositories:
        lines.append(f"- `{repository.repository}`")
    lines.extend(
        [
            "",
            "## Collection coverage",
            "",
            f"{forensics.completeness.repositories_collected} of "
            f"{forensics.completeness.cohort_size} cohort repositories had sufficient collection.",
            "",
            "## Release timeline",
            "",
            "Events are ordered by their evidence timestamps. Lifecycle stages are forensic "
            "evidence categories, not a required chronological or causal sequence. "
            "Remediation or compatibility work may precede later public friction reports "
            "from users of older downstream versions.",
            "",
        ]
    )
    for event in forensics.accepted_events:
        sources = ", ".join(f"[source]({item.url})" for item in event.evidence)
        lines.append(
            f"- {event.occurred_at.date()} — **{event.lifecycle_stage.value}** — "
            f"{event.title} ({event.confidence.value}; {sources})"
        )
    if not forensics.accepted_events:
        lines.append("No accepted events were available.")
    lines.extend(["", "## Repository findings", ""])
    for repository in forensics.repositories:
        confidence = (
            repository.overall_confidence.value if repository.overall_confidence else "none"
        )
        lines.extend(
            [
                f"### {repository.repository}",
                "",
                f"- Observed adoption: `{repository.observed_adoption.state.value}`",
                f"- Migration friction: `{repository.migration_friction.state.value}`",
                f"- Remediation: `{repository.remediation.state.value}`",
                f"- Recovery signal: `{repository.recovery_signal.state.value}`",
                f"- Overall confidence: `{confidence}`",
                "",
            ]
        )
    stage_sections = (
        ("Observed adoption", "observed_adoption"),
        ("Migration friction", "migration_friction"),
        ("Remediation", "remediation"),
        ("Bounded recovery", "recovery_signal"),
    )
    for heading, attribute in stage_sections:
        lines.extend([f"## {heading}", ""])
        for repository in forensics.repositories:
            finding = getattr(repository, attribute)
            lines.append(
                f"- `{repository.repository}`: `{finding.state.value}` — {finding.explanation}"
            )
        lines.append("")
    lines.extend(["## Cohort metrics", ""])
    for metric in forensics.metrics:
        value = "unavailable" if metric.value is None else f"{metric.value:.1%}"
        lines.append(
            f"- **{metric.name}:** {metric.numerator}/{metric.denominator} ({value}). "
            f"{metric.qualification_rule}"
        )
    lines.extend(["", "## Confidence", ""])
    for confidence, count in sorted(forensics.completeness.confidence_distribution.items()):
        lines.append(f"- {confidence}: {count}")
    if not forensics.completeness.confidence_distribution:
        lines.append("No accepted evidence confidence values were available.")
    lines.extend(["", "## Missing evidence", ""])
    lines.extend(f"- {item}" for item in forensics.missing_evidence)
    if not forensics.missing_evidence:
        lines.append("No missing evidence was recorded for the configured stages.")
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in forensics.limitations)
    lines.extend(["", "## Source references", ""])
    sources = sorted(
        {str(ref.url) for event in forensics.accepted_events for ref in event.evidence}
    )
    lines.extend(f"- {source}" for source in sources)
    if not sources:
        lines.append("No accepted source references were available.")
    lines.append("")
    return "\n".join(lines)


def write_forensics_markdown(forensics: ReleaseForensics, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_forensics_markdown(forensics), encoding="utf-8")
    return path
