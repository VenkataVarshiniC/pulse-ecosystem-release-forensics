from __future__ import annotations

from datetime import UTC, datetime

import pytest

from pulse.dependencies.models import TransitionKind
from pulse.dependencies.parsers import parse_dependency_file
from pulse.dependencies.transitions import detect_transition

OBSERVED_AT = datetime(2026, 9, 24, tzinfo=UTC)


@pytest.mark.parametrize(
    ("path", "content"),
    [
        ("requirements.txt", "pydantic>=1.10,<2\nhttpx>=0.27\n"),
        (
            "pyproject.toml",
            '[project]\ndependencies = ["pydantic>=1.10,<2", "httpx>=0.27"]\n',
        ),
        ("setup.cfg", "[options]\ninstall_requires =\n  pydantic>=1.10,<2\n  httpx>=0.27\n"),
        (
            "setup.py",
            'from setuptools import setup\nsetup(install_requires=["pydantic>=1.10,<2"])',
        ),
    ],
)
def test_supported_dependency_files_normalize_constraints(path: str, content: str) -> None:
    observations = parse_dependency_file(
        repository="example/project",
        file_path=path,
        content=content,
        commit_reference="abc123",
        observed_at=OBSERVED_AT,
        source="https://github.com/example/project/blob/abc123/pyproject.toml",
    )

    pydantic = next(item for item in observations if item.package == "pydantic")
    assert pydantic.constraint == "<2,>=1.10"


def test_transition_detects_new_upper_bound_without_inferring_motivation() -> None:
    before = parse_dependency_file(
        repository="PrefectHQ/prefect",
        file_path="requirements.txt",
        content="pydantic>=1.10",
        commit_reference="before",
        observed_at=OBSERVED_AT,
        source="https://github.com/PrefectHQ/prefect/blob/before/requirements.txt",
    )[0]
    after = parse_dependency_file(
        repository="PrefectHQ/prefect",
        file_path="requirements.txt",
        content="pydantic>=1.10,<2",
        commit_reference="after",
        observed_at=OBSERVED_AT,
        source="https://github.com/PrefectHQ/prefect/blob/after/requirements.txt",
    )[0]

    transition = detect_transition(before, after, target_version="2.0")

    assert transition is not None
    assert transition.kind is TransitionKind.TARGET_EXCLUDED
    assert "motivation" not in transition.reason.casefold()
