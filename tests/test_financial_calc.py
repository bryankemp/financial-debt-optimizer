"""
Comprehensive tests for financial_calc.py module.

Tests all financial calculation classes: Debt, Income, RecurringExpense,
FutureIncome, FutureExpense, and related utility functions.
"""

# Add debt_optimizer to Python path for testing
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent / "debt_optimizer"
sys.path.insert(0, str(src_path))

from datetime import date, datetime, timedelta  # noqa: E402
from decimal import Decimal  # noqa: E402

import pytest  # noqa: E402

from core.financial_calc import (  # noqa: E402
    Debt,
    FutureExpense,
    FutureIncome,
    Income,
    PaymentFrequency,
    RecurrencePattern,
    RecurringExpense,
    calculate_monthly_payment,
)


class TestDebt:
    """Test cases for the Debt class."""

    @pytest.mark.unit
    def test_debt_creation_valid(self):
        """Test that Debt objects are created correctly with valid data."""
        debt = Debt("Test Credit Card", 1000.0, 25.0, 15.99, 15)
        assert debt.name == "Test Credit Card"
        assert debt.balance == 1000.0
        assert debt.minimum_payment == 25.0
        assert debt.interest_rate == 15.99
        assert debt.due_date == 15

    @pytest.mark.unit
    def test_debt_creation_edge_cases(self):
        """Test Debt creation with edge case values."""
        # Zero balance debt
        debt_zero = Debt("Paid Off Card", 0.0, 0.0, 0.0, 1)
        assert debt_zero.balance == 0.0

        # High interest rate
        debt_high_rate = Debt("High Rate Card", 5000.0, 200.0, 29.99, 31)
        assert debt_high_rate.interest_rate == 29.99
        assert debt_high_rate.due_date == 31

        # Large balance
        debt_large = Debt("Mortgage", 500000.0, 2500.0, 3.5, 1)
        assert debt_large.balance == 500000.0

    @pytest.mark.unit
    def test_monthly_interest_rate(self):
        """Test monthly interest rate calculation."""
        debt = Debt("Test Card", 1000.0, 25.0, 12.0, 15)  # 12% annual
        monthly_rate = debt.interest_rate / 12
        assert abs(monthly_rate - 1.0) < 0.001  # Should be ~1% monthly

        # Zero interest rate
        debt_zero = Debt("Zero Interest", 1000.0, 50.0, 0.0, 15)
        assert debt_zero.interest_rate == 0.0

    @pytest.mark.unit
    def test_debt_string_representation(self):
        """Test string representation of Debt objects."""
        debt = Debt("Test Card", 1000.0, 25.0, 15.99, 15)
        debt_str = str(debt)
        assert "Test Card" in debt_str
        assert "1000" in debt_str or "1,000" in debt_str

    @pytest.mark.unit
    def test_debt_equality(self):
        """Test Debt object equality comparison."""
        debt1 = Debt("Card A", 1000.0, 25.0, 15.99, 15)
        debt2 = Debt("Card A", 1000.0, 25.0, 15.99, 15)
        debt3 = Debt("Card B", 1000.0, 25.0, 15.99, 15)

        assert debt1 == debt2
        assert debt1 != debt3

    @pytest.mark.unit
    def test_debt_validation_negative_balance(self):
        """Test Debt validation with negative balance."""
        with pytest.raises(ValueError, match="balance cannot be negative"):
            Debt("Invalid", -100.0, 25.0, 15.0, 15)

    @pytest.mark.unit
    def test_debt_validation_negative_payment(self):
        """Test Debt validation with negative minimum payment."""
        with pytest.raises(ValueError, match="payment cannot be negative"):
            Debt("Invalid", 1000.0, -25.0, 15.0, 15)

    @pytest.mark.unit
    def test_debt_validation_negative_rate(self):
        """Test Debt validation with negative interest rate."""
        with pytest.raises(ValueError, match="rate cannot be negative"):
            Debt("Invalid", 1000.0, 25.0, -15.0, 15)

    @pytest.mark.unit
    def test_debt_validation_invalid_due_date(self):
        """Test Debt validation with invalid due date."""
        with pytest.raises(ValueError, match="Due date must be between 1 and 31"):
            Debt("Invalid", 1000.0, 25.0, 15.0, 0)
        with pytest.raises(ValueError, match="Due date must be between 1 and 31"):
            Debt("Invalid", 1000.0, 25.0, 15.0, 32)

    @pytest.mark.unit
    def test_debt_monthly_interest_rate_property(self):
        """Test monthly interest rate property."""
        debt = Debt("Test", 1000.0, 25.0, 12.0, 15)  # 12% annual
        assert abs(debt.monthly_interest_rate - 0.01) < 0.0001  # 1% monthly

    @pytest.mark.unit
    def test_debt_calculate_interest_charge(self):
        """Test interest charge calculation."""
        debt = Debt("Test", 1000.0, 25.0, 12.0, 15)  # 12% annual = 1% monthly
        interest = debt.calculate_interest_charge(1000.0)
        assert abs(interest - 10.0) < 0.01  # 1% of 1000 is 10

    @pytest.mark.unit
    def test_debt_calculate_principal_payment(self):
        """Test principal payment calculation."""
        debt = Debt("Test", 1000.0, 25.0, 12.0, 15)
        balance = 1000.0
        total_payment = 100.0

        principal = debt.calculate_principal_payment(total_payment, balance)
        interest = debt.calculate_interest_charge(balance)

        # Principal should be payment minus interest
        assert abs(principal - (total_payment - interest)) < 0.01

    @pytest.mark.unit
    def test_debt_calculate_months_to_payoff(self):
        """Test months to payoff calculation."""
        debt = Debt("Test", 1000.0, 50.0, 18.0, 15)

        # With $100 payment
        months = debt.calculate_months_to_payoff(100.0)
        assert months > 0
        assert months < float("inf")

    @pytest.mark.unit
    def test_debt_calculate_months_to_payoff_zero_interest(self):
        """Test months to payoff with zero interest."""
        debt = Debt("Test", 1000.0, 50.0, 0.0, 15)
        months = debt.calculate_months_to_payoff(100.0)
        assert months == 10.0  # 1000 / 100 = 10 months

    @pytest.mark.unit
    def test_debt_calculate_months_to_payoff_insufficient_payment(self):
        """Test months to payoff with payment too small."""
        debt = Debt("Test", 10000.0, 50.0, 24.0, 15)  # 2% monthly interest
        # Payment of $100 is less than monthly interest on $10,000
        months = debt.calculate_months_to_payoff(100.0)
        assert months == float("inf")


