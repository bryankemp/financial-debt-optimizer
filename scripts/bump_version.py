#!/usr/bin/env python3
"""
Version bump script for Financial Debt Optimizer.

This script manages semantic versioning by incrementing version numbers
in all relevant files and preparing release tags.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class VersionBumper:
    """Manages version bumping for the project."""

    def __init__(self, project_root: Path, verbose: bool = False):
        """Initialize the version bumper.

        Args:
            project_root: Path to the project root directory
            verbose: Whether to show detailed output
        """
        self.project_root = project_root
        self.verbose = verbose
        self.version_files = [
            "src/__version__.py",
            "setup.py",
            "docs/conf.py",
        ]
        self.current_version: Optional[str] = None
        self.new_version: Optional[str] = None

    def log(self, message: str) -> None:
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            print(f"🔍 {message}")

    def parse_version(self, version_string: str) -> Tuple[int, int, int, Optional[str]]:
        """Parse a semantic version string.

        Args:
            version_string: Version string like "1.2.3" or "1.2.3-alpha.1"

        Returns:
            Tuple of (major, minor, patch, prerelease)

        Raises:
            ValueError: If version string is invalid
        """
        # Match semantic version pattern
        pattern = r"^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9\.\-]+))?$"
        match = re.match(pattern, version_string.strip())

        if not match:
            raise ValueError(f"Invalid version format: {version_string}")

        major, minor, patch = map(int, match.groups()[:3])
        prerelease = match.group(4)

        return major, minor, patch, prerelease

    def format_version(
        self, major: int, minor: int, patch: int, prerelease: Optional[str] = None
    ) -> str:
        """Format version components into a version string.

        Args:
            major: Major version number
            minor: Minor version number
            patch: Patch version number
            prerelease: Optional prerelease identifier

        Returns:
            Formatted version string
        """
        version = f"{major}.{minor}.{patch}"
        if prerelease:
            version += f"-{prerelease}"
        return version

    def get_current_version(self) -> str:
        """Get the current version from __version__.py.

        Returns:
            Current version string

        Raises:
            ValueError: If version cannot be found or parsed
        """
        version_file = self.project_root / "src" / "__version__.py"

        if not version_file.exists():
            raise ValueError("Version file not found: src/__version__.py")

        content = version_file.read_text()

        # Look for __version__ = "x.y.z" pattern
        version_pattern = r'__version__\s*=\s*["\']([^"\']+)["\']'
        match = re.search(version_pattern, content)

        if not match:
            raise ValueError("Version not found in src/__version__.py")

        version = match.group(1)
        self.log(f"Current version: {version}")

        # Validate version format
        self.parse_version(version)  # Will raise if invalid

        self.current_version = version
        return version

    def bump_version(self, bump_type: str, prerelease: Optional[str] = None) -> str:
        """Bump version according to type.

        Args:
            bump_type: Type of bump ('major', 'minor', 'patch')
            prerelease: Optional prerelease identifier

        Returns:
            New version string

        Raises:
            ValueError: If bump type is invalid or version parsing fails
        """
        if not self.current_version:
            self.get_current_version()

        major, minor, patch, current_prerelease = self.parse_version(
            self.current_version
        )

        # Handle prerelease versions
        if current_prerelease and bump_type in ["major", "minor", "patch"]:
            # If we have a prerelease and want to bump to release,
            # just remove prerelease for the same version
            if bump_type == "patch":
                new_version = self.format_version(major, minor, patch)
            elif bump_type == "minor":
                new_version = self.format_version(major, minor + 1, 0)
            else:  # major
                new_version = self.format_version(major + 1, 0, 0)
        else:
            # Normal version bumping
            if bump_type == "major":
                major += 1
                minor = 0
                patch = 0
            elif bump_type == "minor":
                minor += 1
                patch = 0
            elif bump_type == "patch":
                patch += 1
            else:
                raise ValueError(f"Invalid bump type: {bump_type}")

            new_version = self.format_version(major, minor, patch, prerelease)

        self.new_version = new_version
        self.log(f"New version: {new_version}")
        return new_version

    def update_version_file(self, file_path: str) -> bool:
        """Update version in a specific file.

        Args:
            file_path: Relative path to file to update

        Returns:
            True if file was updated, False otherwise
        """
        full_path = self.project_root / file_path

        if not full_path.exists():
            print(f"⚠️  File not found: {file_path}")
            return False

        try:
            content = full_path.read_text()
            original_content = content

            if file_path == "src/__version__.py":
                # Update __version__ = "x.y.z"
                content = re.sub(
                    r'(__version__\s*=\s*["\'])([^"\']+)(["\'])',
                    f"\\g<1>{self.new_version}\\g<3>",
                    content,
                )

            elif file_path == "setup.py":
                # Update version in setup.py fallback
                content = re.sub(
                    r'(__version__\s*=\s*["\'])([^"\']+)(["\'])',
                    f"\\g<1>{self.new_version}\\g<3>",
                    content,
                )

            elif file_path == "docs/conf.py":
                # Update version and release in Sphinx conf.py
                content = re.sub(
                    r'(version\s*=\s*["\'])([^"\']+)(["\'])',
                    f'\\g<1>{".".join(self.new_version.split(".")[:2])}\\g<3>',
                    content,
                )
                content = re.sub(
                    r'(release\s*=\s*["\'])([^"\']+)(["\'])',
                    f"\\g<1>{self.new_version}\\g<3>",
                    content,
                )

            # Only write if content changed
            if content != original_content:
                full_path.write_text(content)
                print(f"✅ Updated version in: {file_path}")
                return True
            else:
                print(f"⚠️  No version pattern found in: {file_path}")
                return False

        except Exception as e:
            print(f"❌ Failed to update {file_path}: {e}")
            return False

    def update_all_version_files(self) -> bool:
        """Update version in all relevant files.

        Returns:
            True if all files were updated successfully, False otherwise
        """
        if not self.new_version:
            raise ValueError("No new version set. Call bump_version() first.")

        print(
            f"\n📝 Updating version from {self.current_version} to {self.new_version}"
        )

        success = True
        updated_files = []

        for file_path in self.version_files:
            if self.update_version_file(file_path):
                updated_files.append(file_path)
            else:
                success = False

        print(f"\n📊 Updated {len(updated_files)} of {len(self.version_files)} files")

        return success

    def create_changelog_entry(self) -> bool:
        """Create or update changelog entry for new version.

        Returns:
            True if changelog was updated, False otherwise
        """
        changelog_path = self.project_root / "CHANGELOG.md"

        from datetime import datetime

        current_date = datetime.now().strftime("%Y-%m-%d")

        # Create new entry
        new_entry = f"""## [{self.new_version}] - {current_date}

