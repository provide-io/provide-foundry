@echo off
REM
REM Build Aggregated Documentation for Provide Foundry (Windows)
REM
REM This script collects documentation from all provide.io projects
REM and builds a unified documentation site.

setlocal enabledelayedexpansion

echo 🏗️ Building Provide Foundry Documentation
echo Foundry root: %~dp0..

REM Change to foundry root
cd /d "%~dp0.."

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not found
    exit /b 1
)

REM Check if uv is available
uv --version >nul 2>&1
if errorlevel 1 (
    echo ❌ uv is required but not found
    echo Install with: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    exit /b 1
)

REM Check if mkdocs is available
mkdocs --version >nul 2>&1
if errorlevel 1 (
    echo ❌ MkDocs is required but not found
    echo Install with: uv sync
    exit /b 1
)

REM Install Python dependencies if needed
if exist pyproject.toml (
    echo 📦 Installing Python dependencies...
    uv sync
)

REM Collect documentation from all projects
echo 📋 Collecting documentation from all projects...
python scripts\docs_aggregator.py collect
if errorlevel 1 (
    echo ⚠️ Some projects may not be available - continuing with available docs
)

REM Build the documentation
echo 🔨 Building documentation site...
mkdocs build
if errorlevel 1 (
    echo ❌ Documentation build failed
    exit /b 1
)

echo ✅ Documentation built successfully!
echo Output directory: %~dp0..\site
echo 🎉 Build complete!
echo To serve locally, run: scripts\serve_docs.bat