# 🌐🔧 provide-workspace

A unified workspace manager for developing across all 13+ provide.io ecosystem packages with coordinated dependencies and shared virtual environments.

## Overview

`provide-workspace` is the official meta-repository that coordinates multi-package development across the entire provide.io ecosystem. It automates workspace setup, dependency installation, and provides a reference implementation of using wrknv for multi-repository coordination.

This workspace manager implements the meta-repository pattern where each package maintains its own git repository with independent history and releases, while the workspace provides a unified development environment with editable installs in a shared virtual environment.

## Key Capabilities

- **Single-Command Setup**: Clone all repositories and configure dependencies with three commands
- **Meta-Repository Pattern**: Coordinate 13+ packages while maintaining repository independence
- **Shared Virtual Environment**: Single `.venv` with all packages installed in editable mode
- **wrknv Integration**: Reference implementation demonstrating workspace management best practices
- **Coordinated Development**: Work across multiple packages with automatic cross-package imports
- **Bootstrap Scripts**: Automated setup, validation, and environment management

## Quick Start

```bash
git clone https://github.com/provide-io/provide-workspace.git
cd provide-workspace
./scripts/bootstrap.sh
./scripts/setup.sh
source .venv/bin/activate
```

## When to Use

**Use provide-workspace when:**
- ✅ New to the ecosystem (easiest onboarding)
- ✅ Cross-package development
- ✅ Building providers using multiple pyvider packages
- ✅ Contributing to multiple packages
- ✅ Testing integration between packages

**Use individual packages when:**
- ✅ Working on single package only
- ✅ Using published packages from PyPI
- ✅ Building applications on top of the framework

## Documentation

For detailed setup instructions, architecture overview, and development workflows, see the [Workspace documentation](https://foundry.provide.io/provide-workspace/).

## Repository

- **Repository**: [provide-workspace](https://github.com/provide-io/provide-workspace)
- **Meta-Repository**: Coordinates 13+ ecosystem packages
- **License**: Apache-2.0
