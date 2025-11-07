# pyvider

The core framework for building Terraform providers in Python with type safety, excellent developer experience, and full compatibility with Terraform's plugin protocol.

## Overview

`pyvider` is the heart of the Provide Foundry's Terraform provider development framework. It provides a Pythonic way to build Terraform providers with decorators, type safety, and automatic gRPC protocol handling.

### Key Features

- **🎯 Declarative Syntax**: Use decorators to define providers, resources, and data sources
- **🔒 Type Safety**: Full type annotations with runtime validation
- **⚡ Auto-Generated gRPC**: Automatic protocol buffer generation
- **🧪 Testing Framework**: Built-in testing utilities for provider development
- **📚 Rich Schema**: Comprehensive schema definition with validation
- **🔄 State Management**: Automatic state handling and migration support

## Installation

```bash
# Basic installation
uv add pyvider

# With all extras for full functionality
uv add pyvider[all]

# Development installation
uv add pyvider[dev]
```

## Quick Start

### Your First Provider

```python
from pyvider.providers import register_provider, BaseProvider
from pyvider.resources import register_resource, BaseResource
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.schema import Attribute, Block
from pyvider.cty import CtyString, CtyNumber, CtyBool

@register_provider("example")
class ExampleProvider(BaseProvider):
    """A simple example provider."""

    # Provider configuration
    api_url: CtyString = Attribute(
        description="API endpoint URL",
        required=True,
        sensitive=False
    )

    api_key: CtyString = Attribute(
        description="API authentication key",
        required=True,
        sensitive=True
    )

    def configure(self) -> None:
        """Configure the provider."""
        self.client = APIClient(
            base_url=self.api_url,
            api_key=self.api_key
        )

@register_resource("user")
class User(BaseResource):
    """User resource management."""

    # Required attributes
    username: CtyString = Attribute(
        description="Username for the user",
        required=True,
        plan_modifiers=["RequiresReplace"]
    )

    email: CtyString = Attribute(
        description="Email address",
        required=True,
        validators=["IsEmailAddress"]
    )

    # Optional attributes
    full_name: CtyString = Attribute(
        description="Full name of the user",
        required=False
    )

    active: CtyBool = Attribute(
        description="Whether the user is active",
        default=True
    )

    # Computed attributes
    id: CtyString = Attribute(
        description="Unique identifier",
        computed=True
    )

    created_at: CtyString = Attribute(
        description="Creation timestamp",
        computed=True
    )

    def create(self, config) -> dict:
        """Create a new user."""
        response = self.provider.client.create_user({
            "username": config.username,
            "email": config.email,
            "full_name": config.full_name,
            "active": config.active
        })

        return {
            "id": response["id"],
            "username": config.username,
            "email": config.email,
            "full_name": config.full_name or "",
            "active": config.active,
            "created_at": response["created_at"]
        }

    def read(self, state) -> dict | None:
        """Read user state."""
        try:
            user = self.provider.client.get_user(state["id"])
            return {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "full_name": user["full_name"],
                "active": user["active"],
                "created_at": user["created_at"]
            }
        except UserNotFoundError:
            return None  # Resource deleted externally

    def update(self, state, config) -> dict:
        """Update user."""
        updated_user = self.provider.client.update_user(
            state["id"],
            {
                "email": config.email,
                "full_name": config.full_name,
                "active": config.active
            }
        )

        return {
            "id": state["id"],
            "username": state["username"],  # Can't change
            "email": updated_user["email"],
            "full_name": updated_user["full_name"],
            "active": updated_user["active"],
            "created_at": state["created_at"]
        }

    def delete(self, state) -> None:
        """Delete user."""
        self.provider.client.delete_user(state["id"])

@register_data_source("users")
class Users(BaseDataSource):
    """Users data source."""

    # Filter attributes
    active_only: CtyBool = Attribute(
        description="Return only active users",
        default=False
    )

    # Computed attributes
    users: list[dict] = Attribute(
        description="List of users",
        computed=True
    )

    total_count: CtyNumber = Attribute(
        description="Total number of users",
        computed=True
    )

    def read(self, config) -> dict:
        """Read users data."""
        users = self.provider.client.list_users(
            active_only=config.active_only
        )

        return {
            "active_only": config.active_only,
            "users": users,
            "total_count": len(users)
        }
```

