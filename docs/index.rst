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

The Financial Debt Optimizer is a comprehensive, battle-tested tool that helps you:

* **Analyze multiple debt repayment strategies** including debt avalanche, snowball, and hybrid approaches
* **Import and validate financial data** from Excel files with robust error handling
* **Generate detailed financial reports** with comprehensive payment schedules and projections
* **Create professional visualizations** to track your debt elimination progress
* **Export results to Excel** with embedded charts and detailed financial analysis
* **Command-line interface** for quick analysis and automation
* **Python API** for programmatic integration and custom workflows

Key Features
------------

🎯 **Multiple Strategy Support**
   Compare debt avalanche, snowball, and hybrid approaches with comprehensive strategy comparison analysis.

📊 **Rich Visualizations**
   Generate professional charts showing debt reduction progress, interest savings, payment timelines, and cash flow projections.

📁 **Excel Integration**
   Robust Excel import/export with template generation, data validation, and comprehensive report creation.

🧮 **Advanced Financial Modeling**
   Accurate calculations with compound interest, payment scheduling, future income/expenses, and cash flow optimization.

⚡ **Command Line Interface**
   Full-featured CLI with template generation, validation, analysis, and reporting capabilities.

🔧 **Extensible Architecture**
   Well-structured, thoroughly tested codebase with comprehensive validation and error handling.

🛡️ **Robust Validation**
   Comprehensive data validation for debts, income, expenses, and financial scenarios.

📈 **Performance Optimized**
   Handles large datasets efficiently with optimized algorithms and memory management.

🧪 **Thoroughly Tested**
   167 comprehensive tests ensuring reliability and correctness of all financial calculations.

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

      from core.debt_optimizer import DebtOptimizer, OptimizationGoal
      from excel_io.excel_reader import ExcelReader
      from excel_io.excel_writer import ExcelReportWriter
      
      # Load debt data from Excel
      reader = ExcelReader("my_debts.xlsx")
      debts, income, expenses, _, _, settings = reader.read_all_data()
      
      # Create optimizer
      optimizer = DebtOptimizer(debts, income, expenses)
      
      # Run optimization
      result = optimizer.optimize_debt_strategy(
          OptimizationGoal.MINIMIZE_INTEREST, extra_payment=200.0
      )
      
      # Generate comprehensive report
      debt_summary = optimizer.generate_debt_summary()
      writer = ExcelReportWriter("debt_analysis_report.xlsx")
      writer.create_comprehensive_report(result, debt_summary)

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
   
   api/modules

.. toctree::
   :maxdepth: 1
   :caption: Quality Assurance:
   
   test_report
   test_coverage

.. toctree::
   :maxdepth: 1
   :caption: Development:
   
   contributing
   testing
   changelog
   license

