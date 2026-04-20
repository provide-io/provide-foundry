# Terraform Providers

The Terraform Providers layer enables infrastructure-as-code using Python-based Terraform providers built on the Pyvider framework. These providers allow you to manage infrastructure resources using Terraform/OpenTofu while implementing provider logic in Python.

## Provider Architecture

```mermaid
graph LR
    terraform[Terraform/OpenTofu] --> grpc[gRPC Protocol]
    grpc --> pyvider[Pyvider Framework]
    pyvider --> provider[Provider Implementation]
    provider --> resources[Resources & Data Sources]

    style terraform fill:#5c4ee5,stroke:#fff,color:#fff
    style pyvider fill:#4051b5,stroke:#fff,color:#fff
    style provider fill:#5c6bc0,stroke:#fff,color:#fff
```

## Available Providers

The provide.io ecosystem includes two production Terraform providers:

**Pyvider Provider**: Reference implementation showcasing the Pyvider framework capabilities. Demonstrates resource lifecycle management, data sources, and provider configuration patterns.

**TofuSoup Provider**: Infrastructure testing and conformance provider. Enables testing Terraform configurations and validating infrastructure compliance using the TofuSoup conformance framework.

## Provider Features

Each provider is built on the Pyvider framework and provides:

- **Type Safety**: Full CTY type system integration for Terraform data types
- **HCL Support**: Native HCL parsing and manipulation
- **gRPC Protocol**: Terraform plugin protocol v6 support
- **Resource Management**: Complete CRUD lifecycle support
- **Data Sources**: Read-only data source implementations
- **Provider Configuration**: Flexible provider-level configuration
- **Schema Validation**: Automatic schema validation and type checking

## Development Workflow

Building Terraform providers with Pyvider:

1. **Define Resources**: Use Pyvider resource decorators to define resource schemas
1. **Implement CRUD**: Implement Create, Read, Update, Delete operations
1. **Add Data Sources**: Define read-only data sources for external data
1. **Configure Provider**: Set up provider-level configuration and authentication
1. **Test**: Use TofuSoup for conformance testing
1. **Package**: Build and distribute using Flavorpack

## Provider Integration

Terraform providers integrate seamlessly with the ecosystem:

- **Foundation**: Uses provide-foundation for logging and telemetry
- **Pyvider Framework**: Built on pyvider core, cty, hcl, and rpcplugin
- **Testing**: Validated using provide-testkit and tofusoup
- **Packaging**: Distributed using Flavorpack secure packaging

## Providers

<div class="grid cards" markdown>

- :material-terraform: **Pyvider Provider**

  ______________________________________________________________________

  Reference Terraform provider implementation showcasing Pyvider framework capabilities and best practices.

  [:octicons-arrow-right-24: Explore Pyvider Provider](https://foundry.provide.io/terraform-provider-pyvider/)

- :material-test-tube: **TofuSoup Provider**

  ______________________________________________________________________

  Infrastructure testing and conformance provider for validating Terraform configurations.

  [:octicons-arrow-right-24: Explore TofuSoup Provider](https://foundry.provide.io/terraform-provider-tofusoup/)

</div>
