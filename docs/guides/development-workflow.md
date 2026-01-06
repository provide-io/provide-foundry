# Development Workflow Guide

Common development patterns and workflows across the provide.io ecosystem.

## Overview

All projects in the ecosystem follow similar development patterns:
- UV for dependency management
- pytest for testing
- Ruff for code quality
- Git for version control
- MkDocs for documentation

## Standard Development Workflow

### 1. Initial Setup

```bash
# Clone repository
git clone https://github.com/provide-io/PROJECT_NAME.git
cd PROJECT_NAME

# Set up development environment
uv sync

# Verify installation
uv run pytest --version
uv run ruff --version
```

### 2. Daily Development Cycle

```bash
# Pull latest changes
git pull origin main

# Sync dependencies (if pyproject.toml changed)
uv sync

# Create feature branch
git checkout -b feature/my-feature

# Make code changes
# ... edit files ...

# Format code
uv run ruff format src/ tests/

# Lint code
uv run ruff check src/ tests/

# Run tests
uv run pytest

# Commit changes
git add .
git commit -m "Add feature description"

# Push changes
git push origin feature/my-feature
```

### 3. Code Quality Checks

Before committing, always run:

```bash
# Format code
uv run ruff format src/ tests/

# Check and fix linting issues
uv run ruff check --fix src/ tests/

# Run type checking (varies by project)
uv run mypy src/

# Run tests with coverage
uv run pytest --cov

# Run pre-commit hooks
pre-commit run --all-files
```

### 4. Documentation Updates

When adding features:

```bash
# Update documentation
# Edit docs/*.md files

# Build documentation locally
mkdocs serve

# View at http://127.0.0.1:800X (port varies by project)

# Verify build
mkdocs build --strict
```

## Project-Specific Workflows

### Foundation Projects

**provide-foundation, provide-testkit:**

```bash
# Run tests (auto-parallel)
uv run pytest -n auto

# Type checking (mypy preferred)
uv run mypy src/

# Build package
uv build
```

**Key considerations:**
- Always use `reset_foundation_setup_for_testing()` in tests
- Test across multiple Python versions if possible
- Ensure backward compatibility within major version

### Framework Projects

**pyvider, pyvider-cty, pyvider-hcl, pyvider-rpcplugin, pyvider-components:**

```bash
# Run tests with coverage
uv run pytest --cov=PACKAGE_NAME --cov-report=term-missing

# Type checking
uv run mypy src/

# Test imports
python -c "from PACKAGE_NAME import MODULE; print('✅ Imports working')"
```

**Key considerations:**
- Cross-project compatibility (pyvider ecosystem)
- Integration tests with other pyvider packages
- Type safety is critical

### Tool Projects

**flavorpack:**

```bash
# Build native helpers
make build-helpers

# Run tests (using pretaster/taster)
make test

# Validate PSPF packages
make validate-pspf
```

**wrknv:**

```bash
# Generate environment scripts
wrknv generate

# Test environment setup
source ./env.sh
```

**supsrc:**

```bash
# Run tests excluding slow tests
uv run pytest -m "not slow"

# Test with TUI
uv run supsrc sui  # Requires [tui] extra
```

**tofusoup:**

```bash
# Build Go harnesses
soup harness build soup-go

# Run conformance tests
soup test cty
soup test hcl
soup test rpc
```

## Testing Strategies

### Test Organization

Standard test structure:

```
tests/
├── unit/              # Fast, isolated tests
├── integration/       # Component interaction tests
├── conformance/       # Cross-language compatibility
└── conftest.py        # Shared fixtures
```

### Running Tests Efficiently

```bash
# During development - fast feedback
uv run pytest tests/unit/ -x --tb=short

# Before commit - comprehensive
uv run pytest -n auto

# Before PR - full validation
uv run pytest --cov --cov-report=html
```

### Test Markers

Common markers across projects:

```python
@pytest.mark.slow          # Long-running tests
@pytest.mark.integration   # Integration tests
@pytest.mark.unit          # Unit tests
@pytest.mark.asyncio       # Async tests
```

Run specific markers:

```bash
uv run pytest -m "not slow"        # Skip slow tests
uv run pytest -m integration       # Only integration tests
uv run pytest -m "unit and not slow"  # Fast unit tests
```

