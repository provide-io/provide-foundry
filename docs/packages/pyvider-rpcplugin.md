# pyvider-rpcplugin

Enterprise-grade RPC plugin framework for Python applications with Foundation integration, security-first architecture, and modern async patterns.

## Overview

`pyvider-rpcplugin` provides everything you need to create production-ready microservices and plugin ecosystems. Part of the provide.foundation ecosystem, it seamlessly integrates with Foundation's configuration, logging, and development toolchain for consistent, unified application architecture.

### Key Features

#### ⚡ **Performance-First**
- **Async-native**: Full `asyncio` integration for maximum concurrency
- **Efficient transports**: Unix domain sockets for local IPC and TCP for network communication
- **Optimized serialization**: Protocol Buffers with streaming support
- **High throughput**: Designed for high-volume, low-latency plugin communication

#### 🔒 **Security-Focused**
- **Built-in mTLS**: Mutual TLS authentication with certificate management utilities
- **Process isolation**: Plugins run as separate processes for enhanced stability
- **Transport encryption**: Secure communication over any network when mTLS is enabled
- **Magic cookie validation**: Handshake verification for trusted connections

#### 🛠️ **Developer Experience**
- **Modern Python**: Python 3.11+ with native type annotations (`dict`, `list`, union operators)
- **Foundation ecosystem**: Unified configuration, logging, and toolchain with other Foundation projects
- **Factory functions**: `plugin_server()` and `plugin_client()` for rapid development
- **Rich error handling**: Detailed exceptions with contextual information and guidance

#### 🏗️ **Production Ready**
- **Foundation configuration**: `PLUGIN_*` environment variables with validation and type safety
- **Structured logging**: Foundation's logging system with context preservation and filtering
- **Health checks**: gRPC Health Checking Protocol with custom status reporting
- **Rate limiting**: Token bucket implementation with per-client and global policies

## Installation

```bash
# Basic installation
uv add pyvider-rpcplugin

# With all extras for full functionality
uv add pyvider-rpcplugin[all]

# Development installation
uv add pyvider-rpcplugin[dev]
```

## Quick Start

### Your First Plugin

Create a complete echo service with modern Python patterns:

```python
import asyncio
from pyvider.rpcplugin import plugin_server, configure
from pyvider.rpcplugin.protocol.base import RPCPluginProtocol
from provide.foundation import logger

# Configure for your environment
configure(
    magic_cookie="my-echo-plugin",
    auto_mtls=False,  # Enable for production
    handshake_timeout=5.0
)

class EchoService:
    """Echo service with Foundation logging."""

    async def echo(self, message: str) -> str:
        # Foundation logger with structured context
        logger.info("Processing echo request", extra={
            "message": message,
            "service": "echo"
        })
        return f"Echo: {message}"

class EchoProtocol(RPCPluginProtocol):
    """Protocol implementation for echo service."""

    async def get_grpc_descriptors(self) -> tuple[object, str]:
        import echo_pb2_grpc
        return echo_pb2_grpc, "echo.EchoService"

    async def add_to_server(self, server: object, handler: object) -> None:
        from echo_pb2_grpc import add_EchoServiceServicer_to_server
        add_EchoServiceServicer_to_server(handler, server)

async def main() -> None:
    """Launch the echo plugin server."""
    server = plugin_server(
        protocol=EchoProtocol(),
        handler=EchoService()
    )
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
```

### Client Usage

Connect from a client with automatic plugin management:

```python
import asyncio
import sys
from pathlib import Path
from pyvider.rpcplugin import plugin_client, configure
from provide.foundation import logger

# Configure client environment
configure(
    magic_cookie="my-echo-plugin",
    handshake_timeout=10.0,
    connection_timeout=5.0
)

async def main() -> None:
    """Client automatically launches and manages plugin process."""
    # Plugin command - client handles process lifecycle
    plugin_path = Path(__file__).parent / "echo_server.py"
    plugin_command = [sys.executable, str(plugin_path)]

    # Environment passed automatically via PLUGIN_* variables
    async with plugin_client(command=plugin_command) as client:
        # Use typed gRPC stub
        from echo_pb2_grpc import EchoServiceStub
        from echo_pb2 import EchoRequest

        stub = EchoServiceStub(client.grpc_channel)
        request = EchoRequest(message="Hello, Foundation!")

        response = await stub.Echo(request)
        logger.info("Plugin response received", extra={
            "request_message": request.message,
            "response_reply": response.reply,
            "client_id": "echo-client"
        })

if __name__ == "__main__":
    asyncio.run(main())
```

## Architecture

Pyvider RPC Plugin follows a clean architecture pattern with these core components:

- **🚀 Server**: High-performance async gRPC server with security and monitoring
- **📱 Client**: Type-safe client with connection management and retry logic
- **🌐 Transports**: Unix domain sockets and TCP with automatic transport negotiation
- **📋 Protocols**: gRPC-based protocols with Protocol Buffer serialization
- **🔐 Security**: mTLS encryption, certificate management, and process isolation
- **⚙️ Configuration**: Foundation-based config with environment variable support

## Use Cases

### **Plugin Architectures**
Build extensible applications where plugins run as separate processes for enhanced stability and security.

### **Microservices Communication**
High-performance inter-service communication with built-in security and monitoring.

### **Foundation Ecosystem Integration**
Seamless integration with other provide.foundation projects for unified application architecture.

### **Enterprise Applications**
Production-ready plugin systems with comprehensive security, monitoring, and configuration management.

## Related Documentation

- **[API Reference](../pyvider-rpcplugin/reference/)** - Complete API documentation
- **[Foundation Integration](../foundry/index.md)** - Foundation ecosystem patterns
- **[Security Guide](../guides/security.md)** - Security configuration and best practices

## Repository

- **Repository**: [pyvider-rpcplugin](https://github.com/provide-io/pyvider-rpcplugin)
- **Package**: `pyvider-rpcplugin` on PyPI
- **License**: MIT