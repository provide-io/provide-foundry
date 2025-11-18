# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Setup

This is the documentation hub for the provide.io ecosystem. For development:

```bash
# Install documentation dependencies
uv sync

# Serve docs locally for development
make docs-serve

# Build complete documentation
make docs-build

# Clean documentation artifacts
make docs-clean
```

## Environment Management

The ecosystem uses `uv` for package management and `env.sh` scripts for environment setup. Always use:
- `uv sync --extra all --extra dev` in parent directory for full ecosystem setup
- Individual project `env.sh` scripts for isolated development
- Workenv directories (not `.venv`) for virtual environments

## Architecture Overview

The provide.io ecosystem is a multi-package Python workspace with three layers:

### Foundation Layer
- **provide-foundation**: Core telemetry, logging, and infrastructure utilities
- **provide-testkit**: Unified testing framework with fixtures and utilities

### Framework Layer
- **pyvider**: Core Terraform provider framework in Python
- **pyvider-cty**: CTY type system bindings for Terraform data types
- **pyvider-hcl**: HCL parsing and manipulation
- **pyvider-rpcplugin**: gRPC plugin protocol implementation
- **pyvider-components**: Standard reusable provider components

### Tools Layer
- **flavorpack**: PSPF/2025 packaging system for secure executable bundles
- **wrknv**: Work environment management and toolchain automation
- **plating**: Documentation and code generation templates
- **tofusoup**: Cross-language conformance testing framework
- **supsrc**: Automated Git workflow and commit management

## Documentation System

This repository aggregates documentation from all ecosystem packages using:
- **mkdocs-monorepo plugin** - Automatic aggregation via `!include` directives
- **MkDocs Material** - Rendering unified documentation site
- **Shared base configuration** - All projects inherit from `base-mkdocs.yml`
- Individual packages maintain their own `docs/` directories

## Key Commands

### Documentation Commands
```bash
make docs-serve     # Development server with auto-reload
make docs-build     # Production build
make docs-validate  # Validate links and structure
```

### Maintenance Commands
```bash
make dev-status     # Check which projects are available
make dev-update     # Pull latest from all projects
make cache-clean-all # Clean all caches (UV, Python, etc.)
make clean-deep     # Deep clean with confirmation
```

### Testing Commands
```bash
make test-build     # Test documentation build
make test-projects  # Test individual project builds
```

## Code Standards

- **Python 3.11+** required across ecosystem
- **Modern typing**: Use `str | None`, not `Optional[str]`
- **Code modernization**: No backward compatibility or migration logic
- **Constants pattern**: No inline defaults - use `constants.py` or `defaults.py`
- **Future annotations**: `from __future__ import annotations` encouraged

## Project Relationships

Projects are interconnected:
- Foundation packages provide core infrastructure to all others
- Pyvider packages depend on Foundation layer
- Tools can depend on both Foundation and Framework layers
- All packages use unified workspace configuration in parent `pyproject.toml`

When making changes that affect multiple packages, test the entire ecosystem build with `uv sync --extra all --extra dev` in the parent directory.
- do not use pkill when kill mkdocs