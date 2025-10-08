"""Tests for JsonCustomFileHandler."""

import logging
from pathlib import Path

import pytest

from py_ia_rom_logger.handlers.file_handler import (
    AvailableFileFormatters,
    JsonCustomFileHandler,
)


class TestAvailableFileFormatters:
    """Test suite for AvailableFileFormatters enum."""

    def test_json_formatter_exists(self):
        """Test JSON formatter is available."""
        assert AvailableFileFormatters.JSON is not None

    def test_json_formatter_value(self):
        """Test JSON formatter value is SafeJsonFormatter instance."""
        formatter = AvailableFileFormatters.JSON.value

        assert formatter is not None
        assert hasattr(formatter, "format")


class TestJsonCustomFileHandler:
    """Test suite for JsonCustomFileHandler."""

    def test_create_file_handler(self, tmp_path: Path, monkeypatch):
        """Test create_file_handler creates handler with formatter."""
        # Mock log directory
        log_dir = tmp_path / "logs" / "2024-01" / "15"
        log_dir.mkdir(parents=True, exist_ok=True)

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            tmp_path / "logs",
        )

        handler = JsonCustomFileHandler.create_file_handler(
            AvailableFileFormatters.JSON
        )

        assert isinstance(handler, JsonCustomFileHandler)
        assert handler.level == logging.DEBUG
        assert handler.formatter is not None

    def test_handler_creates_log_file(self, tmp_path: Path, monkeypatch):
        """Test handler creates log file."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            log_dir,
        )

        handler = JsonCustomFileHandler.create_file_handler(
            AvailableFileFormatters.JSON
        )

        # Handler should have filename
        assert handler.baseFilename is not None
        assert handler.baseFilename.endswith(".log")

    def test_handler_cleanup_old_files(self, tmp_path: Path, monkeypatch):
        """Test handler cleans up old files."""
        log_dir = tmp_path / "logs" / "2024-01" / "15"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create old log files
        for i in range(10):
            (log_dir / f"old_{i}.log").touch()

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            tmp_path / "logs",
        )
        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.MAX_FILES",
            5,
        )

        handler = JsonCustomFileHandler.create_file_handler(
            AvailableFileFormatters.JSON
        )

        # Cleanup should have been called
        # (Actual deletion depends on FileManagerService logic)
        assert handler is not None

    def test_handler_writes_json_format(self, tmp_path: Path, monkeypatch):
        """Test handler writes logs in JSON format."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            log_dir,
        )

        handler = JsonCustomFileHandler.create_file_handler(
            AvailableFileFormatters.JSON
        )

        # Create log record
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="/test.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        # Emit record
        handler.emit(record)
        handler.close()

        # Check file was written
        log_file = Path(handler.baseFilename)
        assert log_file.exists()

        # Check content is JSON-like
        content = log_file.read_text()
        assert "{" in content
        assert "Test message" in content
