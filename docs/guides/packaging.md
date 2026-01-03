# Packaging Guide

Complete guide to packaging, distributing, and publishing Terraform providers built with Pyvider and the provide.foundation ecosystem.

## Overview

This guide covers the entire packaging lifecycle for Pyvider-based Terraform providers, from local development builds to publishing on the Terraform Registry.

## Project Structure

### Standard Provider Layout

```
terraform-provider-myservice/
├── src/
│   └── terraform_provider_myservice/
│       ├── __init__.py
│       ├── provider.py          # Provider definition
│       ├── resources/           # Resource implementations
│       │   ├── __init__.py
│       │   ├── server.py
│       │   └── database.py
│       ├── data_sources/        # Data source implementations
│       │   ├── __init__.py
│       │   └── image.py
│       └── client/              # API client code
│           ├── __init__.py
│           └── api.py
├── tests/                       # Test suite
│   ├── unit/
│   ├── integration/
│   └── acceptance/
├── docs/                        # Documentation
│   ├── index.md
│   ├── resources/
│   └── data-sources/
├── examples/                    # Example configurations
├── pyproject.toml              # Project configuration
├── terraform-registry-manifest.json
└── README.md
```

## Project Configuration

### pyproject.toml Setup

```toml
[build-system]
requires = ["hatchling", "pyvider-build-plugin"]
build-backend = "hatchling.build"

[project]
name = "terraform-provider-myservice"
version = "1.0.0"
description = "Terraform provider for MyService API"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
readme = "README.md"
license = {file = "LICENSE"}
keywords = ["terraform", "provider", "myservice", "pyvider"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: System :: Systems Administration",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

requires-python = ">=3.11"
dependencies = [
    "pyvider>=2.0.0",
    "pyvider-components>=1.0.0",
    "provide-foundation>=1.0.0",
    "requests>=2.28.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-xdist>=3.0.0",
    "provide-testkit>=1.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
]

test = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "provide-testkit>=1.0.0",
]

docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",
    "mkdocstrings[python]>=0.23.0",
]

[project.urls]
Homepage = "https://github.com/yourorg/terraform-provider-myservice"
Documentation = "https://provider-docs.example.com"
Repository = "https://github.com/yourorg/terraform-provider-myservice"
Issues = "https://github.com/yourorg/terraform-provider-myservice/issues"
Changelog = "https://github.com/yourorg/terraform-provider-myservice/blob/main/CHANGELOG.md"

[project.entry-points."terraform.providers"]
myservice = "terraform_provider_myservice:main"

[tool.hatch.build.targets.wheel]
packages = ["src/terraform_provider_myservice"]

[tool.hatch.version]
path = "src/terraform_provider_myservice/__init__.py"

# Pyvider-specific configuration
[tool.pyvider]
provider_name = "myservice"
binary_name = "terraform-provider-myservice"
terraform_protocol_version = 6

[tool.pyvider.build]
# Include documentation in build
include_docs = true
# Generate protocol files
generate_grpc = true
# Optimize for distribution
optimize = true

[tool.black]
target-version = ["py311"]
line-length = 88

[tool.ruff]
target-version = "py311"
line-length = 88

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80",
]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "acceptance: Acceptance tests",
    "slow: Slow running tests",
]
```

## Build Process

### Local Development Builds

```bash
# Install in development mode
uv sync --extra dev

# Run tests
uv run pytest

# Build documentation
uv run mkdocs build

# Build provider binary
uv run pyvider build

# Install provider locally for testing
uv run pyvider install --local
```

### Provider Binary Generation

```python
# src/terraform_provider_myservice/__main__.py
"""Main entry point for the Terraform provider."""

import sys
from pyvider.runtime import run_provider
from .provider import MyServiceProvider

def main():
    """Run the provider."""
    return run_provider(MyServiceProvider, sys.argv[1:])

if __name__ == "__main__":
    sys.exit(main())
```

### Build Script

```python
# scripts/build.py
"""Build script for the provider."""

import os
import shutil
import subprocess
from pathlib import Path

def build_provider():
    """Build the provider for distribution."""

    # Clean previous builds
    build_dir = Path("dist")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    # Build Python package
    subprocess.run(["uv", "build"], check=True)

    # Build provider binary
    subprocess.run(["pyvider", "build", "--release"], check=True)

    # Generate documentation
    subprocess.run(["mkdocs", "build"], check=True)

    # Create distribution package
    create_distribution_package()

def create_distribution_package():
    """Create complete distribution package."""
    dist_dir = Path("dist")

    # Copy binary
    binary_src = Path("build/terraform-provider-myservice")
    binary_dst = dist_dir / "terraform-provider-myservice"
    shutil.copy2(binary_src, binary_dst)

    # Copy documentation
    docs_dst = dist_dir / "docs"
    shutil.copytree("site", docs_dst)

    # Copy examples
    examples_dst = dist_dir / "examples"
    shutil.copytree("examples", examples_dst)

    # Copy metadata
    shutil.copy2("terraform-registry-manifest.json", dist_dir)
    shutil.copy2("README.md", dist_dir)
    shutil.copy2("LICENSE", dist_dir)
    shutil.copy2("CHANGELOG.md", dist_dir)

if __name__ == "__main__":
    build_provider()
```

