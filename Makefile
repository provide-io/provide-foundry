.PHONY: docs-setup docs-build docs-serve docs-clean

docs-setup:
	@uv run python -c "from provide.foundry.config import extract_base_mkdocs; from pathlib import Path; extract_base_mkdocs(Path('.'))"

docs-build: docs-setup
	@uv run mkdocs build

docs-serve: docs-setup
	@uv run mkdocs serve

docs-clean:
	@rm -rf site .provide
