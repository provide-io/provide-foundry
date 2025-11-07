# Design Principles

The Provide Foundry is built on a foundation of carefully considered design principles that guide every architectural decision, API design, and implementation choice. These principles ensure consistency, maintainability, and excellent developer experience across all packages.

## Core Philosophy

### Developer Experience First

Every decision prioritizes the developer experience. This means:

- **Intuitive APIs**: Functions and classes should work as developers expect
- **Excellent Error Messages**: Clear, actionable error messages with suggestions
- **Comprehensive Documentation**: Examples, guides, and API references for everything
- **Fast Feedback Loops**: Quick iteration with immediate feedback

```python
# Good: Clear, intuitive API
@register_resource("webserver")
class WebServer(BaseResource):
    port: int = Attribute(description="Port to listen on", default=8080)

# Bad: Unclear, complex API
class WebServerResource(BaseResource):
    def __init__(self):
        super().__init__()
        self.add_attribute("port", IntegerAttribute(default_value=8080))
```

### Type Safety Everywhere

Static typing catches errors early and improves code quality:

- **Modern Python Typing**: Use `str | None` instead of `Optional[str]`
- **Runtime Validation**: Validate types at runtime where appropriate
- **Schema-Driven**: All data structures defined with comprehensive schemas
- **No `Any` Types**: Avoid `Any` except where absolutely necessary

```python
# Good: Comprehensive type annotations
def create_resource(
    config: ResourceConfig,
    provider: Provider,
    timeout: float = 30.0
) -> ResourceState:
    pass

# Bad: Missing or weak typing
def create_resource(config, provider, timeout=30):
    pass
```

### Composition Over Inheritance

Favor composition and mixins over deep inheritance hierarchies:

- **Small, Focused Classes**: Each class has a single responsibility
- **Mixin Pattern**: Combine behavior through mixins
- **Dependency Injection**: Pass dependencies explicitly
- **Protocol-Based Design**: Use protocols instead of abstract base classes

```python
# Good: Composition with protocols
class ResourceManager:
    def __init__(self, validator: Validator, logger: Logger):
        self.validator = validator
        self.logger = logger

# Bad: Deep inheritance
class ResourceManager(BaseManager, ValidatorMixin, LoggerMixin):
    pass
```

## API Design Principles

### Consistency

Consistent APIs across all packages reduce cognitive load:

#### Naming Conventions

- **Functions**: `snake_case` for functions and variables
- **Classes**: `PascalCase` for classes and types
- **Constants**: `UPPER_SNAKE_CASE` for constants
- **Modules**: `snake_case` for module names

#### Parameter Patterns

- **Required parameters first**: Most important parameters come first
- **Keyword-only for complex functions**: Use `*` to force keyword arguments
- **Sensible defaults**: Provide defaults for optional parameters
- **No boolean traps**: Use enums instead of boolean flags

```python
# Good: Clear parameter pattern
def create_provider(
    name: str,
    *,
    config_path: Path | None = None,
    log_level: LogLevel = LogLevel.INFO,
    enable_telemetry: bool = True
) -> Provider:
    pass

# Bad: Boolean trap and unclear parameters
def create_provider(name, config, log, telemetry=True):
    pass
```

### Discoverability

Make functionality easy to discover:

- **Flat Import Structure**: Important functions available at package root
- **Clear Module Organization**: Related functionality grouped together
- **Comprehensive `__all__`**: Explicit public API definition
- **Type Hints in Signatures**: Rich type information for IDE support

```python
# Good: Clear public API
from pyvider.providers import register_provider
from pyvider.resources import register_resource
from pyvider.data_sources import register_data_source
from pyvider.functions import register_function
from pyvider.schema import Attribute, Block

# Bad: Deep imports required
from pyvider.core.decorators.provider import provider
from pyvider.schema.types.attribute import Attribute
```

### Extensibility

Design for extension without modification:

- **Plugin Architecture**: Use the hub pattern for extensibility
- **Event System**: Allow hooking into lifecycle events
- **Configuration Points**: Provide configuration for customization
- **Protocol-Based**: Define clear interfaces for extension

