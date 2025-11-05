# Provider Development Guide

This guide covers the complete process of developing Terraform providers using the Pyvider framework within the provide.foundation ecosystem.

## Overview

Developing Terraform providers with Pyvider involves understanding the provider lifecycle, implementing resources and data sources, and following best practices for maintainable, production-ready providers.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Understanding of Terraform concepts
- Familiarity with the target API or service
- Development environment setup (see [Installation Guide](installation.md))

### Project Setup

```bash
# Create new provider project
mkdir terraform-provider-myservice
cd terraform-provider-myservice

# Initialize with provide-foundry template
plating create python-terraform-provider \
  --name myservice \
  --api-base-url https://api.myservice.com \
  --author "Your Name"

# Install dependencies
uv sync --extra dev
```

## Provider Architecture

### Basic Provider Structure

```python
from pyvider import provider, resource, data_source
from pyvider.schema import Attribute, Block
from pyvider.cty import CtyString, CtyNumber, CtyBool
from provide.foundation import logger

@provider
class MyServiceProvider:
    """Terraform provider for MyService API."""

    # Provider configuration
    api_url: CtyString = Attribute(
        description="MyService API base URL",
        required=True,
        default="https://api.myservice.com"
    )

    api_key: CtyString = Attribute(
        description="API key for authentication",
        required=True,
        sensitive=True
    )

    def configure(self, config):
        """Configure the provider client."""
        self.client = MyServiceClient(
            base_url=config.api_url,
            api_key=config.api_key
        )
        logger.info("Provider configured", extra={
            "api_url": config.api_url
        })
```

### Resource Implementation

```python
@resource("myservice_server")
class ServerResource:
    """Manages a MyService server instance."""

    # Required attributes
    name: CtyString = Attribute(
        description="Server name",
        required=True
    )

    # Optional attributes with defaults
    size: CtyString = Attribute(
        description="Server size",
        default="small",
        validation=lambda x: x in ["small", "medium", "large"]
    )

    region: CtyString = Attribute(
        description="Deployment region",
        required=True
    )

    # Computed attributes
    id: CtyString = Attribute(
        description="Server ID",
        computed=True
    )

    status: CtyString = Attribute(
        description="Server status",
        computed=True
    )

    created_at: CtyString = Attribute(
        description="Creation timestamp",
        computed=True
    )

    def create(self, config):
        """Create a new server."""
        logger.info("Creating server", extra={
            "name": config.name,
            "size": config.size,
            "region": config.region
        })

        response = self.provider.client.create_server({
            "name": config.name,
            "size": config.size,
            "region": config.region
        })

        # Set computed values
        self.id = response["id"]
        self.status = response["status"]
        self.created_at = response["created_at"]

        return self

    def read(self, config):
        """Read server state."""
        if not self.id:
            return None

        try:
            response = self.provider.client.get_server(self.id)

            # Update state from API
            self.name = response["name"]
            self.size = response["size"]
            self.region = response["region"]
            self.status = response["status"]
            self.created_at = response["created_at"]

            return self
        except NotFoundError:
            # Resource was deleted outside Terraform
            return None

    def update(self, config):
        """Update server configuration."""
        logger.info("Updating server", extra={
            "id": self.id,
            "name": config.name
        })

        response = self.provider.client.update_server(self.id, {
            "name": config.name,
            "size": config.size
        })

        # Update computed values
        self.status = response["status"]

        return self

    def delete(self, config):
        """Delete the server."""
        logger.info("Deleting server", extra={
            "id": self.id
        })

        self.provider.client.delete_server(self.id)
```

### Data Source Implementation

```python
@data_source("myservice_image")
class ImageDataSource:
    """Fetch information about available server images."""

    # Filter attributes
    name_filter: CtyString = Attribute(
        description="Filter images by name pattern",
        required=False
    )

    os_type: CtyString = Attribute(
        description="Operating system type",
        required=False,
        validation=lambda x: x in ["linux", "windows"]
    )

    # Computed attributes
    images: CtyList = Attribute(
        description="List of matching images",
        computed=True
    )

    def read(self, config):
        """Fetch image data."""
        filters = {}
        if config.name_filter:
            filters["name"] = config.name_filter
        if config.os_type:
            filters["os_type"] = config.os_type

        response = self.provider.client.list_images(filters)

        self.images = [
            {
                "id": img["id"],
                "name": img["name"],
                "os_type": img["os_type"],
                "version": img["version"]
            }
            for img in response["images"]
        ]

        return self
```

## Advanced Patterns

### Complex Schema Structures

```python
@resource("myservice_application")
class ApplicationResource:
    """Application with complex configuration."""

    # Nested block configuration
    database: Block = Block(
        description="Database configuration",
        required=False,
        max_items=1,
        attributes={
            "host": CtyString(required=True),
            "port": CtyNumber(default=5432),
            "name": CtyString(required=True),
            "ssl_enabled": CtyBool(default=True)
        }
    )

    # Repeated blocks
    environment_variables: Block = Block(
        description="Environment variables",
        required=False,
        attributes={
            "name": CtyString(required=True),
            "value": CtyString(required=True),
            "sensitive": CtyBool(default=False)
        }
    )
```

