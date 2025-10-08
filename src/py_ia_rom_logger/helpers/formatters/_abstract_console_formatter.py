import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from types import TracebackType
from typing import Optional

from rich.console import ConsoleRenderable


@dataclass
class AbstractConsoleCustomFormatter(logging.Formatter, ABC):
    """Abstract base class for custom Rich log formatters.

    Defines the interface for Rich-based log formatting including
    themes, messages, exceptions, and arguments.

    Attributes:
        fmt: Format string for logs.
        datefmt: Format string for dates.
    """

    fmt: Optional[str] = field(default=None)
    datefmt: Optional[str] = field(default=None)

    def __post_init__(self):
        """Initialize parent Formatter after dataclass creation."""
        super().__init__(fmt=self.fmt, datefmt=self.datefmt, style="{")

    @abstractmethod
    def format_level(self, record: logging.LogRecord) -> str:
        """Format the log level with styling.

        Args:
            record: Log record to format.

        Returns:
            str: Formatted log level string.
        """

    @abstractmethod
    def format_message(self, record: logging.LogRecord) -> str:
        """Format the log message with styling.

        Args:
            record: Log record to format.

        Returns:
            str: Formatted message string.
        """

    @abstractmethod
    def format_exception(
        self,
        ei: (
            tuple[type[BaseException], BaseException, TracebackType | None]
            | tuple[None, None, None]
        ),
    ) -> tuple[str, str]:
        """Format the exception information.

        Args:
            ei: Exception info tuple from sys.exc_info().

        Returns:
            tuple[str, str]: (formatted_traceback, exception_title).
        """

    @abstractmethod
    def format_arguments(self, record: logging.LogRecord) -> ConsoleRenderable:
        """Format the log arguments with Rich rendering.

        Args:
            record: Log record with arguments.

        Returns:
            ConsoleRenderable: Rich renderable object.
        """
