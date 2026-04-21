# IDE Setup Guide

Complete guide for setting up your IDE for development in the provide.io ecosystem.

## Overview

All projects in the provide.io ecosystem are Python 3.11+ projects using modern tooling:
- **UV** for package management
- **Ruff** for linting and formatting
- **pytest** for testing
- **mypy/pyright** for type checking

This guide helps you configure VSCode or PyCharm for optimal development experience.

## Quick Start

For any project in the ecosystem:

```bash
# Navigate to project
cd /path/to/project

# Set up environment
uv sync

# Open in your IDE
code .  # VSCode
# or open with PyCharm File → Open
```

---

## Standard IDE Configuration

The following configuration works for all ecosystem projects:

--8<-- ".provide/foundry/docs/_partials/ide-setup.md"

---

## Ecosystem-Specific Configuration

### Multi-Project Development

When working across multiple ecosystem projects:

**VSCode Workspace (`provide-io.code-workspace`):**

```json
{
  "folders": [
    {"path": "provide-foundation"},
    {"path": "provide-testkit"},
    {"path": "pyvider"},
    {"path": "pyvider-cty"},
    {"path": "pyvider-hcl"},
    {"path": "pyvider-rpcplugin"},
    {"path": "pyvider-components"},
    {"path": "flavorpack"},
    {"path": "wrknv"},
    {"path": "supsrc"},
    {"path": "tofusoup"},
    {"path": "plating"}
  ],
  "settings": {
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.testing.pytestEnabled": true,
    "[python]": {
      "editor.defaultFormatter": "charliermarsh.ruff",
      "editor.formatOnSave": true
    }
  }
}
```

**PyCharm Multi-Module Project:**

1. File → Open → Select parent directory `/Users/tim/code/gh/provide-io/`
2. Each subdirectory becomes a module
3. Configure Python interpreter per module
4. Mark `src/` as Sources Root in each module

### Project-Specific Settings

**Foundation Projects** (provide-foundation, provide-testkit):
```json
{
  "python.testing.pytestArgs": [
    "tests",
    "-v",
    "--cov=provide.foundation"  // or provide.testkit
  ]
}
```

**Pyvider Projects** (pyvider, pyvider-cty, pyvider-hcl, pyvider-rpcplugin):
```json
{
  "python.testing.pytestArgs": [
    "tests",
    "-v",
    "-n", "auto"  // Parallel execution
  ]
}
```

**Tool Projects** (flavorpack, wrknv, supsrc, tofusoup):
```json
{
  "python.testing.pytestArgs": [
    "tests",
    "-v",
    "-m", "not slow"  // Skip slow tests during development
  ]
}
```

## Testing Integration

### Running Tests from IDE

**VSCode Test Explorer:**

1. Install Python extension
2. Open Testing sidebar (beaker icon)
3. Tests auto-discover from `tests/` directory
4. Click play button to run tests
5. Click debug icon to debug tests

**PyCharm Test Runner:**

1. Right-click `tests/` directory
2. Select "Run pytest in tests"
3. Tests appear in Run tool window
4. Use debug icon for breakpoint debugging

### Debugging Tests

**VSCode Launch Configuration:**

```json
{
  "name": "Debug Current Test File",
  "type": "debugpy",
  "request": "launch",
  "module": "pytest",
  "args": [
    "${file}",
    "-v",
    "-s",
    "--no-cov"  // Disable coverage during debugging
  ],
  "console": "integratedTerminal",
  "justMyCode": false,
  "env": {
    "PYTHONPATH": "${workspaceFolder}/src:${workspaceFolder}"
  }
}
```

**PyCharm Debug Configuration:**

- Configuration type: Python tests → pytest
- Target: Current file
- Additional arguments: `-v -s --no-cov`
- Working directory: Project root
- Environment variables: `PYTHONPATH=src`

## Code Quality Integration

### Pre-Commit Hooks

All projects use pre-commit hooks:

```bash
# Install hooks (run once per project)
pre-commit install

# Run manually
pre-commit run --all-files
```

**VSCode Integration:**

