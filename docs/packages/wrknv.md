# wrknv

Work Environment management tool that generates standardized development environment scripts for the Provide Foundry, managing tool versions, sibling package integration, and containerized development environments.

## Overview

`wrknv` (Work Environment) is the central tool that generates all `env.sh` and `env.ps1` scripts for the Provide Foundry. Instead of maintaining hundreds of lines of duplicated shell scripts, each project uses wrknv to generate consistent, maintainable environment setup scripts.

### Key Features

- **🔧 Environment Script Generation**: Creates standardized `env.sh` and `env.ps1` scripts from templates
- **📦 Tool Version Management**: Pin versions of Terraform, OpenTofu, Go, and UV
- **🔗 Sibling Package Integration**: Automatically discover and install local, editable dependencies
- **🐍 Python Version Safety**: Detects `pyproject.toml` Python requirements and manages virtual environments
- **🐳 Containerized Development**: (Experimental) Manage Docker-based development environments
- **📋 Provider Packaging**: (Experimental) Interface for building flavor-based provider packages

## Installation

```bash
# Install from PyPI
uv add wrknv

# Install with all features
uv add wrknv[all]

# Development installation
uv add wrknv[dev]
```

## Quick Start

### 1. Initialize Project

```bash
# Create a wrknv.toml configuration
wrknv init

# Or initialize with specific tools
wrknv init --with-tofu --with-go
```

### 2. Configure Tools

```toml
# wrknv.toml
[project]
name = "my-provider"
description = "My Terraform provider"

[tools]
uv = "latest"
tofu = "1.8.0"
go = "1.22.1"

[siblings]
patterns = [
    "pyvider-*",
    "provide-*"
]

[settings]
python_version = ">=3.11"
verify_checksums = true
```

### 3. Generate Environment Scripts

```bash
# Generate env.sh and env.ps1
wrknv generate

# Generate and show what will be created
wrknv generate --dry-run
```

### 4. Activate Environment

```bash
# Activate the environment
uv sync

# Or on Windows
.\env.ps1

# Verify setup
wrknv status
```

## Core Commands

### Project Management

```bash
# Initialize new project
wrknv init                    # Interactive setup
wrknv init --name my-project  # With project name
wrknv init --template provider # From template

# Generate environment scripts
wrknv generate               # Generate all scripts
wrknv generate --force       # Overwrite existing
wrknv generate --dry-run     # Show what would be generated

# Complete setup workflow
wrknv setup                  # init + generate + instructions
```

### Status and Information

```bash
# Show project status
wrknv status                 # Tool versions and health
wrknv status --verbose       # Detailed information
wrknv status --json          # Machine-readable output

# Show configuration
wrknv config show            # Current configuration
wrknv config validate        # Validate configuration
wrknv config edit            # Edit with $EDITOR
```

### Tool Management

```bash
# Install specific tools
wrknv tools install uv       # Install UV package manager
wrknv tools install tofu     # Install OpenTofu
wrknv tools install go       # Install Go

# Update tools
wrknv tools update           # Update all tools
wrknv tools update tofu      # Update specific tool

# List available tools
wrknv tools list             # Available tools
wrknv tools versions tofu    # Available versions
```

### Container Commands

```bash
# Container management (experimental)
wrknv container build        # Build development container
wrknv container exec         # Execute command in container
wrknv container shell        # Interactive shell
wrknv container clean        # Clean up containers
```

### Package Commands

```bash
# Provider packaging (experimental)
wrknv package build          # Build provider package
wrknv package sign           # Sign package
wrknv package publish        # Publish to registry
wrknv package validate       # Validate package
```

## Configuration

### Project Configuration

