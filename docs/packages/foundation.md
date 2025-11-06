# provide-foundation

The foundation of the entire provide.io foundry, providing core infrastructure services including structured logging, error handling, configuration management, and component discovery.

## Overview

`provide-foundation` is designed to be the bedrock upon which all other foundry packages are built. It provides essential services that every application needs: logging, error handling, configuration, and component management.

### Key Features

- **🎨 Emoji-Enhanced Logging**: Beautiful, structured logs with contextual emojis
- **⚡ High Performance**: >14,000 messages/second with emoji processing
- **🔧 Type-Safe Configuration**: Comprehensive configuration management
- **🏗️ Hub Pattern**: Centralized component discovery and registration
- **🛡️ Rich Error Handling**: Hierarchical errors with rich context
- **🔄 Async-First**: Built for async/await from the ground up

## Quick Start

### Installation

```bash
# Basic installation
uv add provide-foundation

# With all optional features
uv add provide-foundation[all]

# Development installation
git clone https://github.com/provide-io/provide-foundation.git
cd provide-foundation
uv sync
```

### Basic Usage

```python
from provide.foundation import logger

# Get a logger for your module
log = logger.get_logger(__name__)

# Log with emoji enhancement and structured data
log.info("Application started", version="1.0.0", port=8080)
log.error("Database connection failed",
          error="Connection timeout",
          host="db.example.com")
```

## Core Components

### Structured Logging

The logging system provides beautiful, performant structured logging with emoji enhancement:

```python
from provide.foundation import logger

# Configure logging
logger.configure(
    level="INFO",
    format="emoji",  # emoji, json, or text
    enable_emoji=True
)

# Use the logger
log = logger.get_logger(__name__)

# Domain-Action-Status pattern with emojis
log.info("🌐⬇️✅ Downloaded configuration",
         url="https://api.example.com/config",
         size="1.2KB",
         duration=0.45)

# Automatic emoji selection based on context
log.database.info("User created", user_id=123)  # 🗄️👤✅
log.http.error("Request failed", status=500)    # 🌐❌
log.ai.debug("Model loaded", model="gpt-4")     # 🤖🧠💭
```

### Error Handling

Rich error handling with hierarchical error types and context:

```python
from provide.foundation.errors import FoundationError

class DatabaseError(FoundationError):
    """Database operation failed."""

    def _default_code(self) -> str:
        return "DATABASE_ERROR"

# Raise with rich context
raise DatabaseError(
    "Failed to connect to database",
    host="db.example.com",
    port=5432,
    context={
        "operation": "connect",
        "timeout": 30.0,
        "retry_count": 3
    }
)
```

### Configuration Management

Type-safe configuration with environment variable support:

```python
import attrs
from provide.foundation.config import ConfigLoader

@attrs.define
class DatabaseConfig:
    host: str
    port: int = 5432
    username: str = attrs.field(repr=False)
    password: str = attrs.field(repr=False)
    ssl_mode: str = "require"

# Load configuration
loader = ConfigLoader()
config = loader.load(
    DatabaseConfig,
    sources=[
        "config.toml",
        "~/.myapp/config.toml",
        "$DATABASE_CONFIG_PATH"
    ]
)
```

### Hub Pattern

Centralized component discovery and registration:

```python
from provide.foundation.hub import get_hub

# Register a component
hub = get_hub()
hub.register("database", DatabaseConnection(config))

# Discover components
db = hub.get("database")
all_processors = hub.discover_by_type(ProcessorBase)

# Use with decorators
@hub.register_processor
class CustomLogProcessor:
    def process(self, record: LogRecord) -> LogRecord:
        # Custom processing
        return record
```

## Advanced Features

### Platform Detection

Cross-platform compatibility utilities:

```python
from provide.foundation.platform import get_platform_info

platform = get_platform_info()
print(f"OS: {platform.os}")           # darwin, linux, windows
print(f"Arch: {platform.arch}")       # arm64, amd64
print(f"Python: {platform.python}")   # 3.11.5
```

### Process Management

Async process management with structured logging:

```python
from provide.foundation.process import run_process

# Run a subprocess with rich logging
result = await run_process(
    ["curl", "-s", "https://api.example.com"],
    timeout=30.0,
    log_output=True
)

if result.success:
    print(f"Output: {result.stdout}")
else:
    print(f"Error: {result.stderr}")
```

### Resilience Patterns

Built-in resilience patterns for robust applications:

