# 🧱🏗️ provide-foundation

A comprehensive Python foundation library for building robust applications with structured logging, CLI framework, configuration management, and essential building blocks.

## Overview

`provide-foundation` serves as the core infrastructure layer for the entire provide.io ecosystem. It provides essential cross-cutting concerns that all framework and tool packages depend on, including structured logging with OpenTelemetry integration, type-safe configuration management, and common utilities for building production-focused Python applications.

This package is designed to be lightweight yet comprehensive, offering the fundamental capabilities needed for telemetry, observability, and application configuration without imposing heavy dependencies or opinions on application architecture.

## Key Capabilities

- **Structured Logging**: Context-aware logging with automatic trace ID propagation
- **OpenTelemetry Integration**: Distributed tracing and telemetry for observability
- **Configuration Management**: Type-safe configuration with Pydantic and environment variable support
- **CLI Framework**: Command-line interface utilities and application scaffolding
- **Validation Utilities**: Common validation patterns and error handling
- **Platform Detection**: Cross-platform compatibility helpers

## Installation

```bash
# Basic installation
uv add provide-foundation

# With all optional dependencies
uv add provide-foundation[all]
```

## Documentation

For detailed API documentation, usage examples, and guides, see the [Foundation documentation](https://foundry.provide.io/provide-foundation/).

## Repository

- **Repository**: [provide-foundation](https://github.com/provide-io/provide-foundation)
- **Package**: `provide-foundation` on PyPI
- **License**: Apache-2.0
