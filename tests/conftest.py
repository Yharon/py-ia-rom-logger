"""Shared pytest fixtures for all tests.

Provides common fixtures for mocking, test data, and setup/teardown.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pytest


# ============================================================================
# Pytest Configuration Hooks
# ============================================================================


def pytest_configure(config):
    """Configure cache directories dynamically from environment variables.

    Uses RES_ROOT environment variable to set external cache locations.
    Falls back to project-local cache if RES_ROOT is not set.

    Args:
        config: Pytest configuration object.
    """
    res_root = os.environ.get('RES_ROOT')

    if res_root:
        cache_base = Path(res_root) / 'cache' / 'py-ia-rom-logger'

        # Pytest cache directory
        cache_dir = cache_base / '.pytest_cache'
        config.option.cache_dir = str(cache_dir)

        # Coverage data file
        coverage_file = cache_base / '.coverage'
        os.environ['COVERAGE_FILE'] = str(coverage_file)

        # Coverage HTML report directory
        html_dir = cache_base / 'htmlcov'
        os.environ['COVERAGE_HTML_DIR'] = str(html_dir)

        # Coverage XML report file
        xml_file = cache_base / 'coverage.xml'
        os.environ['COVERAGE_XML_FILE'] = str(xml_file)


# ============================================================================
# Configuration Fixtures
# ============================================================================


@pytest.fixture
def mock_settings(tmp_path: Path, monkeypatch):
    """Mock Settings object with temporary paths.

    Args:
        tmp_path: Pytest temporary directory fixture.
        monkeypatch: Pytest monkeypatch fixture.

    Returns:
        Mock Settings instance with safe temporary paths.
    """
    from py_ia_rom_logger.config.config import Settings

    # Create temp log directory
    log_dir = tmp_path / "logs"
    log_dir.mkdir()

    # Mock environment variables
    monkeypatch.setenv("LOG_DIR", str(log_dir))
    monkeypatch.setenv("ROBO_ID", "test_robot")
    monkeypatch.setenv("ROUND_ID", "99")
    monkeypatch.setenv("TIMEZONE", "UTC")

    settings = Settings(
        PROJECT_ROOT_=tmp_path,
        OS_WINDOWS=True,
    )

    return settings


@pytest.fixture
def mock_timezone():
    """Provide UTC timezone for consistent testing.

    Returns:
        ZoneInfo: UTC timezone.
    """
    return ZoneInfo("UTC")


# ============================================================================
# Logging Fixtures
# ============================================================================


@pytest.fixture
def sample_log_record() -> logging.LogRecord:
    """Create sample LogRecord for testing.

    Returns:
        logging.LogRecord: Sample log record with INFO level.
    """
    return logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="/test/path.py",
        lineno=42,
        msg="Test message",
        args=(),
        exc_info=None,
    )


@pytest.fixture
def sample_log_record_with_args() -> logging.LogRecord:
    """Create sample LogRecord with formatting arguments.

    Returns:
        logging.LogRecord: Log record with format args.
    """
    return logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="/test/path.py",
        lineno=42,
        msg="Processing user %s with ID %d",
        args=("John", 123),
        exc_info=None,
    )


@pytest.fixture
def sample_log_record_with_exception() -> logging.LogRecord:
    """Create sample LogRecord with exception info.

    Returns:
        logging.LogRecord: Log record with exception.
    """
    try:
        raise ValueError("Test error")
    except ValueError:
        import sys

        exc_info = sys.exc_info()

    return logging.LogRecord(
        name="test_logger",
        level=logging.ERROR,
        pathname="/test/path.py",
        lineno=42,
        msg="An error occurred",
        args=(),
        exc_info=exc_info,
    )


# ============================================================================
# Data Fixtures
# ============================================================================


@pytest.fixture
def sample_datetime(mock_timezone) -> datetime:
    """Provide fixed datetime for consistent testing.

    Args:
        mock_timezone: Timezone fixture.

    Returns:
        datetime: Fixed datetime (2024-01-15 14:30:25 UTC).
    """
    return datetime(2024, 1, 15, 14, 30, 25, tzinfo=mock_timezone)


@pytest.fixture
def sample_dict_data() -> dict[str, Any]:
    """Sample dictionary for JSON serialization tests.

    Returns:
        dict: Sample data with various types.
    """
    return {
        "string": "test",
        "number": 42,
        "float": 3.14,
        "boolean": True,
        "list": [1, 2, 3],
        "nested": {"key": "value"},
    }


# ============================================================================
# Mock Helpers
# ============================================================================


@pytest.fixture
def mock_system_info(monkeypatch, sample_datetime):
    """Mock SystemInfoHelper with consistent data.

    Args:
        monkeypatch: Pytest monkeypatch fixture.
        sample_datetime: Fixed datetime fixture.

    Returns:
        Mock SystemInfoHelper instance.
    """
    from py_ia_rom_logger.helpers.system_info_helper import SystemInfoHelper

    monkeypatch.setattr(
        "py_ia_rom_logger.helpers.system_info_helper.now",
        lambda: sample_datetime,
    )

    return SystemInfoHelper()


# ============================================================================
# File System Fixtures
# ============================================================================


@pytest.fixture
def temp_log_file(tmp_path: Path) -> Path:
    """Create temporary log file for testing.

    Args:
        tmp_path: Pytest temporary directory.

    Returns:
        Path: Path to temporary log file.
    """
    log_file = tmp_path / "test.log"
    log_file.touch()
    return log_file