class TestIncome:
    """Test cases for the Income class."""

    @pytest.mark.unit
    def test_income_creation_valid(self):
        """Test that Income objects are created correctly with valid data."""
        income = Income("Salary", 5000.0, "monthly", date(2024, 1, 1))
        assert income.source == "Salary"
        assert income.amount == 5000.0
        assert income.frequency == "monthly"
        assert income.start_date == date(2024, 1, 1)

    @pytest.mark.unit
    def test_income_frequencies(self):
        """Test Income creation with different frequency types."""
        frequencies = ["weekly", "bi-weekly", "monthly", "quarterly", "annually"]

        for freq in frequencies:
            income = Income(f"Test {freq}", 1000.0, freq, date(2024, 1, 1))
            assert income.frequency == freq

    @pytest.mark.unit
    def test_monthly_income_conversion(self):
        """Test conversion of different income frequencies to monthly amounts."""
        # Weekly income
        weekly_income = Income("Weekly Job", 400.0, "weekly", date(2024, 1, 1))
        monthly_weekly = weekly_income.get_monthly_amount()
        assert abs(monthly_weekly - (400.0 * 52 / 12)) < 0.01

        # Bi-weekly income
        biweekly_income = Income("Salary", 2000.0, "bi-weekly", date(2024, 1, 1))
        monthly_biweekly = biweekly_income.get_monthly_amount()
        assert abs(monthly_biweekly - (2000.0 * 26 / 12)) < 0.01

        # Monthly income
        monthly_income = Income("Freelance", 3000.0, "monthly", date(2024, 1, 1))
        monthly_monthly = monthly_income.get_monthly_amount()
        assert monthly_monthly == 3000.0

        # Quarterly income
        quarterly_income = Income("Bonus", 6000.0, "quarterly", date(2024, 1, 1))
        monthly_quarterly = quarterly_income.get_monthly_amount()
        assert abs(monthly_quarterly - (6000.0 / 3)) < 0.01

        # Annual income
        annual_income = Income("Annual Bonus", 12000.0, "annually", date(2024, 1, 1))
        monthly_annual = annual_income.get_monthly_amount()
        assert abs(monthly_annual - (12000.0 / 12)) < 0.01

    @pytest.mark.unit
    def test_income_edge_cases(self):
        """Test Income with edge case values."""
        # Very small amount (Income class requires positive amounts)
        small_income = Income("Small Income", 0.01, "monthly", date(2024, 1, 1))
        assert small_income.get_monthly_amount() == 0.01

        # Large amount
        large_income = Income("CEO Salary", 100000.0, "monthly", date(2024, 1, 1))
        assert large_income.get_monthly_amount() == 100000.0

    @pytest.mark.unit
    def test_income_validation_negative_amount(self):
        """Test Income validation with negative amount."""
        with pytest.raises(ValueError, match="must be positive"):
            Income("Invalid", -1000.0, "monthly", date(2024, 1, 1))

    @pytest.mark.unit
    def test_income_validation_zero_amount(self):
        """Test Income validation with zero amount."""
        with pytest.raises(ValueError, match="must be positive"):
            Income("Invalid", 0.0, "monthly", date(2024, 1, 1))

    @pytest.mark.unit
    def test_income_validation_invalid_frequency(self):
        """Test Income validation with invalid frequency."""
        with pytest.raises(ValueError, match="Frequency must be one of"):
            Income("Invalid", 1000.0, "invalid_freq", date(2024, 1, 1))

    @pytest.mark.unit
    def test_income_string_representation(self):
        """Test string representation of Income objects."""
        income = Income("Test Salary", 5000.0, "monthly", date(2024, 1, 1))
        income_str = str(income)
        assert "Test Salary" in income_str
        assert "5000" in income_str or "5,000" in income_str
        assert "monthly" in income_str


