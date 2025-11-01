# Provide Foundry Documentation Makefile
# Comprehensive build system for federated documentation

# ==================== Configuration ====================

# Directories
FOUNDRY_ROOT := $(shell pwd)
DOCS_SOURCE := docs
DOCS_AGGREGATED := .docs_aggregated
DOCS_OUTPUT := site
SCRIPTS_DIR := scripts

# Python configuration
PYTHON := python3
UV := uv
MKDOCS := mkdocs

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m

# Platform detection
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    PLATFORM := darwin
else ifeq ($(UNAME_S),Linux)
    PLATFORM := linux
else
    PLATFORM := windows
endif

# Projects to aggregate (from docs_manifest.yaml)
PROJECTS := foundation testkit flavorpack pyvider pyvider-cty pyvider-hcl pyvider-rpcplugin wrknv

# Cache configuration
CACHE_HOME := $(or $(XDG_CACHE_HOME),$(HOME)/.cache)
FLAVOR_CACHE := $(CACHE_HOME)/flavor
UV_CACHE := $(CACHE_HOME)/uv
DAYS_OLD := 30

# ==================== Main Targets ====================

.PHONY: help
help: ## Show this help message
	@echo "$(BLUE)Provide Foundry Documentation Build System$(NC)"
	@echo "==========================================="
	@echo ""
	@echo "$(GREEN)Main Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep -E "^(docs-|help)" | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Development Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep -E "^(dev-|test-)" | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Cache & Cleanup Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep -E "^(cache-|clean-|pristine)" | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Utility Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep -v -E "^(docs-|dev-|test-|help|cache-|clean-|pristine)" | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

# ==================== Documentation Targets ====================

.PHONY: docs-build
docs-build: ## Build aggregated documentation (using mkdocs-monorepo)
	@echo "$(BLUE)🏗️ Building aggregated documentation...$(NC)"
	@$(MAKE) check-deps
	@$(MKDOCS) build --clean
	@echo "$(GREEN)✅ Documentation built successfully!$(NC)"
	@echo "$(BLUE)ℹ️  mkdocs-monorepo plugin handles aggregation automatically$(NC)"
	@echo "Output: $(FOUNDRY_ROOT)/$(DOCS_OUTPUT)"

.PHONY: docs-serve
docs-serve: ## Serve documentation locally for development (using mkdocs-monorepo)
	@echo "$(BLUE)🚀 Starting documentation development server...$(NC)"
	@$(MAKE) check-deps
	@echo "$(GREEN)📖 Documentation available at: http://localhost:8000$(NC)"
	@echo "$(BLUE)ℹ️  mkdocs-monorepo plugin handles aggregation automatically$(NC)"
	@echo "$(YELLOW)🛑 Press Ctrl+C to stop the server$(NC)"
	@$(MKDOCS) serve

.PHONY: docs-clean
docs-clean: ## Clean all documentation artifacts
	@echo "$(BLUE)🧹 Cleaning documentation artifacts...$(NC)"
	@rm -rf $(DOCS_OUTPUT)
	@echo "$(GREEN)✅ Documentation artifacts cleaned$(NC)"

.PHONY: docs-watch
docs-watch: ## Watch and rebuild docs automatically (development)
	@echo "$(BLUE)👀 Starting documentation watch mode...$(NC)"
	@$(MAKE) check-deps
	@$(PYTHON) $(SCRIPTS_DIR)/docs_aggregator.py watch

.PHONY: docs-validate
docs-validate: ## Validate documentation structure and links
	@echo "$(BLUE)🔍 Validating documentation...$(NC)"
	@$(MAKE) check-deps
	@$(MAKE) docs-collect
	@$(MKDOCS) build --strict
	@echo "$(GREEN)✅ Documentation validation passed$(NC)"

# ==================== Individual Project Documentation ====================

.PHONY: docs-foundation
docs-foundation: ## Build only Foundation documentation
	@echo "$(BLUE)📦 Building Foundation documentation...$(NC)"
	@cd ../provide-foundation && $(MKDOCS) build

