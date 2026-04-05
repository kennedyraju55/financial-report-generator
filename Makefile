.PHONY: help install dev test lint run-cli run-web clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt

dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -e ".[dev]"

test: ## Run test suite with coverage
	pytest tests/ -v --tb=short --cov=src/financial_reporter --cov-report=term-missing

lint: ## Run linters (ruff / flake8)
	@command -v ruff >/dev/null 2>&1 && ruff check src/ tests/ || \
		(command -v flake8 >/dev/null 2>&1 && flake8 src/ tests/ || echo "No linter found — install ruff or flake8")

run-cli: ## Run the CLI (pass ARGS, e.g. make run-cli ARGS="report -f data.csv -p Q4-2024")
	python -m src.financial_reporter.cli $(ARGS)

run-web: ## Launch the Streamlit web UI
	streamlit run src/financial_reporter/web_ui.py

clean: ## Remove caches and build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .eggs/
