"""Tests for minimum payment reservation logic.

This module tests the compute_min_payment_reserves function to ensure that
minimum payments are properly reserved even when intermediate incomes are insufficient.
"""

import pytest
from datetime import date
from decimal import Decimal
from debt_optimizer.core.debt_optimizer import compute_min_payment_reserves


class TestMinPaymentReservation:
    """Test cases for minimum payment reservation calculations."""

    def test_november_2025_scenario(self):
        """Test the specific November 2025 Prime Visa scenario.
        
        On Nov 11, we have:
        - Cash on hand: 1523.75
        - Income on Nov 12: 590.00
        - Income on Nov 21: 1492.37
        - Prime Visa due Nov 19: 805.00 minimum
        
        The tool should reserve at least 215.00 (805 - 590) on Nov 11
        to ensure the Nov 19 payment can be made.
        """
        now = date(2025, 11, 11)
        cash_on_hand = Decimal("1523.75")
        
        # Income events after Nov 11
        incomes = [
            {"date": date(2025, 11, 12), "amount": Decimal("590.00")},
            {"date": date(2025, 11, 21), "amount": Decimal("1492.37")},
        ]
        
        # Obligations
        obligations = [
            {
                "debt_name": "Prime Visa",
                "due_date": date(2025, 11, 19),
                "min_amount": Decimal("805.00"),
            },
        ]
        
        total_reserve, per_obligation = compute_min_payment_reserves(
            now=now,
            cash_on_hand=cash_on_hand,
            incomes=incomes,
            obligations=obligations,
        )
        
        # Should reserve at least 215.00 (the shortfall)
        assert total_reserve >= Decimal("215.00")
        assert per_obligation["Prime Visa"] >= Decimal("215.00")
        
        # After reservation, extra payment should be limited
        available_for_extra = cash_on_hand - total_reserve
        assert available_for_extra <= Decimal("1308.75")  # 1523.75 - 215.00

    def test_no_income_before_due_date(self):
        """When there's no income before due date, reserve the full amount."""
        now = date(2025, 11, 1)
        cash_on_hand = Decimal("2000.00")
        
        incomes = [
            {"date": date(2025, 11, 25), "amount": Decimal("1500.00")},
        ]
        
        obligations = [
            {
                "debt_name": "Credit Card",
                "due_date": date(2025, 11, 15),
                "min_amount": Decimal("500.00"),
            },
        ]
        
        total_reserve, per_obligation = compute_min_payment_reserves(
            now=now,
            cash_on_hand=cash_on_hand,
            incomes=incomes,
            obligations=obligations,
        )
        
        # Must reserve full 500.00 since no income arrives before due date
        assert total_reserve == Decimal("500.00")
        assert per_obligation["Credit Card"] == Decimal("500.00")

    def test_income_on_same_day_as_due_date(self):
        """Income on the same day as due date should be counted as available."""
        now = date(2025, 11, 1)
        cash_on_hand = Decimal("100.00")
        
        incomes = [
            {"date": date(2025, 11, 15), "amount": Decimal("2000.00")},
        ]
        
        obligations = [
            {
                "debt_name": "Credit Card",
                "due_date": date(2025, 11, 15),
                "min_amount": Decimal("500.00"),
            },
        ]
        
        total_reserve, per_obligation = compute_min_payment_reserves(
            now=now,
            cash_on_hand=cash_on_hand,
            incomes=incomes,
            obligations=obligations,
        )
        
        # No reservation needed since income on same day covers it
        assert total_reserve == Decimal("0.00")
        assert per_obligation["Credit Card"] == Decimal("0.00")

    def test_multiple_obligations_same_due_date(self):
        """Multiple obligations on the same date should all be reserved."""
        now = date(2025, 11, 1)
        cash_on_hand = Decimal("2000.00")
        
        incomes = [
            {"date": date(2025, 11, 20), "amount": Decimal("1500.00")},
        ]
        
        obligations = [
            {
                "debt_name": "Card A",
                "due_date": date(2025, 11, 15),
                "min_amount": Decimal("300.00"),
            },
            {
                "debt_name": "Card B",
                "due_date": date(2025, 11, 15),
                "min_amount": Decimal("400.00"),
            },
        ]
        
        total_reserve, per_obligation = compute_min_payment_reserves(
            now=now,
            cash_on_hand=cash_on_hand,
            incomes=incomes,
            obligations=obligations,
        )
        
        # Must reserve both obligations (no income before due date)
        assert total_reserve == Decimal("700.00")
        assert per_obligation["Card A"] == Decimal("300.00")
        assert per_obligation["Card B"] == Decimal("400.00")

    def test_sequential_obligations_with_intermediate_income(self):
        """Test multiple obligations with income arriving between them."""
        now = date(2025, 11, 1)
        cash_on_hand = Decimal("500.00")
        
        incomes = [
            {"date": date(2025, 11, 10), "amount": Decimal("1000.00")},
            {"date": date(2025, 11, 20), "amount": Decimal("1000.00")},
        ]
        
        obligations = [
            {
                "debt_name": "Card A",
                "due_date": date(2025, 11, 5),
                "min_amount": Decimal("300.00"),  # Before first income
            },
            {
                "debt_name": "Card B",
                "due_date": date(2025, 11, 15),
                "min_amount": Decimal("800.00"),  # After first income
            },
        ]
        
        total_reserve, per_obligation = compute_min_payment_reserves(
            now=now,
            cash_on_hand=cash_on_hand,
            incomes=incomes,
            obligations=obligations,
        )
        
        # Card A: need all 300, no income before it
        # Card B: by Nov 15, we have 500 + 1000 - 300 = 1200, need 800
        # So no additional reserve for Card B
        assert per_obligation["Card A"] == Decimal("300.00")
        assert per_obligation["Card B"] == Decimal("0.00")
        assert total_reserve == Decimal("300.00")
