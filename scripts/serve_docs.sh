#!/bin/bash
#
# Serve Aggregated Documentation for Provide Foundry
#
# This script collects documentation from all provide.io projects
# and serves a unified documentation site locally for development.

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FOUNDRY_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}🚀 Serving Provide Foundry Documentation${NC}"
echo "Foundry root: $FOUNDRY_ROOT"

# Change to foundry root
cd "$FOUNDRY_ROOT"

# Check if Python and required packages are available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not found${NC}"
    exit 1
fi

# Check if mkdocs is available
if ! command -v mkdocs &> /dev/null; then
    echo -e "${RED}❌ MkDocs is required but not found${NC}"
    echo "Install with: pip install -r requirements.txt"
    exit 1
fi

# Install Python dependencies if needed
if [ -f "requirements.txt" ]; then
    echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
    pip install -r requirements.txt
fi

# Add missing dependency for docs_aggregator
echo -e "${BLUE}📦 Installing additional dependencies...${NC}"
pip install watchdog pyyaml

# Collect documentation from all projects
echo -e "${BLUE}📋 Collecting documentation from all projects...${NC}"
if ! python3 scripts/docs_aggregator.py collect; then
    echo -e "${YELLOW}⚠️ Some projects may not be available - continuing with available docs${NC}"
fi

# Serve the documentation
echo -e "${BLUE}🌐 Starting development server...${NC}"
echo -e "${GREEN}📖 Documentation will be available at: http://localhost:8000${NC}"
echo -e "${YELLOW}💡 The server will automatically rebuild when files change${NC}"
echo -e "${YELLOW}🛑 Press Ctrl+C to stop the server${NC}"
echo ""

# Start the server (this will block)
mkdocs serve