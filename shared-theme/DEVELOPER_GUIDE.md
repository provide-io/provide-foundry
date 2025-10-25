# Shared Theme Developer Guide

This guide is for developers working on the shared theme system itself. If you're just using the theme in a project, see [README.md](README.md) instead.

## Architecture

### Push-Based Distribution

The shared theme uses a **push-based distribution model** where theme files are synced from the central `provide-foundry/shared-theme/` directory to each project's `docs/.shared-theme/` directory.

**Design Decision**: This solves the `mkdocs serve` 404 problem where MkDocs cannot serve files from parent directories due to security restrictions.

### File Structure

```
provide-foundry/
├── shared-theme/              # Source of truth
│   ├── stylesheets/
│   │   ├── provide-theme.css  # Main theme styles
│   │   └── termynal.css       # Terminal simulator
│   ├── javascripts/
│   │   ├── mermaid-init.js    # Mermaid diagram config
│   │   ├── termynal.js        # Terminal animation engine
│   │   └── custom.js          # Termynal integration
│   ├── data/                  # YAML data for macros plugin
│   │   ├── contributors.yml
│   │   ├── external_links.yml
│   │   ├── people.yml
│   │   └── sponsors.yml
│   ├── assets/                # Images, logos, etc.
│   ├── README.md              # User documentation
│   └── DEVELOPER_GUIDE.md     # This file
└── scripts/
    └── sync_theme.py          # Distribution script

projects/
├── plating/
│   └── docs/
│       └── .shared-theme/     # Synced copy (gitignored)
├── wrknv/
│   └── docs/
│       └── .shared-theme/     # Synced copy (gitignored)
└── ... (10 more projects)
```

## The Sync Script

### Implementation Details

**File**: `provide-foundry/scripts/sync_theme.py`

**Technology**:
- Click framework for CLI
- `shutil.copytree()` for file copying
- `provide.foundation` for console output (`pout`, `perr`, `logger`)

**Commands**:
```bash
sync --all              # Sync to all 12 projects
sync --project <name>   # Sync to specific project
status                  # Show sync status
clean                   # Remove all .shared-theme directories
```

**How It Works**:
1. Finds provide-io root directory
2. Discovers all projects with `mkdocs.yml`
3. Removes old `.shared-theme/` directory (if exists)
4. Copies `provide-foundry/shared-theme/` → `project/docs/.shared-theme/`
5. Reports success/failure for each project

### Adding New Commands

To add a new command to the sync script:

```python
@click.command()
@click.option("--dry-run", is_flag=True, help="Show what would be done")
def your_command(dry_run: bool = False):
    """Your command description."""
    root = find_project_root()
    # Your logic here
    pout("✓ Command completed")

# Register the command
cli.add_command(your_command)
```

## Modifying Theme Files

### CSS Changes

**File**: `stylesheets/provide-theme.css`

**Structure**:
```css
/* Typography */
h1, h2, h3 { font-family: 'Chakra Petch', sans-serif; }

/* Interactive Elements */
.md-typeset a:hover { /* hover styles */ }

/* Layout Components */
.feature-grid { /* grid layout */ }

/* Terminal Simulator */
.termy { /* terminal styling */ }
```

**After making changes**:
```bash
cd provide-foundry
mkdocs serve  # Test locally
python scripts/sync_theme.py sync --all  # Distribute to all projects
```

### JavaScript Changes

**Files**:
- `javascripts/termynal.js` - Terminal animation engine (forked from FastAPI)
- `javascripts/custom.js` - Integration code
- `javascripts/mermaid-init.js` - Mermaid configuration

**Custom.js Integration**:
```javascript
// Initialize Termynal on page load
document.addEventListener('DOMContentLoaded', function() {
  const termyElements = document.querySelectorAll('.termy');
  termyElements.forEach(element => {
    new Termynal(element, {
      // Configuration options
    });
  });
});
```

**Testing JavaScript Changes**:
1. Edit the file in `provide-foundry/shared-theme/javascripts/`
2. Test with `mkdocs serve` in provide-foundry
3. Open browser console to check for errors
4. Test terminal animations on actual documentation pages
5. Sync to all projects when confirmed working

### Data Files

**Location**: `data/*.yml`

**Purpose**: Provide dynamic content via mkdocs-macros plugin

