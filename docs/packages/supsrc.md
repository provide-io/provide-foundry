# 🔼⚙️ supsrc

Automated Git commit/push utility based on filesystem events and rules.

## Overview

`supsrc` is an automated Git workflow tool that monitors filesystem events and automatically creates commits and pushes changes based on configurable rules. It's designed to streamline Git operations during development, reducing the friction of frequent commits while maintaining a clean commit history.

This tool is particularly useful for automated documentation updates, CI/CD workflows, and development environments where frequent commits are desired.

## Key Capabilities

- **Filesystem Monitoring**: Watch for file changes and trigger Git operations
- **Rule-Based Automation**: Configure rules for when to commit and what to include
- **Smart Commit Messages**: Generate contextual commit messages based on changes
- **Automatic Pushing**: Optionally push commits to remote repositories
- **Selective Inclusion**: Fine-grained control over which files trigger commits
- **Integration Ready**: Works with CI/CD pipelines and development workflows

## Installation

```bash
uv tool install supsrc
```

## Documentation

For configuration guides, rule syntax, and usage examples, see the [SupSrc documentation](https://foundry.provide.io/supsrc/).

## Repository

- **Repository**: [supsrc](https://github.com/provide-io/supsrc)
- **Package**: `supsrc` on PyPI
- **License**: Apache-2.0
