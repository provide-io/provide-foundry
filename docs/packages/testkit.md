# provide-testkit

Comprehensive testing utilities and fixtures for the Provide Foundry, organized by domain to provide everything you need for testing Foundation-based applications.

## Overview

`provide-testkit` is a batteries-included testing framework that provides pytest fixtures, mocking utilities, and testing helpers organized by domain (file, process, transport, crypto, etc.). It's designed to make testing in the Provide Foundry both powerful and enjoyable.

### Key Features

- **🗂️ Domain-Organized Fixtures**: Logical organization by testing domain
- **🔄 Lazy Loading**: Minimal production overhead with smart import system
- **🧪 Comprehensive Coverage**: File, process, network, crypto, and more
- **⚡ Performance Focused**: Optimized fixtures with proper scoping
- **🔧 pytest Integration**: Seamless integration with pytest ecosystem

## Installation

```bash
# Basic installation
uv add provide-testkit

# With optional extras for specific domains
uv add provide-testkit[transport]  # HTTP testing
uv add provide-testkit[crypto]     # Cryptographic testing
uv add provide-testkit[process]    # Process monitoring
uv add provide-testkit[all]        # Everything
```

## Quick Start

```python
import pytest
from provide.testkit import temp_directory, mock_server, client_cert

def test_with_temp_files(temp_directory):
    """Test using temporary directory fixture."""
    config_file = temp_directory / "config.json"
    config_file.write_text('{"debug": true}')

    assert config_file.exists()
    assert json.loads(config_file.read_text())["debug"] is True
    # Cleanup is automatic

@pytest.mark.asyncio
async def test_with_mock_server(mock_server):
    """Test with mock HTTP server."""
    mock_server.add_response("/api/data", {"status": "ok"})

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{mock_server.url}/api/data")
        assert response.json()["status"] == "ok"

def test_with_certificates(client_cert, server_cert, ca_cert):
    """Test with generated TLS certificates."""
    # Certificates are automatically generated and valid
    assert client_cert.exists()
    assert validate_cert_chain(client_cert, ca_cert)
```

## Fixture Domains

### 📁 File Domain

Testing filesystem operations, directory structures, and file content:

```python
from provide.testkit import (
    temp_directory,          # Temporary directory with auto-cleanup
    test_files_structure,    # Pre-defined file structures
    binary_file,            # Binary test files
    large_file,             # Large file generation
    file_permissions,       # Permission testing
)

def test_directory_structure(test_files_structure):
    """Test with predefined directory structure."""
    assert test_files_structure["README.md"].exists()
    assert test_files_structure["src/main.py"].is_file()
    assert test_files_structure["tests"].is_dir()
```

**Available Fixtures:**
- `temp_directory` - Temporary directory with Path interface
- `test_files_structure` - Complex directory structures
- `binary_file` - Binary content generation
- `large_file` - Large file creation for performance testing
- `file_permissions` - File permission testing utilities
- `symlink_target` - Symbolic link testing

### ⚡ Process Domain

Testing async operations, subprocesses, and event loops:

```python
from provide.testkit import (
    clean_event_loop,       # Fresh event loop for each test
    async_timeout,          # Timeout context manager
    mock_async_process,     # Mock subprocess execution
    process_monitor,        # Monitor process resources
)

@pytest.mark.asyncio
async def test_async_operation(clean_event_loop, async_timeout):
    """Test async operations with clean event loop."""
    async with async_timeout(5.0):
        result = await long_running_operation()
        assert result.success

def test_subprocess_mock(mock_async_process):
    """Test subprocess execution with mocking."""
    mock_async_process.set_output("echo hello", "hello\n")
    result = subprocess.run(["echo", "hello"], capture_output=True)
    assert result.stdout.decode() == "hello\n"
```

**Available Fixtures:**
- `clean_event_loop` - Fresh asyncio event loop
- `async_timeout` - Async timeout context manager
- `mock_async_process` - Subprocess mocking
- `process_monitor` - Resource monitoring
- `event_emitter` - Event emitter testing

### 🌐 Transport Domain

Testing network operations, HTTP clients, and servers:

```python
from provide.testkit import (
    free_port,              # Get available network port
    mock_server,            # HTTP server mock
    httpx_mock_responses,   # httpx response mocking
    websocket_server,       # WebSocket testing
    grpc_channel,          # gRPC testing utilities
)

def test_with_free_port(free_port):
    """Test with guaranteed free port."""
    server = start_server(port=free_port)
    assert server.is_listening

def test_http_client(httpx_mock_responses):
    """Test HTTP client with mocked responses."""
    httpx_mock_responses.add("GET", "/api/users", json={"users": []})

    client = APIClient()
    users = client.get_users()
    assert users == []
```

