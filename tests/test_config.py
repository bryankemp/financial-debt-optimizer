"""Tests for configuration management module."""

import os
import tempfile
from pathlib import Path

import pytest

from debt_optimizer.core.config import Config


class TestConfig:
    """Test suite for Config class."""

    def test_init_default(self):
        """Test Config initialization with defaults."""
        config = Config()
        assert config.get("input_file") == "default.xlsx"
        assert config.get("optimization_goal") == "minimize_interest"
        assert config.get("fuzzy_match_threshold") == 80

    def test_init_with_nonexistent_path(self):
        """Test Config initialization with nonexistent file raises error."""
        with pytest.raises(FileNotFoundError, match="Config file not found"):
            Config(config_path=Path("/nonexistent/path/config.yaml"))

    def test_get_default_value(self):
        """Test getting configuration with default value."""
        config = Config()
        assert config.get("nonexistent_key", "default_value") == "default_value"

    def test_get_with_env_override(self, monkeypatch):
        """Test environment variable overrides config value."""
        config = Config()
        monkeypatch.setenv("DEBT_OPTIMIZER_INPUT_FILE", "env_override.xlsx")
        assert config.get("input_file") == "env_override.xlsx"

    def test_set(self):
        """Test setting configuration value."""
        config = Config()
        config.set("custom_key", "custom_value")
        assert config.get("custom_key") == "custom_value"

    def test_update(self):
        """Test updating multiple configuration values."""
        config = Config()
        updates = {"key1": "value1", "key2": "value2"}
        config.update(updates)
        assert config.get("key1") == "value1"
        assert config.get("key2") == "value2"

    def test_as_dict(self):
        """Test getting configuration as dictionary."""
        config = Config()
        config_dict = config.as_dict()
        assert isinstance(config_dict, dict)
        assert "input_file" in config_dict
        assert config_dict["optimization_goal"] == "minimize_interest"

    def test_validate_success(self):
        """Test validation with valid configuration."""
        config = Config()
        is_valid, errors = config.validate()
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_fuzzy_threshold_too_low(self):
        """Test validation fails with fuzzy threshold below 0."""
        config = Config()
        config.set("fuzzy_match_threshold", -10)
        is_valid, errors = config.validate()
        assert is_valid is False
        assert len(errors) == 1
        assert "fuzzy_match_threshold" in errors[0]

    def test_validate_fuzzy_threshold_too_high(self):
        """Test validation fails with fuzzy threshold above 100."""
        config = Config()
        config.set("fuzzy_match_threshold", 150)
        is_valid, errors = config.validate()
        assert is_valid is False
        assert len(errors) == 1
        assert "fuzzy_match_threshold" in errors[0]

    def test_validate_fuzzy_threshold_non_numeric(self):
        """Test validation fails with non-numeric fuzzy threshold."""
        config = Config()
        config.set("fuzzy_match_threshold", "invalid")
        is_valid, errors = config.validate()
        assert is_valid is False
        assert "fuzzy_match_threshold" in errors[0]

    def test_validate_negative_extra_payment(self):
        """Test validation fails with negative extra payment."""
        config = Config()
        config.set("extra_payment", -100)
        is_valid, errors = config.validate()
        assert is_valid is False
        assert len(errors) == 1
        assert "extra_payment" in errors[0]

    def test_validate_negative_emergency_fund(self):
        """Test validation fails with negative emergency fund."""
        config = Config()
        config.set("emergency_fund", -500)
        is_valid, errors = config.validate()
        assert is_valid is False
        assert len(errors) == 1
        assert "emergency_fund" in errors[0]

    def test_validate_invalid_optimization_goal(self):
        """Test validation fails with invalid optimization goal."""
        config = Config()
        config.set("optimization_goal", "invalid_goal")
        is_valid, errors = config.validate()
        assert is_valid is False
        assert len(errors) == 1
        assert "optimization_goal" in errors[0]

    def test_validate_multiple_errors(self):
        """Test validation reports multiple errors."""
        config = Config()
        config.set("fuzzy_match_threshold", 150)
        config.set("extra_payment", -100)
        config.set("optimization_goal", "invalid")
        is_valid, errors = config.validate()
        assert is_valid is False
        assert len(errors) == 3


class TestConfigFileOperations:
    """Test suite for Config file operations (requires PyYAML)."""

    def test_save_and_load(self):
        """Test saving and loading configuration file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "test_config.yaml"

            # Create and save config
            config1 = Config()
            config1.set("test_key", "test_value")
            config1.save_to_file(config_path)

            assert config_path.exists()

            # Load config and verify
            config2 = Config(config_path=config_path)
            assert config2.get("test_key") == "test_value"

    def test_save_creates_parent_directory(self):
        """Test save_to_file creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "nested" / "dir" / "config.yaml"

            config = Config()
            config.save_to_file(config_path)

            assert config_path.exists()
            assert config_path.parent.exists()

    def test_save_without_path_raises_error(self):
        """Test save_to_file without path raises ValueError."""
        config = Config()
        with pytest.raises(ValueError, match="No path specified"):
            config.save_to_file()

    def test_save_with_explicit_path(self):
        """Test save_to_file with explicit path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"

            config = Config()
            config.save_to_file(config_path)

            assert config.config_path == config_path

    def test_load_invalid_yaml(self):
        """Test loading invalid YAML raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "invalid.yaml"
            config_path.write_text("invalid: yaml: content: [")

            with pytest.raises(ValueError, match="Invalid YAML"):
                Config(config_path=config_path)

    def test_load_empty_yaml(self):
        """Test loading empty YAML file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "empty.yaml"
            config_path.write_text("")

            config = Config(config_path=config_path)
            # Should still have default values
            assert config.get("input_file") == "default.xlsx"

    def test_create_default_config(self):
        """Test creating default configuration file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "default_config.yaml"

            config = Config.create_default_config(config_path)

            assert config_path.exists()
            assert config.get("input_file") == "default.xlsx"
            assert config.config_path == config_path

    def test_load_from_file_updates_config_path(self):
        """Test load_from_file updates config_path attribute."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"

            # Create initial config file
            Config.create_default_config(config_path)

            # Load into new config instance
            config = Config()
            config.load_from_file(config_path)

            assert config.config_path == config_path


class TestConfigDefaultPaths:
    """Test suite for Config default path searching."""

    def test_init_searches_default_paths(self, tmp_path, monkeypatch):
        """Test Config searches default paths when no path provided."""
        # Create a config in one of the default locations
        config_file = tmp_path / "debt_optimizer.yaml"
        config_file.write_text("test_key: test_value\n")

        # Mock DEFAULT_CONFIG_PATHS to include our test path
        monkeypatch.setattr(Config, "DEFAULT_CONFIG_PATHS", [config_file])

        config = Config()
        assert config.get("test_key") == "test_value"

    def test_init_without_default_paths_uses_defaults(self, monkeypatch):
        """Test Config uses default values when no config files found."""
        # Mock DEFAULT_CONFIG_PATHS to be empty
        monkeypatch.setattr(Config, "DEFAULT_CONFIG_PATHS", [])

        config = Config()
        assert config.get("input_file") == "default.xlsx"