.PHONY: docs-flavorpack
docs-flavorpack: ## Build only FlavorPack documentation
	@echo "$(BLUE)📦 Building FlavorPack documentation...$(NC)"
	@cd ../flavorpack && $(MKDOCS) build

.PHONY: docs-pyvider
docs-pyvider: ## Build only PyVider documentation
	@echo "$(BLUE)📦 Building PyVider documentation...$(NC)"
	@cd ../pyvider && $(MKDOCS) build

.PHONY: docs-testkit
docs-testkit: ## Build only TestKit documentation
	@echo "$(BLUE)📦 Building TestKit documentation...$(NC)"
	@cd ../provide-testkit && $(MKDOCS) build

# ==================== Development Targets ====================

.PHONY: dev-install
dev-install: ## Install documentation dependencies
	@echo "$(BLUE)📦 Installing documentation dependencies...$(NC)"
	@$(UV) sync
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

.PHONY: dev-update
dev-update: ## Update all project documentation
	@echo "$(BLUE)🔄 Updating project documentation...$(NC)"
	@for project in $(PROJECTS); do \
		if [ -d "../$$project" ]; then \
			echo "$(YELLOW)📝 Updating $$project documentation...$(NC)"; \
			cd "../$$project" && git pull origin main 2>/dev/null || git pull origin develop 2>/dev/null || echo "Could not update $$project"; \
			cd "$(FOUNDRY_ROOT)"; \
		fi; \
	done
	@echo "$(GREEN)✅ Documentation updates complete$(NC)"

.PHONY: dev-status
dev-status: ## Show status of all projects
	@echo "$(BLUE)📊 Project Status:$(NC)"
	@for project in $(PROJECTS); do \
		if [ -d "../$$project" ]; then \
			echo "$(GREEN)✅ $$project$(NC) - Available"; \
		else \
			echo "$(RED)❌ $$project$(NC) - Missing"; \
		fi; \
	done

# ==================== Testing Targets ====================

.PHONY: test-build
test-build: ## Test documentation build without serving
	@echo "$(BLUE)🧪 Testing documentation build...$(NC)"
	@$(MAKE) docs-clean
	@$(MAKE) docs-build
	@echo "$(GREEN)✅ Build test passed$(NC)"

.PHONY: test-links
test-links: ## Test for broken links in documentation
	@echo "$(BLUE)🔗 Testing documentation links...$(NC)"
	@$(MAKE) docs-build
	@if command -v linkchecker >/dev/null 2>&1; then \
		linkchecker $(DOCS_OUTPUT)/index.html; \
	else \
		echo "$(YELLOW)⚠️ linkchecker not installed, skipping link validation$(NC)"; \
		echo "Install with: uv add linkchecker"; \
	fi

.PHONY: test-projects
test-projects: ## Test individual project documentation builds
	@echo "$(BLUE)🧪 Testing individual project builds...$(NC)"
	@for project in foundation flavorpack pyvider testkit; do \
		echo "$(YELLOW)Testing $$project...$(NC)"; \
		$(MAKE) docs-$$project || exit 1; \
	done
	@echo "$(GREEN)✅ All project tests passed$(NC)"

# ==================== Deployment Targets ====================

.PHONY: deploy-github
deploy-github: ## Deploy to GitHub Pages
	@echo "$(BLUE)🚀 Deploying to GitHub Pages...$(NC)"
	@$(MAKE) docs-build
	@if command -v mike >/dev/null 2>&1; then \
		mike deploy --push --update-aliases latest main; \
		echo "$(GREEN)✅ Deployed to GitHub Pages$(NC)"; \
	else \
		echo "$(RED)❌ mike not installed. Install with: uv sync$(NC)"; \
		exit 1; \
	fi

.PHONY: deploy-test
deploy-test: ## Test deployment build
	@echo "$(BLUE)🧪 Testing deployment build...$(NC)"
	@$(MAKE) docs-clean
	@$(MAKE) docs-validate
	@echo "$(GREEN)✅ Deployment test passed$(NC)"

# ==================== Utility Targets ====================

