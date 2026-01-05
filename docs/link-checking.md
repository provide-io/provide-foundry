# Link Checking

The provide-foundry documentation uses a two-layer link validation approach to ensure all links are valid and working.

## Overview

We use two complementary tools for comprehensive link checking:

1. **lychee** - Fast, Rust-based link checker for local development and CI
2. **mkdocs-htmlproofer-plugin** - MkDocs plugin that validates links during build

## Local Link Checking

### Prerequisites

Install lychee:

```bash
# macOS
brew install lychee

# Linux (Arch)
sudo pacman -S lychee

# Using Cargo
cargo install lychee

# Docker
docker pull lycheeverse/lychee

# Other platforms: https://github.com/lycheeverse/lychee#installation
```

### Quick Start

```bash
# Check internal links only (fast - recommended for local development)
we run docs.links.check
# or: make links-check (legacy Makefile projects)

# Check all links including external URLs (slow)
we run docs.links.external
# or: make links-check-external (legacy)

# Show available tasks
we tasks
```

### Understanding Results

- ✅ **Success**: All links are valid
- ❌ **Error**: Broken links found (details shown in output)
- ⚠️ **Warning**: Redirects or unusual status codes

### Performance

**Local offline checking** (`we run docs.links.check`):
- Execution time: <1 second
- Checks only internal documentation links
- No network requests made

**External link checking** (`we run docs.links.external`):
- Execution time: ~1-5 seconds (depending on network and link count)
- Validates all external URLs with HTTP requests
- Respects rate limiting (429 responses accepted)

### Expected "Errors" (Not Actually Broken)

When running `we run docs.links.check`, you may see ~206 errors for:

1. **Extensionless link references** (e.g., `docs/guides/installation` instead of `docs/guides/installation.md`)
   - MkDocs allows links without `.md` extensions when `use_directory_urls: true`
   - During build, MkDocs converts these to proper HTML paths
   - Lychee checks raw filesystem and expects exact file paths
   - **These work correctly on the live site!**

2. **Monorepo package directories** (e.g., `docs/pyvider`, `docs/flavorpack`)
   - These directories only exist after `we run docs.build` runs
   - The mkdocs-monorepo plugin creates them during the build
   - They will be validated by mkdocs-htmlproofer-plugin

**Example output showing expected errors**:
```
[ERROR] file:///Users/.../docs/guides/installation | Cannot find file
[ERROR] file:///Users/.../docs/packages/pyvider | Cannot find file
```

**Bottom line**: If you see ~206 errors but the files exist with `.md` extensions, your documentation is correct! These errors are expected and don't affect the rendered site.

**Production validation**: The live site (https://foundry.provide.io) achieves 99.2% link success rate (911 OK / 918 total).

## MkDocs HTML Proofer

The `mkdocs-htmlproofer-plugin` can validate links during the documentation build process.

**Note**: This plugin is **disabled by default** for faster local builds. Enable it for comprehensive validation.

### What it Validates

When enabled, the plugin checks:
- Internal links between documentation pages
- Anchor links (#fragments)
- Template rendering
- Post-build HTML structure

### Configuration

The plugin is configured in `mkdocs.yml`:

```yaml
plugins:
  - htmlproofer:
      enabled: !ENV [HTMLPROOFER_ENABLED, false]  # Disabled by default
      raise_error: false
      validate_external_urls: !ENV [HTMLPROOFER_VALIDATE_EXTERNAL, false]
```

### Environment Variables

- `HTMLPROOFER_ENABLED`: Enable/disable the plugin (default: `false`)
- `HTMLPROOFER_VALIDATE_EXTERNAL`: Check external URLs (default: `false`, very slow)

### Enable for CI or Thorough Validation

```bash
# Enable HTML proofer for comprehensive validation
export HTMLPROOFER_ENABLED=true
we run docs.build
```

## Continuous Integration

Link checking runs automatically in GitHub Actions:

- **Daily**: Full link check at 2 AM UTC
- **On PR**: When documentation files are modified
- **Manual**: Via workflow dispatch

### Workflow Location

`.github/workflows/links.yml`

### What It Checks

- All Markdown files (`**/*.md`)
- All HTML files (`**/*.html`)
- Both internal and external links
- Anchor fragments

### Handling Failures

When broken links are detected:

1. GitHub Action creates an issue automatically
2. Check the workflow logs for specific broken links
3. Fix the links in your local branch
4. Re-run the workflow to verify

## Configuration Files

### `.lychee.toml`

Main configuration for lychee link checker:

- **Concurrency**: 64 parallel requests
- **Timeout**: 30 seconds per request
- **Retries**: Up to 3 attempts
- **Exclusions**: Localhost, development URLs, known false positives

Key settings:

```toml
max_concurrency = 64
max_retries = 3
timeout = 30
exclude_mail = true  # Don't check mailto: links
accept = [200, 204, 301, 302, 307, 308, 429]
```

### Excluded URLs

The configuration excludes:

- Localhost/development URLs (127.0.0.1, localhost)
- Internal MkDocs server addresses
- Social media profile URLs requiring authentication
- Google Analytics URLs

To add exclusions, edit `.lychee.toml`:

```toml
exclude = [
    "https://example.com/broken/*",
    "http://localhost*",
]
```

## Common Issues

### False Positives

Some sites block automated checkers or require authentication:

**Solution**: Add to `.lychee.toml` exclusions:

```toml
exclude = [
    "https://problematic-site.com/*",
]
```

### Rate Limiting (429)

External sites may rate-limit requests:

**Solution**: We accept 429 status codes by default. For persistent issues, add to exclusions.

### Slow External Checks

External link validation can be slow:

**Solution**:
- Use `we run docs.links.check` (internal only) for local development
- External checks run in CI automatically
- Disable with `HTMLPROOFER_VALIDATE_EXTERNAL=false`

### Anchor Links Failing

Anchor validation may fail for dynamically generated content:

**Solution**: The `mkdocs-htmlproofer-plugin` validates anchors in rendered HTML, catching these issues.

## Best Practices

1. **Local Development**: Use `we run docs.links.check` (fast, internal only)
2. **Before Committing**: Run `we run docs.links.check` to catch broken internal links
3. **CI Validation**: Let GitHub Actions handle comprehensive external link checking
4. **Document Changes**: Update `.lychee.toml` exclusions with comments explaining why

## Performance

- **Internal links only** (~10-30 seconds for full monorepo)
- **External links** (~2-5 minutes depending on network)
- **CI execution** (~1-2 minutes with parallel processing)

## Troubleshooting

### Lychee Not Found

```bash
❌ lychee not found. Install with: brew install lychee
```

**Solution**: Install lychee using the instructions in [Prerequisites](#prerequisites)

### Permission Denied

```bash
Permission denied: .lychee.toml
```

**Solution**: Check file permissions:

```bash
chmod 644 .lychee.toml
```

### Too Many Open Files

```bash
Error: Too many open files
```

**Solution**: Reduce concurrency in `.lychee.toml`:

```toml
max_concurrency = 32  # Reduced from 64
```

## Additional Resources

- [lychee Documentation](https://lychee.cli.rs/)
- [mkdocs-htmlproofer-plugin](https://github.com/manuzhang/mkdocs-htmlproofer-plugin)
- [GitHub Actions Workflow](.github/workflows/links.yml)
