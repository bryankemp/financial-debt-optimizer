#!/usr/bin/env python3
"""
Code cleanup script for Financial Debt Optimizer.

This script automatically formats code, sorts imports, fixes linting issues,
and performs other cleanup tasks to prepare code for release.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class CodeCleaner:
    """Manages code cleanup tasks for the project."""

    def __init__(self, project_root: Path, verbose: bool = False):
        """Initialize the code cleaner.

        Args:
            project_root: Path to the project root directory
            verbose: Whether to show detailed output
        """
        self.project_root = project_root
        self.verbose = verbose
        self.source_dirs = ["src", "tests", "scripts"]
        self.issues_found: List[str] = []

    def run_command(
        self, cmd: List[str], description: str, allow_failure: bool = False
    ) -> bool:
        """Run a command and report results.

        Args:
            cmd: Command to run as a list of strings
            description: Human-readable description of the command
            allow_failure: Whether to continue if command fails

        Returns:
            True if command succeeded, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"Running: {description}")
        print(f"Command: {' '.join(cmd)}")
        print("=" * 60)

        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                check=True,
                capture_output=not self.verbose,
                text=True,
            )
            if not self.verbose and result.stdout:
                print(result.stdout)
            print(f"✅ {description} - SUCCESS")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ {description} - FAILED")
            if not self.verbose and e.stdout:
                print(f"STDOUT:\n{e.stdout}")
            if not self.verbose and e.stderr:
                print(f"STDERR:\n{e.stderr}")

            if not allow_failure:
                self.issues_found.append(description)
            return False

    def check_dependencies(self) -> bool:
        """Check if code cleanup dependencies are available."""
        print("\n🔍 Checking code cleanup dependencies...")

        required_packages = ["black", "isort", "flake8", "pycodestyle"]
        missing_packages = []

        for package in required_packages:
            try:
                subprocess.run(
                    [sys.executable, "-c", f"import {package}"],
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError:
                missing_packages.append(package)

        if missing_packages:
            print(f"❌ Missing packages: {', '.join(missing_packages)}")
            print("Install with: pip install black isort flake8 pycodestyle")
            return False

        print("✅ All code cleanup dependencies available")
        return True

    def validate_source_directories(self) -> bool:
        """Check that source directories exist."""
        print("\n📁 Validating source directories...")

        existing_dirs = []
        for source_dir in self.source_dirs:
            dir_path = self.project_root / source_dir
            if dir_path.exists() and dir_path.is_dir():
                existing_dirs.append(source_dir)
                print(f"✅ Found directory: {source_dir}")
            else:
                print(f"⚠️  Directory not found: {source_dir}")

        if not existing_dirs:
            print("❌ No source directories found to clean")
            return False

        # Update source_dirs to only include existing directories
        self.source_dirs = existing_dirs
        print(f"📝 Will clean directories: {', '.join(self.source_dirs)}")
        return True

    def run_pycodestyle_check(self) -> bool:
        """Run pycodestyle to check PEP 8 compliance."""
        print("\n🔧 Running pycodestyle to check PEP 8 compliance...")

        success = True
        for source_dir in self.source_dirs:
            cmd = [
                "pycodestyle",
                "--max-line-length=88",  # Match Black's line length
                "--ignore=E203,W503",  # Ignore conflicts with Black
                "--statistics",
                source_dir,
            ]
            success &= self.run_command(
                cmd, f"pycodestyle check for {source_dir}", allow_failure=True
            )

        return success

    def run_black_formatting(self) -> bool:
        """Run Black code formatter."""
        print("\n🎨 Running Black code formatter...")

        cmd = ["black"] + self.source_dirs
        return self.run_command(cmd, "Black code formatting")

    def run_isort_import_sorting(self) -> bool:
        """Run isort to sort imports."""
        print("\n📚 Running isort to sort imports...")

        cmd = ["isort"] + self.source_dirs
        return self.run_command(cmd, "isort import sorting")

    def check_flake8_issues(self) -> bool:
        """Check for remaining flake8 issues."""
        print("\n🔍 Checking for remaining flake8 issues...")

        cmd = [
            "flake8",
            "--count",
            "--statistics",
            "--max-line-length=88",  # Match Black's line length
            "--extend-ignore=E203,W503",  # Ignore conflicts with Black
        ] + self.source_dirs

        return self.run_command(cmd, "flake8 linting check", allow_failure=True)

    def remove_unused_imports(self) -> bool:
        """Remove unused imports using autoflake."""
        print("\n🧹 Removing unused imports...")

        # Check if autoflake is available
        try:
            subprocess.run(["autoflake", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  autoflake not available, skipping unused import removal")
            return True

        success = True
        for source_dir in self.source_dirs:
            cmd = [
                "autoflake",
                "--in-place",
                "--remove-all-unused-imports",
                "--remove-unused-variables",
                "--recursive",
                source_dir,
            ]
            success &= self.run_command(
                cmd, f"Remove unused imports from {source_dir}", allow_failure=True
            )

        return success

    def fix_docstring_formatting(self) -> bool:
        """Fix docstring formatting using docformatter."""
        print("\n📝 Fixing docstring formatting...")

        # Check if docformatter is available
        try:
            subprocess.run(
                ["docformatter", "--version"], check=True, capture_output=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  docformatter not available, skipping docstring formatting")
            return True

        success = True
        for source_dir in self.source_dirs:
            cmd = [
                "docformatter",
                "--in-place",
                "--wrap-summaries=88",
                "--wrap-descriptions=88",
                "--make-summary-multi-line",
                "--recursive",
                source_dir,
            ]
            success &= self.run_command(
                cmd, f"Fix docstrings in {source_dir}", allow_failure=True
            )

        return success

    def clean_pycache_files(self) -> bool:
        """Clean __pycache__ directories and .pyc files."""
        print("\n🗑️  Cleaning Python cache files...")

        import glob
        import os

        cleaned_files = 0
        cleaned_dirs = 0

        # Remove .pyc files
        for pattern in ["**/*.pyc", "**/*.pyo"]:
            for file_path in self.project_root.glob(pattern):
                try:
                    file_path.unlink()
                    cleaned_files += 1
                except OSError as e:
                    print(f"⚠️  Could not remove {file_path}: {e}")

        # Remove __pycache__ directories
        for pycache_dir in self.project_root.glob("**/__pycache__"):
            try:
                import shutil

                shutil.rmtree(pycache_dir)
                cleaned_dirs += 1
            except OSError as e:
                print(f"⚠️  Could not remove {pycache_dir}: {e}")

        print(
            f"✅ Cleaned {cleaned_files} cache files and {cleaned_dirs} __pycache__ directories"
        )
        return True

    def clean_build_artifacts(self) -> bool:
        """Clean build artifacts and temporary files."""
        print("\n🧹 Cleaning build artifacts...")

        import shutil

        # Directories to clean
        build_dirs = [
            "build",
            "dist",
            "*.egg-info",
            ".pytest_cache",
            ".coverage",
            "htmlcov",
            ".mypy_cache",
            ".tox",
        ]

        cleaned_count = 0

        for pattern in build_dirs:
            for path in self.project_root.glob(pattern):
                try:
                    if path.is_dir():
                        shutil.rmtree(path)
                        print(f"✅ Removed directory: {path.name}")
                    else:
                        path.unlink()
                        print(f"✅ Removed file: {path.name}")
                    cleaned_count += 1
                except OSError as e:
                    print(f"⚠️  Could not remove {path}: {e}")

        if cleaned_count == 0:
            print("✅ No build artifacts to clean")
        else:
            print(f"✅ Cleaned {cleaned_count} build artifacts")

        return True

    def check_file_endings(self) -> bool:
        """Ensure all Python files have proper line endings."""
        print("\n📄 Checking file endings...")

        fixed_files = 0

        for source_dir in self.source_dirs:
            source_path = self.project_root / source_dir
            if not source_path.exists():
                continue

            for py_file in source_path.rglob("*.py"):
                try:
                    with open(py_file, "rb") as f:
                        content = f.read()

                    # Check if file needs fixing (has Windows line endings)
                    if b"\r\n" in content:
                        # Convert to Unix line endings
                        content = content.replace(b"\r\n", b"\n")
                        with open(py_file, "wb") as f:
                            f.write(content)
                        fixed_files += 1
                        print(
                            f"✅ Fixed line endings in: {py_file.relative_to(self.project_root)}"
                        )

                except (OSError, UnicodeDecodeError) as e:
                    print(f"⚠️  Could not process {py_file}: {e}")

        if fixed_files == 0:
            print("✅ All files have correct line endings")
        else:
            print(f"✅ Fixed line endings in {fixed_files} files")

        return True

    def run_complete_cleanup(self, skip_optional: bool = False) -> bool:
        """Run complete code cleanup process.

        Args:
            skip_optional: Whether to skip optional cleanup steps

        Returns:
            True if cleanup completed successfully, False otherwise
        """
        print(f"\n🧹 Starting comprehensive code cleanup for {self.project_root.name}")

        # Check dependencies and directories
        if not self.check_dependencies():
            return False

        if not self.validate_source_directories():
            return False

        success = True

        # Core cleanup steps
        success &= self.clean_pycache_files()
        success &= self.clean_build_artifacts()
        success &= self.check_file_endings()

        # Code formatting and fixes
        if not skip_optional:
            self.remove_unused_imports()  # Optional, may not be available
            self.run_pycodestyle_check()  # Optional, check PEP 8 compliance
            self.fix_docstring_formatting()  # Optional, may not be available

        # Essential formatting
        success &= self.run_black_formatting()
        success &= self.run_isort_import_sorting()

        # Final quality check
        self.check_flake8_issues()  # Don't fail on remaining issues

        # Report results
        print(f"\n{'='*60}")
        print("📊 CODE CLEANUP RESULTS")
        print("=" * 60)

        if success:
            print("✅ CODE CLEANUP COMPLETED SUCCESSFULLY!")
            print("🎉 Code is formatted and ready for release")

            if self.issues_found:
                print("\n⚠️  Some optional steps had issues:")
                for issue in self.issues_found:
                    print(f"  - {issue}")
        else:
            print("❌ CODE CLEANUP HAD ISSUES!")
            print("Issues encountered:")
            for issue in self.issues_found:
                print(f"  - {issue}")

        print(f"\n💡 Tip: Run 'git diff' to see what changes were made")
        return success


def main():
    """Main entry point for the code cleaner."""
    parser = argparse.ArgumentParser(
        description="Clean and format code for Financial Debt Optimizer"
    )
    parser.add_argument(
        "--skip-optional",
        action="store_true",
        help="Skip optional cleanup steps (faster, fewer dependencies)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output from all commands",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check formatting without making changes",
    )

    args = parser.parse_args()

    # Find project root
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent

    if args.check_only:
        # Run check-only mode (like CI)
        print("🔍 Running formatting checks only (no changes will be made)")

        try:
            # Check Black formatting
            result = subprocess.run(
                ["black", "--check", "--diff", "src", "tests", "scripts"],
                cwd=project_root,
                capture_output=True,
            )
            if result.returncode != 0:
                print("❌ Black formatting issues found:")
                print(result.stdout.decode())
                sys.exit(1)

            # Check isort
            result = subprocess.run(
                ["isort", "--check-only", "--diff", "src", "tests", "scripts"],
                cwd=project_root,
                capture_output=True,
            )
            if result.returncode != 0:
                print("❌ Import sorting issues found:")
                print(result.stdout.decode())
                sys.exit(1)

            print("✅ All formatting checks passed!")

        except FileNotFoundError as e:
            print(f"❌ Required tool not found: {e}")
            sys.exit(1)
    else:
        # Run full cleanup
        cleaner = CodeCleaner(project_root, verbose=args.verbose)
        success = cleaner.run_complete_cleanup(skip_optional=args.skip_optional)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
