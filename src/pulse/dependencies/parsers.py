"""Conservative parsers for high-value Python dependency files."""

from __future__ import annotations

import ast
import configparser
import re
import tomllib
from collections.abc import Iterable
from datetime import datetime

from packaging.requirements import InvalidRequirement, Requirement
from packaging.utils import canonicalize_name

from pulse.dependencies.models import DependencyObservation


def parse_dependency_file(
    *,
    repository: str,
    file_path: str,
    content: str,
    commit_reference: str,
    observed_at: datetime,
    source: str,
) -> tuple[DependencyObservation, ...]:
    observations, _ = parse_dependency_file_with_diagnostics(
        repository=repository, file_path=file_path, content=content,
        commit_reference=commit_reference, observed_at=observed_at, source=source,
    )
    return observations


def parse_dependency_file_with_diagnostics(
    *,
    repository: str,
    file_path: str,
    content: str,
    commit_reference: str,
    observed_at: datetime,
    source: str,
) -> tuple[tuple[DependencyObservation, ...], tuple[str, ...]]:
    """Return parsed declarations and unparsed entries without executing project code."""
    lower = file_path.casefold()
    if lower.endswith("requirements.txt") or "/requirements/" in lower:
        raw_requirements = [(raw, None) for raw in _requirements_lines(content)]
    elif lower.endswith("pyproject.toml"):
        raw_requirements = _pyproject_requirements(content)
    elif lower.endswith("setup.cfg"):
        raw_requirements = [(raw, None) for raw in _setup_cfg_requirements(content)]
    elif lower.endswith("setup.py"):
        raw_requirements = [(raw, None) for raw in _setup_py_requirements(content)]
    else:
        return (), ()
    observations = []
    unparsed = []
    for raw, group in raw_requirements:
        try:
            requirement = Requirement(raw)
        except InvalidRequirement:
            unparsed.append(raw)
            continue
        observations.append(
            DependencyObservation(
                repository=repository,
                file_path=file_path,
                package=canonicalize_name(requirement.name),
                constraint=str(requirement.specifier),
                commit_reference=commit_reference,
                observed_at=observed_at,
                source=source,
                raw_requirement=raw,
                declared_package=requirement.name,
                raw_constraint=_raw_constraint(raw, requirement.name),
                marker=str(requirement.marker) if requirement.marker else None,
                extras=tuple(sorted(requirement.extras)),
                direct_reference=requirement.url,
                declaration_group=group,
            )
        )
    return tuple(observations), tuple(unparsed)


def _raw_constraint(raw: str, name: str) -> str | None:
    head = raw.split(";", 1)[0].strip()
    tail = head[len(name):].strip()
    if tail.startswith("[") and "]" in tail:
        tail = tail.split("]", 1)[1].strip()
    if not tail or tail.startswith("@"):
        return None
    return tail


def _requirements_lines(content: str) -> Iterable[str]:
    for line in content.splitlines():
        value = re.split(r"\s+#", line, maxsplit=1)[0].strip()
        if value and not value.startswith(("-", "http://", "https://", "git+")):
            yield value


def _pyproject_requirements(content: str) -> list[tuple[str, str]]:
    payload = tomllib.loads(content)
    project = payload.get("project", {})
    requirements = [
        (raw, "project.dependencies") for raw in project.get("dependencies", [])
    ]
    for group, values in project.get("optional-dependencies", {}).items():
        requirements.extend(
            (raw, f"project.optional-dependencies.{group}") for raw in values
        )
    poetry = payload.get("tool", {}).get("poetry", {}).get("dependencies", {})
    for name, constraint in poetry.items():
        if name.casefold() == "python":
            continue
        if isinstance(constraint, str):
            requirements.append((
                f"{name}{constraint}" if constraint != "*" else name,
                "tool.poetry.dependencies",
            ))
        elif isinstance(constraint, dict) and isinstance(constraint.get("version"), str):
            requirements.append((f"{name}{constraint['version']}", "tool.poetry.dependencies"))
    return requirements


def _setup_cfg_requirements(content: str) -> list[str]:
    parser = configparser.ConfigParser()
    parser.read_string(content)
    if not parser.has_option("options", "install_requires"):
        return []
    return list(_requirements_lines(parser.get("options", "install_requires")))


def _setup_py_requirements(content: str) -> list[str]:
    tree = ast.parse(content)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for keyword in node.keywords:
            if keyword.arg != "install_requires" or not isinstance(
                keyword.value, (ast.List, ast.Tuple)
            ):
                continue
            return [
                item.value
                for item in keyword.value.elts
                if isinstance(item, ast.Constant) and isinstance(item.value, str)
            ]
    return []
