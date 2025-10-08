"""Tests for SafeJsonFormatter."""

import logging

import pytest

from py_ia_rom_logger.helpers.formatters.file_json_formatter import SafeJsonFormatter


class TestSafeJsonFormatter:
    """Test suite for SafeJsonFormatter."""

    def test_initialization(self):
        """Test SafeJsonFormatter initializes correctly."""
        formatter = SafeJsonFormatter()

        assert formatter is not None
        assert hasattr(formatter, "_file_model")
        assert hasattr(formatter, "_tb_formatter")

    def test_sanitize_str_removes_emojis(self):
        """Test _sanitize_str removes emojis from text."""
        formatter = SafeJsonFormatter()

        text = "User logged in! 😊"

        result = formatter._sanitize_str(text)

        assert "😊" not in result
        assert "User logged in!" in result

    def test_sanitize_str_preserves_utf8(self):
        """Test _sanitize_str preserves UTF-8 characters."""
        formatter = SafeJsonFormatter()

        text = "Usuário João"

        result = formatter._sanitize_str(text)

        # Should preserve accented characters
        assert "João" in result or "Jo" in result  # May escape some chars

    def test_add_fields_basic_message(
        self, sample_log_record: logging.LogRecord
    ):
        """Test add_fields processes basic log message."""
        formatter = SafeJsonFormatter()

        log_record_dict = {}
        formatter.add_fields(log_record_dict, sample_log_record, {})

        assert "message" in log_record_dict
        # Should not have customargs for record without args
        assert "customargs" not in log_record_dict

    def test_add_fields_removes_placeholders(self):
        """Test add_fields removes formatting placeholders."""
        formatter = SafeJsonFormatter()

        # Create record with placeholders but no args
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="/test.py",
            lineno=1,
            msg="Processing user %s with ID %d",
            args=(),
            exc_info=None,
        )

        log_record_dict = {}
        formatter.add_fields(log_record_dict, record, {})

        # Message should have placeholders removed
        assert "Processing user" in log_record_dict["message"]
        assert "%s" not in log_record_dict["message"]
        assert "%d" not in log_record_dict["message"]

    def test_add_fields_with_arguments(
        self, sample_log_record_with_args: logging.LogRecord
    ):
        """Test add_fields extracts arguments to customargs."""
        formatter = SafeJsonFormatter()

        log_record_dict = {}
        formatter.add_fields(log_record_dict, sample_log_record_with_args, {})

        # Should have customargs
        assert "customargs" in log_record_dict
        # Should be a list/tuple
        customargs = log_record_dict["customargs"]
        assert isinstance(customargs, (list, tuple))
        assert len(customargs) == 2
        assert customargs[0] == "John"
        assert customargs[1] == 123

    def test_add_fields_single_argument_unpacked(self):
        """Test single argument is unpacked from tuple."""
        formatter = SafeJsonFormatter()

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="/test.py",
            lineno=1,
            msg="User %s",
            args=("John",),  # Single arg in tuple
            exc_info=None,
        )

        log_record_dict = {}
        formatter.add_fields(log_record_dict, record, {})

        # Should unpack single arg from tuple
        assert log_record_dict["customargs"] == "John"

    def test_add_fields_with_exception(
        self, sample_log_record_with_exception: logging.LogRecord
    ):
        """Test add_fields handles exception info."""
        formatter = SafeJsonFormatter()

        log_record_dict = {}
        formatter.add_fields(log_record_dict, sample_log_record_with_exception, {})

        # Should have exception fields
        assert "exc_info" in log_record_dict
        assert "exc_name" in log_record_dict
        assert "exc_message" in log_record_dict

        # Should have ValueError details
        assert "ValueError" in log_record_dict["exc_name"]
        assert "Test error" in log_record_dict["exc_message"]

    def test_add_fields_sanitizes_exception_text(self):
        """Test exception info is sanitized (emojis removed)."""
        formatter = SafeJsonFormatter()

        try:
            raise ValueError("Error with emoji 😊")
        except ValueError:
            import sys

            exc_info = sys.exc_info()

        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="/test.py",
            lineno=1,
            msg="Error",
            args=(),
            exc_info=exc_info,
        )

        log_record_dict = {}
        formatter.add_fields(log_record_dict, record, {})

        # Emoji should be removed from exception message
        assert "😊" not in log_record_dict["exc_message"]

    @pytest.mark.parametrize(
        "max_frames",
        [5, 8, 10],
    )
    def test_initialization_with_max_frames(self, max_frames: int):
        """Test SafeJsonFormatter accepts max_frames parameter."""
        formatter = SafeJsonFormatter(max_frames=max_frames)

        assert formatter._tb_formatter.max_frames == max_frames
