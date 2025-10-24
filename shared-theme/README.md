# Provide.io Shared Theme

This directory contains the shared MkDocs Material theme used across all provide.io documentation.

## Usage

To use the shared theme in your project's `mkdocs.yml`:

```yaml
theme:
  name: material
  # ... other theme config ...

extra_css:
  - ../../provide-foundry/shared-theme/stylesheets/provide-theme.css

extra_javascript:
  - https://unpkg.com/mermaid@10/dist/mermaid.min.js
  - ../../provide-foundry/shared-theme/javascripts/mermaid-init.js
```

## Structure

- `stylesheets/provide-theme.css` - Main theme CSS based on provide-foundation's mature theme
- `javascripts/mermaid-init.js` - Mermaid diagram initialization with provide.io colors
- `assets/` - Shared assets (logos, images, etc.)

## Features

### Typography
- **Headers (H1-H3)**: Chakra Petch font family (bold, professional)
- **Smaller headers (H4-H6)**: IBM Plex Serif
- **Body text**: System font stack for optimal readability
- **Code**: Monospace font stack (SF Mono, Menlo, Monaco, Consolas)

### Interactive Elements
- Smooth hover transitions on all links and navigation
- Fade-in permalink anchors on header hover
- Accent color highlights for hover states

### Layout Components
- `.feature-grid` - Responsive grid for feature cards
- `.feature-card` - Individual feature card with hover effects
- `.getting-started-grid` - Getting started section layout
- `.getting-started-card` - Getting started card with CTA button

### Spacing & Rhythm
- Professional header spacing (2.5rem, 2rem, 1.75rem for H1-H3)
- Optimal paragraph line-height (1.7)
- Consistent list and code block spacing

## Customization

Individual projects can override or extend the shared theme by adding their own CSS after the shared theme:

```yaml
extra_css:
  - ../../provide-foundry/shared-theme/stylesheets/provide-theme.css
  - stylesheets/project-specific.css  # Project overrides
```

## Maintenance

The shared theme is maintained in the `provide-foundry` repository. Updates to the theme will automatically propagate to all projects using it.

### Updating Projects

After updating the shared theme:

1. Run `make docs-collect` in provide-foundry to refresh aggregated docs
2. Individual projects will pick up changes on next build
3. No action needed for aggregated documentation site

## Design Philosophy

- **Professional**: Clean, corporate-appropriate styling
- **Readable**: Optimal typography and spacing
- **Consistent**: Same look across all provide.io docs
- **Accessible**: High contrast, clear hierarchy
- **Interactive**: Smooth transitions and hover states
