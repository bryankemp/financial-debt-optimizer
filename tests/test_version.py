"""Tests for version information module."""

import pytest

from debt_optimizer.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)


class TestVersion:
    """Test suite for version information."""

    def test_version_exists(self):
        """Test that version string exists and is non-empty."""
        assert __version__
        assert isinstance(__version__, str)
        assert len(__version__) > 0

    def test_version_format(self):
        """Test that version follows semantic versioning format."""
        # Basic check for X.Y.Z format
        parts = __version__.split(".")
        assert len(parts) >= 2  # At least major.minor

    def test_title_exists(self):
        """Test that title exists."""
        assert __title__
        assert isinstance(__title__, str)
        assert "Debt" in __title__ or "Financial" in __title__

    def test_description_exists(self):
        """Test that description exists."""
        assert __description__
        assert isinstance(__description__, str)
        assert len(__description__) > 0

    def test_author_exists(self):
        """Test that author information exists."""
        assert __author__
        assert isinstance(__author__, str)

    def test_author_email_exists(self):
        """Test that author email exists."""
        assert __author_email__
        assert isinstance(__author_email__, str)
        assert "@" in __author_email__

    def test_license_exists(self):
        """Test that license information exists."""
        assert __license__
        assert isinstance(__license__, str)

    def test_url_exists(self):
        """Test that URL exists."""
        assert __url__
        assert isinstance(__url__, str)
        assert __url__.startswith("http")
