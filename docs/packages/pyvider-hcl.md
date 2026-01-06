# 📄⚙️ pyvider-hcl

A wrapper for python-hcl2 integrating with Pyvider's Cty type system.

## Overview

`pyvider-hcl` provides HCL (HashiCorp Configuration Language) parsing capabilities for Pyvider-based Terraform providers. It wraps the python-hcl2 parser and integrates with Pyvider's CTY type system to enable parsing and processing of HCL configuration files with proper type handling.

This package allows providers to parse HCL configuration and convert it to CTY-typed values for use within the provider implementation.

## Key Capabilities

- **HCL Parsing**: Parse HCL configuration files and strings
- **CTY Integration**: Automatic conversion of parsed HCL to CTY types
- **python-hcl2 Wrapper**: Builds on the established python-hcl2 library
- **Type-Safe Processing**: Leverages Pyvider's type system for configuration handling
- **Expression Support**: Handle HCL expressions and interpolations

## Installation

```bash
uv add pyvider-hcl
```

## Documentation

For parsing guides, API reference, and integration examples, see the [Pyvider HCL documentation](https://foundry.provide.io/pyvider-hcl/).

## Repository

- **Repository**: [pyvider-hcl](https://github.com/provide-io/pyvider-hcl)
- **Package**: `pyvider-hcl` on PyPI
- **License**: Apache-2.0