**Available Fixtures:**
- `free_port` - Find available network port
- `mock_server` - Full HTTP server mock
- `httpx_mock_responses` - httpx response mocking
- `websocket_server` - WebSocket server for testing
- `grpc_channel` - gRPC channel and service mocking

### 🧵 Threading Domain

Testing concurrent operations and thread safety:

```python
from provide.testkit import (
    thread_pool,            # Managed thread pool
    thread_safe_list,       # Thread-safe data structures
    lock_factory,           # Lock creation utilities
    barrier,                # Thread synchronization
    concurrent_executor,    # Concurrent execution helper
)

def test_thread_safety(thread_pool, thread_safe_list):
    """Test thread-safe operations."""
    def append_item(item):
        thread_safe_list.append(item)

    futures = [
        thread_pool.submit(append_item, i)
        for i in range(100)
    ]

    for future in futures:
        future.result()

    assert len(thread_safe_list) == 100
```

**Available Fixtures:**
- `thread_pool` - Managed ThreadPoolExecutor
- `thread_safe_list` - Thread-safe list implementation
- `thread_safe_dict` - Thread-safe dictionary
- `lock_factory` - Create various lock types
- `barrier` - Thread synchronization barrier
- `concurrent_executor` - Execute functions concurrently

### 🔐 Crypto Domain

Testing cryptographic operations and certificates:

```python
from provide.testkit import (
    client_cert,            # Client TLS certificate
    server_cert,            # Server TLS certificate
    ca_cert,                # Certificate Authority
    rsa_keypair,            # RSA key generation
    encryption_key,         # Symmetric encryption keys
)

def test_certificate_validation(client_cert, ca_cert):
    """Test certificate chain validation."""
    # Certificates are automatically generated
    cert_data = load_certificate(client_cert)
    assert cert_data.subject.CN == "test-client"
    assert validate_chain(client_cert, ca_cert)

def test_encryption(encryption_key):
    """Test symmetric encryption."""
    plaintext = b"sensitive data"
    ciphertext = encrypt(plaintext, encryption_key)
    decrypted = decrypt(ciphertext, encryption_key)
    assert decrypted == plaintext
```

**Available Fixtures:**
- `client_cert` - Client certificate with private key
- `server_cert` - Server certificate with private key
- `ca_cert` - Certificate Authority for signing
- `rsa_keypair` - RSA public/private key pair
- `ed25519_keypair` - Ed25519 key pair
- `encryption_key` - AES encryption key

### 📦 Archive Domain

Testing archive formats and compression:

```python
from provide.testkit import (
    zip_archive,            # ZIP file creation
    tar_archive,            # TAR archive testing
    compressed_file,        # Compression testing
    archive_extractor,      # Archive extraction
)

def test_archive_creation(zip_archive, temp_directory):
    """Test ZIP archive creation and extraction."""
    # Add files to archive
    zip_archive.add_file("README.md", b"# Test")
    zip_archive.add_file("src/main.py", b"print('hello')")

    # Extract and verify
    zip_archive.extract_to(temp_directory)
    assert (temp_directory / "README.md").read_text() == "# Test"
```

**Available Fixtures:**
- `zip_archive` - ZIP archive creation and manipulation
- `tar_archive` - TAR archive with compression options
- `compressed_file` - Various compression formats
- `archive_extractor` - Universal archive extraction

### ⏰ Time Domain

Testing with time manipulation and scheduling:

```python
from provide.testkit import (
    frozen_time,            # Freeze time for testing
    time_machine,           # Advanced time manipulation
    mock_sleep,             # Mock time.sleep
    scheduler,              # Task scheduling testing
)

def test_with_frozen_time(frozen_time):
    """Test with frozen time."""
    frozen_time.freeze("2024-01-01 12:00:00")

    start = datetime.now()
    time.sleep(60)  # Doesn't actually sleep
    end = datetime.now()

    assert start == end  # Time didn't advance

def test_time_travel(time_machine):
    """Test with time manipulation."""
    time_machine.set("2024-01-01")
    assert datetime.now().year == 2024

    time_machine.advance(days=30)
    assert datetime.now().month == 1
    assert datetime.now().day == 31
```

**Available Fixtures:**
- `frozen_time` - Freeze time at specific moment
- `time_machine` - Advanced time manipulation
- `mock_sleep` - Mock sleep without delays
- `scheduler` - Test scheduled tasks

## Advanced Usage

### Fixture Composition

Combine multiple fixtures for complex scenarios:

```python
def test_complex_scenario(
    temp_directory,
    mock_server,
    client_cert,
    frozen_time
):
    """Test combining multiple fixtures."""
    # Set up time
    frozen_time.freeze("2024-01-01")

    # Create config file
    config = temp_directory / "config.json"
    config.write_text(f'{{"server": "{mock_server.url}"}}')

    # Mock server response
    mock_server.add_response("/api/auth", {"token": "secret"})

    # Test with certificate
    client = SecureClient(config, cert=client_cert)
    response = client.authenticate()

    assert response.token == "secret"
    assert response.timestamp.year == 2024
```

### Parametrized Testing

Use fixtures with pytest parametrization:

```python
@pytest.mark.parametrize("compression", ["gzip", "bzip2", "xz"])
def test_compression_formats(compressed_file, compression):
    """Test different compression formats."""
    compressed_file.compress("test data", format=compression)
    decompressed = compressed_file.decompress()
    assert decompressed == "test data"
```

### Custom Fixtures

Extend testkit with your own fixtures:

```python
import pytest
from provide.testkit import temp_directory

@pytest.fixture
def database_fixture(temp_directory):
    """Custom database fixture."""
    db_path = temp_directory / "test.db"
    db = Database(db_path)
    db.initialize()

    yield db

    db.close()

def test_with_database(database_fixture):
    """Test using custom database fixture."""
    database_fixture.insert("users", {"name": "Alice"})
    users = database_fixture.query("users")
    assert len(users) == 1
```

## Configuration

### Fixture Scopes

Control fixture lifecycle with scopes:

```python
@pytest.fixture(scope="session")
def expensive_resource():
    """Create once per test session."""
    resource = create_expensive_resource()
    yield resource
    cleanup_resource(resource)

@pytest.fixture(scope="function")
def isolated_resource():
    """Create fresh for each test."""
    return create_isolated_resource()
```

### Environment Detection

Testkit automatically detects testing context:

```python
# Automatic detection via:
# - pytest in sys.modules
# - PYTEST_CURRENT_TEST environment variable
# - TESTING=true environment variable
# - unittest in sys.modules
# - 'test' in command line arguments
```

### Performance Optimization

Tips for optimal test performance:

1. **Use appropriate fixture scopes** - Session scope for expensive resources
2. **Leverage lazy loading** - Fixtures load only when needed
3. **Parallel execution** - Use pytest-xdist for parallel tests
4. **Mock external services** - Avoid real network calls
5. **Clean up resources** - Ensure proper cleanup in fixtures

## Integration Examples

### With provide-foundation

```python
from provide.foundation import logger
from provide.testkit import temp_directory

def test_logging_to_file(temp_directory):
    """Test foundation logging to file."""
    log_file = temp_directory / "app.log"
    log = logger.get_logger(__name__, file=log_file)

    log.info("Test message")

    assert "Test message" in log_file.read_text()
```

### With pyvider

```python
from pyvider.resources import register_resource, BaseResource
from provide.testkit import mock_server

@register_resource("test")
class TestResource(BaseResource):
    api_url: str

    def create(self):
        response = requests.post(f"{self.api_url}/create")
        return response.json()

def test_resource_creation(mock_server):
    """Test pyvider resource with mock server."""
    mock_server.add_response("/create", {"id": "123"})

    resource = TestResource(api_url=mock_server.url)
    result = resource.create()

    assert result["id"] == "123"
```

## Best Practices

1. **Use domain-specific fixtures** - Choose fixtures from the appropriate domain
2. **Avoid manual cleanup** - Let fixtures handle cleanup automatically
3. **Mock external dependencies** - Use mocks for external services
4. **Test in isolation** - Each test should be independent
5. **Use appropriate assertions** - Be specific in what you're testing
6. **Document test intent** - Clear test names and docstrings
7. **Leverage parametrization** - Test multiple scenarios efficiently

## Troubleshooting

### Common Issues

**Import errors:**
```python
# Ensure testkit is installed with required extras
uv add provide-testkit[all]
```

**Fixture not found:**
```python
# Check fixture is imported from correct domain
from provide.testkit import fixture_name  # Auto-imported
```

**Async test issues:**
```python
# Mark async tests properly
@pytest.mark.asyncio
async def test_async():
    pass
```

**Resource cleanup:**
```python
# Fixtures handle cleanup automatically
# Avoid manual cleanup in tests
```

## API Reference

For detailed API documentation, see the [API Reference](../provide-testkit/reference/).

## Contributing

We welcome contributions! <!-- See our [Contributing Guide](../../CONTRIBUTING.md) for details on: -->
- Adding new fixtures
- Improving existing fixtures
- Documentation improvements
- Bug fixes and feature requests

---

`provide-testkit` makes testing in the Provide Foundry a joy. With comprehensive fixtures organized by domain and automatic cleanup, you can focus on writing tests that matter.