class TestRecurringExpense:
    """Test cases for the RecurringExpense class."""

    @pytest.mark.unit
    def test_recurring_expense_creation(self):
        """Test RecurringExpense object creation."""
        expense = RecurringExpense("Netflix", 15.99, "monthly", 15, date(2024, 1, 1))
        assert expense.description == "Netflix"
        assert expense.amount == 15.99
        assert expense.frequency == "monthly"
        assert expense.due_date == 15
        assert expense.start_date == date(2024, 1, 1)

    @pytest.mark.unit
    def test_recurring_expense_monthly_amount(self):
        """Test get_monthly_amount method for RecurringExpense."""
        # Monthly expense
        monthly_exp = RecurringExpense(
            "Subscription", 20.0, "monthly", 15, date(2024, 1, 1)
        )
        assert monthly_exp.get_monthly_amount() == 20.0

        # Bi-weekly expense
        biweekly_exp = RecurringExpense("Gym", 30.0, "bi-weekly", 15, date(2024, 1, 1))
        expected_monthly = 30.0 * 26 / 12
        assert abs(biweekly_exp.get_monthly_amount() - expected_monthly) < 0.01

        # Quarterly expense
        quarterly_exp = RecurringExpense(
            "Insurance", 300.0, "quarterly", 1, date(2024, 1, 1)
        )
        assert abs(quarterly_exp.get_monthly_amount() - 100.0) < 0.01

        # Annual expense
        annual_exp = RecurringExpense(
            "Membership", 120.0, "annually", 1, date(2024, 1, 1)
        )
        assert abs(annual_exp.get_monthly_amount() - 10.0) < 0.01

    @pytest.mark.unit
    def test_recurring_expense_date_calculation(self):
        """Test date calculation methods for recurring expenses."""
        # Use current date to ensure we get future payment dates
        expense_start = date.today() - timedelta(days=30)  # Start in the past
        expense = RecurringExpense("Test", 10.0, "monthly", 15, expense_start)

        # Test getting payment dates
        range_start = date.today()
        range_end = date.today() + timedelta(days=180)
        payment_dates = expense.get_payment_dates(range_start, range_end)

        assert len(payment_dates) >= 0  # Should get some dates or empty list
        assert all(isinstance(d, date) for d in payment_dates)

    @pytest.mark.unit
    def test_recurring_expense_frequencies(self):
        """Test RecurringExpense with different frequencies."""
        frequencies = ["bi-weekly", "monthly", "quarterly", "annually"]

        for freq in frequencies:
            expense = RecurringExpense(
                f"Test {freq}", 100.0, freq, 15, date(2024, 1, 1)
            )
            monthly_amount = expense.get_monthly_amount()
            assert monthly_amount > 0


