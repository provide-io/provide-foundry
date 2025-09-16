# Ecosystem Overview

The provide.io ecosystem is designed as a cohesive collection of tools and frameworks that work together to solve the challenges of building Terraform providers, packaging applications, and managing development workflows.

## Design Philosophy

The ecosystem is built around core principles that ensure consistency, maintainability, and developer experience:

<div class="grid cards" markdown>

-   :material-layers:{ .lg } **Layered Architecture**

    Clear separation between foundation, framework, and tools with well-defined interfaces.

-   :material-typewriter:{ .lg } **Type Safety First**

    Comprehensive type annotations using modern Python 3.11+ features throughout.

-   :material-rocket-launch:{ .lg } **Developer Experience**

    Excellent error messages, comprehensive documentation, and intuitive APIs.

-   :material-test-tube:{ .lg } **Testing Excellence**

    High test coverage with unit, integration, and property-based testing.

</div>

## Package Relationships

Understanding how packages relate to each other helps you choose the right tools for your needs:

```mermaid
graph TB
    subgraph "User Applications"
        APP[Your Terraform Provider]
        PKG[Your Packaged Application]
        DOC[Generated Documentation]
    end

    subgraph "Tools Layer"
        FP[flavorpack]
        WE[wrknv]
        PL[plating]
        TS[tofusoup]
        SS[supsrc]
    end

    subgraph "Framework Layer"
        PY[pyvider]
        CTY[pyvider-cty]
        HCL[pyvider-hcl]
        RPC[pyvider-rpcplugin]
        COMP[pyvider-components]
        TPP[terraform-provider-pyvider]
    end

    subgraph "Foundation Layer"
        FOUND[provide-foundation]
        TEST[provide-testkit]
    end

    APP --> PY
    APP --> COMP
    PKG --> FP
    DOC --> PL

    FP --> FOUND
    WE --> FOUND
    PL --> PY
    PL --> CTY
    TS --> CTY
    TS --> HCL
    TS --> RPC
    SS --> FOUND

    PY --> FOUND
    PY --> TEST
    CTY --> FOUND
    HCL --> CTY
    HCL --> FOUND
    RPC --> FOUND
    COMP --> PY
    COMP --> CTY
    COMP --> RPC
    TPP --> PY
    TPP --> COMP

    TEST --> FOUND

    classDef foundation fill:#e1f5fe
    classDef framework fill:#f3e5f5
    classDef tools fill:#e8f5e8
    classDef user fill:#fff3e0

    class FOUND,TEST foundation
    class PY,CTY,HCL,RPC,COMP,TPP framework
    class FP,WE,PL,TS,SS tools
    class APP,PKG,DOC user
```

## Package Categories

### Foundation Layer

The foundation provides core infrastructure that all other packages build upon:

- **[provide-foundation](../packages/foundation.md)**: Structured logging, error handling, configuration
- **[provide-testkit](../packages/testkit.md)**: Testing utilities, fixtures, and test infrastructure

### Framework Layer

The Pyvider framework enables building Terraform providers in Python:

- **[pyvider](../packages/pyvider.md)**: Core framework with provider, resource, and data source abstractions
- **[pyvider-cty](../packages/pyvider-cty.md)**: Implementation of Terraform's CTY type system
- **[pyvider-hcl](../packages/pyvider-hcl.md)**: HCL parsing and generation with CTY integration
- **[pyvider-rpcplugin](../packages/pyvider-rpcplugin.md)**: Terraform plugin protocol implementation
- **[pyvider-components](../packages/pyvider-components.md)**: Standard library of components
- **[terraform-provider-pyvider](../packages/terraform-provider-pyvider.md)**: Meta-package demonstrating the framework

### Tools Layer

Development and deployment tools that enhance the development experience:

- **[flavorpack](../packages/flavorpack.md)**: Create self-contained executable packages
- **[wrknv](../packages/wrknv.md)**: Development environment management
- **[plating](../packages/plating.md)**: Documentation generation for Terraform providers
- **[tofusoup](../packages/tofusoup.md)**: Cross-language conformance testing
- **[supsrc](../packages/supsrc.md)**: Automated Git workflow management

## Data Flow

Understanding how data flows through the ecosystem helps with debugging and optimization:

```mermaid
sequenceDiagram
    participant User
    participant Terraform
    participant Provider
    participant Framework
    participant Foundation

    User->>Terraform: terraform apply
    Terraform->>Provider: gRPC calls
    Provider->>Framework: pyvider handlers
    Framework->>Foundation: logging, errors
    Foundation-->>Framework: structured logs
    Framework-->>Provider: processed results
    Provider-->>Terraform: gRPC responses
    Terraform-->>User: apply results
```

## Deployment Architecture

The ecosystem supports multiple deployment patterns:

### Development Mode

```mermaid
graph LR
    Dev[Developer] --> IDE[IDE/Editor]
    IDE --> Git[Git Repository]
    Git --> CI[CI/CD Pipeline]
    CI --> Test[Test Environment]

    subgraph "Development Tools"
        Wrknv[wrknv<br/>Environment]
        Supsrc[supsrc<br/>Git Automation]
        Plating[plating<br/>Documentation]
    end

    Dev --> Wrknv
    Dev --> Supsrc
    Dev --> Plating
```

### Production Deployment

```mermaid
graph TB
    Source[Source Code] --> FP[flavorpack]
    FP --> PSP[Package.psp]
    PSP --> Registry[Package Registry]

    Registry --> Deploy1[Deployment 1]
    Registry --> Deploy2[Deployment 2]
    Registry --> DeployN[Deployment N]

    Deploy1 --> TF1[Terraform]
    Deploy2 --> TF2[Terraform]
    DeployN --> TFN[Terraform]
```

## Quality Assurance

The ecosystem maintains high quality through multiple layers of validation:

### Code Quality

- **Type Checking**: MyPy with strict settings
- **Linting**: Ruff with comprehensive rule sets
- **Formatting**: Consistent code style across all packages
- **Security**: Bandit security scanning

### Testing Strategy

- **Unit Tests**: High coverage for individual components
- **Integration Tests**: Cross-package functionality validation
- **Property-Based Testing**: Hypothesis for edge case discovery
- **Conformance Tests**: TofuSoup for Terraform compatibility

### Documentation Quality

- **API Documentation**: Comprehensive coverage of all public APIs
- **Examples**: Working code examples for all major features
- **Guides**: Step-by-step tutorials for common tasks
- **Architecture**: Clear explanations of design decisions

## Versioning Strategy

The ecosystem uses semantic versioning with coordinated releases:

### Individual Package Versions

Each package maintains its own version following semantic versioning:

- **Major**: Breaking changes to public APIs
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, backward compatible

### Ecosystem Compatibility

Packages declare compatibility with specific versions of their dependencies:

```toml
# Example from pyvider-components
dependencies = [
    "provide-foundation>=0.1.0,<0.2.0",
    "pyvider>=0.1.0,<0.2.0",
    "pyvider-cty>=0.0.113,<0.1.0"
]
```

### Release Coordination

Major releases are coordinated across packages to ensure compatibility:

1. **Planning**: Major changes discussed across affected packages
2. **Alpha/Beta**: Pre-release versions for testing
3. **Release Candidates**: Final validation before release
4. **Coordinated Release**: All packages released together

## Performance Characteristics

The ecosystem is designed for performance at scale:

### Logging Performance

- **14,000+ messages/second** with emoji processing
- **Async-first** design for non-blocking operations
- **Structured data** for efficient processing

### Provider Performance

- **Fast startup**: Minimal import time
- **Efficient gRPC**: Optimized protocol implementation
- **Memory management**: Careful resource handling

### Build Performance

- **Incremental builds**: Only rebuild what changed
- **Parallel execution**: Multi-core utilization
- **Caching**: Aggressive caching of build artifacts

## Security Considerations

Security is built into the ecosystem at multiple levels:

### Package Security

- **Signed packages**: Ed25519 signatures for integrity
- **Dependency scanning**: Automated vulnerability detection
- **Minimal dependencies**: Reduced attack surface

### Runtime Security

- **Secure defaults**: Safe configuration out of the box
- **Input validation**: Comprehensive data validation
- **Error handling**: No sensitive data in error messages

### Development Security

- **Secret management**: No secrets in code or logs
- **Access control**: Principle of least privilege
- **Audit logging**: Comprehensive activity logging

---

Continue exploring the ecosystem with our detailed [architecture guide](architecture.md) or learn about our [design principles](principles.md).