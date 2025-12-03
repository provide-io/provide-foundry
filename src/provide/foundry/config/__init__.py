"""Configuration and resource access for provide-foundry shared documentation assets."""

from __future__ import annotations

import shutil
import tomllib
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from importlib.abc import Traversable


def get_base_mkdocs_path() -> Path:
    """Get path to base mkdocs configuration file.

    Returns:
        Path to base-mkdocs.yml in the installed package.
    """
    resource: Traversable = files("provide.foundry.config") / "base-mkdocs.yml"
    # Convert Traversable to Path - this works for both installed and editable installs
    if hasattr(resource, "__fspath__"):
        return Path(resource.__fspath__())
    # Fallback for older Python or different resource types
    return Path(str(resource))


def get_theme_dir() -> Path:
    """Get path to theme directory in the installed package.

    Returns:
        Path to theme directory containing stylesheets, javascripts, data.
    """
    resource: Traversable = files("provide.foundry.theme")
    if hasattr(resource, "__fspath__"):
        return Path(resource.__fspath__())
    return Path(str(resource))


def extract_base_mkdocs(target_dir: Path | str) -> Path:
    """Extract base mkdocs configuration and theme assets to target directory.

    This function extracts to .provide/foundry/:
    - base-mkdocs.yml
    - theme/ (stylesheets, javascripts, data)
    - docs/_partials/ (shared documentation snippets)
    - gen_ref_pages.py (for mkdocs-gen-files plugin)

    Args:
        target_dir: Directory to extract files into (typically project root).

    Returns:
        Path to the extracted base-mkdocs.yml file.
    """
    target_path = Path(target_dir)
    provide_foundry_dir = target_path / ".provide" / "foundry"

    # Create .provide/foundry directory
    provide_foundry_dir.mkdir(parents=True, exist_ok=True)

    # Extract base-mkdocs.yml
    base_mkdocs_src = get_base_mkdocs_path()
    base_mkdocs_dst = provide_foundry_dir / "base-mkdocs.yml"
    shutil.copy2(base_mkdocs_src, base_mkdocs_dst)

    # Extract gen_ref_pages.py script
    gen_ref_src = files("provide.foundry.docs") / "gen_ref_pages.py"
    if hasattr(gen_ref_src, "__fspath__"):
        gen_ref_path = Path(gen_ref_src.__fspath__())
    else:
        gen_ref_path = Path(str(gen_ref_src))
    gen_ref_dst = provide_foundry_dir / "gen_ref_pages.py"
    shutil.copy2(gen_ref_path, gen_ref_dst)

    # Extract theme assets
    theme_src = get_theme_dir()
    theme_dst = provide_foundry_dir / "theme"

    # Remove existing theme directory if present
    if theme_dst.exists():
        shutil.rmtree(theme_dst)

    # Copy theme directory
    shutil.copytree(theme_src, theme_dst)

    # Extract documentation partials
    partials_src = files("provide.foundry.docs") / "_partials"
    partials_dst = provide_foundry_dir / "docs" / "_partials"

    # Remove existing partials directory if present
    if partials_dst.exists():
        shutil.rmtree(partials_dst)

    # Create docs directory
    (provide_foundry_dir / "docs").mkdir(exist_ok=True)

    # Copy partials directory
    if hasattr(partials_src, "__fspath__"):
        shutil.copytree(Path(partials_src.__fspath__()), partials_dst)
    else:
        # Fallback for resource types that don't support __fspath__
        partials_dst.mkdir(parents=True, exist_ok=True)
        for partial in partials_src.iterdir():
            if partial.name.endswith(".md"):
                shutil.copy2(
                    Path(str(partial)) if hasattr(partial, "__fspath__") else str(partial),
                    partials_dst / partial.name,
                )

    # Extract scripts (docs helper scripts)
    scripts_src = files("provide.foundry.scripts")
    scripts_dst = provide_foundry_dir / "scripts"

    # Remove existing scripts directory if present
    if scripts_dst.exists():
        shutil.rmtree(scripts_dst)

    # Copy scripts directory
    scripts_dst.mkdir(parents=True, exist_ok=True)
    if hasattr(scripts_src, "__fspath__"):
        for script in Path(scripts_src.__fspath__()).glob("*.py"):
            shutil.copy2(script, scripts_dst / script.name)
    else:
        for script in scripts_src.iterdir():
            if script.name.endswith(".py"):
                shutil.copy2(
                    Path(str(script)) if hasattr(script, "__fspath__") else str(script),
                    scripts_dst / script.name,
                )

    # Copy CSS files from theme to docs/css (for projects to use)
    css_src = theme_dst / "css"
    css_dst = target_path / "docs" / "css"
    if css_src.exists():
        css_dst.parent.mkdir(parents=True, exist_ok=True)
        if css_dst.exists():
            shutil.rmtree(css_dst)
        shutil.copytree(css_src, css_dst)
        # Create empty extra.css for project-specific overrides
        (css_dst / "extra.css").touch(exist_ok=True)

    # Copy JS files from theme to docs/js (for projects to use)
    js_src = theme_dst / "js"
    js_dst = target_path / "docs" / "js"
    if js_src.exists():
        js_dst.parent.mkdir(parents=True, exist_ok=True)
        if js_dst.exists():
            shutil.rmtree(js_dst)
        shutil.copytree(js_src, js_dst)

    return base_mkdocs_dst


