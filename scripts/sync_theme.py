#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Sync shared theme files to documentation projects.

This script copies the shared theme from provide-foundry/shared-theme/
into each project's docs/.shared-theme/ directory, allowing mkdocs serve
to work correctly with local file references.

Usage:
    python sync_theme.py sync --all              # Sync to all projects
    python sync_theme.py sync --project plating  # Sync to specific project
    python sync_theme.py status                  # Show sync status
    python sync_theme.py clean                   # Remove all .shared-theme dirs"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from provide.foundation import pout, perr, logger

try:
    from provide.foundation.cli.deps import click
except ImportError:
    import click


def find_project_root() -> Path:
    """Find the provide-io root directory."""
    current = Path(__file__).resolve().parent.parent.parent
    if (current / "provide-foundry").exists():
        return current
    # Fallback: search upward
    current = Path.cwd()
    while current != current.parent:
        if (current / "provide-foundry").exists():
            return current
        current = current.parent
    perr("Could not find provide-io root directory")
    sys.exit(1)


def find_mkdocs_projects(root: Path) -> list[Path]:
    """Find all projects with mkdocs.yml files."""
    mkdocs_files = list(root.glob("*/mkdocs.yml"))
    return sorted([f.parent for f in mkdocs_files])


def get_theme_source(root: Path) -> Path:
    """Get the shared theme source directory."""
    theme_dir = root / "provide-foundry" / "shared-theme"
    if not theme_dir.exists():
        perr(f"Theme source not found at {theme_dir}")
        sys.exit(1)
    return theme_dir


def sync_to_project(project: Path, theme_source: Path, dry_run: bool = False) -> bool:
    """
    Sync theme files to a single project.

    Returns True if sync was successful, False otherwise.
    """
    target = project / "docs" / ".shared-theme"

    if not (project / "docs").exists():
        logger.warning(f"Skipping {project.name}: No docs/ directory")
        return False

    if not dry_run:
        # Remove old theme files
        if target.exists():
            shutil.rmtree(target)

        # Copy new theme files
        shutil.copytree(theme_source, target)
        pout(f"✓ Synced theme to {project.name}")
    else:
        pout(f"Would sync theme to {project.name}")

    return True


@click.command()
@click.option("--all", is_flag=True, help="Sync to all projects")
@click.option("--project", help="Sync to specific project")
@click.option("--dry-run", is_flag=True, help="Show what would be done")
def sync(all: bool = False, project: str | None = None, dry_run: bool = False):
    """Sync shared theme files to projects."""
    root = find_project_root()
    theme_source = get_theme_source(root)

    if not all and not project:
        perr("Specify --all or --project NAME")
        pout("Usage: sync_theme.py sync --all")
        pout("       sync_theme.py sync --project plating")
        sys.exit(1)

    if project:
        # Sync to specific project
        project_path = root / project
        if not project_path.exists():
            perr(f"Project '{project}' not found")
            sys.exit(1)

        pout(f"\nSyncing theme to {project}...")
        sync_to_project(project_path, theme_source, dry_run)

    else:
        # Sync to all projects
        projects = find_mkdocs_projects(root)
        pout(f"\nSyncing theme to {len(projects)} projects...\n")

        success_count = 0
        for proj in projects:
            if sync_to_project(proj, theme_source, dry_run):
                success_count += 1

        pout(f"\n✓ Successfully synced to {success_count}/{len(projects)} projects")


@click.command()
def status():
    """Show sync status for all projects."""
    root = find_project_root()
    projects = find_mkdocs_projects(root)

    pout("\nShared Theme Sync Status:")
    pout("=" * 60)

    for project in projects:
        target = project / "docs" / ".shared-theme"
        if target.exists():
            file_count = len(list(target.rglob("*")))
            status = f"✓ Synced ({file_count} files)"
        else:
            status = "✗ Not synced"

        pout(f"{project.name:25} {status}")

    pout("=" * 60)
    pout("Source: provide-foundry/shared-theme/")


@click.command()
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def clean(yes: bool = False):
    """Remove all .shared-theme directories."""
    root = find_project_root()
    projects = find_mkdocs_projects(root)

    targets = []
    for project in projects:
        target = project / "docs" / ".shared-theme"
        if target.exists():
            targets.append((project.name, target))

    if not targets:
        logger.warning("No .shared-theme directories found")
        return

    pout(f"\nFound {len(targets)} .shared-theme directories:")
    for name, _ in targets:
        pout(f"  - {name}/docs/.shared-theme/")

    if not yes:
        response = input("\nRemove all these directories? [y/N]: ")
        if response.lower() != "y":
            pout("Cancelled")
            return

    pout()
    for name, target in targets:
        shutil.rmtree(target)
        pout(f"✓ Removed {name}/docs/.shared-theme/")

    pout(f"\n✓ Cleaned {len(targets)} directories")


@click.group()
def cli():
    """Sync shared theme files to documentation projects."""
    pass


cli.add_command(sync)
cli.add_command(status)
cli.add_command(clean)


if __name__ == "__main__":
    cli()

# 🏭⚒️🔚
