"""Tests for configuration module."""

from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from py_ia_rom_logger.config.config import Settings, get_prod_env_static, get_timezone


class TestGetProdEnvStatic:
    """Test suite for production environment detection."""

    def test_returns_boolean(self):
        """Test get_prod_env_static returns boolean value."""
        result = get_prod_env_static()

        assert isinstance(result, bool)


class TestGetTimezone:
    """Test suite for timezone configuration."""

    def test_returns_zoneinfo(self):
        """Test get_timezone returns ZoneInfo object."""
        tz = get_timezone()

        assert isinstance(tz, ZoneInfo)
        assert tz.key is not None

    def test_singleton_behavior(self):
        """Test that get_timezone returns same instance (singleton)."""
        tz1 = get_timezone()
        tz2 = get_timezone()

        # Should return same instance due to @singleton
        assert tz1 is tz2


class TestSettings:
    """Test suite for Settings class."""

    def test_settings_singleton_behavior(self):
        """Test Settings uses singleton pattern."""
        # Settings already instantiated globally in config/__init__.py
        settings1 = Settings(PROJECT_ROOT_=Path("/tmp/test1"), OS_WINDOWS=True)
        settings2 = Settings(PROJECT_ROOT_=Path("/tmp/test2"), OS_WINDOWS=False)

        # Should return same instance (global singleton)
        assert settings1 is settings2

    def test_settings_has_required_attributes(self):
        """Test Settings has all required attributes."""
        settings = Settings(PROJECT_ROOT_=Path("/tmp"), OS_WINDOWS=True)

        # Basic attributes
        assert hasattr(settings, "PROJECT_ROOT_")
        assert hasattr(settings, "OS_WINDOWS")
        assert hasattr(settings, "LOG_DIR")
        assert hasattr(settings, "TIMESTAMP_FORMAT")
        assert hasattr(settings, "TZ")

        # Config attributes
        assert hasattr(settings, "MAX_FILES")
        assert hasattr(settings, "ROBO_ID")
        assert hasattr(settings, "ROUND_ID")
        assert hasattr(settings, "TRACEBACKS_MAX_FRAMES")
        assert hasattr(settings, "TRACEBACKS_EXTRA_LINES")
        assert hasattr(settings, "TRACEBACKS_CONTEXT_LINES")

    def test_settings_log_dir_exists(self):
        """Test Settings LOG_DIR is a valid path."""
        settings = Settings(PROJECT_ROOT_=Path("/tmp"), OS_WINDOWS=True)

        assert isinstance(settings.LOG_DIR, Path)

    def test_settings_str_representation(self):
        """Test Settings __str__ method."""
        settings = Settings(PROJECT_ROOT_=Path("/tmp"), OS_WINDOWS=True)

        str_repr = str(settings)

        assert "Settings(" in str_repr
        assert "PROD_ENV=" in str_repr
        assert "LOG_DIR=" in str_repr
        assert "TZ=" in str_repr

    def test_settings_to_json(self):
        """Test Settings serialization to JSON."""
        settings = Settings(PROJECT_ROOT_=Path("/tmp"), OS_WINDOWS=True)

        json_str = settings.to_json

        assert isinstance(json_str, str)
        # Should be valid JSON string
        assert "{" in json_str
        assert "}" in json_str
