"""
Core module for the markdown converter.

This module contains the core functionality including exceptions,
filesystem operations, and utility functions.
"""

from .exceptions import (
    MarkdownConverterError,
    ParserError,
    UnsupportedFormatError,
    ProcessorError,
    FormatterError,
    ConfigurationError,
    FilesystemError,
    PandocError,
    MemoryError,
    ValidationError,
    RetryableError,
    ConversionError,
    BatchProcessingError,
    GridProcessingError,
    DependencyError,
)

from .engine import PandocEngine, ConversionEngine
from .filesystem import FilesystemManager
from .file_converter import FileConverter
from .batch_processor import BatchProcessor, ProcessingStats, ProcessingResult
from .grid_processor import GridProcessor, ClusterInfo, JobInfo
from .utils import (
    get_file_extension,
    validate_file_path,
    get_file_info,
    ensure_directory_exists,
    get_safe_output_path,
    is_binary_file,
    get_file_size_mb,
    is_large_file,
    sanitize_filename,
    create_temp_file,
    cleanup_temp_file,
    format_file_size,
    validate_config,
    merge_configs,
)

__all__ = [
    # Exceptions
    "MarkdownConverterError",
    "ParserError",
    "UnsupportedFormatError",
    "ProcessorError",
    "FormatterError",
    "ConfigurationError",
    "FilesystemError",
    "PandocError",
    "MemoryError",
    "ValidationError",
    "RetryableError",
    "ConversionError",
    "BatchProcessingError",
    "GridProcessingError",
    "DependencyError",
    # Engine components
    "PandocEngine",
    "ConversionEngine",
    # Filesystem components
    "FilesystemManager",
    # File conversion components
    "FileConverter",
    # Batch processing components
    "BatchProcessor",
    "ProcessingStats",
    "ProcessingResult",
    # Grid processing components
    "GridProcessor",
    "ClusterInfo",
    "JobInfo",
    # Utility functions
    "get_file_extension",
    "validate_file_path",
    "get_file_info",
    "ensure_directory_exists",
    "get_safe_output_path",
    "is_binary_file",
    "get_file_size_mb",
    "is_large_file",
    "sanitize_filename",
    "create_temp_file",
    "cleanup_temp_file",
    "format_file_size",
    "validate_config",
    "merge_configs",
]