**Example** (`contributors.yml`):
```yaml
contributors:
  - name: "Developer Name"
    github: "username"
    contributions: 42
    avatar: "https://github.com/username.png"
```

**Usage in Markdown**:
```markdown
## Contributors

{% for contributor in contributors %}
- ![{{ contributor.name }}]({{ contributor.avatar }})
  [{{ contributor.name }}](https://github.com/{{ contributor.github }})
  - {{ contributor.contributions }} contributions
{% endfor %}
```

## Testing Workflow

### 1. Local Testing (provide-foundry)

```bash
cd provide-foundry

# Edit theme files
vim shared-theme/stylesheets/provide-theme.css

# Test immediately
mkdocs serve
# Open http://127.0.0.1:8000

# Check browser console for errors
# Verify visual changes
```

### 2. Single Project Testing

```bash
# Sync to one project for testing
python scripts/sync_theme.py sync --project plating

# Test in that project
cd ../plating
mkdocs serve
# Open http://127.0.0.1:8009
```

### 3. Full Rollout

```bash
cd provide-foundry

# Sync to all projects
python scripts/sync_theme.py sync --all

# Verify sync
python scripts/sync_theme.py status

# Spot-check a few projects
cd ../wrknv && mkdocs serve
cd ../pyvider && mkdocs serve
```

### 4. Build Verification

```bash
# Test that all projects build successfully
cd provide-io
for project in */mkdocs.yml; do
  echo "Building $(dirname $project)..."
  cd $(dirname $project)
  mkdocs build --strict || echo "FAILED: $project"
  cd ..
done
```

## Terminal Simulator (Termynal)

### How It Works

**Source**: Forked from FastAPI's implementation (originally by Ines Montani)

**Process**:
1. Finds all `.termy` divs in the page
2. Parses the console code block inside
3. Identifies command lines (start with `$`)
4. Identifies comments (start with `//`)
5. Identifies progress bars (`---> 100%`)
6. Animates typing for commands
7. Shows output instantly
8. Provides restart and fast-forward controls

**Syntax**:
```console
$ command to type          # Animated input
// Comment text            # Shows with 💬 emoji
---> 100%                  # Animated progress bar
Regular output             # Shown instantly
```

### Customizing Terminal Behavior

**File**: `javascripts/custom.js`

**Configuration Options**:
```javascript
new Termynal(element, {
  prefix: '$',           // Command prompt
  startDelay: 600,       // Initial delay (ms)
  typeDelay: 90,         // Typing speed (ms per char)
  lineDelay: 1500,       // Delay between lines (ms)
  progressLength: 40,    // Progress bar length
  progressChar: '█',     // Progress bar character
  cursor: '▋',           // Cursor character
  noInit: false          // Manual initialization
});
```

### Adding New Line Types

To add a new line type (like comments `//`):

1. **Update Termynal.js**:
```javascript
// In the render method
if (line.startsWith('// ')) {
  return this.renderComment(line.substring(3));
}

// Add render method
renderComment(text) {
  const div = document.createElement('div');
  div.className = 'termynal-comment';
  div.textContent = `💬 ${text}`;
  return div;
}
```

2. **Update CSS** (`termynal.css`):
```css
.termynal-comment {
  color: #6c757d;
  font-style: italic;
}
```

3. **Test and distribute**:
```bash
mkdocs serve  # Test locally
python scripts/sync_theme.py sync --all
```

## MkDocs Path Resolution

### Understanding Path Types

**`extra_css` and `extra_javascript`**: Relative to `docs_dir`
```yaml
docs_dir: docs
extra_css:
  - .shared-theme/stylesheets/provide-theme.css  # Resolves to docs/.shared-theme/...
```

**`macros.include_dir`**: Relative to **project root** (not docs_dir)
```yaml
plugins:
  - macros:
      include_dir: docs/.shared-theme/data  # Relative to project root
```

### Why This Matters

When we migrated from pull-based (`../provide-foundry/shared-theme/`) to push-based (`.shared-theme/`), we had to update:

1. ✅ `extra_css`: `.shared-theme/...` (works - relative to docs_dir)
2. ✅ `extra_javascript`: `.shared-theme/...` (works - relative to docs_dir)
3. ❌ `macros.include_dir`: `.shared-theme/data` (WRONG - mkdocs looks at project root)
4. ✅ `macros.include_dir`: `docs/.shared-theme/data` (CORRECT)

