Frequently Asked Questions
==========================

This page addresses common questions about using the Financial Debt Optimizer.

General Questions
-----------------

What is the Financial Debt Optimizer?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Financial Debt Optimizer is a Python tool that helps you analyze and optimize your debt repayment strategies. It can compare different approaches (avalanche, snowball, hybrid) to help you save money and pay off debt faster.

Who should use this tool?
~~~~~~~~~~~~~~~~~~~~~~~~~

- Anyone with multiple debts who wants to optimize their repayment strategy
- Financial advisors helping clients with debt management
- People who want to understand the impact of extra payments on their debt
- Anyone interested in comparing different debt repayment approaches

Is this tool free to use?
~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, the Financial Debt Optimizer is completely free and open source. You can use it for personal or commercial purposes under the BSD 3-Clause license.

Installation and Setup
----------------------

What do I need to run this tool?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Python 3.8 or higher
- Basic familiarity with Excel or CSV files
- Your debt information (balances, interest rates, minimum payments)

I'm getting "command not found" errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This usually means:
1. Python isn't installed or not in your PATH
2. The package wasn't installed correctly
3. You're not in the correct virtual environment

Try::

    python --version
    pip show financial-debt-optimizer

If Python isn't recognized, install it from `python.org <https://python.org>`_.

Can I use this on Windows/Mac/Linux?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, the tool works on all major operating systems. The installation process is the same across platforms.

Using the Tool
--------------

What file formats are supported?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The tool reads Excel files (.xlsx and .xls formats). Your debt data should be organized with specific column names:
- Name: Description of the debt
- Balance: Current balance owed
- Rate: Annual interest rate (as percentage)
- Min_Pay: Minimum monthly payment

Can I use this without Excel?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While the tool is designed to work with Excel files, you can create the required format in:
- Google Sheets (export as .xlsx)
- LibreOffice Calc
- Apple Numbers
- Even a CSV file renamed to .xlsx (though this may have limitations)

How accurate are the calculations?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The calculations are highly accurate for standard debt scenarios. The tool uses:
- Compound interest formulas
- Precise payment allocation between interest and principal
- Month-by-month payment tracking

However, the tool assumes:
- Fixed interest rates
- Consistent payment amounts
- No additional fees or charges
- No missed payments

Debt Strategies
---------------

Which strategy should I choose?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Debt Avalanche** if you:
- Want to minimize total interest paid
- Are motivated by saving money
- Can stick to a plan without frequent milestones

**Debt Snowball** if you:
- Need psychological motivation
- Want to see individual debts eliminated quickly
- Have struggled to stick with debt repayment in the past

**Hybrid** if you:
- Want a balance between saving money and motivation
- Are unsure which approach is best for you
- Want some quick wins while still focusing on high-interest debt

What if I have very large debts with low interest rates?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Large, low-interest debts (like mortgages or some student loans) should often be treated differently:
- Consider excluding them from optimization (pay minimums)
- Focus optimization on higher-rate, smaller debts
- Factor in tax deductions for mortgage interest
- Consider the opportunity cost of extra payments vs. investing

The tool can handle these, but you might want to analyze them separately.

Can I prioritize certain debts manually?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The tool implements mathematical strategies, but you can:
- Run separate analyses excluding certain debts
- Use the Python API to create custom optimization logic
- Manually adjust your strategy based on the tool's recommendations

Data and Privacy
----------------

Is my financial data secure?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, your data is completely private:
- All processing happens locally on your computer
- No data is sent to external servers
- No data is stored or transmitted anywhere
- The tool only reads the Excel file you provide and writes results locally

Can I share my results?
~~~~~~~~~~~~~~~~~~~~~~~

The Excel output files contain only the analysis results and payment schedules - they don't include sensitive account information unless you put it in the original file. Remove any sensitive data before sharing.

What data should I include?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Required:**
- Debt name/description
- Current balance
- Interest rate (annual percentage)
- Minimum monthly payment

**Optional but helpful:**
- Debt type (credit card, loan, etc.)
- Institution name
- Target payoff dates

**Don't include:**
- Full account numbers
- Social security numbers
- Passwords or PINs

Technical Issues
----------------

The tool is running slowly
~~~~~~~~~~~~~~~~~~~~~~~~~~

Performance depends on:
- Number of debts (20+ may take a few seconds)
- Extra payment amounts (higher payments = longer calculations)
- Chart generation (disable with --no-charts if needed)

For large debt portfolios, consider:
- Breaking into smaller groups
- Using the verbose mode to monitor progress
- Running analysis overnight for very complex scenarios

My Excel file won't load
~~~~~~~~~~~~~~~~~~~~~~~~

