# Documentation Guide

Comprehensive guide to creating, maintaining, and publishing documentation for the provide.foundation ecosystem using modern documentation tools and best practices.

## Overview

This guide covers documentation strategies, tooling, automation, and best practices for creating high-quality documentation across all provide.foundation projects, including Pyvider-based Terraform providers and related tools.

## Documentation Philosophy

### Principles

- **User-Centric**: Documentation serves users first, developers second
- **Comprehensive**: Cover all use cases from beginner to advanced
- **Accurate**: Keep documentation in sync with code changes
- **Accessible**: Make information easy to find and understand
- **Maintainable**: Use automation to reduce manual maintenance burden

### Documentation Types

1. **API Documentation**: Auto-generated from code annotations
2. **User Guides**: Step-by-step instructions for common tasks
3. **Tutorials**: Learning-oriented, hands-on examples
4. **Reference**: Comprehensive information for lookup
5. **Architecture**: High-level system design and decisions

## Documentation Stack

### Core Tools

- **MkDocs**: Static site generator with Markdown support
- **Material for MkDocs**: Modern, responsive theme
- **mkdocstrings**: Automatic API documentation from Python docstrings
- **PlantUML**: Diagram generation from text
- **Mermaid**: Interactive diagrams and flowcharts

### Installation and Setup

```bash
# Install documentation tools
uv add mkdocs mkdocs-material mkdocstrings[python] mkdocs-mermaid2-plugin

# Create documentation structure
mkdocs new my-project-docs
cd my-project-docs

# Customize configuration
cp ../templates/mkdocs.yml .
```

## Project Documentation Structure

### Standard Layout

```
docs/
├── index.md                    # Project overview
├── getting-started/
│   ├── index.md               # Quick start guide
│   ├── installation.md        # Installation instructions
│   └── configuration.md       # Basic configuration
├── guides/
│   ├── index.md               # Guide overview
│   ├── user-guide.md          # Comprehensive user guide
│   ├── api-guide.md           # API usage guide
│   └── troubleshooting.md     # Common issues and solutions
├── tutorials/
│   ├── index.md               # Tutorial overview
│   ├── basic-tutorial.md      # Beginner tutorial
│   └── advanced-tutorial.md   # Advanced use cases
├── reference/
│   ├── index.md               # Reference overview
│   ├── api/                   # Auto-generated API docs
│   ├── configuration.md       # Configuration reference
│   └── cli.md                 # Command-line reference
├── architecture/
│   ├── index.md               # Architecture overview
│   ├── design-decisions.md    # ADRs and design choices
│   └── diagrams/              # Architecture diagrams
└── examples/
    ├── index.md               # Examples overview
    ├── basic-examples.md      # Simple examples
    └── advanced-examples.md   # Complex scenarios
```

## MkDocs Configuration

### Basic Configuration

```yaml
# mkdocs.yml
site_name: My Project Documentation
site_description: Comprehensive documentation for My Project
site_url: https://my-project.readthedocs.io

# Repository
repo_url: https://github.com/provide-io/my-project
repo_name: my-project
edit_uri: edit/main/docs/

# Theme
theme:
  name: material
  palette:
    # Light mode
    - scheme: default
      primary: blue
      accent: blue
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    # Dark mode
    - scheme: slate
      primary: blue
      accent: blue
      toggle:
        icon: material/brightness-4
        name: Switch to light mode

  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.highlight
    - search.share
    - search.suggest
    - content.code.copy
    - content.action.edit
    - content.action.view

  icon:
    repo: fontawesome/brands/github
    edit: material/pencil
    view: material/eye

# Navigation
nav:
  - Home: index.md
  - Getting Started:
    - Overview: getting-started/index.md
    - Installation: getting-started/installation.md
    - Configuration: getting-started/configuration.md
  - User Guide:
    - Overview: guides/index.md
    - User Guide: guides/user-guide.md
    - API Guide: guides/api-guide.md
    - Troubleshooting: guides/troubleshooting.md
  - Tutorials:
    - Overview: tutorials/index.md
    - Basic Tutorial: tutorials/basic-tutorial.md
    - Advanced Tutorial: tutorials/advanced-tutorial.md
  - Reference:
    - Overview: reference/index.md
    - API Reference: reference/api/
    - Configuration: reference/configuration.md
    - CLI Reference: reference/cli.md
  - Architecture:
    - Overview: architecture/index.md
    - Design Decisions: architecture/design-decisions.md
  - Examples:
    - Overview: examples/index.md
    - Basic Examples: examples/basic-examples.md
    - Advanced Examples: examples/advanced-examples.md

# Plugins
plugins:
  - search:
      lang: en
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
            docstring_section_style: table
            show_root_heading: true
            show_root_toc_entry: false
            show_source: true
            members_order: source
            group_by_category: true
            show_category_heading: true
  - mermaid2:
      arguments:
        theme: base
        themeVariables:
          primaryColor: '#2196F3'

# Markdown extensions
markdown_extensions:
  - abbr
  - admonition
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - toc:
      permalink: true
  - tables
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.betterem:
      smart_enable: all
  - pymdownx.caret
  - pymdownx.details
  - pymdownx.emoji:
      emoji_index: !!python/name:materialx.emoji.twemoji
      emoji_generator: !!python/name:materialx.emoji.to_svg
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.keys
  - pymdownx.magiclink:
      repo_url_shorthand: true
      user: provide-io
      repo: my-project
  - pymdownx.mark
  - pymdownx.smartsymbols
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.tilde

# Extra CSS and JavaScript
extra_css:
  - stylesheets/extra.css

extra_javascript:
  - javascripts/mathjax.js
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js

# Additional configuration
extra:
  version:
    provider: mike
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/provide-io/my-project
    - icon: fontawesome/brands/python
      link: https://pypi.org/project/my-project/
    - icon: fontawesome/solid/globe
      link: https://provide.foundation
```

