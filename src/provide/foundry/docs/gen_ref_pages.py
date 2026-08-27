# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Generate API reference pages for MkDocs documentation.

This module auto-generates markdown files with mkdocstrings references
for Python source code at MkDocs build time.

Usage in mkdocs.yml:
    plugins:
      - gen-files:
          scripts:
            - gen:provide.foundry.docs.gen_ref_pages
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import suppress
from pathlib import Path

import mkdocs_gen_files

from provide.foundation import logger


def generate_reference_pages() -> None:
    """Generate API reference markdown files from Python source.

    Scans the src/ directory for Python files and generates corresponding
    markdown documentation files with mkdocstrings references. Creates
    SUMMARY.md for literate-nav navigation.

    Works in both standalone and monorepo contexts by using MKDOCS_CONFIG_DIR
    environment variable to locate the correct source directory.

    The function:
    - Skips __pycache__ directories
    - Skips private modules (except __init__.py)
    - Converts __init__.py to index.md
    - Generates navigation structure
    - Sets edit paths to source files
    """
    import os

    nav = mkdocs_gen_files.Nav()  # type: ignore[attr-defined,no-untyped-call]
    config_dir = Path(os.getenv("MKDOCS_CONFIG_DIR", "."))
    src_root = _resolve_src_root(config_dir)
    # Allow projects to customize the output directory (default: "reference")
    output_dir = os.getenv("MKDOCS_API_DIR", "reference")

    with suppress(Exception):
        logger.debug(
            "gen_ref_pages starting",
            cwd=str(Path.cwd()),
            mkdocs_config_dir=os.getenv("MKDOCS_CONFIG_DIR", "NOT_SET"),
            config_dir=str(config_dir.absolute()),
            src_root=str(src_root.absolute()) if src_root else "MISSING",
            src_root_exists=bool(src_root and src_root.exists()),
            output_dir=output_dir,
        )

    if src_root is None:
        with suppress(Exception):
            logger.warning("gen_ref_pages: No source files found, skipping generation")
        return

    for parts, doc_path, source_path in _iter_module_docs(src_root, output_dir):
        nav[parts] = str(doc_path.relative_to(output_dir))

        with mkdocs_gen_files.open(doc_path, "w") as fd:
            print(f"::: {'.'.join(parts)}", file=fd)

        mkdocs_gen_files.set_edit_path(doc_path, source_path)

    with mkdocs_gen_files.open(f"{output_dir}/SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())


def _resolve_src_root(config_dir: Path) -> Path | None:
    """Return the source root directory, trying fallbacks if needed."""
    candidates = [config_dir / "src", Path("src")]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _iter_module_docs(
    src_root: Path, output_dir: str = "reference"
) -> Iterator[tuple[tuple[str, ...], Path, Path]]:
    """Yield valid module parts with their documentation paths.

    Args:
        src_root: Root directory containing Python source files
        output_dir: Output directory name for generated docs (default: "reference")
    """
    for path in sorted(src_root.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        if not _is_package_module(path, src_root):
            continue

        module_path = path.relative_to(src_root).with_suffix("")
        parts = tuple(module_path.parts)
        if not parts:
            continue
        if any(part.startswith("_") and part != "__init__" for part in parts):
            continue

        doc_path = Path(output_dir) / module_path.with_suffix(".md")
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")
        if not parts:
            continue
        yield parts, doc_path, path


def _is_package_module(path: Path, src_root: Path) -> bool:
    """Return True if each parent directory includes an __init__.py file."""
    current_dir = path.parent
    while current_dir != src_root and current_dir > src_root:
        if not (current_dir / "__init__.py").exists():
            return False
        current_dir = current_dir.parent
    return True


# mkdocs-gen-files executes this file with `runpy.run_path()` and no run_name,
# which leaves __name__ as "<run_path>". The `if __name__ == "__main__"` guard
# this replaces therefore never fired under the plugin, and the plugin has no
# way to tell a script that generated nothing from one that had nothing to
# generate: every consuming project built one hand-written reference page
# instead of the ~350 this emits, and every link into the generated tree
# dangled.
#
# The guard was broken for direct execution too. It sat above the helpers it
# needs, so `python gen_ref_pages.py` died with
# `NameError: name '_resolve_src_root' is not defined`. It has never run in any
# invocation path, which is why this call must be the last statement in the
# file rather than merely unconditional.
#
# runpy and `python gen_ref_pages.py` both leave __spec__ as None; a genuine
# `import provide.foundry.docs.gen_ref_pages` sets it. Generating files is not
# a side effect an import may have -- provide.foundry.docs re-exports
# generate_reference_pages -- so __spec__ is what separates the two.
if __spec__ is None:
    generate_reference_pages()
