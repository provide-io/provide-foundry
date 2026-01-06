# Testing Guide

Comprehensive guide to testing Terraform providers built with Pyvider and the provide.foundation ecosystem.

## Overview

Testing is crucial for reliable Terraform providers. This guide covers unit testing, integration testing, acceptance testing, and advanced testing patterns using the provide-testkit framework.

## Testing Strategy

### Test Pyramid

1. **Unit Tests** (70%): Fast, isolated tests of individual components
2. **Integration Tests** (20%): Tests with real API interactions
3. **Acceptance Tests** (10%): Full Terraform workflow tests

### Test Categories

- **Schema validation**: Ensure correct Terraform schema definition
- **Resource lifecycle**: Test create, read, update, delete operations
- **Data source functionality**: Validate data source behavior
- **Error handling**: Test error conditions and edge cases
- **State management**: Verify state consistency and migration

## Unit Testing

### Basic Setup

```python
import pytest
from unittest.mock import Mock, patch
from provide.testkit import TestCase, fixtures

class TestServerResource(TestCase):
    """Unit tests for server resource."""

    def setUp(self):
        """Set up test fixtures."""
        self.provider = Mock()
        self.provider.client = Mock()
        self.resource = ServerResource(provider=self.provider)

    def test_create_server_success(self):
        """Test successful server creation."""
        # Arrange
        self.provider.client.create_server.return_value = {
            "id": "srv-123",
            "name": "test-server",
            "status": "active",
            "created_at": "2023-01-01T00:00:00Z"
        }

        config = Mock()
        config.name = "test-server"
        config.size = "small"
        config.region = "us-east-1"

        # Act
        result = self.resource.create(config)

        # Assert
        self.assertEqual(result.id, "srv-123")
        self.assertEqual(result.name, "test-server")
        self.assertEqual(result.status, "active")

        self.provider.client.create_server.assert_called_once_with({
            "name": "test-server",
            "size": "small",
            "region": "us-east-1"
        })

    def test_create_server_api_error(self):
        """Test server creation with API error."""
        # Arrange
        from myservice.exceptions import APIError
        self.provider.client.create_server.side_effect = APIError(
            "Server name already exists",
            status_code=409
        )

        config = Mock()
        config.name = "duplicate-server"

        # Act & Assert
        with self.assertRaises(ResourceError) as cm:
            self.resource.create(config)

        self.assertIn("already exists", str(cm.exception))
        self.assertFalse(cm.exception.retryable)
```

### Testing with Fixtures

```python
from provide.testkit import fixtures

class TestServerResource(TestCase):
    """Tests using testkit fixtures."""

    @fixtures.temp_directory
    def test_config_file_handling(self, temp_dir):
        """Test configuration file handling."""
        config_file = temp_dir / "provider.yaml"
        config_file.write_text("""
        api_url: https://test.example.com
        api_key: test-key-123
        """)

        provider = self.create_provider_from_config(config_file)
        self.assertEqual(provider.config.api_url, "https://test.example.com")

    @fixtures.mock_time("2023-01-01T00:00:00Z")
    def test_timestamp_handling(self):
        """Test with fixed timestamp."""
        resource = self.create_resource()
        result = resource.create()

        self.assertEqual(result.created_at, "2023-01-01T00:00:00Z")
```

### Schema Testing

```python
class TestResourceSchema(TestCase):
    """Test resource schema definition."""

    def test_required_attributes(self):
        """Test required attribute validation."""
        schema = ServerResource.get_schema()

        # Verify required attributes
        self.assertTrue(schema.attributes["name"].required)
        self.assertTrue(schema.attributes["region"].required)
        self.assertFalse(schema.attributes["size"].required)

    def test_attribute_types(self):
        """Test attribute type definitions."""
        schema = ServerResource.get_schema()

        # Verify attributes exist in the schema
        self.assertIn("name", schema.attributes)
        self.assertIn("port", schema.attributes)
        self.assertIn("enabled", schema.attributes)

        # Verify attribute properties
        self.assertTrue(schema.attributes["name"].required)
        self.assertEqual(schema.attributes["port"].default, 8080)
        self.assertEqual(schema.attributes["enabled"].default, True)

    def test_validation_rules(self):
        """Test custom validation rules."""
        with self.assertRaises(ValidationError):
            ServerResource.validate({
                "name": "",  # Empty name should fail
                "region": "us-east-1"
            })

        with self.assertRaises(ValidationError):
            ServerResource.validate({
                "name": "test-server",
                "size": "invalid-size"  # Invalid size should fail
            })
```

