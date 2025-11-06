# Documentation Partials

This directory contains reusable documentation snippets that are shared across the provide.io ecosystem.

## Usage

Use the `--8<--` syntax from `pymdownx.snippets` to include partials in your documentation:

```markdown
--8<-- "provide-foundry/docs/_partials/python-requirements.md"
```

## Available Partials

- **python-requirements.md** - Python version requirements
- **uv-installation.md** - Installing the UV package manager
- **python-version-setup.md** - Setting up Python versions with uv
- **virtual-env-setup.md** - Creating and activating virtual environments
- **platform-specific-macos.md** - macOS-specific setup notes
- **troubleshooting-common.md** - Common troubleshooting issues

## Guidelines

- Keep partials focused and single-purpose
- Use clear, descriptive filenames
- Include only content that is truly shared across multiple projects
- Project-specific content belongs in the project's own docs
