#!/usr/bin/env python
"""Validate documentation standardization across all projects."""

from __future__ import annotations

from pathlib import Path
import sys


def check_project_standardization(project_path: Path) -> dict:
    """Check if project follows standardization requirements."""
    issues = []

    # Check 1: Has Makefile
    if not (project_path / "Makefile").exists():
        issues.append("Missing Makefile")

    # Check 2: Has .provide/foundry/
    provide_dir = project_path / ".provide" / "foundry"
    if not provide_dir.exists():
        issues.append("Missing .provide/foundry/ (run we run docs.setup)")
    else:
        # Check extracted files are present
        required = [
            "base-mkdocs.yml",
            "theme",
            "docs/_partials",
            "gen_ref_pages.py",
        ]
        for req in required:
            if not (provide_dir / req).exists():
                issues.append(f"Missing .provide/foundry/{req}")

    # Check 3: Has mkdocs.yml with INHERIT directive
    mkdocs_yml = project_path / "mkdocs.yml"
    if mkdocs_yml.exists():
        content = mkdocs_yml.read_text()
        # provide-foundation is known to not use INHERIT - that's OK
        if (
            "INHERIT: .provide/foundry/base-mkdocs.yml" not in content
            and project_path.name != "provide-foundation"
        ):
            issues.append("mkdocs.yml doesn't use INHERIT directive")
    else:
        issues.append("Missing mkdocs.yml")

    # Check 4: Has docs/ directory
    if not (project_path / "docs").exists():
        issues.append("Missing docs/ directory")

    # Check 5: Has wrknv.toml with docs tasks (optional)
    wrknv_toml = project_path / "wrknv.toml"
    if wrknv_toml.exists():
        content = wrknv_toml.read_text()
        if "[tasks.docs" not in content:
            issues.append("wrknv.toml missing docs tasks")

    return {
        "project": project_path.name,
        "compliant": len(issues) == 0,
        "issues": issues,
    }


def main() -> int:
    """Check all projects in workspace."""
    workspace = Path("/Users/tim/code/gh/provide-io")

    # Get all projects with mkdocs.yml
    projects = sorted(workspace.glob("*/mkdocs.yml"))

    results = []
    for mkdocs_file in projects:
        project_path = mkdocs_file.parent
        result = check_project_standardization(project_path)
        results.append(result)

    # Print report
    print("=" * 70)
    print("DOCUMENTATION STANDARDIZATION REPORT")
    print("=" * 70)
    print()

    compliant_count = sum(1 for r in results if r["compliant"])

    for result in results:
        status = "✅" if result["compliant"] else "❌"
        print(f"{status} {result['project']}")
        if result["issues"]:
            for issue in result["issues"]:
                print(f"    - {issue}")
            print()

    print("=" * 70)
    print(f"Compliant: {compliant_count}/{len(results)}")
    print("=" * 70)

    return 0 if compliant_count == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
