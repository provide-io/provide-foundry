# plating

Documentation and code generation templates for consistent project scaffolding and documentation automation across the provide.foundation ecosystem.

## Overview

`plating` is the template engine and project scaffolding system for the provide.foundation ecosystem. It provides powerful templating capabilities for code generation, documentation automation, and consistent project structure creation across multiple programming languages.

### Key Features

#### 🎨 **Template Engine**
- **Powerful templating**: Advanced templating system with Jinja2-based syntax
- **Variable substitution**: Dynamic content generation with context variables
- **Conditional logic**: Template branching and conditional content generation
- **Template inheritance**: Reusable base templates with extension capabilities

#### 🏗️ **Project Scaffolding**
- **Automated project creation**: Generate complete project structures from templates
- **Multi-language support**: Templates for Python, Go, TypeScript, Rust, and more
- **Customizable structures**: Flexible project layouts and organization patterns
- **Configuration-driven**: Template behavior controlled by configuration files

#### 📚 **Documentation Generation**
- **Consistent patterns**: Standardized documentation structures across projects
- **API documentation**: Automated API documentation generation
- **Multi-format support**: Generate documentation in multiple formats (Markdown, HTML, etc.)
- **Cross-references**: Automatic linking and cross-referencing between documents

#### 🔧 **Integration Tools**
- **CI/CD templates**: Pre-configured GitHub Actions, GitLab CI, and other pipeline templates
- **Development workflows**: Standardized development environment setup
- **Build system integration**: Templates for various build systems and package managers
- **Quality tools**: Pre-configured linting, testing, and code quality tools

## Installation

```bash
# Basic installation
uv add plating

# With all extras for full functionality
uv add plating[all]

# Development installation
uv add plating[dev]
```

## Quick Start

### Basic Template Usage

```python
from plating import Template, Generator

# Load a template
template = Template.load("python-package")

# Generate project structure
generator = Generator(template)
generator.create_project("my-new-project", {
    "package_name": "my_package",
    "author": "Your Name",
    "description": "A new Python package",
    "license": "MIT"
})
```

### Custom Template Creation

```python
from plating import Template, TemplateFile

# Create a custom template
template = Template(
    name="custom-api",
    description="Custom API service template"
)

# Add template files
template.add_file(TemplateFile(
    path="src/{{package_name}}/main.py",
    content="""
from fastapi import FastAPI

app = FastAPI(title="{{title}}")

@app.get("/")
async def root():
    return {"message": "Hello from {{package_name}}"}
"""))

# Generate from custom template
generator = Generator(template)
generator.create_project("my-api", {
    "package_name": "my_api",
    "title": "My API Service"
})
```

### Documentation Templates

```python
from plating.docs import DocumentationGenerator

# Generate documentation structure
doc_gen = DocumentationGenerator()
doc_gen.create_docs_structure("./docs", {
    "project_name": "My Project",
    "api_modules": ["auth", "users", "products"],
    "guide_sections": ["getting-started", "tutorials", "advanced"]
})
```

## Template Types

### **Project Templates**
- **Python packages**: Complete Python package structure with setup.py, pyproject.toml
- **FastAPI services**: Web API services with FastAPI framework
- **CLI applications**: Command-line interface applications
- **Library templates**: Reusable library structures

### **Documentation Templates**
- **README generators**: Comprehensive README.md templates
- **API documentation**: OpenAPI/Swagger documentation templates
- **User guides**: Tutorial and guide documentation structures
- **Reference docs**: API reference documentation templates

### **Configuration Templates**
- **CI/CD pipelines**: GitHub Actions, GitLab CI, Jenkins pipelines
- **Docker configurations**: Dockerfile and docker-compose templates
- **Development environments**: VS Code, PyCharm configuration templates
- **Quality tools**: Pre-commit hooks, linting, testing configurations

## Advanced Features

### Template Inheritance

```python
# Base template
base_template = Template.load("python-base")

# Extended template
web_template = Template.extend(base_template, "python-web")
web_template.add_dependencies(["fastapi", "uvicorn"])
web_template.add_files_from_directory("web-templates/")
```

### Dynamic Content Generation

```python
from plating.generators import APIGenerator

# Generate API documentation from code
api_gen = APIGenerator()
api_docs = api_gen.generate_from_module("my_package.api")

# Include in template
template.add_dynamic_content("api-docs", api_docs)
```

### Template Composition

```python
# Compose multiple templates
composed = Template.compose([
    "python-base",
    "fastapi-web",
    "docker-deployment",
    "github-actions"
])
```

## Use Cases

### **Project Bootstrapping**
Rapidly create new projects with consistent structure and best practices across the provide.foundation ecosystem.

### **Documentation Automation**
Generate and maintain consistent documentation across multiple projects and repositories.

### **CI/CD Standardization**
Ensure consistent build, test, and deployment pipelines across all projects.

### **Code Generation**
Generate boilerplate code, API clients, and service stubs from specifications.

## Integration with Foundation

Plating integrates seamlessly with other provide.foundation tools:

- **provide-foundation**: Uses Foundation's configuration and logging systems
- **pyvider**: Templates for Terraform provider development
- **tofusoup**: Test generation templates for conformance testing
- **wrknv**: Development environment templates

## Related Documentation

- **[API Reference](../plating/reference/)** - Complete API documentation
<!-- - **[Template Gallery](../guides/template-gallery.md)** --> - Available templates and examples
<!-- - **[Custom Templates](../guides/custom-templates.md)** --> - Creating your own templates

## Repository

- **Repository**: [plating](https://github.com/provide-io/plating)
- **Package**: `plating` on PyPI
- **License**: MIT