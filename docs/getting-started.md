# Getting Started

Welcome to the provide.io ecosystem! This guide will get you up and running with all the tools you need to build Terraform providers, package applications, and manage your development workflow.

## Prerequisites

Before you start, ensure you have:

- **Python 3.11 or higher**
- **Git** for version control
- **A Unix-like environment** (macOS, Linux, or WSL on Windows)

!!! tip "Python Version"
    The provide.io ecosystem uses modern Python features and requires 3.11+. We recommend using [pyenv](https://github.com/pyenv/pyenv) to manage Python versions.

## Quick Setup

The fastest way to get started is to set up the entire ecosystem using our unified workspace:

```bash
# Clone the ecosystem repository
git clone https://github.com/provide-io/provide-io.git
cd provide-io

# Set up the unified development environment
uv sync --extra all --extra dev
source .venv/bin/activate
```

This single command:

- ✅ Installs UV package manager (if needed)
- ✅ Creates a unified virtual environment
- ✅ Installs all 13 ecosystem packages in editable mode
- ✅ Includes all development tools (ruff, mypy, pytest, etc.)
- ✅ Sets up proper dependency resolution between packages

!!! success "Verification"
    Verify your setup by running:
    ```bash
    python -c "import provide, pyvider; print('✅ Ecosystem ready!')"
    ```

## Your First Terraform Provider

Let's create a simple Terraform provider to see the framework in action:

### 1. Create a New Provider

```python title="my_provider.py"
from pyvider import provider, resource
from pyvider.schema import Attribute

@provider
class HelloProvider:
    """A simple greeting provider."""

    # Provider configuration
    api_key: str = Attribute(
        description="API key for authentication",
        sensitive=True,
        required=True
    )

@resource
class Greeting:
    """A greeting resource."""

    # Resource schema
    name: str = Attribute(
        description="Name to greet",
        required=True
    )

    message: str = Attribute(
        description="The greeting message",
        computed=True
    )

    # Lifecycle methods
    def create(self, config):
        """Create a new greeting."""
        message = f"Hello, {config.name}!"
        return {
            "id": f"greeting-{config.name.lower()}",
            "name": config.name,
            "message": message
        }

    def read(self, config, state):
        """Read an existing greeting."""
        return state  # Static resource, return as-is

    def update(self, config, state):
        """Update a greeting."""
        message = f"Hello, {config.name}!"
        return {
            **state,
            "name": config.name,
            "message": message
        }

    def delete(self, config, state):
        """Delete a greeting."""
        # Nothing to clean up for this example
        pass
```

### 2. Package Your Provider

Use flavorpack to create a self-contained executable:

```bash
# Create a package manifest
cat > provider.toml << EOF
[package]
name = "terraform-provider-hello"
entry_point = "my_provider:main"

[build]
dependencies = [
    "pyvider",
    "pyvider-components"
]
EOF

# Build the provider
flavor pack --manifest provider.toml --output terraform-provider-hello
```

### 3. Use Your Provider

Create a Terraform configuration:

```hcl title="main.tf"
terraform {
  required_providers {
    hello = {
      source = "local/example/hello"
      version = "1.0.0"
    }
  }
}

provider "hello" {
  api_key = "secret-key"
}

resource "hello_greeting" "example" {
  name = "World"
}

output "greeting_message" {
  value = hello_greeting.example.message
}
```

Run Terraform:

```bash
# Initialize Terraform
terraform init

# Apply the configuration
terraform apply
```

Expected output:
```
greeting_message = "Hello, World!"
```

## Development Workflow

### Project Structure

A typical provide.io project follows this structure:

```
my-provider/
├── pyproject.toml          # Package configuration
├── src/
│   └── my_provider/        # Provider source code
│       ├── __init__.py
│       ├── provider.py     # Provider definition
│       ├── resources/      # Resource implementations
│       └── data_sources/   # Data source implementations
├── tests/                  # Test suite
├── docs/                   # Documentation
├── examples/               # Example configurations
└── README.md               # Project overview
```

### Development Commands

Common development tasks using the ecosystem tools:

```bash
# Code quality
ruff format .               # Format code
ruff check .                # Lint code
mypy src/                   # Type checking

# Testing
pytest                      # Run tests
pytest --cov               # Run with coverage
pytest -m "not slow"       # Skip slow tests

# Documentation
plating render              # Generate provider docs
mkdocs serve               # Serve docs locally

# Environment management
wrknv sync                 # Sync environment
source workenv/env.sh      # Activate environment

# Packaging
flavor pack                # Create executable package
flavor verify package.psp # Verify package integrity
```

### Git Workflow

Use supsrc for automated Git workflow management:

```bash
# Start automated Git watching
supsrc watch

# Configure automatic commits
supsrc config set auto_commit true
supsrc config set commit_interval 300  # 5 minutes
```

## Key Concepts

### 1. Foundation Layer

Everything builds on `provide-foundation`, which provides:

- **Structured Logging**: Beautiful, emoji-enhanced logs
- **Error Handling**: Rich error context and handling
- **Configuration**: Type-safe configuration management

```python
from provide.foundation import logger

log = logger.get_logger(__name__)
log.info("Application started", version="1.0.0")
```

### 2. Type Safety

The ecosystem emphasizes type safety throughout:

```python
from pyvider.cty import CtyString, CtyNumber

# Type-safe configuration
class Config:
    name: CtyString
    port: CtyNumber
    enabled: bool = True  # Modern Python typing
```

### 3. Testing

Use `provide-testkit` for comprehensive testing:

```python
import pytest
from provide.testkit import temp_directory, mock_server

def test_provider_creation(temp_directory):
    """Test provider functionality."""
    # Test implementation
    pass

@pytest.mark.asyncio
async def test_async_operation(mock_server):
    """Test async operations."""
    # Async test implementation
    pass
```

### 4. Documentation

Generate documentation automatically with plating:

```bash
# Generate provider documentation
plating render --provider my_provider --output docs/

# Serve documentation
mkdocs serve -f docs/mkdocs.yml
```

## Next Steps

Now that you have the ecosystem set up, explore these guides:

<div class="grid cards" markdown>

-   :material-terraform:{ .lg } **[Building Providers](guides/provider-development.md)**

    Learn to create comprehensive Terraform providers with resources, data sources, and functions.

-   :material-package:{ .lg } **[Packaging Applications](guides/packaging.md)**

    Use flavorpack to create self-contained, portable executable packages.

-   :material-test-tube:{ .lg } **[Testing Strategy](guides/testing.md)**

    Implement comprehensive testing with unit, integration, and conformance tests.

-   :material-book:{ .lg } **[Documentation](guides/documentation.md)**

    Generate beautiful documentation for your providers and tools.

</div>

## Getting Help

If you run into issues:

1. **Check the documentation**: Each package has comprehensive docs
2. **Search issues**: Look for existing solutions on GitHub
3. **Ask questions**: Use GitHub Discussions for help
4. **Report bugs**: Create detailed issue reports

## Examples Repository

Explore complete examples in the [examples repository](https://github.com/provide-io/examples):

- Simple providers
- Complex multi-resource providers
- Integration with external APIs
- Testing strategies
- Documentation examples

Happy building! 🚀