```python
# Good: Extensible through protocols
class CustomProcessor(LogProcessor):
    def process(self, record: LogRecord) -> LogRecord:
        # Custom processing logic
        return record

# Register the processor
get_hub().register_processor(CustomProcessor())
```

## Implementation Principles

### No Backward Compatibility Burden

The foundry prioritizes clean, modern code over backward compatibility:

- **Direct Implementation**: Implement the target state directly
- **Modern Python Features**: Use Python 3.11+ features without hesitation
- **Clean Abstractions**: Don't compromise design for compatibility
- **Breaking Changes**: Accept breaking changes to improve the design

```python
# Good: Modern Python features
def process_items(items: list[Item]) -> dict[str, Any]:
    return {item.name: item.value for item in items}

# Bad: Backward compatibility
def process_items(items):
    # Type: (List[Item]) -> Dict[str, Any]
    return dict((item.name, item.value) for item in items)
```

### Configuration Over Convention

Explicit configuration is better than implicit behavior:

- **No Magic Defaults**: All defaults defined in configuration files
- **Explicit Dependencies**: Dependencies declared explicitly
- **Environment-Specific**: Configuration varies by environment
- **Type-Safe Config**: All configuration validated against schemas

```python
# Good: Explicit configuration
@attrs.define
class DatabaseConfig:
    host: str
    port: int = 5432
    timeout: float = 30.0

# Bad: Hidden defaults
class Database:
    def __init__(self, host):
        self.host = host
        self.port = 5432  # Hidden default
```

### Fail Fast and Loud

Detect and report errors as early as possible:

- **Input Validation**: Validate inputs at API boundaries
- **Schema Validation**: Validate data against schemas
- **Type Checking**: Use runtime type checking where appropriate
- **Clear Error Messages**: Provide actionable error information

```python
# Good: Early validation with clear errors
def create_server(port: int) -> Server:
    if not (1 <= port <= 65535):
        raise ValueError(
            f"Port {port} is invalid. Must be between 1 and 65535."
        )
    return Server(port)

# Bad: Silent failures or late errors
def create_server(port):
    return Server(port)  # May fail later
```

## Testing Principles

### Test-Driven Development

Write tests before implementation:

- **Red-Green-Refactor**: Write failing test, make it pass, refactor
- **Behavior-Driven**: Test behavior, not implementation details
- **Comprehensive Coverage**: Aim for high test coverage
- **Fast Feedback**: Tests should run quickly

```python
# Good: Test behavior
def test_resource_creation_with_valid_config():
    config = ResourceConfig(name="test", port=8080)
    resource = create_resource(config)
    assert resource.name == "test"
    assert resource.port == 8080

# Bad: Test implementation
def test_resource_creation_calls_constructor():
    config = ResourceConfig(name="test", port=8080)
    with mock.patch('Resource.__init__') as mock_init:
        create_resource(config)
        mock_init.assert_called_once()
```

### Property-Based Testing

Use property-based testing for complex logic:

- **Hypothesis Integration**: Use Hypothesis for property-based tests
- **Edge Case Discovery**: Let tools find edge cases
- **Invariant Testing**: Test properties that should always hold
- **Shrinking**: Minimal failing examples for debugging

```python
from hypothesis import given, strategies as st

@given(st.integers(min_value=1, max_value=65535))
def test_server_accepts_valid_ports(port):
    server = create_server(port)
    assert server.port == port
```

### Integration Testing

Test real interactions between components:

- **End-to-End Tests**: Test complete workflows
- **Cross-Package Tests**: Test interactions between packages
- **Real Dependencies**: Use real external services where possible
- **Conformance Tests**: Test compatibility with external systems

## Documentation Principles

### Documentation as Code

Treat documentation with the same care as code:

- **Version Controlled**: All documentation in version control
- **Tested Examples**: All code examples are tested
- **Automated Generation**: Generate documentation from code where possible
- **Continuous Integration**: Documentation builds on every change

### Multiple Audiences