### Using the Provider

```hcl
# Configure the provider
provider "example" {
  api_url = "https://api.example.com"
  api_key = var.api_key
}

# Create a user
resource "example_user" "alice" {
  username  = "alice"
  email     = "alice@example.com"
  full_name = "Alice Smith"
  active    = true
}

# Read users data
data "example_users" "active" {
  active_only = true
}

# Output user information
output "alice_id" {
  value = example_user.alice.id
}

output "active_users_count" {
  value = data.example_users.active.total_count
}
```

## Core Concepts

### Providers

Providers are the entry point for your Terraform plugin:

```python
@provider
class MyProvider:
    """Provider for managing MyService resources."""

    # Configuration attributes
    endpoint: CtyString = Attribute(required=True)
    timeout: CtyNumber = Attribute(default=30)

    def configure(self) -> None:
        """Initialize provider with configuration."""
        self.client = MyServiceClient(
            endpoint=self.endpoint,
            timeout=self.timeout
        )

    def get_schema(self) -> ProviderSchema:
        """Define provider schema (auto-generated)."""
        # Automatically generated from attributes
        pass
```

### Resources

Resources represent infrastructure objects that can be created, read, updated, and deleted:

```python
@resource
class Database:
    """Database resource."""

    # Required configuration
    name: CtyString = Attribute(required=True)
    engine: CtyString = Attribute(required=True)

    # Optional configuration
    size: CtyString = Attribute(default="small")

    # Computed values
    id: CtyString = Attribute(computed=True)
    endpoint: CtyString = Attribute(computed=True)

    # Lifecycle methods
    def create(self, config) -> dict:
        """Create database."""
        db = self.provider.client.create_database(
            name=config.name,
            engine=config.engine,
            size=config.size
        )
        return {"id": db.id, "endpoint": db.endpoint, **config}

    def read(self, state) -> dict | None:
        """Read database state."""
        try:
            db = self.provider.client.get_database(state["id"])
            return {"id": db.id, "endpoint": db.endpoint, **state}
        except DatabaseNotFound:
            return None

    def update(self, state, config) -> dict:
        """Update database."""
        db = self.provider.client.update_database(
            state["id"],
            size=config.size
        )
        return {"id": state["id"], "endpoint": db.endpoint, **config}

    def delete(self, state) -> None:
        """Delete database."""
        self.provider.client.delete_database(state["id"])
```

### Data Sources

Data sources provide read-only access to external data:

```python
@data_source
class AvailableZones:
    """Available zones data source."""

    # Filter configuration
    region: CtyString = Attribute(required=True)

    # Computed results
    zones: list[str] = Attribute(computed=True)
    count: CtyNumber = Attribute(computed=True)

    def read(self, config) -> dict:
        """Read available zones."""
        zones = self.provider.client.get_zones(config.region)
        return {
            "region": config.region,
            "zones": zones,
            "count": len(zones)
        }
```

## Schema System

### Attributes

Define resource and data source attributes with rich metadata:

```python
from pyvider.schema import Attribute

# Basic attribute
name: CtyString = Attribute(
    description="Resource name",
    required=True
)

# Optional attribute with default
port: CtyNumber = Attribute(
    description="Port number",
    default=8080
)

# Computed attribute
id: CtyString = Attribute(
    description="Unique identifier",
    computed=True
)

# Sensitive attribute
password: CtyString = Attribute(
    description="Database password",
    required=True,
    sensitive=True
)

# Attribute with validation
email: CtyString = Attribute(
    description="Email address",
    required=True,
    validators=["IsEmailAddress"]
)

# Attribute with plan modifiers
key: CtyString = Attribute(
    description="Encryption key",
    required=True,
    plan_modifiers=["RequiresReplace"]
)
```

### Blocks

Define nested configuration blocks:

