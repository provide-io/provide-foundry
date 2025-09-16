# pyvider-cty

Python implementation of Terraform's CTY (Configuration Type System) providing type-safe value handling, serialization, and validation for Terraform provider development.

## Overview

`pyvider-cty` implements Terraform's CTY type system in Python, enabling type-safe configuration and state management for Terraform providers. It provides full compatibility with Terraform's type system while offering a Pythonic interface.

### Key Features

- **🔒 Type Safety**: Complete CTY type system implementation
- **🔄 Bidirectional Conversion**: Seamless conversion between Python and CTY types
- **📏 Schema Validation**: Comprehensive type checking and validation
- **🗂️ Serialization**: JSON/MessagePack serialization with type preservation
- **🧬 Value Operations**: Type-safe operations on CTY values
- **⚡ Performance**: Optimized for high-throughput provider operations

## Installation

```bash
# Basic installation
pip install pyvider-cty

# With all extras for full functionality
pip install pyvider-cty[all]
```

## Quick Start

### Basic Types

```python
from pyvider.cty import (
    CtyString, CtyNumber, CtyBool,
    CtyList, CtySet, CtyMap, CtyObject
)

# Create primitive values
name = CtyString("alice")
age = CtyNumber(25)
active = CtyBool(True)

# Access underlying values
print(name.value)  # "alice"
print(age.as_python())  # 25
print(active.is_true())  # True

# Type checking
assert name.type.is_string_type()
assert age.type.is_number_type()
assert active.type.is_bool_type()
```

### Collection Types

```python
# Lists
tags = CtyList([CtyString("web"), CtyString("api")])
numbers = CtyList([CtyNumber(1), CtyNumber(2), CtyNumber(3)])

# Sets (unique values)
unique_tags = CtySet({CtyString("prod"), CtyString("web")})

# Maps (key-value pairs)
config = CtyMap({
    "database": CtyString("postgres"),
    "port": CtyNumber(5432),
    "ssl": CtyBool(True)
})

# Access collection elements
print(tags[0].value)  # "web"
print(config["port"].value)  # 5432
print(len(unique_tags))  # 2
```

### Object Types

```python
# Define object structure
user_type = CtyObject.type({
    "name": CtyString.type(),
    "age": CtyNumber.type(),
    "active": CtyBool.type(),
    "tags": CtyList[CtyString].type()
})

# Create object instance
user = CtyObject({
    "name": CtyString("alice"),
    "age": CtyNumber(25),
    "active": CtyBool(True),
    "tags": CtyList([CtyString("admin"), CtyString("user")])
}, user_type)

# Access object attributes
print(user["name"].value)  # "alice"
print(user["tags"][0].value)  # "admin"
```

## Type System

### Primitive Types

```python
from pyvider.cty import CtyString, CtyNumber, CtyBool

# String type
text = CtyString("hello world")
assert text.type.is_string_type()
assert text.value == "hello world"

# Number type (handles int, float, Decimal)
integer = CtyNumber(42)
decimal = CtyNumber(3.14159)
big_num = CtyNumber(Decimal("999999999999999999999"))

assert integer.type.is_number_type()
assert decimal.as_python() == 3.14159
assert big_num.is_known()

# Boolean type
flag = CtyBool(True)
disabled = CtyBool(False)

assert flag.type.is_bool_type()
assert flag.is_true()
assert disabled.is_false()
```

### Unknown and Null Values

```python
from pyvider.cty import CtyUnknown, CtyNull

# Unknown value (computed during apply)
unknown_string = CtyUnknown(CtyString.type())
assert unknown_string.is_unknown()
assert not unknown_string.is_known()

# Null value
null_number = CtyNull(CtyNumber.type())
assert null_number.is_null()
assert not null_number.is_known()

# Check value state
def process_value(value):
    if value.is_null():
        return "Value is null"
    elif value.is_unknown():
        return "Value will be computed"
    else:
        return f"Value is {value.as_python()}"
```

### Dynamic Types

```python
from pyvider.cty import CtyDynamic

# Dynamic type (any CTY type)
dynamic_value = CtyDynamic(CtyString("flexible"))
assert dynamic_value.type.is_dynamic_type()

# Can hold any CTY value
dynamic_value = CtyDynamic(CtyNumber(42))
dynamic_value = CtyDynamic(CtyList([CtyString("a"), CtyString("b")]))
```

## Collection Operations

