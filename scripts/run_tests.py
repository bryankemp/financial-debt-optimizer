#!/usr/bin/env python3
"""
Comprehensive test runner for Financial Debt Optimizer.

This script runs all tests, generates coverage reports, and performs code quality checks.
It mimics the CI/CD pipeline locally for release preparation.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class TestRunner:
    """Manages running tests and quality checks for the project."""

    def __init__(self, project_root: Path, verbose: bool = False):
        """Initialize the test runner.

        Args:
            project_root: Path to the project root directory
            verbose: Whether to show detailed output
        """
        self.project_root = project_root
        self.verbose = verbose
        self.failed_checks: List[str] = []

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
            print(f"✅ {description} - PASSED")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ {description} - FAILED")
            if not self.verbose and e.stdout:
                print(f"STDOUT:\n{e.stdout}")
            if not self.verbose and e.stderr:
                print(f"STDERR:\n{e.stderr}")

            if not allow_failure:
                self.failed_checks.append(description)
            return False

    def check_dependencies(self) -> bool:
        """Check if all required dependencies are installed."""
        print("\n🔍 Checking dependencies...")

        required_packages = [
            "pytest",
            "pytest-cov",
            "black",
            "isort",
            "flake8",
            "mypy",
            "safety",
            "bandit",
        ]

        missing_packages = []
        for package in required_packages:
            try:
                subprocess.run(
                    [sys.executable, "-c", f"import {package}"],
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError:
                # Some packages have different import names
                alt_imports = {
                    "pytest-cov": "pytest_cov",
                    "flake8": "flake8",
                }
                alt_name = alt_imports.get(package, package.replace("-", "_"))
                try:
                    subprocess.run(
                        [sys.executable, "-c", f"import {alt_name}"],
                        check=True,
                        capture_output=True,
                    )
                except subprocess.CalledProcessError:
                    missing_packages.append(package)

        if missing_packages:
            print(f"❌ Missing packages: {', '.join(missing_packages)}")
            print("Install with: pip install -r requirements-test.txt")
            return False

        print("✅ All dependencies available")
        return True

    def run_code_formatting_checks(self) -> bool:
        """Run code formatting and style checks."""
        print("\n🎨 Running code formatting checks...")

        success = True

        # Black formatting check
        success &= self.run_command(
            ["black", "--check", "--diff", "debt_optimizer", "tests", "scripts"],
            "Black code formatting check",
        )

        # isort import sorting check
        success &= self.run_command(
            [
                "isort",
                "--profile",
                "black",
                "--check-only",
                "--diff",
                "debt_optimizer",
                "tests",
                "scripts",
            ],
            "isort import sorting check",
        )

        # Flake8 linting
        success &= self.run_command(
            [
                "flake8",
                "debt_optimizer",
                "tests",
                "--count",
                "--select=E9,F63,F7,F82",
                "--show-source",
                "--statistics",
            ],
            "Flake8 critical error check",
        )

        # Additional flake8 checks (warnings only)
        self.run_command(
            [
                "flake8",
                "debt_optimizer",
                "tests",
                "--count",
                "--exit-zero",
                "--max-complexity=10",
                "--max-line-length=127",
                "--statistics",
            ],
            "Flake8 style warnings",
            allow_failure=True,
        )

        return success

    def run_type_checking(self) -> bool:
        """Run type checking with mypy."""
        print("\n🔍 Running type checking...")

        return self.run_command(
            [
                "mypy",
                "debt_optimizer",
                "--ignore-missing-imports",
                "--no-strict-optional",
            ],
            "MyPy type checking",
        )

    def run_security_checks(self) -> bool:
        """Run security vulnerability checks."""
        print("\n🔒 Running security checks...")

        success = True

        # Safety check for known vulnerabilities
        success &= self.run_command(
            ["safety", "check", "--json"],
            "Safety vulnerability check",
            allow_failure=True,  # May have false positives
        )

        # Bandit security linting
        success &= self.run_command(
            ["bandit", "-r", "debt_optimizer", "-f", "json"],
            "Bandit security linting",
            allow_failure=True,  # May have false positives
        )

        return success

    def run_unit_tests(self) -> bool:
        """Run unit tests with coverage."""
        print("\n🧪 Running unit tests...")

        return self.run_command(
            [
                "pytest",
                "-m",
                "unit",
                "--cov=debt_optimizer",
                "--cov-report=term",
                "--cov-report=html:htmlcov/unit",
                "--tb=short",
            ],
            "Unit tests with coverage",
        )

    def run_integration_tests(self) -> bool:
        """Run integration tests."""
        print("\n🔗 Running integration tests...")

        return self.run_command(
            [
                "pytest",
                "-m",
                "integration",
                "--cov=debt_optimizer",
                "--cov-append",
                "--cov-report=term",
                "--cov-report=html:htmlcov/integration",
                "--tb=short",
            ],
            "Integration tests with coverage",
        )

    def run_slow_tests(self) -> bool:
        """Run slow/performance tests."""
        print("\n🐌 Running slow tests...")

        return self.run_command(
            ["pytest", "-m", "slow", "--maxfail=5", "--tb=short"],
            "Slow tests",
            allow_failure=True,  # These might be flaky
        )

    def run_all_tests(self) -> bool:
        """Run complete test suite with coverage."""
        print("\n🎯 Running complete test suite...")

        return self.run_command(
            [
                "pytest",
                "--cov=debt_optimizer",
                "--cov-report=term",
                "--cov-report=html:htmlcov/all",
                "--cov-report=xml",
                "--cov-fail-under=75",
                "--tb=short",
            ],
            "Complete test suite with coverage",
        )

    def run_full_test_suite(
        self, skip_slow: bool = False, skip_security: bool = False
    ) -> bool:
        """Run the complete test suite.

        Args:
            skip_slow: Whether to skip slow tests
            skip_security: Whether to skip security checks

        Returns:
            True if all tests pass, False otherwise
        """
        print(f"\n🚀 Starting comprehensive test suite for {self.project_root.name}")

        # Check dependencies first
        if not self.check_dependencies():
            return False

        success = True

        # Code quality checks
        success &= self.run_code_formatting_checks()
        success &= self.run_type_checking()

        # Security checks (optional)
        if not skip_security:
            self.run_security_checks()  # Don't fail on security warnings

        # Test execution
        success &= self.run_unit_tests()
        success &= self.run_integration_tests()

        if not skip_slow:
            self.run_slow_tests()  # Don't fail on slow test issues

        # Final comprehensive test run
        success &= self.run_all_tests()

        # Report results
        print(f"\n{'='*60}")
        print("📊 TEST SUITE RESULTS")
        print("=" * 60)

        if success:
            print("✅ ALL CRITICAL TESTS PASSED!")
            print("🎉 Code is ready for release")
        else:
            print("❌ SOME TESTS FAILED!")
            print("Failed checks:")
            for check in self.failed_checks:
                print(f"  - {check}")

        print(f"\n📈 Coverage report available at: htmlcov/all/index.html")
        print(f"📄 XML coverage report: coverage.xml")

        return success


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(
        description="Run comprehensive test suite for Financial Debt Optimizer"
    )
    parser.add_argument(
        "--skip-slow", action="store_true", help="Skip slow performance tests"
    )
    parser.add_argument(
        "--skip-security",
        action="store_true",
        help="Skip security vulnerability checks",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output from all commands",
    )

    args = parser.parse_args()

    # Find project root
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent

    # Run tests
    runner = TestRunner(project_root, verbose=args.verbose)
    success = runner.run_full_test_suite(
        skip_slow=args.skip_slow, skip_security=args.skip_security
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
