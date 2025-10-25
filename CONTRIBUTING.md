# Contributing to Financial Debt Optimizer

Thank you for your interest in contributing to the Financial Debt Optimizer! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a code of conduct that fosters an open and welcoming environment. By participating in this project, you agree to abide by its terms:

- Be respectful and inclusive
- Focus on constructive feedback
- Respect different viewpoints and experiences
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of financial concepts (debt, interest, payments)
- Familiarity with pandas, numpy, and Excel file formats

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/financial-debt_optimizer.git
   cd financial-debt_optimizer
   ```

## Development Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install development dependencies**:
   ```bash
   pip install -e .[dev]
   ```

3. **Verify installation**:
   ```bash
   debt_optimizer --help
   pytest
   ```

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs or request features
- Search existing issues before creating new ones
- Provide clear, detailed descriptions with examples
- Include system information (Python version, OS, etc.)

### Feature Requests

- Clearly describe the feature and its use case
- Explain why it would be valuable to users
- Consider providing a rough implementation outline

### Bug Reports

Include:
- Steps to reproduce the issue
- Expected vs actual behavior
- Error messages or screenshots
- Input data files (if applicable, anonymized)
- System environment details

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guidelines (checked with pycodestyle)
- Use type hints for function parameters and return values
- Maximum line length: 88 characters (Black formatter default)
- Use descriptive variable and function names

### Code Organization

```python
# Standard imports
import os
import sys
from datetime import date
from typing import List, Dict, Optional

# Third-party imports
import pandas as pd
import numpy as np

# Local imports
from src.core.financial_calc import Debt
```

### Documentation

- Write clear docstrings for all public functions and classes
- Use Google-style docstrings (see example below)
- Follow Black formatting with 88-character line length
- Documentation is automatically updated during releases (see Release Workflow)

**Google-style Docstring Example:**
```python
def calculate_payment(balance: float, rate: float) -> float:
    """Calculate monthly payment for a given balance and rate.
    
    Args:
        balance: The outstanding debt balance
        rate: Annual interest rate as a decimal
        
    Returns:
        Monthly payment amount
        
    Raises:
        ValueError: If balance or rate is negative
    """
```

### Release Workflow and Documentation

**IMPORTANT**: This project uses a mandatory documentation update step that runs for every release (patch, minor, major). This step is non-skippable and automatically:

- Updates and enhances docstrings in modified Python files
- Updates version references throughout documentation
- Generates CHANGELOG entries from git commits
- Commits all changes before version bumping

**Testing Documentation Updates Locally:**
```bash
# Preview changes without committing (dry-run)
python scripts/update_documentation.py \
    --from-version 2.0.2 \
    --to-version 2.0.3 \
    --verbose \
    --dry-run

# Apply documentation updates
python scripts/update_documentation.py \
    --from-version 2.0.2 \
    --to-version 2.0.3 \
    --verbose
```

**Complete Release Workflow:**
```bash
# The full release workflow automatically includes documentation updates
python scripts/release_workflow.py patch --target-version 2.0.3

# For minor releases
python scripts/release_workflow.py minor --target-version 2.1.0

# For major releases  
python scripts/release_workflow.py major --target-version 3.0.0
```

**What Gets Updated Automatically:**
1. Module docstrings added to files missing them
2. Version references in `README.md`, `docs/`, and `.rst` files
3. CHANGELOG.md with categorized bug fixes and improvements
4. Code formatting with Black

**Your Responsibilities as a Contributor:**
- Write initial docstrings for new code (they'll be enhanced during release)
- Use Google-style docstring format
- Stay within 88-character line length
- Write clear commit messages (they're used to generate CHANGELOG)
- Run tests before submitting PRs

### Error Handling

- Use specific exception types
- Provide helpful error messages
- Log errors appropriately
- Validate inputs early

```python
def process_debt_data(debts: List[Dict]) -> List[Debt]:
    """Process raw debt data into Debt objects."""
    if not debts:
        raise ValueError("No debt data provided")
    
    processed_debts = []
    for debt_data in debts:
        try:
            debt = Debt.from_dict(debt_data)
            processed_debts.append(debt)
        except KeyError as e:
            raise ValueError(f"Missing required field in debt data: {e}")
    
    return processed_debts
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_debt_optimizer.py
```

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names: `test_should_calculate_correct_payment_when_given_valid_inputs`
- Test edge cases and error conditions
- Use fixtures for common test data

```python
import pytest
from src.core.debt_optimizer import DebtOptimizer

@pytest.fixture
def sample_debts():
    """Sample debt data for testing."""
    return [
        Debt("Credit Card", 5000.0, 150.0, 18.99, 15),
        Debt("Student Loan", 25000.0, 300.0, 5.50, 1)
    ]

def test_should_optimize_debts_using_avalanche_strategy(sample_debts):
    """Test debt optimization with avalanche strategy."""
    optimizer = DebtOptimizer(sample_debts, [], [], [], [], {})
    result = optimizer.optimize_debt_strategy(goal=OptimizationGoal.MINIMIZE_INTEREST)
    
    assert result.strategy == "avalanche"
    assert result.total_interest_paid > 0
    assert result.total_months_to_freedom > 0
```

### Test Coverage

- Maintain test coverage above 80%
- Focus on testing critical financial calculations
- Test Excel I/O operations with sample files
- Ensure chart generation works properly

## Documentation

### Code Documentation

- Document all public APIs
- Include usage examples in docstrings
- Keep documentation up-to-date with code changes

### User Documentation

- Update README.md for new features
- Add examples for new functionality
- Update CHANGELOG.md for all changes

## Pull Request Process

### Before Submitting

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/add-new-optimization-strategy
   ```

2. **Run the test suite**:
   ```bash
   pytest
   ```

3. **Format code**:
   ```bash
   black debt_optimizer/ tests/
   ```

4. **Run linting**:
   ```bash
   pylint debt_optimizer/
   ```

### Pull Request Guidelines

1. **Clear title and description**
   - Describe what the PR does and why
   - Reference any related issues: "Fixes #123"

2. **Small, focused changes**
   - One feature or fix per PR
   - Keep changes as small as possible while remaining complete

3. **Update documentation**
   - Update docstrings for modified functions
   - Add examples for new features
   - Update README if necessary

4. **Add tests**
   - Include tests for new functionality
   - Ensure existing tests still pass

5. **Update changelog**
   - Add entry to CHANGELOG.md under "Unreleased"

### Review Process

1. All PRs require review from maintainers
2. Address review feedback promptly
3. Keep the PR updated with the main branch
4. Squash commits if requested

## Financial Calculations

When working with financial calculations, ensure:

- Use appropriate precision (decimal.Decimal for currency)
- Handle edge cases (zero balances, negative rates)
- Validate financial logic with test cases
- Document assumptions in comments

## Excel Integration

When working with Excel features:

- Test with various Excel file formats
- Handle missing or invalid data gracefully
- Validate chart generation across platforms
- Consider performance for large datasets

## Questions and Support

- Open an issue for questions about contributing
- Tag issues with appropriate labels
- Be patient and respectful when seeking help

Thank you for contributing to the Financial Debt Optimizer!