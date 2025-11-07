# Testing Patterns Guide

Testing strategies and patterns used across the provide.io ecosystem.

## Overview

All projects use pytest with async support and follow similar testing patterns. This guide covers common approaches and project-specific considerations.

## Standard Testing Setup

### Basic Test Structure

```python
import pytest
from pathlib import Path

def test_basic_functionality():
    """Test basic feature behavior."""
    result = my_function("input")
    assert result == "expected"

@pytest.mark.asyncio
async def test_async_functionality():
    """Test async features."""
    result = await my_async_function()
    assert result is not None
```

### Using Fixtures

```python
@pytest.fixture
def sample_data():
    """Provide test data."""
    return {"key": "value"}

@pytest.fixture
def temp_dir(tmp_path):
    """Provide temporary directory."""
    return tmp_path

def test_with_fixtures(sample_data, temp_dir):
    """Test using fixtures."""
    assert sample_data["key"] == "value"
    assert temp_dir.exists()
```

## Foundation Testing Patterns

### Foundation Reset (CRITICAL)

**Always reset Foundation state in tests:**

```python
import pytest
from provide.testkit import reset_foundation_setup_for_testing

@pytest.fixture(autouse=True)
def reset_foundation():
    """Reset Foundation state before each test."""
    reset_foundation_setup_for_testing()
```

**Why this matters:**
- Foundation maintains global state (logger, hub, config)
- Tests can interfere with each other without reset
- Ensures clean state for each test

### Capturing Logs in Tests

```python
from provide.testkit import set_log_stream_for_testing
from io import StringIO

def test_logging_output():
    """Test log messages."""
    log_stream = StringIO()
    set_log_stream_for_testing(log_stream)

    from provide.foundation import logger
    logger.info("test message", value=42)

    output = log_stream.getvalue()
    assert "test message" in output
    assert "42" in output
```

### Testing Hub Components

```python
from provide.foundation.hub import get_hub

def test_hub_component():
    """Test Hub initialization."""
    hub = get_hub()
    hub.initialize_foundation()

    # Test hub functionality
    assert hub.is_initialized
```

## Async Testing Patterns

### Basic Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_async_operation():
    """Test async function."""
    result = await my_async_function()
    assert result is not None
```

### Async Fixtures

```python
@pytest.fixture
async def async_client():
    """Provide async client."""
    client = AsyncClient()
    await client.connect()
    yield client
    await client.disconnect()

@pytest.mark.asyncio
async def test_with_async_client(async_client):
    """Test using async client."""
    result = await async_client.fetch_data()
    assert result
```

### Testing Concurrent Operations

```python
import asyncio
import pytest

@pytest.mark.asyncio
async def test_concurrent_operations():
    """Test multiple concurrent operations."""
    tasks = [
        async_operation(1),
        async_operation(2),
        async_operation(3)
    ]
    results = await asyncio.gather(*tasks)
    assert len(results) == 3
    assert all(r is not None for r in results)
```

## Integration Testing

### Cross-Component Tests

```python
def test_integration_flow():
    """Test complete workflow."""
    # Setup
    config = load_config()
    manager = Manager(config)

    # Execute workflow
    result = manager.process_item(test_item)

    # Verify
    assert result.success
    assert result.output is not None
```

### Testing with External Dependencies

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_http_client():
    """Mock HTTP client."""
    with patch('httpx.Client') as mock:
        mock.return_value.get.return_value.json.return_value = {"status": "ok"}
        yield mock

def test_with_mock_http(mock_http_client):
    """Test using mocked HTTP client."""
    result = function_that_uses_http()
    assert result["status"] == "ok"
```

## File Operation Testing

### Testing File Operations

```python
from pathlib import Path

def test_file_operations(tmp_path):
    """Test file read/write."""
    test_file = tmp_path / "test.txt"

    # Write
    test_file.write_text("test content")

    # Read
    content = test_file.read_text()
    assert content == "test content"
```

### Testing Atomic Writes

```python
from provide.foundation.file.atomic import atomic_write

def test_atomic_write(tmp_path):
    """Test atomic file writing."""
    target = tmp_path / "output.txt"

    with atomic_write(target) as f:
        f.write("atomic content")

    assert target.exists()
    assert target.read_text() == "atomic content"
```

## Error Testing

### Testing Expected Exceptions

```python
import pytest
from my_module import MyError

def test_raises_error():
    """Test that error is raised."""
    with pytest.raises(MyError) as exc_info:
        function_that_raises()

    assert "expected message" in str(exc_info.value)
```

### Testing Error Messages

```python
def test_error_message():
    """Test error message content."""
    try:
        function_that_fails()
        pytest.fail("Expected exception was not raised")
    except ValueError as e:
        assert "specific error" in str(e)
        assert e.args[0] == "expected argument"
```

## Performance Testing

### Testing with Timeouts

```python
import pytest

@pytest.mark.timeout(5)
def test_completes_quickly():
    """Test completes within 5 seconds."""
    slow_operation()
```

### Benchmarking

