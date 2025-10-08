"""Tests for LoggingManager."""

import logging
import sys
import threading

import pytest

from py_ia_rom_logger.handlers import AvailableFileFormatters, AvailableFormatters
from py_ia_rom_logger.services.logging_manager_service import LoggingManager


class TestLoggingManager:
    """Test suite for LoggingManager."""

    def test_singleton_pattern(self):
        """Test LoggingManager is a singleton."""
        manager1 = LoggingManager()
        manager2 = LoggingManager()

        assert manager1 is manager2

    def test_initialization(self):
        """Test LoggingManager initializes with handlers."""
        manager = LoggingManager()

        assert manager.RICH_HANDLER is not None
        assert manager.FILE_HANDLER is not None
        assert manager.LOGGER is not None

    def test_setup_logging_adds_handlers(self, tmp_path, monkeypatch):
        """Test setup_logging adds console and file handlers."""
        # Mock log directory
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            log_dir,
        )

        # Clear any existing handlers
        manager = LoggingManager()
        manager.LOGGER.handlers.clear()

        manager.setup_logging()

        # Should have 2 handlers (console + file)
        assert len(manager.LOGGER.handlers) == 2

    def test_setup_logging_prevents_duplicates(self, tmp_path, monkeypatch):
        """Test setup_logging doesn't add duplicate handlers."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            log_dir,
        )

        manager = LoggingManager()
        manager.LOGGER.handlers.clear()

        # Call setup twice
        manager.setup_logging()
        initial_count = len(manager.LOGGER.handlers)

        manager.setup_logging()
        final_count = len(manager.LOGGER.handlers)

        # Should have same number of handlers
        assert initial_count == final_count

    def test_setup_logging_with_custom_formatters(self, tmp_path, monkeypatch):
        """Test setup_logging accepts custom formatters."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            log_dir,
        )

        manager = LoggingManager()
        manager.LOGGER.handlers.clear()

        # Should not raise
        manager.setup_logging(
            console_formatter=AvailableFormatters.RICH,
            file_formatter=AvailableFileFormatters.JSON,
            level="INFO",
        )

        assert manager.LOGGER.level == logging.INFO

    def test_setup_logging_sets_level(self, tmp_path, monkeypatch):
        """Test setup_logging sets correct log level."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            log_dir,
        )

        manager = LoggingManager()
        manager.LOGGER.handlers.clear()

        manager.setup_logging(level="WARNING")

        assert manager.LOGGER.level == logging.WARNING

    def test_get_logger_returns_root_logger(self):
        """Test get_logger returns root logger by default."""
        manager = LoggingManager()

        logger = manager.get_logger()

        assert logger is manager.LOGGER

    def test_get_logger_with_name(self):
        """Test get_logger returns named logger."""
        manager = LoggingManager()

        logger = manager.get_logger("test.module")

        assert logger.name == "test.module"
        assert isinstance(logger, logging.Logger)

    def test_exception_hooks_installed(self, tmp_path, monkeypatch):
        """Test setup_logging installs exception hooks."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            log_dir,
        )

        # Store original hooks
        original_excepthook = sys.excepthook
        original_threading_excepthook = (
            threading.excepthook if hasattr(threading, "excepthook") else None
        )

        manager = LoggingManager()
        manager.LOGGER.handlers.clear()
        manager.setup_logging()

        # Exception hooks should be modified
        assert sys.excepthook != original_excepthook

        if hasattr(threading, "excepthook"):
            assert threading.excepthook != original_threading_excepthook
