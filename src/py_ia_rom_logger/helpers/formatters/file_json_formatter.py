"""Safe JSON formatter for file logging with sanitization.

Implements JSON formatting with emoji removal, placeholder extraction,
and safe object serialization for compatibility with legacy systems.
"""

from typing import Any

from pythonjsonlogger.json import JsonFormatter

from py_ia_rom_logger.models import FileLogModel

from .tracebacks.compact_traceback_formatter import CompactTracebackFormatter


class SafeJsonFormatter(JsonFormatter):
    """JSON formatter with sanitization for legacy systems.

    Extends JsonFormatter with:
    - Automatic emoji removal for legacy system compatibility
    - UTF-8 encoding preservation
    - Message and structured arguments separation
    - Safe complex object serialization

    Attributes:
        _file_model: Model for file-specific operations (emoji stripping, etc.).
        _tb_formatter: Traceback formatter for exception info.
    """

    def __init__(self, *args, **kwargs) -> None:
        # 🔧 Implementation: Extract max_frames before parent init
        max_frames = kwargs.pop("max_frames", 8)

        super().__init__(*args, **kwargs)

        self._file_model = FileLogModel()
        self._tb_formatter = CompactTracebackFormatter(max_frames=max_frames)

    def _sanitize_str(self, txt_: str) -> str:
        """Sanitize string by removing emojis and ensuring UTF-8 encoding.

        Args:
            txt_: String to sanitize.

        Returns:
            str: Sanitized string with UTF-8 encoding guaranteed.
        """
        # ⚠️ Warning: Remove emojis first for legacy system compatibility
        txt: str = self._file_model.strip_emojis(txt_)
        # 🔧 Implementation: Force UTF-8 with backslash escape for problematic chars
        return txt.encode("utf-8", "backslashreplace").decode("utf-8")

    def add_fields(self, log_record: dict, record: Any, message_dict: dict) -> None:
        """Add custom fields to JSON log record.

        Overrides base method to inject custom functionality:
        - Removes placeholders from main message
        - Injects structured arguments in separate field
        - Sanitizes all strings in the log

        Args:
            log_record: Log record dictionary being built.
            record: Original Python LogRecord object.
            message_dict: Dictionary of formatted messages.

        Note:
            Called automatically by JsonFormatter during formatting.
            Not intended for direct client code usage.
        """
        # Fill standard fields using base implementation
        super().add_fields(log_record, record, message_dict)

        # Override 'message' removing formatting placeholders
        raw_msg = str(getattr(record, "msg", ""))
        log_record["message"] = self._sanitize_str(
            self._file_model.remove_placeholders(raw_msg)
        )

        # Inject 'customargs' if formatting arguments exist
        if record.args:
            # Extract from tuple for single args to simplify parsing
            payload = (
                self._file_model.jsonable(record.args[0])
                if isinstance(record.args, tuple) and len(record.args) == 1
                else self._file_model.jsonable(record.args)
            )
            log_record["customargs"] = payload

        # Add exception info if present
        if record.exc_info:
            tb_str, exc_name, exc_msg = self._tb_formatter.format(record.exc_info)

            log_record["exc_info"] = self._sanitize_str(tb_str)
            log_record["exc_name"] = self._sanitize_str(exc_name)
            log_record["exc_message"] = self._sanitize_str(exc_msg)