.PHONY: check-deps
check-deps: ## Check if required dependencies are available
	@command -v $(PYTHON) >/dev/null 2>&1 || { \
		echo "$(RED)❌ Python 3 is required but not found$(NC)"; \
		exit 1; \
	}
	@command -v $(UV) >/dev/null 2>&1 || { \
		echo "$(RED)❌ uv is required but not found$(NC)"; \
		echo "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
		exit 1; \
	}
	@command -v $(MKDOCS) >/dev/null 2>&1 || { \
		echo "$(RED)❌ MkDocs is required but not found$(NC)"; \
		echo "Install with: uv sync"; \
		exit 1; \
	}
	@$(PYTHON) -c "import yaml, watchdog" 2>/dev/null || { \
		echo "$(RED)❌ Missing Python dependencies$(NC)"; \
		echo "Install with: uv sync"; \
		exit 1; \
	}

.PHONY: info
info: ## Show build system information
	@echo "$(BLUE)Provide Foundry Documentation Build System$(NC)"
	@echo "==========================================="
	@echo "Platform: $(PLATFORM)"
	@echo "Python: $(shell $(PYTHON) --version 2>&1)"
	@echo "MkDocs: $(shell $(MKDOCS) --version 2>&1 || echo 'Not installed')"
	@echo "Foundry Root: $(FOUNDRY_ROOT)"
	@echo "Documentation Source: $(DOCS_SOURCE)"
	@echo "Aggregated Docs: $(DOCS_AGGREGATED)"
	@echo "Build Output: $(DOCS_OUTPUT)"
	@echo ""
	@echo "Available Projects:"
	@$(MAKE) dev-status

.PHONY: clean-all
clean-all: ## Alias for clean-deep (cleans everything)
	@$(MAKE) clean-deep

# ==================== Cache and Cleanup Targets ====================

.PHONY: cache-clean-flavor
cache-clean-flavor: ## Clean Flavor workenv cache
	@echo "$(BLUE)🧹 Cleaning Flavor workenv cache...$(NC)"
	@if [ -d "$(FLAVOR_CACHE)" ]; then \
		echo "$(YELLOW)📂 Removing $(FLAVOR_CACHE)/workenv$(NC)"; \
		rm -rf "$(FLAVOR_CACHE)/workenv"; \
		echo "$(GREEN)✅ Flavor cache cleaned$(NC)"; \
	else \
		echo "$(YELLOW)⚠️ No Flavor cache found$(NC)"; \
	fi

.PHONY: cache-clean-uv
cache-clean-uv: ## Clean UV package manager cache
	@echo "$(BLUE)🧹 Cleaning UV cache...$(NC)"
	@if [ -d "$(UV_CACHE)" ]; then \
		CACHE_SIZE=$$(du -sh "$(UV_CACHE)" 2>/dev/null | cut -f1); \
		echo "$(YELLOW)📂 Removing $$CACHE_SIZE from $(UV_CACHE)$(NC)"; \
		rm -rf "$(UV_CACHE)"; \
		echo "$(GREEN)✅ UV cache cleaned ($$CACHE_SIZE recovered)$(NC)"; \
	else \
		echo "$(YELLOW)⚠️ No UV cache found$(NC)"; \
	fi

.PHONY: cache-clean-python
cache-clean-python: ## Clean Python bytecode and caches
	@echo "$(BLUE)🧹 Cleaning Python caches...$(NC)"
	@echo "$(YELLOW)🐍 Removing __pycache__ directories...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(YELLOW)🐍 Removing .pyc and .pyo files...$(NC)"
	@find . -name "*.pyc" -o -name "*.pyo" -delete 2>/dev/null || true
	@echo "$(YELLOW)🧪 Removing pytest cache...$(NC)"
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(YELLOW)🔍 Removing linting caches...$(NC)"
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Python caches cleaned$(NC)"

.PHONY: cache-clean-all
cache-clean-all: ## Clean all caches
	@echo "$(BLUE)🧹 Cleaning all caches...$(NC)"
	@$(MAKE) cache-clean-flavor
	@$(MAKE) cache-clean-uv
	@$(MAKE) cache-clean-python
	@echo "$(GREEN)✅ All caches cleaned$(NC)"

