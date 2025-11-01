"""
Shared template for generating API reference pages using mkdocs-gen-files.

This script is used by projects in the provide.io ecosystem to auto-generate
API documentation from Python source code at mkdocs build time.

Projects can either:
1. Use this shared template directly by referencing it in their mkdocs.yml:
   plugins:
     - gen-files:
         scripts:
           - ../provide-foundry/scripts/gen_ref_pages.py

2. Copy this template to their docs/ directory and customize as needed

Configuration:
- Assumes source code is in 'src/' directory
- Generates docs in 'reference/' directory
- Uses mkdocstrings to document modules
- Creates SUMMARY.md for literate-nav navigation
"""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

# Assuming your source code is in a 'src' directory at the project root
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

    # Strip "reference/" prefix from nav paths since SUMMARY.md is already in reference/
    nav_path = str(doc_path)
    if nav_path.startswith("reference/"):
        nav_path = nav_path[10:]  # Remove "reference/" prefix
    nav[parts] = nav_path

    # Create the markdown file with mkdocstrings reference
    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(parts)
        print(f"::: {identifier}", file=fd)

    # Set edit path to point to the source file
    mkdocs_gen_files.set_edit_path(full_doc_path, path)

# Generate SUMMARY.md for literate-nav
with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
