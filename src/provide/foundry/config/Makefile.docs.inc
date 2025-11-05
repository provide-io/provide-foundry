# Makefile.docs.inc
# Shared documentation targets for provide.io ecosystem projects
#
# Include this file in your project Makefile with:
#   include ../provide-foundry/Makefile.docs.inc
#
# Requirements:
#   - Project must have mkdocs.yml configured
#   - mkdocs must be available via uv run
#
# Available targets:
#   docs-build    - Build documentation
#   docs-serve    - Serve documentation locally
#   docs-clean    - Clean documentation artifacts
#   docs-validate - Validate documentation with strict mode

# Ensure we have colors defined (can be overridden by parent Makefile)
BLUE ?= \033[0;34m
GREEN ?= \033[0;32m
YELLOW ?= \033[0;33m
RED ?= \033[0;31m
NC ?= \033[0m

# Documentation configuration
MKDOCS ?= uv run mkdocs
DOCS_OUTPUT ?= site

# ==================== Documentation Targets ====================

.PHONY: docs-build
docs-build: ## Build documentation
	@echo "$(BLUE)🏗️  Building documentation...$(NC)"
	@$(MKDOCS) build --clean
	@echo "$(GREEN)✅ Documentation built successfully!$(NC)"
	@echo "$(BLUE)ℹ️  Output: $(DOCS_OUTPUT)$(NC)"

.PHONY: docs-serve
docs-serve: ## Serve documentation locally for development
	@echo "$(BLUE)🚀 Starting documentation development server...$(NC)"
	@echo "$(GREEN)📖 Documentation will be available at: http://127.0.0.1:8000$(NC)"
	@echo "$(YELLOW)🛑 Press Ctrl+C to stop the server$(NC)"
	@$(MKDOCS) serve

.PHONY: docs-clean
docs-clean: ## Clean documentation artifacts
	@echo "$(BLUE)🧹 Cleaning documentation artifacts...$(NC)"
	@rm -rf $(DOCS_OUTPUT)
	@echo "$(GREEN)✅ Documentation artifacts cleaned$(NC)"

.PHONY: docs-validate
docs-validate: ## Validate documentation (strict mode)
	@echo "$(BLUE)🔍 Validating documentation...$(NC)"
	@$(MKDOCS) build --strict
	@echo "$(GREEN)✅ Documentation validation passed$(NC)"

.PHONY: docs-test
docs-test: docs-clean docs-validate ## Test documentation build
	@echo "$(GREEN)✅ Documentation test passed$(NC)"
