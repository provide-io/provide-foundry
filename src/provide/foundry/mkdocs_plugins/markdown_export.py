# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
MkDocs plugin to export documentation as markdown files.

Exports the aggregated monorepo documentation to site/md/ preserving:
- Directory structure matching the HTML site
- Markdown extensions (pymdownx, admonitions, etc.)
- Cross-references as relative links
- Optional API reference inclusion
- Incremental builds based on file timestamps
- Single concatenated file option

Controlled by environment variables:
- DOCS_FORMAT=markdown (or both) to enable
- DOCS_INCLUDE_API=false to skip API reference
- DOCS_SINGLE_FILE=true to generate FULL.md
- DOCS_INCREMENTAL=false to disable incremental builds
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, ClassVar

from mkdocs.config import config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page

from provide.foundation.file import atomic_write_text

log = logging.getLogger("mkdocs.plugins.markdown_export")


class MarkdownExportPlugin(BasePlugin):  # type: ignore[type-arg,no-untyped-call]
    """Plugin to export aggregated documentation as markdown files."""

    config_scheme = (
        ("enabled", config_options.Type(bool, default=False)),
        ("output_dir", config_options.Type(str, default="site/md")),
        ("include_api_reference", config_options.Type(bool, default=True)),
        ("include_generated", config_options.Type(bool, default=True)),
        ("preserve_extensions", config_options.Type(bool, default=True)),
        ("incremental", config_options.Type(bool, default=True)),
        ("single_file", config_options.Type(bool, default=False)),
        ("single_file_name", config_options.Type(str, default="FULL.md")),
        ("structure", config_options.Type(str, default="mirror")),
        ("cache_file", config_options.Type(str, default=".markdown-export.cache")),
        ("verbose", config_options.Type(bool, default=False)),
    )

    # API reference patterns to identify generated content
    API_PATTERNS: ClassVar[list[str]] = [
        "/reference/",
        "/api/",
        "SUMMARY.md",
    ]

    def __init__(self) -> None:
        """Initialize plugin state."""
        super().__init__()
        self.cache: dict[str, float] = {}
        self.output_path: Path | None = None
        self.files_processed: int = 0
        self.files_skipped: int = 0
        self.single_file_content: list[tuple[str, str]] = []  # (title, content)
        self.api_files: list[str] = []  # Track API reference files
        self.renamed_files: dict[str, str] = {}  # old_path -> new_path for collapsed structure
        self._enabled: bool = False

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        """Initialize plugin with config."""
        # Check if plugin is enabled via config or environment
        enabled_via_config = self.config.get("enabled", False)

        # Check DOCS_FORMAT environment variable
        docs_format = os.environ.get("DOCS_FORMAT", "html").lower()
        enabled_via_env = docs_format in ("markdown", "both")

        self._enabled = enabled_via_config or enabled_via_env

        if not self._enabled:
            log.debug("Markdown export plugin is disabled")
            return config

        # Apply environment variable overrides
        if "DOCS_INCLUDE_API" in os.environ:
            include_api = os.environ["DOCS_INCLUDE_API"].lower() in ("true", "1", "yes")
            self.config["include_api_reference"] = include_api

        if "DOCS_SINGLE_FILE" in os.environ:
            single_file = os.environ["DOCS_SINGLE_FILE"].lower() in ("true", "1", "yes")
            self.config["single_file"] = single_file

        if "DOCS_INCREMENTAL" in os.environ:
            incremental = os.environ["DOCS_INCREMENTAL"].lower() in ("true", "1", "yes")
            self.config["incremental"] = incremental

        if "DOCS_STRUCTURE" in os.environ:
            structure = os.environ["DOCS_STRUCTURE"].lower()
            if structure in ("mirror", "collapsed"):
                self.config["structure"] = structure
            else:
                log.warning(f"Invalid DOCS_STRUCTURE value: {structure}, using 'mirror'")

        # Set up verbose logging
        verbose = self.config.get("verbose", False)
        if "DOCS_VERBOSE" in os.environ:
            verbose = os.environ["DOCS_VERBOSE"].lower() in ("true", "1", "yes")

        if verbose:
            log.setLevel(logging.DEBUG)

        # Set up output directory
        self.output_path = Path(self.config["output_dir"])
        log.info(
            f"Markdown export: {self.output_path} | "
            f"API={self.config['include_api_reference']}, "
            f"Single={self.config['single_file']}, "
            f"Structure={self.config['structure']}, "
            f"Incremental={self.config['incremental']}"
        )

        # Load cache for incremental builds
        if self.config["incremental"]:
            self._load_cache()

        return config

    def on_files(self, files: Files, config: MkDocsConfig) -> Files:
        """Process files after monorepo aggregation."""
        if not self._enabled:
            return files
        log.info(f"Markdown export processing {len(files)} files")
        return files

    def on_nav(self, nav: Navigation, config: MkDocsConfig, files: Files) -> Navigation:
        """Process navigation structure."""
        if not self._enabled:
            return nav
        if self.config.get("verbose", False):
            log.debug(f"Navigation has {len(nav.pages)} pages")
        return nav

    def on_page_markdown(
        self,
        markdown: str,
        page: Page,
        config: MkDocsConfig,
        files: Files,
    ) -> str:
        """Process page markdown before rendering."""
        # We don't modify markdown during build, just pass through
        return markdown

    def on_post_page(
        self,
        output: str,
        page: Page,
        config: MkDocsConfig,
    ) -> str:
        """Process each page after rendering (but we export markdown, not HTML)."""
        if not self._enabled:
            return output

        # Skip if this is an API reference page and we're not including it
        if not self.config["include_api_reference"] and self._is_api_reference(page):
            self.files_skipped += 1
            if self.config.get("verbose", False):
                log.debug(f"Skipping API reference: {page.file.src_path}")
            return output

        # Export the markdown for this page
        self._export_page_markdown(page)
        return output

    def on_post_build(self, config: MkDocsConfig) -> None:
        """Finalize export after build completes."""
        if not self._enabled:
            return

        log.info(f"Export: {self.files_processed} processed, {self.files_skipped} skipped")

        # Generate single concatenated file if requested
        if self.config["single_file"]:
            self._generate_single_file()

        # Apply collapsed structure if requested
        if self.config["structure"] == "collapsed":
            self._collapse_structure()
            self._update_cross_references()

        # Save cache for next incremental build
        if self.config["incremental"]:
            self._save_cache()

        # Write API manifest file
        if self.api_files:
            self._write_api_manifest()

        # Log summary
        if self.output_path:
            total_size = sum(f.stat().st_size for f in self.output_path.rglob("*.md") if f.is_file())
            size_mb = total_size / (1024 * 1024)
            log.info(f"Exported {size_mb:.1f} MB of markdown to {self.output_path}")
            log.info(f"API reference files: {len(self.api_files)} tracked in manifest")

    def _is_api_reference(self, page: Page) -> bool:
        """Check if a page is API reference documentation."""
        src_path = str(page.file.src_path)
        return any(pattern in src_path for pattern in self.API_PATTERNS)

    def _should_process(self, page: Page) -> bool:
        """Check if page should be processed based on incremental build cache."""
        if not self.config["incremental"]:
            return True

        src_path = str(page.file.abs_src_path)
        if not Path(src_path).exists():
            return True

        # Check if source file is newer than cached version
        current_mtime = Path(src_path).stat().st_mtime
        cached_mtime = self.cache.get(src_path, 0.0)

        return current_mtime > cached_mtime

    def _export_page_markdown(self, page: Page) -> None:  # noqa: C901
        """Export a single page's markdown to the output directory."""
        if not self.output_path:
            log.warning("Output path not set, skipping export")
            return

        # Check if we should process this file
        if not self._should_process(page):
            self.files_skipped += 1
            if self.config.get("verbose", False):
                log.debug(f"Skipping unchanged: {page.file.src_path}")
            return

        # Determine output path
        # Use the dest_path (which mirrors site/ structure) but change extension to .md
        dest_path_str = str(page.file.dest_path)
        if dest_path_str.endswith(".html"):
            dest_path_str = dest_path_str[:-5] + ".md"

        output_file = self.output_path / dest_path_str

        # Create parent directories
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Read the original markdown source
        try:
            abs_src_path = getattr(page.file, "abs_src_path", None)
            if abs_src_path and Path(abs_src_path).exists():
                source_content = Path(abs_src_path).read_text(encoding="utf-8")
            else:
                # Fallback to page markdown (already processed)
                source_content = page.markdown or ""

            # Add frontmatter with metadata
            frontmatter = self._generate_frontmatter(page)

            # Write markdown file atomically
            atomic_write_text(output_file, frontmatter + source_content, encoding="utf-8")

            # Track API reference files
            if self._is_api_reference(page):
                # Store relative path from site-markdown root
                relative_path = output_file.relative_to(self.output_path)
                self.api_files.append(str(relative_path))

            # Store for single file generation
            if self.config["single_file"]:
                self.single_file_content.append((page.title or "Untitled", source_content))

            # Update cache
            if self.config["incremental"] and hasattr(page.file, "abs_src_path"):
                src_path = str(page.file.abs_src_path)
                if Path(src_path).exists():
                    self.cache[src_path] = Path(src_path).stat().st_mtime

            self.files_processed += 1
            if self.config.get("verbose", False):
                log.debug(f"Exported: {page.file.src_path} → {output_file}")

        except Exception as e:
            log.error(f"Failed to export {page.file.src_path}: {e}")

    def _generate_frontmatter(self, page: Page) -> str:
        """Generate YAML frontmatter for exported markdown."""
        metadata: dict[str, Any] = {}

        if page.title:
            metadata["title"] = page.title

        if hasattr(page, "meta") and page.meta:
            # Include custom metadata from the source
            metadata.update(page.meta)

        # Add export metadata
        metadata["exported_from"] = str(page.file.src_path)

        if not metadata:
            return ""

        # Format as YAML frontmatter
        frontmatter_lines = ["---"]
        for key, value in metadata.items():
            # Simple YAML formatting (doesn't handle complex types)
            if isinstance(value, str):
                # Escape quotes
                value_str = value.replace('"', '\\"')
                frontmatter_lines.append(f'{key}: "{value_str}"')
            elif isinstance(value, (int, float, bool)):
                frontmatter_lines.append(f"{key}: {value}")
            elif isinstance(value, list):
                frontmatter_lines.append(f"{key}:")
                for item in value:
                    frontmatter_lines.append(f"  - {item}")
        frontmatter_lines.append("---\n")

        return "\n".join(frontmatter_lines)

    def _generate_single_file(self) -> None:
        """Generate single concatenated markdown file."""
        if not self.output_path:
            return

        single_file_path = self.output_path / self.config["single_file_name"]
        log.info(f"Generating single concatenated file: {single_file_path}")

        # Build content in memory
        parts = []
        parts.append("# Complete Documentation\n\n")
        parts.append(
            "This file contains the complete documentation concatenated into a single markdown file.\n\n"
        )
        parts.append("---\n\n")

        # Table of contents
        parts.append("## Table of Contents\n\n")
        for i, (title, _) in enumerate(self.single_file_content, 1):
            anchor = title.lower().replace(" ", "-").replace("/", "-")
            parts.append(f"{i}. [{title}](#{anchor})\n")
        parts.append("\n---\n\n")

        # Write each section
        for title, content in self.single_file_content:
            parts.append(f"\n\n## {title}\n\n")
            parts.append(content)
            parts.append("\n\n---\n")

        # Write atomically
        content = "".join(parts)
        atomic_write_text(single_file_path, content, encoding="utf-8")

        log.info(
            f"Single file generated: {len(self.single_file_content)} sections, {len(content) / 1024:.1f} KB"
        )

    def _load_cache(self) -> None:
        """Load incremental build cache."""
        cache_path = Path(self.config["cache_file"])
        if cache_path.exists():
            try:
                self.cache = json.loads(cache_path.read_text())
                log.debug(f"Loaded cache with {len(self.cache)} entries")
            except Exception as e:
                log.warning(f"Failed to load cache: {e}")
                self.cache = {}
        else:
            self.cache = {}

    def _save_cache(self) -> None:
        """Save incremental build cache."""
        cache_path = Path(self.config["cache_file"])
        try:
            cache_path.write_text(json.dumps(self.cache, indent=2))
            log.debug(f"Saved cache with {len(self.cache)} entries")
        except Exception as e:
            log.warning(f"Failed to save cache: {e}")

    def _write_api_manifest(self) -> None:
        """Write API reference files manifest."""
        if not self.output_path:
            return

        manifest_path = self.output_path / ".api-manifest.txt"
        try:
            # Apply renamed paths if collapsed structure was used
            sorted_files = sorted(self.renamed_files.get(p, p) for p in self.api_files)

            # Build manifest content
            lines = []
            lines.append("# API Reference Files Manifest\n")
            lines.append("# Generated by markdown-export plugin\n")
            lines.append(f"# Total files: {len(sorted_files)}\n")
            lines.append("#\n")
            lines.append("# Use this manifest to:\n")
            lines.append("#   - Remove API files: xargs rm < .api-manifest.txt\n")
            lines.append("#   - Exclude from processing: grep -v -f .api-manifest.txt\n")
            lines.append("#   - List API directories: cut -d/ -f1-2 | sort -u\n")
            lines.append("#\n\n")

            for file_path in sorted_files:
                lines.append(f"{file_path}\n")

            # Write atomically
            content = "".join(lines)
            atomic_write_text(manifest_path, content, encoding="utf-8")

            log.info(f"API manifest written: {manifest_path} ({len(sorted_files)} files)")

        except Exception as e:
            log.warning(f"Failed to write API manifest: {e}")

    def _collapse_structure(self) -> None:
        """Collapse solo index.md files into parent.md format."""
        if not self.output_path:
            return

        log.info("Applying collapsed structure...")
        collapsed_count = 0

        # Find all index.md files, process bottom-up
        index_files = sorted(self.output_path.rglob("index.md"), reverse=True)

        for index_file in index_files:
            parent_dir = index_file.parent

            # Skip root index.md
            if parent_dir == self.output_path:
                continue

            # Check if this is the only .md file in directory
            md_files = list(parent_dir.glob("*.md"))
            subdirs = [p for p in parent_dir.iterdir() if p.is_dir() and p.name != "__pycache__"]

            # Collapse if it's solo index.md with no subdirectories
            if len(md_files) == 1 and md_files[0].name == "index.md" and not subdirs:
                # Move dir/index.md -> dir.md
                new_path = parent_dir.with_suffix(".md")
                old_relative = str(index_file.relative_to(self.output_path))
                new_relative = str(new_path.relative_to(self.output_path))

                # Track rename for cross-reference updates
                self.renamed_files[old_relative] = new_relative

                # Move file
                index_file.rename(new_path)
                # Remove empty directory
                parent_dir.rmdir()

                collapsed_count += 1
                if self.config.get("verbose", False):
                    log.debug(f"Collapsed: {old_relative} → {new_relative}")

        log.info(f"Collapsed {collapsed_count} solo index.md files")

    def _update_cross_references(self) -> None:
        """Update cross-references to collapsed files."""
        if not self.output_path or not self.renamed_files:
            return

        log.info("Updating cross-references...")
        updated_count = 0

        # Process all markdown files
        for md_file in self.output_path.rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            updated = False

            # Update references to renamed files
            for old_path, new_path in self.renamed_files.items():
                # Match various link formats
                patterns = [
                    (f"]({old_path})", f"]({new_path})"),  # Exact match
                    (f"]({old_path[:-9]})", f"]({new_path})"),  # Without /index.md
                    (f"]({old_path[:-9]}/)", f"]({new_path})"),  # With trailing slash
                ]

                for old_pattern, new_pattern in patterns:
                    if old_pattern in content:
                        content = content.replace(old_pattern, new_pattern)
                        updated = True

            if updated:
                atomic_write_text(md_file, content, encoding="utf-8")
                updated_count += 1

        log.info(f"Updated cross-references in {updated_count} files")
