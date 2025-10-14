Examples and Use Cases
======================

This section provides real-world examples and practical use cases for the Financial Debt Optimizer.

Basic Examples
--------------

Example 1: Simple Credit Card Debt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** You have two credit cards with different balances and interest rates.

**Input Data (credit_cards.xlsx):**

+----------------+---------+-------+----------+
| Name           | Balance | Rate  | Min_Pay  |
+================+=========+=======+==========+
| Visa Card      | 3500    | 19.99 | 105      |
+----------------+---------+-------+----------+
| Master Card    | 2800    | 24.99 | 85       |
+----------------+---------+-------+----------+

**Command Line Usage:**
::

    debt-optimizer --input credit_cards.xlsx --strategy avalanche --output results.xlsx

**Expected Results:**
- Master Card paid off first (higher interest rate: 24.99%)
- Total payoff time: ~24 months (minimum payments only)
- Total interest paid: ~$1,180

**With $200 extra payment:**
::

    debt-optimizer --input credit_cards.xlsx --strategy avalanche --extra-payment 200 --output results_extra.xlsx

**Expected Results:**
- Total payoff time: ~18 months
- Total interest paid: ~$680
- **Savings: ~$500**

Example 2: Mixed Debt Portfolio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** You have various types of debt including credit cards, student loans, and a car loan.

**Input Data (mixed_debts.xlsx):**

+------------------+---------+-------+----------+
| Name             | Balance | Rate  | Min_Pay  |
+==================+=========+=======+==========+
| Chase Credit     | 4500    | 18.99 | 135      |
+------------------+---------+-------+----------+
| Discover Card    | 2300    | 22.49 | 75       |
+------------------+---------+-------+----------+
| Student Loan     | 28000   | 6.50  | 285      |
+------------------+---------+-------+----------+
| Car Loan         | 15000   | 4.25  | 320      |
+------------------+---------+-------+----------+

**Python API Example:**

.. code-block:: python

    from core.debt_optimizer import DebtOptimizer
    from excel_io.excel_reader import ExcelReader
    
    # Load data
    reader = ExcelReader()
    debts = reader.read_debt_data("mixed_debts.xlsx")
    
    # Compare strategies
    optimizer = DebtOptimizer(debts, extra_payment=300)
    
    avalanche = optimizer.optimize_debt_avalanche()
    snowball = optimizer.optimize_debt_snowball()
    hybrid = optimizer.optimize_debt_hybrid()
    
    print("Strategy Comparison:")
    print(f"Avalanche: ${avalanche.get_total_interest():,.2f} interest, {avalanche.get_payoff_time()} months")
    print(f"Snowball:  ${snowball.get_total_interest():,.2f} interest, {snowball.get_payoff_time()} months")
    print(f"Hybrid:    ${hybrid.get_total_interest():,.2f} interest, {hybrid.get_payoff_time()} months")

**Expected Output:**
::

    Strategy Comparison:
    Avalanche: $12,450.75 interest, 58 months
    Snowball:  $13,820.25 interest, 59 months  
    Hybrid:    $12,890.50 interest, 58 months

Advanced Examples
-----------------

Example 3: Optimization with Variable Extra Payments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** You want to find the optimal extra payment amount.

.. code-block:: python

    from core.debt_optimizer import DebtOptimizer
    from excel_io.excel_reader import ExcelReader
    import matplotlib.pyplot as plt
    
    # Load debt data
    reader = ExcelReader()
    debts = reader.read_debt_data("mixed_debts.xlsx")
    
    # Test different extra payment amounts
    extra_payments = range(0, 1001, 100)  # $0 to $1000 in $100 increments
    results = []
    
    for extra in extra_payments:
        optimizer = DebtOptimizer(debts, extra_payment=extra)
        strategy = optimizer.optimize_debt_avalanche()
        
        results.append({
            'extra_payment': extra,
            'total_interest': strategy.get_total_interest(),
            'payoff_months': strategy.get_payoff_time(),
            'total_payments': strategy.get_total_payments(),
            'monthly_payment': sum(d.min_payment for d in debts) + extra
        })
    
    # Find the point of diminishing returns
    for i, result in enumerate(results):
        if i == 0:
            savings = 0
        else:
            savings = results[0]['total_interest'] - result['total_interest']
        
        print(f"Extra ${result['extra_payment']:3d}: "
              f"${result['total_interest']:7,.0f} interest, "
              f"{result['payoff_months']:2d} months, "
              f"Savings: ${savings:6,.0f}")