```python
from provide.foundation.resilience import with_retry, CircuitBreaker

# Retry with exponential backoff
@with_retry(max_attempts=3, backoff_factor=2.0)
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

# Circuit breaker for external services
breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=60.0,
    expected_exception=httpx.HTTPError
)

@breaker
async def call_external_service():
    # Service call that might fail
    pass
```

## Configuration

### Logging Configuration

```python
from provide.foundation.logger import TelemetryConfig

config = TelemetryConfig(
    log_level="INFO",
    log_format="emoji",  # emoji, json, text
    enable_emoji=True,
    enable_file_logging=True,
    log_file_path="/var/log/myapp.log",
    log_file_rotation="1GB",
    structured_logging=True
)

logger.configure(config)
```

### Environment Variables

Configure foundation through environment variables:

```bash
# Logging configuration
export PROVIDE_LOG_LEVEL=DEBUG
export PROVIDE_LOG_FORMAT=json
export PROVIDE_LOG_EMOJI=false

# File logging
export PROVIDE_LOG_FILE_ENABLED=true
export PROVIDE_LOG_FILE_PATH=/var/log/app.log

# Module-specific log levels
export PROVIDE_LOG_MODULE_LEVELS="urllib3:WARNING,asyncio:ERROR"
```

### TOML Configuration

```toml
# config.toml
[logging]
level = "INFO"
format = "emoji"
enable_emoji = true
enable_file_logging = false

[hub]
auto_discovery = true
discovery_paths = ["./plugins", "~/.myapp/plugins"]

[resilience]
default_timeout = 30.0
default_retries = 3
```

## Performance

### Benchmarks

Foundation is optimized for performance:

- **Logging**: >14,000 messages/second with emoji processing
- **Configuration**: Microsecond-level config access
- **Hub Operations**: Sub-millisecond component lookup
- **Memory**: Minimal memory overhead

### Optimization Tips

```python
# Use lazy loggers for performance
log = logger.get_logger(__name__)

# Prefer structured logging over string formatting
log.info("User action", user_id=user.id, action="login")  # Good
log.info(f"User {user.id} logged in")                     # Less efficient

# Use context managers for expensive operations
with logger.context(user_id=user.id):
    # All logs in this block include user_id
    log.info("Processing request")
    process_user_request()
```

## Testing

Foundation provides comprehensive testing utilities:

```python
import pytest
from provide.foundation.testing import (
    reset_foundation_setup_for_testing,
    set_log_stream_for_testing,
    capture_logs
)

@pytest.fixture(autouse=True)
def reset_foundation():
    """Reset foundation state before each test."""
    reset_foundation_setup_for_testing()

def test_logging_output():
    """Test log output capture."""
    with capture_logs() as logs:
        log = logger.get_logger("test")
        log.info("Test message", data="value")

    assert len(logs) == 1
    assert logs[0]["message"] == "Test message"
    assert logs[0]["data"] == "value"
```

## Integration Examples

### With FastAPI

```python
from fastapi import FastAPI
from provide.foundation import logger

app = FastAPI()
log = logger.get_logger(__name__)

@app.middleware("http")
async def logging_middleware(request, call_next):
    with logger.context(
        method=request.method,
        url=str(request.url),
        client=request.client.host
    ):
        log.info("🌐⬅️📝 Request received")
        response = await call_next(request)
        log.info("🌐➡️✅ Response sent", status=response.status_code)
        return response
```

### With Django

```python
# settings.py
import logging
from provide.foundation.logger import configure_django_logging

# Configure Django to use foundation logging
configure_django_logging(
    level="INFO",
    format="emoji",
    enable_emoji=True
)

# views.py
from provide.foundation import logger

log = logger.get_logger(__name__)

def my_view(request):
    log.info("🌐👤📝 User request",
             user=request.user.username,
             view="my_view")
    # View logic here
```

## API Reference

For complete API documentation, see:

- **[Logger API](../provide-foundation/reference/provide/foundation/logger/index.md)**: Complete logging interface
- **[Configuration API](../provide-foundation/reference/provide/foundation/config/index.md)**: Configuration management
- **[Hub API](../provide-foundation/reference/provide/foundation/hub/index.md)**: Component discovery
- **[Error API](../provide-foundation/reference/provide/foundation/errors/index.md)**: Error handling

## Related Packages

- **[provide-testkit](testkit.md)**: Testing utilities that build on foundation
- **[pyvider](pyvider.md)**: Framework that uses foundation for logging and errors
- **[flavorpack](flavorpack.md)**: Packaging tool that uses foundation infrastructure

---

`provide-foundation` is the cornerstone of the provide.io foundry. Master its patterns and you'll be well-equipped to build robust, observable applications with the rest of the foundry.