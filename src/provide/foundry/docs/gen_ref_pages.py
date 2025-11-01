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

from pathlib import Path

import mkdocs_gen_files


def generate_reference_pages() -> None:
    """Generate API reference markdown files from Python source.

    Scans the src/ directory for Python files and generates corresponding
    markdown documentation files with mkdocstrings references. Creates
    SUMMARY.md for literate-nav navigation.

    The function:
    - Skips __pycache__ directories
    - Skips private modules (except __init__.py)
    - Converts __init__.py to index.md
    - Generates navigation structure
    - Sets edit paths to source files
    """
    nav = mkdocs_gen_files.Nav()

    # Source code is in 'src/' directory at project root
    src_root = Path("src")

    for path in sorted(src_root.rglob("*.py")):
        # Skip __pycache__ directories
        if "__pycache__" in str(path):
            continue

        module_path = path.relative_to(src_root).with_suffix("")
        doc_path = Path("reference") / module_path.with_suffix(".md")
        full_doc_path = Path("reference") / module_path.with_suffix(".md")

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

        # Strip "reference/" prefix from nav paths
        nav_path = str(doc_path)
        if nav_path.startswith("reference/"):
            nav_path = nav_path[10:]  # Remove "reference/" prefix
        nav[parts] = nav_path

        # Create markdown file with mkdocstrings reference
        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            identifier = ".".join(parts)
            print(f"::: {identifier}", file=fd)

        # Set edit path to source file
        mkdocs_gen_files.set_edit_path(full_doc_path, path)

    # Generate SUMMARY.md for literate-nav
    with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())


# Support direct execution for testing/debugging
if __name__ == "__main__":
    generate_reference_pages()
