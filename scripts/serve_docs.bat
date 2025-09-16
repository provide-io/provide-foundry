@echo off
REM
REM Serve Aggregated Documentation for Provide Foundry (Windows)
REM
REM This script collects documentation from all provide.io projects
REM and serves a unified documentation site locally for development.

setlocal enabledelayedexpansion

echo 🚀 Serving Provide Foundry Documentation
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

REM Serve the documentation
echo 🌐 Starting development server...
echo 📖 Documentation will be available at: http://localhost:8000
echo 💡 The server will automatically rebuild when files change
echo 🛑 Press Ctrl+C to stop the server
echo.

REM Start the server (this will block)
mkdocs serve