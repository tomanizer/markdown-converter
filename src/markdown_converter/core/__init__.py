"""
Core module for the markdown converter.

This module contains the core functionality including exceptions,
filesystem operations, and utility functions.
"""

from .exceptions import (
    ParserError,
    UnsupportedFormatError,
    ConfigurationError,
    ConversionError,
)

from .file_converter import FileConverter

__all__ = [
    # Exceptions
    "ParserError",
    "UnsupportedFormatError",
    "ConfigurationError",
    "ConversionError",
    # File conversion components
    "FileConverter",
]
