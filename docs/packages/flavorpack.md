# 🌶️📦 flavorpack

Flavor Pack packaging system implementing Progressive Secure Package Format (PSPF/2025).

## Overview

`flavorpack` is a secure packaging system that creates self-contained executable packages (`.psp` files) for distributing Python applications and Terraform providers. It implements the PSPF/2025 specification, providing signature verification, dependency bundling, and cross-platform distribution capabilities.

The package format is designed for secure distribution of executable bundles with built-in integrity verification and support for multiple target platforms.

## Key Capabilities

- **Self-Contained Packages**: Single-file executables with all dependencies bundled
- **PSPF/2025 Specification**: Implements Progressive Secure Package Format standard
- **Signature Verification**: Ed25519-based package signing and verification
- **Cross-Platform Support**: Package creation and execution across Linux, macOS, and Windows
- **Terraform Provider Packaging**: Specialized support for provider distribution
- **Bundle Optimization**: Efficient compression and runtime loading

## Installation

```bash
uv tool install flavorpack
```

## Documentation

For detailed packaging guides, CLI reference, and format specification, see the [FlavorPack documentation](https://foundry.provide.io/flavorpack/).

## Repository

- **Repository**: [flavorpack](https://github.com/provide-io/flavorpack)
- **Package**: `flavorpack` on PyPI
- **License**: Apache-2.0
