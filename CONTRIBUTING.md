# Contributing to the Provide.io Ecosystem

Thank you for your interest in contributing to the provide.io ecosystem! This guide covers contribution guidelines that apply across all packages in the ecosystem.

## 🛠 Development Environment Setup

### Prerequisites
- Python 3.11 or higher
- UV package manager (installed automatically by `env.sh`)
- Git

### Quick Setup
```bash
# Clone and set up the entire ecosystem
cd /REDACTED_ABS_PATH
uv sync --extra all --extra dev
source .venv/bin/activate
```

This sets up all packages in editable mode with unified dependency management.

## 📦 Repository Structure

The provide.io ecosystem is organized as a monorepo with the following structure:

```
provide-io/
├── pyproject.toml              # Workspace configuration
├── provide-ecosystem/          # Documentation hub
│   └── docs/                  # Unified documentation
├── provide-foundation/         # Core infrastructure
├── provide-testkit/           # Testing utilities
├── pyvider/                   # Framework packages
├── pyvider-*/                 # Framework components
├── flavorpack/                # Packaging tools
├── wrknv/                     # Environment management
├── plating/                   # Documentation generation
├── tofusoup/                  # Conformance testing
└── supsrc/                    # Git automation
```

## 🎯 Contribution Guidelines

### Code Standards

#### Python Requirements
- **Python 3.11+**: All code must use modern Python features
- **Type Hints**: Full type annotations required (`str | None`, not `Optional[str]`)
- **No Legacy**: No backward compatibility code or migration logic
- **Modern Patterns**: Use `attrs` for data classes, async where appropriate

#### Code Quality
```bash
# Format and lint
ruff format .
ruff check .

# Type checking
mypy src/

# Run tests
pytest
```

#### Configuration Standards
- **No inline defaults**: Use constants.py or defaults.py files
- **No hardcoded values**: All configuration via environment or config files
- **Modern pyproject.toml**: Use dependency-groups, not extras where possible

### Testing Requirements

#### Test Structure
- Use **provide-testkit** for all testing utilities
- Follow the testing patterns established in provide-foundation
- Include unit, integration, and property-based tests where appropriate

#### Test Commands
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific markers
pytest -m "not slow"
pytest -m integration
```

### Documentation Standards

#### Required Documentation
Every package must include:
- **README.md**: Overview, installation, basic usage
- **CHANGELOG.md**: Keep a Changelog format
- **CONTRIBUTING.md**: Package-specific guidelines
- **CLAUDE.md**: AI assistant instructions
- **docs/**: Detailed documentation
- **examples/**: Runnable code examples

#### Documentation Style
- Use **Markdown** for all documentation
- Include **code examples** that can be copy-pasted
- **Cross-reference** related packages and concepts
- **Test examples** to ensure they work

## 🔄 Development Workflow

### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow code standards above
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**:
   ```bash
   # Run quality checks
   ruff format . && ruff check .
   mypy src/

   # Run tests
   pytest
   ```

4. **Update documentation**:
   - Update README.md if needed
   - Add entries to CHANGELOG.md
   - Update API documentation if applicable

### Submitting Pull Requests

1. **Ensure tests pass**: All CI checks must be green
2. **Write clear commit messages**: Use conventional commit format
3. **Update documentation**: Include relevant documentation updates
4. **Add changelog entry**: Follow Keep a Changelog format

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat(pyvider): add support for ephemeral resources`
- `fix(testkit): resolve fixture cleanup issue`
- `docs(foundation): add logging configuration guide`

## 🏗 Package-Specific Guidelines

### Foundation Layer (provide-*)
- **High stability**: Changes require careful consideration
- **Comprehensive testing**: Near 100% test coverage expected
- **Performance**: Benchmark critical paths
- **Documentation**: Extensive API documentation required

### Framework Layer (pyvider-*)
- **Terraform compatibility**: Follow Terraform conventions
- **Type safety**: Strict typing enforcement
- **Cross-platform**: Support all major platforms
- **Examples**: Include working Terraform examples

### Tools Layer (flavorpack, wrknv, etc.)
- **User experience**: Focus on ease of use
- **CLI design**: Follow best practices for command-line tools
- **Error messages**: Clear, actionable error messages
- **Integration**: Work well with other ecosystem tools

## 🔍 Review Process

### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests are included and pass
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] No security vulnerabilities introduced
- [ ] Performance impact considered

### Review Guidelines
- **Be constructive**: Provide specific, actionable feedback
- **Consider alternatives**: Suggest improvements, not just problems
- **Test thoroughly**: Actually run the code when reviewing
- **Check integration**: Ensure changes work with related packages

## 🐛 Issue Reporting

### Bug Reports
Include:
- **Environment**: OS, Python version, package versions
- **Steps to reproduce**: Minimal example that demonstrates the issue
- **Expected behavior**: What should have happened
- **Actual behavior**: What actually happened
- **Logs**: Any relevant error messages or logs

### Feature Requests
Include:
- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives**: Other ways to solve the problem
- **Impact**: Which packages would be affected?

## 🚀 Release Process

Releases are coordinated across the ecosystem:

1. **Version coordination**: Ensure compatible versions across packages
2. **Testing**: Run full integration test suite
3. **Documentation**: Update all relevant documentation
4. **Changelog**: Consolidate changes across packages
5. **Announcement**: Communicate changes to users

## 📞 Getting Help

- **Documentation**: Check package-specific docs first
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions
- **Code Review**: Don't hesitate to ask for feedback early

## 🎉 Recognition

Contributors are recognized through:
- **Changelog entries**: All contributors are credited
- **GitHub contributors**: Automatic recognition via GitHub
- **Documentation**: Maintainers are listed in each package

Thank you for contributing to the provide.io ecosystem! 🙏