```toml
# wrknv.toml
[project]
name = "my-terraform-provider"
description = "Custom Terraform provider"
version = "0.1.0"
authors = ["Your Name <you@example.com>"]

[tools]
# Package manager (required)
uv = "latest"                 # or specific version like "0.4.0"

# Terraform tools
terraform = "1.9.0"          # HashiCorp Terraform
tofu = "1.8.0"               # OpenTofu
tflint = "latest"            # Terraform linter

# Language runtimes
go = "1.22.1"                # Go language
rust = "1.75.0"              # Rust language
node = "20.11.0"             # Node.js

# Development tools
docker = "latest"            # Docker
kubectl = "latest"           # Kubernetes CLI

[siblings]
# Patterns for discovering sibling packages
patterns = [
    "pyvider-*",             # All pyvider packages
    "provide-*",             # All provide packages
    "my-provider-*"          # Custom patterns
]

# Explicit sibling paths
paths = [
    "../shared-library",
    "../common-components"
]

[settings]
# Python version requirements
python_version = ">=3.11"

# Security and verification
verify_checksums = true      # Verify downloaded tool checksums
verify_signatures = false   # Verify tool signatures (when available)

# Performance
parallel_downloads = true   # Download tools in parallel
cache_tools = true          # Cache downloaded tools

# Environment
workenv_prefix = "workenv"  # Virtual environment directory name
shell_integration = true   # Add shell completions

[container]
# Container settings (experimental)
base_image = "python:3.11-slim"
packages = ["git", "curl", "build-essential"]
ports = [8080, 8443]
volumes = ["./data:/app/data"]

[package]
# Packaging settings (experimental)
format = "psp"              # Package format
compression = "gzip"        # Compression method
include_docs = true         # Include documentation
```

### Environment Variables

Customize wrknv behavior with environment variables:

```bash
# Tool installation
export WRKNV_TOOLS_DIR="$HOME/.local/share/wrknv/tools"
export WRKNV_CACHE_DIR="$HOME/.cache/wrknv"

# Download behavior
export WRKNV_DOWNLOAD_TIMEOUT="300"
export WRKNV_VERIFY_CHECKSUMS="true"
export WRKNV_PARALLEL_DOWNLOADS="true"

# Container settings
export WRKNV_CONTAINER_RUNTIME="docker"  # or "podman"
export WRKNV_CONTAINER_REGISTRY="ghcr.io"

# Debug and logging
export WRKNV_LOG_LEVEL="info"           # debug, info, warn, error
export WRKNV_DEBUG="false"
```

## Tool Managers

### Supported Tools

wrknv includes managers for common development tools:

```toml
[tools]
# Package managers
uv = "latest"               # UV (Python)
npm = "20.11.0"            # Node.js/npm
pip = "latest"             # Python pip

# Terraform ecosystem
terraform = "1.9.0"        # HashiCorp Terraform
tofu = "1.8.0"             # OpenTofu
terragrunt = "latest"      # Terragrunt
tflint = "latest"          # Terraform linter
checkov = "latest"         # Security scanner

# Language runtimes
go = "1.22.1"              # Go
rust = "1.75.0"            # Rust
node = "20.11.0"           # Node.js
python = "3.11.8"          # Python

# Cloud tools
aws = "latest"             # AWS CLI
gcloud = "latest"          # Google Cloud CLI
azure = "latest"           # Azure CLI
kubectl = "latest"         # Kubernetes CLI

# Development tools
docker = "latest"          # Docker
git = "latest"             # Git
make = "latest"            # GNU Make
```

### Custom Tool Managers

Add custom tools by extending the manager system:

```python
# custom_tools.py
from wrknv.managers import BaseToolManager

class CustomToolManager(BaseToolManager):
    """Manager for custom development tool."""

    def get_download_url(self, version: str, platform: str, arch: str) -> str:
        """Get download URL for tool version."""
        return f"https://releases.example.com/v{version}/tool_{platform}_{arch}.tar.gz"

    def get_executable_name(self, platform: str) -> str:
        """Get executable name for platform."""
        return "custom-tool.exe" if platform == "windows" else "custom-tool"

    def install(self, version: str, install_path: Path) -> None:
        """Install tool to specified path."""
        # Custom installation logic
        pass

# Register custom manager
from wrknv.managers import register_manager
register_manager("custom-tool", CustomToolManager)
```

## Templates

### Environment Script Templates

wrknv uses Jinja2 templates to generate environment scripts:

```bash
# Default template locations
~/.config/wrknv/templates/env.sh.j2
~/.config/wrknv/templates/env.ps1.j2

# Project-specific templates
./wrknv/templates/env.sh.j2
./wrknv/templates/env.ps1.j2
```

### Custom Templates

Create custom environment script templates:

