"""Tests for ConsoleLogModel."""

import pytest
from rich.console import Console

from py_ia_rom_logger.models.console_log_model import ConsoleLogModel


class TestConsoleLogModel:
    """Test suite for ConsoleLogModel."""

    def test_initialization(self):
        """Test ConsoleLogModel initializes correctly."""
        model = ConsoleLogModel()

        assert model.THEMES is not None
        assert hasattr(model, "DEFAULT_THEME")
        assert hasattr(model, "RICH_THEME")

    def test_rich_theme_property(self):
        """Test rich_theme property returns RICH_THEME."""
        model = ConsoleLogModel()

        theme = model.rich_theme

        assert theme == model.RICH_THEME
        assert hasattr(theme, "styles")

    def test_create_standard_console(self):
        """Test create_standard_console returns Console."""
        model = ConsoleLogModel()

        console = model.create_standard_console()

        assert isinstance(console, Console)

    def test_create_rich_console(self):
        """Test create_rich_console returns Console."""
        model = ConsoleLogModel()

        console = model.create_rich_console()

        assert isinstance(console, Console)

    def test_create_rich_console_with_kwargs(self):
        """Test create_rich_console accepts custom kwargs."""
        model = ConsoleLogModel()

        console = model.create_rich_console(width=80, legacy_windows=False)

        assert isinstance(console, Console)
        assert console.width == 80

    def test_create_rich_console_default_kwargs(self):
        """Test create_rich_console uses default kwargs."""
        model = ConsoleLogModel()

        console = model.create_rich_console()

        # Should create valid console
        assert isinstance(console, Console)

    def test_inherits_from_log_model(self):
        """Test ConsoleLogModel inherits LogModel functionality."""
        model = ConsoleLogModel()

        # Should have LOG_LEVELS from parent
        assert hasattr(model, "LOG_LEVELS")
        assert model.LOG_LEVELS == ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

        # Should have level_map from parent
        assert hasattr(model, "level_map")

    def test_remove_placeholders_inherited(self):
        """Test remove_placeholders method is inherited and works."""
        model = ConsoleLogModel()

        result = model.remove_placeholders("Test %s message")

        assert result == "Test  message"

    def test_jsonable_inherited(self):
        """Test jsonable method is inherited and works."""
        model = ConsoleLogModel()

        result = model.jsonable({"key": "value"})

        assert result == {"key": "value"}
