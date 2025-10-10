from collections.abc import Mapping, Sequence
from dataclasses import asdict as dataclasses_asdict
from dataclasses import dataclass, field, is_dataclass
from functools import cached_property
from re import VERBOSE
from re import Pattern as re_Pattern
from re import compile as re_compile
from typing import Any

from rich.theme import Theme


@dataclass
class LogModel:
    """Base log model for all logging models.

    Defines the core structure including log levels, placeholder regex
    patterns, and level mapping utilities.

    Attributes:
        LOG_LEVELS: Tuple of supported log levels in priority order.
        _PLACEHOLDER_RE: Regex pattern to identify and remove formatting
            placeholders like %s, %d, %.2f, %(name)s, etc.
    """

    LOG_LEVELS: tuple = field(
        init=False,
        default=(
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ),
    )

    # 🔧 Implementation: Regex to extract Python string formatting placeholders
    _PLACEHOLDER_RE: re_Pattern = field(
        init=False,
        default=re_compile(
            r"""
                %                       # starts with placeholder symbol
                (?:\([^)]+\))?          # optional: named placeholder %(name)s
                [-+#0\s]*               # formatting flags (alignment, padding)
                (?:\d+|\*)?             # field width (number or asterisk)
                (?:\.(?:\d+|\*))?       # decimal precision (for floats)
                [bcdeEfFgGnosxXrs%]     # final type specifier
            """,
            VERBOSE,
        ),
    )

    @cached_property
    def level_map(self) -> dict[str, str]:
        return dict(map(lambda k: (k, k[:4]), self.LOG_LEVELS))

    def remove_placeholders(self, text: str) -> str:
        """Remove Python formatting placeholders from log message.

        Extracts placeholders like %s, %d, %(field)s from the main message,
        keeping only the base text. Placeholder values are preserved
        separately in the 'customargs' field.

        Args:
            text: Log message with placeholders.

        Returns:
            str: Clean message without placeholders, extra spaces removed.

        Examples:
            >>> model.remove_placeholders("Processing user %s with ID %d")
            'Processing user with ID'
            >>> model.remove_placeholders("Field %(field_name)s: %.2f%%")
            'Field:'
        """
        return self._PLACEHOLDER_RE.sub("", text).strip()

    def jsonable(self, value, *, _seen: set[int] | None = None) -> Any:
        """Convert Python objects to JSON-serializable structures.

        Implements cascading strategy to handle different object types:
        1. Primitives (already JSON-compatible)
        2. Dataclasses (via asdict)
        3. Containers (dict, list, tuple) - recursive
        4. Objects with custom __repr__
        5. Objects with to_dict() method
        6. Objects with __dict__ attribute
        7. Fallback to string representation

        Args:
            value: Object to convert to JSON-compatible format.
            _seen: Internal set to track visited objects (prevents cycles).

        Returns:
            JSON-serializable version of the original object.

        Examples:
            >>> model.jsonable({"status": "success", "items": [1, 2, 3]})
            {'status': 'success', 'items': [1, 2, 3]}
        """
        # ⚠️ Warning: Track visited objects to prevent infinite recursion
        if _seen is None:
            _seen = set()
        obj_id = id(value)
        if obj_id in _seen:
            return str(value)
        _seen.add(obj_id)

        # 1) Primitives (already JSON-compatible)
        if value is None or isinstance(value, (str, int, float, bool)):
            return value

        # 2) Dataclasses
        if is_dataclass(value) and not isinstance(value, type):
            return {
                k: self.jsonable(v, _seen=_seen)
                for k, v in dataclasses_asdict(value).items()
            }

        # 3) Containers (dict, list, tuple) - recursive
        if isinstance(value, Mapping):
            return {k: self.jsonable(v, _seen=_seen) for k, v in value.items()}

        if isinstance(value, Sequence) and not isinstance(
            value, (str, bytes, bytearray)
        ):
            return [self.jsonable(v, _seen=_seen) for v in value]

        # 4) Objects with custom __repr__
        if type(value).__repr__ is not object.__repr__:
            return str(value)

        # 5) Objects with to_dict() method
        to_dict = getattr(value, "to_dict", None)
        if callable(to_dict):
            try:
                return self.jsonable(to_dict(), _seen=_seen)
            except Exception:
                pass

        # 6) Objects with __dict__ attribute
        if hasattr(value, "__dict__"):
            return {k: self.jsonable(v, _seen=_seen) for k, v in vars(value).items()}

        # 7) Fallback to string
        return str(value)


@dataclass
class CustomThemes:
    """Custom themes for Rich console logging."""

    DEFAULT: Theme = field(
        init=False,
        default_factory=lambda: Theme(
            {
                "debug": "blue",
                "info": "bright_white",
                "warning": "yellow",
                "error": "red",
                "critical": "bold red",
                "traceback": "dim bright_red",
            }
        ),
    )

    RICH: Theme = field(
        init=False,
        default_factory=lambda: Theme(
            {
                # DEBUG: muted colors for low priority
                "logging.level.DEBUG": "gray35",
                "logging.message.DEBUG": "bright_black",
                # INFO: bright white tones for clarity and distinction
                "logging.level.INFO": "bold white",
                "logging.message.INFO": "bright_white",
                # WARNING: yellow tones with emphasis
                "logging.level.WARNING": "bold white on yellow3",
                "logging.message.WARNING": "yellow2",
                # ERROR: red tones for visibility
                "logging.level.ERROR": "bright_red",
                "logging.message.ERROR": "red3",
                # CRITICAL: maximum emphasis with background
                "logging.level.CRITICAL": "bold white on bright_red",
                "logging.message.CRITICAL": "bold white on red3",
                # Traceback styling
                "traceback.code": "dim white",
                "traceback.locals": "dim blue",
            }
        ),
    )
