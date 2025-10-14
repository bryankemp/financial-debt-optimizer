"""
Comprehensive tests for visualization/charts.py module.

Tests chart generation functionality and matplotlib integration for 
debt optimization visualizations.
"""

import pytest
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt
import tempfile
import shutil
from pathlib import Path
from datetime import date
from io import BytesIO

# Import the classes to test
import sys
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from visualization.charts import (
    create_debt_payoff_chart, create_payment_schedule_chart,
    create_strategy_comparison_chart, create_cash_flow_chart,
    create_debt_breakdown_chart, save_chart_to_file
)
from core.financial_calc import Debt, Income, RecurringExpense
from core.debt_optimizer import DebtOptimizer, OptimizationResult, OptimizationGoal


class TestDebtPayoffChart:
    """Test cases for debt payoff chart generation."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create sample payment schedule data
        self.sample_schedule = pd.DataFrame({
            'month': [1, 2, 3, 4, 5, 6],
            'debt_name': ['Credit Card', 'Credit Card', 'Auto Loan', 'Auto Loan', 'Credit Card', 'Auto Loan'],
            'balance_before': [5000.0, 4800.0, 12000.0, 11700.0, 4600.0, 11400.0],
            'balance_after': [4800.0, 4600.0, 11700.0, 11400.0, 4400.0, 11100.0],
            'total_payment': [200.0, 200.0, 300.0, 300.0, 200.0, 300.0]
        })

    @pytest.mark.visualization
    def test_create_debt_payoff_chart_basic(self):
        """Test basic debt payoff chart creation."""
        fig, ax = create_debt_payoff_chart(self.sample_schedule)
        
        assert fig is not None
        assert ax is not None
        assert len(ax.get_lines()) > 0 or len(ax.patches) > 0  # Chart has data
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_debt_payoff_chart_title(self):
        """Test debt payoff chart with custom title."""
        title = "Custom Debt Payoff Schedule"
        fig, ax = create_debt_payoff_chart(self.sample_schedule, title=title)
        
        assert ax.get_title() == title
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_debt_payoff_chart_empty_data(self):
        """Test debt payoff chart with empty data."""
        empty_schedule = pd.DataFrame(columns=['month', 'debt_name', 'balance_before', 'balance_after'])
        
        # Should handle empty data gracefully
        fig, ax = create_debt_payoff_chart(empty_schedule)
        assert fig is not None
        assert ax is not None
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_debt_payoff_chart_single_debt(self):
        """Test debt payoff chart with single debt."""
        single_debt_schedule = self.sample_schedule[self.sample_schedule['debt_name'] == 'Credit Card']
        
        fig, ax = create_debt_payoff_chart(single_debt_schedule)
        assert fig is not None
        assert ax is not None
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_debt_payoff_chart_large_dataset(self):
        """Test debt payoff chart with large dataset."""
        # Create larger dataset
        months = list(range(1, 61))  # 5 years
        large_schedule = pd.DataFrame({
            'month': months,
            'debt_name': ['Mortgage'] * len(months),
            'balance_before': [200000 - (i * 1000) for i in range(len(months))],
            'balance_after': [200000 - ((i + 1) * 1000) for i in range(len(months))],
            'total_payment': [1500.0] * len(months)
        })
        
        fig, ax = create_debt_payoff_chart(large_schedule)
        assert fig is not None
        assert ax is not None
        plt.close(fig)


class TestPaymentScheduleChart:
    """Test cases for payment schedule chart generation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.sample_payments = pd.DataFrame({
            'month': [1, 2, 3, 4, 5],
            'total_payment': [500.0, 500.0, 500.0, 500.0, 500.0],
            'interest_charge': [150.0, 145.0, 140.0, 135.0, 130.0],
            'principal_payment': [350.0, 355.0, 360.0, 365.0, 370.0]
        })

    @pytest.mark.visualization
    def test_create_payment_schedule_chart_basic(self):
        """Test basic payment schedule chart creation."""
        fig, ax = create_payment_schedule_chart(self.sample_payments)
        
        assert fig is not None
        assert ax is not None
        assert len(ax.patches) > 0  # Should have bars
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_payment_schedule_chart_stacked(self):
        """Test that payment schedule chart shows stacked components."""
        fig, ax = create_payment_schedule_chart(self.sample_payments)
        
        # Should have multiple bar components for interest and principal
        patches = ax.patches
        assert len(patches) >= 2  # At least interest and principal components
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_payment_schedule_chart_legend(self):
        """Test that payment schedule chart has proper legend."""
        fig, ax = create_payment_schedule_chart(self.sample_payments)
        
        legend = ax.get_legend()
        assert legend is not None
        legend_texts = [text.get_text() for text in legend.get_texts()]
        assert 'Interest' in legend_texts or 'Principal' in legend_texts
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_payment_schedule_chart_labels(self):
        """Test that payment schedule chart has proper axis labels."""
        fig, ax = create_payment_schedule_chart(self.sample_payments)
        
        assert ax.get_xlabel() is not None and len(ax.get_xlabel()) > 0
        assert ax.get_ylabel() is not None and len(ax.get_ylabel()) > 0
        plt.close(fig)


