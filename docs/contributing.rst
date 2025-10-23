Contributing
============

We welcome contributions to the Financial Debt Optimizer project! This page provides information for developers and contributors.

For detailed contribution guidelines, please see our `CONTRIBUTING.md <https://github.com/bryankemp/financial-debt_optimizer/blob/main/CONTRIBUTING.md>`_ file on GitHub.

Quick Start for Contributors
----------------------------

1. **Fork the repository** on GitHub
2. **Clone your fork** locally::

    git clone https://github.com/yourusername/financial-debt_optimizer.git
    cd financial-debt_optimizer

3. **Set up development environment**::

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -e ".[dev]"

4. **Make your changes** and test them
5. **Submit a pull request** with your improvements

Types of Contributions
----------------------

We appreciate all types of contributions:

- **Bug reports** and issue identification
- **Feature requests** and enhancement ideas  
- **Code contributions** including bug fixes and new features
- **Documentation improvements**
- **Test coverage** expansion
- **Performance optimizations**
- **User experience** improvements

Development Setup
-----------------

**Prerequisites:**
- Python 3.8 or higher
- Git
- Text editor or IDE

**Installation:**
::

    git clone https://github.com/bryankemp/financial-debt_optimizer.git
    cd financial-debt_optimizer
    python -m venv venv
    source venv/bin/activate
    pip install -e ".[dev]"

**Running Tests:**
::

    pytest

**Building Documentation:**
::

    cd docs
    make html

Code Style
----------

We follow PEP 8 style guidelines with some project-specific conventions. Please:

- Run ``black`` for code formatting
- Use ``pylint`` for code quality checks
- Add docstrings for new functions and classes
- Include type hints where appropriate
- Write tests for new functionality

Pull Request Process
--------------------

1. **Create a feature branch** from main
2. **Make your changes** with clear, descriptive commits
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Ensure all tests pass**
6. **Submit pull request** with detailed description

For complete details, see `CONTRIBUTING.md <https://github.com/bryankemp/financial-debt_optimizer/blob/main/CONTRIBUTING.md>`_.

Reporting Issues
----------------

When reporting bugs or requesting features, please use our `GitHub Issues <https://github.com/bryankemp/financial-debt_optimizer/issues>`_ page.

Include:
- Clear description of the issue
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Your environment details
- Sample data (remove sensitive information)

Communication
-------------

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions
- **Email**: For security issues or private matters

We aim to respond to all contributions within a few days.

Thank you for helping make Financial Debt Optimizer better!