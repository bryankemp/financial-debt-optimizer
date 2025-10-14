#!/usr/bin/env python3
"""
Test report generator for Financial Debt Optimizer documentation.

This script runs the full test suite, generates coverage reports, and creates
formatted output for inclusion in the project documentation.
"""

import argparse
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class TestReportGenerator:
    """Generates comprehensive test reports for documentation."""

    def __init__(self, project_root: Path, verbose: bool = False):
        """Initialize the test report generator.

        Args:
            project_root: Path to the project root directory
            verbose: Whether to show detailed output
        """
        self.project_root = project_root
        self.docs_dir = project_root / "docs"
        self.reports_dir = self.docs_dir / "_static" / "test_reports"
        self.verbose = verbose
        self.test_results: Dict = {}

        # Ensure reports directory exists
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def run_command(self, cmd: List[str], description: str) -> Tuple[bool, str, str]:
        """Run a command and return results.

        Args:
            cmd: Command to run as a list of strings
            description: Human-readable description of the command

        Returns:
            Tuple of (success, stdout, stderr)
        """
        if self.verbose:
            print(f"Running: {description}")
            print(f"Command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=False,  # Don't raise on non-zero exit
            )

            success = result.returncode == 0
            if self.verbose:
                status = "✅ SUCCESS" if success else "❌ FAILED"
                print(f"{description} - {status}")
                if result.stdout:
                    print(f"STDOUT:\n{result.stdout}")
                if result.stderr:
                    print(f"STDERR:\n{result.stderr}")

            return success, result.stdout, result.stderr

        except Exception as e:
            if self.verbose:
                print(f"❌ {description} - ERROR: {e}")
            return False, "", str(e)

    def run_test_suite(self) -> bool:
        """Run the complete test suite with coverage."""
        print("\n🧪 Running test suite with coverage...")

        # Run pytest with coverage and multiple output formats
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "--cov=src",
            "--cov-report=html:" + str(self.reports_dir / "coverage_html"),
            "--cov-report=xml:" + str(self.reports_dir / "coverage.xml"),
            "--cov-report=json:" + str(self.reports_dir / "coverage.json"),
            "--cov-report=term-missing",
            "--junit-xml=" + str(self.reports_dir / "junit.xml"),
            "--tb=short",
            "-v",
        ]

        success, stdout, stderr = self.run_command(cmd, "Run test suite with coverage")

        # Store test output
        with open(self.reports_dir / "test_output.txt", "w") as f:
            f.write(f"Test Suite Output - {datetime.now().isoformat()}\n")
            f.write("=" * 60 + "\n\n")
            f.write("STDOUT:\n")
            f.write(stdout)
            f.write("\n\nSTDERR:\n")
            f.write(stderr)

        return success

    def parse_coverage_report(self) -> Dict:
        """Parse coverage report and extract key metrics."""
        coverage_file = self.reports_dir / "coverage.json"

        if not coverage_file.exists():
            return {"error": "Coverage report not found"}

        try:
            with open(coverage_file, "r") as f:
                coverage_data = json.load(f)

            # Extract summary metrics
            totals = coverage_data.get("totals", {})
            summary = {
                "total_statements": totals.get("num_statements", 0),
                "missing_statements": totals.get("missing_lines", 0),
                "covered_statements": totals.get("covered_lines", 0),
                "coverage_percent": round(totals.get("percent_covered", 0), 2),
                "files_analyzed": len(coverage_data.get("files", {})),
                "timestamp": datetime.now().isoformat(),
            }

            # Extract per-file coverage
            files_coverage = []
            for filepath, file_data in coverage_data.get("files", {}).items():
                file_info = {
                    "file": filepath,
                    "statements": file_data.get("summary", {}).get("num_statements", 0),
                    "missing": file_data.get("summary", {}).get("missing_lines", 0),
                    "coverage": round(
                        file_data.get("summary", {}).get("percent_covered", 0), 2
                    ),
                }
                files_coverage.append(file_info)

            # Sort by coverage percentage (lowest first for attention)
            files_coverage.sort(key=lambda x: x["coverage"])

            summary["files"] = files_coverage
            return summary

        except Exception as e:
            return {"error": f"Failed to parse coverage report: {e}"}

    def parse_junit_report(self) -> Dict:
        """Parse JUnit XML report and extract test metrics."""
        junit_file = self.reports_dir / "junit.xml"

        if not junit_file.exists():
            return {"error": "JUnit report not found"}

        try:
            tree = ET.parse(junit_file)
            root = tree.getroot()

            # Extract test suite metrics
            testsuite = root.find("testsuite")
            if testsuite is not None:
                summary = {
                    "total_tests": int(testsuite.get("tests", 0)),
                    "failures": int(testsuite.get("failures", 0)),
                    "errors": int(testsuite.get("errors", 0)),
                    "skipped": int(testsuite.get("skipped", 0)),
                    "time": float(testsuite.get("time", 0)),
                    "timestamp": testsuite.get("timestamp", datetime.now().isoformat()),
                }

                # Calculate derived metrics
                summary["passed"] = (
                    summary["total_tests"]
                    - summary["failures"]
                    - summary["errors"]
                    - summary["skipped"]
                )
                summary["success_rate"] = round(
                    (
                        (summary["passed"] / summary["total_tests"] * 100)
                        if summary["total_tests"] > 0
                        else 0
                    ),
                    2,
                )

                # Extract individual test cases
                test_cases = []
                for testcase in root.findall(".//testcase"):
                    case_info = {
                        "name": testcase.get("name", "Unknown"),
                        "classname": testcase.get("classname", "Unknown"),
                        "time": float(testcase.get("time", 0)),
                        "status": "passed",
                    }

                    # Check for failures or errors
                    if testcase.find("failure") is not None:
                        case_info["status"] = "failed"
                        case_info["message"] = testcase.find("failure").get(
                            "message", ""
                        )
                    elif testcase.find("error") is not None:
                        case_info["status"] = "error"
                        case_info["message"] = testcase.find("error").get("message", "")
                    elif testcase.find("skipped") is not None:
                        case_info["status"] = "skipped"
                        case_info["message"] = testcase.find("skipped").get(
                            "message", ""
                        )

                    test_cases.append(case_info)

                summary["test_cases"] = test_cases
                return summary
            else:
                return {"error": "No testsuite element found in JUnit XML"}

        except Exception as e:
            return {"error": f"Failed to parse JUnit report: {e}"}

    def generate_rst_report(self) -> bool:
        """Generate RST files for inclusion in documentation."""
        print("\n📝 Generating RST reports...")

        # Parse reports
        coverage_data = self.parse_coverage_report()
        junit_data = self.parse_junit_report()

        # Generate main test report RST
        rst_content = self._generate_main_test_report(coverage_data, junit_data)

        # Write main test report
        test_report_file = self.docs_dir / "test_report.rst"
        try:
            with open(test_report_file, "w") as f:
                f.write(rst_content)
            print(f"✅ Generated main test report: {test_report_file}")
        except Exception as e:
            print(f"❌ Failed to write test report: {e}")
            return False

        # Generate coverage detail RST
        coverage_rst = self._generate_coverage_report(coverage_data)
        coverage_file = self.docs_dir / "test_coverage.rst"

        try:
            with open(coverage_file, "w") as f:
                f.write(coverage_rst)
            print(f"✅ Generated coverage report: {coverage_file}")
        except Exception as e:
            print(f"❌ Failed to write coverage report: {e}")
            return False

        return True

    def _generate_main_test_report(self, coverage_data: Dict, junit_data: Dict) -> str:
        """Generate the main test report RST content."""
        rst_lines = [
            "Test Reports",
            "============",
            "",
            "This page provides an overview of the test suite results and code coverage for the Financial Debt Optimizer.",
            "",
            f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]

        # Test Results Summary
        if "error" not in junit_data:
            rst_lines.extend(
                [
                    "Test Results Summary",
                    "-------------------",
                    "",
                    ".. list-table::",
                    "   :header-rows: 1",
                    "   :widths: 30 15 15 15 15 10",
                    "",
                    "   * - Metric",
                    "     - Total Tests",
                    "     - Passed",
                    "     - Failed",
                    "     - Skipped",
                    "     - Success Rate",
                    f"   * - Results",
                    f"     - {junit_data.get('total_tests', 0)}",
                    f"     - {junit_data.get('passed', 0)}",
                    f"     - {junit_data.get('failures', 0)}",
                    f"     - {junit_data.get('skipped', 0)}",
                    f"     - {junit_data.get('success_rate', 0)}%",
                    "",
                    f"**Test Execution Time:** {junit_data.get('time', 0):.2f} seconds",
                    "",
                ]
            )
        else:
            rst_lines.extend(
                [
                    "Test Results Summary",
                    "-------------------",
                    "",
                    f"❌ **Error:** {junit_data['error']}",
                    "",
                ]
            )

        # Coverage Summary
        if "error" not in coverage_data:
            rst_lines.extend(
                [
                    "Code Coverage Summary",
                    "--------------------",
                    "",
                    ".. list-table::",
                    "   :header-rows: 1",
                    "   :widths: 25 15 15 15 15 15",
                    "",
                    "   * - Metric",
                    "     - Total Lines",
                    "     - Covered Lines",
                    "     - Missing Lines",
                    "     - Coverage %",
                    "     - Files Analyzed",
                    f"   * - Coverage",
                    f"     - {coverage_data.get('total_statements', 0)}",
                    f"     - {coverage_data.get('covered_statements', 0)}",
                    f"     - {coverage_data.get('missing_statements', 0)}",
                    f"     - {coverage_data.get('coverage_percent', 0)}%",
                    f"     - {coverage_data.get('files_analyzed', 0)}",
                    "",
                ]
            )

            # Coverage by file (worst performers)
            files = coverage_data.get("files", [])[:10]  # Top 10 worst coverage
            if files:
                rst_lines.extend(
                    [
                        "Files Needing Attention (Lowest Coverage)",
                        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
                        "",
                        ".. list-table::",
                        "   :header-rows: 1",
                        "   :widths: 50 15 15 20",
                        "",
                        "   * - File",
                        "     - Statements",
                        "     - Missing",
                        "     - Coverage %",
                    ]
                )

                for file_info in files:
                    rst_lines.append(f"   * - ``{file_info['file']}``")
                    rst_lines.append(f"     - {file_info['statements']}")
                    rst_lines.append(f"     - {file_info['missing']}")
                    rst_lines.append(f"     - {file_info['coverage']}%")

                rst_lines.append("")
        else:
            rst_lines.extend(
                [
                    "Code Coverage Summary",
                    "--------------------",
                    "",
                    f"❌ **Error:** {coverage_data['error']}",
                    "",
                ]
            )

        # Links to detailed reports
        rst_lines.extend(
            [
                "Detailed Reports",
                "---------------",
                "",
                "* :doc:`test_coverage` - Detailed code coverage analysis",
                "* `Interactive Coverage Report <_static/test_reports/coverage_html/index.html>`_ - Browse coverage by file",
                "",
                ".. note::",
                "   Test reports are automatically generated during the documentation build process.",
                "   The interactive coverage report provides line-by-line coverage information.",
                "",
            ]
        )

        return "\n".join(rst_lines)

    def _generate_coverage_report(self, coverage_data: Dict) -> str:
        """Generate detailed coverage report RST content."""
        rst_lines = [
            "Test Coverage Details",
            "====================",
            "",
            "This page provides detailed information about code coverage across all project files.",
            "",
        ]

        if "error" not in coverage_data:
            rst_lines.extend(
                [
                    f"**Coverage Analysis Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    "",
                    f"**Overall Coverage:** {coverage_data.get('coverage_percent', 0)}%",
                    "",
                ]
            )

            # All files coverage table
            files = coverage_data.get("files", [])
            if files:
                rst_lines.extend(
                    [
                        "Coverage by File",
                        "---------------",
                        "",
                        ".. list-table::",
                        "   :header-rows: 1",
                        "   :widths: 60 15 15 10",
                        "",
                        "   * - File",
                        "     - Statements",
                        "     - Missing",
                        "     - Coverage %",
                    ]
                )

                for file_info in sorted(files, key=lambda x: x["file"]):
                    coverage_pct = file_info["coverage"]
                    # Add visual indicators
                    if coverage_pct >= 90:
                        indicator = "🟢"
                    elif coverage_pct >= 75:
                        indicator = "🟡"
                    else:
                        indicator = "🔴"

                    rst_lines.append(f"   * - {indicator} ``{file_info['file']}``")
                    rst_lines.append(f"     - {file_info['statements']}")
                    rst_lines.append(f"     - {file_info['missing']}")
                    rst_lines.append(f"     - {coverage_pct}%")

                rst_lines.extend(
                    [
                        "",
                        "**Legend:**",
                        "",
                        "* 🟢 Excellent coverage (≥90%)",
                        "* 🟡 Good coverage (75-89%)",
                        "* 🔴 Needs improvement (<75%)",
                        "",
                    ]
                )

            # Coverage goals and recommendations
            rst_lines.extend(
                [
                    "Coverage Goals and Recommendations",
                    "---------------------------------",
                    "",
                    "**Project Coverage Goals:**",
                    "",
                    "* **Target:** 85% overall coverage",
                    "* **Minimum:** 75% for all modules",
                    "* **Critical modules:** 95% coverage (core financial calculations)",
                    "",
                    "**Recommendations:**",
                    "",
                ]
            )

            # Generate specific recommendations based on coverage
            low_coverage_files = [f for f in files if f["coverage"] < 75]
            if low_coverage_files:
                rst_lines.extend(
                    [
                        "**Priority Actions:**",
                        "",
                    ]
                )
                for file_info in low_coverage_files[:5]:  # Top 5 priorities
                    rst_lines.append(
                        f"* Improve coverage for ``{file_info['file']}`` "
                        f"(currently {file_info['coverage']}%)"
                    )
                rst_lines.append("")

            rst_lines.extend(
                [
                    "**Best Practices:**",
                    "",
                    "* Write tests for all new features before implementation",
                    "* Focus on testing edge cases and error conditions",
                    "* Ensure financial calculation functions have comprehensive test coverage",
                    "* Test CLI commands and Excel I/O operations thoroughly",
                    "",
                ]
            )
        else:
            rst_lines.extend(
                [
                    f"❌ **Error generating coverage report:** {coverage_data['error']}",
                    "",
                    "Please ensure the test suite runs successfully and generates coverage data.",
                    "",
                ]
            )

        return "\n".join(rst_lines)

    def generate_reports(self) -> bool:
        """Generate all test reports for documentation."""
        print(f"\n📊 Generating test reports for documentation")

        success = True

        # Run test suite
        if not self.run_test_suite():
            print("⚠️  Test suite failed, but continuing with report generation...")

        # Generate RST reports
        success &= self.generate_rst_report()

        print(f"\n{'='*60}")
        print("📊 TEST REPORT GENERATION RESULTS")
        print("=" * 60)

        if success:
            print("✅ TEST REPORTS GENERATED SUCCESSFULLY!")
            print(f"📁 Reports directory: {self.reports_dir}")
            print(f"📄 Main report: {self.docs_dir / 'test_report.rst'}")
            print(f"📄 Coverage details: {self.docs_dir / 'test_coverage.rst'}")
        else:
            print("❌ TEST REPORT GENERATION HAD ISSUES!")

        return success


def main():
    """Main entry point for the test report generator."""
    parser = argparse.ArgumentParser(
        description="Generate test reports for Financial Debt Optimizer documentation"
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

    # Create report generator
    generator = TestReportGenerator(project_root, verbose=args.verbose)

    # Generate reports
    success = generator.generate_reports()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
