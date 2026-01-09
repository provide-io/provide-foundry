# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Generate API reference pages for all projects in the monorepo.

This script runs during provide-foundry monorepo builds to generate API
reference documentation for all included child projects.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import suppress
from pathlib import Path

import mkdocs_gen_files

from provide.foundation import logger

# Define all child projects with their site_name values (used for directory prefixes)
# Each value can be either a string (path) or tuple (path, api_dir)
CHILD_PROJECTS = {
    "provide-foundation": "../provide-foundation",
    "provide-testkit": "../provide-testkit",
    "flavorpack": "../flavorpack",
    "pyvider": "../pyvider",
    "pyvider-cty": "../pyvider-cty",
    "pyvider-hcl": "../pyvider-hcl",
    "pyvider-rpcplugin": "../pyvider-rpcplugin",
    "pyvider-components": "../pyvider-components",
    "wrknv": ("../wrknv", "api"),  # wrknv uses 'api' instead of 'reference'
}


def _is_package_module(path: Path, src_root: Path) -> bool:
    """Return True if the path resides inside a Python package tree."""
    current_dir = path.parent
    while current_dir != src_root and current_dir > src_root:
        if not (current_dir / "__init__.py").exists():
            return False
        current_dir = current_dir.parent
    return True


def _iter_module_docs(
    project_name: str,
    src_root: Path,
    api_dir: str = "reference",
) -> Iterator[tuple[tuple[str, ...], Path, Path]]:
    """Yield valid module parts with their documentation paths.

    Args:
        project_name: Name of the project for path prefixing
        src_root: Root directory containing Python source
        api_dir: API documentation directory name (default: "reference")
    """
    for path in sorted(src_root.rglob("*.py")):
        if "__pycache__" in path.parts or "pb2" in path.name:
            continue
        if not _is_package_module(path, src_root):
            continue

        module_path = path.relative_to(src_root).with_suffix("")
        parts = tuple(module_path.parts)
        if not parts:
            continue

        if any(part.startswith("_") and part != "__init__" for part in parts):
            continue

        doc_path = Path(project_name) / api_dir / module_path.with_suffix(".md")
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            continue

        yield parts, doc_path, path


def generate_reference_pages_for_project(
    project_name: str, project_path: str, api_dir: str = "reference"
) -> None:
    """Generate API reference pages for a single project.

    Args:
        project_name: The site_name value (used as directory prefix)
        project_path: Relative path to the project directory
        api_dir: API documentation directory name (default: "reference")
    """
    nav = mkdocs_gen_files.Nav()  # type: ignore[attr-defined,no-untyped-call]

    # Get absolute path to project
    foundry_root = Path(__file__).parent.parent
    project_root = (foundry_root / project_path).resolve()
    src_root = project_root / "src"

    with suppress(Exception):
        logger.debug(
            "Generating references for project",
            project_name=project_name,
            project_root=str(project_root),
            src_root=str(src_root),
            src_exists=src_root.exists(),
            api_dir=api_dir,
        )

    if not src_root.exists():
        with suppress(Exception):
            logger.warning(
                "Skipping project - no src directory",
                project_name=project_name,
                src_root=str(src_root),
            )
        return

    # Track if any files were processed
    files_processed = 0

    reference_root = Path(project_name) / api_dir
    for parts, doc_path, source_path in _iter_module_docs(project_name, src_root, api_dir):
        nav[parts] = str(doc_path.relative_to(reference_root))

        with mkdocs_gen_files.open(doc_path, "w") as fd:
            print(f"::: {'.'.join(parts)}", file=fd)

        mkdocs_gen_files.set_edit_path(doc_path, source_path)
        files_processed += 1

    # Generate SUMMARY.md for literate-nav
    if files_processed > 0:
        summary_path = reference_root / "SUMMARY.md"
        with mkdocs_gen_files.open(summary_path, "w") as nav_file:
            nav_file.writelines(nav.build_literate_nav())

        with suppress(Exception):
            logger.debug(
                "Generated references for project",
                project_name=project_name,
                files_processed=files_processed,
            )
    else:
        with suppress(Exception):
            logger.warning(
                "No files processed for project",
                project_name=project_name,
            )


def generate_all_references() -> None:
    """Generate API reference pages for all child projects."""
    with suppress(Exception):
        logger.debug(
            "Starting monorepo reference generation",
            projects=list(CHILD_PROJECTS.keys()),
        )

    for project_name, project_config in CHILD_PROJECTS.items():
        # Support both string paths and tuple (path, api_dir) configs
        if isinstance(project_config, tuple):
            project_path, api_dir = project_config
        else:
            project_path = project_config
            api_dir = "reference"

        generate_reference_pages_for_project(project_name, project_path, api_dir)

    with suppress(Exception):
        logger.debug("Completed monorepo reference generation")


# Execute generation when module is imported by gen-files plugin
generate_all_references()