### List Operations

```python
from pyvider.cty import CtyList, CtyString, CtyNumber

# Create and manipulate lists
tags = CtyList([CtyString("web"), CtyString("api")])

# Append elements
tags = tags.append(CtyString("prod"))

# Access by index
first_tag = tags[0]  # CtyString("web")

# Iterate over elements
for tag in tags:
    print(tag.value)

# List comprehension with type preservation
numbers = CtyList([CtyNumber(1), CtyNumber(2), CtyNumber(3)])
doubled = CtyList([CtyNumber(n.value * 2) for n in numbers])

# Type-safe operations
string_list = CtyList[CtyString]([CtyString("a"), CtyString("b")])
assert string_list.element_type.is_string_type()
```

### Set Operations

```python
from pyvider.cty import CtySet

# Create sets (unique elements)
tags = CtySet({CtyString("web"), CtyString("api"), CtyString("web")})
print(len(tags))  # 2 (duplicates removed)

# Set operations
new_tags = CtySet({CtyString("prod"), CtyString("staging")})
all_tags = tags.union(new_tags)
common_tags = tags.intersection(new_tags)

# Check membership
has_web = CtyString("web") in tags  # True
```

### Map Operations

```python
from pyvider.cty import CtyMap

# Create maps
config = CtyMap({
    "host": CtyString("localhost"),
    "port": CtyNumber(8080),
    "ssl": CtyBool(False)
})

# Access values
host = config["host"]  # CtyString("localhost")
port = config.get("port", CtyNumber(80))  # With default

# Update maps (immutable operations)
updated_config = config.set("ssl", CtyBool(True))
new_config = config.merge(CtyMap({
    "timeout": CtyNumber(30),
    "retries": CtyNumber(3)
}))

# Iterate over keys and values
for key, value in config.items():
    print(f"{key}: {value.as_python()}")
```

## Type Conversion

### From Python to CTY

```python
from pyvider.cty import from_python

# Automatic conversion from Python types
python_data = {
    "name": "alice",
    "age": 25,
    "active": True,
    "tags": ["user", "admin"],
    "config": {
        "theme": "dark",
        "notifications": True
    }
}

cty_value = from_python(python_data)
assert isinstance(cty_value, CtyObject)
assert cty_value["name"].value == "alice"
assert cty_value["tags"][0].value == "user"
```

### From CTY to Python

```python
# Convert CTY values back to Python
user = CtyObject({
    "name": CtyString("bob"),
    "age": CtyNumber(30),
    "settings": CtyMap({
        "theme": CtyString("light"),
        "lang": CtyString("en")
    })
})

python_dict = user.as_python()
print(python_dict)
# {
#     "name": "bob",
#     "age": 30,
#     "settings": {
#         "theme": "light",
#         "lang": "en"
#     }
# }
```

### Type Conformance

```python
from pyvider.cty import conform_type

# Convert values to match specific types
string_value = CtyString("42")
number_type = CtyNumber.type()

# Safe conversion with type checking
try:
    number_value = conform_type(string_value, number_type)
    print(number_value.value)  # 42 (as number)
except TypeError as e:
    print(f"Cannot convert: {e}")

# Automatic type promotion
small_list = CtyList([CtyString("a")])
large_list_type = CtyList[CtyString].type(min_items=3)

# Pad with unknowns if needed for schema compliance
conformed = conform_type(small_list, large_list_type)
```

## Schema Validation

### Type Constraints

```python
from pyvider.cty import CtyNumber, CtyString, ValidationError

# Number with constraints
def validate_port(value: CtyNumber) -> bool:
    """Validate port number range."""
    if not value.is_known():
        return True  # Unknown values pass validation
    port = value.value
    return 1 <= port <= 65535

port = CtyNumber(8080)
assert validate_port(port)

try:
    invalid_port = CtyNumber(70000)
    if not validate_port(invalid_port):
        raise ValidationError("Port must be between 1 and 65535")
except ValidationError as e:
    print(f"Validation failed: {e}")
```

### Complex Validation

