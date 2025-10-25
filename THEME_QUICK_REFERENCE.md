# Shared Theme Quick Reference

> One-page cheat sheet for working with the provide.io shared documentation theme

## Daily Usage

### After Editing Theme Files

```bash
cd provide-foundry
python scripts/sync_theme.py sync --all
```

### Check Sync Status

```bash
cd provide-foundry
python scripts/sync_theme.py status
```

### Sync to Specific Project

```bash
cd provide-foundry
python scripts/sync_theme.py sync --project plating
```

## Common Commands

| Command | Purpose |
|---------|---------|
| `sync --all` | Sync theme to all 12 projects |
| `sync --project <name>` | Sync to specific project |
| `status` | Show which projects have synced theme |
| `clean` | Remove all `.shared-theme/` directories |
| `sync --dry-run --all` | Preview what would be synced |

## File Locations

### Source (Edit Here)
```
provide-foundry/shared-theme/
├── stylesheets/
│   ├── provide-theme.css      # Main theme CSS
│   └── termynal.css           # Terminal animations
├── javascripts/
│   ├── termynal.js            # Terminal engine
│   ├── custom.js              # Integration code
│   └── mermaid-init.js        # Diagram config
└── data/
    ├── contributors.yml       # Data files for macros
    ├── external_links.yml
    ├── people.yml
    └── sponsors.yml
```

### Destination (Auto-Generated)
```
project-name/docs/.shared-theme/  # Copied by sync script (gitignored)
```

## MkDocs Configuration

### Correct Paths in `mkdocs.yml`

```yaml
plugins:
  - macros:
      include_dir: docs/.shared-theme/data  # Relative to project root

extra_css:
  - .shared-theme/stylesheets/provide-theme.css  # Relative to docs_dir
  - .shared-theme/stylesheets/termynal.css

extra_javascript:
  - https://unpkg.com/mermaid@10/dist/mermaid.min.js
  - .shared-theme/javascripts/mermaid-init.js
  - .shared-theme/javascripts/termynal.js
  - .shared-theme/javascripts/custom.js
```

### .gitignore Entry

```gitignore
# Synced theme files (source: provide-foundry/shared-theme/)
docs/.shared-theme/
```

## Terminal Animations

### Basic Syntax

````markdown
<div class="termy">

```console
$ command to execute          # Animated typing
// Comment about the command  # Shows with 💬
Output from command           # Instant display
---> 100%                     # Progress bar
```

</div>
````

### Line Prefixes

| Prefix | Behavior |
|--------|----------|
| `$` | Animated command input |
| `//` | Comment with 💬 emoji |
| `---> 100%` | Animated progress bar |
| (none) | Instant output display |

## Testing Workflow

### 1. Local Testing (Fastest)

```bash
cd provide-foundry
# Edit shared-theme/stylesheets/provide-theme.css
mkdocs serve  # Test at http://127.0.0.1:8000
```

### 2. Single Project Test

```bash
cd provide-foundry
python scripts/sync_theme.py sync --project plating

cd ../plating
mkdocs serve  # Test at configured port
```

### 3. Full Rollout

```bash
cd provide-foundry
python scripts/sync_theme.py sync --all
python scripts/sync_theme.py status  # Verify
```

## Troubleshooting

### 404 Errors for Theme Files

**Solution:** Theme not synced

```bash
cd provide-foundry
python scripts/sync_theme.py sync --project <project>
```

### Macros Can't Find Data Files

**Problem:** Wrong path in `mkdocs.yml`

```yaml
# ❌ Wrong
plugins:
  - macros:
      include_dir: .shared-theme/data

# ✅ Correct
plugins:
  - macros:
      include_dir: docs/.shared-theme/data
```

### Terminal Animations Not Working

**Check:**
1. `.termy` wrapper div present?
2. JavaScript loaded? (check browser console)
3. Theme synced? `ls docs/.shared-theme/javascripts/`

### Changes Not Appearing

```bash
# Clear browser cache (Cmd+Shift+R / Ctrl+F5)
cd provide-foundry
python scripts/sync_theme.py sync --all
# Restart mkdocs serve
```

## Projects Using Theme

All 12 projects in the ecosystem:
- plating
- wrknv
- tofusoup
- supsrc
- provide-foundation
- provide-testkit
- pyvider
- pyvider-cty
- pyvider-hcl
- pyvider-rpcplugin
- flavorpack
- provide-foundry

## Path Resolution Rules

| Config Option | Relative To | Example |
|--------------|-------------|---------|
| `extra_css` | `docs_dir` | `.shared-theme/stylesheets/` |
| `extra_javascript` | `docs_dir` | `.shared-theme/javascripts/` |
| `macros.include_dir` | **Project root** | `docs/.shared-theme/data` |

## Additional Resources

- **User Docs:** `provide-foundry/shared-theme/README.md`
- **Developer Guide:** `provide-foundry/shared-theme/DEVELOPER_GUIDE.md`
- **Full Guide:** `docs/DOCUMENTATION_GUIDE.md`
- **Handoff:** `HANDOFF_PUSH_BASED_THEME.md`

## Emergency Commands

```bash
# Remove all synced themes (nuclear option)
cd provide-foundry
python scripts/sync_theme.py clean

# Re-sync everything from scratch
python scripts/sync_theme.py sync --all

# Verify all projects have theme
python scripts/sync_theme.py status
```

---

**Quick Tip:** Always sync after editing theme files! Your changes won't appear in projects until synced.

**Remember:** Theme files are gitignored in projects. The source of truth is `provide-foundry/shared-theme/`.
