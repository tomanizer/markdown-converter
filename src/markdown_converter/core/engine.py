"""
Pandoc Integration Engine

This module provides the core pandoc integration for document conversion.
It handles format detection, error handling, and LLM-optimized output.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Tuple
import logging

import pypandoc
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .exceptions import PandocError, ConversionError, UnsupportedFormatError
from .utils import get_file_extension, validate_file_path


class PandocEngine:
    """
    Core pandoc integration engine for document conversion.
    
    This class provides a robust interface to pandoc with error handling,
    format detection, and LLM-optimized output settings.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the pandoc engine.
        
        :param config: Configuration dictionary for the engine
        """
        self.config = config or {}
        self.logger = logging.getLogger("PandocEngine")
        self._validate_pandoc_installation()
        self._setup_default_config()
    
    def _validate_pandoc_installation(self) -> None:
        """Validate that pandoc is properly installed and accessible."""
        try:
            version = pypandoc.get_pandoc_version()
            self.logger.info(f"Pandoc version: {version}")
            
            # Check if version is 3.7+
            major, minor = map(int, version.split('.')[:2])
            if major < 3 or (major == 3 and minor < 7):
                self.logger.warning(f"Pandoc version {version} is older than 3.7")
                
        except Exception as e:
            raise PandocError(f"Pandoc not properly installed: {e}")
    
    def _setup_default_config(self) -> None:
        """Setup default configuration for pandoc conversion."""
        self.default_config = {
            # LLM-optimized markdown settings
            "markdown_settings": {
                "wrap": "none",  # No line wrapping
                "toc": False,     # No table of contents
                "number-sections": False,  # No section numbering
                "standalone": False,  # No standalone document
                # "extract-media": True,  # Extract images - requires path argument
                # "data-dir": None,  # Use default data directory
            },
            # Error handling
            "max_retries": 3,
            "retry_delay": 1.0,
            # Memory management
            "max_file_size": 100 * 1024 * 1024,  # 100MB
            "chunk_size": 10 * 1024 * 1024,  # 10MB chunks
        }
        
        # Merge with user config
        self.default_config.update(self.config)
    
    def detect_format(self, file_path: Union[str, Path]) -> str:
        """
        Detect the input format of a file.
        
        :param file_path: Path to the file
        :return: Detected format string for pandoc
        :raises: UnsupportedFormatError if format cannot be detected
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        # Format mapping
        format_map = {
            '.docx': 'docx',
            '.doc': 'doc',
            '.pdf': 'pdf',
            '.html': 'html',
            '.htm': 'html',
            '.xlsx': 'xlsx',
            '.xls': 'xls',
            '.odt': 'odt',
            '.rtf': 'rtf',
            '.epub': 'epub',
            '.txt': 'markdown',
            '.md': 'markdown',
            '.msg': 'email',
            '.eml': 'email',
        }
        
        if extension in format_map:
            return format_map[extension]
        
        # Try to detect from file content
        try:
            with open(file_path, 'rb') as f:
                header = f.read(8)
                
                # Check for common file signatures
                if header.startswith(b'PK\x03\x04'):
                    return 'docx'  # ZIP-based format
                elif header.startswith(b'%PDF'):
                    return 'pdf'
                elif header.startswith(b'<!DOCTYPE') or header.startswith(b'<html'):
                    return 'html'
                elif header.startswith(b'From:') or header.startswith(b'Return-Path:'):
                    return 'email'
                else:
                    return 'markdown'  # Default to markdown
                    
        except Exception as e:
            self.logger.warning(f"Could not detect format for {file_path}: {e}")
            raise UnsupportedFormatError(f"Cannot detect format for {file_path}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((PandocError, subprocess.CalledProcessError))
    )
    def convert_file(self, input_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None, 
                    input_format: Optional[str] = None, output_format: str = 'markdown',
                    options: Optional[Dict[str, Any]] = None) -> str:
        """
        Convert a file using pandoc with retry logic.
        
        :param input_path: Path to input file
        :param output_path: Path to output file (optional)
        :param input_format: Input format (auto-detected if None)
        :param output_format: Output format (default: markdown)
        :param options: Additional pandoc options
        :return: Converted content as string
        :raises: PandocError if conversion fails
        """
        input_path = Path(input_path)
        validate_file_path(input_path)
        
        # Auto-detect input format if not specified
        if input_format is None:
            input_format = self.detect_format(input_path)
        
        # Setup options
        conversion_options = self.default_config["markdown_settings"].copy()
        if options:
            conversion_options.update(options)
        
        try:
            self.logger.info(f"Converting {input_path} from {input_format} to {output_format}")
            
            if output_path:
                # Convert to file
                result = pypandoc.convert_file(
                    str(input_path),
                    output_format,
                    format=input_format,
                    outputfile=str(output_path),
                    extra_args=self._build_extra_args(conversion_options)
                )
                return result
            else:
                # Convert to string
                result = pypandoc.convert_file(
                    str(input_path),
                    output_format,
                    format=input_format,
                    extra_args=self._build_extra_args(conversion_options)
                )
                return result
                
        except Exception as e:
            self.logger.error(f"Pandoc conversion failed for {input_path}: {e}")
            raise PandocError(f"Failed to convert {input_path}: {e}", 
                            pandoc_command=f"pandoc {input_path} -> {output_format}")
    
    def convert_text(self, text: str, input_format: str = 'markdown', 
                    output_format: str = 'markdown', options: Optional[Dict[str, Any]] = None) -> str:
        """
        Convert text content using pandoc.
        
        :param text: Input text content
        :param input_format: Input format
        :param output_format: Output format
        :param options: Additional pandoc options
        :return: Converted content as string
        """
        conversion_options = self.default_config["markdown_settings"].copy()
        if options:
            conversion_options.update(options)
        
        try:
            result = pypandoc.convert_text(
                text,
                output_format,
                format=input_format,
                extra_args=self._build_extra_args(conversion_options)
            )
            return result
        except Exception as e:
            self.logger.error(f"Pandoc text conversion failed: {e}")
            raise PandocError(f"Failed to convert text: {e}")
    
    def _build_extra_args(self, options: Dict[str, Any]) -> List[str]:
        """
        Build extra arguments for pandoc command.
        
        :param options: Pandoc options dictionary
        :return: List of command line arguments
        """
        args = []
        
        for key, value in options.items():
            if value is True:
                args.append(f"--{key}")
            elif value is False:
                # For boolean false values, use the =false syntax
                args.append(f"--{key}=false")
            elif value is not None:
                args.extend([f"--{key}", str(value)])
        
        return args
    
    def get_supported_formats(self) -> Dict[str, List[str]]:
        """
        Get supported input and output formats.
        
        :return: Dictionary with input and output format lists
        """
        # These are the formats we've tested and support
        input_formats = [
            'docx', 'doc', 'pdf', 'html', 'htm', 'xlsx', 'xls',
            'odt', 'rtf', 'epub', 'markdown', 'md', 'email'
        ]
        
        output_formats = [
            'markdown', 'md', 'html', 'htm', 'pdf', 'docx',
            'txt', 'rst', 'latex', 'tex'
        ]
        
        return {
            'input': input_formats,
            'output': output_formats
        }
    
    def validate_format_support(self, input_format: str, output_format: str) -> bool:
        """
        Validate that the specified formats are supported.
        
        :param input_format: Input format to check
        :param output_format: Output format to check
        :return: True if both formats are supported
        """
        formats = self.get_supported_formats()
        return (input_format in formats['input'] and 
                output_format in formats['output'])
    
    def get_conversion_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get information about a file for conversion.
        
        :param file_path: Path to the file
        :return: Dictionary with conversion information
        """
        file_path = Path(file_path)
        stat = file_path.stat()
        
        return {
            'file_path': str(file_path),
            'file_size': stat.st_size,
            'detected_format': self.detect_format(file_path),
            'supported_formats': self.get_supported_formats(),
            'is_supported': self.validate_format_support(
                self.detect_format(file_path), 'markdown'
            )
        }


class ConversionEngine:
    """
    High-level conversion engine that coordinates pandoc operations.
    
    This class provides a simplified interface for document conversion
    with automatic format detection and error handling.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the conversion engine.
        
        :param config: Configuration dictionary
        """
        self.pandoc_engine = PandocEngine(config)
        self.logger = logging.getLogger("ConversionEngine")
    
    def convert_document(self, input_path: Union[str, Path], 
                        output_path: Optional[Union[str, Path]] = None,
                        output_format: str = 'markdown') -> str:
        """
        Convert a document to the specified format.
        
        :param input_path: Path to input document
        :param output_path: Path to output file (optional)
        :param output_format: Output format (default: markdown)
        :return: Converted content as string
        :raises: ConversionError if conversion fails
        """
        try:
            # Get conversion info
            info = self.pandoc_engine.get_conversion_info(input_path)
            
            if not info['is_supported']:
                raise ConversionError(f"Unsupported format: {info['detected_format']}")
            
            # Perform conversion
            result = self.pandoc_engine.convert_file(
                input_path, output_path, 
                input_format=info['detected_format'],
                output_format=output_format
            )
            
            self.logger.info(f"Successfully converted {input_path} to {output_format}")
            return result
            
        except Exception as e:
            self.logger.error(f"Conversion failed for {input_path}: {e}")
            raise ConversionError(f"Failed to convert {input_path}: {e}",
                               input_file=str(input_path),
                               output_file=str(output_path) if output_path else None)
    
    def batch_convert(self, input_files: List[Union[str, Path]], 
                     output_dir: Optional[Union[str, Path]] = None,
                     output_format: str = 'markdown') -> List[Dict[str, Any]]:
        """
        Convert multiple files in batch.
        
        :param input_files: List of input file paths
        :param output_dir: Output directory (optional)
        :param output_format: Output format
        :return: List of conversion results
        """
        results = []
        
        for input_file in input_files:
            try:
                if output_dir:
                    output_path = Path(output_dir) / f"{Path(input_file).stem}.{output_format}"
                else:
                    output_path = None
                
                content = self.convert_document(input_file, output_path, output_format)
                
                results.append({
                    'input_file': str(input_file),
                    'output_file': str(output_path) if output_path else None,
                    'success': True,
                    'content': content,
                    'error': None
                })
                
            except Exception as e:
                results.append({
                    'input_file': str(input_file),
                    'output_file': None,
                    'success': False,
                    'content': None,
                    'error': str(e)
                })
        
        return results 