```python
import pytest

@pytest.mark.benchmark
def test_performance(benchmark):
    """Benchmark function performance."""
    result = benchmark(expensive_function, arg1, arg2)
    assert result is not None
```

## Parametrized Testing

### Basic Parametrization

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("test", "TEST"),
])
def test_upper(input, expected):
    """Test uppercase conversion."""
    assert input.upper() == expected
```

### Complex Parametrization

```python
@pytest.mark.parametrize("config", [
    {"mode": "sync", "timeout": 30},
    {"mode": "async", "timeout": 60},
])
def test_with_config(config):
    """Test with different configurations."""
    result = process_with_config(config)
    assert result.mode == config["mode"]
```

## Project-Specific Patterns

### FlavorPack Testing

**Use pretaster/taster for PSPF validation:**

```bash
# Run PSPF validation tests
make validate-pspf

# Test specific builder/launcher combo
make validate-pspf-combo
```

**Never create standalone test packages:**
```python
# ❌ DON'T: Create test packages in /tmp
test_package = create_package("/tmp/test.psp")

# ✅ DO: Use pretaster
from tests.pretaster import validate_package
validate_package(package_spec)
```

### Pyvider RPC Plugin Testing

**Always reset Foundation:**

```python
import pytest
from provide.testkit import reset_foundation_setup_for_testing

@pytest.fixture(autouse=True)
def reset_foundation():
    """Reset Foundation state."""
    reset_foundation_setup_for_testing()

@pytest.mark.asyncio
async def test_rpc_server():
    """Test RPC server."""
    server = plugin_server(protocol, handler)
    # Test server functionality
```

### TofuSoup Conformance Testing

**Run via CLI or pytest:**

```bash
# Via soup CLI
soup test cty
soup test hcl
soup test rpc

# Via pytest
uv run pytest conformance/cty/ -v
uv run pytest -m cty
```

**Test harness integration:**

```python
def test_with_harness():
    """Test using Go harness."""
    result = run_harness_command(["cty", "view", "test.json"])
    assert result.returncode == 0
```

### SupSrc Event Testing

**Complete event sequences required:**

```python
import asyncio

async def test_atomic_detection():
    """Test atomic save detection."""
    buffer = EventBuffer(mode="smart")

    # Send complete sequence
    buffer.add_event(create_event)
    buffer.add_event(modify_event)
    buffer.add_event(move_event)

    # Wait for detection window + post-delay + margin
    await asyncio.sleep(0.15)

    # Flush and verify
    groups = buffer.flush_all()
    assert len(groups) == 1
```

## Test Markers

### Standard Markers

```python
@pytest.mark.slow          # Long-running tests
@pytest.mark.integration   # Integration tests
@pytest.mark.unit          # Unit tests
@pytest.mark.asyncio       # Async tests
@pytest.mark.benchmark     # Performance benchmarks
```

### Running by Marker

```bash
# Skip slow tests
uv run pytest -m "not slow"

# Only integration tests
uv run pytest -m integration

# Unit tests excluding slow ones
uv run pytest -m "unit and not slow"
```

## Coverage Best Practices

### Measuring Coverage

```bash
# Generate coverage report
uv run pytest --cov=PACKAGE --cov-report=term-missing

# HTML report for detailed view
uv run pytest --cov=PACKAGE --cov-report=html
open htmlcov/index.html

# Fail if coverage below threshold
uv run pytest --cov=PACKAGE --cov-fail-under=80
```

### Coverage Configuration

**In pyproject.toml:**

```toml
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/site-packages/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

## Testing Checklist

Before pushing code, ensure:

- [ ] All tests pass locally
- [ ] New features have tests
- [ ] Bug fixes have regression tests
- [ ] Coverage doesn't decrease
- [ ] Tests are fast (use markers for slow tests)
- [ ] Async tests use proper fixtures
- [ ] Foundation reset fixture used where needed
- [ ] No test pollution (each test independent)
- [ ] Clear test names and docstrings

## Troubleshooting Tests

### Tests Pass Individually, Fail Together

**Cause:** Shared state not being reset

**Solution:**
```python
@pytest.fixture(autouse=True)
def reset_state():
    """Reset state before each test."""
    global_state.clear()
    yield
    global_state.clear()
```

### Async Tests Hang

**Cause:** Unclosed resources or infinite loops

**Solution:**
```python
@pytest.mark.timeout(10)
@pytest.mark.asyncio
async def test_with_timeout():
    """Test with timeout to prevent hanging."""
    await operation_that_might_hang()
```

### Flaky Tests

**Cause:** Race conditions or timing issues

**Solution:**
```python
import asyncio

async def test_with_retry():
    """Test with retry for flaky operations."""
    for _ in range(3):
        try:
            result = await flaky_operation()
            assert result
            break
        except AssertionError:
            await asyncio.sleep(0.1)
    else:
        pytest.fail("Test failed after 3 retries")
```

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [provide-testkit API Reference](../packages/testkit.md)

---

**Related Guides:**
- [Development Workflow Guide](development-workflow.md) - Daily development patterns
- [IDE Setup Guide](ide-setup.md) - Configure testing in your IDE
