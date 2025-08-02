"""
Custom Exception Classes

This module defines custom exception classes for the markdown converter.
These exceptions provide specific error handling for different components.
"""

from typing import Any, Dict, Optional


class ParserError(Exception):
    """Exception raised when document parsing fails."""

    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        format_type: Optional[str] = None,
    ) -> None:
        """
        Initialize the parser error.

        :param message: Error message
        :param file_path: Path to the file that failed to parse
        :param format_type: Type of file format that failed
        """
        super().__init__(message)
        self.message = message
        self.file_path = file_path
        self.format_type = format_type


class UnsupportedFormatError(ParserError):
    """Exception raised when a file format is not supported."""

    def __init__(self, format_type: str, file_path: Optional[str] = None) -> None:
        """
        Initialize the unsupported format error.

        :param format_type: The unsupported format type
        :param file_path: Path to the unsupported file
        """
        message = f"Unsupported file format: {format_type}"
        super().__init__(message, file_path, format_type)


class ConfigurationError(Exception):
    """Exception raised when configuration is invalid."""

    def __init__(
        self,
        message: str,
        config_key: Optional[str] = None,
        config_value: Optional[Any] = None,
    ) -> None:
        """
        Initialize the configuration error.

        :param message: Error message
        :param config_key: Configuration key that caused the error
        :param config_value: Configuration value that caused the error
        """
        super().__init__(message)
        self.message = message
        self.config_key = config_key
        self.config_value = config_value


class ConversionError(Exception):
    """Exception raised when the overall conversion process fails."""

    def __init__(
        self,
        message: str,
        input_file: Optional[str] = None,
        output_file: Optional[str] = None,
    ) -> None:
        """
        Initialize the conversion error.

        :param message: Error message
        :param input_file: Path to the input file
        :param output_file: Path to the output file
        """
        super().__init__(message)
        self.message = message
        self.input_file = input_file
        self.output_file = output_file