## API Documentation

### Docstring Standards

```python
"""
Module for handling user authentication and authorization.

This module provides classes and functions for managing user sessions,
authentication tokens, and access control within the application.

Example:
    >>> from myproject.auth import AuthManager
    >>> auth = AuthManager()
    >>> user = auth.authenticate("username", "password")
    >>> print(user.permissions)
    ['read', 'write']
"""

class AuthManager:
    """
    Manages user authentication and session handling.

    The AuthManager class provides a centralized interface for user
    authentication, session management, and permission checking.

    Attributes:
        session_timeout (int): Session timeout in seconds.
        max_login_attempts (int): Maximum failed login attempts before lockout.

    Example:
        >>> auth = AuthManager(session_timeout=3600)
        >>> success = auth.authenticate("user@example.com", "password123")
        >>> if success:
        ...     print("Authentication successful")
    """

    def __init__(self, session_timeout: int = 1800, max_attempts: int = 3):
        """
        Initialize the AuthManager.

        Args:
            session_timeout: Session timeout in seconds. Defaults to 1800.
            max_attempts: Maximum login attempts before lockout. Defaults to 3.

        Raises:
            ValueError: If session_timeout is less than 60 seconds.

        Example:
            >>> auth = AuthManager(session_timeout=3600, max_attempts=5)
        """
        if session_timeout < 60:
            raise ValueError("Session timeout must be at least 60 seconds")

        self.session_timeout = session_timeout
        self.max_login_attempts = max_attempts
        self._sessions = {}

    def authenticate(self, username: str, password: str) -> User | None:
        """
        Authenticate a user with username and password.

        Args:
            username: The user's username or email address.
            password: The user's password.

        Returns:
            User object if authentication successful, None otherwise.

        Raises:
            AuthenticationError: If authentication fails due to invalid credentials.
            AccountLockedException: If account is locked due to too many failed attempts.

        Example:
            >>> auth = AuthManager()
            >>> user = auth.authenticate("john@example.com", "secret123")
            >>> if user:
            ...     print(f"Welcome, {user.name}!")
            ... else:
            ...     print("Authentication failed")
        """
        # Implementation here
        pass
```

### Automatic API Documentation

```yaml
# mkdocs.yml - mkdocstrings configuration
plugins:
  - mkdocstrings:
      handlers:
        python:
          options:
            # Show source code
            show_source: true

            # Docstring parsing
            docstring_style: google
            docstring_section_style: table

            # Member organization
            members_order: alphabetical
            group_by_category: true
            show_category_heading: true

            # Inheritance
            show_inheritance_diagram: true

            # Signatures
            show_signature_annotations: true
            separate_signature: true

            # Root handling
            show_root_heading: true
            show_root_toc_entry: false

            # Filtering
            filters:
              - "!^_"  # Exclude private members
              - "!^__"  # Exclude magic methods
```

### API Reference Pages

```markdown
<!-- docs/reference/api/auth.md -->
# Authentication API

::: myproject.auth
    options:
      show_root_heading: false
      show_root_toc_entry: false
      members:
        - AuthManager
        - User
        - Permission

## Usage Examples

### Basic Authentication

```python
from myproject.auth import AuthManager

# Initialize auth manager
auth = AuthManager()

# Authenticate user
user = auth.authenticate("user@example.com", "password")
if user:
    print(f"Welcome, {user.name}!")
```

### Session Management

```python
# Create session
session = auth.create_session(user)

# Check session validity
if auth.is_session_valid(session.token):
    print("Session is active")

# Logout
auth.logout(session.token)
```
```

## Content Guidelines

### Writing Style