```python
from pyvider.schema import Block, Attribute

@Block
class DatabaseConfig:
    """Database configuration block."""

    engine: CtyString = Attribute(required=True)
    version: CtyString = Attribute(required=True)
    parameters: dict = Attribute(default={})

@resource
class Database:
    """Database with configuration block."""

    name: CtyString = Attribute(required=True)
    config: DatabaseConfig = Block(required=True)

    def create(self, config) -> dict:
        """Create database with nested configuration."""
        db = self.provider.client.create_database(
            name=config.name,
            engine=config.config.engine,
            version=config.config.version,
            parameters=config.config.parameters
        )
        return {"id": db.id, **config}
```

### Lists and Sets

Handle collections of attributes:

```python
# List of strings
tags: list[CtyString] = Attribute(
    description="Resource tags",
    default=[]
)

# Set of complex objects
rules: set[SecurityRule] = Attribute(
    description="Security rules",
    default=set()
)

# Map of attributes
metadata: dict[str, CtyString] = Attribute(
    description="Resource metadata",
    default={}
)
```

## Type System Integration

Pyvider uses the CTY type system for full Terraform compatibility:

```python
from pyvider.cty import (
    CtyString, CtyNumber, CtyBool,
    CtyList, CtySet, CtyMap, CtyObject
)

# Primitive types
name: CtyString
count: CtyNumber
enabled: CtyBool

# Collection types
tags: CtyList[CtyString]
unique_tags: CtySet[CtyString]
labels: CtyMap[CtyString]

# Complex object type
config: CtyObject[{
    "database": CtyString,
    "port": CtyNumber,
    "ssl": CtyBool
}]
```

## Error Handling

Comprehensive error handling with rich context:

```python
from pyvider.errors import (
    ProviderError,
    ResourceError,
    ValidationError,
    ConfigurationError
)

@resource
class Database:
    def create(self, config) -> dict:
        """Create database with error handling."""
        try:
            if not self._validate_name(config.name):
                raise ValidationError(
                    "Invalid database name",
                    attribute="name",
                    value=config.name,
                    suggestion="Use alphanumeric characters only"
                )

            db = self.provider.client.create_database(config.name)
            return {"id": db.id, **config}

        except APIError as e:
            raise ResourceError(
                f"Failed to create database: {e}",
                operation="create",
                resource_type="database",
                details={"api_error": str(e)}
            ) from e

    def _validate_name(self, name: str) -> bool:
        """Validate database name."""
        return name.isalnum() and len(name) <= 32
```

## Testing Framework

Built-in testing utilities for provider development:

```python
import pytest
from pyvider.testing import ProviderTest, MockClient

class TestUserResource(ProviderTest):
    """Test user resource."""

    def setup_method(self):
        """Set up test environment."""
        self.mock_client = MockClient()
        self.provider = ExampleProvider(
            api_url="https://test.example.com",
            api_key="test-key"
        )
        self.provider.client = self.mock_client

    def test_user_creation(self):
        """Test user creation."""
        # Configure mock responses
        self.mock_client.expect_call(
            "create_user",
            args={
                "username": "alice",
                "email": "alice@example.com",
                "active": True
            },
            returns={
                "id": "user-123",
                "created_at": "2024-01-01T00:00:00Z"
            }
        )

        # Test resource creation
        user = User(provider=self.provider)
        config = UserConfig(
            username="alice",
            email="alice@example.com",
            active=True
        )

        result = user.create(config)

        assert result["id"] == "user-123"
        assert result["username"] == "alice"
        assert result["email"] == "alice@example.com"
        assert result["active"] is True
        assert result["created_at"] == "2024-01-01T00:00:00Z"

    def test_user_not_found(self):
        """Test handling of missing user."""
        self.mock_client.expect_call(
            "get_user",
            args="user-123",
            raises=UserNotFoundError("User not found")
        )

        user = User(provider=self.provider)
        state = {"id": "user-123"}

        result = user.read(state)
        assert result is None  # Resource deleted externally
```

## Plugin Protocol

Pyvider automatically handles the Terraform plugin protocol:

```python
# Entry point for your provider plugin
def main():
    """Main entry point for provider plugin."""
    from pyvider.plugin import serve_provider

    provider = ExampleProvider()
    serve_provider(provider)

if __name__ == "__main__":
    main()
```

