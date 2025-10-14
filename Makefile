# Makefile for Financial Debt Optimizer

.PHONY: help install install-dev test test-unit test-integration test-slow test-coverage clean lint format type-check security docs

# Default target
help:
	@echo "Financial Debt Optimizer - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  install          Install production dependencies"
	@echo "  install-dev      Install development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test             Run all tests"
	@echo "  test-unit        Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-slow        Run slow tests only"
	@echo "  test-coverage    Run tests with detailed coverage report"
	@echo "  test-parallel    Run tests in parallel for speed"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint             Run linting checks"
	@echo "  format           Format code with black and isort"
	@echo "  type-check       Run type checking with mypy"
	@echo "  security         Run security checks"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean            Clean up temporary files and caches"
	@echo "  docs             Generate documentation"

# Setup targets
install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-test.txt
	pip install -e .

# Testing targets
test:
	pytest

test-unit:
	pytest -m "unit" -v

test-integration:
	pytest -m "integration" -v

test-slow:
	pytest -m "slow" -v --tb=short

test-coverage:
	pytest --cov=src --cov-report=html --cov-report=term-missing

test-parallel:
	pytest -n auto

# Code quality targets
lint:
	flake8 src tests
	black --check src tests
	isort --check-only src tests

format:
	black src tests
	isort src tests

type-check:
	mypy src --ignore-missing-imports

security:
	safety check
	bandit -r src

# Maintenance targets
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find tests -name "*.xlsx" -delete
	find tests -name "test_output" -type d -exec rm -rf {} + 2>/dev/null || true

docs:
	cd docs && make html

# Development workflow targets
check: lint type-check security test-unit

ci: check test-integration

# Package building
build:
	python -m build

upload-test:
	python -m twine upload --repository testpypi dist/*

upload:
	python -m twine upload dist/*

# Quick development cycle
dev: format test-unit

# Full validation before commit
pre-commit: clean format lint type-check security test-coverage