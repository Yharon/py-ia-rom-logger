"""Rich formatter for console log output.

Provides Rich-formatted log messages with colors, styles,
and visual structuring for enhanced readability.
"""
import logging
from types import TracebackType

from rich.console import ConsoleRenderable, Group
from rich.json import JSON
from rich.markup import escape
from rich.panel import Panel
from rich.text import Text

from py_ia_rom_logger.models import ConsoleLogModel

from . import AbstractConsoleCustomFormatter
from .tracebacks.console_rich_traceback_formatter import TracebackRichFormatter


class RichFormatter(AbstractConsoleCustomFormatter):
    """Rich-based formatter for enhanced console logging.

    Applies Rich styling to log messages including level-specific colors,
    timestamp formatting, and visual information structuring.
    """

    def __init__(self) -> None:
        super().__init__()

        self._console_model = ConsoleLogModel()
        self._traceback = TracebackRichFormatter()

    def format_level(self, record: logging.LogRecord) -> str:
        """Format log level with 4-letter code and color.

        Args:
            record: Log record to format.

        Returns:
            str: 4-letter level code with Rich color markup.
        """
        level_name = record.levelname
        short_name = self._console_model.level_map.get(level_name, level_name[:4])
        color = self._console_model.rich_theme.styles.get(
            f"logging.level.{level_name}", ""
        )
        return Text(short_name, style=color).markup

    def format_message(self, record: logging.LogRecord) -> str:
        """Format log message with level-specific styling.

        Args:
            record: Log record to format.

        Returns:
            str: Formatted message with Rich markup.
        """
        message = escape(record.getMessage())
        color = self._console_model.rich_theme.styles.get(
            f"logging.message.{record.levelname}", ""
        )
        return Text(message, style=color).markup

    def format_arguments(self, record: logging.LogRecord) -> ConsoleRenderable:
        """Format log arguments as Rich JSON panel.

        Args:
            record: Log record with arguments.

        Returns:
            ConsoleRenderable: Group with message and JSON panel.
        """
        renderables: list[ConsoleRenderable] = []
        message = escape(record.msg)
        color = self._console_model.rich_theme.styles.get(
            f"logging.message.{record.levelname}", ""
        )

        msg_formatted = self._console_model.remove_placeholders(message)
        renderables.append(Text(msg_formatted, style=color))

        payload = (
            self._console_model.jsonable(record.args[0])
            if isinstance(record.args, tuple) and len(record.args) == 1
            else self._console_model.jsonable(record.args)
        )

        panel = Panel.fit(
            JSON.from_data(payload),
            title="Arguments",
            title_align="left",
            border_style=color,
        )
        renderables.append(panel)

        return Group(*renderables)

    def format_exception(
        self,
        ei: (
            tuple[type[BaseException], BaseException, TracebackType | None]
            | tuple[None, None, None]
        ),
    ) -> tuple[str, str]:
        """Format exception information with Rich traceback.

        Args:
            ei: Exception info tuple from sys.exc_info().

        Returns:
            tuple[str, str]: (formatted_traceback, exception_title)
                or ("", "") if no exception.
        """
        if not ei or ei == (None, None, None):
            return "", ""

        exc_type, exc_value, exc_traceback = ei
        if not exc_type or not exc_value or not exc_traceback:
            return "", ""

        return (
            self._traceback.create_rich_traceback(exc_type, exc_value, exc_traceback),
            self._traceback.exc_title
        )