Different audiences need different documentation:

- **Tutorials**: For learning step-by-step
- **How-To Guides**: For solving specific problems
- **Reference**: For looking up details
- **Explanations**: For understanding concepts

```markdown
<!-- Good: Clear audience targeting -->
# Tutorial: Your First Provider
*For developers new to Pyvider*

This tutorial walks you through creating your first Terraform provider...

# Reference: Provider API
*For developers implementing providers*

## Provider Class
```python
class Provider:
    """Base class for all providers."""
```

<!-- Bad: Mixed audiences -->
# Provider Documentation
This explains providers and also shows how to create them...
```

## Performance Principles

### Async by Default

Embrace asynchronous programming for scalability:

- **Non-Blocking Operations**: Use async/await for I/O operations
- **Concurrent Execution**: Process operations concurrently where possible
- **Backpressure Handling**: Handle backpressure gracefully
- **Resource Management**: Use context managers for resource cleanup

```python
# Good: Async operations
async def fetch_resource_data(resource_id: str) -> ResourceData:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/resources/{resource_id}")
        return ResourceData.from_json(response.json())

# Bad: Blocking operations
def fetch_resource_data(resource_id: str) -> ResourceData:
    response = requests.get(f"/resources/{resource_id}")
    return ResourceData.from_json(response.json())
```

### Lazy Initialization

Initialize resources only when needed:

- **Lazy Loading**: Load modules and components on first use
- **Singleton Pattern**: Use singletons for expensive resources
- **Connection Pooling**: Pool expensive connections
- **Caching**: Cache expensive computations

### Memory Efficiency

Be conscious of memory usage:

- **Generator Functions**: Use generators for large datasets
- **Streaming**: Stream large files instead of loading into memory
- **Weak References**: Use weak references to break reference cycles
- **Resource Cleanup**: Explicitly clean up resources

## Security Principles

### Security by Default

Security should be the default, not an option:

- **Secure Defaults**: All defaults should be secure
- **Principle of Least Privilege**: Grant minimal necessary permissions
- **Input Validation**: Validate all inputs thoroughly
- **No Secrets in Logs**: Never log sensitive information

```python
# Good: Secure by default
@attrs.define
class DatabaseConfig:
    password: str = attrs.field(repr=False)  # Hidden from repr
    ssl_mode: str = "require"  # Secure default

# Bad: Insecure defaults
@attrs.define
class DatabaseConfig:
    password: str
    ssl_mode: str = "disable"  # Insecure default
```

### Defense in Depth

Implement multiple layers of security:

- **Input Validation**: Validate at API boundaries
- **Authentication**: Verify identity before access
- **Authorization**: Check permissions for operations
- **Audit Logging**: Log security-relevant events

### Transparent Security

Security should be visible and understandable:

- **Clear Policies**: Document security policies clearly
- **Audit Trails**: Provide comprehensive audit trails
- **Error Messages**: Security errors should be informative
- **Documentation**: Document security considerations

## Ecosystem Principles

### Interoperability

Components should work well together:

- **Standard Interfaces**: Use common interfaces across packages
- **Data Format Compatibility**: Use compatible data formats
- **Protocol Adherence**: Follow established protocols
- **Graceful Degradation**: Work with missing optional dependencies

### Modularity

Each package should be independently useful:

- **Single Responsibility**: Each package has a clear purpose
- **Minimal Dependencies**: Avoid unnecessary dependencies
- **Optional Features**: Make advanced features optional
- **Clear Boundaries**: Well-defined package boundaries

### Evolution

The foundry should evolve gracefully:

- **Versioned APIs**: Use semantic versioning for APIs
- **Deprecation Process**: Clear process for deprecating features
- **Migration Guides**: Help users migrate between versions
- **Experimental Features**: Mark experimental features clearly

---

These principles guide every decision in the provide.io foundry. They ensure that the tools remain consistent, maintainable, and enjoyable to use as the foundry grows and evolves.

Continue exploring with our [architecture overview](architecture.md) or see these principles in action in our [development guides](../guides/index.md).