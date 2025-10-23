# Release Scripts for Financial Debt Optimizer

This directory contains automated scripts for managing releases of the Financial Debt Optimizer project. These scripts handle testing, code quality, documentation, versioning, and publishing.

## Scripts Overview

### 🚀 Master Workflow Script

**`release_workflow.py`** - The main release orchestration script

```bash
# Full release workflow (patch version)
./scripts/release_workflow.py patch

# Minor version release
./scripts/release_workflow.py minor

# Major version release with prerelease
./scripts/release_workflow.py major --prerelease alpha.1

# Dry run to see what would happen
./scripts/release_workflow.py patch --dry-run

# Quick release (minimal checks, creates draft)
./scripts/release_workflow.py --quick

# Upload to Test PyPI
./scripts/release_workflow.py patch --test-pypi
```

### 🧪 Testing Scripts

**`run_tests.py`** - Comprehensive test runner with coverage

```bash
# Run all tests with coverage
./scripts/run_tests.py

# Skip slow tests
./scripts/run_tests.py --skip-slow

# Skip security checks
./scripts/run_tests.py --skip-security

# Verbose output
./scripts/run_tests.py --verbose
```

### 🧹 Code Quality Scripts

**`clean_code.py`** - Code formatting and cleanup

```bash
# Full code cleanup
./scripts/clean_code.py

# Skip optional steps (faster)
./scripts/clean_code.py --skip-optional

# Check formatting without changes
./scripts/clean_code.py --check-only
```

### 📚 Documentation Scripts

**`build_docs.py`** - Documentation generation

```bash
# Build HTML documentation
./scripts/build_docs.py

# Include PDF generation (requires LaTeX)
./scripts/build_docs.py --include-pdf

# Skip validation for faster build
./scripts/build_docs.py --no-validate

# Clean build directory only
./scripts/build_docs.py --clean-only
```

### 🔢 Version Management Scripts

**`bump_version.py`** - Semantic version management

```bash
# Patch version bump (1.0.0 → 1.0.1)
./scripts/bump_version.py patch

# Minor version bump (1.0.0 → 1.1.0)
./scripts/bump_version.py minor

# Major version bump (1.0.0 → 2.0.0)
./scripts/bump_version.py major

# Prerelease version (1.0.0 → 1.0.1-rc.1)
./scripts/bump_version.py patch --prerelease rc.1

# Dry run to see changes
./scripts/bump_version.py patch --dry-run

# Skip git operations
./scripts/bump_version.py patch --skip-git
```

### 📦 Publishing Scripts

**`publish_release.py`** - Release publishing to GitHub and PyPI

```bash
# Publish to GitHub and PyPI
./scripts/publish_release.py

# Create draft GitHub release
./scripts/publish_release.py --draft

# Upload to Test PyPI
./scripts/publish_release.py --test-pypi

# Skip GitHub operations
./scripts/publish_release.py --skip-github

# Skip PyPI operations
./scripts/publish_release.py --skip-pypi
```

## Typical Release Workflow

### 1. Standard Release

For most releases, use the master workflow script:

```bash
# 1. Dry run first to check everything
./scripts/release_workflow.py patch --dry-run

# 2. Run actual release
./scripts/release_workflow.py patch
```

This will:
- ✅ Run all tests with coverage
- 🎨 Format and clean code
- 📚 Build documentation
- 🔢 Bump version and create git tag
- 📤 Push to GitHub
- 🏷️ Create GitHub release
- 📦 Build and upload to PyPI
- 📖 Trigger ReadTheDocs build

### 2. Hotfix Release

For urgent fixes with minimal checks:

```bash
./scripts/release_workflow.py --quick
```

This creates a draft release that you can review before publishing.

### 3. Prerelease

For alpha/beta/rc releases:

```bash
./scripts/release_workflow.py minor --prerelease beta.1
```

### 4. Test Release

To test the release process:

```bash
./scripts/release_workflow.py patch --test-pypi --draft
```

## Individual Script Usage

You can also run individual scripts for specific tasks:

```bash
# Run tests only
./scripts/run_tests.py

# Clean code only
./scripts/clean_code.py

# Build docs only
./scripts/build_docs.py

# Just bump version
./scripts/bump_version.py patch
```

## Prerequisites

### Required Python Packages

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Install build dependencies
pip install build twine

# Install documentation dependencies
pip install -r docs/requirements.txt
```

### Optional Tools

- **GitHub CLI** (`gh`) - For GitHub release creation
  ```bash
  brew install gh
  gh auth login
  ```

- **LaTeX** - For PDF documentation generation
  ```bash
  brew install --cask mactex
  ```

## Environment Variables

### For PyPI Publishing

```bash
# Method 1: API Token (recommended)
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-api-token-here

# Method 2: Username/Password
export TWINE_USERNAME=your-pypi-username
export TWINE_PASSWORD=your-pypi-password
```

### For Test PyPI

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-test-pypi-token-here
```

## Configuration Files

The scripts read configuration from:
- `debt-optimizer/__version__.py` - Version information
- `setup.py` - Package configuration
- `docs/conf.py` - Documentation configuration
- `CHANGELOG.md` - Release notes (created automatically)

## Troubleshooting

### Common Issues

**Git working directory not clean**
```bash
git status
git add .
git commit -m "Fix issue"
```

**Missing dependencies**
```bash
pip install -r requirements-test.txt
pip install build twine sphinx
```

**GitHub CLI not authenticated**
```bash
gh auth login
```

**PyPI credentials not set**
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=your-api-token
```

### Debug Mode

All scripts support `--verbose` for detailed output:

```bash
./scripts/release_workflow.py patch --verbose
```

### Dry Run Mode

Most scripts support `--dry-run` to see what would happen:

```bash
./scripts/release_workflow.py patch --dry-run
```

## Script Architecture

Each script is self-contained with:
- ✅ Comprehensive error handling
- 📊 Progress reporting with emojis
- 🔍 Verbose mode for debugging
- 🏃‍♂️ Dry run capabilities
- 📝 Clear success/failure reporting

The master workflow script orchestrates all individual scripts in the correct order, providing a single command for complete releases.

## Contributing to Scripts

When modifying scripts:

1. Maintain consistent error handling patterns
2. Use descriptive progress messages
3. Support verbose and dry-run modes
4. Follow the existing code style
5. Test all code paths
6. Update this README if adding new features

## Security Notes

- Scripts validate git repository state before making changes
- Version tags are created before publishing
- Draft releases can be created for review
- Test PyPI can be used for validation
- All operations can be run in dry-run mode first