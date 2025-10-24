#!/usr/bin/env python3
"""
Documentation Aggregator for Provide Foundry

Collects documentation from all provide.io projects and creates a unified
documentation site while maintaining each project's ability to serve docs
independently.

Features:
- Cross-platform (Windows, macOS, Linux)
- No symlinks required
- Preserves project independence
- Handles cross-references
- Supports hot reload in development
"""

import argparse
import logging
from pathlib import Path
import re
import shutil
import sys
import time
from typing import Any

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import yaml

logger = logging.getLogger(__name__)


class ProjectConfig:
    """Configuration for a single project."""

    def __init__(self, name: str, config: dict[str, Any]):
        self.name = name
        self.source_path = Path(config["source"]).resolve()
        self.target = config["target"]
        self.nav_title = config["nav_title"]
        self.docs_dir = self.source_path / "docs"
        self.mkdocs_config = self.source_path / "mkdocs.yml"
        self.enabled = config.get("enabled", True)

    @property
    def exists(self) -> bool:
        """Check if project source exists."""
        return self.source_path.exists() and self.docs_dir.exists()

    def __repr__(self) -> str:
        return f"ProjectConfig(name='{self.name}', source='{self.source_path}')"


class DocsAggregator:
    """Main documentation aggregator."""

    def __init__(self, foundry_root: Path, manifest_path: Path | None = None):
        self.foundry_root = foundry_root
        self.manifest_path = manifest_path or foundry_root / "docs_manifest.yaml"
        self.docs_dir = foundry_root / "docs"
        self.aggregated_dir = foundry_root / ".docs_aggregated"
        self.projects: dict[str, ProjectConfig] = {}

        self._setup_logging()
        self._load_manifest()

    def _setup_logging(self):
        """Configure logging."""
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def _load_manifest(self):
        """Load projects manifest."""
        if not self.manifest_path.exists():
            logger.error(f"Manifest not found: {self.manifest_path}")
            sys.exit(1)

        with open(self.manifest_path) as f:
            manifest = yaml.safe_load(f)

        for name, config in manifest.get("projects", {}).items():
            project = ProjectConfig(name, config)
            if project.enabled:
                self.projects[name] = project
                logger.info(f"Loaded project: {project}")
            else:
                logger.info(f"Skipped disabled project: {name}")

    def collect_all(self) -> bool:
        """Collect documentation from all projects."""
        logger.info("🏗️ Starting documentation aggregation")

        # Clean aggregated directory
        if self.aggregated_dir.exists():
            shutil.rmtree(self.aggregated_dir)
        self.aggregated_dir.mkdir(exist_ok=True)

        # Copy shared theme first
        self._copy_shared_theme()

        # Copy foundry's own docs
        foundry_docs = self.docs_dir
        if foundry_docs.exists():
            logger.info("📋 Copying foundry documentation")
            for item in foundry_docs.iterdir():
                if item.is_file():
                    shutil.copy2(item, self.aggregated_dir)
                elif item.is_dir():
                    dest = self.aggregated_dir / item.name
                    if not dest.exists():
                        shutil.copytree(item, dest)

        # Collect from each project
        success_count = 0
        for name, project in self.projects.items():
            if self._collect_project(project):
                success_count += 1

        logger.info(f"✅ Aggregation complete: {success_count}/{len(self.projects)} projects")
        return success_count > 0

    def _copy_shared_theme(self):
        """Copy shared theme to aggregated docs directory."""
        shared_theme_src = self.foundry_root / "shared-theme"
        if not shared_theme_src.exists():
            logger.warning("⚠️ Shared theme directory not found")
            return

        logger.info("🎨 Copying shared theme")

        # Copy stylesheets
        stylesheets_src = shared_theme_src / "stylesheets"
        if stylesheets_src.exists():
            stylesheets_dest = self.aggregated_dir / "stylesheets"
            stylesheets_dest.mkdir(parents=True, exist_ok=True)
            for css_file in stylesheets_src.glob("*.css"):
                shutil.copy2(css_file, stylesheets_dest)

        # Copy javascripts
        javascripts_src = shared_theme_src / "javascripts"
        if javascripts_src.exists():
            javascripts_dest = self.aggregated_dir / "javascripts"
            javascripts_dest.mkdir(parents=True, exist_ok=True)
            for js_file in javascripts_src.glob("*.js"):
                shutil.copy2(js_file, javascripts_dest)

        # Copy assets
        assets_src = shared_theme_src / "assets"
        if assets_src.exists():
            assets_dest = self.aggregated_dir / "assets"
            if assets_dest.exists():
                shutil.rmtree(assets_dest)
            shutil.copytree(assets_src, assets_dest, dirs_exist_ok=True)

        logger.info("✅ Shared theme copied")

    def _collect_project(self, project: ProjectConfig) -> bool:
        """Collect documentation from a single project."""
        if not project.exists:
            logger.warning(f"⚠️ Project not found: {project.name} at {project.source_path}")
            return False

        logger.info(f"📦 Collecting {project.name} documentation")

        try:
            # Create target directory
            target_dir = self.aggregated_dir / project.target
            if target_dir.exists():
                shutil.rmtree(target_dir)
            target_dir.mkdir(parents=True, exist_ok=True)

            # Copy documentation files
            shutil.copytree(
                project.docs_dir,
                target_dir,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
            )

            # Process markdown files for cross-references
            self._process_markdown_files(target_dir, project)

            # Copy any generated API docs if they exist
            api_source = project.source_path / "site" / "api"
            if api_source.exists():
                api_target = target_dir / "api"
                if api_target.exists():
                    shutil.rmtree(api_target)
                shutil.copytree(api_source, api_target, dirs_exist_ok=True)

            logger.info(f"✅ Collected {project.name}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to collect {project.name}: {e}")
            return False

    def _process_markdown_files(self, target_dir: Path, project: ProjectConfig):
        """Process markdown files to fix cross-references."""
        for md_file in target_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")

                # Fix relative references to other projects
                # Pattern: ../other-project/path -> /other-project/path
                content = self._fix_cross_references(content, project)

                # Fix asset references
                content = self._fix_asset_references(content, project)

                md_file.write_text(content, encoding="utf-8")

            except Exception as e:
                logger.warning(f"⚠️ Failed to process {md_file}: {e}")

    def _fix_cross_references(self, content: str, project: ProjectConfig) -> str:
        """Fix cross-references between projects."""
        # Pattern for relative references to sibling projects
        # ../project-name/path -> /project-name/path in aggregated context

        def replace_ref(match):
            full_match = match.group(0)
            ref_path = match.group(1)

            # Check if this is a reference to another project
            for other_name, other_project in self.projects.items():
                if other_name != project.name:
                    # Try different patterns that might indicate cross-references
                    project_patterns = [
                        f"../{other_project.source_path.name}",
                        f"../{other_name}",
                        f"../{other_project.target}",
                    ]

                    for pattern in project_patterns:
                        if ref_path.startswith(pattern):
                            # Replace with aggregated path
                            remainder = ref_path[len(pattern) :].lstrip("/")
                            new_path = f"/{other_project.target}/" + remainder
                            return full_match.replace(ref_path, new_path)

            return full_match

        # Match markdown links [text](path) and reference links [text]: path
        patterns = [
            r"\[([^\]]+)\]\(([^)]+)\)",  # [text](path)
            r"\[([^\]]+)\]:\s*([^\s]+)",  # [text]: path
        ]

        for pattern in patterns:
            content = re.sub(pattern, replace_ref, content)

        return content

    def _fix_asset_references(self, content: str, project: ProjectConfig) -> str:
        """Fix asset references (images, CSS, JS)."""
        # This is a placeholder for asset reference fixing
        # Could be expanded to handle project-specific assets
        return content

    def generate_navigation(self) -> dict[str, Any]:
        """Generate navigation structure for aggregated site."""
        nav = [{"Home": "index.md"}]

        # Add each project to navigation
        for name, project in self.projects.items():
            if project.exists:
                nav.append({project.nav_title: f"{project.target}/"})

        return {"nav": nav}

    def watch_mode(self):
        """Run in watch mode for development."""
        logger.info("👀 Starting watch mode")

        class ProjectWatcher(FileSystemEventHandler):
            def __init__(self, aggregator: DocsAggregator):
                self.aggregator = aggregator
                self.last_update = 0

            def on_any_event(self, event):
                # Debounce rapid file changes
                now = time.time()
                if now - self.last_update < 1.0:
                    return

                if event.is_directory:
                    return

                # Only watch markdown and yaml files
                if not any(event.src_path.endswith(ext) for ext in [".md", ".yml", ".yaml"]):
                    return

                logger.info(f"📝 Detected change: {event.src_path}")
                self.aggregator.collect_all()
                self.last_update = now

        # Initial collection
        self.collect_all()

        # Set up watchers
        observer = Observer()
        handler = ProjectWatcher(self)

        # Watch foundry docs
        if self.docs_dir.exists():
            observer.schedule(handler, str(self.docs_dir), recursive=True)

        # Watch each project's docs
        for project in self.projects.values():
            if project.exists:
                observer.schedule(handler, str(project.docs_dir), recursive=True)

        observer.start()

        try:
            logger.info("🔄 Watching for changes... (Ctrl+C to stop)")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Stopping watch mode")
            observer.stop()

        observer.join()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Provide Foundry Documentation Aggregator")
    parser.add_argument("command", choices=["collect", "watch"], help="Command to run")
    parser.add_argument("--manifest", type=Path, help="Path to docs manifest file")
    parser.add_argument("--foundry-root", type=Path, default=Path.cwd(), help="Path to foundry root directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize aggregator
    aggregator = DocsAggregator(foundry_root=args.foundry_root, manifest_path=args.manifest)

    # Run command
    if args.command == "collect":
        success = aggregator.collect_all()
        sys.exit(0 if success else 1)
    elif args.command == "watch":
        aggregator.watch_mode()


if __name__ == "__main__":
    main()
