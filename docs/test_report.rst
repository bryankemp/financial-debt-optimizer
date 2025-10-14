Test Reports
============

This page provides an overview of the test suite results and code coverage for the Financial Debt Optimizer.

**Report Generated:** 2025-10-14 01:41:01

Test Results Summary
-------------------

.. list-table::
   :header-rows: 1
   :widths: 30 15 15 15 15 10

   * - Metric
     - Total Tests
     - Passed
     - Failed
     - Skipped
     - Success Rate
   * - Results
     - 167
     - 167
     - 0
     - 0
     - 100.0%

**Test Execution Time:** 6.80 seconds

Code Coverage Summary
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 15 15

   * - Metric
     - Total Lines
     - Covered Lines
     - Missing Lines
     - Coverage %
     - Files Analyzed
   * - Coverage
     - 2962
     - 2236
     - 726
     - 75.49%
     - 14

Files Needing Attention (Lowest Coverage)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 50 15 15 20

   * - File
     - Statements
     - Missing
     - Coverage %
   * - ``src/__version__.py``
     - 7
     - 7
     - 0.0%
   * - ``src/core/logging_config.py``
     - 28
     - 20
     - 28.57%
   * - ``src/core/financial_calc.py``
     - 559
     - 244
     - 56.35%
   * - ``src/visualization/charts.py``
     - 232
     - 70
     - 69.83%
   * - ``src/core/validation.py``
     - 169
     - 40
     - 76.33%
   * - ``src/excel_io/excel_writer.py``
     - 734
     - 165
     - 77.52%
   * - ``src/excel_io/excel_reader.py``
     - 465
     - 93
     - 80.0%
   * - ``src/cli/commands.py``
     - 232
     - 43
     - 81.47%
   * - ``src/core/debt_optimizer.py``
     - 536
     - 44
     - 91.79%
   * - ``src/__init__.py``
     - 0
     - 0
     - 100.0%

Detailed Reports
---------------

* :doc:`test_coverage` - Detailed code coverage analysis
* `Interactive Coverage Report <_static/test_reports/coverage_html/index.html>`_ - Browse coverage by file

.. note::
   Test reports are automatically generated during the documentation build process.
   The interactive coverage report provides line-by-line coverage information.