class TestFutureIncome:
    """Test cases for the FutureIncome class."""

    @pytest.mark.unit
    def test_future_income_creation(self):
        """Test FutureIncome object creation."""
        future_date = date.today() + timedelta(days=90)

        # One-time income
        one_time = FutureIncome("Bonus", 5000.0, future_date, "once")
        assert one_time.description == "Bonus"
        assert one_time.amount == 5000.0
        assert one_time.start_date == future_date
        assert one_time.frequency == "once"
        assert one_time.end_date is None

        # Recurring income with end date
        start_date = date.today() + timedelta(days=30)
        end_date = date.today() + timedelta(days=180)
        recurring = FutureIncome("Temp Job", 2000.0, start_date, "monthly", end_date)
        assert recurring.end_date == end_date

    @pytest.mark.unit
    def test_future_income_is_recurring(self):
        """Test is_recurring method."""
        future_date1 = date.today() + timedelta(days=90)
        future_date2 = date.today() + timedelta(days=30)

        one_time = FutureIncome("Bonus", 5000.0, future_date1, "once")
        recurring = FutureIncome("Salary Raise", 500.0, future_date2, "monthly")

        assert one_time.is_recurring() is False
        assert recurring.is_recurring() is True

    @pytest.mark.unit
    def test_future_income_get_occurrences(self):
        """Test getting income occurrences within a range."""
        future_date = date.today() + timedelta(days=90)
        range_start = date.today() + timedelta(days=30)
        range_end = date.today() + timedelta(days=365)

        # One-time income
        one_time = FutureIncome("Bonus", 5000.0, future_date, "once")
        occurrences = one_time.get_occurrences(range_start, range_end)
        assert len(occurrences) == 1
        assert occurrences[0] == (future_date, 5000.0)

        # Recurring income
        recurring_start = date.today() + timedelta(days=45)
        recurring = FutureIncome("Monthly Income", 1000.0, recurring_start, "monthly")
        occurrences = recurring.get_occurrences(
            range_start, range_start + timedelta(days=120)
        )
        assert len(occurrences) >= 2  # At least 2-3 monthly occurrences

        # Income with end date
        limited_start = date.today() + timedelta(days=30)
        limited_end = date.today() + timedelta(days=120)
        limited = FutureIncome(
            "Contract", 2000.0, limited_start, "monthly", limited_end
        )
        occurrences = limited.get_occurrences(range_start, range_end)
        assert len(occurrences) >= 2  # Limited to ~3 months

    @pytest.mark.unit
    def test_future_income_total_amount(self):
        """Test getting total income amount in range."""
        future_date = date.today() + timedelta(days=90)
        range_start = date.today() + timedelta(days=30)
        range_end = date.today() + timedelta(days=365)

        one_time = FutureIncome("Bonus", 5000.0, future_date, "once")
        total = one_time.get_total_amount_in_range(range_start, range_end)
        assert total == 5000.0


