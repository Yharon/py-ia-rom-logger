"""Tests for FileLogModel."""

from datetime import datetime

import pytest
from py_ia_rom_logger.models.file_log_model import FileLogModel


class TestFileLogModel:
    """Test suite for FileLogModel."""

    def test_initialization(self):
        """Test FileLogModel initializes with correct defaults."""
        model = FileLogModel()

        assert model.BACKUP_LOG_NAME is not None
        assert model.FORMAT_DATE_NAME == "%Y%m%d"
        assert model.FORMAT_TIME_NAME == "%H%M%S"
        assert hasattr(model, "_EMOJI_RE")

    def test_create_log_file_name_default(self):
        """Test create_log_file_name with default datetime."""
        model = FileLogModel()

        filename = model.create_log_file_name()

        # Should match pattern: {name}_{date}_{time}_{round}.log
        assert filename.endswith(".log")
        assert "_" in filename

    def test_create_log_file_name_custom_datetime(self, sample_datetime: datetime):
        """Test create_log_file_name with custom datetime."""
        model = FileLogModel()

        filename = model.create_log_file_name(date_=sample_datetime)

        # Should contain date: 20240115
        assert "20240115" in filename
        # Should contain time: 143025
        assert "143025" in filename
        # Should end with .log
        assert filename.endswith(".log")

    @pytest.mark.parametrize(
        "input_text,expected",
        [
            ("User processed! 😊✅", "User processed! "),
            ("Critical error ❌🚨", "Critical error "),
            ("Hello 🌍 World 🌟", "Hello  World "),
            ("No emojis here", "No emojis here"),
            ("", ""),
            ("🔥🔥🔥", ""),
        ],
    )
    def test_strip_emojis(self, input_text: str, expected: str):
        """Test strip_emojis removes emoji characters."""
        model = FileLogModel()

        result = model.strip_emojis(input_text)

        assert result == expected

    def test_strip_emojis_none_input(self):
        """Test strip_emojis handles None input."""
        model = FileLogModel()

        result = model.strip_emojis(None) # type: ignore

        assert result == ""

    def test_strip_emojis_unicode_symbols(self):
        """Test strip_emojis removes Unicode symbols."""
        model = FileLogModel()

        text_with_symbols = "Weather: ☀️ Temperature: 🌡️"

        result = model.strip_emojis(text_with_symbols)

        # Should remove weather symbols
        assert "☀" not in result
        assert "🌡" not in result

    def test_strip_emojis_preserves_text(self):
        """Test strip_emojis preserves regular text."""
        model = FileLogModel()

        text = "Processing data 😊 Complete!"

        result = model.strip_emojis(text)

        assert "Processing data" in result
        assert "Complete!" in result
        assert "😊" not in result

    def test_inherits_log_model_functionality(self):
        """Test FileLogModel inherits LogModel methods."""
        model = FileLogModel()

        # Should have LOG_LEVELS
        assert hasattr(model, "LOG_LEVELS")

        # Should have remove_placeholders
        result = model.remove_placeholders("Test %s")
        assert result == "Test"

        # Should have jsonable
        assert hasattr(model, "jsonable")

    def test_filename_pattern_consistency(self, sample_datetime):
        """Test filename follows consistent pattern."""
        model = FileLogModel()

        filename = model.create_log_file_name(date_=sample_datetime)

        # Pattern: {robot_id}_{part}_{date}_{time}_{round}.log
        parts = filename.replace(".log", "").split("_")

        assert len(parts) == 5  # robot, part, date, time, round
        assert parts[1] == "01"  # part_01
        assert parts[2] == "20240115"  # date
        assert parts[3] == "143025"  # time
        # parts[4] is round_id from SETTINGS (could be any value)
