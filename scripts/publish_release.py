#!/usr/bin/env python3
"""
Release publishing script for Financial Debt Optimizer.

This script handles pushing releases to GitHub and publishing to PyPI.
It can create GitHub releases, upload packages to PyPI, and trigger
documentation builds on ReadTheDocs.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


class ReleasePublisher:
    """Manages publishing releases to various platforms."""

    def __init__(self, project_root: Path, verbose: bool = False):
        """Initialize the release publisher.

        Args:
            project_root: Path to the project root directory
            verbose: Whether to show detailed output
        """
        self.project_root = project_root
        self.verbose = verbose
        self.current_version: Optional[str] = None
        self.failed_steps: List[str] = []

    def run_command(
        self,
        cmd: List[str],
        description: str,
        allow_failure: bool = False,
        env: Optional[Dict] = None,
    ) -> bool:
        """Run a command and report results.

        Args:
            cmd: Command to run as a list of strings
            description: Human-readable description of the command
            allow_failure: Whether to continue if command fails
            env: Optional environment variables to set

        Returns:
            True if command succeeded, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"Running: {description}")
        if self.verbose:
            print(f"Command: {' '.join(cmd)}")
        print("=" * 60)

        # Merge environment variables
        run_env = os.environ.copy()
        if env:
            run_env.update(env)

        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                check=True,
                capture_output=not self.verbose,
                text=True,
                env=run_env,
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

    def get_current_version(self) -> str:
        """Get the current version from __version__.py.

        Returns:
            Current version string

        Raises:
            ValueError: If version cannot be found
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

        self.current_version = match.group(1)
        return self.current_version

    def check_git_status(self) -> bool:
        """Check if git repository is in a clean state for release.

        Returns:
            True if repository is ready for release, False otherwise
        """
        print("\n🔍 Checking Git repository status...")

        try:
            # Check if we're on main branch
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
            )
            current_branch = result.stdout.strip()

            if current_branch != "main":
                print(f"⚠️  Currently on branch '{current_branch}', should be on 'main'")
                print("Switch to main branch before releasing")
                return False

            # Check if working directory is clean
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
            )

            if result.stdout.strip():
                print("⚠️  Git working directory is not clean:")
                print(result.stdout)
                return False

            # Check if we have the version tag
            version = self.get_current_version()
            tag_name = f"v{version}"

            result = subprocess.run(
                ["git", "tag", "-l", tag_name],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
            )

            if not result.stdout.strip():
                print(f"⚠️  Version tag '{tag_name}' not found")
                print("Run version bump script first")
                return False

            print(f"✅ Git repository ready for release (v{version})")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to check git status: {e}")
            return False
        except FileNotFoundError:
            print("❌ Git not found")
            return False

    def push_to_github(self) -> bool:
        """Push changes and tags to GitHub.

        Returns:
            True if push succeeded, False otherwise
        """
        print("\n📤 Pushing changes to GitHub...")

        success = True

        # Push main branch
        success &= self.run_command(
            ["git", "push", "origin", "main"], "Push main branch to GitHub"
        )

        # Push tags
        success &= self.run_command(
            ["git", "push", "origin", "--tags"], "Push tags to GitHub"
        )

        return success

    def create_github_release(self, draft: bool = False) -> bool:
        """Create a GitHub release using gh CLI.

        Args:
            draft: Whether to create as draft release

        Returns:
            True if release creation succeeded, False otherwise
        """
        print("\n🏷️  Creating GitHub release...")

        # Check if gh CLI is available
        try:
            subprocess.run(["gh", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  GitHub CLI (gh) not found, skipping release creation")
            print("Install with: brew install gh")
            return True  # Don't fail the build

        version = self.get_current_version()
        tag_name = f"v{version}"

        # Read changelog for release notes
        changelog_path = self.project_root / "CHANGELOG.md"
        release_notes = f"Release version {version}"

        if changelog_path.exists():
            try:
                content = changelog_path.read_text()
                lines = content.split("\n")

                # Find this version's changelog entry
                start_idx = None
                end_idx = None

                for i, line in enumerate(lines):
                    if line.startswith(f"## [{version}]"):
                        start_idx = i + 1
                    elif start_idx is not None and line.startswith("## ["):
                        end_idx = i
                        break

                if start_idx is not None:
                    if end_idx is None:
                        end_idx = len(lines)

                    changelog_lines = lines[start_idx:end_idx]
                    # Remove empty lines at start and end
                    while changelog_lines and not changelog_lines[0].strip():
                        changelog_lines.pop(0)
                    while changelog_lines and not changelog_lines[-1].strip():
                        changelog_lines.pop()

                    if changelog_lines:
                        release_notes = "\n".join(changelog_lines)

            except Exception as e:
                print(f"⚠️  Could not read changelog: {e}")

        # Create release
        cmd = ["gh", "release", "create", tag_name]

        if draft:
            cmd.append("--draft")

        cmd.extend(["--title", f"Release {version}", "--notes", release_notes])

        return self.run_command(
            cmd,
            f"Create GitHub release {tag_name}",
            allow_failure=True,  # Don't fail if release already exists
        )

    def build_package(self) -> bool:
        """Build Python package for PyPI.

        Returns:
            True if build succeeded, False otherwise
        """
        print("\n📦 Building Python package...")

        # Clean previous builds
        dist_dir = self.project_root / "dist"
        if dist_dir.exists():
            import shutil

            try:
                shutil.rmtree(dist_dir)
                print("✅ Cleaned previous builds")
            except OSError as e:
                print(f"⚠️  Could not clean dist directory: {e}")

        # Check if build tools are available
        try:
            subprocess.run(
                [sys.executable, "-c", "import build"], check=True, capture_output=True
            )
        except subprocess.CalledProcessError:
            print("⚠️  'build' package not found, trying to install...")
            if not self.run_command(
                [sys.executable, "-m", "pip", "install", "build"],
                "Install build package",
            ):
                return False

        # Build package
        return self.run_command([sys.executable, "-m", "build"], "Build Python package")

    def check_package_quality(self) -> bool:
        """Check package quality with twine.

        Returns:
            True if package passes quality checks, False otherwise
        """
        print("\n🔍 Checking package quality...")

        # Check if twine is available
        try:
            subprocess.run(
                [sys.executable, "-c", "import twine"], check=True, capture_output=True
            )
        except subprocess.CalledProcessError:
            print("⚠️  'twine' package not found, trying to install...")
            if not self.run_command(
                [sys.executable, "-m", "pip", "install", "twine"],
                "Install twine package",
            ):
                return False

        # Check package
        return self.run_command(
            [sys.executable, "-m", "twine", "check", "dist/*"],
            "Check package quality with twine",
        )

    def upload_to_pypi(self, test_pypi: bool = False) -> bool:
        """Upload package to PyPI or Test PyPI.

        Args:
            test_pypi: Whether to upload to Test PyPI instead

        Returns:
            True if upload succeeded, False otherwise
        """
        repository_name = "Test PyPI" if test_pypi else "PyPI"
        print(f"\n📤 Uploading package to {repository_name}...")

        # Check if twine is available
        try:
            subprocess.run(
                [sys.executable, "-c", "import twine"], check=True, capture_output=True
            )
        except subprocess.CalledProcessError:
            print("❌ 'twine' package not found")
            return False

        cmd = [sys.executable, "-m", "twine", "upload"]

        if test_pypi:
            cmd.extend(["--repository", "testpypi"])

        cmd.append("dist/*")

        # Note: This will prompt for credentials or use stored credentials
        print("💡 Tip: Set TWINE_USERNAME and TWINE_PASSWORD environment variables")
        print(
            "💡 Or use: python -m twine upload --username __token__ --password <api-token>"
        )

        return self.run_command(cmd, f"Upload package to {repository_name}")

    def trigger_readthedocs_build(self) -> bool:
        """Trigger documentation build on ReadTheDocs.

        Returns:
            True if trigger succeeded, False otherwise
        """
        print("\n📚 Triggering ReadTheDocs build...")

        # ReadTheDocs should automatically build when tags are pushed
        # But we can also trigger manually if needed
        print("✅ ReadTheDocs will build automatically from pushed tags")
        print(
            "💡 Check build status at: https://readthedocs.org/projects/financial-debt-optimizer/"
        )

        return True

    def run_full_release(
        self,
        test_pypi: bool = False,
        draft_release: bool = False,
        skip_github: bool = False,
        skip_pypi: bool = False,
    ) -> bool:
        """Run complete release process.

        Args:
            test_pypi: Whether to upload to Test PyPI
            draft_release: Whether to create draft GitHub release
            skip_github: Whether to skip GitHub operations
            skip_pypi: Whether to skip PyPI operations

        Returns:
            True if release completed successfully, False otherwise
        """
        print(f"\n🚀 Starting release process for {self.project_root.name}")

        # Check prerequisites
        if not self.check_git_status():
            return False

        success = True

        # GitHub operations
        if not skip_github:
            success &= self.push_to_github()
            success &= self.create_github_release(draft=draft_release)

        # Package building and PyPI upload
        if not skip_pypi:
            success &= self.build_package()
            success &= self.check_package_quality()
            success &= self.upload_to_pypi(test_pypi=test_pypi)

        # Documentation
        success &= self.trigger_readthedocs_build()

        # Report results
        print(f"\n{'='*60}")
        print("📊 RELEASE RESULTS")
        print("=" * 60)

        if success:
            print("✅ RELEASE COMPLETED SUCCESSFULLY!")
            print(f"🎉 Version {self.get_current_version()} published")
            if not skip_github:
                print(
                    f"🔗 GitHub: https://github.com/bryankemp/financial-debt-optimizer/releases/tag/v{self.get_current_version()}"
                )
            if not skip_pypi:
                pypi_url = "https://test.pypi.org" if test_pypi else "https://pypi.org"
                print(f"📦 PyPI: {pypi_url}/project/financial-debt-optimizer/")
        else:
            print("❌ RELEASE HAD ISSUES!")
            print("Failed steps:")
            for step in self.failed_steps:
                print(f"  - {step}")

        return success


def main():
    """Main entry point for the release publisher."""
    parser = argparse.ArgumentParser(
        description="Publish release for Financial Debt Optimizer"
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
        "--skip-github",
        action="store_true",
        help="Skip GitHub operations (push, release)",
    )
    parser.add_argument(
        "--skip-pypi", action="store_true", help="Skip PyPI operations (build, upload)"
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

    # Run release
    publisher = ReleasePublisher(project_root, verbose=args.verbose)
    success = publisher.run_full_release(
        test_pypi=args.test_pypi,
        draft_release=args.draft,
        skip_github=args.skip_github,
        skip_pypi=args.skip_pypi,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