## Advanced Features

### Custom Validators

Create custom attribute validators:

```python
from pyvider.validators import Validator

class IPAddressValidator(Validator):
    """Validate IP address format."""

    def validate(self, value: str) -> bool:
        """Validate IP address."""
        try:
            ipaddress.ip_address(value)
            return True
        except ValueError:
            return False

    def error_message(self, value: str) -> str:
        """Error message for invalid IP."""
        return f"'{value}' is not a valid IP address"

# Use in attribute definition
ip_address: CtyString = Attribute(
    description="Server IP address",
    required=True,
    validators=[IPAddressValidator()]
)
```

### Plan Modifiers

Customize resource planning behavior:

```python
from pyvider.plan import PlanModifier

class DefaultFromEnvironment(PlanModifier):
    """Set default value from environment variable."""

    def __init__(self, env_var: str):
        self.env_var = env_var

    def modify_plan(self, plan, config, state):
        """Set default from environment."""
        if plan.attribute_value is None:
            plan.attribute_value = os.getenv(self.env_var)

# Use in attribute definition
api_key: CtyString = Attribute(
    description="API key",
    plan_modifiers=[DefaultFromEnvironment("API_KEY")]
)
```

### State Migration

Handle schema changes with state migration:

```python
@resource
class Database:
    """Database resource with state migration."""

    # Schema version tracking
    __schema_version__ = 2

    def migrate_state(self, state: dict, from_version: int) -> dict:
        """Migrate state between schema versions."""
        if from_version == 1:
            # Migration from v1 to v2
            if "size" in state:
                # Convert old size enum to new size format
                size_mapping = {
                    "small": "db.t3.micro",
                    "medium": "db.t3.small",
                    "large": "db.t3.medium"
                }
                state["instance_type"] = size_mapping.get(
                    state.pop("size"), "db.t3.micro"
                )

        return state
```

## Performance Considerations

### Lazy Loading

Resources and data sources are loaded on-demand:

```python
# Provider discovery is lazy
@provider
class OptimizedProvider:
    """Provider with optimized loading."""

    def __init__(self):
        self._client = None

    @property
    def client(self):
        """Lazy-loaded client."""
        if self._client is None:
            self._client = self._create_client()
        return self._client

    def _create_client(self):
        """Create API client."""
        return APIClient(self.api_url, self.api_key)
```

### Batch Operations

Optimize API calls with batching:

```python
@resource
class BatchableResource:
    """Resource with batch operations."""

    def create_batch(self, configs: list) -> list[dict]:
        """Create multiple resources in batch."""
        return self.provider.client.create_batch(configs)

    def read_batch(self, ids: list[str]) -> list[dict]:
        """Read multiple resources in batch."""
        return self.provider.client.read_batch(ids)
```

## Best Practices

1. **Use type hints everywhere** - Full type annotations improve development experience
2. **Validate inputs early** - Check configuration in validators, not lifecycle methods
3. **Handle errors gracefully** - Provide clear error messages with context
4. **Test thoroughly** - Use the testing framework for comprehensive coverage
5. **Document schemas** - Clear descriptions help users understand attributes
6. **Follow Terraform conventions** - Use standard Terraform patterns and naming
7. **Optimize API calls** - Batch operations and cache responses when possible

## Examples

For complete examples, see:
- [Simple Provider Example](https://github.com/provide-io/pyvider-examples/tree/main/simple)
- [Complex Provider Example](https://github.com/provide-io/pyvider-examples/tree/main/complex)
- [Testing Examples](https://github.com/provide-io/pyvider-examples/tree/main/testing)

## Related Packages

- **[pyvider-cty](pyvider-cty.md)**: CTY type system implementation
- **[pyvider-hcl](pyvider-hcl.md)**: HCL configuration parsing
- **[pyvider-rpcplugin](pyvider-rpcplugin.md)**: gRPC plugin protocol
- **[pyvider-components](pyvider-components.md)**: Standard component library

---

Pyvider makes building Terraform providers in Python both powerful and enjoyable. With its declarative syntax, type safety, and comprehensive tooling, you can focus on your provider's logic rather than the underlying protocol complexity.