def extract_makefile_provider(target_dir: Path | str) -> Path:
    """Extract Makefile.provider.tmpl to project root as Makefile.

    Args:
        target_dir: Directory to extract file into.

    Returns:
        Path to the extracted Makefile file.
    """
    target_path = Path(target_dir)

    makefile_src = files("provide.foundry.config") / "Makefile.provider.tmpl"
    if hasattr(makefile_src, "__fspath__"):
        src_path = Path(makefile_src.__fspath__())
    else:
        src_path = Path(str(makefile_src))

    makefile_dst = target_path / "Makefile"
    shutil.copy2(src_path, makefile_dst)
    return makefile_dst


def extract_python_makefile(target_dir: Path | str) -> Path:
    """Extract Makefile.python.tmpl to project root as Makefile.

    This provides a standardized Makefile for Python library projects with
    common targets for testing, linting, formatting, building, and documentation.

    Args:
        target_dir: Directory to extract file into (typically project root).

    Returns:
        Path to the extracted Makefile file.
    """
    target_path = Path(target_dir)

    makefile_src = files("provide.foundry.config") / "Makefile.python.tmpl"
    if hasattr(makefile_src, "__fspath__"):
        src_path = Path(makefile_src.__fspath__())
    else:
        src_path = Path(str(makefile_src))

    makefile_dst = target_path / "Makefile"
    shutil.copy2(src_path, makefile_dst)
    return makefile_dst


def extract_validate_examples_script(target_dir: Path | str) -> Path:
    """Extract validate_examples.tmpl.sh to project scripts/ directory.

    Args:
        target_dir: Directory to extract file into (typically project root).

    Returns:
        Path to the extracted validate_examples.sh file.
    """
    target_path = Path(target_dir)
    scripts_dir = target_path / "scripts"
    scripts_dir.mkdir(exist_ok=True)

    script_src = files("provide.foundry.scripts") / "validate_examples.tmpl.sh"
    if hasattr(script_src, "__fspath__"):
        src_path = Path(script_src.__fspath__())
    else:
        src_path = Path(str(script_src))

    script_dst = scripts_dir / "validate_examples.sh"
    shutil.copy2(src_path, script_dst)
    # Make script executable
    script_dst.chmod(0o755)
    return script_dst


def extract_clean_artifacts_script(target_dir: Path | str) -> Path:
    """Extract clean_artifacts.tmpl.sh to project scripts/ directory.

    Args:
        target_dir: Directory to extract file into (typically project root).

    Returns:
        Path to the extracted clean_artifacts.sh file.
    """
    target_path = Path(target_dir)
    scripts_dir = target_path / "scripts"
    scripts_dir.mkdir(exist_ok=True)

    script_src = files("provide.foundry.scripts") / "clean_artifacts.tmpl.sh"
    if hasattr(script_src, "__fspath__"):
        src_path = Path(script_src.__fspath__())
    else:
        src_path = Path(str(script_src))

    script_dst = scripts_dir / "clean_artifacts.sh"
    shutil.copy2(src_path, script_dst)
    # Make script executable
    script_dst.chmod(0o755)
    return script_dst


