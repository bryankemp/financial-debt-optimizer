Quick Start Guide
=================

This guide will help you get started with the Financial Debt Optimizer in just a few minutes.

Prerequisites
-------------

- Python 3.8 or higher installed
- Financial Debt Optimizer package installed (see :doc:`installation`)
- Basic knowledge of your debt information (balances, interest rates, minimum payments)

30-Second Start
---------------

1. **Install the package**::

    pip install financial-debt_optimizer

2. **Run with sample data**::

    debt_optimizer --help

That's it! You now have the Financial Debt Optimizer ready to use.

5-Minute Tutorial
-----------------

Let's walk through a complete debt optimization analysis.

Step 1: Prepare Your Data
~~~~~~~~~~~~~~~~~~~~~~~~~

Create a simple Excel file (``my_debts.xlsx``) with your debt information:

+------------------+---------+-------+----------+
| Name             | Balance | Rate  | Min_Pay  |
+==================+=========+=======+==========+
| Credit Card 1    | 5000    | 18.99 | 150      |
+------------------+---------+-------+----------+
| Credit Card 2    | 3500    | 22.49 | 100      |
+------------------+---------+-------+----------+
| Student Loan     | 25000   | 5.50  | 250      |
+------------------+---------+-------+----------+
| Car Loan         | 15000   | 4.25  | 300      |
+------------------+---------+-------+----------+

**Required Columns:**
- **Name**: Description of the debt
- **Balance**: Current balance owed
- **Rate**: Annual interest rate (as percentage)
- **Min_Pay**: Minimum monthly payment required

Step 2: Run Basic Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~

Compare different debt repayment strategies::

    debt_optimizer --input my_debts.xlsx --strategy avalanche --output results.xlsx

This command will:

- Load your debt data from ``my_debts.xlsx``
- Apply the debt avalanche strategy (pay off highest interest rate first)
- Generate a comprehensive report in ``results.xlsx``

Step 3: View Results
~~~~~~~~~~~~~~~~~~~~

Open ``results.xlsx`` to see:

- **Payment schedule** showing monthly payments and balances
- **Summary statistics** including total interest paid and payoff time
- **Comparison charts** visualizing debt reduction progress
- **Strategy analysis** showing potential savings

Python API Example
------------------

For more control, use the Python API:

.. code-block:: python

    from core.debt_optimizer import DebtOptimizer
    from excel_io.excel_reader import ExcelReader
    from excel_io.excel_writer import ExcelWriter
    
    # Load debt data
    reader = ExcelReader()
    debts = reader.read_debt_data("my_debts.xlsx")
    
    # Create optimizer
    optimizer = DebtOptimizer(debts)
    
    # Compare strategies
    avalanche_strategy = optimizer.optimize_debt_avalanche()
    snowball_strategy = optimizer.optimize_debt_snowball()
    
    # Get key metrics
    avalanche_interest = avalanche_strategy.get_total_interest()
    snowball_interest = snowball_strategy.get_total_interest()
    
    savings = snowball_interest - avalanche_interest
    print(f"Avalanche strategy saves: ${savings:,.2f}")
    
    # Export detailed results
    writer = ExcelWriter("detailed_results.xlsx")
    writer.write_strategy_comparison([avalanche_strategy, snowball_strategy])

Available Strategies
--------------------

The Financial Debt Optimizer supports several debt repayment strategies:

**Debt Avalanche** (``--strategy avalanche``)
    Pay minimums on all debts, put extra toward highest interest rate debt first.
    - **Pros**: Minimizes total interest paid
    - **Best for**: Mathematically optimal approach

**Debt Snowball** (``--strategy snowball``)
    Pay minimums on all debts, put extra toward lowest balance debt first.
    - **Pros**: Provides quick psychological wins
    - **Best for**: Building momentum and motivation

**Hybrid Approach** (``--strategy hybrid``)
    Combines elements of both avalanche and snowball strategies.
    - **Pros**: Balances math and psychology
    - **Best for**: Most people seeking a practical approach

Command Line Options
--------------------

Common command-line options:

**Basic Usage**::

    debt_optimizer --input FILE --strategy STRATEGY --output FILE

**Advanced Options**::

    debt_optimizer \\
        --input my_debts.xlsx \\
        --strategy avalanche \\
        --output results.xlsx \\
        --extra-payment 200 \\
        --charts

**Available Flags:**

- ``--input FILE``: Input Excel file with debt data
- ``--output FILE``: Output Excel file for results
- ``--strategy STRATEGY``: Choose from avalanche, snowball, or hybrid
- ``--extra-payment AMOUNT``: Additional monthly payment amount
- ``--charts``: Generate visualization charts
- ``--verbose``: Show detailed progress information
- ``--help``: Show all available options

Next Steps
----------

Now that you've completed the quick start:

1. **Read the full** :doc:`user_guide` **for advanced features**
2. **Check out** :doc:`examples` **for more complex scenarios**
3. **Explore the** :doc:`modules` **for API documentation**
4. **See** :doc:`faq` **for common questions**

Common Use Cases
----------------

**"I want to pay off debt as quickly as possible"**
    Use the avalanche strategy with extra payments::

        debt_optimizer --input debts.xlsx --strategy avalanche --extra-payment 500

**"I need motivation to stick with debt repayment"**
    Use the snowball strategy to build momentum::

        debt_optimizer --input debts.xlsx --strategy snowball --charts

**"I want to see all options before deciding"**
    Generate a comprehensive comparison::

        debt_optimizer --input debts.xlsx --strategy hybrid --output comparison.xlsx

**"I want to integrate with my own Python code"**
    Use the Python API for custom analysis and integration with other financial tools.

Troubleshooting Quick Issues
----------------------------

**"Command not found: debt_optimizer"**
    Make sure you've installed the package and it's in your PATH. Try::

        python -m pip show financial-debt_optimizer

**"File not found error"**
    Ensure your Excel file exists and has the correct column names (Name, Balance, Rate, Min_Pay).

**"Invalid strategy"**
    Use one of: ``avalanche``, ``snowball``, or ``hybrid``.

**"Permission denied"**
    Make sure you have write permissions in the output directory and the output Excel file isn't open in another program.

For more help, see the :doc:`installation` and :doc:`faq` sections.