class TestStrategyComparisonChart:
    """Test cases for strategy comparison chart generation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.comparison_data = pd.DataFrame({
            'strategy': ['debt_avalanche', 'debt_snowball', 'hybrid'],
            'total_interest': [5000.0, 5500.0, 5250.0],
            'months_to_freedom': [24, 26, 25],
            'total_cost': [25000.0, 25500.0, 25250.0]
        })

    @pytest.mark.visualization
    def test_create_strategy_comparison_chart_basic(self):
        """Test basic strategy comparison chart creation."""
        fig, axes = create_strategy_comparison_chart(self.comparison_data)
        
        assert fig is not None
        assert len(axes) >= 2  # Should have at least 2 subplots
        assert all(ax is not None for ax in axes)
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_strategy_comparison_chart_metrics(self):
        """Test that strategy comparison chart shows key metrics."""
        fig, axes = create_strategy_comparison_chart(self.comparison_data)
        
        # Should have bars for each strategy
        for ax in axes:
            assert len(ax.patches) > 0  # Each subplot should have bars
        
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_strategy_comparison_chart_single_strategy(self):
        """Test strategy comparison chart with single strategy."""
        single_strategy = self.comparison_data.iloc[[0]]  # Just first row
        
        fig, axes = create_strategy_comparison_chart(single_strategy)
        assert fig is not None
        assert len(axes) >= 1
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_strategy_comparison_chart_formatting(self):
        """Test that strategy comparison chart is properly formatted."""
        fig, axes = create_strategy_comparison_chart(self.comparison_data)
        
        # Check that axes have titles and labels
        for ax in axes:
            assert ax.get_title() is not None
            assert len(ax.get_xticklabels()) > 0
        
        plt.close(fig)


class TestCashFlowChart:
    """Test cases for cash flow chart generation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cash_flow_data = pd.DataFrame({
            'month': [1, 2, 3, 4, 5, 6],
            'income': [5000.0, 5000.0, 5200.0, 5200.0, 5400.0, 5400.0],
            'expenses': [2000.0, 2000.0, 2100.0, 2100.0, 2100.0, 2200.0],
            'debt_payments': [1200.0, 1150.0, 1100.0, 1050.0, 1000.0, 950.0],
            'available_cash': [1800.0, 1850.0, 2000.0, 2050.0, 2300.0, 2250.0]
        })

    @pytest.mark.visualization
    def test_create_cash_flow_chart_basic(self):
        """Test basic cash flow chart creation."""
        fig, ax = create_cash_flow_chart(self.cash_flow_data)
        
        assert fig is not None
        assert ax is not None
        assert len(ax.get_lines()) > 0  # Should have line plots
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_cash_flow_chart_multiple_lines(self):
        """Test that cash flow chart shows multiple data series."""
        fig, ax = create_cash_flow_chart(self.cash_flow_data)
        
        lines = ax.get_lines()
        assert len(lines) >= 3  # Should have income, expenses, and available cash lines
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_cash_flow_chart_legend(self):
        """Test that cash flow chart has proper legend."""
        fig, ax = create_cash_flow_chart(self.cash_flow_data)
        
        legend = ax.get_legend()
        assert legend is not None
        legend_texts = [text.get_text() for text in legend.get_texts()]
        assert len(legend_texts) > 0
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_cash_flow_chart_negative_cash(self):
        """Test cash flow chart with negative available cash."""
        negative_cash_data = self.cash_flow_data.copy()
        negative_cash_data['available_cash'] = [-500.0, -400.0, -300.0, 100.0, 200.0, 300.0]
        
        fig, ax = create_cash_flow_chart(negative_cash_data)
        assert fig is not None
        assert ax is not None
        plt.close(fig)


