Installation
============

System Requirements
-------------------

The Financial Debt Optimizer requires:

* **Python**: 3.8 or higher
* **Operating System**: Windows, macOS, or Linux
* **Memory**: 512MB RAM minimum (2GB recommended for large datasets)
* **Disk Space**: 50MB for installation

Dependencies
------------

The following packages will be automatically installed:

* **pandas** (≥1.3.0): Data manipulation and analysis
* **numpy** (≥1.21.0): Numerical computing
* **xlsxwriter** (≥3.0.0): Excel file writing
* **openpyxl** (≥3.0.0): Excel file reading
* **click** (≥8.0.0): Command-line interface
* **matplotlib** (≥3.5.0): Data visualization

Installation Methods
--------------------

PyPI (Recommended)
~~~~~~~~~~~~~~~~~~

The easiest way to install Financial Debt Optimizer is using pip::

    pip install financial-debt-optimizer

This will install the latest stable version from PyPI along with all required dependencies.

Install Specific Version
~~~~~~~~~~~~~~~~~~~~~~~~

To install a specific version::

    pip install financial-debt-optimizer==1.1.0

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

If you want to contribute to the project or use the latest development version:

1. **Clone the repository**::

    git clone https://github.com/bryankemp/financial-debt-optimizer.git
    cd financial-debt-optimizer

2. **Create a virtual environment** (recommended)::

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install in development mode**::

    pip install -e .

4. **Install development dependencies**::

    pip install -e ".[dev]"

Virtual Environment (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's highly recommended to install the package in a virtual environment to avoid conflicts with other Python packages::

    # Create virtual environment
    python -m venv debt-optimizer-env
    
    # Activate virtual environment
    # On macOS/Linux:
    source debt-optimizer-env/bin/activate
    # On Windows:
    debt-optimizer-env\Scripts\activate
    
    # Install the package
    pip install financial-debt-optimizer

Verification
------------

To verify the installation was successful, run::

    debt-optimizer --version

You should see output similar to::

    Financial Debt Optimizer version 1.1.0

You can also test the Python API::

    python -c "from core.debt_optimizer import DebtOptimizer; print('Installation successful!')"

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**ImportError: No module named 'pandas'**
    This usually means the dependencies weren't installed correctly. Try reinstalling::

        pip uninstall financial-debt-optimizer
        pip install financial-debt-optimizer

**Permission denied errors**
    On some systems, you may need to use ``--user`` flag::

        pip install --user financial-debt-optimizer

**Python version compatibility**
    Ensure you're using Python 3.8 or higher::

        python --version

**Excel file permissions**
    Make sure you have read permissions for input Excel files and write permissions for output directories.

Getting Help
~~~~~~~~~~~~

If you encounter issues:

1. Check the `GitHub Issues <https://github.com/bryankemp/financial-debt-optimizer/issues>`_
2. Create a new issue with:
   - Your operating system
   - Python version
   - Error message (if any)
   - Steps to reproduce the problem

Upgrading
---------

To upgrade to the latest version::

    pip install --upgrade financial-debt-optimizer

To upgrade to a specific version::

    pip install --upgrade financial-debt-optimizer==1.1.0

Uninstalling
------------

To remove the package::

    pip uninstall financial-debt-optimizer

This will remove the package but keep any Excel files or data you've created.