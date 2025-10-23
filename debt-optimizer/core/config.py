"""
Configuration management for Financial Debt Optimizer.

Supports loading configuration from YAML files with CLI overrides.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class Config:
    """Configuration manager for debt optimizer."""

    DEFAULT_CONFIG_PATHS = [
        Path.home() / ".debt-optimizer",
        Path("debt-optimizer.yaml"),
        Path("debt-optimizer.yml"),
    ]

    DEFAULT_VALUES = {
        # File paths
        "input_file": "default.xlsx",
        "output_file": "debt_analysis.xlsx",
        "quicken_db_path": str(Path.home() / "Documents" / "Bryan.quicken" / "data"),
        # Analysis settings
        "optimization_goal": "minimize_interest",
        "extra_payment": 0.0,
        "emergency_fund": 1000.0,
        # Balance update settings
        "fuzzy_match_threshold": 80,
        "bank_account_name": "PECU Checking",
        "auto_backup": True,
        # Output settings
        "simple_report": False,
        "compare_strategies": False,
    }

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration.

        Args:
            config_path: Path to config file. If None, searches default locations.
        """
        self.config_path = config_path
        self._config: Dict[str, Any] = self.DEFAULT_VALUES.copy()

        if config_path:
            if not config_path.exists():
                raise FileNotFoundError(f"Config file not found: {config_path}")
            self.load_from_file(config_path)
        else:
            # Try to find config in default locations
            for path in self.DEFAULT_CONFIG_PATHS:
                if path.exists():
                    self.load_from_file(path)
                    break

    def load_from_file(self, path: Path) -> None:
        """Load configuration from YAML file.

        Args:
            path: Path to YAML config file

        Raises:
            ImportError: If PyYAML is not installed
            ValueError: If file is not valid YAML
        """
        if not HAS_YAML:
            raise ImportError(
                "PyYAML is required to load config files. "
                "Install it with: pip install pyyaml"
            )

        try:
            with open(path, "r", encoding="utf-8") as f:
                loaded = yaml.safe_load(f)
                if loaded:
                    self._config.update(loaded)
                self.config_path = path
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file {path}: {e}")

    def save_to_file(self, path: Optional[Path] = None) -> None:
        """Save current configuration to YAML file.

        Args:
            path: Path to save config. If None, uses current config_path.

        Raises:
            ImportError: If PyYAML is not installed
            ValueError: If no path specified and no config_path set
        """
        if not HAS_YAML:
            raise ImportError(
                "PyYAML is required to save config files. "
                "Install it with: pip install pyyaml"
            )

        save_path = path or self.config_path
        if not save_path:
            raise ValueError("No path specified for saving config")

        # Create parent directory if needed
        save_path.parent.mkdir(parents=True, exist_ok=True)

        with open(save_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self._config, f, default_flow_style=False, sort_keys=False)

        self.config_path = save_path

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        # Check environment variable override
        env_key = f"DEBT_OPTIMIZER_{key.upper()}"
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value

        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value

    def update(self, values: Dict[str, Any]) -> None:
        """Update multiple configuration values.

        Args:
            values: Dictionary of configuration values
        """
        self._config.update(values)

    def as_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary.

        Returns:
            Dictionary of all configuration values
        """
        return self._config.copy()

    def validate(self) -> tuple[bool, list[str]]:
        """Validate configuration values.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Validate fuzzy match threshold
        threshold = self.get("fuzzy_match_threshold")
        if not isinstance(threshold, (int, float)) or not (0 <= threshold <= 100):
            errors.append(
                f"fuzzy_match_threshold must be between 0 and 100, got: {threshold}"
            )

        # Validate extra payment
        extra = self.get("extra_payment")
        if not isinstance(extra, (int, float)) or extra < 0:
            errors.append(f"extra_payment must be >= 0, got: {extra}")

        # Validate emergency fund
        efund = self.get("emergency_fund")
        if not isinstance(efund, (int, float)) or efund < 0:
            errors.append(f"emergency_fund must be >= 0, got: {efund}")

        # Validate optimization goal
        goal = self.get("optimization_goal")
        valid_goals = ["minimize_interest", "minimize_time", "maximize_cashflow"]
        if goal not in valid_goals:
            errors.append(
                f"optimization_goal must be one of {valid_goals}, got: {goal}"
            )

        return (len(errors) == 0, errors)

    @classmethod
    def create_default_config(cls, path: Path) -> "Config":
        """Create a new configuration file with default values.

        Args:
            path: Path where to create the config file

        Returns:
            New Config instance
        """
        config = cls()
        config.save_to_file(path)
        return config
