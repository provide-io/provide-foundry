#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# Documentation validation wrapper script for provide.io ecosystem
#
# This script runs all documentation validation checks and optionally
# validates mkdocs builds for specified projects.
#
# Usage:
#   ./scripts/validate_docs.sh              # Run all validation checks
#   ./scripts/validate_docs.sh pyvider wrknv  # Also build specified projects

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FOUNDRY_DIR="$(dirname "$SCRIPT_DIR")"
ECOSYSTEM_ROOT="$(dirname "$FOUNDRY_DIR")"

# Track overall status
OVERALL_STATUS=0

# Function to print colored output
print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Run validation command
run_validation() {
    local command=$1
    local description=$2

    print_header "$description"

    if python3 "$SCRIPT_DIR/docs_validate.py" "$command"; then
        print_success "$description passed"
        echo
        return 0
    else
        print_error "$description failed"
        echo
        OVERALL_STATUS=1
        return 1
    fi
}

# Main validation sequence
main() {
    echo
    print_header "📚 Documentation Validation Suite"
    echo "Running comprehensive documentation checks..."
    echo

    # Step 1: Verify configuration
    run_validation "verify-config" "Configuration Validation"

    # Step 2: Check structure
    run_validation "check-structure" "Structure Validation"

    # Step 3: Verify links
    run_validation "verify-links" "Link Validation"

    # Step 4: Build validation for specified projects
    if [ $# -gt 0 ]; then
        print_header "Build Validation"
        echo "Building documentation for specified projects..."
        echo

        for project in "$@"; do
            project_path="$ECOSYSTEM_ROOT/$project"

            if [ ! -d "$project_path" ]; then
                print_warning "Project not found: $project (skipping)"
                continue
            fi

            if [ ! -f "$project_path/mkdocs.yml" ]; then
                print_warning "No mkdocs.yml in $project (skipping)"
                continue
            fi

            echo -e "${BLUE}Building $project...${NC}"

            if (cd "$project_path" && mkdocs build --strict 2>&1 | grep -v "INFO"); then
                print_success "$project build passed"
                echo
            else
                print_error "$project build failed"
                echo
                OVERALL_STATUS=1
            fi
        done
    fi

    # Final summary
    print_header "Summary"

    if [ $OVERALL_STATUS -eq 0 ]; then
        print_success "All validation checks passed! 🎉"
        echo
        echo "Your documentation is in great shape."
        if [ $# -eq 0 ]; then
            echo
            echo "Tip: You can also validate specific project builds:"
            echo "  $0 pyvider wrknv flavorpack"
        fi
    else
        print_error "Some validation checks failed"
        echo
        echo "Please fix the errors above before continuing."
        echo "Run individual checks for more details:"
        echo "  python scripts/docs_validate.py verify-config"
        echo "  python scripts/docs_validate.py check-structure"
        echo "  python scripts/docs_validate.py verify-links"
    fi

    echo
    exit $OVERALL_STATUS
}

# Run main with all arguments
main "$@"