- **Clear and Concise**: Use simple, direct language
- **Active Voice**: "Configure the provider" vs "The provider is configured"
- **Present Tense**: "The function returns" vs "The function will return"
- **Second Person**: "You can configure" vs "One can configure"

### Content Structure

#### Overview Pages

```markdown
# Project Name

Brief description of what the project does and its main benefits.

## Key Features

- **Feature 1**: Brief description
- **Feature 2**: Brief description
- **Feature 3**: Brief description

## Quick Start

```bash
# Installation
uv add project-name

# Basic usage
from project import MainClass
instance = MainClass()
result = instance.main_method()
```

## Use Cases

- **Use Case 1**: Description and link to guide
- **Use Case 2**: Description and link to guide

## Next Steps

<!-- - [Installation Guide](getting-started/installation/) -->
<!-- - [User Guide](guides/user-guide/) -->
- [API Reference](reference/api/)
```

#### Tutorial Structure

```markdown
# Tutorial: Building Your First Application

Learn how to build a complete application using our framework.

**What you'll learn:**
- How to set up a new project
- How to configure basic settings
- How to implement core functionality
- How to test your application

**Prerequisites:**
- Python 3.11 or higher
- Basic understanding of web development
- 30 minutes of time

## Step 1: Project Setup

First, create a new project directory:

```bash
mkdir my-application
cd my-application
```

Now initialize the project:

```bash
project-cli init --name="My Application"
```

This creates the following structure:
- `src/` - Source code
- `tests/` - Test files
- `docs/` - Documentation
- `pyproject.toml` - Project configuration

## Step 2: Configuration

[Continue with detailed steps...]

## What's Next?

Now that you've built your first application, try these next steps:
<!-- - [Advanced Tutorial](advanced-tutorial/) -->
<!-- - [Deployment Guide](../guides/deployment/) -->
- [API Reference](../reference/api/)
```

## Documentation Automation

### Auto-Generation Scripts

```python
# scripts/generate_docs.py
"""Generate documentation from code and templates."""

import ast
import inspect
from pathlib import Path
from typing import Any, Dict, List

class DocumentationGenerator:
    """Generate documentation from Python code."""

    def __init__(self, source_dir: Path, docs_dir: Path):
        self.source_dir = source_dir
        self.docs_dir = docs_dir

    def generate_api_docs(self):
        """Generate API documentation from source code."""
        api_dir = self.docs_dir / "reference" / "api"
        api_dir.mkdir(parents=True, exist_ok=True)

        for python_file in self.source_dir.rglob("*.py"):
            if python_file.name.startswith("_"):
                continue

            module_name = self._get_module_name(python_file)
            doc_file = api_dir / f"{module_name}.md"

            self._generate_module_doc(python_file, doc_file, module_name)

    def generate_cli_docs(self):
        """Generate CLI documentation from click commands."""
        cli_dir = self.docs_dir / "reference"
        cli_dir.mkdir(parents=True, exist_ok=True)

        # Generate CLI reference
        cli_doc = cli_dir / "cli.md"
        self._generate_cli_reference(cli_doc)

    def _generate_module_doc(self, python_file: Path, doc_file: Path, module_name: str):
        """Generate documentation for a Python module."""
        content = f"""# {module_name}

::: {module_name}
    options:
      show_root_heading: false
      members_order: source
      group_by_category: true

## Examples

[Add usage examples here]
"""
        doc_file.write_text(content)

    def _generate_cli_reference(self, doc_file: Path):
        """Generate CLI reference documentation."""
        # Use click's built-in help generation
        import click
        from myproject.cli import main

        ctx = click.Context(main)
        help_text = main.get_help(ctx)

        content = f"""# Command Line Interface

## Overview

{help_text}

## Commands

### Global Options

[Document global options]

### Commands

[Document each command with examples]
"""
        doc_file.write_text(content)

if __name__ == "__main__":
    generator = DocumentationGenerator(
        source_dir=Path("src"),
        docs_dir=Path("docs")
    )
    generator.generate_api_docs()
    generator.generate_cli_docs()
```

### Documentation Testing

