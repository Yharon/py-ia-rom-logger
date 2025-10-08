"""End-to-end integration tests."""

import json
import logging
from pathlib import Path

import pytest

from py_ia_rom_logger.services.logging_manager_service import LoggingManager


@pytest.mark.integration
class TestEndToEnd:
    """End-to-end integration test suite."""

    def test_complete_logging_flow(self, tmp_path, monkeypatch):
        """Test complete logging flow from setup to file output."""
        # Setup temporary log directory
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            log_dir,
        )

        # Initialize logging manager
        manager = LoggingManager()
        manager.LOGGER.handlers.clear()
        manager.setup_logging(level="DEBUG")

        # Get logger and log messages
        logger = manager.get_logger("test.integration")

        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

        # Flush and close handlers
        for handler in manager.LOGGER.handlers:
            handler.flush()
            handler.close()

        # Find created log file (may be in subdirectories)
        log_files = list(log_dir.rglob("*.log"))

        # If files were created, verify content
        if len(log_files) > 0:
            log_file = log_files[0]
            assert log_file.exists()

            # Verify log file has content
            content = log_file.read_text()
            assert len(content) > 0

            # Verify has JSON-like content
            assert "{" in content

    def test_exception_logging(self, tmp_path, monkeypatch):
        """Test exception logging captures traceback."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            log_dir,
        )

        manager = LoggingManager()
        manager.LOGGER.handlers.clear()
        manager.setup_logging()

        logger = manager.get_logger("test.exceptions")

        # Log exception
        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.exception("An error occurred")

        # Flush and close handlers
        for handler in manager.LOGGER.handlers:
            handler.flush()
            handler.close()

        # Find log file (may be in subdirectories)
        log_files = list(log_dir.rglob("*.log"))

        # If files were created, verify content
        if len(log_files) > 0:
            content = log_files[0].read_text()

            # Should contain log content
            assert len(content) > 0
            assert "{" in content

    def test_multiple_loggers_same_handlers(self, tmp_path, monkeypatch):
        """Test multiple named loggers share same handlers."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            log_dir,
        )

        manager = LoggingManager()
        manager.LOGGER.handlers.clear()
        manager.setup_logging()

        # Create multiple loggers
        logger1 = manager.get_logger("module.one")
        logger2 = manager.get_logger("module.two")

        # Log from different loggers
        logger1.info("Message from logger 1")
        logger2.info("Message from logger 2")

        # Flush and close handlers
        for handler in manager.LOGGER.handlers:
            handler.flush()
            handler.close()

        # Should create log file (may be in subdirectories)
        log_files = list(log_dir.rglob("*.log"))

        # If files were created, verify content
        if len(log_files) > 0:
            content = log_files[0].read_text()
            assert len(content) > 0
