"""
Dataclasses defining the types of a `pyproject.toml` file.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packaging.requirements import Requirement
    from packaging.specifiers import SpecifierSet
    from packaging.version import Version

type TomlBasic = bool | float | int | str
type TomlDate = date | datetime | time

type TomlArray = list[TomlValue]
type TomlTable = dict[str, TomlValue]

type TomlValue = TomlBasic | TomlDate | TomlArray | TomlTable

type Classifiers = list[str]
type Dependencies = list[Requirement]
type Keywords = list[str]
type OptionalDependencies = dict[str, Dependencies]
type Urls = dict[str, str]


@dataclass
class BuildSystem:
    """
    Represents a PEP518-compliant build system definition.
    """

    requires: Dependencies
    build_backend: str
    backend_path: list[str] | None


@dataclass
class Project:
    """
    Represents a project's core metadata, according to PEP621.
    """

    authors: TomlArray
    classifiers: Classifiers
    dependencies: Dependencies
    description: str | None
    keywords: Keywords
    license: TomlTable | str | None
    maintainers: TomlArray
    name: str
    optional_dependencies: OptionalDependencies
    readme: TomlTable | str | None
    requires_python: SpecifierSet | None
    urls: Urls
    version: Version | None


@dataclass
class PyProject:
    """
    Represents a PEP621-compliant `pyproject.toml` file.
    """

    build_system: BuildSystem | None
    project: Project | None
    tool: TomlTable | None
