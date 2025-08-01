"""
Custom Exception Classes

This module defines custom exception classes for the markdown converter.
These exceptions provide specific error handling for different components.
"""

from typing import Optional, Any, Dict


class MarkdownConverterError(Exception):
    """Base exception class for all markdown converter errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the exception.
        
        :param message: Error message
        :param details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ParserError(MarkdownConverterError):
    """Exception raised when document parsing fails."""
    
    def __init__(self, message: str, file_path: Optional[str] = None, format_type: Optional[str] = None) -> None:
        """
        Initialize the parser error.
        
        :param message: Error message
        :param file_path: Path to the file that failed to parse
        :param format_type: Type of file format that failed
        """
        details = {
            "file_path": file_path,
            "format_type": format_type,
            "error_type": "parser_error"
        }
        super().__init__(message, details)


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


class ProcessorError(MarkdownConverterError):
    """Exception raised when content processing fails."""
    
    def __init__(self, message: str, content_type: Optional[str] = None, processor_name: Optional[str] = None) -> None:
        """
        Initialize the processor error.
        
        :param message: Error message
        :param content_type: Type of content that failed to process
        :param processor_name: Name of the processor that failed
        """
        details = {
            "content_type": content_type,
            "processor_name": processor_name,
            "error_type": "processor_error"
        }
        super().__init__(message, details)


class FormatterError(MarkdownConverterError):
    """Exception raised when output formatting fails."""
    
    def __init__(self, message: str, output_type: Optional[str] = None, formatter_name: Optional[str] = None) -> None:
        """
        Initialize the formatter error.
        
        :param message: Error message
        :param output_type: Type of output format that failed
        :param formatter_name: Name of the formatter that failed
        """
        details = {
            "output_type": output_type,
            "formatter_name": formatter_name,
            "error_type": "formatter_error"
        }
        super().__init__(message, details)


class ConfigurationError(MarkdownConverterError):
    """Exception raised when configuration is invalid."""
    
    def __init__(self, message: str, config_key: Optional[str] = None, config_value: Optional[Any] = None) -> None:
        """
        Initialize the configuration error.
        
        :param message: Error message
        :param config_key: Configuration key that caused the error
        :param config_value: Configuration value that caused the error
        """
        details = {
            "config_key": config_key,
            "config_value": config_value,
            "error_type": "configuration_error"
        }
        super().__init__(message, details)


class FilesystemError(MarkdownConverterError):
    """Exception raised when filesystem operations fail."""
    
    def __init__(self, message: str, operation: Optional[str] = None, path: Optional[str] = None) -> None:
        """
        Initialize the filesystem error.
        
        :param message: Error message
        :param operation: Filesystem operation that failed
        :param path: Path involved in the failed operation
        """
        details = {
            "operation": operation,
            "path": path,
            "error_type": "filesystem_error"
        }
        super().__init__(message, details)


class PandocError(MarkdownConverterError):
    """Exception raised when pandoc operations fail."""
    
    def __init__(self, message: str, pandoc_command: Optional[str] = None, exit_code: Optional[int] = None) -> None:
        """
        Initialize the pandoc error.
        
        :param message: Error message
        :param pandoc_command: Pandoc command that failed
        :param exit_code: Exit code from pandoc
        """
        details = {
            "pandoc_command": pandoc_command,
            "exit_code": exit_code,
            "error_type": "pandoc_error"
        }
        super().__init__(message, details)


class MemoryError(MarkdownConverterError):
    """Exception raised when memory limits are exceeded."""
    
    def __init__(self, message: str, memory_usage: Optional[int] = None, memory_limit: Optional[int] = None) -> None:
        """
        Initialize the memory error.
        
        :param message: Error message
        :param memory_usage: Current memory usage in bytes
        :param memory_limit: Memory limit in bytes
        """
        details = {
            "memory_usage": memory_usage,
            "memory_limit": memory_limit,
            "error_type": "memory_error"
        }
        super().__init__(message, details)


class ValidationError(MarkdownConverterError):
    """Exception raised when input validation fails."""
    
    def __init__(self, message: str, field_name: Optional[str] = None, field_value: Optional[Any] = None) -> None:
        """
        Initialize the validation error.
        
        :param message: Error message
        :param field_name: Name of the field that failed validation
        :param field_value: Value that failed validation
        """
        details = {
            "field_name": field_name,
            "field_value": field_value,
            "error_type": "validation_error"
        }
        super().__init__(message, details)


class RetryableError(MarkdownConverterError):
    """Exception that indicates an operation should be retried."""
    
    def __init__(self, message: str, retry_count: int = 0, max_retries: int = 3) -> None:
        """
        Initialize the retryable error.
        
        :param message: Error message
        :param retry_count: Current retry attempt number
        :param max_retries: Maximum number of retry attempts
        """
        details = {
            "retry_count": retry_count,
            "max_retries": max_retries,
            "error_type": "retryable_error"
        }
        super().__init__(message, details)


class ConversionError(MarkdownConverterError):
    """Exception raised when the overall conversion process fails."""
    
    def __init__(self, message: str, input_file: Optional[str] = None, output_file: Optional[str] = None) -> None:
        """
        Initialize the conversion error.
        
        :param message: Error message
        :param input_file: Path to the input file
        :param output_file: Path to the output file
        """
        details = {
            "input_file": input_file,
            "output_file": output_file,
            "error_type": "conversion_error"
        }
        super().__init__(message, details) 