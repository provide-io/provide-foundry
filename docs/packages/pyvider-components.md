# pyvider-components

Standard reusable provider components for building Terraform providers with the Pyvider framework in the provide.foundation ecosystem.

## Overview

`pyvider-components` provides a comprehensive library of pre-built, reusable components for Terraform provider development. These components encapsulate common patterns, reduce boilerplate code, and ensure consistency across provider implementations built with the Pyvider framework.

### Key Features

#### 🧩 **Reusable Components**
- **Standard resources**: Common resource types with built-in best practices
- **Data sources**: Pre-configured data source components with validation
- **Provider schemas**: Standardized provider configuration schemas
- **Authentication handlers**: OAuth, API key, and certificate-based auth components

#### 🔧 **Schema Components**
- **Attribute definitions**: Pre-defined attribute types with validation
- **Block structures**: Reusable configuration block components
- **Validation rules**: Common validation patterns and custom validators
- **Type converters**: Automatic conversion between Terraform and native types

#### 🔐 **Authentication Components**
- **OAuth 2.0 flows**: Complete OAuth implementation with token management
- **API key management**: Secure API key handling with rotation support
- **Certificate auth**: X.509 certificate-based authentication
- **Custom auth**: Extensible authentication framework for custom schemes

#### 🌐 **HTTP Components**
- **REST clients**: Pre-configured HTTP clients with retry logic
- **Request builders**: Fluent API for building HTTP requests
- **Response parsers**: Automatic parsing and validation of API responses
- **Error handlers**: Standardized error handling and mapping

#### 📋 **State Management**
- **State mappers**: Automatic conversion between API and Terraform state
- **Diff calculators**: Intelligent change detection and planning
- **Import handlers**: Support for importing existing resources
- **Migration utilities**: Schema migration and state upgrade utilities

#### ⚡ **Performance Components**
- **Caching layers**: Intelligent caching for API responses
- **Batch operations**: Efficient bulk resource operations
- **Rate limiting**: Built-in rate limiting and throttling
- **Connection pooling**: Optimized HTTP connection management

## Installation

```bash
# Basic installation
uv add pyvider-components

# With all extras for full functionality
uv add pyvider-components[all]

# Development installation
uv add pyvider-components[dev]
```

## Quick Start

### Using Standard Components

```python
from pyvider import provider, resource
from pyvider.components import (
    RestResourceComponent,
    OAuthAuthenticator,
    StandardAttributes
)

@provider
class MyCloudProvider:
    """Provider using standard components."""

    # Use standard OAuth component
    authenticator = OAuthAuthenticator(
        client_id_attr="client_id",
        client_secret_attr="client_secret",
        token_url="https://api.example.com/oauth/token"
    )

@resource("mycloud_server")
class ServerResource(RestResourceComponent):
    """Server resource using REST component."""

    # Standard attributes with validation
    name = StandardAttributes.string(required=True)
    size = StandardAttributes.choice(
        choices=["small", "medium", "large"],
        default="small"
    )
    region = StandardAttributes.string(required=True)

    # Override component methods
    def get_api_endpoint(self) -> str:
        return f"/servers/{self.get_id()}"

    def create_payload(self) -> dict:
        return {
            "name": self.name,
            "size": self.size,
            "region": self.region
        }
```

### Custom Component Development

```python
from pyvider.components.base import BaseComponent
from pyvider.schema import Attribute
from pyvider.cty import CtyString

class DatabaseComponent(BaseComponent):
    """Custom database component."""

    # Define component schema
    connection_string = CtyString = Attribute(
        description="Database connection string",
        required=True,
        sensitive=True
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._connection = None

    def connect(self):
        """Establish database connection."""
        if not self._connection:
            self._connection = self.create_connection(
                self.connection_string
            )
        return self._connection

    def execute_query(self, query: str) -> list:
        """Execute database query."""
        conn = self.connect()
        return conn.execute(query).fetchall()

# Use custom component
@resource("mydb_table")
class TableResource(DatabaseComponent):
    """Database table resource."""

    table_name = CtyString = Attribute(required=True)

    def create(self):
        self.execute_query(f"CREATE TABLE {self.table_name} (...)")

    def read(self):
        return self.execute_query(f"DESCRIBE {self.table_name}")

    def delete(self):
        self.execute_query(f"DROP TABLE {self.table_name}")
```

## Component Categories

### **Authentication Components**

