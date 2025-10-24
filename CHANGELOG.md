# Changelog

All notable changes to the Financial Debt Optimizer project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2025-10-24

### 🐛 Bug Fixes
- Fixed all mypy type errors (List, Tuple imports, type annotations)
- Fixed Windows file handle issues in logging tests
- Fixed all black formatting issues
- Fixed ReadTheDocs documentation configuration
- Fixed setup.py package discovery issue

### ✅ Test Coverage Improvements
- **Increased test coverage from 70% to 74.46%**
- Added 88 new tests (167 → 255 total tests)
- New comprehensive test modules:
  - `test_config.py` - Full Config class coverage (37% → 95%)
  - `test_logging_config.py` - Complete logging setup testing (54% → 100%)
  - `test_version.py` - Version metadata testing (0% → 100%)
- Enhanced `test_financial_calc.py` with 83 additional tests:
  - Debt class validation and calculation methods
  - Income validation tests
  - RecurrencePattern tests for all 9 frequencies
  - FutureExpense and PaymentFrequency enum tests

### 📊 Coverage by Module
- **config.py**: 37% → 95%
- **logging_config.py**: 54% → 100%
- **__version__.py**: 0% → 100%
- **financial_calc.py**: 56% → 72%
- **Overall**: 70% → 74.46%

### 🔧 Technical Improvements
- Cross-platform compatibility fixes for Windows file handling
- Improved type safety with comprehensive mypy coverage
- Better test infrastructure with proper teardown handling
- Updated GitHub Actions to v4 artifact upload (v3 deprecated)
- Added HTML coverage report uploads to GitHub Actions artifacts
- Enhanced documentation with corrected ReadTheDocs configuration

### 📖 Documentation
- Fixed ReadTheDocs URLs (changed mixed dash/underscore to all dashes)
- Updated documentation version to 2.0.1
- Fixed API documentation generation path
- Added Codecov and GitHub Actions badges to README
- Disabled test report generation in ReadTheDocs (reports available via GitHub)

## [2.0.0] - 2025-10-23

### 🎉 Major Release - Complete Integration & Optimization

### Added
- **Quicken Database Integration**: Direct balance syncing from Quicken SQLite databases
  - New `update-balances` CLI command for standalone balance updates
  - `-u/--update-balances` flag in `analyze` command for automatic sync before analysis
  - Fuzzy matching support with configurable threshold for account name matching
  - Automatic backup creation before balance updates
  - Support for both rapidfuzz and thefuzz fuzzy matching libraries
  
- **Configuration System**: YAML-based configuration management
  - `config init` command to create default configuration files
  - `config show` command to view current settings
  - `config get/set` commands for individual setting management
  - Multiple config file locations: `~/.debt_optimizer/config.yaml`, `./debt_optimizer.yaml`
  - Environment variable overrides with `DEBT_OPTIMIZER_*` prefix
  - CLI arguments always take precedence over config file settings

- **Enhanced Balance Updater**:
  - Updates both Debts sheet (credit cards) and Settings sheet (bank balance)
  - Exact and fuzzy matching for account names
  - Interactive prompts for uncertain matches
  - Only updates balances when they actually change (prevents unnecessary updates)
  - Comprehensive update summaries with row numbers and old/new values

### Changed
- **Surplus Calculation Fix**: Now correctly includes expenses in monthly surplus calculation
  - Previous: `surplus = income - payment`
  - Current: `surplus = income - expenses - payment`
  - Fixes negative surplus displays when using bank balance or extra payments
  
- **Workbook Sheet Access**: Fixed openpyxl compatibility issue
  - Changed from `wb.get("Settings")` to proper `wb["Settings"] if "Settings" in wb.sheetnames else None`
  - Eliminates AttributeError on Workbook objects

- **File Overwrite Prompts**: Now displays actual file path instead of "None"
  - Fixed variable reference to use resolved `output_path` instead of raw `output` parameter

### Removed
- Deprecated `update_balances.py` standalone script (functionality now integrated)
- Deprecated `debug_optimizer.py` debug script
- Removed `INTEGRATION_COMPLETE.md` and `INTEGRATION_PROGRESS.md` (obsolete documentation)

### Fixed
- **Balance Update Logic**: Balances only update when changed, not on every run
  - Prevents duplicate update reports for unchanged data
  - Reduces workbook modifications and backup file creation
  - Smarter detection of actual changes vs. matching existing values
  
- **Workbook AttributeError**: Fixed "'Workbook' object has no attribute 'get'" error
  - Proper openpyxl sheet access patterns throughout codebase
  
- **Monthly Surplus Display**: Fixed negative surplus in month 3 and other months
  - Surplus now correctly accounts for all expenses before calculating available cash flow
  - Charts and reports now show accurate cash flow after all obligations

