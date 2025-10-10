"""Tests for base LogModel."""

from dataclasses import dataclass

import pytest
from py_ia_rom_logger.models._log_model import CustomThemes, LogModel


class TestLogModel:
    """Test suite for LogModel base class."""

    def test_log_levels_tuple(self):
        """Test LOG_LEVELS contains expected levels."""
        model = LogModel()

        assert model.LOG_LEVELS == ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

    def test_level_map_property(self):
        """Test level_map creates 4-letter codes."""
        model = LogModel()

        level_map = model.level_map

        assert level_map["DEBUG"] == "DEBU"
        assert level_map["INFO"] == "INFO"
        assert level_map["WARNING"] == "WARN"
        assert level_map["ERROR"] == "ERRO"
        assert level_map["CRITICAL"] == "CRIT"

    @pytest.mark.parametrize(
        "input_text,expected",
        [
            ("Processing user %s", "Processing user"),
            ("User %s with ID %d", "User  with ID"),
            ("Field %(name)s value %.2f", "Field  value"),
            ("Status: %s | Progress: %d of %d", "Status:  | Progress:  of"),
            ("No placeholders here", "No placeholders here"),
            ("", ""),
        ],
    )
    def test_remove_placeholders(self, input_text: str, expected: str):
        """Test remove_placeholders strips formatting codes."""
        model = LogModel()

        result = model.remove_placeholders(input_text)

        assert result == expected

    def test_jsonable_primitives(self, sample_dict_data: dict):
        """Test jsonable handles primitive types."""
        model = LogModel()

        result = model.jsonable(sample_dict_data)

        assert result["string"] == "test"
        assert result["number"] == 42
        assert result["float"] == 3.14
        assert result["boolean"] is True

    def test_jsonable_containers(self):
        """Test jsonable handles dict and list."""
        model = LogModel()

        data = {"list": [1, 2, 3], "dict": {"nested": "value"}}

        result = model.jsonable(data)

        assert result["list"] == [1, 2, 3]
        assert result["dict"]["nested"] == "value"

    def test_jsonable_dataclass(self):
        """Test jsonable converts dataclass to dict."""

        @dataclass
        class Person:
            name: str
            age: int

        model = LogModel()
        person = Person(name="John", age=30)

        result = model.jsonable(person)

        assert result == {"name": "John", "age": 30}

    def test_jsonable_custom_repr(self):
        """Test jsonable uses custom __repr__ when available."""

        class CustomClass:
            def __repr__(self):
                return "CustomObject(42)"

        model = LogModel()
        obj = CustomClass()

        result = model.jsonable(obj)

        assert result == "CustomObject(42)"

    def test_jsonable_with_to_dict_method(self):
        """Test jsonable uses to_dict() method when available."""

        class HasToDict:
            def to_dict(self):
                return {"method": "to_dict", "value": 123}

        model = LogModel()
        obj = HasToDict()

        result = model.jsonable(obj)

        assert result == {"method": "to_dict", "value": 123}

    def test_jsonable_with_dict_attribute(self):
        """Test jsonable uses __dict__ as fallback."""

        class SimpleObject:
            def __init__(self):
                self.attr1 = "value1"
                self.attr2 = 42

        model = LogModel()
        obj = SimpleObject()

        result = model.jsonable(obj)

        assert result["attr1"] == "value1"
        assert result["attr2"] == 42

    def test_jsonable_prevents_cycles(self):
        """Test jsonable handles circular references safely."""
        model = LogModel()

        circular = {"self": None}
        circular["self"] = circular # type: ignore

        # Should not raise RecursionError
        result = model.jsonable(circular)

        # Circular reference converted to string
        assert isinstance(result["self"], str)

    def test_jsonable_none_value(self):
        """Test jsonable handles None value."""
        model = LogModel()

        result = model.jsonable(None)

        assert result is None


class TestCustomThemes:
    """Test suite for CustomThemes."""

    def test_default_theme_exists(self):
        """Test DEFAULT theme is created."""
        themes = CustomThemes()

        assert themes.DEFAULT is not None
        assert hasattr(themes.DEFAULT, "styles")

    def test_rich_theme_exists(self):
        """Test RICH theme is created."""
        themes = CustomThemes()

        assert themes.RICH is not None
        assert hasattr(themes.RICH, "styles")

    def test_rich_theme_has_level_styles(self):
        """Test RICH theme contains all log level styles."""
        themes = CustomThemes()

        styles = themes.RICH.styles

        assert "logging.level.DEBUG" in styles
        assert "logging.level.INFO" in styles
        assert "logging.level.WARNING" in styles
        assert "logging.level.ERROR" in styles
        assert "logging.level.CRITICAL" in styles

    def test_rich_theme_has_message_styles(self):
        """Test RICH theme contains message styles."""
        themes = CustomThemes()

        styles = themes.RICH.styles

        assert "logging.message.DEBUG" in styles
        assert "logging.message.INFO" in styles
        assert "logging.message.WARNING" in styles
