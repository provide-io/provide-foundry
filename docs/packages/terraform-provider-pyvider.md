# terraform-provider-pyvider

The official reference implementation Terraform provider built with the Pyvider framework, demonstrating best practices and serving as a learning resource.

## Overview

`terraform-provider-pyvider` is the canonical example provider for the Pyvider framework. It showcases how to build production-focused Terraform providers using pyvider-components and the full Pyvider ecosystem.

### Key Features

- **📚 Learning Resource**: Comprehensive examples of provider development patterns
- **🧩 Component Integration**: Demonstrates using pyvider-components library
- **✅ Best Practices**: Reference implementation following all Pyvider conventions
- **🧪 Test Coverage**: Extensive test suite showing testing approaches
- **📦 FlavorPack Integration**: Production binary packaging examples
- **📖 Rich Documentation**: Complete guides for provider development

## Purpose

This provider serves multiple purposes:

1. **Reference Implementation**: Shows how to structure a production provider
2. **Testing Playground**: Used to validate Pyvider framework features
3. **Documentation Source**: Provides real-world examples for guides
4. **Component Showcase**: Demonstrates pyvider-components in action

## Installation

### Using the Provider

```hcl
terraform {
  required_providers {
    pyvider = {
      source = "provide-io/pyvider"
      version = "~> 0.1"
    }
  }
}

provider "pyvider" {
  # Provider configuration
}
```

### Development

```bash
# Clone and setup
git clone https://github.com/provide-io/terraform-provider-pyvider
cd terraform-provider-pyvider
source env.sh

# Run tests
uv run pytest

# Build provider binary
uv run plating plate
```

## Components Included

The provider includes examples of:

- **Resources**: File operations, timed tokens, private state management
- **Data Sources**: Environment variables, HTTP APIs, configuration readers
- **Functions**: String manipulation, numeric operations, jq transformations
- **Capabilities**: Lens transformations, API interactions

## Documentation

<!-- See the [Provider Tour](../pyvider-components/guides/provider-tour/) --> and [Build Your Own](../pyvider-components/guides/build-your-own/) guides for detailed walkthroughs.

## Related Packages

- [pyvider](pyvider.md) - Core framework
- [pyvider-components](pyvider-components.md) - Component library
- [plating](plating.md) - Documentation and code generation
- [flavorpack](flavorpack.md) - Binary packaging system