## Documentation Generation

### Automatic Documentation

```python
# scripts/generate_docs.py
"""Generate provider documentation from code."""

from pyvider.docs import DocumentationGenerator
from terraform_provider_myservice import MyServiceProvider

def generate_docs():
    """Generate documentation for all resources and data sources."""

    generator = DocumentationGenerator(MyServiceProvider)

    # Generate resource documentation
    for resource_name, resource_class in MyServiceProvider.get_resources():
        doc_path = f"docs/resources/{resource_name}.md"
        generator.generate_resource_docs(resource_class, doc_path)

    # Generate data source documentation
    for ds_name, ds_class in MyServiceProvider.get_data_sources():
        doc_path = f"docs/data-sources/{ds_name}.md"
        generator.generate_data_source_docs(ds_class, doc_path)

    # Generate provider documentation
    generator.generate_provider_docs("docs/index.md")

if __name__ == "__main__":
    generate_docs()
```

### MkDocs Configuration

```yaml
# mkdocs.yml
site_name: MyService Terraform Provider
site_description: Terraform provider for MyService API
site_url: https://provider-docs.example.com

repo_url: https://github.com/yourorg/terraform-provider-myservice
repo_name: terraform-provider-myservice

theme:
  name: material
  palette:
    - scheme: default
      primary: blue
      accent: blue
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.highlight
    - search.share

nav:
  - Home: index.md
  - Resources:
    - myservice_server: resources/myservice_server.md
    - myservice_database: resources/myservice_database.md
  - Data Sources:
    - myservice_image: data-sources/myservice_image.md
  - Guides:
    - Installation: guides/installation.md
    - Authentication: guides/authentication.md
    - Examples: guides/examples.md

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
```

## Registry Preparation

### Terraform Registry Manifest

```json
{
  "version": 1,
  "metadata": {
    "protocol_versions": ["6.0"]
  }
}
```

### Provider Documentation Structure

```
docs/
├── index.md                    # Provider overview
├── data-sources/
│   └── myservice_image.md     # Data source docs
├── resources/
│   ├── myservice_server.md    # Resource docs
│   └── myservice_database.md
└── guides/
    ├── installation.md
    ├── authentication.md
    └── examples.md
```

### Example Configurations

```hcl
# examples/basic/main.tf
terraform {
  required_providers {
    myservice = {
      source  = "yourorg/myservice"
      version = "~> 1.0"
    }
  }
}

provider "myservice" {
  api_url = "https://api.myservice.com"
  api_key = var.myservice_api_key
}

resource "myservice_server" "example" {
  name   = "example-server"
  size   = "small"
  region = "us-east-1"

  tags = {
    Environment = "development"
    Project     = "example"
  }
}

data "myservice_image" "ubuntu" {
  name_filter = "ubuntu-22.04"
  os_type     = "linux"
}

output "server_id" {
  value = myservice_server.example.id
}
```

## Distribution Methods

### Local Installation

```bash
# Build and install locally
uv run pyvider build --install

# Create local mirror
mkdir -p ~/.terraform.d/plugins/local/yourorg/myservice/1.0.0/linux_amd64/
cp dist/terraform-provider-myservice ~/.terraform.d/plugins/local/yourorg/myservice/1.0.0/linux_amd64/

# Test local installation
cd examples/basic
terraform init
terraform plan
```

### GitHub Releases

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0

    - uses: actions/setup-python@v4
      with:
        python-version: "3.11"

    - name: Install dependencies
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        uv sync --extra dev

    - name: Build provider
      run: |
        source .venv/bin/activate
        python scripts/build.py

    - name: Create checksums
      run: |
        cd dist
        sha256sum * > terraform-provider-myservice_${{ github.ref_name }}_SHA256SUMS

    - name: Sign checksums
      env:
        GPG_PRIVATE_KEY: ${{ secrets.GPG_PRIVATE_KEY }}
        GPG_PASSPHRASE: ${{ secrets.GPG_PASSPHRASE }}
      run: |
        echo "$GPG_PRIVATE_KEY" | gpg --import
        cd dist
        gpg --batch --yes --detach-sign --armor terraform-provider-myservice_${{ github.ref_name }}_SHA256SUMS

    - name: Create release
      uses: softprops/action-gh-release@v1
      with:
        files: |
          dist/terraform-provider-myservice
          dist/terraform-provider-myservice_${{ github.ref_name }}_SHA256SUMS
          dist/terraform-provider-myservice_${{ github.ref_name }}_SHA256SUMS.sig
        generate_release_notes: true
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### PyPI Distribution

