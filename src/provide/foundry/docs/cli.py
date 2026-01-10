# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Command-line interface for markdown link fixer.

This module provides the Click-based CLI for fixing markdown links.
For programmatic use, import from `provide.foundry.docs.link_fixer` instead.
"""

from __future__ import annotations

from pathlib import Path
import sys

import click

from provide.foundation import perr, pout
from provide.foundry.docs.link_fixer import find_markdown_files, process_file


def _resolve_paths(paths: tuple[str, ...]) -> tuple[Path, ...]:
    """Resolve paths, defaulting to docs/ if none provided.

    Args:
        paths: User-provided paths as strings

    Returns:
        Resolved paths as Path objects

    Raises:
        SystemExit: If no paths provided and docs/ doesn't exist
    """
    if not paths:
        default_path = Path.cwd() / "docs"
        if not default_path.exists():
            perr("Error: No paths provided and 'docs/' directory not found")
            perr("Usage: provide-foundry-link-fixer [PATHS...]")
            sys.exit(1)
        return (default_path,)
    return tuple(Path(p) for p in paths)


def _apply_exclusions(
    markdown_files: list[Path],
    exclude_pattern: tuple[str, ...],
    *,
    verbose: bool,
) -> list[Path]:
    """Apply exclusion patterns to file list.

    Args:
        markdown_files: List of markdown files
        exclude_pattern: Patterns to exclude
        verbose: Whether to show verbose output

    Returns:
        Filtered list of markdown files
    """
    if not exclude_pattern:
        return markdown_files

    original_count = len(markdown_files)
    for pattern in exclude_pattern:
        markdown_files = [f for f in markdown_files if pattern not in str(f)]
    excluded_count = original_count - len(markdown_files)

    if excluded_count > 0 and verbose:
        pout(f"Excluded {excluded_count} file(s) matching patterns")

    return markdown_files


def _process_all_files(
    markdown_files: list[Path],
    *,
    dry_run: bool,
    verbose: bool,
) -> tuple[int, int, int]:
    """Process all markdown files.

    Args:
        markdown_files: List of files to process
        dry_run: Whether to run in dry-run mode
        verbose: Whether to show verbose output

    Returns:
        Tuple of (total_changes, files_changed, errors)
    """
    total_changes = 0
    files_changed = 0
    errors = 0

    for file_path in markdown_files:
        success, changes = process_file(file_path, dry_run=dry_run, verbose=verbose)
        if success:
            total_changes += changes
            if changes > 0:
                files_changed += 1
        else:
            errors += 1

    return total_changes, files_changed, errors


def _print_summary(
    total_files: int,
    files_changed: int,
    total_changes: int,
    errors: int,
    *,
    dry_run: bool,
) -> None:
    """Print processing summary.

    Args:
        total_files: Total number of files processed
        files_changed: Number of files that were changed
        total_changes: Total number of link fixes
        errors: Number of errors encountered
        dry_run: Whether in dry-run mode
    """
    pout("")
    pout("Summary:")
    pout(f"  Files processed: {total_files}")
    pout(f"  Files {'that would be ' if dry_run else ''}changed: {files_changed}")
    pout(f"  Total link fixes: {total_changes}")
    if errors > 0:
        pout(f"  Errors: {errors}")

    if dry_run and files_changed > 0:
        pout("")
        pout("Run without --dry-run to apply these changes")


@click.command()
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(exists=True),
    required=False,
)
@click.option(
    "--dry-run",
    "-n",
    is_flag=True,
    help="Show what would be changed without modifying files",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed output including files with no changes",
)
@click.option(
    "--exclude-pattern",
    "-e",
    multiple=True,
    help="Exclude files matching pattern (can be specified multiple times)",
)
def main(
    paths: tuple[str, ...],
    dry_run: bool,
    verbose: bool,
    exclude_pattern: tuple[str, ...],
) -> None:
    """Fix markdown links to use directory URLs instead of .md extensions.

    If no PATHS are provided, defaults to the 'docs/' directory in the current
    working directory.

    Examples:

        \b
        # Fix links in docs/ directory (default)
        python -m provide.foundry.docs

        \b
        # Check what would change without modifying files
        python -m provide.foundry.docs --dry-run

        \b
        # Fix links in specific directories
        python -m provide.foundry.docs docs/ ../other-project/docs/

        \b
        # Fix links with verbose output
        python -m provide.foundry.docs --verbose docs/
    """
    # Resolve paths with defaults
    resolved_paths = _resolve_paths(paths)

    if dry_run:
        pout("Running in DRY-RUN mode - no files will be modified")
        pout("")

    # Find and filter markdown files
    markdown_files = find_markdown_files(resolved_paths)
    markdown_files = _apply_exclusions(markdown_files, exclude_pattern, verbose=verbose)

    if not markdown_files:
        pout("No markdown files found to process")
        sys.exit(0)

    pout(f"Processing {len(markdown_files)} markdown file(s)...")
    pout("")

    # Process all files
    total_changes, files_changed, errors = _process_all_files(markdown_files, dry_run=dry_run, verbose=verbose)

    # Print summary
    _print_summary(len(markdown_files), files_changed, total_changes, errors, dry_run=dry_run)

    sys.exit(1 if errors > 0 else 0)