```jinja2
{# env.sh.j2 - Custom Bash template #}
#!/bin/bash
# Generated by wrknv for {{ project.name }}

set -euo pipefail

# Project information
export PROJECT_NAME="{{ project.name }}"
export PROJECT_VERSION="{{ project.version }}"
export WORKENV_DIR="{{ workenv_dir }}"

# Create virtual environment
if [[ ! -d "$WORKENV_DIR" ]]; then
    echo "🔨 Creating virtual environment..."
    {{ tools.uv.executable }} venv "$WORKENV_DIR"
fi

# Activate virtual environment
source "$WORKENV_DIR/bin/activate"

# Install project dependencies
echo "📦 Installing dependencies..."
{{ tools.uv.executable }} uv add -e .

# Install sibling packages
{% for sibling in siblings %}
if [[ -d "{{ sibling.path }}" ]]; then
    echo "🔗 Installing {{ sibling.name }}..."
    {{ tools.uv.executable }} uv add -e "{{ sibling.path }}"
fi
{% endfor %}

# Set up tools
{% for tool_name, tool in tools.items() %}
export {{ tool_name.upper() }}_VERSION="{{ tool.version }}"
export PATH="{{ tool.bin_dir }}:$PATH"
{% endfor %}

# Custom environment setup
{% if project.environment_setup %}
{{ project.environment_setup }}
{% endif %}

echo "✅ Environment ready!"
echo "   Project: {{ project.name }}"
echo "   Python: $(python --version)"
{% for tool_name, tool in tools.items() %}
echo "   {{ tool_name }}: $({{ tool.executable }} --version 2>/dev/null | head -n1 || echo 'not found')"
{% endfor %}
```

## Sibling Package Discovery

### Automatic Discovery

wrknv automatically discovers related packages based on patterns:

```toml
[siblings]
# Pattern-based discovery
patterns = [
    "pyvider-*",        # Matches pyvider-cty, pyvider-hcl, etc.
    "provide-*",        # Matches provide-foundation, provide-testkit
    "my-company-*"      # Custom namespace
]

# Directory scanning
scan_directories = [
    "../",              # Parent directory
    "../../packages/"   # Relative path
]

# Exclusions
exclude_patterns = [
    "*-archived",       # Skip archived packages
    "*-deprecated"      # Skip deprecated packages
]
```

### Manual Configuration

Explicitly specify sibling packages:

```toml
[siblings]
# Direct paths
paths = [
    "../provide-foundation",
    "../provide-testkit",
    "../pyvider-cty",
    "../pyvider-hcl"
]

# With custom names
named_paths = [
    { name = "foundation", path = "../provide-foundation" },
    { name = "testkit", path = "../provide-testkit" }
]

# Git repositories
git_repos = [
    { name = "shared-lib", url = "https://github.com/company/shared-lib.git", branch = "main" }
]
```

## Container Support

### Container Configuration

Set up containerized development environments:

```toml
[container]
# Base configuration
base_image = "python:3.11-slim"
name = "{{ project.name }}-dev"
workspace = "/workspace"

# System packages
packages = [
    "git",
    "curl",
    "build-essential",
    "postgresql-client"
]

# Environment variables
environment = [
    "PYTHONPATH=/workspace/src",
    "PYTHONUNBUFFERED=1"
]

# Port mappings
ports = [
    { host = 8080, container = 8080 },
    { host = 5432, container = 5432 }
]

# Volume mounts
volumes = [
    { host = ".", container = "/workspace" },
    { host = "~/.aws", container = "/root/.aws" },
    { host = "/var/run/docker.sock", container = "/var/run/docker.sock" }
]

# Network configuration
networks = ["development"]

# Resource limits
resources = [
    { memory = "4g" },
    { cpus = "2.0" }
]
```

### Container Commands

```bash
# Build development container
wrknv container build

# Start container with shell
wrknv container shell

# Execute command in container
wrknv container exec -- python -m pytest

# Run development server
wrknv container run --service web

# Clean up containers and images
wrknv container clean
```

## Provider Packaging

### Package Configuration

Configure provider packaging (experimental):