#### OAuth 2.0 Component
```python
from pyvider.components.auth import OAuth2Component

class OAuth2Provider(OAuth2Component):
    client_id = "your-client-id"
    client_secret = "your-client-secret"
    token_url = "https://api.example.com/oauth/token"
    scopes = ["read", "write"]
```

#### API Key Component
```python
from pyvider.components.auth import APIKeyComponent

class APIKeyProvider(APIKeyComponent):
    api_key_header = "X-API-Key"
    api_key_param = "api_key"  # Or query parameter
```

### **HTTP Components**

#### REST Client Component
```python
from pyvider.components.http import RestClientComponent

class APIResource(RestClientComponent):
    base_url = "https://api.example.com/v1"

    def get_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "User-Agent": "terraform-provider-example/1.0"
        }
```

#### GraphQL Component
```python
from pyvider.components.graphql import GraphQLComponent

class GraphQLResource(GraphQLComponent):
    endpoint = "https://api.example.com/graphql"

    def get_query(self) -> str:
        return """
        query GetUser($id: ID!) {
            user(id: $id) {
                name
                email
                created_at
            }
        }
        """
```

### **Schema Components**

#### Standard Attributes
```python
from pyvider.components.schema import StandardAttributes

# Common attribute patterns
name = StandardAttributes.string(required=True)
tags = StandardAttributes.tags()
timeouts = StandardAttributes.timeouts()
created_at = StandardAttributes.timestamp(computed=True)
size = StandardAttributes.choice(choices=["small", "medium", "large"])
```

#### Validation Components
```python
from pyvider.components.validation import Validators

# Built-in validators
email = Validators.email()
url = Validators.url()
port = Validators.port_range(1024, 65535)
cidr = Validators.cidr_block()
json_string = Validators.json()
```

### **State Management Components**

#### State Mapper
```python
from pyvider.components.state import StateMapper

class ServerStateMapper(StateMapper):
    """Map API response to Terraform state."""

    def api_to_state(self, api_response: dict) -> dict:
        return {
            "id": api_response["server_id"],
            "name": api_response["display_name"],
            "status": api_response["current_status"],
            "created_at": api_response["creation_time"]
        }

    def state_to_api(self, state: dict) -> dict:
        return {
            "display_name": state["name"],
            "server_type": state["size"]
        }
```

## Advanced Features

### Component Composition

```python
from pyvider.components import ComponentMixin

class AdvancedResource(
    RestClientComponent,
    OAuth2Component,
    StateMapper,
    ComponentMixin
):
    """Resource with multiple composed components."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_components()
```

### Custom Middleware

```python
from pyvider.components.middleware import BaseMiddleware

class LoggingMiddleware(BaseMiddleware):
    """Log all API requests and responses."""

    def before_request(self, request):
        self.logger.info(f"API Request: {request.method} {request.url}")
        return request

    def after_response(self, response):
        self.logger.info(f"API Response: {response.status_code}")
        return response
```

### Component Testing

```python
from pyvider.components.testing import ComponentTestCase

class TestServerResource(ComponentTestCase):
    """Test server resource component."""

    def test_create_server(self):
        resource = self.create_resource(ServerResource, {
            "name": "test-server",
            "size": "small",
            "region": "us-east-1"
        })

        result = resource.create()
        self.assertIsNotNone(result.id)
        self.assertEqual(result.name, "test-server")
```

## Use Cases

### **Rapid Provider Development**
Accelerate provider development by using pre-built components for common patterns and functionality.

### **Consistency Across Providers**
Ensure consistent behavior and patterns across multiple Terraform providers in your organization.

### **Best Practice Implementation**
Automatically incorporate Terraform provider best practices without manual implementation.

### **Reduced Maintenance**
Leverage maintained, tested components to reduce the maintenance burden of custom provider code.

## Integration with Pyvider

pyvider-components is designed to work seamlessly with the Pyvider framework:

- **Decorator compatibility**: Components work with Pyvider's `@resource` and `@data_source` decorators
- **Schema integration**: Components automatically integrate with Pyvider's schema system
- **Type safety**: Full type annotations and validation support
- **Testing framework**: Built-in testing utilities for component validation

## Related Documentation

- **[API Reference](../pyvider-components/reference/)** - Complete API documentation
- **[Pyvider Integration](../packages/pyvider.md)** - Pyvider framework documentation
- **[Component Guide](../guides/component-development.md)** - Building custom components

## Repository

- **Repository**: [pyvider-components](https://github.com/provide-io/pyvider-components)
- **Package**: `pyvider-components` on PyPI
- **License**: MIT