## Integration Testing

### API Integration Tests

```python
from provide.testkit import IntegrationTestCase

class TestServerResourceIntegration(IntegrationTestCase):
    """Integration tests with real API."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.provider = cls.create_test_provider({
            "api_url": cls.get_test_api_url(),
            "api_key": cls.get_test_api_key()
        })

    def setUp(self):
        """Set up each test."""
        self.cleanup_resources = []

    def tearDown(self):
        """Clean up test resources."""
        for resource in self.cleanup_resources:
            try:
                resource.delete()
            except Exception:
                pass  # Resource may already be deleted

    def test_server_lifecycle(self):
        """Test complete server lifecycle."""
        # Create server
        server = self.create_resource("myservice_server", {
            "name": f"test-server-{self.test_id}",
            "size": "small",
            "region": "us-east-1"
        })
        self.cleanup_resources.append(server)

        # Verify creation
        self.assertIsNotNone(server.id)
        self.assertEqual(server.status, "active")

        # Test read (refresh)
        refreshed = server.read()
        self.assertEqual(refreshed.id, server.id)
        self.assertEqual(refreshed.name, server.name)

        # Test update
        updated = server.update({
            "name": f"updated-server-{self.test_id}"
        })
        self.assertEqual(updated.name, f"updated-server-{self.test_id}")

        # Test delete
        server.delete()

        # Verify deletion
        with self.assertRaises(NotFoundError):
            server.read()

    def test_concurrent_operations(self):
        """Test concurrent resource operations."""
        import concurrent.futures
        import threading

        def create_server(index):
            return self.create_resource("myservice_server", {
                "name": f"concurrent-server-{index}-{self.test_id}",
                "size": "small",
                "region": "us-east-1"
            })

        # Create servers concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(create_server, i)
                for i in range(5)
            ]

            servers = [
                future.result(timeout=30)
                for future in concurrent.futures.as_completed(futures)
            ]

        # Verify all servers created successfully
        self.assertEqual(len(servers), 5)
        for server in servers:
            self.assertIsNotNone(server.id)
            self.cleanup_resources.append(server)
```

### Error Condition Testing

```python
class TestErrorHandling(IntegrationTestCase):
    """Test error handling scenarios."""

    def test_network_timeout(self):
        """Test handling of network timeouts."""
        with patch('requests.post') as mock_post:
            mock_post.side_effect = requests.Timeout("Request timeout")

            with self.assertRaises(ProviderError) as cm:
                self.create_resource("myservice_server", {
                    "name": "timeout-test",
                    "region": "us-east-1"
                })

            self.assertTrue(cm.exception.retryable)

    def test_rate_limiting(self):
        """Test rate limiting handling."""
        # Simulate rate limiting by making many rapid requests
        for i in range(100):
            try:
                self.create_resource("myservice_server", {
                    "name": f"rate-test-{i}",
                    "region": "us-east-1"
                })
            except ProviderError as e:
                if "rate limit" in str(e).lower():
                    self.assertTrue(e.retryable)
                    break
        else:
            self.skipTest("Rate limiting not triggered")

    def test_invalid_credentials(self):
        """Test handling of invalid credentials."""
        invalid_provider = self.create_test_provider({
            "api_url": self.get_test_api_url(),
            "api_key": "invalid-key-123"
        })

        with self.assertRaises(ProviderError) as cm:
            invalid_provider.create_resource("myservice_server", {
                "name": "auth-test",
                "region": "us-east-1"
            })

        self.assertIn("authentication", str(cm.exception).lower())
```

## Acceptance Testing

### Terraform Acceptance Tests

