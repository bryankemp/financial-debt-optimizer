#!/usr/bin/env fish
# Reinstall debt_optimizer and run with --target-only mode

set -l script_dir (dirname (status filename))
cd $script_dir

echo "🔧 Reinstalling debt_optimizer..."
source .venv/bin/activate.fish 2>/dev/null
pip install -e . --quiet

echo "📊 Running analysis with --target-only mode..."
echo ""

debt_optimizer analyze --update-balances --target-only

echo ""
echo "✅ Done!"
