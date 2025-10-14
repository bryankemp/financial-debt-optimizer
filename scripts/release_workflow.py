#!/usr/bin/env python3
"""
Master release workflow for Financial Debt Optimizer.

This script orchestrates the complete release process by running all the
individual scripts in the correct order. It provides a single command to
run tests, clean code, build docs, bump version, and publish releases.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


class ReleaseWorkflow:
    """Orchestrates the complete release workflow."""

    def __init__(self, project_root: Path, verbose: bool = False):
        """Initialize the release workflow.

        Args:
            project_root: Path to the project root directory
            verbose: Whether to show detailed output
        """
        self.project_root = project_root
        self.scripts_dir = project_root / "scripts"
        self.verbose = verbose
        self.failed_steps: List[str] = []

    def run_script(
        self,
        script_name: str,
        args: List[str] = None,
        description: str = None,
        allow_failure: bool = False,
    ) -> bool:
        """Run a release script.

        Args:
            script_name: Name of the script to run (without .py extension)
            args: Optional arguments to pass to the script
            description: Human-readable description of the step
            allow_failure: Whether to continue if the script fails

        Returns:
            True if script succeeded, False otherwise
        """
        if args is None:
            args = []

        if description is None:
            description = f"Running {script_name}"

        script_path = self.scripts_dir / f"{script_name}.py"

        if not script_path.exists():
            print(f"❌ Script not found: {script_path}")
            if not allow_failure:
                self.failed_steps.append(description)
            return False

        cmd = [sys.executable, str(script_path)] + args

        if self.verbose:
            cmd.append("--verbose")

        print(f"\n{'='*60}")
        print(f"🔄 {description}")
        print(f"Script: {script_name}.py")
        if args:
            print(f"Args: {' '.join(args)}")
        print("=" * 60)

        try:
            result = subprocess.run(cmd, cwd=self.project_root, check=True)
            print(f"✅ {description} - SUCCESS")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ {description} - FAILED (exit code: {e.returncode})")
            if not allow_failure:
                self.failed_steps.append(description)
            return False

    def get_current_version(self) -> str:
        """Get the current version from __version__.py.

        Returns:
            Current version string
        """
        version_file = self.project_root / "src" / "__version__.py"

        if not version_file.exists():
            raise ValueError("Version file not found: src/__version__.py")

        content = version_file.read_text()

        # Look for __version__ = "x.y.z" pattern
        import re

        version_pattern = r'__version__\s*=\s*["\']([^"\']+)["\']'
        match = re.search(version_pattern, content)

        if not match:
            raise ValueError("Version not found in src/__version__.py")

        return match.group(1)

    def run_tests(self, skip_slow: bool = False, skip_security: bool = False) -> bool:
        """Run the complete test suite.

        Args:
            skip_slow: Whether to skip slow tests
            skip_security: Whether to skip security checks

        Returns:
            True if tests passed, False otherwise
        """
        args = []
        if skip_slow:
            args.append("--skip-slow")
        if skip_security:
            args.append("--skip-security")

        return self.run_script(
            "run_tests", args=args, description="Running comprehensive test suite"
        )

    def clean_code(self, skip_optional: bool = False) -> bool:
        """Clean and format the code.

        Args:
            skip_optional: Whether to skip optional cleanup steps

        Returns:
            True if cleanup succeeded, False otherwise
        """
        args = []
        if skip_optional:
            args.append("--skip-optional")

        return self.run_script(
            "clean_code", args=args, description="Cleaning and formatting code"
        )

    def build_documentation(self, include_pdf: bool = False) -> bool:
        """Build the documentation.

        Args:
            include_pdf: Whether to build PDF documentation

        Returns:
            True if build succeeded, False otherwise
        """
        args = []
        if include_pdf:
            args.append("--include-pdf")

        return self.run_script(
            "build_docs", args=args, description="Building documentation"
        )

    def bump_version(
        self, bump_type: str, prerelease: Optional[str] = None, dry_run: bool = False
    ) -> bool:
        """Bump the version number.

        Args:
            bump_type: Type of version bump ('major', 'minor', 'patch')
            prerelease: Optional prerelease identifier
            dry_run: Whether to perform a dry run

        Returns:
            True if version bump succeeded, False otherwise
        """
        args = [bump_type]

        if prerelease:
            args.extend(["--prerelease", prerelease])

        if dry_run:
            args.append("--dry-run")

        return self.run_script(
            "bump_version", args=args, description=f"Bumping version ({bump_type})"
        )

    def publish_release(
        self,
        test_pypi: bool = False,
        draft_release: bool = False,
        skip_github: bool = False,
        skip_pypi: bool = False,
    ) -> bool:
        """Publish the release.

        Args:
            test_pypi: Whether to upload to Test PyPI
            draft_release: Whether to create draft GitHub release
            skip_github: Whether to skip GitHub operations
            skip_pypi: Whether to skip PyPI operations

        Returns:
            True if publishing succeeded, False otherwise
        """
        args = []

        if test_pypi:
            args.append("--test-pypi")
        if draft_release:
            args.append("--draft")
        if skip_github:
            args.append("--skip-github")
        if skip_pypi:
            args.append("--skip-pypi")

        return self.run_script(
            "publish_release", args=args, description="Publishing release"
        )

    def run_full_workflow(
        self,
        bump_type: str,
        prerelease: Optional[str] = None,
        skip_tests: bool = False,
        skip_docs: bool = False,
        test_pypi: bool = False,
        draft_release: bool = False,
        dry_run: bool = False,
    ) -> bool:
        """Run the complete release workflow.

        Args:
            bump_type: Type of version bump
            prerelease: Optional prerelease identifier
            skip_tests: Whether to skip running tests
            skip_docs: Whether to skip building documentation
            test_pypi: Whether to upload to Test PyPI
            draft_release: Whether to create draft GitHub release
            dry_run: Whether to perform a dry run (no actual changes)

        Returns:
            True if workflow completed successfully, False otherwise
        """
        current_version = self.get_current_version()

        print(f"\n🚀 Starting complete release workflow for Financial Debt Optimizer")
        print(f"📋 Current version: {current_version}")
        print(f"📈 Bump type: {bump_type}")
        if prerelease:
            print(f"🏷️  Prerelease: {prerelease}")
        if dry_run:
            print("🔍 DRY RUN MODE - No permanent changes will be made")

        success = True

        # Step 1: Run tests (unless skipped)
        if not skip_tests:
            success &= self.run_tests()
        else:
            print("\n⚠️  SKIPPING TESTS - Use with caution!")

        # Step 2: Clean code
        if success or dry_run:
            success &= self.clean_code()

        # Step 3: Build documentation (unless skipped)
        if (success or dry_run) and not skip_docs:
            success &= self.build_documentation()
        elif skip_docs:
            print("\n⚠️  SKIPPING DOCUMENTATION BUILD")

        # Step 4: Bump version
        if success or dry_run:
            success &= self.bump_version(bump_type, prerelease, dry_run=dry_run)

        # Step 5: Publish release (unless dry run)
        if success and not dry_run:
            success &= self.publish_release(
                test_pypi=test_pypi, draft_release=draft_release
            )
        elif dry_run:
            print("\n🔍 DRY RUN - Skipping release publishing")

        # Report final results
        print(f"\n{'='*60}")
        print("📊 RELEASE WORKFLOW RESULTS")
        print("=" * 60)

        if success:
            if dry_run:
                print("✅ DRY RUN COMPLETED SUCCESSFULLY!")
                print("🔍 No changes were made to the repository")
                print("💡 Remove --dry-run flag to perform actual release")
            else:
                new_version = self.get_current_version()
                print("✅ RELEASE WORKFLOW COMPLETED SUCCESSFULLY!")
                print(f"🎉 Version {current_version} → {new_version} released")
                print(
                    f"🔗 GitHub: https://github.com/bryankemp/financial-debt-optimizer/releases"
                )
                if not test_pypi:
                    print(
                        f"📦 PyPI: https://pypi.org/project/financial-debt-optimizer/"
                    )
                else:
                    print(
                        f"📦 Test PyPI: https://test.pypi.org/project/financial-debt-optimizer/"
                    )
        else:
            print("❌ RELEASE WORKFLOW FAILED!")
            print("Failed steps:")
            for step in self.failed_steps:
                print(f"  - {step}")
            print("\n💡 Fix the issues above and try again")

        return success

    def run_quick_workflow(self, bump_type: str = "patch") -> bool:
        """Run a quick release workflow with minimal checks.

        This is useful for hotfix releases where you want to minimize the steps.

        Args:
            bump_type: Type of version bump (defaults to patch)

        Returns:
            True if workflow completed successfully, False otherwise
        """
        print(f"\n⚡ Starting QUICK release workflow")
        print("⚠️  This workflow has minimal safety checks!")

        success = True

        # Quick steps: clean code, bump version, publish
        success &= self.clean_code(skip_optional=True)

        if success:
            success &= self.bump_version(bump_type)

        if success:
            success &= self.publish_release(
                draft_release=True
            )  # Create as draft for safety

        if success:
            print("✅ QUICK RELEASE COMPLETED!")
            print("🏷️  GitHub release created as DRAFT - review before publishing")
        else:
            print("❌ QUICK RELEASE FAILED!")

        return success


def main():
    """Main entry point for the release workflow."""
    parser = argparse.ArgumentParser(
        description="Complete release workflow for Financial Debt Optimizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s patch                    # Patch release (1.0.0 -> 1.0.1)
  %(prog)s minor                    # Minor release (1.0.0 -> 1.1.0)  
  %(prog)s major                    # Major release (1.0.0 -> 2.0.0)
  %(prog)s patch --prerelease rc.1  # Prerelease (1.0.0 -> 1.0.1-rc.1)
  %(prog)s patch --dry-run          # Dry run (no changes)
  %(prog)s patch --test-pypi        # Upload to Test PyPI
  %(prog)s --quick                  # Quick workflow (hotfix)
        """,
    )

    parser.add_argument(
        "bump_type",
        nargs="?",
        choices=["major", "minor", "patch"],
        default="patch",
        help="Type of version bump to perform (default: patch)",
    )
    parser.add_argument(
        "--prerelease", help='Prerelease identifier (e.g., "alpha.1", "beta.2", "rc.1")'
    )
    parser.add_argument(
        "--skip-tests", action="store_true", help="Skip running tests (not recommended)"
    )
    parser.add_argument(
        "--skip-docs", action="store_true", help="Skip building documentation"
    )
    parser.add_argument(
        "--test-pypi",
        action="store_true",
        help="Upload to Test PyPI instead of main PyPI",
    )
    parser.add_argument(
        "--draft", action="store_true", help="Create draft GitHub release"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick workflow (minimal checks, draft release)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output from all scripts",
    )

    args = parser.parse_args()

    # Find project root
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent

    # Create workflow manager
    workflow = ReleaseWorkflow(project_root, verbose=args.verbose)

    # Run appropriate workflow
    if args.quick:
        success = workflow.run_quick_workflow(bump_type=args.bump_type)
    else:
        success = workflow.run_full_workflow(
            bump_type=args.bump_type,
            prerelease=args.prerelease,
            skip_tests=args.skip_tests,
            skip_docs=args.skip_docs,
            test_pypi=args.test_pypi,
            draft_release=args.draft,
            dry_run=args.dry_run,
        )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