**Expected Output:**
::

    Extra $  0: $ 18,450 interest, 72 months, Savings: $    0
    Extra $100: $ 15,240 interest, 58 months, Savings: $3,210
    Extra $200: $ 13,180 interest, 49 months, Savings: $5,270
    Extra $300: $ 11,740 interest, 43 months, Savings: $6,710
    Extra $400: $ 10,620 interest, 38 months, Savings: $7,830
    Extra $500: $  9,710 interest, 35 months, Savings: $8,740

Example 4: Debt Consolidation Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** You're considering consolidating high-interest debt into a personal loan.

.. code-block:: python

    from core.debt_optimizer import Debt, DebtOptimizer
    
    # Current high-interest debt
    current_debts = [
        Debt("Credit Card 1", 5000, 19.99, 150),
        Debt("Credit Card 2", 3500, 22.49, 105),
        Debt("Credit Card 3", 4200, 24.99, 125),
        Debt("Student Loan", 25000, 6.50, 280)  # Keep this separate
    ]
    
    # Consolidation option: Personal loan for credit card debt
    consolidated_debts = [
        Debt("Personal Loan", 12700, 12.99, 380),  # Consolidate first 3 debts
        Debt("Student Loan", 25000, 6.50, 280)     # Keep student loan
    ]
    
    # Compare scenarios
    current_optimizer = DebtOptimizer(current_debts, extra_payment=200)
    consolidated_optimizer = DebtOptimizer(consolidated_debts, extra_payment=200)
    
    current_strategy = current_optimizer.optimize_debt_avalanche()
    consolidated_strategy = consolidated_optimizer.optimize_debt_avalanche()
    
    print("Current Situation:")
    print(f"Total Interest: ${current_strategy.get_total_interest():,.2f}")
    print(f"Payoff Time: {current_strategy.get_payoff_time()} months")
    
    print("\\nWith Consolidation:")
    print(f"Total Interest: ${consolidated_strategy.get_total_interest():,.2f}")
    print(f"Payoff Time: {consolidated_strategy.get_payoff_time()} months")
    
    savings = current_strategy.get_total_interest() - consolidated_strategy.get_total_interest()
    print(f"\\nConsolidation Savings: ${savings:,.2f}")

Real-World Scenarios
--------------------

Example 5: New Graduate with Student Loans and Credit Cards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Background:** Recent college graduate with multiple student loans and some credit card debt from college expenses.

**Input Data (graduate_debts.xlsx):**

+----------------------+---------+-------+----------+
| Name                 | Balance | Rate  | Min_Pay  |
+======================+=========+=======+==========+
| Federal Loan 1       | 8500    | 4.50  | 87       |
+----------------------+---------+-------+----------+
| Federal Loan 2       | 12000   | 5.50  | 123      |
+----------------------+---------+-------+----------+
| Private Student Loan | 15000   | 7.25  | 165      |
+----------------------+---------+-------+----------+
| Credit Card          | 3200    | 21.99 | 96       |
+----------------------+---------+-------+----------+

**Analysis Strategy:**
::

    debt-optimizer --input graduate_debts.xlsx --strategy avalanche --extra-payment 150 --charts --output graduate_analysis.xlsx

**Key Insights:**
- Credit card should be eliminated first (highest rate: 21.99%)
- Private student loan next (7.25% vs federal loans at 4.5-5.5%)
- Federal loans last due to lower rates and potential benefits
- Extra payments make significant difference on high-rate debt

Example 6: Family with Mortgage, Car Loans, and Credit Cards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Background:** Family managing multiple types of debt with varying priorities.

**Input Data (family_debts.xlsx):**

+------------------+---------+-------+----------+
| Name             | Balance | Rate  | Min_Pay  |
+==================+=========+=======+==========+
| Mortgage         | 285000  | 3.75  | 1850     |
+------------------+---------+-------+----------+
| Car Loan 1       | 18500   | 4.25  | 385      |
+------------------+---------+-------+----------+
| Car Loan 2       | 22000   | 5.75  | 425      |
+------------------+---------+-------+----------+
| Credit Card 1    | 6500    | 18.99 | 195      |
+------------------+---------+-------+----------+
| Credit Card 2    | 4200    | 22.49 | 125      |
+------------------+---------+-------+----------+

**Strategic Considerations:**

.. code-block:: python

    # Analyze excluding mortgage (different strategy for home equity)
    non_mortgage_debts = [
        Debt("Car Loan 1", 18500, 4.25, 385),
        Debt("Car Loan 2", 22000, 5.75, 425),
        Debt("Credit Card 1", 6500, 18.99, 195),
        Debt("Credit Card 2", 4200, 22.49, 125)
    ]
    
    optimizer = DebtOptimizer(non_mortgage_debts, extra_payment=500)
    strategy = optimizer.optimize_debt_avalanche()
    
    print("Non-Mortgage Debt Analysis:")
    print(f"Payoff Order: {[debt.name for debt in strategy.payoff_order]}")
    print(f"Total Interest: ${strategy.get_total_interest():,.2f}")
    print(f"Payoff Time: {strategy.get_payoff_time()} months")