Check that:
- File is saved in .xlsx or .xls format
- Required columns exist with correct names (Name, Balance, Rate, Min_Pay)
- All numeric fields contain only numbers (no currency symbols)
- There are no completely empty rows in your data

Excel files created in newer versions should work fine.

The results look wrong
~~~~~~~~~~~~~~~~~~~~~~

Common issues:
- Interest rates entered as decimals instead of percentages (use 18.99, not 0.1899)
- Minimum payments are annual instead of monthly
- Balances are outdated
- Extra payment amount is unrealistic for your budget

Double-check your input data and try a simple example first.

Financial Planning
------------------

How often should I run this analysis?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recommended frequency:
- **Monthly**: Update balances and track progress
- **Quarterly**: Reassess strategy and adjust for changes
- **Annually**: Major review when income/expenses change
- **As needed**: When adding new debt or making large payments

Should I always follow the recommended strategy?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The tool provides mathematically optimal recommendations, but consider:
- Your personal financial situation
- Psychological factors and motivation
- Other financial goals (emergency fund, retirement)
- Cash flow constraints

The recommendations are a starting point for your decision-making.

What about emergency funds?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most financial advisors recommend:
1. Build a small emergency fund ($1,000) first
2. Pay off high-interest debt (>10% rates)
3. Build full emergency fund (3-6 months expenses)
4. Focus on remaining debt

The tool focuses on debt optimization - factor in emergency savings separately.

Can this help with mortgage decisions?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While you can include mortgages in the analysis, they often require special consideration:
- Tax deductibility of mortgage interest
- Opportunity cost vs. investing
- PMI removal thresholds
- Refinancing opportunities

Consider consulting a financial advisor for major mortgage decisions.

Advanced Usage
--------------

Can I automate this analysis?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, using the Python API you can:
- Schedule regular analysis runs
- Integrate with budgeting software
- Create custom reporting
- Build web applications around the tool

See the :doc:`user_guide` for automation examples.

How do I contribute improvements?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The project welcomes contributions:
- Report bugs on GitHub Issues
- Suggest features through GitHub Discussions
- Submit code improvements via Pull Requests
- Help improve documentation

See :doc:`contributing` for detailed guidelines.

Can I use this commercially?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, the BSD 3-Clause license allows commercial use. You can:
- Use it in financial planning businesses
- Integrate it into commercial software
- Modify it for specific use cases
- Redistribute it (with proper attribution)

Error Messages
--------------

"ImportError: No module named 'pandas'"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dependencies weren't installed. Try::

    pip uninstall financial-debt-optimizer
    pip install financial-debt-optimizer

"Permission denied" errors
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Make sure the output directory exists and is writable
- Close the output Excel file if it's open in another program
- Try running with ``--user`` flag: ``pip install --user financial-debt-optimizer``

"Invalid strategy" error
~~~~~~~~~~~~~~~~~~~~~~~~

Use one of the supported strategies:
- ``avalanche``
- ``snowball``
- ``hybrid``

These are case-sensitive.

"File not found" error
~~~~~~~~~~~~~~~~~~~~~~

- Verify the input file path is correct
- Use absolute paths if relative paths aren't working
- Make sure the file extension is .xlsx or .xls
- Check that you have read permissions for the file

Getting More Help
-----------------

Where can I get additional support?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Documentation**: Check the complete :doc:`user_guide` and :doc:`examples`
2. **GitHub Issues**: Report bugs or ask questions at https://github.com/bryankemp/financial-debt-optimizer/issues
3. **Examples**: Review the :doc:`examples` section for similar use cases
4. **Community**: Join discussions on the GitHub repository

How do I report a bug?
~~~~~~~~~~~~~~~~~~~~~~

When reporting issues, please include:
- Your operating system and Python version
- The complete error message
- A sample of your input data (remove sensitive information)
- The exact command you ran
- Expected vs actual results

What features are planned?
~~~~~~~~~~~~~~~~~~~~~~~~~~

Potential future features:
- Web-based interface
- More debt strategies
- Integration with banking APIs
- Mobile app version
- Advanced visualization options

Feature requests and contributions are welcome!

Is there a user community?
~~~~~~~~~~~~~~~~~~~~~~~~~~

While there isn't a dedicated forum yet, you can:
- Follow the GitHub repository for updates
- Participate in GitHub Discussions
- Connect with other users through issues and pull requests
- Share your success stories and use cases

Still Have Questions?
---------------------

If your question isn't answered here:

1. Check the :doc:`user_guide` for detailed information
2. Review the :doc:`examples` for similar scenarios
3. Search existing GitHub issues
4. Create a new issue with your specific question

The maintainers and community are happy to help!