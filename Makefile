.PHONY: help install install-dev test test-cov lint format type-check clean build dist docs

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install base dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code with black"
	@echo "  type-check   - Run type checking"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build package"
	@echo "  dist         - Create distribution"
	@echo "  docs         - Build documentation"

# Installation
install:
	pip install -r requirements/base.txt

install-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements/dev.txt
	@if command -v pre-commit > /dev/null 2>&1; then \
		pre-commit install; \
		echo "Pre-commit hooks installed successfully."; \
	else \
		echo "Pre-commit not found. Skipping pre-commit installation."; \
	fi

# Testing
test:
	@echo "Running unit tests..."
	pytest tests/unit/ -v

test-cov:
	@echo "Running tests with coverage..."
	pytest tests/ --cov=src/markdown_converter --cov-report=html --cov-report=term-missing

test-performance:
	@echo "Running performance tests..."
	@if [ -d "tests/performance" ]; then \
		pytest tests/performance/ -v -m performance; \
	else \
		echo "Performance tests directory not found. Skipping..."; \
	fi

test-integration:
	@echo "Running integration tests..."
	@if [ -d "tests/integration" ]; then \
		pytest tests/integration/ -v -m integration; \
	else \
		echo "Integration tests directory not found. Skipping..."; \
	fi

# Code quality
lint:
	flake8 src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

format:
	black src/ tests/
	isort src/ tests/

type-check:
	mypy src/

# Pre-commit
pre-commit-run:
	@echo "Running pre-commit hooks..."
	@if command -v pre-commit > /dev/null 2>&1; then \
		pre-commit run --all-files; \
	else \
		echo "Pre-commit not found. Install with: pip install pre-commit"; \
	fi

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Building
build:
	python -m build

dist: clean build

# Documentation
docs:
	@echo "Building documentation..."
	@if [ -d "docs" ] && [ -f "docs/Makefile" ]; then \
		cd docs && make html; \
	else \
		echo "Documentation directory or Makefile not found. Skipping..."; \
	fi

docs-serve:
	@echo "Starting documentation server..."
	@if [ -d "docs/build/html" ]; then \
		cd docs/build/html && python -m http.server 8000; \
	else \
		echo "Documentation not built. Run 'make docs' first."; \
	fi

# Development
dev-install: install-dev
	@echo "Development installation complete!"

dev-setup: dev-install
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to verify installation"
	@echo "Run 'make format' to format code"
	@echo "Run 'make lint' to check code quality"

# CI/CD helpers
ci-test: lint type-check test-cov

ci-build: clean build

# Virtual environment
venv:
	python -m venv venv
	@echo "Virtual environment created. Activate with:"
	@echo "source venv/bin/activate"

# Package management
update-deps:
	pip install --upgrade -r requirements/base.txt
	pip install --upgrade -r requirements/dev.txt

# Quick development cycle
dev-cycle: format lint type-check test

# Release helpers
release-check: clean lint type-check test-cov build
	@echo "Release checks completed successfully!"

# Project setup
setup: venv install-dev
	@echo "Project setup complete!"
	@echo "Activate virtual environment: source venv/bin/activate"
	@echo "Run tests: make test"