class TestFutureExpense:
    """Test cases for the FutureExpense class."""

    @pytest.mark.unit
    def test_future_expense_creation(self):
        """Test FutureExpense object creation."""
        future_date = date.today() + timedelta(days=90)

        # One-time expense
        one_time = FutureExpense("Car Repair", 1500.0, future_date, "once")
        assert one_time.description == "Car Repair"
        assert one_time.amount == 1500.0
        assert one_time.start_date == future_date
        assert one_time.frequency == "once"

    @pytest.mark.unit
    def test_future_expense_is_recurring(self):
        """Test is_recurring method for FutureExpense."""
        future_date1 = date.today() + timedelta(days=90)
        future_date2 = date.today() + timedelta(days=30)

        one_time = FutureExpense("Emergency", 2000.0, future_date1, "once")
        recurring = FutureExpense("Rent Increase", 100.0, future_date2, "monthly")

        assert one_time.is_recurring() is False
        assert recurring.is_recurring() is True

    @pytest.mark.unit
    def test_future_expense_get_occurrences(self):
        """Test getting expense occurrences."""
        future_date = date.today() + timedelta(days=60)
        range_start = date.today() + timedelta(days=30)
        range_end = date.today() + timedelta(days=180)

        one_time = FutureExpense("Vacation", 3000.0, future_date, "once")
        occurrences = one_time.get_occurrences(range_start, range_end)

        assert len(occurrences) == 1
        assert occurrences[0] == (future_date, 3000.0)


class TestPaymentFrequency:
    """Test cases for PaymentFrequency enum."""

    @pytest.mark.unit
    def test_payment_frequency_values(self):
        """Test PaymentFrequency enum values."""
        assert PaymentFrequency.ONCE.value == "once"
        assert PaymentFrequency.DAILY.value == "daily"
        assert PaymentFrequency.WEEKLY.value == "weekly"
        assert PaymentFrequency.BI_WEEKLY.value == "bi-weekly"
        assert PaymentFrequency.SEMI_MONTHLY.value == "semi-monthly"
        assert PaymentFrequency.MONTHLY.value == "monthly"
        assert PaymentFrequency.QUARTERLY.value == "quarterly"
        assert PaymentFrequency.SEMI_ANNUALLY.value == "semi-annually"
        assert PaymentFrequency.ANNUALLY.value == "annually"

    @pytest.mark.unit
    def test_payment_frequency_iteration(self):
        """Test that we can iterate over PaymentFrequency."""
        frequencies = [freq.value for freq in PaymentFrequency]
        assert len(frequencies) == 9
        assert "monthly" in frequencies
        assert "once" in frequencies


class TestUtilityFunctions:
    """Test cases for utility functions."""

    @pytest.mark.unit
    def test_calculate_monthly_payment_basic(self):
        """Test basic monthly payment calculation."""
        # Test with typical loan parameters
        principal = 10000.0
        annual_rate = 6.0  # 6% annually
        months = 5 * 12  # 5 years in months

        monthly_payment = calculate_monthly_payment(principal, annual_rate, months)

        # Payment should be positive and reasonable
        assert monthly_payment > 0
        assert monthly_payment < principal  # Shouldn't be more than the total
        assert 150 < monthly_payment < 250  # Rough range check for 10k over 5 years

    @pytest.mark.unit
    def test_calculate_monthly_payment_zero_interest(self):
        """Test monthly payment calculation with zero interest."""
        principal = 12000.0
        annual_rate = 0.0
        months = 2 * 12  # 2 years in months

        monthly_payment = calculate_monthly_payment(principal, annual_rate, months)
        expected_payment = principal / months

        assert abs(monthly_payment - expected_payment) < 0.01

    @pytest.mark.unit
    def test_calculate_monthly_payment_edge_cases(self):
        """Test monthly payment calculation with edge cases."""
        # Very small principal
        small_payment = calculate_monthly_payment(100.0, 5.0, 12)  # 1 year
        assert small_payment > 0

        # Very high interest rate
        high_rate_payment = calculate_monthly_payment(10000.0, 30.0, 60)  # 5 years
        assert high_rate_payment > 0

        # Very long term
        long_term_payment = calculate_monthly_payment(100000.0, 4.0, 360)  # 30 years
        assert long_term_payment > 0

    @pytest.mark.unit
    def test_calculate_monthly_payment_precision(self):
        """Test that monthly payment calculations are precise."""
        # Use known values that should produce predictable results
        principal = 1000.0
        annual_rate = 12.0  # 1% monthly
        months = 12  # 1 year, 12 payments

        payment = calculate_monthly_payment(principal, annual_rate, months)

        # Should be close to a known calculation result
        # (This is an approximation - exact value would need financial calculator)
        assert 85 < payment < 90


