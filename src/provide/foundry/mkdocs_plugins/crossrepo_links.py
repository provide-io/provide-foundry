"""
MkDocs plugin to fix cross-repository documentation links.

Transforms links to use root-level package paths:
- ../pyvider/ → /pyvider/
- ../terraform-provider-pyvider/ → /terraform-provider-pyvider/
- Handles both relative and absolute links
"""

from __future__ import annotations

import logging
import re
from typing import ClassVar

from mkdocs.config import config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

log = logging.getLogger("mkdocs.plugins.crossrepo_links")


class CrossRepoLinksPlugin(BasePlugin):  # type: ignore[type-arg,no-untyped-call]
    """Plugin to transform cross-repository links to root-level paths."""

    config_scheme = (
        ("enabled", config_options.Type(bool, default=True)),
        ("verbose", config_options.Type(bool, default=False)),
    )

    # Package names that should be accessible at root level
    PACKAGES: ClassVar[list[str]] = [
        "provide-foundation",
        "provide-testkit",
        "pyvider",
        "pyvider-cty",
        "pyvider-hcl",
        "pyvider-rpcplugin",
        "pyvider-components",
        "terraform-provider-pyvider",
        "tofusoup",
        "flavorpack",
        "wrknv",
        "supsrc",
        "plating",
    ]

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        """Initialize plugin with config."""
        if self.config.get("verbose"):
            log.setLevel(logging.DEBUG)
        log.info(f"CrossRepoLinks plugin initialized for {len(self.PACKAGES)} packages")
        return config

    def on_page_markdown(
        self,
        markdown: str,
        page: Page,
        config: MkDocsConfig,
        files: Files,
    ) -> str:
        """Transform links in raw markdown before rendering."""
        if not self.config.get("enabled", True):
            return markdown

        # Count transformations for logging
        transform_count = 0

        # Pattern 1: Transform relative links like ../package-name/
        # Matches: [text](../package-name/...)
        for package in self.PACKAGES:
            # Handle various relative link patterns
            patterns = [
                # ../package/ or ../package/path
                (rf"\[([^\]]+)\]\(\.\./({re.escape(package)}/?[^\)]*)\)", r"[\1](/\2)"),
                # Just package/ (relative to current)
                (rf"\[([^\]]+)\]\(({re.escape(package)}/?[^\)]*)\)", r"[\1](/\2)"),
            ]

            for pattern, replacement in patterns:
                new_markdown, count = re.subn(pattern, replacement, markdown)
                if count > 0:
                    transform_count += count
                    if self.config.get("verbose"):
                        log.debug(f"Transformed {count} links for package {package}")
                markdown = new_markdown

        # Pattern 2: Fix nested paths to root paths
        # Transform /pyvider-framework/pyvider/ → /pyvider/
        nested_mappings = {
            "/pyvider-framework/pyvider/": "/pyvider/",
            "/pyvider-framework/pyvider-cty/": "/pyvider-cty/",
            "/pyvider-framework/pyvider-hcl/": "/pyvider-hcl/",
            "/pyvider-framework/pyvider-rpcplugin/": "/pyvider-rpcplugin/",
            "/pyvider-framework/pyvider-components/": "/pyvider-components/",
            "/pyvider-framework/tofusoup/": "/tofusoup/",
            "/pyvider-framework/terraform-provider-pyvider/": "/terraform-provider-pyvider/",
            "/foundation/foundation/": "/provide-foundation/",
            "/foundation/testkit/": "/provide-testkit/",
            "/development-tools/flavorpack/": "/flavorpack/",
            "/development-tools/wrknv/": "/wrknv/",
            "/development-tools/supsrc/": "/supsrc/",
            "/development-tools/plating/": "/plating/",
        }

        for nested_path, root_path in nested_mappings.items():
            pattern = rf"\[([^\]]+)\]\({re.escape(nested_path)}([^\)]*)\)"
            replacement = rf"[\1]({root_path}\2)"
            new_markdown, count = re.subn(pattern, replacement, markdown)
            if count > 0:
                transform_count += count
                if self.config.get("verbose"):
                    log.debug(f"Transformed {count} nested paths: {nested_path} → {root_path}")
            markdown = new_markdown

        # Pattern 3: Fix broken ecosystem.md specific patterns
        # The ecosystem.md file has many links like [Pyvider](../pyvider/)
        # that should become [Pyvider](/pyvider/)

        if transform_count > 0:
            log.info(f"Transformed {transform_count} links in {page.file.src_path}")

        return markdown

    def on_page_content(
        self,
        html: str,
        page: Page,
        config: MkDocsConfig,
        files: Files,
    ) -> str:
        """Optional: Transform HTML links after markdown rendering."""
        if not self.config.get("enabled", True):
            return html

        # Additional HTML-level transformations if needed
        # This can catch links that weren't in markdown format

        for package in self.PACKAGES:
            # Transform href="../package/" to href="/package/"
            pattern = rf'href="\.\./({re.escape(package)}/?[^"]*)"'
            replacement = r'href="/\1"'
            html = re.sub(pattern, replacement, html)

            # Transform relative package links
            pattern = rf'href="({re.escape(package)}/?[^"]*)"'
            replacement = r'href="/\1"'
            html = re.sub(pattern, replacement, html)

        # Fix nested paths in HTML
        html_mappings: dict[str, str] = {
            'href="/pyvider-framework/pyvider/': 'href="/pyvider/',
            'href="/pyvider-framework/pyvider-cty/': 'href="/pyvider-cty/',
            'href="/pyvider-framework/pyvider-hcl/': 'href="/pyvider-hcl/',
            'href="/pyvider-framework/pyvider-rpcplugin/': 'href="/pyvider-rpcplugin/',
            'href="/pyvider-framework/pyvider-components/': 'href="/pyvider-components/',
            'href="/pyvider-framework/tofusoup/': 'href="/tofusoup/',
            ('href="/pyvider-framework/terraform-provider-pyvider/'): 'href="/terraform-provider-pyvider/',
            'href="/foundation/foundation/': 'href="/provide-foundation/',
            'href="/foundation/testkit/': 'href="/provide-testkit/',
            'href="/development-tools/flavorpack/': 'href="/flavorpack/',
            'href="/development-tools/wrknv/': 'href="/wrknv/',
            'href="/development-tools/supsrc/': 'href="/supsrc/',
            'href="/development-tools/plating/': 'href="/plating/',
        }

        for old_href, new_href in html_mappings.items():
            html = html.replace(old_href, new_href)

        return html


# For hook-style usage (alternative to plugin)
def on_page_markdown(markdown: str, page: Page, config: MkDocsConfig, files: Files) -> str:
    """Hook function for transforming markdown links."""
    plugin = CrossRepoLinksPlugin()
    plugin.config = {"enabled": True, "verbose": False}
    return plugin.on_page_markdown(markdown, page, config, files)


def on_page_content(html: str, page: Page, config: MkDocsConfig, files: Files) -> str:
    """Hook function for transforming HTML content."""
    plugin = CrossRepoLinksPlugin()
    plugin.config = {"enabled": True, "verbose": False}
    return plugin.on_page_content(html, page, config, files)
