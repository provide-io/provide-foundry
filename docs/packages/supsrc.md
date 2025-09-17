# supsrc

Automated Git workflow and commit management for intelligent source code operations in the provide.foundation ecosystem.

## Overview

`supsrc` is an intelligent Git workflow automation tool that enhances developer productivity through AI-powered commit message generation, automated branch management, and smart code analysis. It provides a rich terminal interface for interactive Git operations while maintaining compatibility with existing Git workflows.

### Key Features

#### 🧠 **Intelligent Commits**
- **AI-powered commit messages**: Generate descriptive, conventional commit messages from code changes
- **Context-aware analysis**: Understand code changes and their impact on the codebase
- **Commit optimization**: Suggest optimal commit boundaries and message formats
- **Convention compliance**: Follow conventional commit formats and project standards

#### 🔄 **Workflow Automation**
- **Automated Git workflows**: Streamline common Git operations and patterns
- **Branch management**: Intelligent branch creation, merging, and cleanup
- **Release automation**: Automated versioning and release preparation
- **Conflict resolution**: Smart merge conflict detection and resolution assistance

#### 📊 **Code Analysis**
- **Smart change analysis**: Analyze code changes for impact and significance
- **Dependency tracking**: Understand how changes affect other parts of the codebase
- **Quality assessment**: Evaluate code quality and suggest improvements
- **Risk analysis**: Identify potentially risky changes and suggest caution

#### 🔗 **Integration Tools**
- **CI/CD integration**: Seamless integration with continuous integration pipelines
- **Development tools**: Integration with popular IDEs and development environments
- **Issue tracking**: Connect commits to issue trackers and project management tools
- **Code review**: Enhanced code review workflows with automated insights

#### 📈 **History Management**
- **Advanced Git history**: Sophisticated Git history analysis and visualization
- **Change tracking**: Track code evolution and development patterns
- **Author analytics**: Analyze contribution patterns and code ownership
- **Repository insights**: Generate insights about repository health and activity

#### 🖥️ **Terminal UI**
- **Rich terminal interface**: Beautiful, interactive terminal user interface
- **Command palette**: Quick access to all Git operations and tools
- **Visual diff viewer**: Enhanced diff viewing with syntax highlighting
- **Interactive workflows**: Step-by-step guidance through complex Git operations

## Installation

```bash
# Basic installation
uv add supsrc

# With all extras for full functionality
uv add supsrc[all]

# Development installation
uv add supsrc[dev]
```

## Quick Start

### Basic Git Operations

```python
from supsrc import GitManager, CommitAnalyzer

# Analyze and create intelligent commits
git = GitManager()
analyzer = CommitAnalyzer()

# Generate smart commit messages
changes = git.get_staged_changes()
message = analyzer.generate_message(changes)
git.commit(message)
```

### Automated Workflows

```python
from supsrc import WorkflowManager

# Create a feature branch workflow
workflow = WorkflowManager()
workflow.create_feature_branch("add-user-authentication")
workflow.auto_commit_changes("Implement user authentication system")
workflow.create_pull_request(
    title="Add user authentication",
    description="Implements JWT-based authentication with role-based access control"
)
```

### Code Analysis

```python
from supsrc import CodeAnalyzer

# Analyze code changes
analyzer = CodeAnalyzer()
changes = analyzer.analyze_staged_changes()

print(f"Changed files: {len(changes.files)}")
print(f"Lines added: {changes.lines_added}")
print(f"Lines removed: {changes.lines_removed}")
print(f"Complexity change: {changes.complexity_delta}")
print(f"Risk level: {changes.risk_level}")
```

### Terminal UI

```bash
# Launch interactive terminal UI
supsrc tui

# Quick commit with AI-generated message
supsrc commit --auto

# Create feature branch with workflow
supsrc feature start user-profile-page

# Analyze repository health
supsrc analyze --full
```

## Advanced Features

### Custom Commit Templates

