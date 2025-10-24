# Examples

This directory contains example data files and templates for the Financial Debt Optimizer.

## Files

### `sample_data.xlsx`
A complete example with realistic debt, income, and expense data demonstrating:
- Multiple credit cards and loans with varying interest rates
- Bi-weekly income with future income (bonuses, raises)
- Recurring monthly expenses
- Future expense planning

This file can be used as:
1. **Learning tool**: See how to structure your data
2. **Testing**: Verify the optimizer works correctly
3. **Template**: Copy and modify with your own data

## Usage

### Run Analysis on Sample Data
```bash
debt_optimizer analyze --input examples/sample_data.xlsx --output my-results.xlsx
```

### Generate New Template
```bash
debt_optimizer generate-template my-template.xlsx
```

### Compare Strategies
```bash
debt_optimizer analyze \
    --input examples/sample_data.xlsx \
    --output comprehensive-analysis.xlsx \
    --compare-strategies \
    --goal minimize_interest
```

## Data Structure

The sample file demonstrates the complete Excel template structure:

- **Debts Sheet**: Credit cards, loans, and other debts
- **Income Sheet**: Regular salary and income sources  
- **Recurring Expenses Sheet**: Monthly bills and fixed costs
- **Future Income Sheet**: Bonuses, raises, and additional income
- **Future Expenses Sheet**: Planned future costs (currently empty in sample)
- **Settings Sheet**: Optimization preferences and configuration

## Privacy Note

All data in these examples is fictitious and for demonstration purposes only. Never commit real financial data to version control.

## Creating Your Own Data

1. Copy `sample_data.xlsx` to a new file outside this directory
2. Replace the sample data with your actual financial information
3. Run the analysis on your personalized file
4. Keep your real data files private and outside of version control