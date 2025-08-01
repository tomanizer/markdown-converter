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
	pip install -r requirements/dev.txt
	pre-commit install

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src/markdown_converter --cov-report=html --cov-report=term-missing

test-performance:
	pytest tests/performance/ -v -m performance

test-integration:
	pytest tests/integration/ -v -m integration

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
	pre-commit run --all-files

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
	cd docs && make html

docs-serve:
	cd docs && python -m http.server 8000

# Development
dev-install: install-dev
	pre-commit install

dev-setup: dev-install
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to verify installation"

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