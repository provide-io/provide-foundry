# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Comprehensive tests for markdown export plugin."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path
import tempfile
from unittest.mock import Mock, patch

from mkdocs.config import Config
from mkdocs.structure.files import File
from mkdocs.structure.pages import Page
import pytest

from provide.foundry.mkdocs_plugins.markdown_export import MarkdownExportPlugin


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def plugin() -> MarkdownExportPlugin:
    """Create a plugin instance with default config."""
    plugin = MarkdownExportPlugin()
    plugin.config = {
        "enabled": True,
        "output_dir": "site-markdown",
        "include_api_reference": True,
        "structure": "mirror",
        "single_file": False,
        "single_file_name": "FULL.md",
        "incremental": True,
        "cache_file": ".markdown-export.cache",
        "verbose": False,
    }
    return plugin


@pytest.fixture
def mkdocs_config(temp_dir: Path) -> Mock:
    """Create a mock MkDocs config."""
    config = Mock(spec=Config)
    config.site_dir = str(temp_dir / "site")
    config.docs_dir = str(temp_dir / "docs")
    return config


class TestPluginConfiguration:
    """Tests for plugin configuration."""

    def test_plugin_initialization(self) -> None:
        """Test plugin initializes correctly."""
        plugin = MarkdownExportPlugin()
        assert hasattr(plugin, "config")
        assert hasattr(plugin, "cache")
        assert hasattr(plugin, "api_files")
        assert hasattr(plugin, "renamed_files")

    def test_config_defaults(self, plugin: MarkdownExportPlugin) -> None:
        """Test default configuration values."""
        assert plugin.config["enabled"] is True
        assert plugin.config["output_dir"] == "site-markdown"
        assert plugin.config["include_api_reference"] is True
        assert plugin.config["structure"] == "mirror"
        assert plugin.config["single_file"] is False
        assert plugin.config["incremental"] is True

    def test_on_config_disabled(self, plugin: MarkdownExportPlugin, mkdocs_config: Mock) -> None:
        """Test on_config when plugin is disabled."""
        plugin.config["enabled"] = False
        result = plugin.on_config(mkdocs_config)
        assert result == mkdocs_config
        assert not plugin._enabled

    def test_on_config_enabled(
        self, plugin: MarkdownExportPlugin, mkdocs_config: Mock, temp_dir: Path
    ) -> None:
        """Test on_config when plugin is enabled."""
        plugin.config["output_dir"] = str(temp_dir / "site-markdown")
        result = plugin.on_config(mkdocs_config)
        assert result == mkdocs_config
        assert plugin.output_path == temp_dir / "site-markdown"


class TestMirrorStructure:
    """Tests for mirror structure export."""

    def test_identify_api_reference(self, plugin: MarkdownExportPlugin) -> None:
        """Test identifying API reference pages."""
        # Create page with API path
        page = Mock(spec=Page)
        page.file = Mock(spec=File)
        page.file.src_path = "reference/api/client.md"

        assert plugin._is_api_reference(page)

        # Create non-API page
        page.file.src_path = "guide/getting-started.md"
        assert not plugin._is_api_reference(page)


