"""
`pyproject.toml` parsing function.
"""

from __future__ import annotations

from pathlib import Path
from tomllib import load
from typing import TYPE_CHECKING

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.version import Version

from .models import BuildSystem, Project, PyProject

if TYPE_CHECKING:
    from .models import Dependencies, OptionalDependencies, TomlTable


def pyparse(filepath: str | Path) -> PyProject:
    """
    Parse the given `pyproject.toml` file, and return a typed `PyProject`.

    Args:
        filepath: Path to `pyproject.toml`.

    Returns:
        PyProject: Statically-typed dataclass object representing the parsed `TOML`.

    """

    path = Path(filepath)

    with path.open(encoding="utf-8", mode="rb") as f:
        data: TomlTable = load(f)

    raw_build: TomlTable | None = data.get("build-system")
    build = None

    if raw_build is not None:
        build = BuildSystem(
            build_backend=raw_build.get("build-backend", ""),
            backend_path=raw_build.get("backend-path"),
            requires=[
                Requirement(req)
                for req in raw_build.get("requires", [])
            ],
        )  # fmt: skip

    raw_project: TomlTable | None = data.get("project")
    project = None

    if raw_project is not None:
        deps: Dependencies = [
            Requirement(r)
            for r in raw_project.get("dependencies", [])
        ]  # fmt: skip

        opt_deps: OptionalDependencies = {
            group: [Requirement(r) for r in reqs]
            for group, reqs in raw_project.get("optional-dependencies", {}).items()
        }

        version: Version | None = raw_project.get("version")
        req_python: SpecifierSet | None = raw_project.get("requires-python")

        project = Project(
            authors=raw_project.get("authors", []),
            classifiers=raw_project.get("classifiers", []),
            dependencies=deps,
            description=raw_project.get("description"),
            keywords=raw_project.get("keywords", []),
            license=raw_project.get("license"),
            maintainers=raw_project.get("maintainers", []),
            name=raw_project["name"],
            optional_dependencies=opt_deps,
            readme=raw_project.get("readme"),
            requires_python=SpecifierSet(req_python) if req_python else None,
            urls=raw_project.get("urls", {}),
            version=Version(version) if version else None,
        )

    raw_tool: TomlTable = data.get("tool", {})

    return PyProject(
        build_system=build,
        project=project,
        tool=raw_tool,
    )
