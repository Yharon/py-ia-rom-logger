from re import compile as re_compile, UNICODE as re_UNICODE, Pattern as re_Pattern
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from py_ia_rom_logger.config import SETTINGS

from . import LogModel


@dataclass
class FileLogModel(LogModel):
    """Log model for file output with naming and emoji stripping.

    Extends LogModel to provide file-specific functionality including
    log file naming patterns and emoji sanitization for legacy systems.

    Attributes:
        BACKUP_LOG_NAME: Base name for backup log files.
        FORMAT_DATE_NAME: Date format for log file names.
        FORMAT_TIME_NAME: Time format for log file names.
        _EMOJI_RE: Regex pattern to remove emojis and special Unicode chars.
    """

    _robo_id = SETTINGS.ROBO_ID
    _part_01 = "01"
    _full_name: str = field(init=False, default=f"{_robo_id}_{_part_01}")

    BACKUP_LOG_NAME: str = field(init=False, default=_full_name)
    FORMAT_DATE_NAME: str = field(init=False, default="%Y%m%d")
    FORMAT_TIME_NAME: str = field(init=False, default="%H%M%S")

    # 🔧 Implementation: Regex to remove emojis for legacy system compatibility
    _EMOJI_RE: re_Pattern = field(
        init=False,
        default=re_compile(
            "["
            "\U0001f600-\U0001f64f"  # emoticons (faces and gestures)
            "\U0001f300-\U0001f5ff"  # symbols & miscellaneous pictographs
            "\U0001f680-\U0001f6ff"  # transport & map symbols
            "\U0001f1e0-\U0001f1ff"  # flags (regional indicator symbols)
            "\U0001f900-\U0001f9ff"  # supplemental symbols and pictographs
            "\U0001fa00-\U0001fa6f"  # chess symbols
            "\U0001fa70-\U0001faff"  # symbols and pictographs extended-A
            "\u2600-\u26ff"  # miscellaneous symbols (weather, zodiac, etc.)
            "\u2700-\u27bf"  # dingbats (decorative symbols)
            "\u2300-\u23ff"  # miscellaneous technical
            "\u2b50"  # star
            "]+",
            flags=re_UNICODE,
        ),
    )

    def create_log_file_name(self, date_: Optional[datetime] = None) -> str:
        """Create log filename based on defined format pattern.

        Args:
            date_: Date to use for filename, defaults to current datetime.

        Returns:
            str: Formatted log filename (e.g., 'robot_01_20240115_143025_01.log').
        """
        if date_ is None:
            date_ = datetime.now(SETTINGS.TZ)

        name = self._full_name
        date_name = date_.strftime(self.FORMAT_DATE_NAME)
        hour_name = date_.strftime(self.FORMAT_TIME_NAME)
        round_id = SETTINGS.ROUND_ID

        return f"{name}_{date_name}_{hour_name}_{round_id}.log"

    def strip_emojis(self, text: str) -> str:
        """Remove emojis and decorative Unicode symbols from text.

        Essential for systems integrating with legacy platforms
        that don't support emojis or special Unicode characters.

        Args:
            text: Text to sanitize.

        Returns:
            str: Text without emojis, or empty string if input is None/empty.

        Examples:
            >>> model.strip_emojis("User processed! 😊✅")
            'User processed! '
            >>> model.strip_emojis("Critical error ❌🚨")
            'Critical error '
        """
        return self._EMOJI_RE.sub("", text) if text else ""
