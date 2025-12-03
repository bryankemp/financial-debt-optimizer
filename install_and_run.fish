#!/usr/bin/env fish

# Install the local version of debt_optimizer
echo "Installing local version of debt_optimizer..."
pipx install . --force

# Check if installation was successful
if test $status -eq 0
    echo "Installation successful!"
    echo "Running debt_optimizer analyze..."
    debt_optimizer analyze -u -i default.xlsx -o out.xlsx
else
    echo "Installation failed!"
    exit 1
end