class TestCollapsedStructure:
    """Tests for collapsed structure algorithm."""

    def test_collapse_solo_index_md(self, plugin: MarkdownExportPlugin, temp_dir: Path) -> None:
        """Test collapsing solo index.md files."""
        # Setup directory with solo index.md
        (temp_dir / "roadmap").mkdir()
        (temp_dir / "roadmap" / "index.md").write_text("# Roadmap")

        plugin.output_path = temp_dir
        plugin.renamed_files = {}

        # Run collapse
        plugin._collapse_structure()

        # Verify: roadmap/index.md -> roadmap.md
        assert not (temp_dir / "roadmap").exists()
        assert (temp_dir / "roadmap.md").exists()
        assert "roadmap/index.md" in plugin.renamed_files
        assert plugin.renamed_files["roadmap/index.md"] == "roadmap.md"

    def test_preserve_multi_file_directory(self, plugin: MarkdownExportPlugin, temp_dir: Path) -> None:
        """Test preserving directories with multiple files."""
        # Setup directory with multiple files
        (temp_dir / "guides").mkdir()
        (temp_dir / "guides" / "index.md").write_text("# Guides")
        (temp_dir / "guides" / "installation.md").write_text("# Installation")
        (temp_dir / "guides" / "usage.md").write_text("# Usage")

        plugin.output_path = temp_dir
        plugin.renamed_files = {}

        # Run collapse
        plugin._collapse_structure()

        # Verify: directory preserved
        assert (temp_dir / "guides").is_dir()
        assert (temp_dir / "guides" / "index.md").exists()
        assert (temp_dir / "guides" / "installation.md").exists()
        assert (temp_dir / "guides" / "usage.md").exists()
        assert "guides/index.md" not in plugin.renamed_files

    def test_preserve_directory_with_subdirectories(
        self, plugin: MarkdownExportPlugin, temp_dir: Path
    ) -> None:
        """Test preserving directories with subdirectories."""
        # Setup directory with subdirectories
        (temp_dir / "api").mkdir()
        (temp_dir / "api" / "index.md").write_text("# API")
        (temp_dir / "api" / "client").mkdir()
        (temp_dir / "api" / "client" / "index.md").write_text("# Client")

        plugin.output_path = temp_dir
        plugin.renamed_files = {}

        # Run collapse
        plugin._collapse_structure()

        # Verify: parent directory preserved, subdirectory collapsed
        assert (temp_dir / "api").is_dir()
        assert (temp_dir / "api" / "index.md").exists()
        assert not (temp_dir / "api" / "client").exists()
        assert (temp_dir / "api" / "client.md").exists()

    def test_collapse_multiple_levels(self, plugin: MarkdownExportPlugin, temp_dir: Path) -> None:
        """Test collapsing at multiple directory levels."""
        # Setup nested solo index.md files
        (temp_dir / "a" / "b" / "c").mkdir(parents=True)
        (temp_dir / "a" / "b" / "c" / "index.md").write_text("# C")

        plugin.output_path = temp_dir
        plugin.renamed_files = {}

        # Run collapse
        plugin._collapse_structure()

        # Verify: all collapsed
        assert not (temp_dir / "a" / "b" / "c").exists()
        assert (temp_dir / "a" / "b" / "c.md").exists()
        assert "a/b/c/index.md" in plugin.renamed_files

    def test_skip_root_index(self, plugin: MarkdownExportPlugin, temp_dir: Path) -> None:
        """Test that root index.md is not collapsed."""
        # Setup root index.md
        (temp_dir / "index.md").write_text("# Root")

        plugin.output_path = temp_dir
        plugin.renamed_files = {}

        # Run collapse
        plugin._collapse_structure()

        # Verify: root index.md preserved
        assert (temp_dir / "index.md").exists()
        assert "index.md" not in plugin.renamed_files


class TestCrossReferenceUpdates:
    """Tests for cross-reference updating."""

    def test_update_exact_links(self, plugin: MarkdownExportPlugin, temp_dir: Path) -> None:
        """Test updating exact path links."""
        # Setup renamed file
        plugin.renamed_files = {"roadmap/index.md": "roadmap.md"}
        plugin.output_path = temp_dir

        # Create file with link to renamed path
        (temp_dir / "about.md").write_text("See [Roadmap](roadmap/index.md)")

        # Update cross-references
        plugin._update_cross_references()

        # Verify link updated
        content = (temp_dir / "about.md").read_text()
        assert "](roadmap.md)" in content
        assert "](roadmap/index.md)" not in content

    def test_update_directory_links(self, plugin: MarkdownExportPlugin, temp_dir: Path) -> None:
        """Test updating directory-style links."""
        # Setup renamed file
        plugin.renamed_files = {"guide/concepts/index.md": "guide/concepts.md"}
        plugin.output_path = temp_dir

        # Create file with directory-style link
        (temp_dir / "index.md").write_text("See [Concepts](guide/concepts/)")

        # Update cross-references
        plugin._update_cross_references()

        # Verify link updated
        content = (temp_dir / "index.md").read_text()
        assert "](guide/concepts.md)" in content
        assert "](guide/concepts/)" not in content

    def test_update_multiple_links_in_file(self, plugin: MarkdownExportPlugin, temp_dir: Path) -> None:
        """Test updating multiple links in one file."""
        # Setup renamed files
        plugin.renamed_files = {
            "roadmap/index.md": "roadmap.md",
            "architecture/index.md": "architecture.md",
        }
        plugin.output_path = temp_dir

        # Create file with multiple links
        content = """# Home

- [Roadmap](roadmap/index.md)
- [Architecture](architecture/)
"""
        (temp_dir / "index.md").write_text(content)

        # Update cross-references
        plugin._update_cross_references()

        # Verify all links updated
        result = (temp_dir / "index.md").read_text()
        assert "](roadmap.md)" in result
        assert "](architecture.md)" in result

    def test_skip_files_without_changes(self, plugin: MarkdownExportPlugin, temp_dir: Path) -> None:
        """Test files without matching links are not modified."""
        # Setup renamed file
        plugin.renamed_files = {"roadmap/index.md": "roadmap.md"}
        plugin.output_path = temp_dir

        # Create file with no matching links
        original_content = "# About\n\nNo links here."
        (temp_dir / "about.md").write_text(original_content)

        # Update cross-references
        plugin._update_cross_references()

        # Verify file not modified
        assert (temp_dir / "about.md").read_text() == original_content


