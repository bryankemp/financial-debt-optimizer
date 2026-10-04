"""Tests for paydown percentage feature.

Tests the credit_limit and paydown_target_pct fields on Debt,
Excel reader/writer support, and balance updater integration.
"""

import tempfile
from pathlib import Path

import openpyxl
import pytest

from debt_optimizer.core.financial_calc import Debt
from debt_optimizer.excel_io.excel_reader import ExcelReader, ExcelTemplateGenerator


class TestDebtPaydownPercentage:
    """Test Debt dataclass with paydown percentage fields."""

    def test_debt_with_credit_limit_and_paydown(self):
        """Test Debt creation with credit limit and paydown percentage."""
        debt = Debt(
            name="Credit Card",
            balance=5000.0,
            minimum_payment=150.0,
            interest_rate=18.99,
            due_date=15,
            credit_limit=10000.0,
            paydown_target_pct=29.0,
        )
        assert debt.credit_limit == 10000.0
        assert debt.paydown_target_pct == 29.0
        assert debt.target_balance == 2900.0  # 10000 * 0.29
        assert debt.paydown_amount == 2100.0  # 5000 - 2900

    def test_debt_without_paydown_target(self):
        """Test Debt with credit limit but no paydown target."""
        debt = Debt(
            name="Credit Card",
            balance=5000.0,
            minimum_payment=150.0,
            interest_rate=18.99,
            due_date=15,
            credit_limit=10000.0,
        )
        assert debt.credit_limit == 10000.0
        assert debt.paydown_target_pct is None
        assert debt.target_balance is None
        assert debt.paydown_amount == 5000.0  # Full balance

    def test_debt_without_credit_limit(self):
        """Test Debt without credit limit (e.g., personal loan)."""
        debt = Debt(
            name="Personal Loan",
            balance=3000.0,
            minimum_payment=120.0,
            interest_rate=12.5,
            due_date=25,
        )
        assert debt.credit_limit is None
        assert debt.paydown_target_pct is None
        assert debt.target_balance is None
        assert debt.paydown_amount == 3000.0  # Full balance

    def test_debt_at_target_balance(self):
        """Test Debt when balance is already at target."""
        debt = Debt(
            name="Credit Card",
            balance=2900.0,
            minimum_payment=150.0,
            interest_rate=18.99,
            due_date=15,
            credit_limit=10000.0,
            paydown_target_pct=29.0,
        )
        assert debt.target_balance == 2900.0
        assert debt.paydown_amount == 0.0  # Already at target

    def test_debt_below_target_balance(self):
        """Test Debt when balance is below target."""
        debt = Debt(
            name="Credit Card",
            balance=1000.0,
            minimum_payment=150.0,
            interest_rate=18.99,
            due_date=15,
            credit_limit=10000.0,
            paydown_target_pct=29.0,
        )
        assert debt.target_balance == 2900.0
        assert debt.paydown_amount == 0.0  # Already below target

    def test_invalid_negative_credit_limit(self):
        """Test that negative credit limit raises error."""
        with pytest.raises(ValueError, match="Credit limit cannot be negative"):
            Debt(
                name="Credit Card",
                balance=5000.0,
                minimum_payment=150.0,
                interest_rate=18.99,
                due_date=15,
                credit_limit=-1000.0,
            )

    def test_invalid_paydown_percentage_too_high(self):
        """Test that paydown percentage > 100 raises error."""
        with pytest.raises(
            ValueError, match="Paydown target percentage must be between 0 and 100"
        ):
            Debt(
                name="Credit Card",
                balance=5000.0,
                minimum_payment=150.0,
                interest_rate=18.99,
                due_date=15,
                credit_limit=10000.0,
                paydown_target_pct=150.0,
            )

    def test_invalid_paydown_percentage_negative(self):
        """Test that negative paydown percentage raises error."""
        with pytest.raises(
            ValueError, match="Paydown target percentage must be between 0 and 100"
        ):
            Debt(
                name="Credit Card",
                balance=5000.0,
                minimum_payment=150.0,
                interest_rate=18.99,
                due_date=15,
                credit_limit=10000.0,
                paydown_target_pct=-10.0,
            )

    def test_zero_paydown_percentage(self):
        """Test paydown percentage of 0 (pay to $0)."""
        debt = Debt(
            name="Credit Card",
            balance=5000.0,
            minimum_payment=150.0,
            interest_rate=18.99,
            due_date=15,
            credit_limit=10000.0,
            paydown_target_pct=0.0,
        )
        assert debt.target_balance == 0.0
        assert debt.paydown_amount == 5000.0