def extract_inject_partials_script(target_dir: Path | str) -> Path:
    """Extract inject_partials.py to project scripts/ directory.

    Args:
        target_dir: Directory to extract file into (typically project root).

    Returns:
        Path to the extracted inject_partials.py file.
    """
    target_path = Path(target_dir)
    scripts_dir = target_path / "scripts"
    scripts_dir.mkdir(exist_ok=True)

    script_src = files("provide.foundry.scripts") / "inject_partials.py"
    if hasattr(script_src, "__fspath__"):
        src_path = Path(script_src.__fspath__())
    else:
        src_path = Path(str(script_src))

    script_dst = scripts_dir / "inject_partials.py"
    shutil.copy2(src_path, script_dst)
    # Make script executable
    script_dst.chmod(0o755)
    return script_dst


def extract_mkdocs_hooks(target_dir: Path | str) -> Path:
    """Extract MkDocs hooks to project scripts/ directory.

    MkDocs requires hooks to be file paths, not Python module imports.
    This extracts the terraform_provider hook from foundry to a local file.

    Args:
        target_dir: Directory to extract file into (typically project root).

    Returns:
        Path to the extracted mkdocs_hooks.py file.
    """
    target_path = Path(target_dir)
    scripts_dir = target_path / "scripts"
    scripts_dir.mkdir(exist_ok=True)

    hook_src = files("provide.foundry.theme.hooks") / "terraform_provider.py"
    if hasattr(hook_src, "__fspath__"):
        src_path = Path(hook_src.__fspath__())
    else:
        src_path = Path(str(hook_src))

    hook_dst = scripts_dir / "mkdocs_hooks.py"
    shutil.copy2(src_path, hook_dst)
    return hook_dst


def extract_python_wrknv_tasks(target_dir: Path | str, merge: bool = True) -> Path:
    """Extract wrknv.python.tmpl task definitions to wrknv.toml.

    This provides standardized task definitions for Python library projects.
    If merge=True and wrknv.toml exists, the [tasks] section is merged with
    existing content, preserving custom tasks and other configuration sections.

    Args:
        target_dir: Directory to extract file into (typically project root).
        merge: If True, merge [tasks] with existing wrknv.toml. If False, replace entire file.

    Returns:
        Path to the wrknv.toml file.
    """
    target_path = Path(target_dir)
    wrknv_dst = target_path / "wrknv.toml"

    # Get template content
    template_src = files("provide.foundry.config") / "wrknv.python.tmpl"
    if hasattr(template_src, "__fspath__"):
        template_path = Path(template_src.__fspath__())
    else:
        template_path = Path(str(template_src))

    # Read template
    with template_path.open("rb") as f:
        template_data = tomllib.load(f)

    if merge and wrknv_dst.exists():
        # Merge with existing wrknv.toml
        with wrknv_dst.open("rb") as f:
            existing_data = tomllib.load(f)

        # Deep merge tasks section
        existing_tasks = existing_data.get("tasks", {})
        template_tasks = template_data.get("tasks", {})

        # Merge template tasks into existing (template takes precedence for standard tasks)
        def merge_dicts(base: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
            """Recursively merge dicts, with updates taking precedence."""
            result = base.copy()
            for key, value in updates.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_dicts(result[key], value)
                else:
                    result[key] = value
            return result

        merged_tasks = merge_dicts(existing_tasks, template_tasks)
        existing_data["tasks"] = merged_tasks

        # Write merged content
        _write_toml(wrknv_dst, existing_data)
    else:
        # Just copy template (no existing file or merge=False)
        shutil.copy2(template_path, wrknv_dst)

    return wrknv_dst


def _write_toml(path: Path, data: dict[str, Any]) -> None:
    """Write TOML data to file using tomli-w.

    Args:
        path: Path to write TOML file to
        data: Dictionary to serialize to TOML
    """
    from provide.foundation.serialization.toml import toml_dumps

    toml_str = toml_dumps(data)
    path.write_text(toml_str)


__all__ = [
    "extract_base_mkdocs",
    "extract_clean_artifacts_script",
    "extract_inject_partials_script",
    "extract_makefile_provider",
    "extract_mkdocs_hooks",
    "extract_python_makefile",
    "extract_python_wrknv_tasks",
    "extract_validate_examples_script",
    "get_base_mkdocs_path",
    "get_theme_dir",
]