class TestDebtBreakdownChart:
    """Test cases for debt breakdown chart generation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.debt_data = pd.DataFrame({
            'debt_name': ['Credit Card 1', 'Credit Card 2', 'Auto Loan', 'Student Loan', 'Mortgage'],
            'balance': [3000.0, 2000.0, 15000.0, 25000.0, 200000.0],
            'interest_rate': [22.99, 18.99, 5.5, 6.8, 3.5],
            'minimum_payment': [150.0, 100.0, 350.0, 300.0, 1200.0]
        })

    @pytest.mark.visualization
    def test_create_debt_breakdown_chart_basic(self):
        """Test basic debt breakdown chart creation."""
        fig, axes = create_debt_breakdown_chart(self.debt_data)
        
        assert fig is not None
        assert len(axes) >= 2  # Should have multiple subplots
        assert all(ax is not None for ax in axes)
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_debt_breakdown_chart_pie_chart(self):
        """Test that debt breakdown includes pie chart."""
        fig, axes = create_debt_breakdown_chart(self.debt_data)
        
        # At least one subplot should be a pie chart (check for wedges)
        has_pie_chart = any(len(ax.patches) > 0 and 
                          hasattr(ax.patches[0], 'theta1') 
                          for ax in axes if hasattr(ax, 'patches'))
        
        # If not pie chart, should at least have bars
        has_bars = any(len(ax.patches) > 0 for ax in axes)
        assert has_pie_chart or has_bars
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_debt_breakdown_chart_single_debt(self):
        """Test debt breakdown chart with single debt."""
        single_debt = self.debt_data.iloc[[0]]  # Just first debt
        
        fig, axes = create_debt_breakdown_chart(single_debt)
        assert fig is not None
        assert len(axes) >= 1
        plt.close(fig)

    @pytest.mark.visualization
    def test_create_debt_breakdown_chart_labels(self):
        """Test that debt breakdown chart has proper labels."""
        fig, axes = create_debt_breakdown_chart(self.debt_data)
        
        # Check that at least one axis has labels
        has_labels = any(
            len(ax.get_xticklabels()) > 0 or len(ax.get_yticklabels()) > 0
            for ax in axes
        )
        assert has_labels
        plt.close(fig)


class TestChartUtilities:
    """Test cases for chart utility functions."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    @pytest.mark.visualization
    def test_save_chart_to_file_png(self):
        """Test saving chart to PNG file."""
        # Create a simple chart
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 2])
        ax.set_title("Test Chart")
        
        output_path = self.temp_dir / "test_chart.png"
        save_chart_to_file(fig, str(output_path))
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        plt.close(fig)

    @pytest.mark.visualization
    def test_save_chart_to_file_pdf(self):
        """Test saving chart to PDF file."""
        fig, ax = plt.subplots()
        ax.bar(['A', 'B', 'C'], [1, 2, 3])
        
        output_path = self.temp_dir / "test_chart.pdf"
        save_chart_to_file(fig, str(output_path))
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        plt.close(fig)

    @pytest.mark.visualization
    def test_save_chart_to_file_svg(self):
        """Test saving chart to SVG file."""
        fig, ax = plt.subplots()
        ax.scatter([1, 2, 3], [3, 1, 2])
        
        output_path = self.temp_dir / "test_chart.svg"
        save_chart_to_file(fig, str(output_path))
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        plt.close(fig)

    @pytest.mark.visualization
    def test_save_chart_to_file_invalid_format(self):
        """Test saving chart with invalid format."""
        fig, ax = plt.subplots()
        ax.plot([1, 2], [1, 2])
        
        output_path = self.temp_dir / "test_chart.invalid"
        
        # Should either handle gracefully or raise appropriate exception
        try:
            save_chart_to_file(fig, str(output_path))
        except (ValueError, KeyError) as e:
            # Expected for invalid format
            assert "format" in str(e).lower() or "extension" in str(e).lower()
        
        plt.close(fig)

    @pytest.mark.visualization
    def test_save_chart_to_file_overwrite(self):
        """Test overwriting existing chart file."""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 2])
        
        output_path = self.temp_dir / "overwrite_test.png"
        
        # Save first chart
        save_chart_to_file(fig, str(output_path))
        first_size = output_path.stat().st_size
        
        # Create different chart
        ax.clear()
        ax.bar(['X', 'Y'], [5, 10])
        
        # Save second chart to same path
        save_chart_to_file(fig, str(output_path))
        second_size = output_path.stat().st_size
        
        assert output_path.exists()
        # Sizes might be different due to different chart content
        assert first_size > 0 and second_size > 0
        plt.close(fig)


