"""Tests for logging configuration module."""

import logging
import tempfile
from pathlib import Path

import pytest

from debt_optimizer.core.logging_config import get_logger, setup_logging


class TestSetupLogging:
    """Test suite for setup_logging function."""

    def teardown_method(self):
        """Clean up logger handlers after each test."""
        logger = logging.getLogger("financial_debt_optimizer")
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    def test_setup_logging_default(self):
        """Test setup_logging with default parameters."""
        logger = setup_logging()
        assert logger.name == "financial_debt_optimizer"
        assert logger.level == logging.INFO
        assert len(logger.handlers) >= 1  # At least console handler

    def test_setup_logging_debug_level(self):
        """Test setup_logging with DEBUG level."""
        logger = setup_logging(level="DEBUG")
        assert logger.level == logging.DEBUG

    def test_setup_logging_warning_level(self):
        """Test setup_logging with WARNING level."""
        logger = setup_logging(level="WARNING")
        assert logger.level == logging.WARNING

    def test_setup_logging_error_level(self):
        """Test setup_logging with ERROR level."""
        logger = setup_logging(level="ERROR")
        assert logger.level == logging.ERROR

    def test_setup_logging_critical_level(self):
        """Test setup_logging with CRITICAL level."""
        logger = setup_logging(level="CRITICAL")
        assert logger.level == logging.CRITICAL

    def test_setup_logging_lowercase_level(self):
        """Test setup_logging handles lowercase level names."""
        logger = setup_logging(level="info")
        assert logger.level == logging.INFO

    def test_setup_logging_with_console_output(self):
        """Test setup_logging with console output enabled."""
        logger = setup_logging(console_output=True)
        console_handlers = [
            h
            for h in logger.handlers
            if isinstance(h, logging.StreamHandler)
            and not isinstance(h, logging.FileHandler)
        ]
        assert len(console_handlers) >= 1

    def test_setup_logging_without_console_output(self):
        """Test setup_logging with console output disabled."""
        logger = setup_logging(console_output=False)
        console_handlers = [
            h
            for h in logger.handlers
            if isinstance(h, logging.StreamHandler)
            and not isinstance(h, logging.FileHandler)
        ]
        assert len(console_handlers) == 0

    def test_setup_logging_with_file(self):
        """Test setup_logging with file handler."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = str(Path(tmpdir) / "test.log")
            logger = setup_logging(log_file=log_file)

            file_handlers = [
                h for h in logger.handlers if isinstance(h, logging.FileHandler)
            ]
            assert len(file_handlers) == 1
            assert Path(log_file).exists()

            # Close file handler explicitly for Windows compatibility
            for handler in file_handlers:
                handler.close()
                logger.removeHandler(handler)

    def test_setup_logging_file_invalid_path(self):
        """Test setup_logging handles invalid file path gracefully."""
        # This should not raise an exception, just log a warning
        logger = setup_logging(log_file="/nonexistent/directory/test.log")
        assert logger is not None

    def test_setup_logging_removes_existing_handlers(self):
        """Test setup_logging removes existing handlers."""
        # Setup twice to ensure handlers are replaced, not duplicated
        logger1 = setup_logging()
        handler_count_1 = len(logger1.handlers)

        logger2 = setup_logging()
        handler_count_2 = len(logger2.handlers)

        assert handler_count_1 == handler_count_2

    def test_setup_logging_formatter(self):
        """Test setup_logging creates proper formatter."""
        logger = setup_logging()
        assert len(logger.handlers) > 0

        handler = logger.handlers[0]
        assert handler.formatter is not None

        # Check that formatter includes expected components
        log_record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        formatted = handler.formatter.format(log_record)
        assert "Test message" in formatted

    def test_setup_logging_file_debug_level(self):
        """Test file handler always uses DEBUG level."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = str(Path(tmpdir) / "test.log")
            logger = setup_logging(level="INFO", log_file=log_file)

            file_handlers = [
                h for h in logger.handlers if isinstance(h, logging.FileHandler)
            ]
            assert len(file_handlers) == 1
            # File handler should always be DEBUG level
            assert file_handlers[0].level == logging.DEBUG

            # Close file handler explicitly for Windows compatibility
            for handler in file_handlers:
                handler.close()
                logger.removeHandler(handler)

    def test_setup_logging_write_log_message(self):
        """Test that setup_logging actually writes log messages."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = str(Path(tmpdir) / "test.log")
            logger = setup_logging(level="INFO", log_file=log_file)

            logger.info("Test log message")

            # Close file handler before reading to ensure all data is flushed
            file_handlers = [
                h for h in logger.handlers if isinstance(h, logging.FileHandler)
            ]
            for handler in file_handlers:
                handler.close()
                logger.removeHandler(handler)

            log_path = Path(log_file)
            assert log_path.exists()
            content = log_path.read_text()
            assert "Test log message" in content


class TestGetLogger:
    """Test suite for get_logger function."""

    def test_get_logger_default(self):
        """Test get_logger with no name."""
        logger = get_logger()
        assert logger.name == "financial_debt_optimizer"

    def test_get_logger_with_name(self):
        """Test get_logger with custom name."""
        logger = get_logger("custom_module")
        assert logger.name == "financial_debt_optimizer.custom_module"

    def test_get_logger_returns_same_instance(self):
        """Test get_logger returns the same instance for same name."""
        logger1 = get_logger("test")
        logger2 = get_logger("test")
        assert logger1 is logger2

    def test_get_logger_different_names(self):
        """Test get_logger returns different instances for different names."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        assert logger1 is not logger2
        assert logger1.name != logger2.name

    def test_get_logger_inherits_configuration(self):
        """Test get_logger inherits configuration from parent logger."""
        # Setup parent logger
        parent_logger = setup_logging(level="DEBUG")

        # Get child logger
        child_logger = get_logger("child")

        # Child should inherit parent's level
        assert child_logger.getEffectiveLevel() == logging.DEBUG