```python
from provide.testkit import AcceptanceTestCase

class TestServerResourceAcceptance(AcceptanceTestCase):
    """Terraform acceptance tests."""

    def test_basic_server_creation(self):
        """Test basic server creation through Terraform."""
        config = '''
        resource "myservice_server" "test" {
          name   = "acceptance-test-server"
          size   = "small"
          region = "us-east-1"
        }
        '''

        with self.terraform_config(config) as tf:
            # Apply configuration
            tf.apply()

            # Verify resource exists
            state = tf.state()
            server = state.resources["myservice_server.test"]

            self.assertEqual(server.attributes["name"], "acceptance-test-server")
            self.assertEqual(server.attributes["size"], "small")
            self.assertIsNotNone(server.attributes["id"])

            # Test import
            imported_state = tf.import_resource(
                "myservice_server.test_import",
                server.attributes["id"]
            )

            self.assertEqual(
                imported_state.attributes["name"],
                server.attributes["name"]
            )

            # Test plan shows no changes
            plan = tf.plan()
            self.assertEqual(len(plan.changes), 0)

    def test_server_update(self):
        """Test server updates through Terraform."""
        initial_config = '''
        resource "myservice_server" "test" {
          name   = "update-test-server"
          size   = "small"
          region = "us-east-1"
        }
        '''

        updated_config = '''
        resource "myservice_server" "test" {
          name   = "updated-test-server"
          size   = "medium"
          region = "us-east-1"
        }
        '''

        with self.terraform_config(initial_config) as tf:
            # Initial apply
            tf.apply()
            initial_state = tf.state()
            initial_id = initial_state.resources["myservice_server.test"].attributes["id"]

            # Update configuration
            tf.update_config(updated_config)

            # Plan should show update
            plan = tf.plan()
            self.assertEqual(len(plan.changes), 1)
            self.assertEqual(plan.changes[0].action, "update")

            # Apply update
            tf.apply()

            # Verify update
            updated_state = tf.state()
            server = updated_state.resources["myservice_server.test"]

            self.assertEqual(server.attributes["id"], initial_id)  # ID unchanged
            self.assertEqual(server.attributes["name"], "updated-test-server")
            self.assertEqual(server.attributes["size"], "medium")

    def test_data_source(self):
        """Test data source functionality."""
        config = '''
        data "myservice_image" "test" {
          name_filter = "ubuntu"
          os_type     = "linux"
        }

        output "image_count" {
          value = length(data.myservice_image.test.images)
        }
        '''

        with self.terraform_config(config) as tf:
            tf.apply()

            outputs = tf.outputs()
            self.assertGreater(outputs["image_count"], 0)

            state = tf.state()
            images = state.data_sources["myservice_image.test"].attributes["images"]

            # Verify all images match filter
            for image in images:
                self.assertIn("ubuntu", image["name"].lower())
                self.assertEqual(image["os_type"], "linux")
```

### Cross-Version Testing

```python
class TestProviderCompatibility(AcceptanceTestCase):
    """Test provider version compatibility."""

    def test_state_migration(self):
        """Test state migration between provider versions."""
        # Create resource with old provider version
        with self.provider_version("1.0.0"):
            config = '''
            resource "myservice_server" "test" {
              name          = "migration-test"
              instance_type = "small"  # Old attribute name
              region        = "us-east-1"
            }
            '''

            with self.terraform_config(config) as tf:
                tf.apply()
                old_state = tf.state()

        # Upgrade to new provider version
        with self.provider_version("2.0.0"):
            updated_config = '''
            resource "myservice_server" "test" {
              name   = "migration-test"
              size   = "small"  # New attribute name
              region = "us-east-1"
            }
            '''

            with self.terraform_config(updated_config, state=old_state) as tf:
                # Plan should show no changes (migration handled automatically)
                plan = tf.plan()
                self.assertEqual(len(plan.changes), 0)

                tf.apply()
                new_state = tf.state()

                # Verify state was migrated correctly
                server = new_state.resources["myservice_server.test"]
                self.assertEqual(server.attributes["size"], "small")
                self.assertNotIn("instance_type", server.attributes)
```

## Performance Testing

### Load Testing

```python
from provide.testkit import PerformanceTestCase

class TestProviderPerformance(PerformanceTestCase):
    """Performance and load testing."""

    def test_bulk_resource_creation(self):
        """Test creating many resources efficiently."""
        resource_count = 50

        with self.measure_time() as timer:
            servers = []
            for i in range(resource_count):
                server = self.create_resource("myservice_server", {
                    "name": f"bulk-test-{i}",
                    "size": "small",
                    "region": "us-east-1"
                })
                servers.append(server)

        # Verify performance targets
        avg_time_per_resource = timer.elapsed / resource_count
        self.assertLess(avg_time_per_resource, 2.0)  # Less than 2s per resource

        # Clean up
        for server in servers:
            server.delete()

    def test_concurrent_reads(self):
        """Test concurrent read operations."""
        # Create test server
        server = self.create_resource("myservice_server", {
            "name": "read-test-server",
            "size": "small",
            "region": "us-east-1"
        })

        def read_server():
            return server.read()

        # Perform concurrent reads
        with self.measure_concurrent_operations(read_server, workers=10, operations=100) as results:
            # Verify all operations succeeded
            self.assertEqual(len(results.successes), 100)
            self.assertEqual(len(results.failures), 0)

            # Verify performance
            self.assertLess(results.avg_duration, 0.5)  # Less than 500ms average

        server.delete()
```