```toml
[package]
# Package format
format = "psp"              # Provide Self-contained Package
compression = "gzip"        # Compression method

# Metadata
name = "{{ project.name }}"
version = "{{ project.version }}"
description = "{{ project.description }}"

# Content inclusion
include = [
    "src/",
    "README.md",
    "LICENSE"
]

exclude = [
    "tests/",
    "*.pyc",
    "__pycache__/"
]

# Dependencies
bundle_dependencies = true  # Include all dependencies
optimize_size = true       # Optimize package size

# Signing
sign_package = true        # Sign with Ed25519
keyfile = "~/.wrknv/signing.key"

# Publishing
registry = "https://registry.provide.io"
namespace = "my-company"
```

### Package Commands

```bash
# Build package
wrknv package build
wrknv package build --output dist/

# Validate package
wrknv package validate my-provider.psp

# Sign package
wrknv package sign my-provider.psp

# Publish to registry
wrknv package publish my-provider.psp
wrknv package publish --registry https://custom-registry.com
```

## Integration Examples

### With provide-foundation

```python
# Using wrknv in Python applications
from wrknv import WorkEnvironment
from provide.foundation import logger

log = logger.get_logger(__name__)

def setup_development_environment():
    """Set up development environment programmatically."""
    workenv = WorkEnvironment(".")

    # Load configuration
    config = workenv.load_config()
    log.info("Loaded configuration", project=config.project.name)

    # Install tools
    for tool_name, version in config.tools.items():
        log.info("Installing tool", tool=tool_name, version=version)
        workenv.install_tool(tool_name, version)

    # Install siblings
    for sibling in workenv.discover_siblings():
        log.info("Installing sibling", name=sibling.name, path=sibling.path)
        workenv.install_sibling(sibling)

    log.info("Environment setup complete")

if __name__ == "__main__":
    setup_development_environment()
```

### With CI/CD

```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install wrknv
        run: uv add wrknv

      - name: Set up development environment
        run: |
          wrknv generate
          uv sync

      - name: Run tests
        run: |
          uv sync
          pytest tests/

      - name: Check tool versions
        run: |
          uv sync
          wrknv status
```

## Performance Optimization

### Caching

Enable caching for faster environment setup:

```toml
[settings]
# Tool caching
cache_tools = true
cache_dir = "~/.cache/wrknv"
cache_ttl = 86400  # 24 hours

# Download optimization
parallel_downloads = true
download_timeout = 300
retry_attempts = 3

# Sibling caching
cache_sibling_discovery = true
sibling_cache_ttl = 3600  # 1 hour
```

### Parallel Operations

Configure parallel processing:

```bash
# Environment variables
export WRKNV_PARALLEL_DOWNLOADS="true"
export WRKNV_MAX_WORKERS="4"
export WRKNV_DOWNLOAD_TIMEOUT="300"

# Generate with parallel sibling installation
wrknv generate --parallel
```

## Troubleshooting

### Common Issues

**Tool installation fails:**
```bash
# Check available versions
wrknv tools versions tofu

# Force reinstall
wrknv tools install tofu --force

# Check system requirements
wrknv status --verbose
```

**Sibling discovery issues:**
```bash
# Debug sibling discovery
wrknv config show --siblings

# Manual sibling paths
wrknv config edit  # Add explicit paths
```

**Container problems:**
```bash
# Check container runtime
docker --version
podman --version

# Clean container cache
wrknv container clean --all

# Debug container build
wrknv container build --verbose
```

### Debug Mode

Enable debug logging for troubleshooting:

```bash
# Enable debug mode
export WRKNV_DEBUG="true"
export WRKNV_LOG_LEVEL="debug"

# Run commands with verbose output
wrknv generate --verbose
wrknv status --debug
```

## Best Practices

1. **Version pinning** - Pin specific tool versions for reproducible environments
2. **Regular updates** - Keep tool versions updated for security and features
3. **Sibling patterns** - Use clear patterns for sibling package discovery
4. **Container isolation** - Use containers for consistent development environments
5. **Cache management** - Enable caching for faster setup times
6. **Documentation** - Document custom configurations and requirements
7. **Testing** - Test environment scripts across different platforms

## Related Packages

- **[provide-foundation](foundation.md)**: Foundation services used by wrknv
- **[flavorpack](flavorpack.md)**: Packaging tool for applications
- **[provide-testkit](testkit.md)**: Testing utilities

---

wrknv eliminates the burden of maintaining complex environment setup scripts across projects, providing a consistent, reliable foundation for development in the Provide Foundry.