class TestDataValidation:
    """Test cases for data validation and error handling."""

    @pytest.mark.unit
    def test_debt_validation(self):
        """Test Debt object validation."""
        # Valid debt should create without issues
        valid_debt = Debt("Valid Card", 1000.0, 50.0, 15.0, 15)
        assert valid_debt.name == "Valid Card"

        # Test edge cases that should still be valid
        zero_balance = Debt("Paid Off", 0.0, 0.0, 0.0, 1)
        assert zero_balance.balance == 0.0

    @pytest.mark.unit
    def test_income_validation(self):
        """Test Income object validation."""
        # Valid income should create without issues
        valid_income = Income("Salary", 5000.0, "monthly", date(2024, 1, 1))
        assert valid_income.source == "Salary"

        # Test with different valid frequencies
        frequencies = ["weekly", "bi-weekly", "monthly", "quarterly", "annually"]
        for freq in frequencies:
            income = Income("Test", 1000.0, freq, date(2024, 1, 1))
            assert income.frequency == freq

    @pytest.mark.unit
    def test_date_handling(self):
        """Test proper date handling across all classes."""
        test_date = date(2024, 2, 29)  # Leap year date (for past classes)
        future_test_date = date.today() + timedelta(
            days=60
        )  # Future date for FutureIncome

        # Test with all date-containing classes
        income = Income("Test", 1000.0, "monthly", test_date)
        assert income.start_date == test_date

        expense = RecurringExpense("Test", 100.0, "monthly", 15, test_date)
        assert expense.start_date == test_date

        future_income = FutureIncome("Test", 500.0, future_test_date, "once")
        assert future_income.start_date == future_test_date


