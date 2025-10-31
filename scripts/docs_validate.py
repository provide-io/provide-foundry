#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Documentation validation CLI tool for the provide.io ecosystem.

Provides commands to validate links, configs, structure, and list projects.
Inspired by FastAPI's docs.py validation approach."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

import typer
import yaml
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Documentation validation and management tools")
console = Console()


def find_project_root() -> Path:
    """Find the provide-io root directory."""
    current = Path.cwd()
    while current != current.parent:
        if (current / "provide-foundry").exists() or (current / ".git").exists():
            return current
        current = current.parent
    return Path.cwd()


def find_mkdocs_projects() -> list[Path]:
    """Find all projects with mkdocs.yml files."""
    root = find_project_root()
    mkdocs_files = list(root.glob("*/mkdocs.yml"))
    return sorted([f.parent for f in mkdocs_files])


def read_mkdocs_config(project_path: Path) -> dict[str, Any] | None:
    """Read and parse mkdocs.yml config."""
    mkdocs_file = project_path / "mkdocs.yml"
    if not mkdocs_file.exists():
        return None

    try:
        with open(mkdocs_file) as f:
            return yaml.safe_load(f)
    except Exception as e:
        console.print(f"[red]Error reading {mkdocs_file}: {e}[/red]")
        return None


@app.command()
def list_projects():
    """List all projects with documentation."""
    projects = find_mkdocs_projects()

    table = Table(title="Documentation Projects")
    table.add_column("Project", style="cyan")
    table.add_column("Site Name", style="green")
    table.add_column("Docs Dir", style="yellow")
    table.add_column("Status", style="magenta")

    for project in projects:
        config = read_mkdocs_config(project)
        if config:
            site_name = config.get("site_name", "N/A")
            docs_dir = config.get("docs_dir", "docs")
            docs_path = project / docs_dir
            status = "✓" if docs_path.exists() else "✗"
            table.add_row(project.name, site_name, docs_dir, status)

    console.print(table)
    console.print(f"\n[green]Total projects: {len(projects)}[/green]")


@app.command()
def verify_config():
    """Verify mkdocs.yml configuration for all projects."""
    projects = find_mkdocs_projects()
    errors = []
    warnings = []

    console.print("[bold]Verifying mkdocs.yml configurations...[/bold]\n")

    for project in projects:
        config = read_mkdocs_config(project)
        if not config:
            errors.append(f"{project.name}: Failed to read mkdocs.yml")
            continue

        # Check required fields
        if "site_name" not in config:
            errors.append(f"{project.name}: Missing 'site_name'")

        if "theme" not in config:
            errors.append(f"{project.name}: Missing 'theme' configuration")
        elif config["theme"].get("name") != "material":
            warnings.append(f"{project.name}: Not using Material theme")

        # Check if docs directory exists
        docs_dir = config.get("docs_dir", "docs")
        docs_path = project / docs_dir
        if not docs_path.exists():
            errors.append(f"{project.name}: Docs directory '{docs_dir}' not found")

        # Check for shared theme usage
        extra_css = config.get("extra_css", [])
        uses_shared_theme = any("shared-theme" in str(css) for css in extra_css)
        if not uses_shared_theme:
            warnings.append(f"{project.name}: Not using shared theme")

        console.print(f"✓ {project.name}", style="green" if not errors else "yellow")

    # Report results
    console.print()
    if errors:
        console.print("[bold red]Errors:[/bold red]")
        for error in errors:
            console.print(f"  • {error}", style="red")

    if warnings:
        console.print("[bold yellow]Warnings:[/bold yellow]")
        for warning in warnings:
            console.print(f"  • {warning}", style="yellow")

    if not errors and not warnings:
        console.print("[bold green]All configurations valid![/bold green]")
        return 0

    return 1 if errors else 0


@app.command()
def verify_links(
    project: str = typer.Option(None, help="Specific project to check"),
    external: bool = typer.Option(False, help="Check external links (slow)"),
):
    """Verify internal and optionally external links in documentation."""
    if project:
        projects = [find_project_root() / project]
        if not (projects[0] / "mkdocs.yml").exists():
            console.print(
                f"[red]Project {project} not found or has no mkdocs.yml[/red]"
            )
            return 1
    else:
        projects = find_mkdocs_projects()

    console.print("[bold]Checking links in documentation...[/bold]\n")

    total_issues = 0

    for proj_path in projects:
        config = read_mkdocs_config(proj_path)
        if not config:
            continue

        docs_dir = proj_path / config.get("docs_dir", "docs")
        if not docs_dir.exists():
            continue

        console.print(f"[cyan]{proj_path.name}[/cyan]")

        # Find all markdown files
        md_files = list(docs_dir.glob("**/*.md"))

        for md_file in md_files:
            content = md_file.read_text()

            # Check for internal links
            internal_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)

            for link_text, link_url in internal_links:
                # Skip external URLs
                if link_url.startswith(("http://", "https://", "mailto:", "#")):
                    continue

                # Resolve relative link
                target = (md_file.parent / link_url).resolve()
                if not target.exists():
                    console.print(
                        f"  ✗ {md_file.relative_to(docs_dir)}: Broken link to {link_url}",
                        style="red",
                    )
                    total_issues += 1

        if total_issues == 0:
            console.print("  ✓ All internal links valid", style="green")

    console.print()
    if total_issues > 0:
        console.print(f"[bold red]Found {total_issues} broken links[/bold red]")
        return 1
    else:
        console.print("[bold green]All links valid![/bold green]")
        return 0


