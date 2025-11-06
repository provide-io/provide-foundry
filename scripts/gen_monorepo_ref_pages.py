"""Generate API reference pages for all projects in the monorepo.

This script runs during provide-foundry monorepo builds to generate API
reference documentation for all included child projects.
"""

from __future__ import annotations

from pathlib import Path

import mkdocs_gen_files
from provide.foundation import logger

# Define all child projects with their site_name values (used for directory prefixes)
CHILD_PROJECTS = {
    "provide-foundation": "../provide-foundation",
    "provide-testkit": "../provide-testkit",
    "flavorpack": "../flavorpack",
    "pyvider": "../pyvider",
    "pyvider-cty": "../pyvider-cty",
    "pyvider-hcl": "../pyvider-hcl",
    "pyvider-rpcplugin": "../pyvider-rpcplugin",
    "pyvider-components": "../pyvider-components",
    "wrknv": "../wrknv",
}


def generate_reference_pages_for_project(project_name: str, project_path: str) -> None:
    """Generate API reference pages for a single project.

    Args:
        project_name: The site_name value (used as directory prefix)
        project_path: Relative path to the project directory
    """
    nav = mkdocs_gen_files.Nav()  # type: ignore[attr-defined,no-untyped-call]

    # Get absolute path to project
    foundry_root = Path(__file__).parent.parent
    project_root = (foundry_root / project_path).resolve()
    src_root = project_root / "src"

    try:
        logger.debug(
            "Generating references for project",
            project_name=project_name,
            project_root=str(project_root),
            src_root=str(src_root),
            src_exists=src_root.exists(),
        )
    except Exception:
        pass

    if not src_root.exists():
        try:
            logger.warning(
                "Skipping project - no src directory",
                project_name=project_name,
                src_root=str(src_root),
            )
        except Exception:
            pass
        return

    # Track if any files were processed
    files_processed = 0

    for path in sorted(src_root.rglob("*.py")):
        # Skip __pycache__ directories
        if "__pycache__" in str(path):
            continue

        # Skip generated protobuf files (for pyvider-rpcplugin)
        if "pb2" in path.name:
            continue

        # Skip files in directories that aren't Python packages (no __init__.py)
        # Check all parent directories from src_root to file location
        current_dir = path.parent
        is_package = True
        while current_dir != src_root and current_dir > src_root:
            if not (current_dir / "__init__.py").exists():
                is_package = False
                break
            current_dir = current_dir.parent

        if not is_package:
            continue

        module_path = path.relative_to(src_root).with_suffix("")

        # Doc path includes project prefix
        doc_path = Path(project_name) / "reference" / module_path.with_suffix(".md")
        full_doc_path = Path(project_name) / "reference" / module_path.with_suffix(".md")

        parts = tuple(module_path.parts)

        # Skip private modules (but allow __init__)
        if any(part.startswith("_") and part != "__init__" for part in parts):
            continue

        # Handle __init__.py files -> index.md
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")
            full_doc_path = full_doc_path.with_name("index.md")

        # Skip empty parts
        if not parts:
            continue

        # Build navigation - strip project prefix from nav paths
        nav_path = str(doc_path)
        if nav_path.startswith(f"{project_name}/reference/"):
            nav_path = nav_path[len(f"{project_name}/reference/") :]
        nav[parts] = nav_path

        # Create markdown file with mkdocstrings reference
        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            identifier = ".".join(parts)
            print(f"::: {identifier}", file=fd)

        # Set edit path to source file
        mkdocs_gen_files.set_edit_path(full_doc_path, path)

        files_processed += 1

    # Generate SUMMARY.md for literate-nav
    if files_processed > 0:
        summary_path = Path(project_name) / "reference" / "SUMMARY.md"
        with mkdocs_gen_files.open(summary_path, "w") as nav_file:
            nav_file.writelines(nav.build_literate_nav())

        try:
            logger.debug(
                "Generated references for project",
                project_name=project_name,
                files_processed=files_processed,
            )
        except Exception:
            pass
    else:
        try:
            logger.warning(
                "No files processed for project",
                project_name=project_name,
            )
        except Exception:
            pass


def generate_all_references() -> None:
    """Generate API reference pages for all child projects."""
    try:
        logger.debug(
            "Starting monorepo reference generation",
            projects=list(CHILD_PROJECTS.keys()),
        )
    except Exception:
        pass

    for project_name, project_path in CHILD_PROJECTS.items():
        generate_reference_pages_for_project(project_name, project_path)

    try:
        logger.debug("Completed monorepo reference generation")
    except Exception:
        pass


# Execute generation when module is imported by gen-files plugin
generate_all_references()
