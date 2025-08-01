"""
Utility functions for the markdown converter.

This module provides common utility functions for file handling,
validation, and other operations used throughout the converter.
"""

import os
import mimetypes
from pathlib import Path
from typing import Union, Optional, Dict, Any
import logging

from .exceptions import FilesystemError, ValidationError


def get_file_extension(file_path: Union[str, Path]) -> str:
    """
    Get the file extension from a file path.
    
    :param file_path: Path to the file
    :return: File extension (lowercase, with dot)
    """
    return Path(file_path).suffix.lower()


def validate_file_path(file_path: Union[str, Path]) -> None:
    """
    Validate that a file path exists and is accessible.
    
    :param file_path: Path to validate
    :raises: FilesystemError if file is invalid
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FilesystemError(f"File does not exist: {path}")
    
    if not path.is_file():
        raise FilesystemError(f"Path is not a file: {path}")
    
    if not os.access(path, os.R_OK):
        raise FilesystemError(f"File is not readable: {path}")


def get_file_info(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Get comprehensive information about a file.
    
    :param file_path: Path to the file
    :return: Dictionary with file information
    """
    path = Path(file_path)
    stat = path.stat()
    
    # Get MIME type
    mime_type, _ = mimetypes.guess_type(str(path))
    
    return {
        'path': str(path),
        'name': path.name,
        'stem': path.stem,
        'suffix': path.suffix.lower(),
        'size': stat.st_size,
        'mime_type': mime_type,
        'created_time': stat.st_ctime,
        'modified_time': stat.st_mtime,
        'is_readable': os.access(path, os.R_OK),
        'is_writable': os.access(path, os.W_OK),
    }


def ensure_directory_exists(directory_path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    :param directory_path: Path to the directory
    :return: Path object for the directory
    :raises: FilesystemError if directory cannot be created
    """
    path = Path(directory_path)
    
    try:
        path.mkdir(parents=True, exist_ok=True)
        return path
    except Exception as e:
        raise FilesystemError(f"Cannot create directory {path}: {e}")


def get_safe_output_path(input_path: Union[str, Path], output_dir: Union[str, Path], 
                        output_format: str = 'md') -> Path:
    """
    Generate a safe output path for converted files.
    
    :param input_path: Path to input file
    :param output_dir: Output directory
    :param output_format: Output format extension
    :return: Safe output path
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    
    # Ensure output directory exists
    ensure_directory_exists(output_dir)
    
    # Generate output filename
    stem = input_path.stem
    output_filename = f"{stem}.{output_format}"
    output_path = output_dir / output_filename
    
    # Handle filename conflicts
    counter = 1
    original_path = output_path
    while output_path.exists():
        output_filename = f"{stem}_{counter}.{output_format}"
        output_path = output_dir / output_filename
        counter += 1
        
        # Prevent infinite loop
        if counter > 1000:
            raise FilesystemError(f"Cannot create unique filename for {original_path}")
    
    return output_path


def is_binary_file(file_path: Union[str, Path]) -> bool:
    """
    Check if a file is binary.
    
    :param file_path: Path to the file
    :return: True if file is binary
    """
    path = Path(file_path)
    
    try:
        with open(path, 'rb') as f:
            # Read first 1024 bytes
            chunk = f.read(1024)
            return b'\x00' in chunk
    except Exception:
        return False


def get_file_size_mb(file_path: Union[str, Path]) -> float:
    """
    Get file size in megabytes.
    
    :param file_path: Path to the file
    :return: File size in MB
    """
    path = Path(file_path)
    return path.stat().st_size / (1024 * 1024)


def is_large_file(file_path: Union[str, Path], threshold_mb: float = 100.0) -> bool:
    """
    Check if a file is considered large.
    
    :param file_path: Path to the file
    :param threshold_mb: Size threshold in MB
    :return: True if file is larger than threshold
    """
    return get_file_size_mb(file_path) > threshold_mb


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename for safe filesystem operations.
    
    :param filename: Original filename
    :return: Sanitized filename
    """
    import re
    
    # Remove or replace problematic characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    
    # Ensure filename is not empty
    if not sanitized:
        sanitized = 'unnamed_file'
    
    # Limit length
    if len(sanitized) > 255:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:255-len(ext)] + ext
    
    return sanitized


def create_temp_file(suffix: str = '.tmp', prefix: str = 'markdown_converter_') -> Path:
    """
    Create a temporary file for processing.
    
    :param suffix: File suffix
    :param prefix: File prefix
    :return: Path to temporary file
    """
    import tempfile
    
    temp_file = tempfile.NamedTemporaryFile(
        suffix=suffix,
        prefix=prefix,
        delete=False
    )
    temp_file.close()
    
    return Path(temp_file.name)


def cleanup_temp_file(file_path: Union[str, Path]) -> None:
    """
    Clean up a temporary file.
    
    :param file_path: Path to temporary file
    """
    path = Path(file_path)
    
    try:
        if path.exists():
            path.unlink()
    except Exception as e:
        logging.warning(f"Could not cleanup temp file {path}: {e}")


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    :param size_bytes: Size in bytes
    :return: Formatted size string
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def validate_config(config: Dict[str, Any], required_keys: Optional[list] = None) -> None:
    """
    Validate a configuration dictionary.
    
    :param config: Configuration dictionary
    :param required_keys: List of required keys
    :raises: ValidationError if configuration is invalid
    """
    if not isinstance(config, dict):
        raise ValidationError("Configuration must be a dictionary")
    
    if required_keys:
        for key in required_keys:
            if key not in config:
                raise ValidationError(f"Missing required configuration key: {key}")


def merge_configs(default_config: Dict[str, Any], user_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge user configuration with default configuration.
    
    :param default_config: Default configuration
    :param user_config: User configuration
    :return: Merged configuration
    """
    result = default_config.copy()
    
    for key, value in user_config.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    
    return result 