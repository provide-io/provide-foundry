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

REM Check if mkdocs is available
mkdocs --version >nul 2>&1
if errorlevel 1 (
    echo ❌ MkDocs is required but not found
    echo Install with: pip install -r requirements.txt
    exit /b 1
)

REM Install Python dependencies if needed
if exist requirements.txt (
    echo 📦 Installing Python dependencies...
    pip install -r requirements.txt
)

REM Add missing dependency for docs_aggregator
echo 📦 Installing additional dependencies...
pip install watchdog pyyaml

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