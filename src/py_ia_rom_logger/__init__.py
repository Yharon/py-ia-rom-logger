"""Custom logging library for Python projects with Rich console and JSON file output.

Provides structured logging with:
- Rich-formatted console output with colors and styling
- JSON-formatted file logging for analysis
- Exception tracking with detailed tracebacks
- Easy integration into existing projects
"""
from .services import LoggingManager


__all__ = ["LoggingManager"]