.PHONY: clean-build
clean-build: ## Clean build artifacts from all projects
	@echo "$(BLUE)🧹 Cleaning build artifacts...$(NC)"
	@echo "$(YELLOW)📦 Removing dist/ and build/ directories...$(NC)"
	@find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(YELLOW)🥚 Removing egg-info directories...$(NC)"
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(YELLOW)🦀 Removing Rust target directories...$(NC)"
	@find . -type d -name "target" -path "*/flavor-rs/*" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(YELLOW)🐹 Removing Go coverage files...$(NC)"
	@find . -name "coverage.out" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Build artifacts cleaned$(NC)"

.PHONY: clean-workenv
clean-workenv: ## Clean all workenv directories
	@echo "$(BLUE)🧹 Cleaning workenv directories...$(NC)"
	@for project in $(PROJECTS); do \
		if [ -d "../$$project/workenv" ]; then \
			echo "$(YELLOW)📁 Removing ../$$project/workenv$(NC)"; \
			rm -rf "../$$project/workenv"; \
		fi; \
	done
	@echo "$(GREEN)✅ Workenv directories cleaned$(NC)"

.PHONY: clean-coverage
clean-coverage: ## Clean test coverage artifacts
	@echo "$(BLUE)🧹 Cleaning coverage artifacts...$(NC)"
	@echo "$(YELLOW)📊 Removing coverage files...$(NC)"
	@find . -name ".coverage" -delete 2>/dev/null || true
	@find . -name "coverage.xml" -delete 2>/dev/null || true
	@find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.prof" -delete 2>/dev/null || true
	@find . -type d -name ".benchmarks" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Coverage artifacts cleaned$(NC)"

.PHONY: clean-logs
clean-logs: ## Clean log files
	@echo "$(BLUE)🧹 Cleaning log files...$(NC)"
	@echo "$(YELLOW)📝 Removing log files...$(NC)"
	@find . -name "*.log" -delete 2>/dev/null || true
	@find . -name "*.out" ! -path "./site/*" -delete 2>/dev/null || true
	@find . -name "*.err" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Log files cleaned$(NC)"

.PHONY: clean-projects
clean-projects: ## Clean all project build artifacts
	@echo "$(BLUE)🧹 Cleaning project artifacts...$(NC)"
	@for project in $(PROJECTS); do \
		if [ -d "../$$project" ]; then \
			echo "$(YELLOW)🧹 Cleaning $$project...$(NC)"; \
			cd "../$$project" && { \
				if [ -f "Makefile" ]; then \
					make clean 2>/dev/null || true; \
				fi; \
				if [ -f "pyproject.toml" ] && command -v uv >/dev/null 2>&1; then \
					uv cache clean 2>/dev/null || true; \
				fi; \
			} && cd "$(FOUNDRY_ROOT)"; \
		fi; \
	done
	@echo "$(GREEN)✅ Project artifacts cleaned$(NC)"

.PHONY: clean-deep
clean-deep: ## Deep clean everything (with confirmation)
	@echo "$(RED)⚠️ This will clean all caches, build artifacts, and logs$(NC)"
	@echo "$(YELLOW)Continue? [y/N]$(NC)"; \
	read -r confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		echo "$(BLUE)🧹 Starting deep clean...$(NC)"; \
		$(MAKE) cache-clean-all; \
		$(MAKE) clean-build; \
		$(MAKE) clean-workenv; \
		$(MAKE) clean-coverage; \
		$(MAKE) clean-logs; \
		$(MAKE) clean-projects; \
		$(MAKE) docs-clean; \
		echo "$(GREEN)✅ Deep clean completed$(NC)"; \
	else \
		echo "$(YELLOW)❌ Deep clean cancelled$(NC)"; \
	fi

