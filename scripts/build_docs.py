#!/usr/bin/env python3
"""
Documentation builder for Financial Debt Optimizer.

This script generates API documentation, builds HTML docs, and validates the documentation.
It can also clean up old documentation builds and prepare docs for release.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class DocumentationBuilder:
    """Manages building and validating documentation for the project."""

    def __init__(self, project_root: Path, verbose: bool = False):
        """Initialize the documentation builder.

        Args:
            project_root: Path to the project root directory
            verbose: Whether to show detailed output
        """
        self.project_root = project_root
        self.docs_dir = project_root / "docs"
        self.build_dir = self.docs_dir / "_build"
        self.verbose = verbose
        self.failed_steps: List[str] = []

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
                self.failed_steps.append(description)
            return False

    def check_dependencies(self) -> bool:
        """Check if documentation dependencies are available."""
        print("\n🔍 Checking documentation dependencies...")

        required_packages = [
            "sphinx",
            "sphinx_rtd_theme",
            "myst_parser",
            "pytest",
            "coverage",
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
                # Handle packages with different import names
                alt_names = {
                    "sphinx_rtd_theme": "sphinx_rtd_theme",
                    "myst_parser": "myst_parser",
                }
                alt_name = alt_names.get(package, package.replace("-", "_"))
                try:
                    subprocess.run(
                        [sys.executable, "-c", f"import {alt_name}"],
                        check=True,
                        capture_output=True,
                    )
                except subprocess.CalledProcessError:
                    missing_packages.append(package)

        # Check for sphinx-apidoc
        try:
            subprocess.run(
                ["sphinx-apidoc", "--version"], check=True, capture_output=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_packages.append("sphinx-apidoc")

        if missing_packages:
            print(f"❌ Missing packages: {', '.join(missing_packages)}")
            print("Install with: pip install -r docs/requirements.txt")
            return False

        print("✅ All documentation dependencies available")
        return True

    def clean_build_directory(self) -> bool:
        """Clean the documentation build directory."""
        print("\n🧹 Cleaning documentation build directory...")

        if self.build_dir.exists():
            try:
                shutil.rmtree(self.build_dir)
                print(f"✅ Cleaned build directory: {self.build_dir}")
            except OSError as e:
                print(f"❌ Failed to clean build directory: {e}")
                return False
        else:
            print("✅ Build directory already clean")

        return True

    def generate_api_docs(self) -> bool:
        """Generate API documentation using sphinx-apidoc."""
        print("\n📚 Generating API documentation...")

        api_docs_dir = self.docs_dir / "api"

        # Clean existing API docs
        if api_docs_dir.exists():
            try:
                shutil.rmtree(api_docs_dir)
                print(f"✅ Cleaned existing API docs: {api_docs_dir}")
            except OSError as e:
                print(f"⚠️  Could not clean API docs: {e}")

        # Generate new API docs
        return self.run_command(
            [
                "sphinx-apidoc",
                "-f",  # Force overwrite
                "-o",
                str(api_docs_dir),  # Output directory
                "src",  # Source directory
                "--separate",  # Create separate files for each module
                "--module-first",  # Put module documentation before submodule
                "--implicit-namespaces",  # Support PEP 420 implicit namespaces
            ],
            "Generate API documentation",
        )

    def build_html_docs(self) -> bool:
        """Build HTML documentation."""
        print("\n🏗️  Building HTML documentation...")

        return self.run_command(
            [
                sys.executable,
                "-m",
                "sphinx",  # Use Python module to ensure venv
                "-b",
                "html",  # Builder type
                "-j",
                "auto",  # Use multiple processes
                str(self.docs_dir),  # Source directory
                str(self.build_dir / "html"),  # Output directory
            ],
            "Build HTML documentation",
        )

    def build_pdf_docs(self) -> bool:
        """Build PDF documentation (if LaTeX is available)."""
        print("\n📄 Building PDF documentation...")

        # Check if pdflatex is available
        try:
            subprocess.run(["pdflatex", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  pdflatex not available, skipping PDF generation")
            return True

        # Build LaTeX first
        latex_success = self.run_command(
            [
                "sphinx-build",
                "-b",
                "latex",
                "-j",
                "auto",
                str(self.docs_dir),
                str(self.build_dir / "latex"),
            ],
            "Build LaTeX documentation",
            allow_failure=True,
        )

        if not latex_success:
            print("⚠️  LaTeX build failed, skipping PDF generation")
            return True

        # Build PDF from LaTeX
        latex_dir = self.build_dir / "latex"
        return self.run_command(
            ["make", "-C", str(latex_dir)], "Build PDF from LaTeX", allow_failure=True
        )

    def validate_links(self) -> bool:
        """Validate documentation links."""
        print("\n🔗 Validating documentation links...")

        return self.run_command(
            [
                "sphinx-build",
                "-b",
                "linkcheck",
                str(self.docs_dir),
                str(self.build_dir / "linkcheck"),
            ],
            "Validate documentation links",
            allow_failure=True,
        )

    def check_documentation_coverage(self) -> bool:
        """Check documentation coverage."""
        print("\n📊 Checking documentation coverage...")

        return self.run_command(
            [
                "sphinx-build",
                "-b",
                "coverage",
                str(self.docs_dir),
                str(self.build_dir / "coverage"),
            ],
            "Check documentation coverage",
            allow_failure=True,
        )

    def validate_build_output(self) -> bool:
        """Validate that documentation was built successfully."""
        print("\n✅ Validating build output...")

        html_dir = self.build_dir / "html"

        # Check that HTML directory exists
        if not html_dir.exists():
            print("❌ HTML documentation directory not found")
            return False

        # Check for main index file
        index_file = html_dir / "index.html"
        if not index_file.exists():
            print("❌ Main index.html file not found")
            return False

        # Check for basic structure
        required_files = ["genindex.html", "search.html"]
        missing_files = []

        for filename in required_files:
            if not (html_dir / filename).exists():
                missing_files.append(filename)

        if missing_files:
            print(f"⚠️  Missing HTML files: {', '.join(missing_files)}")

        # Count HTML files to ensure substantial content
        html_files = list(html_dir.rglob("*.html"))
        print(f"📄 Generated {len(html_files)} HTML files")

        if len(html_files) < 5:
            print("⚠️  Fewer HTML files than expected - documentation may be incomplete")

        print("✅ Documentation build validation passed")
        return True

    def create_documentation_report(self) -> None:
        """Create a summary report of documentation build."""
        print("\n📋 Creating documentation report...")

        report_file = self.build_dir / "build_report.txt"
        report_content = []

        report_content.append("Financial Debt Optimizer - Documentation Build Report")
        report_content.append("=" * 60)
        report_content.append("")

        # Build information
        html_dir = self.build_dir / "html"
        if html_dir.exists():
            html_files = list(html_dir.rglob("*.html"))
            report_content.append(f"HTML Files Generated: {len(html_files)}")

            # Calculate total size
            total_size = sum(f.stat().st_size for f in html_files)
            report_content.append(f"Total HTML Size: {total_size / 1024:.1f} KB")

        # API documentation
        api_dir = self.docs_dir / "api"
        if api_dir.exists():
            api_files = list(api_dir.glob("*.rst"))
            report_content.append(f"API Documentation Files: {len(api_files)}")

        # Coverage information
        coverage_dir = self.build_dir / "coverage"
        if coverage_dir.exists():
            coverage_file = coverage_dir / "python.txt"
            if coverage_file.exists():
                report_content.append("")
                report_content.append("Documentation Coverage:")
                with open(coverage_file, "r") as f:
                    report_content.extend(f.readlines()[:10])  # First 10 lines

        # Link check results
        linkcheck_dir = self.build_dir / "linkcheck"
        if linkcheck_dir.exists():
            output_file = linkcheck_dir / "output.txt"
            if output_file.exists():
                report_content.append("")
                report_content.append("Link Check Results:")
                with open(output_file, "r") as f:
                    lines = f.readlines()
                    if lines:
                        report_content.extend(lines[-5:])  # Last 5 lines

        # Write report
        try:
            with open(report_file, "w") as f:
                f.write("\n".join(report_content))
            print(f"📋 Documentation report saved to: {report_file}")
        except IOError as e:
            print(f"⚠️  Could not save documentation report: {e}")

    def build_complete_documentation(
        self, include_pdf: bool = False, validate: bool = True
    ) -> bool:
        """Build complete documentation suite.

        Args:
            include_pdf: Whether to build PDF documentation
            validate: Whether to run validation checks

        Returns:
            True if documentation built successfully, False otherwise
        """
        print(f"\n📖 Building complete documentation for {self.project_root.name}")

        # Check dependencies
        if not self.check_dependencies():
            return False

        success = True

        # Clean and prepare
        success &= self.clean_build_directory()

        # Generate API documentation
        success &= self.generate_api_docs()

        # Generate test reports (this will be called automatically by Sphinx extension,
        # but we can also run it manually here for standalone report generation)
        print("\n📊 Pre-generating test reports...")
        test_report_script = self.project_root / "scripts" / "generate_test_reports.py"
        if test_report_script.exists():
            self.run_command(
                [sys.executable, str(test_report_script)],
                "Generate test reports",
                allow_failure=True,  # Don't fail if test reports fail
            )

        # Build main documentation
        success &= self.build_html_docs()

        # Optional PDF build
        if include_pdf:
            self.build_pdf_docs()  # Don't fail if PDF build fails

        # Validation steps
        if validate:
            self.validate_links()  # Don't fail on link validation
            self.check_documentation_coverage()  # Don't fail on coverage

        # Final validation
        if success:
            success &= self.validate_build_output()

        # Create report
        self.create_documentation_report()

        # Report results
        print(f"\n{'='*60}")
        print("📊 DOCUMENTATION BUILD RESULTS")
        print("=" * 60)

        if success:
            print("✅ DOCUMENTATION BUILT SUCCESSFULLY!")
            print(f"📁 HTML documentation: {self.build_dir / 'html' / 'index.html'}")
            print(
                f"🌐 Open in browser: file://{self.build_dir / 'html' / 'index.html'}"
            )
        else:
            print("❌ DOCUMENTATION BUILD FAILED!")
            print("Failed steps:")
            for step in self.failed_steps:
                print(f"  - {step}")

        return success


def main():
    """Main entry point for the documentation builder."""
    parser = argparse.ArgumentParser(
        description="Build comprehensive documentation for Financial Debt Optimizer"
    )
    parser.add_argument(
        "--include-pdf",
        action="store_true",
        help="Build PDF documentation (requires LaTeX)",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip validation steps (faster build)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output from all commands",
    )
    parser.add_argument(
        "--clean-only",
        action="store_true",
        help="Only clean build directory, do not build",
    )

    args = parser.parse_args()

    # Find project root
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent

    # Create builder
    builder = DocumentationBuilder(project_root, verbose=args.verbose)

    # Handle clean-only mode
    if args.clean_only:
        success = builder.clean_build_directory()
        sys.exit(0 if success else 1)

    # Build documentation
    success = builder.build_complete_documentation(
        include_pdf=args.include_pdf, validate=not args.no_validate
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
