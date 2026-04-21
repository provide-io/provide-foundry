# Deploying wrknv Task Definitions Across the Ecosystem

This guide explains how to deploy standardized task definitions from provide-foundry to projects in the provide.io ecosystem using the wrknv task runner.

## Overview

The provide.io ecosystem uses centralized task templates stored in provide-foundry that can be extracted to individual projects. This ensures consistency across repositories while allowing per-project customization.

## Task Templates

The template is located at:
- **`wrknv.python.tmpl`** - For Python library projects

This template provides standardized tasks for:
- Testing (test, test.parallel, test.coverage)
- Code quality (lint, format, typecheck, quality)
- Documentation (docs.build, docs.serve, docs.links.check)
- Mutation testing (mutation)
- Build & packaging (build, pkg.install, pkg.lock)
- CI/CD pipelines (ci, ci.test, ci.quality)

## Deployment Methods

### Method 1: Python Command (Recommended)

```bash
cd /path/to/project
python -c "from provide.foundry.config import extract_python_wrknv_tasks; from pathlib import Path; extract_python_wrknv_tasks(Path('.'))"
```

### Method 2: Using UV

```bash
cd /path/to/project
uv run python -c "from provide.foundry.config import extract_python_wrknv_tasks; from pathlib import Path; extract_python_wrknv_tasks(Path('.'))"
```

### Method 3: From Parent Directory

If running from the ecosystem parent directory with all projects installed:

```bash
cd /Users/tim/code/gh/provide-io
uv run python -c "from provide.foundry.config import extract_python_wrknv_tasks; from pathlib import Path; extract_python_wrknv_tasks(Path('project-name'))"
```

## Task Merging Behavior

The extraction function intelligently merges tasks:

1. **Existing wrknv.toml**: Tasks from template are merged with existing custom tasks
2. **Custom tasks preserved**: Your project-specific tasks (like wrknv's "hello" task) are kept
3. **Standard tasks updated**: Template tasks override existing standard tasks
4. **Other config preserved**: Project metadata, tools, profiles, workenv settings remain unchanged

## Deployment Workflow

### 1. Update Template in provide-foundry

The template is located at:
```
provide-foundry/src/provide/foundry/config/wrknv.python.tmpl
```

Edit the template and commit changes.

### 2. Deploy to Core Projects

Currently deployed to 5 core projects:
- provide-foundry
- wrknv
- pyvider
- pyvider-cty
- pyvider-rpcplugin

```bash
#!/bin/bash
# deploy-wrknv-tasks.sh

cd /Users/tim/code/gh/provide-io

PROJECTS=(
    "provide-foundry"
    "wrknv"
    "pyvider"
    "pyvider-cty"
    "pyvider-rpcplugin"
)

for project in "${PROJECTS[@]}"; do
    if [ -d "$project" ]; then
        echo "Updating: $project"
        uv run python -c "from provide.foundry.config import extract_python_wrknv_tasks; from pathlib import Path; extract_python_wrknv_tasks(Path('$project'))"
        echo "✅ Updated $project"
    else
        echo "⚠️  Skipping (not found): $project"
    fi
done
```

### 3. Deploy to Additional Projects

For other Python libraries that want to adopt wrknv tasks:

```bash
#!/bin/bash
# deploy-additional-projects.sh

ADDITIONAL_PROJECTS=(
    "provide-foundation"
    "provide-testkit"
    "pyvider-hcl"
    "pyvider-components"
    "flavorpack"
    "wrknv"
    "tofusoup"
    "supsrc"
    "plating"
)

# Same deployment loop as above
```

## Post-Deployment

### 1. Verify Installation

In each updated project:

```bash
we tasks
```

You should see hierarchical task listing:
```
docs
├── _default (default)
├── build
├── clean
├── serve
└── setup

docs.links
├── _default (default)
├── check
├── external
└── local

test
├── _default (default)
├── parallel
├── coverage
...
```

### 2. Test Task Execution

```bash
# Run a simple task
we run test

# Run nested task
we run docs.links.check

# Show task info
we run test --info

# Dry run
we run build --dry-run
```

### 3. Customize Per-Project

Each project can add custom tasks to their `wrknv.toml`:

```toml
# Project-specific custom tasks
[tasks.custom]
deploy = "bash scripts/deploy.sh"
benchmark = "uv run pytest benchmarks/ --benchmark-only"

[tasks.hello]
run = "echo 'Welcome to this project!'"
description = "Custom greeting"
```

These custom tasks will be preserved when extracting template updates.

## Comparison with Makefiles

### Before (Makefile approach):
```makefile
docs-build: docs-setup
    @mkdocs build

links-check-local:
    @lychee --offline ...
```

### After (wrknv tasks):
```toml
[tasks.docs]
build = "uv run mkdocs build"
setup = "python -c \"from provide.foundry.config import extract_base_mkdocs...\""

[tasks.docs.links]
check = "lychee --offline ..."
local = "lychee --offline ..."
```

### Benefits:
1. **Hierarchical organization**: `docs.links.check` vs `links-check-local`
2. **Discoverable**: `we tasks` shows all available tasks
3. **No extraction needed**: wrknv.toml is source-controlled, not generated
4. **Cleaner syntax**: TOML vs Make
5. **Better UX**: `we run test` vs `make test`

## Migration from Makefiles

For projects migrating from Makefiles to wrknv:

### 1. Extract wrknv tasks
```bash
python -c "from provide.foundry.config import extract_python_wrknv_tasks; from pathlib import Path; extract_python_wrknv_tasks(Path('.'))"
```

### 2. Remove Makefile
```bash
rm Makefile
```

### 3. Update CI/CD workflows
Replace make commands with `we run`:
```yaml
# Before
- name: Run tests
  run: make test

# After
- name: Run tests
  run: we run test
```

### 4. Update README
Change documentation examples from `make` to `we`:
```markdown
# Before
make test
make lint

# After
we run test
we run lint
```

## Verification Script

Create a script to verify all projects have tasks deployed:

```bash
#!/bin/bash
# verify-wrknv-tasks.sh

echo "Checking for wrknv.toml in all projects..."

for project in provide-foundry wrknv pyvider pyvider-cty pyvider-rpcplugin; do
    if [ -f "/Users/tim/code/gh/provide-io/$project/wrknv.toml" ]; then
        # Count tasks
        task_count=$(grep -c "^\[tasks" "/Users/tim/code/gh/provide-io/$project/wrknv.toml" || echo "0")
        echo "✅ $project ($task_count task sections)"
    else
        echo "❌ $project (no wrknv.toml)"
    fi
done
```

## Rollback

If you need to roll back changes:

1. **Revert template changes** in provide-foundry
2. **Re-extract** to affected projects using the deployment methods above
3. Or **restore from git**: `git checkout wrknv.toml`

## Best Practices

1. **Test templates** in provide-foundry first before deploying
2. **Document changes** in the template file header comments
3. **Communicate updates** to the team before mass deployment
4. **Version control** - commit wrknv.toml updates in each project
5. **Gradual rollout** - deploy to 1-2 projects first to verify
6. **Preserve custom tasks** - the merge function protects project-specific tasks

## Template Update Guidelines

When modifying templates:

1. **Maintain compatibility** - Don't break existing task names
2. **Use consistent patterns**:
   - Hierarchical tasks: `[tasks.category.subtask]`
   - Default tasks: `_default = "command"`
   - Composite tasks: `run = ["task1", "task2"]`
3. **Add descriptions** for complex tasks
4. **Test extraction** - Verify templates extract correctly
5. **Update documentation** - Document new tasks in this file

## Troubleshooting

### "Module not found: provide.foundry.config"

**Solution:** Ensure provide-foundry is installed in the environment:
```bash
uv sync  # or uv pip install -e /path/to/provide-foundry
```

### "Permission denied" when extracting

**Solution:** Check file permissions:
```bash
chmod 644 wrknv.toml
```

### Template changes not reflected

**Solution:** Ensure you're running extraction from a project with access to the updated provide-foundry package:
```bash
uv sync --force
```

### Custom tasks disappeared

**Solution:** The merge function should preserve custom tasks. If lost, restore from git:
```bash
git diff wrknv.toml  # Check what changed
git checkout HEAD -- wrknv.toml  # Restore if needed
```

## Related Documentation

- [wrknv Task Reference](wrknv-task-reference.md) - Complete task documentation
- [Link Checking Guide](link-checking.md) - Link validation with wrknv

## Questions or Issues

If you encounter issues deploying templates:

1. Check provide-foundry installation
2. Verify Python path and environment
3. Check file permissions
4. Review merge behavior (custom tasks should be preserved)
5. Consult this documentation
6. Ask in team channels
