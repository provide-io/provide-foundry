#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Validate that partial references in documentation are correct.

This script checks that all partial includes (--8<-- syntax) point to existing files.
Run from any project directory that uses provide-foundry partials.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

PARTIAL_PATTERN = re.compile(r'--8<--\s+"([^"]+)"')


def find_partial_references(docs_dir: Path) -> list[tuple[Path, str, int]]:
    """Find all partial references in markdown files.

    Returns:
        List of (file_path, partial_reference, line_number) tuples.
    """
    references = []

    if not docs_dir.exists():
        return references

    for md_file in docs_dir.rglob("*.md"):
        try:
            lines = md_file.read_text().splitlines()
            for line_num, line in enumerate(lines, start=1):
                for match in PARTIAL_PATTERN.finditer(line):
                    partial_ref = match.group(1)
                    references.append((md_file, partial_ref, line_num))
        except Exception as e:
            print(f"⚠️  Warning: Could not read {md_file}: {e}", file=sys.stderr)

    return references


def validate_references(project_root: Path, references: list[tuple[Path, str, int]]) -> list[str]:
    """Validate that referenced partials exist.

    Returns:
        List of error messages for missing partials.
    """
    errors = []

    for md_file, partial_ref, line_num in references:
        # Resolve partial path relative to project root
        partial_path = project_root / partial_ref

        if not partial_path.exists():
            relative_md = md_file.relative_to(project_root)
            errors.append(f"{relative_md}:{line_num}: Referenced partial '{partial_ref}' does not exist")

    return errors


def check_extracted_partials(project_root: Path) -> bool:
    """Check if partials have been extracted from provide-foundry.

    Returns:
        True if partials directory exists, False otherwise.
    """
    partials_dir = project_root / ".provide" / "foundry" / "docs" / "_partials"
    return partials_dir.exists()


def main() -> int:
    """Run partial validation."""
    project_root = Path.cwd()
    docs_dir = project_root / "docs"

    print("🔍 Validating partial references...")
    print(f"   Project: {project_root.name}")
    print(f"   Docs: {docs_dir}")
    print()

    # Check if partials have been extracted
    if not check_extracted_partials(project_root):
        print("⚠️  Partials not extracted yet. Run:")
        print(
            '   python -c "from provide.foundry.config import extract_base_mkdocs; '
            "from pathlib import Path; extract_base_mkdocs(Path('.'))\""
        )
        print()

    # Find all partial references
    references = find_partial_references(docs_dir)

    if not references:
        print("INFO: No partial references found in documentation")
        return 0

    print(f"📝 Found {len(references)} partial reference(s)")
    print()

    # Validate references
    errors = validate_references(project_root, references)

    if errors:
        print("❌ VALIDATION FAILED")
        print()
        for error in errors:
            print(f"  {error}")
        print()
        print(f"Total errors: {len(errors)}")
        return 1
    else:
        print("✅ All partial references are valid")
        return 0


if __name__ == "__main__":
    sys.exit(main())
