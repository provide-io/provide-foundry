# 🧪✅ provide-testkit

Testing utilities and fixtures for the provide ecosystem.

## Overview

`provide-testkit` provides pytest fixtures, mocking utilities, and testing helpers for testing applications built with the provide.io ecosystem. It offers domain-organized fixtures for common testing scenarios including file operations, network testing, process management, and cryptographic testing.

The testkit is designed to integrate seamlessly with pytest and provides both synchronous and asynchronous testing capabilities.

## Key Capabilities

- **Pytest Fixtures**: Pre-built fixtures for common testing scenarios
- **Mock Utilities**: Mocking helpers for Terraform plugin protocol and RPC communication
- **Async Support**: Fixtures and utilities for testing async/await code
- **Domain Organization**: Fixtures organized by testing domain (file, transport, crypto, process)
- **Provider Testing**: Specialized utilities for testing Terraform provider implementations

## Installation

```bash
# Basic installation
uv add provide-testkit

# With optional extras for specific domains
uv add provide-testkit[transport]  # Network testing
uv add provide-testkit[crypto]     # Cryptographic testing
uv add provide-testkit[process]    # Process testing
uv add provide-testkit[all]        # All extras
```

## Documentation

For detailed API documentation, fixture reference, and testing guides, see the [TestKit documentation](https://foundry.provide.io/provide-testkit/).

## Repository

- **Repository**: [provide-testkit](https://github.com/provide-io/provide-testkit)
- **Package**: `provide-testkit` on PyPI
- **License**: Apache-2.0