### State Migration

```python
class ServerResource:
    """Server resource with state migration."""

    # Schema version for migration
    __schema_version__ = 2

    def migrate_state(self, old_version: int, old_state: dict) -> dict:
        """Migrate state from older schema versions."""
        if old_version == 1:
            # v1 -> v2: rename 'instance_type' to 'size'
            if "instance_type" in old_state:
                old_state["size"] = old_state.pop("instance_type")

        return old_state
```

### Custom Validation

```python
from pyvider.validation import ValidationError

@resource("myservice_database")
class DatabaseResource:
    """Database with custom validation."""

    name: CtyString = Attribute(required=True)
    backup_retention_days: CtyNumber = Attribute(default=7)

    def validate(self, config):
        """Custom validation logic."""
        if not config.name.startswith("db-"):
            raise ValidationError(
                "Database name must start with 'db-'",
                attribute="name"
            )

        if config.backup_retention_days < 1 or config.backup_retention_days > 365:
            raise ValidationError(
                "Backup retention must be between 1 and 365 days",
                attribute="backup_retention_days"
            )
```

## Error Handling

### Robust Error Handling

```python
from pyvider.exceptions import ProviderError, ResourceError

class ServerResource:
    """Server resource with comprehensive error handling."""

    def create(self, config):
        try:
            response = self.provider.client.create_server(config)
            return self._update_from_response(response)

        except APIError as e:
            if e.status_code == 409:
                raise ResourceError(
                    f"Server with name '{config.name}' already exists",
                    retryable=False
                )
            elif e.status_code == 429:
                raise ResourceError(
                    "Rate limit exceeded, please retry",
                    retryable=True
                )
            else:
                raise ProviderError(f"API error: {e.message}")

        except NetworkError as e:
            raise ProviderError(
                f"Network error: {e.message}",
                retryable=True
            )
```

## Testing

### Unit Testing

```python
import pytest
from unittest.mock import Mock
from provide.testkit import TestCase

class TestServerResource(TestCase):
    """Test server resource functionality."""

    def setUp(self):
        self.provider = Mock()
        self.provider.client = Mock()
        self.resource = ServerResource(provider=self.provider)

    def test_create_server(self):
        """Test server creation."""
        # Mock API response
        self.provider.client.create_server.return_value = {
            "id": "srv-123",
            "name": "test-server",
            "status": "creating",
            "created_at": "2023-01-01T00:00:00Z"
        }

        # Create server
        config = Mock()
        config.name = "test-server"
        config.size = "small"
        config.region = "us-east-1"

        result = self.resource.create(config)

        # Verify API call
        self.provider.client.create_server.assert_called_once_with({
            "name": "test-server",
            "size": "small",
            "region": "us-east-1"
        })

        # Verify state
        self.assertEqual(result.id, "srv-123")
        self.assertEqual(result.status, "creating")
```

### Integration Testing

```python
from provide.testkit import IntegrationTestCase

class TestServerResourceIntegration(IntegrationTestCase):
    """Integration tests with real API."""

    def setUp(self):
        self.provider = self.create_test_provider()

    def test_server_lifecycle(self):
        """Test complete server lifecycle."""
        # Create server
        server = self.create_resource("myservice_server", {
            "name": "integration-test-server",
            "size": "small",
            "region": "us-east-1"
        })

        self.assertIsNotNone(server.id)
        self.assertEqual(server.name, "integration-test-server")

        # Update server
        updated = self.update_resource(server, {
            "name": "updated-server-name"
        })

        self.assertEqual(updated.name, "updated-server-name")

        # Clean up
        self.destroy_resource(server)
```

## Best Practices

### Configuration Management

- Use Foundation's configuration system for consistent settings
- Implement proper environment variable handling
- Support multiple authentication methods
- Validate configuration early and clearly

### State Management

- Always implement proper state refresh
- Handle resources deleted outside Terraform gracefully
- Use appropriate computed attributes
- Implement state migration for schema changes

### Error Handling

- Provide clear, actionable error messages
- Distinguish between retryable and non-retryable errors
- Log sufficient context for debugging
- Handle API rate limits and timeouts gracefully

### Performance

- Implement efficient bulk operations where possible
- Use appropriate caching strategies
- Minimize API calls during planning
- Implement proper pagination for list operations

## Debugging

### Enable Debug Logging

```bash
export TF_LOG=DEBUG
export PYVIDER_LOG_LEVEL=DEBUG
terraform apply
```

### Provider Development Tools

```python
# Enable development mode
from pyvider.dev import enable_debug_mode
enable_debug_mode()

# Mock API responses for testing
from pyvider.testing import mock_api_response
with mock_api_response("create_server", {"id": "test-123"}):
    # Run provider operations
    pass
```

## Related Documentation

- **[Testing Guide](testing.md)** - Comprehensive testing strategies
- **[Packaging Guide](packaging.md)** - Building and distributing providers
- **[API Reference](../pyvider/reference/)** - Complete Pyvider API documentation

## Community Resources

- **Provider Registry**: Submit your provider to the Terraform Registry
- **Community Forum**: Get help and share experiences
- **Contributing**: Contribute to the Pyvider framework itself