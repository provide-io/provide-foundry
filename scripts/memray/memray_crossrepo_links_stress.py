#!/usr/bin/env python3
"""Memray stress test for CrossRepoLinksPlugin regex hot paths.

Exercises the regex-heavy link transformation pipeline that runs on every
documentation page during mkdocs builds: temp-path fixing, .md stripping,
package link transforms, and nested path resolution.
"""
import os

os.environ.setdefault("LOG_LEVEL", "ERROR")

CYCLES = 200
PAGES_PER_CYCLE = 20


def _build_sample_markdown(page_idx: int) -> str:
    """Generate realistic markdown with cross-repo links and temp paths."""
    lines = [
        f"# Page {page_idx} — Cross-Repo Integration Guide\n",
        "Some introductory text with inline code `example`.\n",
        # Relative package links (should be transformed)
        "[Foundation docs](../provide-foundation/getting-started.md)",
        "[Pyvider API](../pyvider/api/reference.md#section)",
        "[wrknv tasks](../wrknv/tasks.md)",
        "[Flavorpack](../flavorpack/usage.md)",
        "[TofuSoup](../tofusoup/overview.md)",
        "[Plating guide](../plating/guide.md)",
        # Nested paths (should be flattened)
        "[Nested pyvider](/pyvider-framework/pyvider/docs/index.md)",
        "[Nested cty](/pyvider-framework/pyvider-cty/types.md)",
        "[Nested foundation](/foundation/foundation/core.md)",
        "[Nested wrknv](/development-tools/wrknv/cli.md)",
        # External links (should be preserved)
        "[GitHub](https://github.com/provide-io/provide-foundry)",
        "[PyPI](https://pypi.org/project/provide-foundry/)",
        # .md extension links (should be stripped)
        "[Local page](./sibling-page.md)",
        "[Deep link](../../other/page.md#anchor)",
        # Plain text paragraphs to add bulk
        "\n## Section Two\n",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 5,
        "\n## Section Three\n",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " * 5,
    ]
    return "\n".join(lines)


def main() -> None:
    from provide.foundry.mkdocs_plugins.crossrepo_links import CrossRepoLinksPlugin

    plugin = CrossRepoLinksPlugin()
    plugin.config = {"enabled": True, "verbose": False}

    # Build sample pages once
    pages = [_build_sample_markdown(i) for i in range(PAGES_PER_CYCLE)]

    # Warmup — single pass
    for md in pages[:2]:
        plugin._transform_package_links(md)
        plugin._fix_nested_paths(md)
        plugin._strip_md_extensions(md)

    # Stress: run the full transform pipeline
    total_transforms = 0
    for _cycle in range(CYCLES):
        for md in pages:
            md, c1 = plugin._strip_md_extensions(md)
            md, c2 = plugin._transform_package_links(md)
            md, c3 = plugin._fix_nested_paths(md)
            total_transforms += c1 + c2 + c3

    total_pages = CYCLES * PAGES_PER_CYCLE
    print(f"crossrepo_links stress complete: {CYCLES} cycles, {total_pages} pages, {total_transforms} transforms")


if __name__ == "__main__":
    main()