### Technical Improvements
- Enhanced error handling for missing Quicken databases
- Better validation of configuration file settings
- Improved user feedback during balance updates and analysis
- More consistent CLI command structure
- Added comprehensive docstrings to new modules

### Dependencies
- Added `pyyaml>=6.0` for configuration file support
- Added optional `rapidfuzz>=3.0.0` for balance updates (install with `pip install debt_optimizer[balance]`)
- All dependencies updated to modern versions with proper version constraints
## [1.1.1] - 2025-01-14

### Fixed
- **Resolved all Sphinx documentation warnings** for clean builds
- **Fixed unsupported theme options** in Read the Docs configuration
- **Improved autodoc configuration** to handle imports gracefully
- **Regenerated API documentation** with proper module structure
- **Enhanced documentation build reliability** for CI/CD pipelines

### Technical
- Removed unsupported `display_version` theme option
- Added proper autodoc mock imports for dependencies
- Configured Sphinx to suppress import warnings appropriately
- Regenerated all API documentation files with correct structure

## [1.1.0] - 2025-01-14

### Added
- **Complete Sphinx documentation system** with professional RTD theme
- **Read the Docs integration** with automated documentation builds
- **Comprehensive user guide** with real-world examples and use cases
- **Installation guide** with multiple installation methods and troubleshooting
- **Quick start tutorial** to get users productive in minutes
- **Extensive examples collection** covering basic to advanced scenarios
- **FAQ section** addressing common questions and issues
- **API reference documentation** with detailed docstrings
- **Contributing guide** for developers and contributors
- **Changelog and license documentation** for transparency

### Improved
- **Enhanced documentation structure** with professional navigation
- **Better code organization** with cleaner module imports
- **Improved error messages** and validation feedback
- **Professional documentation theme** with search functionality
- **Cross-platform compatibility** documentation
- **Development workflow** documentation

### Documentation Features
- Professional Sphinx-generated documentation
- Read the Docs hosting with automatic builds
- Multiple output formats (HTML, PDF, ePub)
- Comprehensive API documentation with type hints
- Real-world examples for various financial scenarios
- Troubleshooting guides and FAQ section
- Contributing guidelines for open source collaboration
- Professional documentation theme with search

### Technical
- Added Sphinx documentation framework
- Configured Read the Docs integration
- Enhanced project metadata and packaging
- Improved code documentation and docstrings
- Added documentation build automation

## [1.0.0] - 2025-01-14

### Added
- **Complete debt optimization engine** with multiple strategies (Avalanche, Snowball, Hybrid)
- **Excel integration** for input templates and comprehensive reporting
- **Advanced financial modeling** including future income and recurring expenses
- **Professional charts and visualizations** with 6 different chart types
- **Decision logging system** for audit trails and rationale tracking
- **Monthly extra funds tracking** with allocation efficiency analysis
- **Strategy comparison** functionality to evaluate different approaches
- **Command-line interface** with comprehensive options and validation
- **Comprehensive test suite** with unit tests for all major components
- **Professional documentation** including README, contributing guidelines, and API docs

### Core Features
- Multiple optimization strategies (Debt Avalanche, Snowball, Hybrid)
- Future income integration (bonuses, raises, additional income streams)
- Recurring expense management (monthly, bi-weekly, quarterly, annual)
- Extra payment optimization and allocation
- Cash flow analysis and monitoring
- Excel template generation and data import
- Multi-sheet Excel reporting with professional formatting

### Charts and Visualizations
- Individual debt progression over time
- Principal vs interest payment breakdown
- Total debt reduction progress
- Monthly cash flow analysis (income vs expenses vs payments)
- Debt payoff timeline and order
- Extra funds utilization efficiency

### Technical Improvements
- Modern Python packaging with setuptools
- Type hints throughout codebase
- Comprehensive error handling and validation
- Logging system for debugging and monitoring
- BSD 3-Clause licensing
- Professional code organization and structure

### Documentation
- Comprehensive README with examples and usage instructions
- Contributing guidelines for developers
- Full API documentation
- Changelog for version tracking
- Professional setup.py with proper metadata

### Dependencies
- pandas >= 1.5.0 (data manipulation)
- numpy >= 1.21.0 (numerical computations)
- xlsxwriter >= 3.0.3 (Excel file creation with charts)
- openpyxl >= 3.0.7 (Excel file reading)
- click >= 8.0.0 (command-line interface)
- matplotlib >= 3.4.0 (chart generation)

### Breaking Changes
- N/A (initial release)

### Security
- No known security issues
- Input validation for all Excel data
- Safe file handling practices

---

### Legend
- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for security-related changes