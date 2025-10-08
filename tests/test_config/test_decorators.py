"""Tests for decorator utilities."""

import pytest

from py_ia_rom_logger.config.decorators import singleton


class TestSingletonDecorator:
    """Test suite for singleton decorator."""

    def test_singleton_creates_single_instance(self):
        """Test that singleton decorator creates only one instance."""

        @singleton
        class TestClass:
            def __init__(self, value: int):
                self.value = value

        # Create two instances with different values
        instance1 = TestClass(10)
        instance2 = TestClass(20)

        # Both should reference the same object
        assert instance1 is instance2
        # Value should remain from first instantiation
        assert instance1.value == 10
        assert instance2.value == 10

    def test_singleton_persists_state(self):
        """Test that singleton maintains state across calls."""

        @singleton
        class Counter:
            def __init__(self):
                self.count = 0

            def increment(self):
                self.count += 1

        counter1 = Counter()
        counter1.increment()

        counter2 = Counter()
        counter2.increment()

        # Should have incremented twice on same instance
        assert counter1.count == 2
        assert counter2.count == 2
        assert counter1 is counter2

    def test_singleton_with_no_args(self):
        """Test singleton with class that takes no arguments."""

        @singleton
        class SimpleClass:
            pass

        instance1 = SimpleClass()
        instance2 = SimpleClass()

        assert instance1 is instance2

    def test_singleton_with_kwargs(self):
        """Test singleton with keyword arguments."""

        @singleton
        class ConfigClass:
            def __init__(self, *, debug: bool = False):
                self.debug = debug

        config1 = ConfigClass(debug=True)
        config2 = ConfigClass(debug=False)

        assert config1 is config2
        assert config1.debug is True  # First call wins
