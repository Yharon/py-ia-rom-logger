"""Main logging system manager.

Coordinates all handlers and logging system configurations
using the Singleton pattern.
"""

import threading
import logging
import sys
from dataclasses import dataclass, field
from typing import Optional

from py_ia_rom_logger.config.decorators import singleton
from py_ia_rom_logger.handlers import (
    ConsoleHandler,
    AvailableFormatters,
    JsonCustomFileHandler,
    AvailableFileFormatters,
)


def _install_sys_excepthook(logger_: logging.Logger) -> None:
    """Register unhandled exceptions to logger.

    Args:
        logger_: Logger instance to capture exceptions.
    """
    def _hook(exc_type, exc_value, exc_tb):
        msg = "Unhandled exception"
        # Handle keyboard interrupts separately
        if issubclass(exc_type, KeyboardInterrupt):
            msg = "Keyboard interrupt exception"
        logger_.critical(msg, exc_info=(exc_type, exc_value, exc_tb))
    sys.excepthook = _hook


def _install_threading_excepthook(logger_: logging.Logger) -> None:
    """Capture thread exceptions (Python ≥3.8).

    Args:
        logger_: Logger instance to capture thread exceptions.
    """
    if hasattr(threading, "excepthook"):
        def _thread_hook(args: threading.ExceptHookArgs):  # type: ignore[attr-defined]
            name_ = args.thread.name if args.thread else "MainThread"
            msg = "Unhandled exception"
            if issubclass(args.exc_type, KeyboardInterrupt):
                msg = "Keyboard interrupt exception"
            logger_.critical(
                f"{msg} in thread {name_}",
                exc_info=(args.exc_type, args.exc_value, args.exc_traceback),  # type: ignore[attr-defined]
            )
        threading.excepthook = _thread_hook


@singleton
@dataclass
class LoggingManager:
    """Main logging system manager with singleton pattern.

    Ensures only one manager instance exists throughout program execution.

    Responsibilities:
    - Configure console and file handlers
    - Manage log directories
    - Clean old files
    - Coordinate formatters
    - Install exception hooks

    Attributes:
        RICH_HANDLER: Console handler factory.
        FILE_HANDLER: File handler factory.
        LOGGER: Root logger instance.
    """

    RICH_HANDLER: ConsoleHandler = field(init=False, default_factory=ConsoleHandler)
    FILE_HANDLER: JsonCustomFileHandler = field(
        init=False, default_factory=JsonCustomFileHandler
    )
    LOGGER: logging.Logger = field(init=False, default_factory=logging.getLogger)

    def setup_logging(
        self,
        *,
        console_formatter: AvailableFormatters = AvailableFormatters.RICH,
        file_formatter: AvailableFileFormatters = AvailableFileFormatters.JSON,
        level: str = "DEBUG",
    ) -> None:
        """Configure complete logging system.

        Creates and configures all necessary handlers:
        - Console handler with Rich formatting
        - JSON file handler with rotation

        Args:
            console_formatter: Formatter for console output.
            file_formatter: Formatter for file output.
            level: Global logging level.
        """
        # ⚠️ Warning: Skip if already configured to prevent duplicate handlers
        if self.LOGGER.hasHandlers():
            return

        # Create handlers
        console_handler = self.RICH_HANDLER.create_rich_handler(console_formatter)
        file_handler = self.FILE_HANDLER.create_file_handler(file_formatter)

        # Add handlers to logger
        self.LOGGER.addHandler(console_handler)
        self.LOGGER.addHandler(file_handler)

        # Set global level
        self.LOGGER.setLevel(level)

        # 🔧 Implementation: Install exception hooks for uncaught exceptions
        _install_sys_excepthook(self.LOGGER)
        _install_threading_excepthook(self.LOGGER)

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """Get configured logger instance.

        Args:
            name: Logger name, defaults to root logger.

        Returns:
            logging.Logger: Configured logger ready for use.
        """
        if name:
            return logging.getLogger(name)
        return self.LOGGER