class TestExcelReaderPaydownPercentage:
    """Test Excel reader with paydown percentage columns."""

    @pytest.fixture
    def temp_xlsx_with_paydown(self):
        """Create temporary Excel file with paydown columns."""
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            xlsx_path = Path(f.name)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Debts"

        # Headers including new columns
        ws.append(
            [
                "Name",
                "Balance",
                "Min Payment",
                "Interest Rate",
                "Due Date",
                "Credit Limit",
                "Paydown %",
            ]
        )

        # Data rows
        ws.append(["Apple Card", 5000.00, 150.00, 0.1899, 15, 7500.00, 29])
        ws.append(["Auto Loan", 12000.00, 325.00, 0.045, 10, None, None])
        ws.append(["Prime Visa", 2000.00, 50.00, 0.2199, 20, 30000.00, 0])

        # Add Income sheet (required)
        ws_income = wb.create_sheet("Income")
        ws_income.append(["Source", "Amount", "Frequency", "Start Date"])
        ws_income.append(["Salary", 5000.00, "monthly", "2024-01-01"])

        wb.save(xlsx_path)
        wb.close()

        yield xlsx_path
        xlsx_path.unlink()

    def test_read_debts_with_paydown_columns(self, temp_xlsx_with_paydown):
        """Test reading debts with credit limit and paydown percentage."""
        reader = ExcelReader(str(temp_xlsx_with_paydown))
        debts = reader.read_debts()

        assert len(debts) == 3

        # Apple Card - has both credit limit and paydown %
        assert debts[0].name == "Apple Card"
        assert debts[0].credit_limit == 7500.0
        assert debts[0].paydown_target_pct == 29.0
        assert debts[0].target_balance == 2175.0  # 7500 * 0.29

        # Auto Loan - no credit limit or paydown
        assert debts[1].name == "Auto Loan"
        assert debts[1].credit_limit is None
        assert debts[1].paydown_target_pct is None
        assert debts[1].target_balance is None

        # Prime Visa - has credit limit, paydown % is 0
        assert debts[2].name == "Prime Visa"
        assert debts[2].credit_limit == 30000.0
        assert debts[2].paydown_target_pct == 0.0
        assert debts[2].target_balance == 0.0

    @pytest.fixture
    def temp_xlsx_without_paydown(self):
        """Create temporary Excel file without paydown columns (legacy)."""
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            xlsx_path = Path(f.name)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Debts"

        # Legacy headers (no paydown columns)
        ws.append(["Name", "Balance", "Min Payment", "Interest Rate", "Due Date"])
        ws.append(["Credit Card", 5000.00, 150.00, 0.1899, 15])

        # Add Income sheet (required)
        ws_income = wb.create_sheet("Income")
        ws_income.append(["Source", "Amount", "Frequency", "Start Date"])
        ws_income.append(["Salary", 5000.00, "monthly", "2024-01-01"])

        wb.save(xlsx_path)
        wb.close()

        yield xlsx_path
        xlsx_path.unlink()

    def test_read_debts_without_paydown_columns(self, temp_xlsx_without_paydown):
        """Test reading legacy debts without paydown columns."""
        reader = ExcelReader(str(temp_xlsx_without_paydown))
        debts = reader.read_debts()

        assert len(debts) == 1
        assert debts[0].name == "Credit Card"
        assert debts[0].credit_limit is None
        assert debts[0].paydown_target_pct is None
        assert debts[0].target_balance is None


class TestExcelTemplatePaydownColumns:
    """Test Excel template generator includes paydown columns."""

    def test_template_has_paydown_columns(self):
        """Test generated template includes credit limit and paydown % columns."""
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            xlsx_path = Path(f.name)

        try:
            ExcelTemplateGenerator.generate_template(
                str(xlsx_path), include_sample_data=True
            )

            wb = openpyxl.load_workbook(xlsx_path)
            ws = wb["Debts"]

            # Check headers
            headers = [ws.cell(row=1, column=i).value for i in range(1, 8)]
            assert "Credit Limit" in headers
            assert "Paydown %" in headers

            # Check sample data has values
            credit_limit_col = headers.index("Credit Limit") + 1
            paydown_col = headers.index("Paydown %") + 1

            # First row should have credit limit and paydown %
            assert ws.cell(row=2, column=credit_limit_col).value == 10000.00
            assert ws.cell(row=2, column=paydown_col).value == 29

            wb.close()
        finally:
            xlsx_path.unlink()
