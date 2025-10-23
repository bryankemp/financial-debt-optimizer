#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from src.excel_io.excel_reader import ExcelReader
from src.core.debt_optimizer import DebtOptimizer, OptimizationGoal

try:
    reader = ExcelReader('default.xlsx')
    debts, income_sources, recurring_expenses, future_income, future_expenses, settings = reader.read_all_data()
    
    print(f"Read {len(debts)} debts, {len(income_sources)} income sources")
    
    optimizer = DebtOptimizer(
        debts=debts,
        income_sources=income_sources,
        recurring_expenses=recurring_expenses,
        future_income=future_income,
        future_expenses=future_expenses,
        settings=settings,
    )
    
    debt_summary = optimizer.generate_debt_summary()
    print("Generated debt summary successfully")
    print(f"Total debt: {debt_summary['total_debt']}")
    
    result = optimizer.optimize_debt_strategy(
        goal=OptimizationGoal.MINIMIZE_INTEREST,
        extra_payment=settings.get('extra_payment', 0.0)
    )
    
    print(f"Optimization successful! Strategy: {result.strategy}")
    
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
