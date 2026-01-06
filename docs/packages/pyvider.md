# 🐍🏗️ pyvider

Python Terraform Provider Framework.

## Overview

`pyvider` is the core framework for building Terraform providers in Python. It implements the Terraform plugin protocol, allowing developers to create providers using Python instead of Go, with support for resources, data sources, provider configuration, and state management.

The framework handles the complexity of the Terraform plugin protocol (both version 5 and 6), allowing you to focus on implementing your provider's business logic using familiar Python patterns and types.

## Key Capabilities

- **Terraform Plugin Protocol**: Full implementation of Terraform's gRPC plugin protocol (v5 and v6)
- **Resource & Data Source Support**: Define resources and data sources with Python classes
- **Type-Safe Schemas**: Schema definition with type validation using Pydantic models
- **State Management**: Automatic state handling and migration support
- **Async Support**: Native async/await for I/O-bound operations
- **Provider Configuration**: Structured provider configuration with validation

## Installation

```bash
# Basic installation
uv add pyvider

# With all extras
uv add pyvider[all]
```

## Documentation

For detailed guides, API reference, and provider development tutorials, see the [Pyvider documentation](https://foundry.provide.io/pyvider/).

## Repository

- **Repository**: [pyvider](https://github.com/provide-io/pyvider)
- **Package**: `pyvider` on PyPI
- **License**: Apache-2.0
