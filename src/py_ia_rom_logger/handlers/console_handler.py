import logging
from enum import Enum

from rich.console import ConsoleRenderable
from rich.logging import RichHandler
from rich.panel import Panel
from rich.text import Text

from py_ia_rom_logger.config import SETTINGS
from py_ia_rom_logger.helpers.formatters import (
    AbstractConsoleCustomFormatter,
    RichFormatter,
)
from py_ia_rom_logger.models import ConsoleLogModel


class AvailableFormatters(Enum):
    """Available formatters for Rich logging.

    Attributes:
        RICH: Default Rich formatter for logs.
    """

    RICH = RichFormatter()


class ConsoleHandler(RichHandler):
    """Custom Rich handler with 4-letter level codes.

    Extends RichHandler to provide:
    - 4-letter level codes (DEBG, INFO, WARN, ERRO, CRIT)
    - Custom colors for each level
    - Consistent message formatting
    - Visual icons and symbols

    Args:
        console: Rich console instance to use.
        **kwargs: Additional arguments passed to RichHandler.
    """

    _formatter: AbstractConsoleCustomFormatter
    _console_log = ConsoleLogModel()

    def __init__(self, **kwargs):
        """Initialize ConsoleHandler with Rich console.

        Args:
            **kwargs: Additional arguments passed to RichHandler.
        """
        kwargs.setdefault("show_path", False)
        kwargs.setdefault("enable_link_path", False)
        kwargs.setdefault("log_time_format", f"[{SETTINGS.TIMESTAMP_FORMAT}]")
        kwargs.setdefault("rich_tracebacks", False)
        kwargs.setdefault("tracebacks_max_frames", SETTINGS.TRACEBACKS_MAX_FRAMES)
        kwargs.setdefault("tracebacks_extra_lines", SETTINGS.TRACEBACKS_MAX_FRAMES)
        kwargs.setdefault("console", self._console_log.create_rich_console())

        super().__init__(**kwargs)

    @classmethod
    def create_rich_handler(
        cls, formatter: AvailableFormatters, **kwargs
    ) -> "ConsoleHandler":
        """Create ConsoleHandler instance with custom configuration.

        Args:
            formatter: Formatter to use for log messages.
            **kwargs: Additional arguments passed to RichHandler.

        Returns:
            ConsoleHandler: Configured handler instance.
        """
        cls._formatter = formatter.value
        rich_handler = cls(**kwargs)

        rich_handler.setLevel(logging.DEBUG)
        rich_handler.setFormatter(cls._formatter)

        return rich_handler

    def get_level_text(self, record: logging.LogRecord) -> Text:
        """Get formatted log level text.

        Args:
            record: Log record.

        Returns:
            Text: Log level formatted with Rich color.
        """
        return Text.from_markup(self._formatter.format_level(record))

    def render_message(
        self, record: logging.LogRecord, message: str
    ) -> ConsoleRenderable:
        """Render log message with Rich formatting.

        Args:
            record: Log record.
            message: Message to render.

        Returns:
            ConsoleRenderable: Rendered message with Rich formatting.
        """
        if record.args:
            return self._formatter.format_arguments(record)
        msg_formatted = self._formatter.format_message(record)
        return Text.from_markup(msg_formatted)

    def emit(self, record: logging.LogRecord) -> None:
        """Emit log with enhanced visual formatting.

        Handles exception formatting specially for ERROR and CRITICAL levels.

        Args:
            record: Log record to emit.

        Note:
            Overrides base emit() to ensure proper exception formatting.
        """
        try:
            # ⚠️ Warning: Special handling for exceptions at ERROR+ levels
            if record.exc_info and record.levelno >= logging.ERROR:
                self._format_print_exc(record.getMessage(), record.exc_info)
            else:
                super().emit(record)
        except Exception:
            self.handleError(record)

    def _format_print_exc(self, text_log: str, exc_info) -> None:

        log_exc = self._formatter.format_exception(exc_info)
        text_exc = log_exc[0]
        title_exc = log_exc[1]

        self.console.print()
        self.console.print(text_log, style="bold white on red", justify="center")

        panel = Panel(
            text_exc,
            title=title_exc,
            title_align="left",
            border_style="red",
        )
        self.console.print(panel)
        self.console.print()
