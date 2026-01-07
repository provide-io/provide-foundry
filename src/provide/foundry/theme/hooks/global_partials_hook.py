"""
MkDocs hook to inject global header and footer into all pages.

This hook:
1. Reads _global_header.md and _global_footer.md from the partials directory
2. Injects header after the first heading on every page
3. Appends footer at the end of every page
4. Respects frontmatter opt-out flags (skip_global_header, skip_global_footer)
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

# Cache for partial contents
_header_content: str | None = None
_footer_content: str | None = None


def _find_partials_dir(config: dict[str, Any]) -> Path | None:
    """Find the partials directory, checking project overrides first, then foundry defaults.

    NOTE: When mkdocs-monorepo is used, docs_dir points to a temp directory.
    We must use config_file_path to find the actual project root.
    """
    # Get actual project root from config file path (not docs_dir which may be temp)
    config_file = config.get("config_file_path")
    if config_file:
        project_root = Path(config_file).parent
    else:
        # Fallback for non-monorepo builds
        docs_dir = Path(config.get("docs_dir", "docs"))
        project_root = docs_dir.parent

    # Check project-specific overrides first
    project_partials = project_root / "docs" / "_partials"
    if project_partials.exists():
        return project_partials

    # Special case for provide-foundry source tree (canonical source)
    # Check this BEFORE .provide/ since source is authoritative for provide-foundry
    src_foundry_partials = project_root / "src" / "provide" / "foundry" / "docs" / "_partials"
    if src_foundry_partials.exists():
        return src_foundry_partials

    # Fall back to foundry defaults (extracted via we run docs.setup)
    foundry_partials = project_root / ".provide" / "foundry" / "docs" / "_partials"
    if foundry_partials.exists():
        return foundry_partials

    return None


def _load_partials(config: dict[str, Any]) -> tuple[str, str]:
    """Load global header and footer content."""
    global _header_content, _footer_content

    if _header_content is not None and _footer_content is not None:
        return _header_content, _footer_content

    partials_dir = _find_partials_dir(config)
    if partials_dir is None:
        _header_content = ""
        _footer_content = ""
        return _header_content, _footer_content

    header_file = partials_dir / "_global_header.md"
    footer_file = partials_dir / "_global_footer.md"

    _header_content = header_file.read_text(encoding="utf-8").strip() if header_file.exists() else ""
    _footer_content = footer_file.read_text(encoding="utf-8").strip() if footer_file.exists() else ""

    return _header_content, _footer_content


def on_page_markdown(
    markdown: str,
    page: Any,
    config: dict[str, Any],
    files: Any,
) -> str:
    """
    Hook called for each page's markdown content before rendering.

    Injects global header after first heading and footer at end.
    """
    header_content, footer_content = _load_partials(config)

    # Check frontmatter for opt-out flags
    meta = getattr(page, "meta", {}) or {}
    skip_header = meta.get("skip_global_header", False)
    skip_footer = meta.get("skip_global_footer", False)

    # Skip if already has header/footer injected (idempotency)
    has_header = "AI-Generated Content" in markdown or "<!-- global-header -->" in markdown
    has_footer = "<!-- global-footer -->" in markdown

    # Inject header after first heading if not skipped and not already present
    if header_content and not skip_header and not has_header:
        # Find first heading (# Title)
        heading_match = re.search(r"^# .+$", markdown, re.MULTILINE)
        header_block = f"<!-- global-header -->\n{header_content}\n<!-- /global-header -->\n\n"
        if heading_match:
            insert_pos = heading_match.end()
            # Skip past any immediate content blocks after the heading
            # This includes: empty lines, admonitions (!!!), and description text
            remaining = markdown[insert_pos:]
            lines = remaining.split("\n")
            i = 0
            while i < len(lines):
                line = lines[i]
                stripped = line.strip()

                # Skip empty lines
                if not stripped:
                    i += 1
                    continue

                # Check for admonition block (!!!)
                if stripped.startswith("!!!"):
                    # Skip the admonition header line
                    i += 1
                    # Skip all subsequent indented lines (admonition content)
                    while i < len(lines):
                        next_line = lines[i]
                        # Admonition content is indented (starts with spaces/tabs)
                        # or is an empty line within the block
                        if next_line.startswith("    ") or next_line.startswith("\t") or not next_line.strip():
                            # Check if empty line is followed by non-indented content
                            if not next_line.strip():
                                # Look ahead to see if next non-empty line is still indented
                                lookahead = i + 1
                                while lookahead < len(lines) and not lines[lookahead].strip():
                                    lookahead += 1
                                if lookahead < len(lines) and (
                                    lines[lookahead].startswith("    ") or lines[lookahead].startswith("\t")
                                ):
                                    i += 1
                                    continue
                                else:
                                    # End of admonition block
                                    break
                            i += 1
                        else:
                            # Non-indented line - end of admonition
                            break
                    continue

                # Check for heading (stop here, insert before it)
                if stripped.startswith("#"):
                    break

                # Found a description line - skip it and insert after
                i += 1
                break

            # Calculate insert position based on lines consumed
            insert_pos += len("\n".join(lines[:i])) + (1 if i > 0 else 0)

            header_block = f"\n\n<!-- global-header -->\n{header_content}\n<!-- /global-header -->\n"
            markdown = markdown[:insert_pos] + header_block + markdown[insert_pos:]
        else:
            # No heading found (e.g., auto-generated API reference pages)
            # Prepend header at the very beginning
            markdown = header_block + markdown

    # Append footer if not skipped and not already present
    if footer_content and not skip_footer and not has_footer:
        footer_block = f"\n\n<!-- global-footer -->\n{footer_content}\n<!-- /global-footer -->"
        markdown = markdown.rstrip() + footer_block

    return markdown