@app.command()
def check_structure():
    """Check documentation structure follows best practices."""
    projects = find_mkdocs_projects()

    console.print("[bold]Checking documentation structure...[/bold]\n")

    recommendations = []

    for project in projects:
        config = read_mkdocs_config(project)
        if not config:
            continue

        docs_dir = project / config.get("docs_dir", "docs")
        if not docs_dir.exists():
            continue

        console.print(f"[cyan]{project.name}[/cyan]")

        # Check for index.md
        if not (docs_dir / "index.md").exists():
            recommendations.append(f"{project.name}: Missing index.md")
            console.print("  ✗ Missing index.md", style="red")
        else:
            console.print("  ✓ Has index.md", style="green")

        # Check for common sections
        sections = [
            "getting-started",
            "tutorials",
            "guides",
            "reference",
            "api-reference",
        ]
        found_sections = []
        for section in sections:
            section_path = docs_dir / section
            if section_path.exists():
                found_sections.append(section)

        if found_sections:
            console.print(
                f"  ✓ Found sections: {', '.join(found_sections)}", style="green"
            )
        else:
            recommendations.append(
                f"{project.name}: Consider adding structured sections"
            )
            console.print("  ⚠ No standard sections found", style="yellow")

        console.print()

    if recommendations:
        console.print("[bold yellow]Recommendations:[/bold yellow]")
        for rec in recommendations:
            console.print(f"  • {rec}", style="yellow")
    else:
        console.print("[bold green]All projects follow good structure![/bold green]")

    return 0


@app.command()
def build_all(
    parallel: bool = typer.Option(
        False, "--parallel", "-p", help="Build projects in parallel"
    ),
):
    """Build all documentation projects."""
    projects = find_mkdocs_projects()

    console.print(f"[bold]Building {len(projects)} documentation projects...[/bold]\n")

    failed = []

    for project in projects:
        console.print(f"Building {project.name}...", style="cyan")

        try:
            result = subprocess.run(
                ["mkdocs", "build"],
                cwd=project,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0:
                console.print(f"  ✓ {project.name} built successfully", style="green")
            else:
                console.print(f"  ✗ {project.name} failed to build", style="red")
                console.print(f"    {result.stderr}", style="red dim")
                failed.append(project.name)

        except subprocess.TimeoutExpired:
            console.print(f"  ✗ {project.name} build timed out", style="red")
            failed.append(project.name)
        except FileNotFoundError:
            console.print(
                "[red]mkdocs not found. Install with: uv sync --group docs[/red]"
            )
            return 1

    console.print()
    if failed:
        console.print(f"[bold red]Failed to build: {', '.join(failed)}[/bold red]")
        return 1
    else:
        console.print("[bold green]All projects built successfully![/bold green]")
        return 0


@app.command()
def update_shared_theme():
    """Check which projects need to update their shared theme references."""
    projects = find_mkdocs_projects()

    console.print("[bold]Checking shared theme usage...[/bold]\n")

    needs_update = []
    using_shared = []
    not_using = []

    for project in projects:
        if project.name == "provide-foundry":
            continue  # Skip foundry itself

        config = read_mkdocs_config(project)
        if not config:
            continue

        extra_css = config.get("extra_css", [])
        extra_js = config.get("extra_javascript", [])

        has_theme_css = any("provide-theme.css" in str(css) for css in extra_css)
        has_termynal_css = any("termynal.css" in str(css) for css in extra_css)
        has_termynal_js = any("termynal.js" in str(js) for js in extra_js)
        has_custom_js = any("custom.js" in str(js) for js in extra_js)

        if has_theme_css and has_termynal_css and has_termynal_js and has_custom_js:
            using_shared.append(project.name)
            console.print(
                f"  ✓ {project.name}: Fully using shared theme", style="green"
            )
        elif has_theme_css:
            needs_update.append(project.name)
            console.print(
                f"  ⚠ {project.name}: Partial shared theme (missing Termynal)",
                style="yellow",
            )
        else:
            not_using.append(project.name)
            console.print(f"  ✗ {project.name}: Not using shared theme", style="red")

    console.print()
    console.print(f"[green]Using shared theme: {len(using_shared)}[/green]")
    console.print(f"[yellow]Needs update: {len(needs_update)}[/yellow]")
    console.print(f"[red]Not using: {len(not_using)}[/red]")

    if needs_update or not_using:
        console.print("\n[bold]Projects to update:[/bold]")
        for proj in needs_update + not_using:
            console.print(f"  • {proj}")


if __name__ == "__main__":
    app()

# 🏭⚒️🔚