### Added
- 

### Changed
- 

### Deprecated
- 

### Removed
- 

### Fixed
- 

### Security
- 

"""

        try:
            if changelog_path.exists():
                content = changelog_path.read_text()

                # Find where to insert (after # Changelog header)
                lines = content.split("\n")
                insert_index = 0

                for i, line in enumerate(lines):
                    if line.strip().startswith("## [") or line.strip().startswith(
                        "## Unreleased"
                    ):
                        insert_index = i
                        break
                    elif line.strip() == "# Changelog":
                        insert_index = i + 2  # Skip header and empty line
                        break

                # Insert new entry
                lines.insert(insert_index, new_entry.strip())
                new_content = "\n".join(lines)

            else:
                # Create new changelog
                new_content = f"""# Changelog

All notable changes to Financial Debt Optimizer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

{new_entry}"""

            changelog_path.write_text(new_content)
            print(f"✅ Created changelog entry for version {self.new_version}")
            return True

        except Exception as e:
            print(f"❌ Failed to update changelog: {e}")
            return False

    def validate_git_status(self) -> bool:
        """Check if git working directory is clean or has only expected changes.

        Returns:
            True if working directory is clean or has only expected changes, False otherwise
        """
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
            )

            if not result.stdout.strip():
                print("✅ Git working directory is clean")
                return True

            # Check if changes are only in expected files (test reports, formatting)
            changed_files = []
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    # Extract filename from git status output
                    # Handle both " M filename" and "M filename" formats
                    parts = line.strip().split(None, 1)
                    if len(parts) >= 2:
                        file_path = parts[1]
                        changed_files.append(file_path)

            # Define expected files that can be modified during release workflow
            expected_files = {
                "docs/test_coverage.rst",
                "docs/test_report.rst",
                # Allow any .py files that might have been reformatted
            }

            # Check if all changes are in expected files or Python files (formatting)
            unexpected_changes = []
            for file_path in changed_files:
                if (
                    file_path not in expected_files
                    and not file_path.endswith(".py")
                ):
                    unexpected_changes.append(file_path)

            if unexpected_changes:
                print("⚠️  Git working directory has unexpected changes:")
                for file_path in unexpected_changes:
                    print(f"  - {file_path}")
                print("Commit or stash unexpected changes before bumping version.")
                return False

            if changed_files:
                print(
                    "ℹ️  Found expected changes (test reports and/or code formatting):"
                )
                for file_path in changed_files:
                    print(f"  - {file_path}")
                print(
                    "✅ These changes will be committed as part of the release process"
                )

            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to check git status: {e}")
            return False
        except FileNotFoundError:
            print("⚠️  Git not found. Skipping git status check.")
            return True

    def commit_pre_release_changes(self) -> bool:
        """Commit any pre-release changes (test reports, formatting).

        Returns:
            True if commit was successful or no changes needed, False otherwise
        """
        try:
            # Check for any staged or unstaged changes that need to be committed
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
            )

            if not result.stdout.strip():
                return True  # No changes to commit

            # Get list of changed files
            changed_files = []
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    # Extract filename from git status output
                    # Handle both " M filename" and "M filename" formats
                    parts = line.strip().split(None, 1)
                    if len(parts) >= 2:
                        file_path = parts[1]
                        changed_files.append(file_path)

            # Filter for expected pre-release changes
            pre_release_files = []
            for file_path in changed_files:
                if (
                    file_path in {"docs/test_coverage.rst", "docs/test_report.rst"}
                    or file_path.endswith(".py")
                    and (file_path.startswith("src/") or file_path.startswith("tests/"))
                ):
                    pre_release_files.append(file_path)

            if not pre_release_files:
                return True  # No pre-release files to commit

            # Add and commit pre-release changes
            subprocess.run(
                ["git", "add"] + pre_release_files, cwd=self.project_root, check=True
            )

            subprocess.run(
                [
                    "git",
                    "commit",
                    "-m",
                    "chore: update test reports and code formatting for release",
                ],
                cwd=self.project_root,
                check=True,
            )

            print(f"✅ Committed pre-release changes: {len(pre_release_files)} files")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to commit pre-release changes: {e}")
            return False
        except FileNotFoundError:
            print("⚠️  Git not found. Skipping pre-release commit.")
            return True

    def create_git_commit(self, skip_commit: bool = False) -> bool:
        """Create git commit for version bump.

        Args:
            skip_commit: Whether to skip creating the commit

        Returns:
            True if commit was created successfully, False otherwise
        """
        if skip_commit:
            print("⚠️  Skipping git commit creation")
            return True

        try:
            # First commit any pre-release changes (test reports, formatting)
            if not self.commit_pre_release_changes():
                return False

            # Add version-related files
            changed_files = []
            for file_path in self.version_files:
                full_path = self.project_root / file_path
                if full_path.exists():
                    changed_files.append(file_path)

            # Add changelog if it exists
            changelog_path = self.project_root / "CHANGELOG.md"
            if changelog_path.exists():
                changed_files.append("CHANGELOG.md")

            if not changed_files:
                print("⚠️  No version files to commit")
                return True

            # Add version files to git
            subprocess.run(
                ["git", "add"] + changed_files, cwd=self.project_root, check=True
            )

            # Create version bump commit
            commit_message = f"release: bump version to {self.new_version}"
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=self.project_root,
                check=True,
            )

            print(f"✅ Created version bump commit: {commit_message}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create git commit: {e}")
            return False
        except FileNotFoundError:
            print("⚠️  Git not found. Skipping commit creation.")
            return True

    def create_git_tag(self, skip_tag: bool = False) -> bool:
        """Create git tag for new version.

        Args:
            skip_tag: Whether to skip creating the tag

        Returns:
            True if tag was created successfully, False otherwise
        """
        if skip_tag:
            print("⚠️  Skipping git tag creation")
            return True

        try:
            tag_name = f"v{self.new_version}"
            tag_message = f"Release version {self.new_version}"

            subprocess.run(
                ["git", "tag", "-a", tag_name, "-m", tag_message],
                cwd=self.project_root,
                check=True,
            )

            print(f"✅ Created git tag: {tag_name}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create git tag: {e}")
            return False
        except FileNotFoundError:
            print("⚠️  Git not found. Skipping tag creation.")
            return True

    def run_version_bump(
        self,
        bump_type: str,
        prerelease: Optional[str] = None,
        skip_git: bool = False,
        dry_run: bool = False,
    ) -> bool:
        """Run complete version bump process.

        Args:
            bump_type: Type of version bump
            prerelease: Optional prerelease identifier
            skip_git: Whether to skip git operations
            dry_run: Whether to perform a dry run (no changes)

        Returns:
            True if version bump completed successfully, False otherwise
        """
        print(f"\n🔄 Starting version bump ({bump_type})")

        try:
            # Get current version
            current = self.get_current_version()

            # Calculate new version
            new = self.bump_version(bump_type, prerelease)

            print(f"📈 Version bump: {current} → {new}")

            if dry_run:
                print("🔍 DRY RUN - No changes will be made")
                return True

            # Validate git status
            if not skip_git and not self.validate_git_status():
                return False

            success = True

            # Update version files
            success &= self.update_all_version_files()

            # Create changelog entry
            success &= self.create_changelog_entry()

            # Git operations
            if not skip_git:
                success &= self.create_git_commit()
                success &= self.create_git_tag()

            # Report results
            print(f"\n{'='*60}")
            print("📊 VERSION BUMP RESULTS")
            print("=" * 60)

            if success:
                print(f"✅ VERSION BUMP COMPLETED SUCCESSFULLY!")
                print(f"🎉 New version: {self.new_version}")
                if not skip_git:
                    print(f"🏷️  Git tag: v{self.new_version}")
                    print("💡 Push changes with: git push origin main --tags")
            else:
                print("❌ VERSION BUMP HAD ISSUES!")
                print("Check the output above for details")

            return success

        except Exception as e:
            print(f"❌ Version bump failed: {e}")
            return False


def main():
    """Main entry point for the version bumper."""
    parser = argparse.ArgumentParser(
        description="Bump version for Financial Debt Optimizer"
    )
    parser.add_argument(
        "bump_type",
        choices=["major", "minor", "patch"],
        help="Type of version bump to perform",
    )
    parser.add_argument(
        "--prerelease", help='Prerelease identifier (e.g., "alpha.1", "beta.2", "rc.1")'
    )
    parser.add_argument(
        "--skip-git", action="store_true", help="Skip git commit and tag creation"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )

    args = parser.parse_args()

    # Find project root
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent

    # Run version bump
    bumper = VersionBumper(project_root, verbose=args.verbose)
    success = bumper.run_version_bump(
        bump_type=args.bump_type,
        prerelease=args.prerelease,
        skip_git=args.skip_git,
        dry_run=args.dry_run,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
