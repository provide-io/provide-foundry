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
cd /Users/tim/code/gh/provide-io
uv sync --all-groups
source .venv/bin/activate
```

This sets up all packages in editable mode with unified dependency management.

## 📦 Repository Structure

The provide.io ecosystem is organized as a monorepo with the following structure:

```
provide-io/
├── pyproject.toml              # Workspace configuration
├── provide-foundry/            # Documentation hub
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
- **Modern Only**: No backward compatibility code or migration logic
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

## 🔨 Build System Standards

### Makefiles Over Scripts

All Python library projects in the ecosystem use **standardized Makefiles** for development tasks. Custom shell scripts are only allowed for specific cases.

#### Core Principle

**Use Makefiles, not shell scripts, for common development tasks.**

#### Why Makefiles?

✅ **Consistency**: Same commands work across all projects (`make test`, `make lint`, etc.)
✅ **Discoverability**: `make help` shows all available targets
✅ **Dependencies**: Make handles target dependencies elegantly
✅ **Standards**: Industry-standard build tool
✅ **Maintenance**: Single source of truth (template + custom targets)

#### Standard Makefile Targets

All Python library projects have these standard targets:

**Setup & Environment**:
- `make setup` - Initialize development environment (uv sync)

**Testing** (8 targets):
- `make test` - Run all tests
- `make test-parallel` - Run tests in parallel
- `make test-verbose` - Run tests with verbose output
- `make test-unit` - Run only unit tests
- `make test-integration` - Run only integration tests
- `make coverage` - Run tests with coverage report (with line-by-line coverage)
- `make coverage-xml` - Generate XML coverage report for CI systems

**Mutation Testing** (4 targets):
- `make mutation-run` - Run mutation testing with mutmut
- `make mutation-results` - Show mutation testing results
- `make mutation-browse` - Open interactive mutation browser
- `make mutation-clean` - Clean mutation testing artifacts

**Code Quality** (7 targets):
- `make lint` - Run linter (ruff check)
- `make lint-fix` - Run linter with auto-fix
- `make format` - Format code with ruff
- `make format-check` - Check formatting without modifying
- `make typecheck` - Run type checker (mypy)
- `make quality` - Run lint + typecheck
- `make quality-all` - Run all quality checks including tests

**Build & Package** (5 targets):
- `make build` - Build package
- `make install` - Install in development mode
- `make uninstall` - Uninstall package
- `make lock` - Update dependency lock file
- `make version` - Show package version

**Documentation** (4 targets):
- `we run docs.setup` - Extract base-mkdocs.yml from foundry
- `we run docs.build` - Build documentation
- `we run docs.serve` - Serve documentation locally
- `we run docs.clean` - Clean documentation artifacts

**CI/CD** (3 targets):
- `make ci-test` - Run tests with coverage for CI
- `make ci-quality` - Run all quality checks for CI
- `make ci-all` - Run full CI pipeline

**Development Shortcuts** (3 targets):
- `make dev-setup` - Alias for setup
- `make dev-test` - Quick test run (parallel)
- `make dev-check` - Quick quality check

**Clean**:
- `make clean` - Clean all build artifacts and caches

### When Shell Scripts Are Allowed

Scripts are **only** allowed if they meet one of these criteria:

1. **Templated from foundry**: Extracted via `extract_*_script()` functions
   - Examples: `validate_examples.sh`, `clean_artifacts.sh` (for Terraform providers)

2. **Truly unique functionality**: Not duplicating Make targets
   - Examples: `test-registry-url-alignment.sh` (plating), `build.sh` (flavorpack helpers)

### When Scripts Are NOT Allowed

❌ **Never create scripts that duplicate Makefile targets**:
- NO: `scripts/test.sh` (use `make test`)
- NO: `scripts/setup.sh` (use `make setup`)
- NO: `scripts/docs-serve.sh` (use `we run docs.serve`)
- NO: `scripts/quality.sh` (use `make quality`)

### Adding Custom Targets

If your project needs custom functionality, **add it to the Makefile**, not as a separate script.

#### Example: Adding Custom Targets

```makefile
# ==============================================================================
# 🎨 Project-Specific Targets (Custom)
# ==============================================================================

custom-build: ## Build project-specific artifacts
	@echo '$(BLUE)Building custom artifacts...$(NC)'
	./build-custom-thing.sh
	@echo '$(GREEN)✓ Custom build complete$(NC)'

custom-validate: ## Validate project-specific things
	@echo '$(BLUE)Validating...$(NC)'
	python tools/validate.py
	@echo '$(GREEN)✓ Validation complete$(NC)'
```

**Best practices**:
- Add custom section with clear header
- Update `.PHONY` declaration
- Use template color variables (`$(BLUE)`, `$(GREEN)`, etc.)
- Add `##` comments for help integration
- Organize related targets into sections

### Getting the Standard Makefile

For new Python library projects:

```python
from provide.foundry.config import extract_python_makefile
from pathlib import Path

# Extract to current directory
extract_python_makefile(Path('.'))
```

Or via command line:
```bash
python -c "from provide.foundry.config import extract_python_makefile; from pathlib import Path; extract_python_makefile(Path('.'))"
```

### Examples in the Ecosystem

**Standard template only** (10 projects):
- provide-foundation, provide-testkit, pyvider, pyvider-cty, pyvider-hcl, pyvider-rpcplugin, wrknv, tofusoup, supsrc, plating

**Standard + custom targets** (2 projects):
- **pyvider-components**: Adds plating documentation generation targets
- **flavorpack**: Adds PSPF validation, build helpers, and release management targets

### Migration from Scripts

If you find scripts that duplicate Makefile functionality:

1. **Verify**: Check if script functionality exists in Makefile
2. **Test**: Ensure Make target works correctly
3. **Remove**: Delete the redundant script
4. **Update docs**: Change documentation to reference Make targets

Example:
```bash
# Before
./scripts/test.sh

# After
make test
```

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
4. **Changelog**: Compile changes across packages
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