```python
# scripts/test_docs.py
"""Test documentation for accuracy and completeness."""

import subprocess
from pathlib import Path

def test_code_examples():
    """Test all code examples in documentation."""
    docs_dir = Path("docs")

    for md_file in docs_dir.rglob("*.md"):
        print(f"Testing examples in {md_file}")

        # Extract code blocks
        content = md_file.read_text()
        code_blocks = extract_python_code_blocks(content)

        for i, code in enumerate(code_blocks):
            try:
                # Test syntax
                compile(code, f"{md_file}:block_{i}", "exec")
                print(f"  ✓ Block {i}: Syntax OK")

                # Optionally execute code
                if not has_external_dependencies(code):
                    exec(code)
                    print(f"  ✓ Block {i}: Execution OK")

            except Exception as e:
                print(f"  ✗ Block {i}: {e}")

def extract_python_code_blocks(content: str) -> List[str]:
    """Extract Python code blocks from Markdown."""
    import re

    pattern = r"```python\n(.*?)\n```"
    matches = re.findall(pattern, content, re.DOTALL)
    return matches

def has_external_dependencies(code: str) -> bool:
    """Check if code has external dependencies."""
    import_lines = [line.strip() for line in code.split('\n')
                   if line.strip().startswith(('import ', 'from '))]

    # List of safe imports for testing
    safe_imports = ['os', 'sys', 'json', 'datetime', 'pathlib']

    for line in import_lines:
        module = line.split()[1].split('.')[0]
        if module not in safe_imports:
            return True

    return False

def test_links():
    """Test all internal and external links."""
    docs_dir = Path("docs")

    for md_file in docs_dir.rglob("*.md"):
        content = md_file.read_text()

        # Extract markdown links
        import re
        links = re.findall(r'\[.*?\]\((.*?)\)', content)

        for link in links:
            if link.startswith('http'):
                # Test external link
                test_external_link(link)
            else:
                # Test internal link
                test_internal_link(md_file, link)

def test_external_link(url: str):
    """Test external link availability."""
    import requests

    try:
        response = requests.head(url, timeout=10)
        if response.status_code < 400:
            print(f"  ✓ {url}")
        else:
            print(f"  ✗ {url}: HTTP {response.status_code}")
    except Exception as e:
        print(f"  ✗ {url}: {e}")

def test_internal_link(source_file: Path, link: str):
    """Test internal link exists."""
    if link.startswith('#'):
        # Anchor link - would need to parse headers
        return

    # Resolve relative path
    target = source_file.parent / link
    target = target.resolve()

    if target.exists():
        print(f"  ✓ {link}")
    else:
        print(f"  ✗ {link}: File not found")

if __name__ == "__main__":
    test_code_examples()
    test_links()
```

## Publishing Documentation

### GitHub Pages

```yaml
# .github/workflows/docs.yml
name: Documentation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - uses: actions/setup-python@v4
      with:
        python-version: "3.11"

    - name: Install dependencies
      run: |
        uv tool install mkdocs
        uv tool install mkdocs-material
        uv tool install mkdocstrings[python]

    - name: Generate API docs
      run: python scripts/generate_docs.py

    - name: Test documentation
      run: python scripts/test_docs.py

    - name: Build documentation
      run: mkdocs build

    - name: Deploy to GitHub Pages
      if: github.ref == 'refs/heads/main'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./site
```

### Read the Docs

```yaml
# .readthedocs.yml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

python:
  install:
    - requirements: docs/requirements.txt
    - path: .

mkdocs:
  configuration: mkdocs.yml
```

### Versioned Documentation

```bash
# Install mike for versioning
uv tool install mike

# Deploy version
mike deploy --push --update-aliases 1.0 latest

# Set default version
mike set-default --push latest

# List versions
mike list
```

## Best Practices

### Content Organization

- **Hierarchical Structure**: Organize content from general to specific
- **Cross-References**: Link related content liberally
- **Search Optimization**: Use descriptive headings and keywords
- **Mobile-Friendly**: Ensure content works on all devices

### Maintenance

- **Regular Reviews**: Schedule periodic documentation reviews
- **Version Control**: Track documentation changes with code
- **Automated Testing**: Test code examples and links regularly
- **User Feedback**: Provide channels for documentation feedback

### Accessibility

- **Alt Text**: Provide alt text for images and diagrams
- **Semantic HTML**: Use proper heading hierarchy
- **Color Contrast**: Ensure sufficient color contrast
- **Keyboard Navigation**: Support keyboard-only navigation

## Integration with Development

### Documentation-Driven Development

1. **Write Documentation First**: Start with user stories and API design
2. **Code to Match**: Implement functionality to match documentation
3. **Keep in Sync**: Update documentation with code changes
4. **Review Together**: Review documentation and code changes together

### Documentation in CI/CD

```python
# pre-commit hook
#!/usr/bin/env python3
"""Pre-commit hook to validate documentation."""

import subprocess
import sys

def main():
    """Run documentation checks."""

    # Check for missing docstrings
    result = subprocess.run([
        "python", "scripts/check_docstrings.py"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("Documentation check failed:")
        print(result.stdout)
        return 1

    # Test code examples
    result = subprocess.run([
        "python", "scripts/test_docs.py"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("Documentation tests failed:")
        print(result.stdout)
        return 1

    print("Documentation checks passed ✓")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Related Documentation

- **[Installation Guide](installation.md)** - Setting up development environment
- **[Testing Guide](testing.md)** - Testing documentation and code
- **[Packaging Guide](packaging.md)** - Publishing documentation with packages
