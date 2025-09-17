# flavorpack

Cross-language packaging system that creates self-contained executable packages (.psp files) for distributing applications across different platforms and environments.

## Overview

`flavorpack` enables you to package Python applications, Terraform providers, and other software into single-file executables that contain all dependencies and can run on any compatible system without requiring installation.

### Key Features

- **📦 Self-Contained Packages**: Everything bundled into a single .psp file
- **🌍 Cross-Platform**: Works on Linux, macOS, and Windows
- **🔒 Secure Packaging**: Ed25519 signing and verification
- **⚡ Fast Execution**: Optimized runtime with minimal overhead
- **🎯 Multiple Formats**: Support for different package types
- **🔧 Tool Integration**: Works with wrknv and other foundry tools

## Installation

```bash
uv add flavorpack
```

## Quick Start

### Basic Packaging

```bash
# Package a Python application
flavor pack --manifest pyproject.toml --output myapp.psp

# Run the packaged application
./myapp.psp --help
```

### Advanced Packaging

```bash
# Package with custom configuration
flavor pack \
  --manifest pyproject.toml \
  --config flavor.toml \
  --output dist/myapp.psp \
  --sign \
  --compress gzip

# Package Terraform provider
flavor pack \
  --type terraform-provider \
  --manifest provider.toml \
  --output terraform-provider-custom.psp
```

## Package Types

### Python Applications

Package Python CLI tools and applications:

```toml
# pyproject.toml
[project]
name = "myapp"
version = "1.0.0"
scripts = {myapp = "myapp.cli:main"}

[tool.flavorpack]
type = "python-app"
entry_point = "myapp.cli:main"
include_stdlib = false
optimize = true
```

### Terraform Providers

Package Terraform providers:

```toml
# provider.toml
[provider]
name = "custom"
version = "1.0.0"
platform = "linux_amd64"

[flavorpack]
type = "terraform-provider"
binary_name = "terraform-provider-custom"
protocols = ["5.0"]
```

### Generic Executables

Package any executable with dependencies:

```toml
# flavor.toml
[package]
name = "mytool"
version = "1.0.0"
executable = "./bin/mytool"

[flavorpack]
type = "executable"
runtime = "generic"
dependencies = ["./lib/", "./data/"]
```

## Configuration

### Package Configuration

```toml
# flavor.toml
[package]
name = "myapp"
version = "1.0.0"
description = "My application"
authors = ["Your Name <you@example.com>"]

[flavorpack]
# Package type
type = "python-app"           # python-app, terraform-provider, executable

# Runtime configuration
runtime = "python311"        # Runtime version
entry_point = "myapp:main"   # Entry point function

# Content inclusion
include = [
    "src/",
    "data/",
    "config/",
    "README.md"
]

exclude = [
    "tests/",
    "*.pyc",
    "__pycache__/",
    ".git/"
]

# Optimization
optimize = true              # Optimize bytecode
strip_debug = true          # Remove debug information
compress = "gzip"           # Compression method

# Security
sign = true                 # Sign package
verify_deps = true          # Verify dependency integrity

# Platform targeting
platforms = [
    "linux_amd64",
    "darwin_amd64",
    "darwin_arm64",
    "windows_amd64"
]
```

### Runtime Configuration

```toml
[runtime]
# Python runtime
python_version = "3.11"
include_stdlib = false      # Bundle Python stdlib
precompile = true          # Precompile Python modules

# Environment variables
environment = [
    "PYTHONPATH=/app/src",
    "PYTHONUNBUFFERED=1"
]

# Resource limits
memory_limit = "1g"
cpu_limit = "2.0"

# Startup optimization
lazy_imports = true
optimize_startup = true
```

## Commands

### Packaging Commands

```bash
# Basic packaging
flavor pack --manifest pyproject.toml

# With custom output
flavor pack --manifest pyproject.toml --output dist/app.psp

# Different package types
flavor pack --type python-app --manifest pyproject.toml
flavor pack --type terraform-provider --manifest provider.toml
flavor pack --type executable --manifest flavor.toml

# With signing
flavor pack --manifest pyproject.toml --sign
flavor pack --manifest pyproject.toml --sign --keyfile ~/.keys/signing.key

# Platform-specific builds
flavor pack --manifest pyproject.toml --platform linux_amd64
flavor pack --manifest pyproject.toml --platform all

# Optimization options
flavor pack --manifest pyproject.toml --optimize --compress gzip
```

### Package Management

```bash
# Verify package
flavor verify myapp.psp
flavor verify myapp.psp --keyfile public.key

# Extract package contents
flavor extract myapp.psp --output extracted/
flavor extract myapp.psp --list  # List contents only

# Package information
flavor info myapp.psp
flavor info myapp.psp --json

# Test package
flavor test myapp.psp
flavor test myapp.psp --args "--help"
```

### Registry Operations

```bash
# Publish to registry
flavor publish myapp.psp
flavor publish myapp.psp --registry https://packages.company.com
flavor publish myapp.psp --token $REGISTRY_TOKEN

# Install from registry
flavor install myapp
flavor install myapp@1.0.0
flavor install company/myapp

# Registry management
flavor login https://packages.company.com
flavor logout
flavor search terraform-provider
```

## Package Format

### .psp File Structure

```
package.psp
├── manifest.json          # Package metadata
├── signature.sig          # Ed25519 signature
├── runtime/               # Runtime environment
│   ├── python/           # Python interpreter (if bundled)
│   └── libs/             # Shared libraries
├── app/                  # Application code
│   ├── src/              # Source code
│   ├── data/             # Data files
│   └── config/           # Configuration
└── bootstrap            # Bootstrap executable
```

