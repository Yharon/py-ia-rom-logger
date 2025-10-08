"""Tests for SystemInfoHelper."""

from datetime import datetime

import pytest

from py_ia_rom_logger.helpers.system_info_helper import SystemInfoHelper


class TestSystemInfoHelper:
    """Test suite for SystemInfoHelper."""

    def test_initialization(self, mock_system_info: SystemInfoHelper):
        """Test SystemInfoHelper initializes with system data."""
        info = mock_system_info

        assert info.hostname is not None
        assert info.username is not None
        assert info.platform is not None
        assert isinstance(info.timestamp, datetime)

    def test_str_representation(self, mock_system_info: SystemInfoHelper):
        """Test __str__ method provides readable output."""
        info = mock_system_info

        str_repr = str(info)

        assert "SystemInfo(" in str_repr
        assert "hostname=" in str_repr
        assert "username=" in str_repr
        assert "platform=" in str_repr
        assert "timestamp=" in str_repr

    def test_repr_equals_str(self, mock_system_info: SystemInfoHelper):
        """Test __repr__ returns same as __str__."""
        info = mock_system_info

        assert repr(info) == str(info)

    def test_to_json_property(self, mock_system_info: SystemInfoHelper):
        """Test to_json serializes to valid JSON string."""
        info = mock_system_info

        json_str = info.to_json

        assert isinstance(json_str, str)
        assert "{" in json_str
        assert "}" in json_str
        assert "hostname" in json_str
        assert "username" in json_str
        assert "platform" in json_str
        assert "timestamp" in json_str

    def test_to_json_timestamp_format(self, mock_system_info: SystemInfoHelper):
        """Test timestamp in JSON is ISO formatted."""
        info = mock_system_info

        json_str = info.to_json

        # Should contain timestamp field
        assert "timestamp" in json_str
        assert ":" in json_str  # Has time component

    def test_captures_real_system_data(self):
        """Test SystemInfoHelper captures actual system information."""
        info = SystemInfoHelper()

        # Should have non-empty values
        assert len(info.hostname) > 0
        assert len(info.username) > 0
        assert len(info.platform) > 0
        assert isinstance(info.timestamp, datetime)