class TestAPIManifest:
    """Tests for API manifest generation."""

    def test_write_api_manifest_basic(self, plugin: MarkdownExportPlugin, temp_dir: Path) -> None:
        """Test basic API manifest generation."""
        plugin.output_path = temp_dir
        plugin.api_files = [
            "api/client/index.md",
            "api/server/index.md",
            "api/index.md",
        ]
        plugin.renamed_files = {}

        # Write manifest
        plugin._write_api_manifest()

        # Verify manifest created
        manifest_file = temp_dir / ".api-manifest.txt"
        assert manifest_file.exists()

        # Verify content
        content = manifest_file.read_text()
        assert "# API Reference Files Manifest" in content
        assert "# Total files: 3" in content
        assert "api/client/index.md" in content
        assert "api/server/index.md" in content
        assert "api/index.md" in content

    def test_api_manifest_with_collapsed_paths(self, plugin: MarkdownExportPlugin, temp_dir: Path) -> None:
        """Test API manifest with collapsed structure."""
        plugin.output_path = temp_dir
        plugin.api_files = [
            "api/client/index.md",
            "api/server/index.md",
        ]
        plugin.renamed_files = {
            "api/client/index.md": "api/client.md",
            "api/server/index.md": "api/server.md",
        }

        # Write manifest
        plugin._write_api_manifest()

        # Verify manifest uses collapsed paths
        content = (temp_dir / ".api-manifest.txt").read_text()
        assert "api/client.md" in content
        assert "api/server.md" in content
        assert "api/client/index.md" not in content

    def test_api_manifest_sorted(self, plugin: MarkdownExportPlugin, temp_dir: Path) -> None:
        """Test API manifest files are sorted."""
        plugin.output_path = temp_dir
        plugin.api_files = [
            "z/file.md",
            "a/file.md",
            "m/file.md",
        ]
        plugin.renamed_files = {}

        # Write manifest
        plugin._write_api_manifest()

        # Verify sorted order
        lines = [
            line
            for line in (temp_dir / ".api-manifest.txt").read_text().split("\n")
            if line and not line.startswith("#")
        ]
        assert lines == sorted(lines)


class TestCaching:
    """Tests for incremental build caching."""

    def test_load_empty_cache(self, plugin: MarkdownExportPlugin, temp_dir: Path) -> None:
        """Test loading non-existent cache."""
        plugin.config["cache_file"] = str(temp_dir / ".cache")
        plugin._load_cache()
        assert plugin.cache == {}

    def test_save_and_load_cache(self, plugin: MarkdownExportPlugin, temp_dir: Path) -> None:
        """Test saving and loading cache."""
        cache_path = temp_dir / ".cache"
        plugin.config["cache_file"] = str(cache_path)

        # Set cache data
        plugin.cache = {
            "test.md": 1234567890.0,
            "guide/index.md": 9876543210.0,
        }

        # Save cache
        plugin._save_cache()

        # Verify file created
        assert cache_path.exists()

        # Load cache in new plugin instance
        plugin2 = MarkdownExportPlugin()
        plugin2.config = plugin.config.copy()
        plugin2._load_cache()

        assert plugin2.cache == plugin.cache


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_on_post_build_mirror_structure(
        self, plugin: MarkdownExportPlugin, mkdocs_config: Mock, temp_dir: Path
    ) -> None:
        """Test on_post_build with mirror structure."""
        plugin.config["structure"] = "mirror"
        plugin.config["verbose"] = True
        plugin.output_path = temp_dir
        plugin._enabled = True

        # Run post-build (should not collapse)
        with patch.object(plugin, "_collapse_structure") as mock_collapse:
            plugin.on_post_build(mkdocs_config)
            mock_collapse.assert_not_called()

    def test_on_post_build_collapsed_structure(
        self, plugin: MarkdownExportPlugin, mkdocs_config: Mock, temp_dir: Path
    ) -> None:
        """Test on_post_build with collapsed structure."""
        plugin.config["structure"] = "collapsed"
        plugin.config["verbose"] = True
        plugin.output_path = temp_dir
        plugin._enabled = True

        # Create test file
        temp_dir.mkdir(parents=True, exist_ok=True)
        (temp_dir / "solo").mkdir()
        (temp_dir / "solo" / "index.md").write_text("# Solo")

        # Run post-build (should collapse)
        plugin.on_post_build(mkdocs_config)

        # Verify collapsed
        assert (temp_dir / "solo.md").exists()