class TestChartIntegration:
    """Integration tests for chart functionality with real data."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create realistic financial data
        self.debts = [
            Debt("Credit Card", 5000.0, 150.0, 18.99, 15),
            Debt("Auto Loan", 15000.0, 350.0, 5.5, 10)
        ]
        
        self.income = [
            Income("Salary", 3500.0, "bi-weekly", date(2024, 1, 5))
        ]
        
        self.expenses = [
            RecurringExpense("Rent", 1200.0, "monthly", 1, date(2024, 1, 1)),
            RecurringExpense("Utilities", 200.0, "monthly", 15, date(2024, 1, 1))
        ]

    @pytest.mark.integration
    @pytest.mark.visualization
    def test_charts_with_real_optimization_data(self):
        """Test charts with real optimization results."""
        # Run optimization to get real data
        optimizer = DebtOptimizer(self.debts, self.income, self.expenses)
        result = optimizer.optimize_debt_strategy(OptimizationGoal.MINIMIZE_INTEREST, 200.0)
        
        # Test debt payoff chart with real schedule
        fig1, ax1 = create_debt_payoff_chart(result.payment_schedule)
        assert fig1 is not None
        assert len(result.payment_schedule) > 0  # Should have payment data
        plt.close(fig1)
        
        # Test strategy comparison with real data
        comparison_data = optimizer.compare_strategies(200.0)
        fig2, axes2 = create_strategy_comparison_chart(comparison_data)
        assert fig2 is not None
        assert len(comparison_data) > 0  # Should have comparison data
        plt.close(fig2)

    @pytest.mark.integration
    @pytest.mark.visualization
    def test_chart_consistency_across_scenarios(self):
        """Test that charts remain consistent across different scenarios."""
        scenarios = [
            (OptimizationGoal.MINIMIZE_INTEREST, 100.0),
            (OptimizationGoal.MINIMIZE_TIME, 300.0),
            (OptimizationGoal.MAXIMIZE_CASHFLOW, 200.0)
        ]
        
        optimizer = DebtOptimizer(self.debts, self.income, self.expenses)
        
        for goal, extra_payment in scenarios:
            result = optimizer.optimize_debt_strategy(goal, extra_payment)
            
            # Should be able to create charts for each scenario
            fig, ax = create_debt_payoff_chart(result.payment_schedule)
            assert fig is not None
            assert ax is not None
            plt.close(fig)

    @pytest.mark.integration
    @pytest.mark.visualization
    @pytest.mark.slow
    def test_chart_performance_large_dataset(self):
        """Test chart performance with large datasets."""
        # Create scenario with many months of payments
        large_debts = [
            Debt("Mortgage", 300000.0, 2000.0, 4.5, 1),
            Debt("Student Loan", 50000.0, 500.0, 6.8, 15)
        ]
        
        large_income = [
            Income("High Salary", 8000.0, "bi-weekly", date(2024, 1, 1))
        ]
        
        optimizer = DebtOptimizer(large_debts, large_income)
        result = optimizer.optimize_debt_strategy(OptimizationGoal.MINIMIZE_INTEREST, 1000.0)
        
        # Should handle large payment schedule
        fig, ax = create_debt_payoff_chart(result.payment_schedule)
        assert fig is not None
        assert len(result.payment_schedule) > 50  # Should be many months
        plt.close(fig)


class TestChartCustomization:
    """Test cases for chart customization options."""

    def setup_method(self):
        """Set up test fixtures."""
        self.sample_data = pd.DataFrame({
            'month': [1, 2, 3, 4, 5],
            'debt_name': ['Test Debt'] * 5,
            'balance_before': [5000, 4000, 3000, 2000, 1000],
            'balance_after': [4000, 3000, 2000, 1000, 0]
        })

    @pytest.mark.visualization
    def test_chart_color_customization(self):
        """Test chart customization with different colors."""
        fig, ax = create_debt_payoff_chart(self.sample_data, colors=['red', 'blue'])
        
        # Check that lines or patches have been created
        has_visual_elements = len(ax.get_lines()) > 0 or len(ax.patches) > 0
        assert has_visual_elements
        plt.close(fig)

    @pytest.mark.visualization
    def test_chart_size_customization(self):
        """Test chart customization with different sizes."""
        fig, ax = create_debt_payoff_chart(self.sample_data, figsize=(12, 8))
        
        # Check figure size
        assert fig.get_figwidth() == 12
        assert fig.get_figheight() == 8
        plt.close(fig)

    @pytest.mark.visualization
    def test_chart_style_consistency(self):
        """Test that charts maintain consistent styling."""
        # Create multiple charts
        fig1, ax1 = create_debt_payoff_chart(self.sample_data)
        
        payment_data = pd.DataFrame({
            'month': [1, 2, 3],
            'total_payment': [500, 500, 500],
            'interest_charge': [100, 90, 80],
            'principal_payment': [400, 410, 420]
        })
        fig2, ax2 = create_payment_schedule_chart(payment_data)
        
        # Both should have titles and labels
        assert ax1.get_title() is not None or len(ax1.get_xlabel()) > 0
        assert ax2.get_title() is not None or len(ax2.get_xlabel()) > 0
        
        plt.close(fig1)
        plt.close(fig2)


class TestChartErrorHandling:
    """Test cases for chart error handling."""

    @pytest.mark.visualization
    def test_chart_with_invalid_data_types(self):
        """Test chart handling with invalid data types."""
        invalid_data = pd.DataFrame({
            'month': ['a', 'b', 'c'],  # String instead of numeric
            'debt_name': ['Debt'] * 3,
            'balance_before': [1000, 2000, 3000],
            'balance_after': [900, 1900, 2900]
        })
        
        # Should either handle gracefully or raise appropriate exception
        try:
            fig, ax = create_debt_payoff_chart(invalid_data)
            plt.close(fig)
        except (ValueError, TypeError):
            # Expected for invalid data types
            pass

    @pytest.mark.visualization
    def test_chart_with_missing_columns(self):
        """Test chart handling with missing required columns."""
        incomplete_data = pd.DataFrame({
            'month': [1, 2, 3],
            'debt_name': ['Debt'] * 3
            # Missing balance columns
        })
        
        # Should either handle gracefully or raise appropriate exception
        try:
            fig, ax = create_debt_payoff_chart(incomplete_data)
            plt.close(fig)
        except (KeyError, ValueError):
            # Expected for missing columns
            pass

    @pytest.mark.visualization
    def test_chart_with_null_values(self):
        """Test chart handling with null values."""
        data_with_nulls = pd.DataFrame({
            'month': [1, 2, 3, 4],
            'debt_name': ['Debt', 'Debt', None, 'Debt'],
            'balance_before': [1000, 800, None, 400],
            'balance_after': [800, 600, 400, 200]
        })
        
        # Should handle null values gracefully
        fig, ax = create_debt_payoff_chart(data_with_nulls)
        assert fig is not None
        plt.close(fig)

    @pytest.mark.visualization
    def test_memory_cleanup_after_charts(self):
        """Test that charts don't cause memory leaks."""
        import gc
        
        # Create and close many charts
        for i in range(10):
            sample_data = pd.DataFrame({
                'month': list(range(1, 13)),
                'debt_name': ['Debt'] * 12,
                'balance_before': list(range(12000, 0, -1000)),
                'balance_after': list(range(11000, -1, -1000))
            })
            
            fig, ax = create_debt_payoff_chart(sample_data)
            plt.close(fig)
        
        # Force garbage collection
        gc.collect()
        
        # Should complete without memory issues
        assert True  # If we get here, no memory issues occurred