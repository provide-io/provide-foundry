# tofusoup

Cross-language conformance testing framework for ensuring compatibility and consistency across polyglot systems in the provide.foundation ecosystem.

## Overview

`tofusoup` is a comprehensive testing framework designed to validate conformance and compatibility across multiple programming languages and implementations. It ensures that polyglot systems maintain consistent behavior, data formats, and protocol implementations.

### Key Features

#### 🌐 **Cross-Language Testing**
- **Multi-language support**: Test compatibility between Python, Go, TypeScript, Rust, and more
- **Implementation validation**: Ensure different language implementations behave identically
- **Protocol conformance**: Validate that implementations follow the same protocols
- **Data format consistency**: Verify consistent data serialization/deserialization

#### ✅ **Conformance Validation**
- **Specification compliance**: Ensure implementations meet defined specifications
- **Behavioral testing**: Validate that all implementations produce identical results
- **Edge case handling**: Test boundary conditions and error scenarios
- **Regression testing**: Detect when implementations drift apart

#### 📡 **Protocol Testing**
- **Communication protocols**: Validate RPC, REST, and other communication protocols
- **Message formats**: Test Protocol Buffers, JSON, and other message formats
- **Transport layers**: Validate TCP, UDP, Unix sockets, and other transports
- **Security protocols**: Test authentication, authorization, and encryption

#### 📋 **Schema Validation**
- **Type system validation**: Ensure consistent type definitions across languages
- **Schema evolution**: Test forward and backward compatibility of schemas
- **Serialization formats**: Validate JSON, Protocol Buffers, MessagePack, etc.
- **Data integrity**: Ensure data remains consistent across language boundaries

#### 🔗 **Integration Testing**
- **End-to-end testing**: Test complete workflows across multiple services
- **Service composition**: Validate that services work together correctly
- **Dependency validation**: Test interactions between different components
- **Environment consistency**: Ensure behavior is consistent across environments

#### ⚡ **Performance Benchmarking**
- **Cross-language performance**: Compare performance across implementations
- **Regression detection**: Identify performance regressions over time
- **Resource usage**: Monitor memory, CPU, and network usage
- **Scalability testing**: Test performance under load

## Installation

```bash
# Basic installation
uv add tofusoup

# With all extras for full functionality
uv add tofusoup[all]

# Development installation
uv add tofusoup[dev]
```

## Quick Start

### Basic Conformance Testing

```python
from tofusoup import ConformanceTest, Protocol

# Define a cross-language test
test = ConformanceTest("user-api")
test.add_implementation("python", "api.py")
test.add_implementation("go", "api.go")
test.add_implementation("typescript", "api.ts")

# Run conformance validation
results = test.validate()
print(f"Conformance: {results.all_passed}")
```

### Protocol Testing

```python
from tofusoup import ProtocolTest, MessageFormat

# Test a gRPC service across languages
protocol_test = ProtocolTest("user-service")
protocol_test.set_format(MessageFormat.PROTOBUF)

# Add implementations
protocol_test.add_server("python", "server.py")
protocol_test.add_client("go", "client.go")

# Run protocol tests
results = protocol_test.run_tests()
```

### Schema Validation

```python
from tofusoup import SchemaValidator, SerializationFormat

# Validate schema consistency
validator = SchemaValidator()
validator.add_schema("user", "user.proto")

# Test across serialization formats
results = validator.validate_formats([
    SerializationFormat.JSON,
    SerializationFormat.PROTOBUF,
    SerializationFormat.MESSAGEPACK
])
```

### Performance Benchmarking

```python
from tofusoup import PerformanceBenchmark

# Create benchmark suite
benchmark = PerformanceBenchmark("api-performance")
benchmark.add_implementation("python", "api_server.py")
benchmark.add_implementation("go", "api_server.go")
benchmark.add_implementation("rust", "api_server.rs")

# Run performance tests
results = benchmark.run_benchmarks(
    duration="60s",
    concurrent_users=100
)

print(f"Python RPS: {results['python'].requests_per_second}")
print(f"Go RPS: {results['go'].requests_per_second}")
print(f"Rust RPS: {results['rust'].requests_per_second}")
```

## Testing Strategies

### **Specification-Driven Testing**
Define tests based on formal specifications and validate that all implementations conform to the specification.

### **Reference Implementation Testing**
Use one implementation as a reference and validate that others behave identically.

### **Differential Testing**
Compare outputs from multiple implementations for the same inputs to detect inconsistencies.

### **Property-Based Testing**
Generate test cases based on properties that should hold across all implementations.

## Advanced Features

### Custom Test Runners

```python
from tofusoup import TestRunner, TestCase

class CustomAPITest(TestCase):
    def setup(self):
        # Setup test environment
        pass

    def run_test(self, implementation):
        # Custom test logic
        response = implementation.call_api("/users/1")
        return response.status_code == 200

runner = TestRunner()
runner.add_test_case(CustomAPITest())
```

### Continuous Integration

```python
from tofusoup import CIIntegration

# Generate CI configuration
ci = CIIntegration()
ci.generate_github_actions("conformance-tests")
ci.generate_gitlab_ci("conformance-tests")
```

### Test Report Generation

```python
from tofusoup import ReportGenerator

# Generate comprehensive test reports
reporter = ReportGenerator()
reporter.add_results(conformance_results)
reporter.add_results(performance_results)

# Export reports
reporter.export_html("test-report.html")
reporter.export_json("test-results.json")
reporter.export_junit("junit-results.xml")
```

## Use Cases

### **Polyglot Microservices**
Ensure that microservices written in different languages maintain consistent behavior and can communicate correctly.

### **API Compatibility**
Validate that API implementations in different languages provide identical functionality and responses.

### **Protocol Implementation**
Test that protocol implementations (gRPC, REST, GraphQL) behave consistently across languages.

### **Library Validation**
Ensure that library ports maintain the same behavior and API across programming languages.

### **Migration Testing**
Validate that migrated services maintain the same behavior as the original implementation.

## Integration with Foundation

TofuSoup integrates with other provide.foundation tools:

- **provide-foundation**: Uses Foundation's logging and configuration systems
- **pyvider**: Tests Terraform provider implementations across languages
- **plating**: Generates test templates and scaffolding
- **supsrc**: Automated test execution and reporting

## Related Documentation

- **[API Reference](../api/tofusoup.md)** - Complete API documentation
- **[Testing Guide](../guides/conformance-testing.md)** - Best practices for conformance testing
- **[Performance Testing](../guides/performance-testing.md)** - Performance benchmarking strategies

## Repository

- **Repository**: [tofusoup](https://github.com/provide-io/tofusoup)
- **Package**: `tofusoup` on PyPI
- **License**: MIT