### Manifest Format

```json
{
  "name": "myapp",
  "version": "1.0.0",
  "type": "python-app",
  "platform": "linux_amd64",
  "runtime": {
    "type": "python",
    "version": "3.11.8"
  },
  "entry_point": "myapp:main",
  "signature": {
    "algorithm": "ed25519",
    "public_key": "...",
    "signed_hash": "..."
  },
  "dependencies": [
    {"name": "requests", "version": "2.31.0"},
    {"name": "click", "version": "8.1.7"}
  ],
  "build_info": {
    "timestamp": "2024-01-15T10:30:00Z",
    "builder": "flavorpack-1.0.0",
    "platform": "linux_amd64"
  }
}
```

## Security

### Package Signing

```bash
# Generate signing keys
flavor keygen --output ~/.keys/
# Creates signing.key (private) and signing.pub (public)

# Sign package during build
flavor pack --manifest pyproject.toml --sign --keyfile ~/.keys/signing.key

# Verify signed package
flavor verify myapp.psp --keyfile ~/.keys/signing.pub

# List package signatures
flavor info myapp.psp --signatures
```

### Key Management

```bash
# Key operations
flavor keygen --algorithm ed25519 --output keys/
flavor keyinfo keys/signing.pub
flavor keyexport keys/signing.key --format pem

# Registry keys
flavor keyadd registry https://packages.company.com keys/registry.pub
flavor keylist
flavor keyremove registry
```

## Advanced Features

### Multi-Platform Builds

```bash
# Build for multiple platforms
flavor pack --manifest pyproject.toml --platform all

# Specific platforms
flavor pack \
  --manifest pyproject.toml \
  --platform linux_amd64,darwin_amd64,windows_amd64

# Platform-specific configuration
flavor pack \
  --manifest pyproject.toml \
  --config-linux flavor-linux.toml \
  --config-windows flavor-windows.toml
```

### Custom Runtimes

```toml
# flavor.toml
[runtime.python]
version = "3.11.8"
implementation = "cpython"
include_stdlib = true
optimize_level = 2

[runtime.system]
libraries = [
    "libssl.so.3",
    "libcrypto.so.3"
]

[runtime.custom]
bootstrap = "./scripts/bootstrap.sh"
environment = ["CUSTOM_VAR=value"]
```

### Plugin System

```python
# Custom packaging plugin
from flavorpack.plugins import PackagingPlugin

class CustomPlugin(PackagingPlugin):
    """Custom packaging plugin."""

    def process_manifest(self, manifest):
        """Process package manifest."""
        manifest["custom_field"] = "custom_value"
        return manifest

    def package_files(self, files):
        """Process files before packaging."""
        # Custom file processing
        return processed_files

    def post_package(self, package_path):
        """Post-packaging operations."""
        print(f"Package created: {package_path}")

# Register plugin
from flavorpack import register_plugin
register_plugin("custom", CustomPlugin)
```

## Integration Examples

### With wrknv

```toml
# wrknv.toml
[package]
format = "psp"
tool = "flavorpack"

[tools]
flavorpack = "latest"

# Build package in wrknv environment
$ source env.sh
$ flavor pack --manifest pyproject.toml
```

### With CI/CD

```yaml
# .github/workflows/package.yml
- name: Package Application
  run: |
    uv add flavorpack
    flavor pack \
      --manifest pyproject.toml \
      --output dist/${{ github.event.repository.name }}.psp \
      --sign \
      --keyfile ${{ secrets.SIGNING_KEY }}

- name: Upload Package
  uses: actions/upload-artifact@v4
  with:
    name: package
    path: dist/*.psp
```

### With Terraform

```hcl
# Package Terraform provider
resource "null_resource" "package_provider" {
  provisioner "local-exec" {
    command = <<-EOT
      flavor pack \
        --type terraform-provider \
        --manifest provider.toml \
        --output terraform-provider-${var.provider_name}.psp
    EOT
  }
}
```

## Performance

### Build Optimization

```toml
[flavorpack.optimization]
# Code optimization
precompile = true           # Precompile Python modules
optimize_bytecode = true    # Optimize bytecode
strip_debug = true          # Remove debug information
remove_docstrings = false   # Keep documentation

# Size optimization
compress = "gzip"           # Compression method
compression_level = 6       # Compression level (1-9)
exclude_unused = true       # Remove unused dependencies
minimize_stdlib = true      # Minimize stdlib inclusion

# Runtime optimization
lazy_loading = true         # Lazy load modules
cache_imports = true        # Cache import resolution
optimize_startup = true     # Optimize startup time
```

### Runtime Performance

```bash
# Performance profiling
flavor profile myapp.psp --duration 60s
flavor profile myapp.psp --memory --cpu

# Runtime statistics
flavor stats myapp.psp
flavor stats myapp.psp --detailed
```

## Best Practices

1. **Pin dependencies** - Use exact versions for reproducible packages
2. **Optimize size** - Exclude unnecessary files and dependencies
3. **Sign packages** - Always sign packages for security
4. **Test packages** - Test packaged applications before distribution
5. **Use compression** - Enable compression for smaller packages
6. **Platform-specific builds** - Create optimized builds for target platforms
7. **Version management** - Use semantic versioning for packages

## Related Packages

- **[wrknv](wrknv.md)**: Environment management with packaging integration
- **[provide-foundation](foundation.md)**: Foundation services
- **[pyvider](pyvider.md)**: Framework for provider packaging

---

flavorpack revolutionizes application distribution by creating truly portable, self-contained packages that run anywhere without installation requirements.