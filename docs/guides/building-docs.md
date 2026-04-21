# Building Documentation - Complete Guide

## Quick Start (30 seconds)

```bash
we run docs.serve
```

Open: http://127.0.0.1:11000 (for provide-foundry)

That's it! The first run will automatically:
- Extract theme and configuration
- Install dependencies
- Start the development server

## Available Commands

```bash
# Development
we run docs.serve     # Serve with live reload
we run docs.build     # Build static site
we run docs.clean     # Clean artifacts

# Validation
python scripts/docs_validate.py verify-config      # Validate mkdocs.yml files
python scripts/validate_partials.py                # Validate partial references
python scripts/validate_standardization.py         # Check standardization

# Maintenance
we run docs.setup     # Re-extract theme/config (rarely needed)
```

## Port Registry

Each project uses a unique port to avoid conflicts when running multiple documentation servers simultaneously. Ports are organized by project layer:

### Foundation Layer (11001-11003)
- **11001** - provide-foundation
- **11002** - provide-testkit
- **11003** - provide-workspace

### Pyvider Framework (11010-11014)
- **11010** - pyvider
- **11011** - pyvider-cty
- **11012** - pyvider-hcl
- **11013** - pyvider-rpcplugin
- **11014** - pyvider-components

### Tools Layer (11020-11027)
- **11020** - ci-tooling
- **11021** - flavorpack
- **11022** - plating
- **11023** - wrknv
- **11024** - supsrc
- **11025** - tofusoup
- **11026** - messometer
- **11027** - bfiles

### Terraform Providers (11030-11031)
- **11030** - terraform-provider-pyvider
- **11031** - terraform-provider-tofusoup

### Documentation Hub (11000)
- **11000** - provide-foundry (monorepo aggregator)

## First-Time Setup

Normally automatic, but if needed manually:

```bash
# Install dependencies
uv sync

# Extract documentation assets
we run docs.setup
```

## Troubleshooting

### Build fails with "cannot find base-mkdocs.yml"
**Fix:** `we run docs.setup`

**Explanation:** Documentation theme and configuration need to be extracted from the `provide-foundry` package to `.provide/foundry/` before building.

### Port already in use
**Fix:** Each project has a unique port (see Port Registry above). If you see a port conflict, check what's running on that port:

```bash
lsof -ti:11000  # Replace 11000 with your project's port
```

Kill the process if needed:
```bash
lsof -ti:11000 | xargs kill
```

### Link checker shows many "errors"
**Expected behavior:** When running `lychee` in offline mode, you may see warnings about:
- Extensionless links (e.g., `docs/guides` instead of `docs/guides.md`)
- Monorepo package directories (created at build time)
- Anchor links in markdown files

These are **not real errors** - MkDocs handles these correctly when building. The `.lychee.toml` config filters most false positives.

For accurate link validation, run after building:
```bash
mkdocs build
lychee site/
```

### Still having issues?
Run diagnostics:
```bash
python scripts/validate_standardization.py
```

## Architecture

All projects inherit from shared base configuration:
- **Base config:** `.provide/foundry/base-mkdocs.yml`
- **Theme:** `.provide/foundry/theme/` (CSS, JS, custom Material theme)
- **Shared partials:** `.provide/foundry/docs/_partials/` (reusable documentation snippets)
- **API generator:** `.provide/foundry/gen_ref_pages.py`

When you run `we run docs.setup`, these are extracted from the `provide-foundry` package.

### How Documentation Builds Work

1. **Extraction** (`we run docs.setup`):
   - Copies theme assets from installed `provide-foundry` package
   - Creates `.provide/foundry/` directory structure
   - Extracts base configuration, partials, and scripts

2. **Configuration Inheritance**:
   - Each project's `mkdocs.yml` starts with: `INHERIT: .provide/foundry/base-mkdocs.yml`
   - Projects override only: site_name, site_url, repo_url, dev_addr, navigation
   - All theme, plugins, and markdown extensions come from base config

3. **Building** (`we run docs.build`):
   - MkDocs loads base config + project overrides
   - Processes markdown with extensions (code highlighting, admonitions, etc.)
   - Generates API docs using mkdocstrings
   - Applies theme and custom CSS/JS
   - Outputs static HTML to `site/`

4. **Serving** (`we run docs.serve`):
   - Starts development server on project's assigned port
   - Watches files for changes and auto-rebuilds
   - Provides live reload in browser

### Monorepo Documentation (provide-foundry only)

The `provide-foundry` project aggregates documentation from all 18 projects using the `mkdocs-monorepo-plugin`:

```yaml
nav:
  - Home: index.md
  - '!include ./pyvider/mkdocs.yml'
  - '!include ./flavorpack/mkdocs.yml'
  # ... all projects included
```

This creates one unified documentation site at http://127.0.0.1:11000 with:
- Cross-project search
- Unified navigation
- Consistent theme across all projects
- API docs from all packages

## Advanced Usage

See [Link Checking Reference](../link-checking.md) for understanding lychee and link validation.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `we run docs.serve` | Start dev server with live reload |
| `we run docs.build` | Build static HTML site |
| `we run docs.clean` | Remove build artifacts |
| `we run docs.setup` | Extract theme/config (rarely needed) |
| `python scripts/docs_validate.py verify-config` | Validate configurations |
| `python scripts/validate_standardization.py` | Check project compliance |

## Need Help?

1. Check this guide first
2. Run `python scripts/validate_standardization.py` to diagnose issues
3. Ask in #documentation channel
