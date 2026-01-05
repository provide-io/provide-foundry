# Provide.io Ecosystem Documentation

Welcome to the comprehensive documentation hub for the provide.io ecosystem - a collection of Python tools and frameworks for building Terraform providers, packaging applications, and managing development workflows.

## Key Features
Key features are highlighted in the sections below and in the documentation.

## 🚀 Quick Start

```bash
# Set up the entire ecosystem
cd /path/to/provide-workspace
uv sync --all-groups
source .venv/bin/activate
```

## 📚 Documentation

The documentation is built with MkDocs Material and covers:

- **Getting Started**: Installation and first steps
- **Ecosystem**: Architecture and design principles
- **Packages**: Individual package documentation
- **Guides**: Cross-package integration guides
- **API Reference**: Complete API documentation

## Development
- See [CLAUDE.md](https://github.com/provide-io/provide-foundry/blob/main/CLAUDE.md) for local development notes.
- Run `mkdocs serve` in this repo for a live docs preview.

## 🤝 Contributing

See [CONTRIBUTING.md](https://github.com/provide-io/provide-foundry/blob/main/CONTRIBUTING.md) for ecosystem-wide contribution guidelines.

## 📄 License

All packages in the provide.io ecosystem are licensed under Apache-2.0 unless otherwise specified.

## 🛠 Building Documentation

The documentation system uses a modern, DRY approach with shared configuration:

### Architecture Overview

- **Shared Base Configuration** (`base-mkdocs.yml`) - Common theme, plugins, and extensions
- **Centralized Theme** (`src/provide/foundry/theme/`) - Namespace package with CSS, JavaScript, and assets
  - Install: `uv pip install -e .` for editable development
- **Monorepo Plugin** - Automatic aggregation of all project documentation
- **Auto-Generated API Docs** - Build-time generation using mkdocs-gen-files
- **Canonical Makefile** (`Makefile.provider.tmpl`) - Standardized provider Makefile template

### Building the Documentation

```bash
# Install dependencies
cd provide-foundry
uv sync

# Serve documentation locally (all projects)
we run docs.serve
# or: uv run mkdocs serve

# Build complete documentation site
we run docs.build
# or: uv run mkdocs build --clean

# Validate documentation (strict mode)
uv run mkdocs build --strict

# Clean documentation artifacts
we run docs.clean

# Check links (fast, internal only)
we run docs.links.check

# Check all links including external
we run docs.links.external
```

### Building Individual Project Documentation

Each project can build documentation independently:

```bash
# Navigate to any project
cd ../pyvider

# Use wrknv tasks
we run docs.build       # Build documentation
we run docs.serve       # Serve locally
we run docs.clean       # Clean artifacts
we run docs.links.check # Check links

# Or use mkdocs directly
uv run mkdocs build
uv run mkdocs serve
```

### Documentation Structure

```
provide-foundry/                    # Documentation hub
├── base-mkdocs.yml                # Shared configuration (inherited by all projects)
├── mkdocs.yml                     # Documentation site configuration
├── Makefile.provider.tmpl         # Canonical provider Makefile template
├── scripts/
│   └── gen_ref_pages.py          # Shared API doc generator
├── src/provide/foundry/           # Namespace package
│   ├── __init__.py
│   ├── py.typed
│   ├── docs/
│   │   ├── __init__.py
│   │   └── gen_ref_pages.py      # API documentation generator
│   └── theme/                     # Centralized theme assets
│       ├── __init__.py
│   ├── stylesheets/
│   ├── javascripts/
│   └── data/
└── docs/                          # Hub-specific documentation

Individual Projects:
provide-foundation/
├── mkdocs.yml                     # Inherits from base-mkdocs.yml
├── Makefile                       # Standard project Makefile
└── docs/                          # Project-specific docs
    ├── index.md
    ├── guides/
    └── reference/                 # Auto-generated at build time
```

## 📦 Ecosystem Packages

### Foundation Layer
- **[provide-foundation](https://github.com/provide-io/provide-foundation)** - Core telemetry and logging infrastructure
- **[provide-testkit](https://github.com/provide-io/provide-testkit)** - Testing utilities and fixtures

### Pyvider Framework
- **[pyvider](https://github.com/provide-io/pyvider)** - Core Terraform provider framework
- **[pyvider-cty](https://github.com/provide-io/pyvider-cty)** - CTY type system implementation
- **[pyvider-hcl](https://github.com/provide-io/pyvider-hcl)** - HCL parsing with CTY integration
- **[pyvider-rpcplugin](https://github.com/provide-io/pyvider-rpcplugin)** - gRPC plugin protocol implementation
- **[pyvider-components](https://github.com/provide-io/pyvider-components)** - Standard components library
- **[terraform-provider-pyvider](https://github.com/provide-io/terraform-provider-pyvider)** - Official Pyvider provider

### Tools & Utilities
- **[flavorpack](https://github.com/provide-io/flavorpack)** - PSPF packaging system for executable bundles
- **[wrknv](https://github.com/provide-io/wrknv)** - Work environment management
- **[plating](https://github.com/provide-io/plating)** - Documentation generation for providers
- **[tofusoup](https://github.com/provide-io/tofusoup)** - Cross-language conformance testing
- **[supsrc](https://github.com/provide-io/supsrc)** - Automated Git commit/push utility

## 🏗 Architecture

The provide.io ecosystem follows a layered architecture:

```
┌─────────────────────────────────────────────────────┐
│                    Tools Layer                      │
│  flavorpack │ wrknv │ plating │ tofusoup │ supsrc  │
├─────────────────────────────────────────────────────┤
│                  Framework Layer                    │
│  pyvider │ pyvider-cty │ pyvider-hcl │ pyvider-*   │
├─────────────────────────────────────────────────────┤
│                 Foundation Layer                    │
│       provide-foundation │ provide-testkit         │
└─────────────────────────────────────────────────────┘
```

## 📝 Adding Documentation to Projects

### For New Projects

1. **Create mkdocs.yml** inheriting from base configuration:

   ```yaml
   # Inherit shared configuration from provide-foundry
   INHERIT: ../provide-foundry/base-mkdocs.yml

   # Project-Specific Configuration
   site_name: Your Project Documentation
   site_url: https://foundry.provide.io/your-project/
   dev_addr: '127.0.0.1:8XXX'  # Use unique port
   ```

1. **Extract standardized task definitions** to wrknv.toml:

   ```python
   # Extract canonical wrknv.toml for Python library projects
   from provide.foundry.config import extract_python_wrknv_tasks
   from pathlib import Path

   # Fresh extraction (no merge)
   extract_python_wrknv_tasks(Path('.'), merge=False)

   # Or merge with existing wrknv.toml (preserves custom tasks/config)
   extract_python_wrknv_tasks(Path('.'), merge=True)
   ```

   The template provides standardized tasks for all Python projects:

   - Testing: `test`, `test.unit`, `test.integration`, `test.coverage`, `test.parallel`
   - Quality: `lint`, `format`, `typecheck`, `quality`
   - Build: `build`, `clean`
   - Docs: `docs.build`, `docs.serve`, `docs.clean`, `docs.links.check`
   - Development: `dev.setup`, `dev.test`, `dev.check`
   - CI/CD: `ci`, `ci.test`, `ci.quality`

1. **Include shared Makefile targets** (DEPRECATED - use wrknv.toml instead):

   ```python
   # Extract canonical Makefile for terraform-provider-* projects
   from provide.foundry.config import extract_makefile_provider
   from pathlib import Path
   extract_makefile_provider(Path('.'))
   ```

1. **Configure API documentation** by adding gen-files plugin:

   ```yaml
   plugins:
     - gen-files:
         scripts:
           - docs/scripts/gen_api.py  # Wrapper imports from provide.foundry.docs
     - literate-nav:
         nav_file: SUMMARY.md
   ```

### Documentation Guidelines

- All documentation uses **Markdown** with Material theme extensions
- API documentation is **auto-generated** from Python docstrings at build time
- Use **Google-style docstrings** for consistent API documentation
- Project documentation lives in `<project>/docs/` directory
- API reference is auto-generated in `<project>/docs/reference/` at build time

Copyright (c) Provide.io LLC.