```python
from supsrc import CommitTemplate

# Create custom commit template
template = CommitTemplate()
template.set_format("conventional")
template.add_scope_detection(True)
template.add_breaking_change_detection(True)

# Use template for commits
analyzer = CommitAnalyzer(template=template)
message = analyzer.generate_message(changes)
```

### Workflow Automation

```python
from supsrc import Workflow, WorkflowStep

# Define custom workflow
workflow = Workflow("feature-development")
workflow.add_step(WorkflowStep.CREATE_BRANCH)
workflow.add_step(WorkflowStep.RUN_TESTS)
workflow.add_step(WorkflowStep.LINT_CODE)
workflow.add_step(WorkflowStep.COMMIT_CHANGES)
workflow.add_step(WorkflowStep.PUSH_BRANCH)
workflow.add_step(WorkflowStep.CREATE_PR)

# Execute workflow
result = workflow.execute()
```

### Integration with CI/CD

```python
from supsrc import CIIntegration

# Generate CI configuration
ci = CIIntegration()
ci.generate_github_actions({
    "test_on_pr": True,
    "auto_merge": True,
    "require_conventional_commits": True
})
```

### Repository Analytics

```python
from supsrc import RepositoryAnalyzer

# Analyze repository health
analyzer = RepositoryAnalyzer()
report = analyzer.generate_health_report()

print(f"Commit frequency: {report.commit_frequency}")
print(f"Test coverage trend: {report.coverage_trend}")
print(f"Code quality score: {report.quality_score}")
print(f"Technical debt: {report.technical_debt}")
```

## Use Cases

### **Enhanced Developer Experience**
Streamline Git workflows with intelligent automation and rich terminal interfaces.

### **Team Collaboration**
Improve team collaboration with consistent commit messages and automated workflows.

### **Code Quality**
Maintain high code quality through automated analysis and quality gates.

### **Release Management**
Automate release processes with intelligent versioning and changelog generation.

### **Repository Maintenance**
Keep repositories healthy with automated cleanup and maintenance tasks.

## Integration with Foundation

SupSrc integrates seamlessly with other provide.foundation tools:

- **provide-foundation**: Uses Foundation's configuration and logging systems
- **plating**: Templates for Git workflow configurations
- **tofusoup**: Automated testing integration in Git workflows
- **wrknv**: Development environment integration

## Configuration

### Global Configuration

```yaml
# ~/.supsrc/config.yaml
commit:
  format: conventional
  auto_generate: true
  require_scope: true

workflow:
  default_branch: main
  auto_push: false
  create_pr: true

analysis:
  enable_ai: true
  risk_threshold: medium
  complexity_warning: true
```

### Repository Configuration

```yaml
# .supsrc.yaml
project:
  name: my-project
  type: python-package

commit:
  scopes: [api, ui, tests, docs, ci]
  breaking_change_prefixes: ["BREAKING", "!"]

workflow:
  feature_branch_prefix: feature/
  hotfix_branch_prefix: hotfix/
  release_branch_prefix: release/
```

## Command Line Interface

```bash
# Intelligent commits
supsrc commit --auto
supsrc commit --interactive

# Branch management
supsrc branch create feature/new-feature
supsrc branch cleanup
supsrc branch merge --auto

# Repository analysis
supsrc analyze --changes
supsrc analyze --health
supsrc analyze --contributors

# Workflow management
supsrc workflow run feature-development
supsrc workflow create custom-workflow

# Interactive UI
supsrc tui
supsrc tui --repo /path/to/repo
```

## Related Documentation

- **[API Reference](../api/supsrc.md)** - Complete API documentation
- **[Workflow Guide](../guides/git-workflows.md)** - Git workflow best practices
- **[Configuration](../guides/supsrc-config.md)** - Configuration options and examples

## Repository

- **Repository**: [supsrc](https://github.com/provide-io/supsrc)
- **Package**: `supsrc` on PyPI
- **License**: MIT