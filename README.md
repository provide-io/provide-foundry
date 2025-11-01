# Provide.io Ecosystem Documentation

Welcome to the comprehensive documentation hub for the provide.io ecosystem - a collection of Python tools and frameworks for building Terraform providers, packaging applications, and managing development workflows.

## 🚀 Quick Start

```bash
# Set up the entire ecosystem
cd /REDACTED_ABS_PATH
uv sync --extra all --extra dev
source .venv/bin/activate
```

## 📚 Documentation

The documentation is built with MkDocs Material and covers:

- **Getting Started**: Installation and first steps
- **Ecosystem**: Architecture and design principles
- **Packages**: Individual package documentation
- **Guides**: Cross-package integration guides
- **API Reference**: Complete API documentation

## 🛠 Building Documentation

The documentation system uses a modern, DRY approach with shared configuration:

### Architecture Overview

- **Shared Base Configuration** (`base-mkdocs.yml`) - Common theme, plugins, and extensions
- **Centralized Theme** (`src/provide/foundry/theme/`) - Namespace package with CSS, JavaScript, and assets
  - Install: `uv pip install -e .` for editable development
- **Monorepo Plugin** - Automatic aggregation of all project documentation
- **Auto-Generated API Docs** - Build-time generation using mkdocs-gen-files
- **Shared Makefile** (`Makefile.docs.inc`) - Standardized build targets

### Building the Aggregated Documentation

```bash
# Install dependencies
cd provide-foundry
uv sync

# Serve aggregated documentation locally (all projects)
make docs-serve
# or: uv run mkdocs serve

# Build complete documentation site
make docs-build
# or: uv run mkdocs build --clean

# Validate documentation (strict mode)
make docs-validate
# or: uv run mkdocs build --strict

# Clean documentation artifacts
make docs-clean
```

### Building Individual Project Documentation

Each project can build documentation independently:

```bash
# Navigate to any project
cd ../pyvider

# Use shared Makefile targets
make docs-build    # Build documentation
make docs-serve    # Serve locally on project's port
make docs-clean    # Clean artifacts

# Or use mkdocs directly
uv run mkdocs build
uv run mkdocs serve
```

### Documentation Structure

```
provide-foundry/                    # Documentation hub
├── base-mkdocs.yml                # Shared configuration (inherited by all projects)
├── mkdocs.yml                     # Aggregated site configuration
├── Makefile.docs.inc              # Shared documentation targets
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
├── Makefile                       # Includes Makefile.docs.inc
└── docs/                          # Project-specific docs
    ├── index.md
    ├── guides/
    └── reference/                 # Auto-generated at build time
```

## 📦 Ecosystem Packages

### Foundation Layer
- **[provide-foundation](../provide-foundation/)** - Core telemetry and logging infrastructure
- **[provide-testkit](../provide-testkit/)** - Testing utilities and fixtures

### Pyvider Framework
- **[pyvider](../pyvider/)** - Core Terraform provider framework
- **[pyvider-cty](../pyvider-cty/)** - CTY type system implementation
- **[pyvider-hcl](../pyvider-hcl/)** - HCL parsing with CTY integration
- **[pyvider-rpcplugin](../pyvider-rpcplugin/)** - gRPC plugin protocol implementation
- **[pyvider-components](../pyvider-components/)** - Standard components library
- **[terraform-provider-pyvider](../terraform-provider-pyvider/)** - Official Pyvider provider

### Tools & Utilities
- **[flavorpack](../flavorpack/)** - PSPF packaging system for executable bundles
- **[wrknv](../wrknv/)** - Work environment management
- **[plating](../plating/)** - Documentation generation for providers
- **[tofusoup](../tofusoup/)** - Cross-language conformance testing
- **[supsrc](../supsrc/)** - Automated Git commit/push utility

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

2. **Include shared Makefile targets** in your Makefile:
   ```makefile
   # Include shared documentation targets from provide-foundry
   include ../provide-foundry/Makefile.docs.inc
   ```

3. **Configure API documentation** by adding gen-files plugin:
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

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for ecosystem-wide contribution guidelines.

## 📄 License

All packages in the provide.io ecosystem are licensed under Apache-2.0 unless otherwise specified.