.PHONY: cache-info
cache-info: ## Show cache usage information
	@echo "$(BLUE)📊 Cache Usage Information$(NC)"
	@echo "=========================="
	@echo ""
	@echo "$(GREEN)Cache Directories:$(NC)"
	@if [ -d "$(FLAVOR_CACHE)" ]; then \
		FLAVOR_SIZE=$$(du -sh "$(FLAVOR_CACHE)" 2>/dev/null | cut -f1); \
		echo "  $(YELLOW)Flavor cache:$(NC)     $$FLAVOR_SIZE ($(FLAVOR_CACHE))"; \
	else \
		echo "  $(YELLOW)Flavor cache:$(NC)     Not found"; \
	fi
	@if [ -d "$(UV_CACHE)" ]; then \
		UV_SIZE=$$(du -sh "$(UV_CACHE)" 2>/dev/null | cut -f1); \
		echo "  $(YELLOW)UV cache:$(NC)         $$UV_SIZE ($(UV_CACHE))"; \
	else \
		echo "  $(YELLOW)UV cache:$(NC)         Not found"; \
	fi
	@echo ""
	@echo "$(GREEN)Build Artifacts:$(NC)"
	@DIST_COUNT=$$(find . -type d -name "dist" 2>/dev/null | wc -l); \
	echo "  $(YELLOW)dist/ directories:$(NC) $$DIST_COUNT"
	@BUILD_COUNT=$$(find . -type d -name "build" 2>/dev/null | wc -l); \
	echo "  $(YELLOW)build/ directories:$(NC) $$BUILD_COUNT"
	@PYCACHE_COUNT=$$(find . -type d -name "__pycache__" 2>/dev/null | wc -l); \
	echo "  $(YELLOW)__pycache__ dirs:$(NC)  $$PYCACHE_COUNT"
	@echo ""
	@echo "$(GREEN)Disk Usage:$(NC)"
	@TOTAL_SIZE=$$(du -sh . 2>/dev/null | cut -f1); \
	echo "  $(YELLOW)Total directory:$(NC)   $$TOTAL_SIZE"

.PHONY: cache-prune
cache-prune: ## Prune old cache entries (DAYS=30)
	@echo "$(BLUE)🧹 Pruning cache entries older than $(DAYS_OLD) days...$(NC)"
	@if [ -d "$(FLAVOR_CACHE)/workenv" ]; then \
		echo "$(YELLOW)🔍 Checking Flavor workenv cache...$(NC)"; \
		find "$(FLAVOR_CACHE)/workenv" -type d -mtime +$(DAYS_OLD) -exec rm -rf {} + 2>/dev/null || true; \
	fi
	@echo "$(YELLOW)🐍 Removing old Python cache files...$(NC)"
	@find . -name "*.pyc" -mtime +$(DAYS_OLD) -delete 2>/dev/null || true
	@find . -name "*.pyo" -mtime +$(DAYS_OLD) -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Cache pruning completed$(NC)"

.PHONY: pristine
pristine: ## Complete reset to fresh state (DANGEROUS)
	@echo "$(RED)⚠️ WARNING: This will remove ALL caches, builds, and temporary files$(NC)"
	@echo "$(RED)⚠️ This cannot be undone!$(NC)"
	@echo "$(YELLOW)Type 'PRISTINE' to confirm:$(NC)"; \
	read -r confirm; \
	if [ "$$confirm" = "PRISTINE" ]; then \
		echo "$(BLUE)🧹 Resetting to pristine state...$(NC)"; \
		$(MAKE) clean-deep; \
		echo "$(GREEN)✅ Pristine reset completed$(NC)"; \
	else \
		echo "$(YELLOW)❌ Pristine reset cancelled$(NC)"; \
	fi

# ==================== Default Target ====================

.DEFAULT_GOAL := help

# ==================== Special Targets ====================

# Quick aliases for common commands
.PHONY: build serve clean watch
build: docs-build   ## Alias for docs-build
serve: docs-serve   ## Alias for docs-serve
clean: docs-clean   ## Alias for docs-clean
watch: docs-watch   ## Alias for docs-watch

# Cache cleaning aliases
.PHONY: clean-cache clean-python clean-uv
clean-cache: cache-clean-all      ## Alias for cache-clean-all
clean-python: cache-clean-python  ## Alias for cache-clean-python
clean-uv: cache-clean-uv          ## Alias for cache-clean-uv