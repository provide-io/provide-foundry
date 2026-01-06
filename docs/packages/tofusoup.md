# 🥣🔬 tofusoup

Cross-language conformance test suite for OpenTofu tooling.

## Overview

`tofusoup` provides a conformance testing framework for validating Terraform and OpenTofu provider implementations across different languages and implementations. It ensures that providers behave correctly and consistently, regardless of whether they're written in Go, Python, or other languages.

This testing framework is essential for verifying that Python-based Pyvider providers maintain compatibility with the Terraform/OpenTofu ecosystem standards.

## Key Capabilities

- **Conformance Testing**: Validate provider behavior against Terraform specifications
- **Cross-Language Support**: Test providers regardless of implementation language
- **Protocol Compliance**: Verify correct implementation of plugin protocol
- **Behavior Validation**: Ensure consistent provider behavior across implementations
- **Test Suites**: Pre-built test suites for common provider scenarios
- **Custom Test Definition**: Define custom conformance tests for specific requirements

## Installation

```bash
uv tool install tofusoup
```

## Documentation

For test suite reference, testing guides, and conformance specifications, see the [TofuSoup documentation](https://foundry.provide.io/tofusoup/).

## Repository

- **Repository**: [tofusoup](https://github.com/provide-io/tofusoup)
- **Package**: `tofusoup` on PyPI
- **License**: Apache-2.0
