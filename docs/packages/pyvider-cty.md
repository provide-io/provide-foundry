# 🌊🪢 pyvider-cty

Pure-Python implementation of the go-cty type system with strong validation, serialization, and Terraform interoperability.

## Overview

`pyvider-cty` provides Python bindings for Terraform's CTY (Configuration Type System), enabling type-safe data handling for Terraform provider implementations. It implements the complete CTY type system including primitives, collections, objects, and dynamic types with full serialization and validation support.

This package is essential for Pyvider providers to correctly handle Terraform configuration values and state data with the same type semantics as Go-based providers.

## Key Capabilities

- **Complete CTY Type System**: Primitives, collections (list, set, map), objects, and dynamic types
- **Type Conversion**: Bidirectional conversion between Python and CTY types
- **Serialization**: JSON and MessagePack serialization with type preservation
- **Schema Validation**: Type checking and constraint validation
- **Value Operations**: Type-safe operations on CTY values
- **Terraform Compatibility**: Full interoperability with Terraform's type system

## Installation

```bash
uv add pyvider-cty
```

## Documentation

For detailed API reference, type system documentation, and usage examples, see the [Pyvider CTY documentation](https://foundry.provide.io/pyvider-cty/).

## Repository

- **Repository**: [pyvider-cty](https://github.com/provide-io/pyvider-cty)
- **Package**: `pyvider-cty` on PyPI
- **License**: Apache-2.0
