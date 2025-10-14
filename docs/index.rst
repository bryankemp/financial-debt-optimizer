Financial Debt Optimizer Documentation
======================================

Welcome to the comprehensive documentation for Financial Debt Optimizer, a powerful Python tool designed to help you analyze and optimize your debt repayment strategies.

.. image:: https://img.shields.io/pypi/v/financial-debt-optimizer.svg
   :target: https://pypi.org/project/financial-debt-optimizer/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/financial-debt-optimizer.svg
   :target: https://pypi.org/project/financial-debt-optimizer/
   :alt: Python Versions

.. image:: https://img.shields.io/github/license/bryankemp/financial-debt-optimizer.svg
   :target: https://github.com/bryankemp/financial-debt-optimizer/blob/main/LICENSE
   :alt: License

Overview
--------

The Financial Debt Optimizer is a comprehensive tool that helps you:

* **Analyze multiple debt repayment strategies** including debt snowball, avalanche, and custom approaches
* **Import debt data from Excel** files for easy data management
* **Generate detailed financial reports** with payment schedules and projections
* **Create professional visualizations** to understand your debt elimination progress
* **Export results to Excel** with charts and detailed breakdowns

Key Features
------------

🎯 **Multiple Strategy Support**
   Compare debt snowball, avalanche, and hybrid approaches to find the optimal strategy for your situation.

📊 **Rich Visualizations**
   Generate professional charts showing debt reduction progress, interest savings, and payment timelines.

📁 **Excel Integration**
   Import your debt data from Excel and export comprehensive reports with embedded charts.

🧮 **Advanced Calculations**
   Accurate financial modeling with compound interest calculations and payment scheduling.

⚡ **Command Line Interface**
   Easy-to-use CLI for quick debt optimization analysis.

🔧 **Extensible Design**
   Well-structured codebase that can be extended for additional financial calculations.

Quick Start
-----------

1. **Installation**

   .. code-block:: bash
   
      pip install financial-debt-optimizer

2. **Basic Usage**

   .. code-block:: bash
   
      debt-optimizer --input my_debts.xlsx --strategy avalanche --output results.xlsx

3. **Python API**

   .. code-block:: python

   from core.debt_optimizer import DebtOptimizer
   from excel_io.excel_reader import ExcelReader
   
   # Load debt data
   reader = ExcelReader()
   debts = reader.read_debt_data("my_debts.xlsx")
   
   # Optimize debt repayment
   optimizer = DebtOptimizer(debts)
   strategy = optimizer.optimize_debt_avalanche()
   
   # Get results
   total_interest = strategy.get_total_interest()
   payoff_time = strategy.get_payoff_time()

.. toctree::
   :maxdepth: 2
   :caption: User Guide:
   
   installation
   quickstart
   user_guide
   examples
   faq

.. toctree::
   :maxdepth: 2
   :caption: API Reference:
   
   modules

.. toctree::
   :maxdepth: 1
   :caption: Development:
   
   contributing
   changelog
   license

