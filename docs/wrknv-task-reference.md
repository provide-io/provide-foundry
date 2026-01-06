# wrknv Task Reference

Complete reference for all standard tasks provided by the wrknv.python.tmpl template.

## Quick Reference

```bash
# List all tasks
we tasks

# Run a task
we run <task>

# Task information
we run <task> --info

# Dry run (show what would execute)
we run <task> --dry-run
```

## Task Categories

- [Testing](#testing) - Run tests with various configurations
- [Code Quality](#code-quality) - Linting, formatting, type checking
- [Documentation](#documentation) - Build, serve, validate docs
- [Link Checking](#link-checking) - Validate documentation links
- [Mutation Testing](#mutation-testing) - Advanced test quality analysis
- [Build & Package](#build--package) - Build distributions, manage dependencies
- [Development Shortcuts](#development-shortcuts) - Common dev workflows
- [CI/CD Pipelines](#cicd-pipelines) - Complete CI workflows

---

## Testing

### `we run test`

Run all tests using pytest.

```bash
we run test
```

**Subtasks:**

#### `we run test.parallel`
Run tests in parallel using pytest-xdist.

```bash
we run test.parallel
```

Equivalent to: `uv run pytest -n auto`

#### `we run test.verbose`
Run tests with verbose output.

```bash
we run test.verbose
```

Equivalent to: `uv run pytest -vvv`

#### `we run test.unit`
Run only unit tests (requires pytest markers).

```bash
we run test.unit
```

Equivalent to: `uv run pytest -m unit`

#### `we run test.integration`
Run only integration tests (requires pytest markers).

```bash
we run test.integration
```

Equivalent to: `uv run pytest -m integration`

### Coverage

#### `we run test.coverage`

Run tests with coverage report (HTML + terminal).

```bash
we run test.coverage
```

Coverage report is generated in `htmlcov/` directory.

#### `we run test.coverage.xml`
Run tests with XML coverage output (for CI).

```bash
we run test.coverage.xml
```

Generates `coverage.xml` for CI systems.

---

## Code Quality

### Linting

#### `we run lint`
Run ruff linter to check code quality.

```bash
we run lint
```

Equivalent to: `uv run ruff check .`

#### `we run lint.fix`
Run linter with auto-fix enabled.

```bash
we run lint.fix
```

Fixes automatically fixable issues.

### Formatting

#### `we run format`
Format code using ruff formatter.

```bash
we run format
```

Modifies files in-place.

#### `we run format.check`
Check code formatting without modifying files.

```bash
we run format.check
```

Returns non-zero exit code if formatting needed.

### Type Checking

#### `we run typecheck`
Run mypy type checker on source code.

```bash
we run typecheck
```

Equivalent to: `uv run mypy src/`

### Quality Checks

#### `we quality`
Run all quality checks (lint + typecheck).

```bash
we quality
```

Composite task that runs:
1. `lint` - Code linting
2. `typecheck` - Type checking

#### `we quality all`
Run all quality checks including tests.

```bash
we run quality.all
```

Composite task that runs:
1. `format.check` - Check formatting
2. `lint` - Code linting
3. `typecheck` - Type checking
4. `test` - Run tests

---

## Documentation

### `we run docs`
**Default:** `docs.serve`

Serve documentation locally (default action).

```bash
we run docs
# or explicitly:
we run docs.serve
```

#### `we run docs.setup`
Extract base MkDocs configuration from provide-foundry.

```bash
we run docs.setup
```

Extracts to `.provide/foundry/`:
- `base-mkdocs.yml`
- Theme assets
- Documentation partials
- Generation scripts

#### `we run docs.build`
Build documentation site.

```bash
we run docs.build
```

Builds to `site/` directory.

#### `we run docs.serve`
Serve documentation locally with auto-reload.

```bash
we run docs.serve
```

Typically serves on `http://127.0.0.1:11000/`

#### `we run docs.clean`
Remove documentation build artifacts.

```bash
we run docs.clean
```

Removes `site/` and `.provide/` directories.

---

## Link Checking

### `we run docs.links.check`
**Default:** `docs.links.check`

Check internal documentation links (fast).

```bash
we run docs.links.check
```

Uses lychee to validate:
- `./docs/**/*.md`
- `./src/**/*.md`
- `./README.md`
- `./.github/**/*.md`
- `./CONTRIBUTING.md`

**Performance:** <1 second for internal links

#### `we run docs.links.local`
Same as `we run docs.links.check` - check internal links only.

```bash
we run docs.links.local
```

Runs offline mode (no external URL checking).

#### `we run docs.links.external`
Check all links including external URLs.

```bash
we run docs.links.external
```

**Performance:** 2-5 minutes depending on network

**Note:** Requires lychee to be installed:
```bash
brew install lychee
# or see: https://github.com/lycheeverse/lychee#installation
```

---

## Mutation Testing

Mutation testing validates the quality of your tests by introducing bugs and checking if tests catch them.

### `we mutation`
Run mutation testing with mutmut.

```bash
we mutation
```

Equivalent to: `uv run mutmut run`

### Subtasks

#### `we mutation results`
Show mutation testing results summary.

```bash
we mutation results
```

#### `we mutation browse`
Open interactive mutation browser (web UI).

```bash
we mutation browse
```

#### `we mutation clean`
Clean mutation testing artifacts.

```bash
we mutation clean
```

Removes `.mutmut-cache` and `html/` directories.

---

## Build & Package

### `we build`
Build package distributions.

```bash
we build
```

Creates wheel and sdist in `dist/` directory.

Equivalent to: `uv build`

### Package Management

#### `we pkg install`
Install package in development/editable mode.

```bash
we run pkg.install
```

Equivalent to: `uv pip install -e .`

#### `we pkg uninstall`
Uninstall package.

```bash
we run pkg.uninstall
```

Auto-detects package name from `pyproject.toml`.

#### `we pkg lock`
Update dependency lock file.

```bash
we run pkg.lock
```

Equivalent to: `uv lock`

#### `we pkg version`
Show package version.

```bash
we run pkg.version
```

Reads from `VERSION` file or `pyproject.toml`.

---

## Development Shortcuts

Quick commands for common development tasks.

### `we dev setup`
Initialize development environment.

```bash
we dev setup
```

Equivalent to: `uv sync`

### `we dev test`
Quick test run (parallel mode).

```bash
we dev test
```

Equivalent to: `we run test.parallel`

### `we dev check`
Quick quality check (format + lint + typecheck).

```bash
we dev check
```

Runs code formatting, linting, and type checking in sequence.

---

## CI/CD Pipelines

Composite tasks for complete CI workflows.

### `we ci`
Complete CI pipeline (quality + test + build).

```bash
we ci
```

Runs in sequence:
1. `quality` - All quality checks
2. `test` - Run tests
3. `build` - Build package

#### `we ci test`
CI testing pipeline with coverage.

```bash
we run ci.test
```

Runs:
1. `test.parallel` - Parallel test execution
2. `test.coverage` - Coverage reporting

#### `we ci quality`
CI quality checks pipeline.

```bash
we run ci.quality
```

Runs:
1. `format.check` - Verify formatting
2. `lint` - Code linting
3. `typecheck` - Type checking

---

## Clean

### `we clean`
Remove all build artifacts and caches.

```bash
we run clean
```

Removes:
- `build/`, `dist/`, `*.egg-info`
- `.pytest_cache`, `.mypy_cache`, `.ruff_cache`
- `.hypothesis`, `htmlcov/`, `.coverage`
- `.mutmut-cache`, `site/`
- All `__pycache__` directories
- All `.pyc` and `.pyo` files

---

## Setup

### `we setup`
Initialize development environment.

```bash
we setup
```

Equivalent to: `uv sync`

#### `we setup pre_commit`
Install pre-commit hooks.

```bash
we run setup.pre_commit
```

Installs:
1. pre-commit tool (if not installed)
2. Standard pre-commit config from ci-tooling
3. Git hooks for commit and commit-msg

---

## Task Composition

Tasks can be combined in your project-specific `wrknv.toml`:

```toml
# Create custom composite tasks
[tasks.all-checks]
run = ["format", "lint", "typecheck", "test"]
description = "Run all checks sequentially"

[tasks.quick]
run = ["format", "lint", "test.fast"]
description = "Quick validation for rapid iteration"
```

## Environment Variables

Tasks can use environment variables:

```toml
[tasks.test.integration]
run = "uv run pytest tests/integration/"
env = { DATABASE_URL = "postgresql://localhost/test" }
timeout = 300.0
```

## Task Timeouts

Set timeouts for long-running tasks:

```toml
[tasks.mutation]
_default = "uv run mutmut run"
timeout = 1800.0  # 30 minutes
```

## Working Directories

Specify working directory for tasks:

```toml
[tasks.docs.api]
run = "python scripts/generate_api_docs.py"
working_dir = "./docs"
```

## Related Documentation

- [Deploying wrknv Tasks](deploying-wrknv-tasks.md) - How to deploy these tasks
- [Link Checking Guide](link-checking.md) - Link validation details
- [wrknv Documentation](../wrknv/README/) - Full wrknv user guide

## Customizing Tasks

Projects can customize or extend standard tasks in their `wrknv.toml`:

```toml
# Override standard task
[tasks.test]
_default = "uv run pytest -v --tb=short"

# Add project-specific task
[tasks.benchmark]
run = "uv run pytest benchmarks/ --benchmark-only"
description = "Run performance benchmarks"

# Extend standard task category
[tasks.docs.pdf]
run = "mkdocs build && pandoc site/index.html -o docs.pdf"
description = "Generate PDF documentation"
```

Custom tasks are preserved when extracting template updates.
