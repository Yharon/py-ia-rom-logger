"""Compact traceback formatter for JSON logging.

Generates a concise traceback representation limiting frame count
and displaying only essential information in format:

    path/relative.py:line  in function
    [...]
    path/relative.py:line  "source code"

Example (max_frames=8):
    examples/usage.py:88 in basic_usage
    examples/usage.py:46 in level_1
    examples/usage.py:55  "result = 10 / 0"
"""

from __future__ import annotations

import os
import traceback
from typing import List, Tuple


class CompactTracebackFormatter:
    """Compact traceback formatter for concise exception logging.

    Args:
        max_frames: Maximum number of frames to include (counting from bottom up).
            Defaults to 8.
        base_dir: Base directory for relative paths. Defaults to current directory.
    """

    def __init__(self, max_frames: int = 8, base_dir: str | None = None) -> None:
        self.max_frames = max_frames
        self.base_dir = base_dir or os.getcwd()

    def format(self, exc_info) -> Tuple[str, str, str]:
        """Format exception info into compact traceback representation.

        Args:
            exc_info: Exception info tuple from sys.exc_info().

        Returns:
            tuple: (traceback_str, exc_name, exc_msg) where:
                - traceback_str: Formatted traceback with lines separated by newline+space.
                - exc_name: Exception name (e.g., 'ZeroDivisionError').
                - exc_msg: Exception message/description.
        """
        exc_type, exc_val, tb = exc_info
        exc_name = exc_type.__name__ if exc_type else ""
        exc_msg = str(exc_val) if exc_val else ""

        frames = traceback.extract_tb(tb)
        # 🔧 Implementation: Get only last N frames (ascending path to origin)
        frames = frames[-self.max_frames :] if self.max_frames else frames

        formatted: List[str] = []
        for filename, lineno, func, text in frames[:-1]:
            rel = os.path.relpath(filename, self.base_dir)
            formatted.append(f"{rel}:{lineno} in {func}")

        # Last frame includes source code line
        if frames:
            filename, lineno, func, text = frames[-1]
            rel = os.path.relpath(filename, self.base_dir)
            code = (text or "").strip().replace('"', r"\"").replace("'", r"\'")
            formatted.append(f'{rel}:{lineno}  "{code}"')

        traceback_str = "\n ".join(formatted)
        return traceback_str, exc_name, exc_msg