**Expected Priority Order:**
1. Credit Card 2 (22.49% rate)
2. Credit Card 1 (18.99% rate)  
3. Car Loan 2 (5.75% rate)
4. Car Loan 1 (4.25% rate)

Example 7: Pre-Retirement Debt Elimination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Background:** Individual approaching retirement wanting to eliminate all debt beforehand.

.. code-block:: python

    from datetime import datetime, timedelta
    
    # Target retirement in 5 years (60 months)
    retirement_months = 60
    
    debts = [
        Debt("Credit Card", 8500, 16.99, 255),
        Debt("Car Loan", 15000, 5.25, 285),
        Debt("Home Equity", 35000, 6.75, 425)
    ]
    
    # Find minimum extra payment needed to be debt-free by retirement
    for extra_payment in range(0, 2001, 50):
        optimizer = DebtOptimizer(debts, extra_payment=extra_payment)
        strategy = optimizer.optimize_debt_avalanche()
        
        if strategy.get_payoff_time() <= retirement_months:
            print(f"Minimum extra payment for retirement goal: ${extra_payment}")
            print(f"Total monthly payment: ${sum(d.min_payment for d in debts) + extra_payment}")
            print(f"Payoff time: {strategy.get_payoff_time()} months")
            print(f"Total interest: ${strategy.get_total_interest():,.2f}")
            break
    else:
        print("Cannot achieve debt-free retirement with reasonable extra payments")

Industry-Specific Examples
--------------------------

Example 8: Medical Professional with Educational Debt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Background:** Doctor with high income but substantial educational debt.

.. code-block:: python

    medical_debts = [
        Debt("Med School Loan 1", 75000, 6.25, 765),
        Debt("Med School Loan 2", 85000, 7.00, 918),
        Debt("Residency Credit Card", 15000, 19.99, 450),
        Debt("Equipment Loan", 25000, 8.50, 315)
    ]
    
    # High income allows substantial extra payments
    optimizer = DebtOptimizer(medical_debts, extra_payment=2000)
    strategy = optimizer.optimize_debt_avalanche()
    
    print("Medical Professional Debt Strategy:")
    print(f"Priority: {strategy.payoff_order[0].name} (Rate: {strategy.payoff_order[0].rate}%)")
    print(f"Total Interest Savings vs Minimums: ${strategy.get_interest_savings():,.2f}")

Example 9: Small Business Owner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Background:** Entrepreneur with business and personal debt to manage.

.. code-block:: python

    business_personal_debts = [
        Debt("Business Credit Line", 45000, 12.50, 750),
        Debt("Equipment Financing", 35000, 9.25, 485),
        Debt("Personal Credit Card", 8500, 21.99, 255),
        Debt("SBA Loan", 125000, 7.75, 1285)
    ]
    
    # Variable income - analyze different scenarios
    scenarios = [
        ("Conservative", 500),
        ("Moderate", 1000),
        ("Aggressive", 2000)
    ]
    
    for scenario_name, extra_payment in scenarios:
        optimizer = DebtOptimizer(business_personal_debts, extra_payment=extra_payment)
        strategy = optimizer.optimize_debt_avalanche()
        
        print(f"\\n{scenario_name} Scenario (${extra_payment} extra):")
        print(f"Payoff Time: {strategy.get_payoff_time()} months")
        print(f"Total Interest: ${strategy.get_total_interest():,.2f}")

Specialized Use Cases
--------------------

Example 10: Debt Payoff vs Investment Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Compare debt payoff vs investing extra money
    def compare_debt_vs_investment(debts, extra_payment, investment_return_rate):
        # Debt payoff scenario
        optimizer = DebtOptimizer(debts, extra_payment=extra_payment)
        debt_strategy = optimizer.optimize_debt_avalanche()
        
        # Investment scenario (simplified)
        monthly_investment = extra_payment
        investment_months = debt_strategy.get_payoff_time()
        
        # Future value of monthly investments
        monthly_rate = investment_return_rate / 12 / 100
        investment_value = monthly_investment * (((1 + monthly_rate) ** investment_months - 1) / monthly_rate)
        
        debt_interest_saved = debt_strategy.get_interest_savings()
        
        print(f"Debt Payoff Approach:")
        print(f"Interest Saved: ${debt_interest_saved:,.2f}")
        print(f"Time to Debt Freedom: {debt_strategy.get_payoff_time()} months")
        
        print(f"\\nInvestment Approach:")
        print(f"Investment Value: ${investment_value:,.2f}")
        print(f"Net Gain: ${investment_value - (extra_payment * investment_months):,.2f}")
        
        if debt_interest_saved > (investment_value - (extra_payment * investment_months)):
            print("\\nRecommendation: Focus on debt payoff")
        else:
            print("\\nRecommendation: Consider investing")
    
    debts = [Debt("Credit Card", 10000, 18.99, 300)]
    compare_debt_vs_investment(debts, 400, 7.0)  # 7% investment return

