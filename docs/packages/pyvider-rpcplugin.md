# 🔌📞 pyvider-rpcplugin

Pyvider RPC Plugin.

## Overview

`pyvider-rpcplugin` implements Terraform's gRPC plugin protocol for Pyvider providers. It handles the low-level communication between Terraform CLI and Python-based providers, including protocol negotiation, message serialization, and lifecycle management.

This package is used internally by Pyvider to enable providers to communicate with Terraform/OpenTofu using the standard plugin protocol.

## Key Capabilities

- **gRPC Plugin Protocol**: Implementation of Terraform plugin protocol versions 5 and 6
- **Protocol Negotiation**: Automatic version negotiation with Terraform/OpenTofu
- **Message Handling**: Serialization and deserialization of plugin protocol messages
- **Lifecycle Management**: Plugin startup, shutdown, and health checking
- **Transport Support**: Unix socket and TCP transport for plugin communication
- **Async Support**: Asynchronous message handling for concurrent operations

## Installation

```bash
uv add pyvider-rpcplugin
```

## Documentation

For protocol details, integration guides, and API reference, see the [Pyvider RPC Plugin documentation](https://foundry.provide.io/pyvider-rpcplugin/).

## Repository

- **Repository**: [pyvider-rpcplugin](https://github.com/provide-io/pyvider-rpcplugin)
- **Package**: `pyvider-rpcplugin` on PyPI
- **License**: Apache-2.0
