"""
Shared pytest fixtures and configuration for Financial Debt Optimizer tests.
"""

# Add debt_optimizer to Python path for testing
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent / "debt_optimizer"
sys.path.insert(0, str(src_path))

import os  # noqa: E402
import shutil  # noqa: E402
import tempfile  # noqa: E402
from datetime import date  # noqa: E402
from typing import List  # noqa: E402

import pytest  # noqa: E402

from core.financial_calc import (  # noqa: E402
    Debt,
    FutureExpense,
    FutureIncome,
    Income,
    RecurringExpense,
)
from excel_io.excel_reader import ExcelTemplateGenerator  # noqa: E402


@pytest.fixture
def sample_debts() -> List[Debt]:
    """Fixture providing sample debt data for testing."""
    return [
        Debt("Credit Card", 5000.00, 150.00, 18.99, 15),
        Debt("Auto Loan", 15000.00, 350.00, 4.50, 10),
        Debt("Personal Loan", 3000.00, 125.00, 12.50, 25),
        Debt("Student Loan", 8000.00, 85.00, 6.80, 5),
    ]


@pytest.fixture
def sample_income() -> List[Income]:
    """Fixture providing sample income data for testing."""
    return [
        Income("Primary Salary", 3500.00, "bi-weekly", date(2024, 1, 5)),
        Income("Freelance", 800.00, "monthly", date(2024, 1, 1)),
        Income("Side Job", 200.00, "weekly", date(2024, 1, 8)),
    ]


@pytest.fixture
def sample_recurring_expenses() -> List[RecurringExpense]:
    """Fixture providing sample recurring expenses for testing."""
    return [
        RecurringExpense("Netflix", 15.99, "monthly", 15, date(2024, 1, 1)),
        RecurringExpense("Car Insurance", 120.00, "monthly", 25, date(2024, 1, 1)),
        RecurringExpense("Bank Fee", 2.00, "monthly", 1, date(2024, 1, 1)),
        RecurringExpense("Gym Membership", 29.99, "bi-weekly", 15, date(2024, 1, 15)),
    ]


@pytest.fixture
def sample_future_income() -> List[FutureIncome]:
    """Fixture providing sample future income for testing."""
    return [
        FutureIncome("Annual Bonus", 5000.00, date(2025, 3, 15), "once"),
        FutureIncome("Tax Refund", 1200.00, date(2025, 4, 1), "once"),
        FutureIncome("Salary Increase", 500.00, date(2025, 6, 1), "monthly"),
        FutureIncome("Quarterly Bonus", 1000.00, date(2025, 3, 31), "quarterly"),
    ]


@pytest.fixture
def sample_future_expenses() -> List[FutureExpense]:
    """Fixture providing sample future expenses for testing."""
    return [
        FutureExpense("Car Repair", 800.00, date(2025, 2, 15), "once"),
        FutureExpense("Home Improvement", 2500.00, date(2025, 5, 1), "once"),
        FutureExpense(
            "Insurance Increase", 25.00, date(2025, 1, 1), "monthly", date(2025, 12, 31)
        ),
        FutureExpense("Annual Fee", 99.00, date(2025, 1, 1), "annually"),
    ]


@pytest.fixture
def sample_settings() -> dict:
    """Fixture providing sample settings for testing."""
    return {
        "emergency_fund": 1000.0,
        "current_bank_balance": 2500.0,
        "optimization_goal": "minimize_interest",
        "extra_payment": 200.0,
    }


@pytest.fixture
def temp_dir():
    """Fixture providing a temporary directory for file operations."""
    temp_directory = tempfile.mkdtemp()
    yield Path(temp_directory)
    shutil.rmtree(temp_directory)


@pytest.fixture
def sample_excel_template(temp_dir):
    """Fixture providing a sample Excel template file for testing."""
    template_path = temp_dir / "test_template.xlsx"
    ExcelTemplateGenerator.generate_template(
        str(template_path), include_sample_data=True
    )
    return template_path


@pytest.fixture
def empty_excel_template(temp_dir):
    """Fixture providing an empty Excel template file for testing."""
    template_path = temp_dir / "empty_template.xlsx"
    ExcelTemplateGenerator.generate_template(
        str(template_path), include_sample_data=False
    )
    return template_path


# Test data constants
VALID_DEBT_DATA = [
    ["Credit Card 1", 5000.00, 150.00, 18.99, 15],
    ["Auto Loan", 12000.00, 325.00, 4.50, 10],
    ["Personal Loan", 3000.00, 120.00, 12.50, 25],
]

VALID_INCOME_DATA = [
    ["Salary", 3500.00, "bi-weekly", "2024-01-05"],
    ["Freelance", 800.00, "monthly", "2024-01-01"],
]

VALID_SETTINGS_DATA = [
    ["Emergency Fund", 1000.00],
    ["Current Bank Balance", 2000.00],
    ["Optimization Goal", "minimize_interest"],
]


def pytest_configure(config):
    """Pytest configuration hook."""
    # Register custom markers
    config.addinivalue_line("markers", "cli: mark test as CLI command test")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running test")
    config.addinivalue_line("markers", "visualization: mark test as visualization test")
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "excel: mark test as Excel file operation test")

    # Ensure test output directory exists
    test_output_dir = Path(__file__).parent / "test_output"
    test_output_dir.mkdir(exist_ok=True)


@pytest.fixture
def mock_config():
    """Fixture providing a mock Config object for CLI tests."""
    from unittest.mock import MagicMock

    from core.config import Config

    config = MagicMock(spec=Config)
    config.get.side_effect = lambda key, default=None: {
        "input_file": "default.xlsx",
        "output_file": "debt_analysis.xlsx",
        "quicken_db_path": "~/Documents/Test.quicken/data",
        "optimization_goal": "minimize_interest",
        "extra_payment": 0.0,
        "emergency_fund": 1000.0,
        "fuzzy_match_threshold": 80,
        "bank_account_name": "PECU Checking",
        "auto_backup": True,
        "simple_report": False,
        "compare_strategies": False,
    }.get(key, default)
    config.config_path = None

    return config
