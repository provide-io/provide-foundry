# Contributing to Documentation

This guide explains how to contribute to the provide.io ecosystem documentation.

## Documentation Architecture

The provide.io documentation uses a **monorepo aggregation** approach:

- **`provide-foundry/docs/`** - Hub documentation and shared resources
- **Individual project docs** - Each project maintains its own `docs/` directory
- **MkDocs Monorepo Plugin** - Automatically aggregates all documentation into a unified site

## Shared Partials System

To reduce duplication and maintain consistency, we use **shared documentation partials** for common content.

### Available Partials

Packaged with provide-foundry and extracted to `.provide/foundry/docs/_partials/`:

| Partial | Purpose | Use When |
|---------|---------|----------|
| `python-requirements.md` | Python 3.11+ requirements | Documenting Python version requirements |
| `uv-installation.md` | UV package manager installation | Installing UV across platforms |
| `python-version-setup.md` | Python version management with UV | Setting up Python versions |
| `virtual-env-setup.md` | Virtual environment creation/activation | Virtual environment setup |
| `platform-specific-macos.md` | macOS-specific setup notes | macOS platform-specific content |
| `troubleshooting-common.md` | Common troubleshooting issues | General troubleshooting sections |

### Using Partials

Include a partial using the `--8<--` syntax from `pymdownx.snippets`:

```markdown
## Python Requirements

--8<-- ".provide/foundry/docs/_partials/python-requirements.md"
```

**Important**: The path starts with `.provide/foundry/` which is where the files are extracted when you run `make docs-setup` or when provide-foundry is installed.

### When to Use Partials

✅ **DO use partials for:**
- Installation instructions (UV, Python version setup)
- Virtual environment setup
- Platform-specific notes (macOS, Linux, Windows)
- Common troubleshooting steps

❌ **DON'T use partials for:**
- Project-specific content
- API documentation
- Examples and tutorials
- Feature-specific guides

### Creating New Partials

Before creating a new partial, ask:

1. **Is this content truly duplicated across 3+ projects?**
2. **Will this content remain stable?**
3. **Is this generic enough to be shared?**

If yes to all three, create a new partial:

```bash
# Create the partial in the package source
cat > provide-foundry/src/provide/foundry/docs/_partials/my-new-partial.md << 'EOF'
### My Section

Content here...
EOF

# Update the partials README
# Add to provide-foundry/src/provide/foundry/docs/_partials/README.md

# The partial will be packaged and extracted to .provide/foundry/docs/_partials/
# when other projects run make docs-setup
```

## Documentation Standards

### Tooling Recommendations

**✅ Always Recommend:**
- **UV** for package management and Python version management
- **`uv python install`** instead of pyenv
- **`uv sync`** for dependency installation
- **`uv add`** for adding packages

**❌ Never Recommend:**
- ~~pyenv~~ (use `uv python install` instead)
- ~~virtualenv~~ (use `uv venv` or `python -m venv`)
- ~~pip~~ as the primary tool (UV is preferred, pip as fallback only)

### Markdown Style

- Use **ATX-style headers** (`##` not underlines)
- **Code blocks** must specify language (` ```bash ` not ` ``` `)
- **Use admonitions** for tips, warnings, notes:
  ```markdown
  !!! tip "Python Version"
      Content here
  ```
- **Use tabs** for platform-specific content:
  ```markdown
  === "macOS"
      macOS content

  === "Linux"
      Linux content
  ```

### File Organization

Follow this structure for project documentation:

```
docs/
├── index.md                    # Project homepage
├── getting-started/
│   ├── installation.md        # How to install
│   ├── quick-start.md         # 5-minute tutorial
│   └── first-app.md           # Detailed first project
├── guides/                     # How-to guides
├── tutorials/                  # Step-by-step tutorials
├── api/                        # API reference
└── reference/                  # Technical reference
```

## Building Documentation Locally

### Build Single Project

```bash
# Navigate to project directory
cd provide-foundation

# Serve docs with live reload
mkdocs serve

# Build static site
mkdocs build
```

### Build Unified Documentation

```bash
# Navigate to provide-foundry
cd provide-foundry

# Serve complete ecosystem docs
mkdocs serve

# Build complete site
mkdocs build
```

**Note**: The unified build aggregates all project documentation and may take 30-60 seconds.

## MkDocs Configuration

### Base Configuration

All projects inherit from `.provide/foundry/base-mkdocs.yml`:

- Material theme
- Plugins: search, snippets, mkdocstrings
- Markdown extensions
- Shared styling

### Project-Specific Configuration

Each project's `mkdocs.yml` should:

```yaml
# Inherit shared configuration
INHERIT: .provide/foundry/base-mkdocs.yml

# Project-specific settings
site_name: My Project
site_description: Project description
site_url: https://foundry.provide.io/my-project/
```

### Enabling Snippets

The `pymdownx.snippets` extension is already configured in the base config:

```yaml
markdown_extensions:
  - pymdownx.snippets:
      check_paths: true
      base_path: docs
```

No additional configuration needed!

## Testing Documentation

Before submitting documentation changes:

1. **Build locally** to verify syntax:
   ```bash
   mkdocs build --strict
   ```

2. **Check for broken links**:
   ```bash
   # Install link checker
   uv add mkdocs-linkcheck

   # Run check
   mkdocs build --strict --verbose
   ```

3. **Review rendered output**:
   ```bash
   mkdocs serve
   # Open http://127.0.0.1:8000
   ```

## Common Documentation Tasks

### Adding a New Page

1. Create the Markdown file in the appropriate directory
2. Update `mkdocs.yml` navigation:
   ```yaml
   nav:
     - Getting Started:
       - getting-started/installation.md
       - getting-started/quick-start.md
       - getting-started/my-new-page.md  # Add here
   ```

### Updating Partials

When updating a partial:

1. **Test impact** - The partial affects multiple pages
2. **Build all projects** - Verify changes work everywhere
3. **Update partial README** if adding/removing partials

### Cross-Referencing

Link to other docs using relative paths:

```markdown
<!-- Link within same project -->
See [Quick Start](../getting-started/quick-start/)

<!-- Link to another project (in monorepo) -->
See [Foundation Guide](../provide-foundation/getting-started/installation/)
```

## Commit Guidelines

Documentation commits should:

- **Be focused** - One logical change per commit
- **Include context** - Explain why, not just what
- **Test first** - Verify builds succeed before committing

Good commit messages:

```
docs: add shared partial for UV installation

- Created uv-installation.md partial for reuse
- Replaced duplicate UV install instructions in 3 files
- Reduces duplication by ~100 lines

docs: fix broken link in provide-foundation guide

- Corrected reference to quick-start.md
- Added mkdocs strict mode to catch these earlier
```

## Getting Help

- **Documentation Issues**: [GitHub Issues](https://github.com/provide-io/provide-io/issues)
- **Questions**: [GitHub Discussions](https://github.com/provide-io/provide-io/discussions)
- **Style Questions**: Check existing docs for examples

## Additional Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/)
- [MkDocs Monorepo Plugin](https://github.com/spotify/mkdocs-monorepo-plugin)