## Git Workflow

### Branch Naming

```
feature/description    # New features
fix/description        # Bug fixes
docs/description       # Documentation updates
refactor/description   # Code refactoring
test/description       # Test improvements
```

### Commit Messages

Follow conventional commits:

```bash
git commit -m "feat: add new feature description"
git commit -m "fix: resolve bug description"
git commit -m "docs: update installation guide"
git commit -m "test: add tests for feature"
git commit -m "refactor: improve code structure"
```

### Pull Request Workflow

1. **Create PR with descriptive title and description**
2. **Ensure CI passes** (tests, linting, type checking)
3. **Request review** from maintainers
4. **Address feedback** in additional commits
5. **Squash and merge** once approved

## Dependency Management

### Adding Dependencies

```bash
# Add runtime dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Add optional dependency
# Edit pyproject.toml [project.optional-dependencies]
```

### Updating Dependencies

```bash
# Update specific package
uv add package-name --upgrade

# Update all dependencies
uv sync --upgrade

# Lock file management
uv lock
```

### Ecosystem Dependencies

When working across multiple projects:

```bash
# Install local development version
cd /path/to/dependency-project
uv build

cd /path/to/consuming-project
uv pip install -e /path/to/dependency-project
```

## Documentation Workflow

### Writing Documentation

1. **Follow existing structure** in `docs/` directory
2. **Use partials** for common content (see `.provide/foundry/docs/_partials/`)
3. **Include code examples** with syntax highlighting
4. **Add cross-references** to related docs
5. **Test all code examples** before committing

### Building Documentation Locally

```bash
# Development server with auto-reload
mkdocs serve

# Production build
mkdocs build

# Strict build (fails on warnings)
mkdocs build --strict
```

### Documentation Standards

- **Use present tense**: "This function returns..." not "This function will return..."
- **Be concise**: Get to the point quickly
- **Include examples**: Show, don't just tell
- **Link to related docs**: Help users navigate
- **Keep it updated**: Update docs with code changes

## Troubleshooting Common Issues

### UV Sync Fails

```bash
# Clear cache and retry
uv cache clean
uv sync

# Force reinstall
rm -rf .venv
uv sync
```

### Tests Fail After Dependency Update

```bash
# Check for version conflicts
uv run python -c "import importlib.metadata as m; print(m.version('package-name'))"

# Downgrade if needed
uv add "package-name<2.0.0"
```

### Import Errors

```bash
# Verify PYTHONPATH
echo $PYTHONPATH

# Check virtual environment
which python
python -c "import sys; print(sys.prefix)"

# Reinstall in editable mode
uv pip install -e .
```

### Type Checking Errors After Update

```bash
# Clear mypy cache
rm -rf .mypy_cache

# Re-run type checking
uv run mypy src/
```

## Performance Optimization

### Test Execution

```bash
# Parallel execution
uv run pytest -n auto

# Disable coverage during development
uv run pytest --no-cov

# Run only changed tests (with pytest-testmon)
uv run pytest --testmon
```

### Build Times

```bash
# Clean build artifacts
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name "*.egg-info" -exec rm -rf {} +

# Rebuild package
uv build
```

## Best Practices

1. **Keep branches small and focused** - Easier to review and merge
2. **Write tests first** - TDD leads to better design
3. **Run tests frequently** - Catch issues early
4. **Format on save** - Keep code consistent automatically
5. **Use type hints** - Catch errors before runtime
6. **Document as you code** - Don't leave it for later
7. **Review your own code** - Catch issues before PR
8. **Keep dependencies minimal** - Reduce complexity and conflicts

## Quick Reference

| Task | Command |
|------|---------|
| Setup environment | `uv sync` |
| Run tests | `uv run pytest` |
| Format code | `uv run ruff format src/ tests/` |
| Lint code | `uv run ruff check src/ tests/` |
| Type check | `uv run mypy src/` |
| Build docs | `mkdocs build` |
| Serve docs | `mkdocs serve` |
| Build package | `uv build` |
| Run pre-commit | `pre-commit run --all-files` |

---

**Related Guides:**
- [IDE Setup Guide](ide-setup.md) - Configure your development environment
- [Testing Patterns Guide](testing-patterns.md) - Testing strategies across projects