```python
from pyvider.cty import CtyObject, ValidationResult

def validate_user_config(user: CtyObject) -> ValidationResult:
    """Validate user configuration object."""
    errors = []

    # Check required fields
    if not user.has_attribute("email"):
        errors.append("email is required")
    elif user["email"].is_known():
        email = user["email"].value
        if "@" not in email:
            errors.append("email must be valid email address")

    # Check age constraints
    if user.has_attribute("age") and user["age"].is_known():
        age = user["age"].value
        if not (13 <= age <= 120):
            errors.append("age must be between 13 and 120")

    return ValidationResult(valid=len(errors) == 0, errors=errors)

# Validate user object
user = CtyObject({
    "name": CtyString("alice"),
    "email": CtyString("alice@example.com"),
    "age": CtyNumber(25)
})

result = validate_user_config(user)
if result.valid:
    print("User configuration is valid")
else:
    for error in result.errors:
        print(f"Error: {error}")
```

## Serialization

### JSON Serialization

```python
import json
from pyvider.cty import CtyObject, CtyString, CtyNumber

# Create CTY value
user = CtyObject({
    "name": CtyString("alice"),
    "age": CtyNumber(25)
})

# Serialize to JSON with type information
json_data = user.to_json()
print(json_data)
# {
#     "value": {"name": "alice", "age": 25},
#     "type": {"object": {"name": "string", "age": "number"}}
# }

# Deserialize from JSON
restored_user = CtyObject.from_json(json_data)
assert restored_user["name"].value == "alice"
assert restored_user["age"].value == 25
```

### MessagePack Serialization

```python
import msgpack
from pyvider.cty import CtyList, CtyString

# Binary serialization for performance
tags = CtyList([CtyString("web"), CtyString("api")])

# Serialize to MessagePack
msgpack_data = tags.to_msgpack()
print(len(msgpack_data))  # Binary size

# Deserialize from MessagePack
restored_tags = CtyList.from_msgpack(msgpack_data)
assert len(restored_tags) == 2
assert restored_tags[0].value == "web"
```

## Value Operations

### Equality and Comparison

```python
from pyvider.cty import CtyString, CtyNumber

# Value equality
name1 = CtyString("alice")
name2 = CtyString("alice")
name3 = CtyString("bob")

assert name1 == name2  # Same value
assert name1 != name3  # Different value

# Type compatibility
number = CtyNumber(42)
string = CtyString("42")

assert number != string  # Different types
assert number.value == int(string.value)  # Same underlying value
```

### Path Operations

```python
from pyvider.cty import CtyObject, CtyPath

# Access nested values with paths
config = CtyObject({
    "database": CtyObject({
        "host": CtyString("localhost"),
        "port": CtyNumber(5432)
    }),
    "cache": CtyObject({
        "ttl": CtyNumber(300)
    })
})

# Create paths to nested values
db_host_path = CtyPath(["database", "host"])
cache_ttl_path = CtyPath(["cache", "ttl"])

# Get values using paths
db_host = config.get_path(db_host_path)  # CtyString("localhost")
cache_ttl = config.get_path(cache_ttl_path)  # CtyNumber(300)

# Set values using paths
updated_config = config.set_path(db_host_path, CtyString("database.example.com"))
```

## Advanced Features

### Custom Types

```python
from pyvider.cty import CtyType, CtyValue

class CtyIPAddress(CtyValue):
    """Custom type for IP addresses."""

    @classmethod
    def type(cls) -> CtyType:
        """Return IP address type."""
        return CtyType("ipaddress")

    def __init__(self, value: str):
        """Initialize IP address."""
        if not self._is_valid_ip(value):
            raise ValueError(f"Invalid IP address: {value}")
        super().__init__(value, self.type())

    def _is_valid_ip(self, value: str) -> bool:
        """Validate IP address format."""
        try:
            ipaddress.ip_address(value)
            return True
        except ValueError:
            return False

    def to_json(self) -> dict:
        """Serialize to JSON."""
        return {
            "value": self.value,
            "type": "ipaddress"
        }

# Use custom type
ip = CtyIPAddress("192.168.1.1")
assert ip.value == "192.168.1.1"
```

### Type Functions

```python
from pyvider.cty import CtyFunction, CtyString, CtyList

def concat_function(*args: CtyString) -> CtyString:
    """Concatenate strings."""
    result = "".join(arg.value for arg in args)
    return CtyString(result)

def length_function(value: CtyList) -> CtyNumber:
    """Get length of list."""
    return CtyNumber(len(value))

# Register functions
functions = {
    "concat": CtyFunction(concat_function),
    "length": CtyFunction(length_function)
}

# Use functions
result = functions["concat"](
    CtyString("hello"),
    CtyString(" "),
    CtyString("world")
)
assert result.value == "hello world"

list_length = functions["length"](
    CtyList([CtyString("a"), CtyString("b")])
)
assert list_length.value == 2
```