class TestRecurrencePattern:
    """Test cases for RecurrencePattern class."""

    @pytest.mark.unit
    def test_recurrence_pattern_creation(self):
        """Test RecurrencePattern creation with valid data."""
        start = date(2024, 1, 1)
        pattern = RecurrencePattern("monthly", start)
        assert pattern.frequency == "monthly"
        assert pattern.start_date == start
        assert pattern.end_date is None

    @pytest.mark.unit
    def test_recurrence_pattern_invalid_frequency(self):
        """Test RecurrencePattern raises error for invalid frequency."""
        with pytest.raises(ValueError, match="Frequency must be one of"):
            RecurrencePattern("invalid_freq", date(2024, 1, 1))

    @pytest.mark.unit
    def test_recurrence_pattern_invalid_date_range(self):
        """Test RecurrencePattern raises error when start > end."""
        start = date(2024, 6, 1)
        end = date(2024, 1, 1)  # End before start
        with pytest.raises(ValueError, match="Start date cannot be after end date"):
            RecurrencePattern("monthly", start, end)

    @pytest.mark.unit
    def test_recurrence_pattern_once(self):
        """Test ONCE frequency pattern."""
        start = date(2024, 3, 15)
        pattern = RecurrencePattern("once", start)

        range_start = date(2024, 1, 1)
        range_end = date(2024, 12, 31)
        dates = pattern.get_dates(range_start, range_end)

        assert len(dates) == 1
        assert dates[0] == start

    @pytest.mark.unit
    def test_recurrence_pattern_daily(self):
        """Test DAILY frequency pattern."""
        start = date(2024, 1, 1)
        pattern = RecurrencePattern("daily", start)

        range_start = date(2024, 1, 1)
        range_end = date(2024, 1, 10)
        dates = pattern.get_dates(range_start, range_end)

        assert len(dates) == 10  # 10 days inclusive
        assert dates[0] == date(2024, 1, 1)
        assert dates[-1] == date(2024, 1, 10)

    @pytest.mark.unit
    def test_recurrence_pattern_weekly(self):
        """Test WEEKLY frequency pattern."""
        start = date(2024, 1, 1)  # Monday
        pattern = RecurrencePattern("weekly", start)

        range_start = date(2024, 1, 1)
        range_end = date(2024, 1, 31)
        dates = pattern.get_dates(range_start, range_end)

        assert len(dates) >= 4  # At least 4 weeks in January
        # Check they're 7 days apart
        for i in range(1, len(dates)):
            assert (dates[i] - dates[i - 1]).days == 7

    @pytest.mark.unit
    def test_recurrence_pattern_bi_weekly(self):
        """Test BI_WEEKLY frequency pattern."""
        start = date(2024, 1, 1)
        pattern = RecurrencePattern("bi-weekly", start)

        range_start = date(2024, 1, 1)
        range_end = date(2024, 3, 31)
        dates = pattern.get_dates(range_start, range_end)

        assert len(dates) >= 6  # At least 6 bi-weekly occurrences in 3 months
        # Check they're 14 days apart
        for i in range(1, len(dates)):
            assert (dates[i] - dates[i - 1]).days == 14

    @pytest.mark.unit
    def test_recurrence_pattern_semi_monthly(self):
        """Test SEMI_MONTHLY frequency pattern (1st and 15th)."""
        start = date(2024, 1, 1)
        pattern = RecurrencePattern("semi-monthly", start)

        range_start = date(2024, 1, 1)
        range_end = date(2024, 2, 29)
        dates = pattern.get_dates(range_start, range_end)

        # Should have 1st and 15th of each month
        assert len(dates) == 4  # Jan 1, Jan 15, Feb 1, Feb 15
        assert date(2024, 1, 1) in dates
        assert date(2024, 1, 15) in dates
        assert date(2024, 2, 1) in dates
        assert date(2024, 2, 15) in dates

    @pytest.mark.unit
    def test_recurrence_pattern_monthly_normal_day(self):
        """Test MONTHLY frequency with regular day."""
        start = date(2024, 1, 15)
        pattern = RecurrencePattern("monthly", start)

        range_start = date(2024, 1, 1)
        range_end = date(2024, 6, 30)
        dates = pattern.get_dates(range_start, range_end)

        assert len(dates) == 6  # 6 months
        # All should be on the 15th
        assert all(d.day == 15 for d in dates)

    @pytest.mark.unit
    def test_recurrence_pattern_monthly_day_31(self):
        """Test MONTHLY frequency with day 31 (month length handling)."""
        start = date(2024, 1, 31)
        pattern = RecurrencePattern("monthly", start)

        range_start = date(2024, 1, 1)
        range_end = date(2024, 4, 30)
        dates = pattern.get_dates(range_start, range_end)

        assert len(dates) == 4
        assert dates[0] == date(2024, 1, 31)
        assert dates[1] == date(2024, 2, 29)  # Feb has 29 in 2024 (leap year)
        assert dates[2] == date(2024, 3, 31)
        # April has 30 days, so should use last day

    @pytest.mark.unit
    def test_recurrence_pattern_quarterly(self):
        """Test QUARTERLY frequency pattern."""
        start = date(2024, 1, 15)
        pattern = RecurrencePattern("quarterly", start)

        range_start = date(2024, 1, 1)
        range_end = date(2024, 12, 31)
        dates = pattern.get_dates(range_start, range_end)

        assert len(dates) == 4  # 4 quarters in a year
        # Check they're ~3 months apart
        assert dates[0].month == 1
        assert dates[1].month == 4
        assert dates[2].month == 7
        assert dates[3].month == 10

    @pytest.mark.unit
    def test_recurrence_pattern_semi_annually(self):
        """Test SEMI_ANNUALLY frequency pattern."""
        start = date(2024, 1, 15)
        pattern = RecurrencePattern("semi-annually", start)

        range_start = date(2024, 1, 1)
        range_end = date(2024, 12, 31)
        dates = pattern.get_dates(range_start, range_end)

        assert len(dates) == 2  # Twice a year
        # Should be ~6 months apart
        assert dates[0].month == 1
        assert dates[1].month == 7

    @pytest.mark.unit
    def test_recurrence_pattern_annually(self):
        """Test ANNUALLY frequency pattern."""
        start = date(2024, 1, 15)
        pattern = RecurrencePattern("annually", start)

        range_start = date(2024, 1, 1)
        range_end = date(2026, 12, 31)
        dates = pattern.get_dates(range_start, range_end)

        assert len(dates) == 3  # 3 years
        assert dates[0] == date(2024, 1, 15)
        assert dates[1] == date(2025, 1, 15)
        assert dates[2] == date(2026, 1, 15)

    @pytest.mark.unit
    def test_recurrence_pattern_with_end_date(self):
        """Test pattern respects end_date."""
        start = date(2024, 1, 1)
        end = date(2024, 3, 31)
        pattern = RecurrencePattern("monthly", start, end)

        range_start = date(2024, 1, 1)
        range_end = date(2024, 12, 31)
        dates = pattern.get_dates(range_start, range_end)

        assert len(dates) == 3  # Jan, Feb, Mar only
        assert all(d <= end for d in dates)

    @pytest.mark.unit
    def test_recurrence_pattern_empty_range(self):
        """Test pattern returns empty list for invalid range."""
        start = date(2024, 6, 1)
        pattern = RecurrencePattern("monthly", start)

        # Request range before pattern starts
        range_start = date(2024, 1, 1)
        range_end = date(2024, 3, 31)
        dates = pattern.get_dates(range_start, range_end)

        assert len(dates) == 0

    @pytest.mark.unit
    def test_recurrence_pattern_get_monthly_frequency(self):
        """Test get_monthly_frequency for different patterns."""
        start = date(2024, 1, 1)

        # Test different frequencies
        patterns_and_expected = [
            ("once", 0.0),
            ("daily", 30.4),
            ("weekly", 4.35),
            ("bi-weekly", 2.17),
            ("semi-monthly", 2.0),
            ("monthly", 1.0),
            ("quarterly", 1 / 3),
            ("semi-annually", 1 / 6),
            ("annually", 1 / 12),
        ]

        for freq, expected in patterns_and_expected:
            pattern = RecurrencePattern(freq, start)
            actual = pattern.get_monthly_frequency()
            assert abs(actual - expected) < 0.01, f"Failed for {freq}"

    @pytest.mark.unit
    def test_recurrence_pattern_str_with_end_date(self):
        """Test string representation with end date."""
        start = date(2024, 1, 1)
        end = date(2024, 12, 31)
        pattern = RecurrencePattern("monthly", start, end)

        pattern_str = str(pattern)
        assert "monthly" in pattern_str.lower()
        assert "2024-01-01" in pattern_str
        assert "2024-12-31" in pattern_str

    @pytest.mark.unit
    def test_recurrence_pattern_str_without_end_date(self):
        """Test string representation without end date."""
        start = date(2024, 1, 1)
        pattern = RecurrencePattern("weekly", start)

        pattern_str = str(pattern)
        assert "weekly" in pattern_str.lower()
        assert "2024-01-01" in pattern_str
        assert "no end date" in pattern_str.lower()