Add task to `.vscode/tasks.json`:

```json
{
  "label": "Pre-commit Check",
  "type": "shell",
  "command": "pre-commit run --all-files",
  "group": "test",
  "presentation": {
    "reveal": "always",
    "panel": "new"
  }
}
```

**PyCharm Integration:**

- Settings → Tools → External Tools → Add
- Name: Pre-commit
- Program: `$ProjectFileDir$/.venv/bin/pre-commit`
- Arguments: `run --all-files`
- Working directory: `$ProjectFileDir$`

### Type Checking

Projects use different type checkers:

| Project | Type Checker | Command |
|---------|-------------|---------|
| provide-foundation | mypy | `uv run mypy src/` |
| pyvider-* | mypy | `uv run mypy src/` |
| flavorpack | mypy | `uv run mypy src/flavor` |
| wrknv | mypy | `uv run mypy src/` |

**VSCode Type Checking:**

```json
{
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.diagnosticMode": "workspace",
  "python.analysis.autoImportCompletions": true
}
```

**PyCharm Type Checking:**

- Settings → Editor → Inspections → Python
- Enable: Type checker, Missing type hinting
- Set severity to Warning or Error

## Troubleshooting

### Import Errors

**Problem:** IDE shows import errors but code runs fine

**Solution:**
```json
// VSCode - Add to settings.json
{
  "python.analysis.extraPaths": ["src"],
  "python.analysis.autoSearchPaths": true
}

// PyCharm - Mark directories
// Right-click src/ → Mark Directory as → Sources Root
```

### Tests Not Discovered

**Problem:** Tests don't appear in test explorer

**Solution:**

VSCode:
```bash
# Reload test discovery
Python: Discover Tests (Command Palette)

# Check pytest is installed
uv run pytest --version
```

PyCharm:
- Settings → Tools → Python Integrated Tools
- Set Default test runner to pytest
- Invalidate Caches (File → Invalidate Caches)

### Linter Not Working

**Problem:** Ruff not formatting/linting

**Solution:**

VSCode:
```bash
# Check ruff is installed
uv run ruff --version

# Reinstall extension
code --install-extension charliermarsh.ruff --force
```

PyCharm:
- Install Ruff external tool
- Configure file watcher for auto-format

### Debugger Not Stopping at Breakpoints

**Problem:** Breakpoints are ignored

**Solution:**

VSCode:
```json
{
  "justMyCode": false,  // Debug into libraries
  "redirectOutput": true
}
```

PyCharm:
- Run → Edit Configurations
- Ensure "Attach to subprocess" is enabled
- Check breakpoint is not disabled (red dot vs gray)

## Best Practices

### Development Workflow

1. **Start fresh:** `uv sync` before coding session
2. **Format on save:** Enable auto-format in IDE
3. **Run tests frequently:** Use IDE shortcuts (Ctrl+Shift+F10)
4. **Type check regularly:** Fix type errors as you code
5. **Pre-commit before push:** Ensure hooks pass locally

### Performance Tips

1. **Exclude build directories:**
   ```json
   {
     "files.watcherExclude": {
       "**/.venv/**": true,
       "**/workenv/**": true,
       "**/__pycache__/**": true,
       "**/.pytest_cache/**": true,
       "**/.mypy_cache/**": true,
       "**/site/**": true,
       "**/dist/**": true
     }
   }
   ```

2. **Limit test auto-discovery:**
   ```json
   {
     "python.testing.autoTestDiscoverOnSaveEnabled": false
   }
   ```

3. **Use focused tests during development:**
   ```bash
   # Only run tests related to current work
   uv run pytest tests/test_specific_feature.py -v
   ```

## Additional Resources

- [VSCode Python Documentation](https://code.visualstudio.com/docs/python/python-tutorial)
- [PyCharm Python Guide](https://www.jetbrains.com/help/pycharm/quick-start-guide.html)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)

---

**Next Steps:**
- [Development Workflow Guide](development-workflow.md) - Day-to-day development patterns
- [Testing Patterns Guide](testing-patterns.md) - Testing strategies across projects
