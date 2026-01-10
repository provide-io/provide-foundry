# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Fix markdown links to use directory URLs instead of .md extensions.

This module provides library functions to convert markdown links from `.md` format
to directory URLs, which is required when `use_directory_urls: true` in MkDocs.

For CLI usage, use `python -m provide.foundry.docs.link_fixer` or import from
`provide.foundry.docs.cli`.

Examples:
    >>> from provide.foundry.docs import fix_md_links
    >>> content = "[link](page.md)"
    >>> new_content, changes = fix_md_links(content)
    >>> print(new_content)
    [link](page/)
    >>> print(changes)
    1
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import TYPE_CHECKING

from provide.foundation import perr, pout

if TYPE_CHECKING:
    from collections.abc import Sequence


def fix_md_links(content: str, *, preserve_special: bool = True) -> tuple[str, int]:
    """Replace .md links with directory URLs.

    Converts markdown links from `.md` extension to directory URLs:
    - [text](file.md) → [text](file/)
    - [text](file.md#anchor) → [text](file/#anchor)
    - [text](../path/file.md) → [text](../path/file/)
    - [text](path/file.md) → [text](path/file/)

    Preserves:
    - External links (http://, https://)
    - Anchors (moved after the /)
    - Links that already end with /
    - Special paths (e.g., .provide/) when preserve_special is True

    Args:
        content: Markdown file content to process
        preserve_special: If True, preserve links containing /.provide/ or other
                         special patterns (default: True)

    Returns:
        Tuple of (modified_content, number_of_changes)
    """
    # Pattern matches markdown links with .md extension (with or without anchors)
    # Captures: [text](path/file.md#anchor) or [text](path/file.md)
    pattern = r"(\[[^\]]+\]\()([^)]+?\.md)(#[^)]+)?(\))"
    changes = 0

    def replace_link(match: re.Match[str]) -> str:
        nonlocal changes
        prefix = match.group(1)  # [text](
        link = match.group(2)  # path/file.md (without anchor)
        anchor = match.group(3) or ""  # #anchor or empty string
        suffix = match.group(4)  # )

        # Skip external links
        if link.startswith(("http://", "https://")):
            return match.group(0)

        # Skip special paths if requested
        if preserve_special and "/.provide/" in link:
            return match.group(0)

        # Replace .md with / and preserve anchor
        new_link = link[:-3] + "/" + anchor
        changes += 1

        return f"{prefix}{new_link}{suffix}"

    new_content = re.sub(pattern, replace_link, content)
    return new_content, changes


def process_file(
    file_path: Path,
    *,
    dry_run: bool = False,
    verbose: bool = False,
) -> tuple[bool, int]:
    """Process a single markdown file.

    Args:
        file_path: Path to the markdown file
        dry_run: If True, don't write changes, just report what would change
        verbose: If True, show detailed output

    Returns:
        Tuple of (success, number_of_changes)
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        new_content, changes = fix_md_links(content)

        if changes > 0:
            if dry_run:
                pout(f"  Would fix {changes} link(s) in: {file_path}")
            else:
                file_path.write_text(new_content, encoding="utf-8")
                pout(f"  Fixed {changes} link(s) in: {file_path}")
            return True, changes
        if verbose:
            pout(f"  No changes needed: {file_path}")
        return True, 0

    except Exception as e:
        perr(f"  Error processing {file_path}: {e}")
        return False, 0


def find_markdown_files(paths: Sequence[Path]) -> list[Path]:
    """Find all markdown files in the given paths.

    Args:
        paths: List of file or directory paths to search

    Returns:
        List of markdown file paths
    """
    markdown_files: list[Path] = []

    for path in paths:
        if not path.exists():
            perr(f"Warning: Path does not exist: {path}")
            continue

        if path.is_file() and path.suffix == ".md":
            markdown_files.append(path)
        elif path.is_dir():
            # Recursively find all .md files
            markdown_files.extend(path.rglob("*.md"))

    return sorted(set(markdown_files))
