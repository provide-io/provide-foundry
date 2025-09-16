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

```bash
# Install documentation dependencies
pip install -r requirements.txt

# Serve documentation locally
mkdocs serve

# Build static documentation
mkdocs build
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

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for ecosystem-wide contribution guidelines.

## 📄 License

All packages in the provide.io ecosystem are licensed under Apache-2.0 unless otherwise specified.