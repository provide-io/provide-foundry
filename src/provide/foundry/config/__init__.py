"""Configuration and resource access for provide-foundry shared documentation assets."""

from __future__ import annotations

import shutil
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING

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


def get_makefile_inc_path() -> Path:
    """Get path to Makefile.docs.inc in the installed package.

    Returns:
        Path to Makefile.docs.inc file.
    """
    resource: Traversable = files("provide.foundry.config") / "Makefile.docs.inc"
    if hasattr(resource, "__fspath__"):
        return Path(resource.__fspath__())
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

    return base_mkdocs_dst


def extract_makefile_inc(target_dir: Path | str) -> Path:
    """Extract Makefile.docs.inc to .provide/foundry/ directory.

    Args:
        target_dir: Directory to extract file into.

    Returns:
        Path to the extracted Makefile.docs.inc file.
    """
    target_path = Path(target_dir)
    provide_foundry_dir = target_path / ".provide" / "foundry"
    provide_foundry_dir.mkdir(parents=True, exist_ok=True)

    makefile_src = get_makefile_inc_path()
    makefile_dst = provide_foundry_dir / "Makefile.docs.inc"
    shutil.copy2(makefile_src, makefile_dst)
    return makefile_dst


__all__ = [
    "extract_base_mkdocs",
    "extract_makefile_inc",
    "get_base_mkdocs_path",
    "get_makefile_inc_path",
    "get_theme_dir",
]
