# Installation Guide

Complete installation guide for the Provide Foundry, covering all platforms and installation methods.

## Prerequisites

### System Requirements

- **Python 3.11 or higher**
- **Git** for version control
- **Internet connection** for downloading packages
- **4GB RAM minimum** (8GB recommended)
- **2GB free disk space**

### Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| macOS (Intel) | ✅ Full Support | Recommended |
| macOS (Apple Silicon) | ✅ Full Support | Recommended |
| Linux (x86_64) | ✅ Full Support | Ubuntu 20.04+, CentOS 8+ |
| Windows 11 | ✅ Full Support | WSL2 recommended |
| Windows 10 | ⚠️ Limited Support | WSL2 required |

## Quick Installation

### Option 1: Complete Foundry (Recommended)

Install the entire foundry as a unified workspace:

```bash
# Clone the foundry repository
git clone https://github.com/provide-io/provide-io.git
cd provide-io

# Set up the unified development environment
uv sync --extra all --extra dev
source .venv/bin/activate

# Verify installation
python -c "import provide, pyvider; print('✅ Foundry ready!')"
```

This installs all 13 foundry packages in editable mode with proper dependency resolution.

### Option 2: Individual Packages

Install specific packages as needed:

```bash
# Core packages
pip install provide-foundation provide-testkit

# Framework packages
pip install pyvider pyvider-cty pyvider-hcl

# Tool packages
pip install wrknv flavorpack
```

## Detailed Installation

### Step 1: Install UV Package Manager

UV is the recommended package manager for the Provide Foundry:

=== "macOS"

    ```bash
    # Using Homebrew (recommended)
    brew install uv

    # Or using curl
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "Linux"

    ```bash
    # Using curl
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Or using pip
    pip install uv
    ```

=== "Windows"

    ```powershell
    # Using PowerShell
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

    # Or using pip
    pip install uv
    ```

### Step 2: Python Version Management

Ensure you have Python 3.11 or higher:

=== "Using pyenv (Recommended)"

    ```bash
    # Install pyenv if not present
    curl https://pyenv.run | bash

    # Install Python 3.11
    pyenv install 3.11.8
    pyenv global 3.11.8

    # Verify version
    python --version  # Should show 3.11.8
    ```

=== "Using UV"

    ```bash
    # UV can manage Python versions
    uv python install 3.11.8
    uv python pin 3.11.8
    ```

=== "System Package Manager"

    ```bash
    # Ubuntu/Debian
    sudo apt update
    sudo apt install python3.11 python3.11-venv python3.11-dev

    # CentOS/RHEL
    sudo dnf install python3.11 python3.11-venv python3.11-devel

    # macOS (Homebrew)
    brew install python@3.11
    ```

### Step 3: Clone and Set Up Foundry

```bash
# Clone the repository
git clone https://github.com/provide-io/provide-io.git
cd provide-io

# Verify structure
ls -la
# Should show all package directories: provide-foundation, pyvider, wrknv, etc.

# Set up unified development environment
uv sync --extra all --extra dev

# Activate environment
source .venv/bin/activate

# Verify all packages are installed
uv pip list | grep -E "(provide|pyvider|wrknv|flavorpack)"
```

### Step 4: Verification

Run comprehensive verification tests:

```bash
# Test core imports
python -c "
import provide.foundation
import provide.testkit
import pyvider
import pyvider.cty
import pyvider.hcl
print('✅ All core packages imported successfully')
"

# Test tool availability
wrknv --version
flavor --version

# Run quick test suite
python -m pytest tests/integration/test_installation.py -v
```

## Installation Methods

### Method 1: Development Installation

For active development on foundry packages:

```bash
git clone https://github.com/provide-io/provide-io.git
cd provide-io

# Development installation with all extras
uv sync --extra all --extra dev --extra testing

# Install pre-commit hooks
pre-commit install

# Verify development setup
make test-all  # If Makefile is present
# or
python -m pytest tests/ -x
```

### Method 2: User Installation

For using foundry packages in your projects:

```bash
# Install specific packages
pip install provide-foundation[all]
pip install pyvider[all]
pip install wrknv flavorpack

# Or install everything
pip install \
  provide-foundation[all] \
  provide-testkit[all] \
  pyvider[all] \
  pyvider-cty \
  pyvider-hcl \
  wrknv \
  flavorpack
```

### Method 3: Container Installation

Use Docker for isolated environments:

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Clone and install foundry
RUN git clone https://github.com/provide-io/provide-io.git /workspace
WORKDIR /workspace
RUN uv sync --extra all

# Set up environment
ENV VIRTUAL_ENV=/workspace/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

CMD ["bash"]
```