## Common Issues & Solutions

### Issue: 404 errors for theme files

**Symptom**: Browser console shows 404 for `.shared-theme/stylesheets/provide-theme.css`

**Cause**: Theme not synced to project

**Solution**:
```bash
cd provide-foundry
python scripts/sync_theme.py sync --project <project-name>
```

### Issue: Macros can't find data files

**Symptom**: `FileNotFoundError: MACROS ERROR: Include directory '.shared-theme/data' does not exist!`

**Cause**: Wrong path in `mkdocs.yml` (macros plugin resolves from project root)

**Solution**: Change `include_dir: .shared-theme/data` → `include_dir: docs/.shared-theme/data`

### Issue: Terminal animations not working

**Symptom**: Terminal blocks show as static code blocks

**Possible Causes**:
1. Missing `.termy` wrapper div
2. JavaScript not loaded
3. Console errors in browser

**Debug Steps**:
```bash
# 1. Check theme is synced
ls docs/.shared-theme/javascripts/termynal.js

# 2. Check mkdocs.yml references
grep "termynal.js" mkdocs.yml

# 3. Check browser console
# Open DevTools → Console → Look for errors

# 4. Verify HTML structure
# View source → Search for "termy" class
```

### Issue: Changes not appearing

**Symptom**: Made changes to theme but they don't show up

**Cause**: Browser cache or forgot to sync

**Solution**:
```bash
# Clear browser cache (Cmd+Shift+R / Ctrl+F5)

# Re-sync theme
cd provide-foundry
python scripts/sync_theme.py sync --all

# Verify sync
python scripts/sync_theme.py status

# Restart mkdocs serve
cd ../plating
mkdocs serve
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Documentation

on:
  push:
    paths:
      - 'provide-foundry/shared-theme/**'

jobs:
  sync-theme:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Sync theme to all projects
        run: |
          cd provide-foundry
          python scripts/sync_theme.py sync --all

      - name: Commit changes
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add -A
          git commit -m "Sync shared theme to all projects" || exit 0
          git push
```

**Note**: This is optional - sync can be manual or automated.

## Future Enhancements

### Potential Improvements

1. **Version Tracking**: Add `.theme-version` file with checksum
   ```bash
   # In each project
   echo "$(git -C provide-foundry rev-parse HEAD:shared-theme)" > docs/.theme-version
   ```

2. **Pre-commit Hook**: Auto-sync theme on commit
   ```bash
   # .git/hooks/pre-commit
   #!/bin/bash
   cd provide-foundry && python scripts/sync_theme.py sync --all
   ```

3. **Diff Check**: Only sync if theme changed
   ```python
   def theme_changed(project: Path, theme_source: Path) -> bool:
       checksum_file = project / "docs" / ".theme-version"
       current_checksum = calculate_checksum(theme_source)
       if checksum_file.exists():
           stored_checksum = checksum_file.read_text()
           return current_checksum != stored_checksum
       return True
   ```

4. **Selective Sync**: Sync only changed files
   ```python
   def sync_changed_files_only(project: Path, theme_source: Path):
       for src_file in theme_source.rglob("*"):
           dst_file = project / "docs" / ".shared-theme" / src_file.relative_to(theme_source)
           if not dst_file.exists() or files_differ(src_file, dst_file):
               shutil.copy2(src_file, dst_file)
   ```

## Contributing

When contributing to the shared theme:

1. **Test locally first** in provide-foundry
2. **Test in one project** before rolling out
3. **Check all 12 projects build** after sync
4. **Document breaking changes** in commit message
5. **Update this guide** if adding new features

## Questions?

- Review the main [README.md](README.md) for user documentation
- Check [DOCUMENTATION_GUIDE.md](../../docs/DOCUMENTATION_GUIDE.md) for usage patterns
- Review commit history for past changes
- Ask in the provide.io discussion forum

---

**Maintained by**: provide.io team
**Last Updated**: 2025-10-24
**Related**: [README.md](README.md), [DOCUMENTATION_GUIDE.md](../../docs/DOCUMENTATION_GUIDE.md)