## Test Configuration

### Test Environment Setup

```yaml
# tests/config/test_config.yaml
test_environments:
  unit:
    mock_api: true
    log_level: ERROR

  integration:
    api_url: https://api-staging.example.com
    api_key: ${TEST_API_KEY}
    log_level: INFO
    cleanup_resources: true

  acceptance:
    api_url: https://api-test.example.com
    api_key: ${ACCEPTANCE_API_KEY}
    log_level: DEBUG
    terraform_version: "1.5.0"
    cleanup_resources: true

performance_targets:
  resource_creation_time: 2.0  # seconds
  bulk_operation_throughput: 25  # resources per second
  concurrent_read_latency: 0.5  # seconds
```

### Test Runners

```python
# conftest.py - pytest configuration
import pytest
from provide.testkit import configure_testing

def pytest_configure(config):
    """Configure pytest for provider testing."""
    configure_testing(
        config_file="tests/config/test_config.yaml",
        environment=config.getoption("--test-env", default="unit")
    )

def pytest_addoption(parser):
    """Add custom pytest options."""
    parser.addoption(
        "--test-env",
        choices=["unit", "integration", "acceptance"],
        default="unit",
        help="Test environment to use"
    )

    parser.addoption(
        "--cleanup",
        action="store_true",
        default=False,
        help="Clean up test resources after running"
    )

@pytest.fixture(scope="session")
def test_provider():
    """Provide test provider instance."""
    from provide.testkit import create_test_provider
    return create_test_provider()
```

### Running Tests

```bash
# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/ --test-env=integration

# Acceptance tests
pytest tests/acceptance/ --test-env=acceptance

# Performance tests
pytest tests/performance/ --test-env=integration

# All tests with coverage
pytest --cov=src/ --cov-report=html

# Specific test patterns
pytest -k "test_server" -v

# Parallel execution
pytest -n auto --dist worksteal
```

## Continuous Integration

### GitHub Actions Configuration

```yaml
# .github/workflows/test.yml
name: Test Provider

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
    - uses: actions/checkout@v3

    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        uv sync --all-groups

    - name: Run unit tests
      run: |
        source .venv/bin/activate
        pytest tests/unit/ --cov=src/ --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests

    steps:
    - uses: actions/checkout@v3

    - name: Run integration tests
      env:
        TEST_API_KEY: ${{ secrets.TEST_API_KEY }}
      run: |
        uv sync --all-groups
        source .venv/bin/activate
        pytest tests/integration/ --test-env=integration

  acceptance-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v3

    - uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: 1.5.0

    - name: Run acceptance tests
      env:
        ACCEPTANCE_API_KEY: ${{ secrets.ACCEPTANCE_API_KEY }}
      run: |
        uv sync --all-groups
        source .venv/bin/activate
        pytest tests/acceptance/ --test-env=acceptance
```

## Best Practices

### Test Organization

- Organize tests by functionality (unit/integration/acceptance)
- Use descriptive test names that explain the scenario
- Group related tests in test classes
- Use setup/teardown methods for resource management

### Test Data Management

- Use factories for creating test data
- Avoid hardcoded values; use parameterized tests
- Clean up test resources reliably
- Use unique identifiers to avoid conflicts

### Assertion Strategies

- Test both positive and negative scenarios
- Verify state changes explicitly
- Test error conditions and edge cases
- Use specific assertions over generic ones

### Test Maintenance

- Keep tests simple and focused
- Update tests when adding new features
- Remove or update obsolete tests
- Monitor test performance and reliability

## Related Documentation

- **[Provider Development Guide](provider-development.md)** - Building providers with Pyvider
- **[API Reference](https://foundry.provide.io/provide-testkit/api/)** - Complete testing framework API
- **[Packaging Guide](packaging.md)** - Preparing providers for distribution
