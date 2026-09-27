"""Deterministic path-scoped anchors around a declared release timestamp."""

from __future__ import annotations

import re
from datetime import UTC, datetime, time, timedelta
from typing import Any

from pulse.history.models import AnchorRole, HistoricalRef, HistoricalRefPair, PairStatus
from pulse.models.case import CaseDefinition
from pulse.models.evidence import Confidence

STRATEGY = "manifest_path_first_change"


def select_ref_pair(
    definition: CaseDefinition, repository: str, path: str,
    commits: list[dict[str, Any]],
) -> HistoricalRefPair:
    """Select latest path change <= release and earliest path change > release."""
    case = definition.case
    start = datetime.combine(case.observation_window_start, time.min, tzinfo=UTC)
    end = datetime.combine(
        case.observation_window_end + timedelta(days=1), time.min, tzinfo=UTC
    )
    records: dict[str, datetime] = {}
    malformed = False
    for item in commits:
        try:
            sha = item["sha"]
            raw_date = item["commit"]["committer"]["date"]
            timestamp = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
            if (
                not isinstance(sha, str)
                or not re.fullmatch(r"[0-9a-f]{40}(?:[0-9a-f]{24})?", sha)
                or timestamp.tzinfo is None
            ):
                raise ValueError("missing commit identity or timezone")
        except (KeyError, TypeError, AttributeError, ValueError):
            malformed = True
            continue
        timestamp = timestamp.astimezone(UTC)
        if start <= timestamp < end:
            if sha in records and records[sha] != timestamp:
                malformed = True
            records[sha] = timestamp
    if malformed:
        return _pair(
            definition, repository, path, None, None, PairStatus.AMBIGUOUS,
            "At least one path-history commit lacked a reliable SHA or committer timestamp.",
        )
    if not records:
        return _pair(
            definition, repository, path, None, None, PairStatus.INSUFFICIENT_HISTORY,
            "No manifest-path changes were returned inside the observation window; "
            "historical file absence is not established.",
        )
    before = [(timestamp, sha) for sha, timestamp in records.items()
              if timestamp <= case.release_timestamp]
    after = [(timestamp, sha) for sha, timestamp in records.items()
             if timestamp > case.release_timestamp]
    latest = max((item[0] for item in before), default=None)
    earliest = min((item[0] for item in after), default=None)
    if (
        (latest is not None and sum(item[0] == latest for item in before) > 1)
        or (earliest is not None and sum(item[0] == earliest for item in after) > 1)
    ):
        return _pair(
            definition, repository, path, None, None, PairStatus.AMBIGUOUS,
            "Multiple manifest-changing commits share a boundary timestamp; "
            "no arbitrary SHA was selected.",
        )
    before_ref = (
        _ref(repository, path, next(sha for timestamp, sha in before if timestamp == latest),
             latest, AnchorRole.PRE_RELEASE)
        if latest else None
    )
    after_ref = (
        _ref(repository, path, next(sha for timestamp, sha in after if timestamp == earliest),
             earliest, AnchorRole.FIRST_CHANGE_AFTER_RELEASE)
        if earliest else None
    )
    if before_ref and after_ref:
        status = PairStatus.PAIRED
        reason = (
            "Selected the latest bounded manifest-path change at or before release "
            "and the earliest later change to the same path."
        )
    elif before_ref:
        status = PairStatus.MISSING_AFTER
        reason = "No later manifest-path change was observed inside the window."
    else:
        status = PairStatus.MISSING_BEFORE
        reason = "No manifest-path change at or before release was observed inside the window."
    return _pair(definition, repository, path, before_ref, after_ref, status, reason)


def unresolved_pair(
    definition: CaseDefinition, repository: str, path: str,
    status: PairStatus, reason: str,
) -> HistoricalRefPair:
    return _pair(definition, repository, path, None, None, status, reason)


def _ref(
    repository: str, path: str, sha: str, timestamp: datetime, role: AnchorRole,
) -> HistoricalRef:
    return HistoricalRef(
        repository=repository, path=path, commit_sha=sha,
        commit_timestamp=timestamp, role=role,
        source=f"https://github.com/{repository}/commit/{sha}",
        selection_strategy=STRATEGY,
        reason=(
            "Latest path change at or before the release."
            if role is AnchorRole.PRE_RELEASE
            else "Earliest path change strictly after the release."
        ),
        confidence=Confidence.HIGH,
    )


def _pair(
    definition: CaseDefinition, repository: str, path: str,
    before: HistoricalRef | None, after: HistoricalRef | None,
    status: PairStatus, reason: str,
) -> HistoricalRefPair:
    return HistoricalRefPair(
        case_id=definition.case.case_id, repository=repository, manifest_path=path,
        before=before, after=after, pairing_strategy=STRATEGY,
        release_timestamp=definition.case.release_timestamp,
        observation_window_start=definition.case.observation_window_start,
        observation_window_end=definition.case.observation_window_end,
        confidence=Confidence.MEDIUM if status is PairStatus.PAIRED else Confidence.LOW,
        reason=reason, status=status,
    )
