"""
A custom logging library for RPA projects, designed to log messages in JSON format to a file, 
with support for different log levels and easy integration into existing projects.
"""
from .services import LoggingManager


__all__ = [
    "LoggingManager"
]
