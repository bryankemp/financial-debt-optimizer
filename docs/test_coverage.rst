Test Coverage Details
====================

This page provides detailed information about code coverage across all project files.

**Coverage Analysis Generated:** 2025-10-14 01:48:09

**Overall Coverage:** 75.49%

Coverage by File
---------------

.. list-table::
   :header-rows: 1
   :widths: 60 15 15 10

   * - File
     - Statements
     - Missing
     - Coverage %
   * - 🟢 ``debt_optimizer/__init__.py``
     - 0
     - 0
     - 100.0%
   * - 🔴 ``debt_optimizer/__version__.py``
     - 7
     - 7
     - 0.0%
   * - 🟢 ``debt_optimizer/cli/__init__.py``
     - 0
     - 0
     - 100.0%
   * - 🟡 ``debt_optimizer/cli/commands.py``
     - 232
     - 43
     - 81.47%
   * - 🟢 ``debt_optimizer/core/__init__.py``
     - 0
     - 0
     - 100.0%
   * - 🟢 ``debt_optimizer/core/debt_optimizer.py``
     - 536
     - 44
     - 91.79%
   * - 🔴 ``debt_optimizer/core/financial_calc.py``
     - 559
     - 244
     - 56.35%
   * - 🔴 ``debt_optimizer/core/logging_config.py``
     - 28
     - 20
     - 28.57%
   * - 🟡 ``debt_optimizer/core/validation.py``
     - 169
     - 40
     - 76.33%
   * - 🟢 ``debt_optimizer/excel_io/__init__.py``
     - 0
     - 0
     - 100.0%
   * - 🟡 ``debt_optimizer/excel_io/excel_reader.py``
     - 465
     - 93
     - 80.0%
   * - 🟡 ``debt_optimizer/excel_io/excel_writer.py``
     - 734
     - 165
     - 77.52%
   * - 🟢 ``debt_optimizer/visualization/__init__.py``
     - 0
     - 0
     - 100.0%
   * - 🔴 ``debt_optimizer/visualization/charts.py``
     - 232
     - 70
     - 69.83%

**Legend:**

* 🟢 Excellent coverage (≥90%)
* 🟡 Good coverage (75-89%)
* 🔴 Needs improvement (<75%)

Coverage Goals and Recommendations
---------------------------------

**Project Coverage Goals:**

* **Target:** 85% overall coverage
* **Minimum:** 75% for all modules
* **Critical modules:** 95% coverage (core financial calculations)

**Recommendations:**

**Priority Actions:**

* Improve coverage for ``debt_optimizer/__version__.py`` (currently 0.0%)
* Improve coverage for ``debt_optimizer/core/logging_config.py`` (currently 28.57%)
* Improve coverage for ``debt_optimizer/core/financial_calc.py`` (currently 56.35%)
* Improve coverage for ``debt_optimizer/visualization/charts.py`` (currently 69.83%)

**Best Practices:**

* Write tests for all new features before implementation
* Focus on testing edge cases and error conditions
* Ensure financial calculation functions have comprehensive test coverage
* Test CLI commands and Excel I/O operations thoroughly