```bash
# Build and run container
docker build -t provide-foundry .
docker run -it --rm -v $(pwd):/app provide-foundry
```

## Platform-Specific Setup

### macOS

```bash
# Install Xcode command line tools
xcode-select --install

# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install git python@3.11 uv

# Clone and setup
git clone https://github.com/provide-io/provide-io.git
cd provide-io
uv sync --extra all --extra dev
source .venv/bin/activate
```

### Linux (Ubuntu/Debian)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    git \
    curl \
    build-essential \
    pkg-config \
    libffi-dev \
    libssl-dev

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Clone and setup
git clone https://github.com/provide-io/provide-io.git
cd provide-io
uv sync --extra all --extra dev
source .venv/bin/activate
```

### Windows (WSL2)

```bash
# Enable WSL2 (run in PowerShell as Administrator)
wsl --install

# In WSL2 Ubuntu
sudo apt update
sudo apt install -y python3.11 python3.11-venv git curl build-essential

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Clone and setup
git clone https://github.com/provide-io/provide-io.git
cd provide-io
uv sync --extra all --extra dev
source .venv/bin/activate
```

## Environment Configuration

### Shell Integration

Add foundry tools to your shell:

=== "Bash"

    ```bash
    # Add to ~/.bashrc
    export PATH="$HOME/.local/bin:$PATH"

    # Optional: Auto-activate when entering foundry projects
    cd() {
        builtin cd "$@"
        if [[ -f "pyproject.toml" && -f ".venv/bin/activate" ]]; then
            source .venv/bin/activate
        fi
    }
    ```

=== "Zsh"

    ```zsh
    # Add to ~/.zshrc
    export PATH="$HOME/.local/bin:$PATH"

    # Optional: Auto-activation
    chpwd() {
        if [[ -f "pyproject.toml" && -f ".venv/bin/activate" ]]; then
            source .venv/bin/activate
        fi
    }
    ```

=== "Fish"

    ```fish
    # Add to ~/.config/fish/config.fish
    set -gx PATH $HOME/.local/bin $PATH

    # Optional: Auto-activation
    function __auto_activate --on-variable PWD
        if test -f pyproject.toml -a -f .venv/bin/activate
            source .venv/bin/activate
        end
    end
    ```

### IDE Configuration

#### VS Code

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".venv": false
    }
}
```

#### PyCharm

1. Open the provide-io directory as project
2. Go to Settings → Project → Python Interpreter
3. Select "Existing environment"
4. Choose `.venv/bin/python`
5. Enable pytest as test runner

## Troubleshooting

### Common Issues

#### Python Version Issues

```bash
# Check Python version
python --version

# If wrong version, use pyenv
pyenv install 3.11.8
pyenv local 3.11.8

# Or specify python3.11 explicitly
python3.11 -m venv .venv
```

#### UV Installation Issues

```bash
# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH manually
export PATH="$HOME/.cargo/bin:$PATH"

# Verify installation
uv --version
```

#### Permission Issues

```bash
# Fix permission issues on macOS/Linux
sudo chown -R $(whoami) /usr/local/lib/python3.11/site-packages

# Or use user installation
pip install --user package-name
```

#### Network Issues

```bash
# Configure proxy if needed
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# Use different index URL
pip install --index-url https://pypi.org/simple/ package-name
```

### Verification Commands

```bash
# Verify Python environment
python -c "import sys; print(f'Python {sys.version}')"
python -c "import site; print(f'Site packages: {site.getsitepackages()}')"

# Verify foundry packages
python -c "
packages = ['provide.foundation', 'provide.testkit', 'pyvider', 'pyvider.cty', 'pyvider.hcl']
for pkg in packages:
    try:
        __import__(pkg)
        print(f'✅ {pkg}')
    except ImportError as e:
        print(f'❌ {pkg}: {e}')
"

# Verify tools
which uv && echo "✅ UV installed" || echo "❌ UV missing"
which wrknv && echo "✅ wrknv installed" || echo "❌ wrknv missing"
which flavor && echo "✅ flavorpack installed" || echo "❌ flavorpack missing"
```

### Getting Help

If you encounter issues:

1. **Check the logs** - Look for error messages in terminal output
2. **Search issues** - Check [GitHub Issues](https://github.com/provide-io/provide-io/issues)
3. **Ask for help** - Create a new issue with:
   - Your platform and Python version
   - Complete error messages
   - Steps to reproduce
4. **Community support** - Join discussions in GitHub Discussions

## Next Steps

After successful installation:

1. **[Development Setup](development.md)** - Configure your development environment
2. **[Provider Development](provider-development.md)** - Build your first provider
3. **[Testing Guide](testing.md)** - Learn testing best practices

---

You now have the complete Provide Foundry installed and ready for development!