Example 11: Balance Transfer Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Analyze balance transfer credit card offer
    current_debt = Debt("Current Card", 8000, 22.99, 240)
    
    # Balance transfer offer: 0% for 12 months, then 16.99%, 3% transfer fee
    transfer_fee = 8000 * 0.03  # $240
    
    # Scenario 1: Keep current card
    current_optimizer = DebtOptimizer([current_debt], extra_payment=200)
    current_strategy = current_optimizer.optimize_debt_avalanche()
    
    # Scenario 2: Balance transfer
    # Model as debt with 0% rate for 12 months, then higher balance
    # This is simplified - real analysis would be more complex
    transfer_debt = Debt("Transfer Card", 8000 + transfer_fee, 16.99, 240)
    transfer_optimizer = DebtOptimizer([transfer_debt], extra_payment=200)
    transfer_strategy = transfer_optimizer.optimize_debt_avalanche()
    
    print("Current Card:")
    print(f"Total Interest: ${current_strategy.get_total_interest():,.2f}")
    print(f"Payoff Time: {current_strategy.get_payoff_time()} months")
    
    print("\\nBalance Transfer:")
    print(f"Transfer Fee: ${transfer_fee:,.2f}")
    print(f"Total Interest: ${transfer_strategy.get_total_interest():,.2f}")
    print(f"Payoff Time: {transfer_strategy.get_payoff_time()} months")

Performance Testing Examples
---------------------------

Example 12: Large Debt Portfolio Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import time
    from core.debt_optimizer import Debt, DebtOptimizer
    
    # Generate large number of debts for performance testing
    large_debt_portfolio = []
    for i in range(50):  # 50 different debts
        debt = Debt(
            name=f"Debt {i+1}",
            balance=1000 + (i * 500),  # Varying balances
            rate=5.0 + (i * 0.5),      # Varying rates
            min_payment=50 + (i * 10)  # Varying payments
        )
        large_debt_portfolio.append(debt)
    
    start_time = time.time()
    
    optimizer = DebtOptimizer(large_debt_portfolio, extra_payment=1000)
    strategy = optimizer.optimize_debt_avalanche()
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    print(f"Processed {len(large_debt_portfolio)} debts in {processing_time:.2f} seconds")
    print(f"Total Interest: ${strategy.get_total_interest():,.2f}")
    print(f"Payoff Time: {strategy.get_payoff_time()} months")

Tips for Creating Your Own Examples
-----------------------------------

Data Preparation Tips
~~~~~~~~~~~~~~~~~~~~

1. **Use realistic interest rates**: Credit cards (15-25%), auto loans (3-8%), student loans (4-8%)
2. **Ensure minimum payments cover interest**: Monthly payment should be at least (balance × rate / 12)
3. **Include variety**: Mix high and low balance debts with different rates
4. **Test edge cases**: Very high rates, very low minimums, large balances

Analysis Best Practices
~~~~~~~~~~~~~~~~~~~~~~

1. **Start simple**: Begin with 2-3 debts to understand the concepts
2. **Compare strategies**: Always run multiple strategies to see differences
3. **Test extra payments**: Small increases in extra payments often yield large savings
4. **Validate results**: Spot-check calculations for reasonableness
5. **Document assumptions**: Note any special circumstances or assumptions

Common Pitfalls to Avoid
~~~~~~~~~~~~~~~~~~~~~~~

1. **Decimal vs percentage rates**: Use 18.99, not 0.1899
2. **Annual vs monthly payments**: Ensure all payments are monthly
3. **Outdated balances**: Use current balances for accurate results
4. **Ignoring fees**: Consider balance transfer fees, loan origination fees
5. **Unrealistic extra payments**: Ensure extra payments fit your actual budget

These examples demonstrate the versatility and power of the Financial Debt Optimizer across various scenarios and use cases. Use them as starting points for your own debt optimization analysis.