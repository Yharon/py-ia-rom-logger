from linecache import getline
import traceback as tb_module
from pathlib import Path
from datetime import datetime
from types import TracebackType

from rich.text import Text

from py_ia_rom_logger.config import SETTINGS


def truncate_string(s, max_length=100):
    if len(s) > max_length:
        return s[: max_length - 4] + " ..."
    return s


class TracebackRichFormatter:
    """Rich traceback formatter with structured table presentation.

    Formats exception tracebacks in a structured visual format
    for enhanced readability in console output.
    """

    _traceback_lines: list[str]
    _tb_list: tb_module.StackSummary
    _last_frames: list[tb_module.FrameSummary]

    _exc_title = (
        Text()
        .append("🐛 ", style="bold")
        .append("DEBUG", style="bold yellow")
        .append("INFO - ", style="bold red")
        .append(
            datetime.now(SETTINGS.TZ).strftime(SETTINGS.TIMESTAMP_FORMAT),
            style="bold white",
        )
    )

    def create_rich_traceback(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
    ) -> str:
        """Create formatted traceback in table format.

        Args:
            exc_type: Exception type.
            exc_value: Exception value.
            exc_traceback: Exception traceback, can be None.

        Returns:
            str: Formatted traceback as string.
        """
        self._configs(exc_traceback)
        self._cabecalho()
        self._formata_frames()
        self._format_exc_msg(exc_type, exc_value)

        return "\n".join(self._traceback_lines)

    def _format_exc_msg(
        self, exc_type: type[BaseException], exc_value: BaseException
    ) -> None:
        """Format exception message with styling.

        Args:
            exc_type: Exception type.
            exc_value: Exception value.
        """
        exc_name = exc_type.__name__
        exc_message = str(exc_value)

        self._traceback_lines.append(
            Text(f"\n🚨 {exc_name}: ", style="bold red").markup
        )
        self._traceback_lines.append(
            Text(f"    {str(exc_message)}", style="yellow").markup
        )

    def _configs(self, exc_traceback: TracebackType | None) -> None:
        """Initialize traceback configuration."""
        self._traceback_lines = []
        self._tb_list = tb_module.extract_tb(exc_traceback)
        self._last_frames = (
            self._tb_list[-SETTINGS.TRACEBACKS_MAX_FRAMES :] if self._tb_list else []
        )

    def _cabecalho(self) -> None:
        """Add traceback header."""
        self._traceback_lines.append("")

    def _formata_frames(self) -> None:
        """Format all traceback frames."""
        for i, frame in enumerate(self._last_frames):
            self._info_file(frame)
            self._info_lines(frame, i)

    def _info_lines(self, frame: tb_module.FrameSummary, frame_num: int) -> None:
        """Format frame line information.

        Args:
            frame: Frame summary from traceback.
            frame_num: Frame index number.
        """
        if frame.line and frame.lineno:
            lineno = frame.lineno

            if frame_num == len(self._last_frames) - 1:
                self._format_frame_lines(frame, lineno)
            else:
                self._format_frame_func(frame)

    def _format_frame_func(self, frame: tb_module.FrameSummary) -> None:
        """Format frame function name.

        Args:
            frame: Frame summary from traceback.
        """
        self._traceback_lines.append(
            f'{Text("    in", style="dim").markup} '
            f'{Text(frame.name, style="green").markup}'
        )

    def _format_frame_lines(self, frame: tb_module.FrameSummary, lineno: int) -> None:
        """Format frame lines with context.

        Args:
            frame: Frame summary from traceback.
            lineno: Line number of the error.
        """
        context = SETTINGS.TRACEBACKS_CONTEXT_LINES
        start = max(1, lineno - context)
        end = lineno + context

        for i in range(start, end + 1):
            line = getline(frame.filename, i).rstrip()
            formatted_line = self._format_indentation(line)
            if i == lineno:
                self._traceback_lines.append(
                    Text(
                        truncate_string(f"👀{i:4d}: {formatted_line}"),
                        style="bold white on red",
                    ).markup
                )
            else:
                self._traceback_lines.append(
                    truncate_string(f"  {i:4d}: {formatted_line}")
                )

    def _format_indentation(self, line: str) -> str:
        """Format frame indentation with visual guides.

        Args:
            line: Frame line to format.

        Returns:
            str: Formatted line with proper indentation.
        """
        INDENT_SPACES = 4

        # Calculate indentation spaces
        leading_spaces = len(line) - len(line.lstrip(" "))

        # Calculate indentation groups and leftover spaces
        groups = leading_spaces // INDENT_SPACES
        leftover = leading_spaces % INDENT_SPACES

        # 🎨 Visual: Replace each indent group with vertical bar guide
        vertical_indent = ("│" + " " * (INDENT_SPACES - 1)) * groups + " " * leftover

        return vertical_indent + line.lstrip().rstrip()

    def _info_file(self, frame: tb_module.FrameSummary) -> None:
        """Format and add frame file information to traceback.

        Args:
            frame: Frame summary from traceback.
        """
        file_path = Path(frame.filename)
        filename = file_path.name
        directory = (
            file_path.parent.name
            if file_path.parent.name != file_path.parent.anchor
            else ""
        )
        self._traceback_lines.append(
            f'📁 {directory}/{filename}{Text(":", style="dim").markup}'
            f'{Text(str(frame.lineno), style="magenta").markup}'
        )

    @property
    def exc_title(self) -> str:
        """Get formatted exception title.

        Returns:
            str: Exception title with Rich markup.
        """
        return self._exc_title.markup