## Performance Optimization

### Value Caching

```python
from pyvider.cty import CtyObject, enable_caching

# Enable caching for repeated operations
with enable_caching():
    large_object = CtyObject({
        f"key_{i}": CtyString(f"value_{i}")
        for i in range(1000)
    })

    # First access computes and caches
    json_data = large_object.to_json()

    # Second access uses cache
    json_data_cached = large_object.to_json()
    assert json_data == json_data_cached
```

### Lazy Evaluation

```python
from pyvider.cty import CtyLazy

# Defer expensive computations
def expensive_computation():
    """Simulate expensive operation."""
    time.sleep(1)
    return CtyString("computed result")

lazy_value = CtyLazy(expensive_computation)

# Value is computed only when accessed
result = lazy_value.evaluate()  # Takes 1 second
cached_result = lazy_value.evaluate()  # Instant (cached)
```

## Testing Utilities

```python
from pyvider.cty.testing import (
    assert_cty_equal,
    assert_type_equal,
    generate_test_value
)

def test_user_processing():
    """Test user data processing."""
    # Generate test data
    test_user = generate_test_value(CtyObject.type({
        "name": CtyString.type(),
        "age": CtyNumber.type()
    }))

    # Process user data
    processed = process_user(test_user)

    # Assert results with helpful error messages
    assert_cty_equal(
        processed["status"],
        CtyString("active"),
        "User should be marked as active"
    )

    assert_type_equal(
        processed.type,
        expected_user_type,
        "Processed user should match expected schema"
    )
```

## Integration Examples

### With pyvider

```python
from pyvider import resource
from pyvider.cty import CtyString, CtyObject

@resource
class Database:
    """Database resource using CTY types."""

    config: CtyObject = Attribute(
        description="Database configuration",
        type=CtyObject.type({
            "engine": CtyString.type(),
            "version": CtyString.type(),
            "parameters": CtyMap[CtyString].type()
        })
    )

    def create(self, config) -> dict:
        """Create database with CTY configuration."""
        db_config = config.config
        engine = db_config["engine"].value
        version = db_config["version"].value
        params = {
            k: v.value for k, v in db_config["parameters"].items()
        }

        db = self.provider.client.create_database(
            engine=engine,
            version=version,
            parameters=params
        )

        return {"id": db.id, "config": config.config}
```

### With Terraform State

```python
from pyvider.cty import from_terraform_state, to_terraform_state

# Load from Terraform state
terraform_state = {
    "id": "db-123",
    "name": "mydb",
    "config": {
        "engine": "postgres",
        "version": "13"
    }
}

cty_state = from_terraform_state(terraform_state, schema)

# Modify state
updated_state = cty_state.set_path(
    CtyPath(["config", "version"]),
    CtyString("14")
)

# Convert back to Terraform format
new_terraform_state = to_terraform_state(updated_state)
```

## Best Practices

1. **Use type hints** - Always specify CTY types for clarity
2. **Validate early** - Check types and constraints as soon as possible
3. **Handle unknowns** - Always check for unknown values in computations
4. **Immutable operations** - CTY values are immutable, operations return new values
5. **Schema-driven** - Define schemas first, then create values
6. **Performance-aware** - Use caching and lazy evaluation for large values
7. **Test thoroughly** - Use testing utilities for comprehensive validation

## Migration Guide

### From Raw Python Types

```python
# Old: Raw Python types
user_data = {
    "name": "alice",
    "age": 25,
    "tags": ["user", "admin"]
}

# New: CTY types
user_data = CtyObject({
    "name": CtyString("alice"),
    "age": CtyNumber(25),
    "tags": CtyList([CtyString("user"), CtyString("admin")])
})

# Or convert automatically
user_data = from_python({
    "name": "alice",
    "age": 25,
    "tags": ["user", "admin"]
})
```

## Related Packages

- **[pyvider](pyvider.md)**: Core framework that uses CTY types
- **[pyvider-hcl](pyvider-hcl.md)**: HCL parser with CTY integration
- **[provide-foundation](foundation.md)**: Foundation services

---

pyvider-cty provides the type-safe foundation for all Terraform provider operations in the Provide Foundry. Its comprehensive CTY implementation ensures full compatibility with Terraform while offering an intuitive Python interface.