```bash
# Build Python package
uv build

# Upload to PyPI
uv publish --token $PYPI_TOKEN

# Install from PyPI
uv add terraform-provider-myservice
```

## Terraform Registry Publishing

### Registry Preparation

1. **Create GitHub repository** with proper structure
2. **Tag releases** following semantic versioning
3. **Sign releases** with GPG key
4. **Add documentation** in correct format
5. **Test installation** from GitHub releases

### Registry Submission

```yaml
# terraform-registry-manifest.json
{
  "version": 1,
  "metadata": {
    "protocol_versions": ["6.0"]
  }
}
```

### Documentation Requirements

- Provider overview in `docs/index.md`
- Resource documentation in `docs/resources/`
- Data source documentation in `docs/data-sources/`
- Example configurations in `examples/`

## Quality Assurance

### Pre-Release Checklist

- [ ] All tests pass (unit, integration, acceptance)
- [ ] Documentation is complete and accurate
- [ ] Examples work correctly
- [ ] Version numbers are updated
- [ ] Changelog is updated
- [ ] License is included
- [ ] Security scan passes

### Automated Quality Gates

```yaml
# .github/workflows/quality.yml
name: Quality Gates

on:
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Security scan
      uses: securecodewarrior/github-action-add-sarif@v1
      with:
        sarif-file: security-scan-results.sarif

    - name: License compliance
      run: |
        # Check for proper license headers
        python scripts/check_licenses.py

    - name: Documentation check
      run: |
        # Verify all resources have documentation
        python scripts/check_docs.py

    - name: Example validation
      run: |
        # Validate all example configurations
        for dir in examples/*/; do
          cd "$dir"
          terraform init
          terraform validate
          cd -
        done
```

## Multi-Platform Builds

### Cross-Platform Configuration

```yaml
# .github/workflows/build.yml
name: Build

on:
  push:
    tags: ['v*']

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        arch: [amd64, arm64]
        exclude:
          - os: windows-latest
            arch: arm64

    runs-on: ${{ matrix.os }}

    steps:
    - uses: actions/checkout@v3

    - name: Build provider
      run: |
        pyvider build --os=${{ matrix.os }} --arch=${{ matrix.arch }}

    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: terraform-provider-myservice_${{ matrix.os }}_${{ matrix.arch }}
        path: dist/terraform-provider-myservice*
```

## Maintenance and Updates

### Version Management

```python
# scripts/bump_version.py
"""Version management script."""

import re
from pathlib import Path

def bump_version(part="patch"):
    """Bump version number."""

    # Read current version
    init_file = Path("src/terraform_provider_myservice/__init__.py")
    content = init_file.read_text()

    # Extract version
    version_match = re.search(r'__version__ = "(\d+)\.(\d+)\.(\d+)"', content)
    if not version_match:
        raise ValueError("Version not found")

    major, minor, patch = map(int, version_match.groups())

    # Bump version
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1

    new_version = f"{major}.{minor}.{patch}"

    # Update files
    update_version_in_file(init_file, new_version)
    update_version_in_file(Path("pyproject.toml"), new_version)

    return new_version

def update_version_in_file(file_path, version):
    """Update version in file."""
    content = file_path.read_text()

    if file_path.name == "__init__.py":
        content = re.sub(
            r'__version__ = "\d+\.\d+\.\d+"',
            f'__version__ = "{version}"',
            content
        )
    elif file_path.name == "pyproject.toml":
        content = re.sub(
            r'version = "\d+\.\d+\.\d+"',
            f'version = "{version}"',
            content
        )

    file_path.write_text(content)

if __name__ == "__main__":
    import sys
    part = sys.argv[1] if len(sys.argv) > 1 else "patch"
    new_version = bump_version(part)
    print(f"Version bumped to {new_version}")
```

### Dependency Updates

```bash
# Update dependencies
uv sync --upgrade

# Check for security vulnerabilities
uv audit

# Update pre-commit hooks
pre-commit autoupdate
```

## Best Practices

### Build Optimization

- Use multi-stage builds for Docker images
- Optimize binary size with build flags
- Cache dependencies for faster builds
- Use parallel builds where possible

### Documentation

- Keep documentation in sync with code
- Use automation for documentation generation
- Include working examples
- Test documentation regularly

### Security

- Sign all releases with GPG
- Scan for vulnerabilities regularly
- Use secure build environments
- Follow security best practices for secrets

### Testing

- Test packages before publishing
- Validate against multiple Terraform versions
- Test installation on clean environments
- Automate testing in CI/CD

## Related Documentation

- **[Provider Development Guide](provider-development/)** - Building providers with Pyvider
- **[Testing Guide](testing/)** - Comprehensive testing strategies
- **[API Reference](../pyvider/reference/)** - Complete Pyvider API documentation
