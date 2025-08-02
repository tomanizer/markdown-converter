"""
Pandoc Multi-Format Parser

This module provides a unified parser interface for Pandoc, making it
transparent within the parser registry architecture.
"""

import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pypandoc
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from ..core.exceptions import ParserError, UnsupportedFormatError
from .base import BaseParser, ParserResult


class PandocParser(BaseParser):
    """
    Multi-format parser using Pandoc for document conversion.

    This parser provides a unified interface to Pandoc, making it
    transparent within the parser registry architecture.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Pandoc parser.

        :param config: Configuration dictionary
        """
        super().__init__(config)
        self.logger = logging.getLogger("PandocParser")
        self._setup_default_config()
        self._validate_dependencies()

    def _setup_default_config(self) -> None:
        """Setup default configuration for Pandoc parsing."""
        self.default_config = {
            # Pandoc engine configuration
            "pandoc_config": {
                "markdown_settings": {
                    "wrap": "none",
                    "toc": False,
                    "number-sections": False,
                    "standalone": False,
                },
                "max_retries": 3,
                "retry_delay": 1.0,
                "max_file_size": 100 * 1024 * 1024,  # 100MB
            },
            # Parser-specific settings
            "extract_metadata": True,
            "preserve_formatting": True,
            "handle_errors_gracefully": True,
            # Supported formats (Pandoc handles many formats)
            "supported_formats": [
                # Document formats
                ".docx",
                ".html",
                ".htm",
                ".rtf",
                ".odt",
                ".epub",
                # Markup formats
                ".md",
                ".markdown",
                ".rst",
                ".org",
                ".textile",
                ".mediawiki",
                # Data formats
                ".csv",
                ".tsv",
                # Notebook formats
                ".ipynb",
                # LaTeX formats
                ".tex",
                ".latex",
                # Plain text
                ".txt",
            ],
        }

        # Merge with user config
        if self.config:
            self.default_config.update(self.config)

    def _validate_dependencies(self) -> None:
        """Validate that Pandoc is available."""
        try:
            version = pypandoc.get_pandoc_version()
            self.logger.info(f"Pandoc version: {version}")

            # Check if version is 3.7+
            major, minor = map(int, version.split(".")[:2])
            if major < 3 or (major == 3 and minor < 7):
                self.logger.warning(f"Pandoc version {version} is older than 3.7")

            self.pandoc_available = True
            self.logger.info("Pandoc engine initialized successfully")
        except Exception as e:
            self.pandoc_available = False
            self.logger.warning(f"Pandoc not available: {e}")
            raise ParserError("Pandoc is required for PandocParser")

    def detect_format(self, file_path: Union[str, Path]) -> str:
        """
        Detect the input format of a file.

        :param file_path: Path to the file
        :return: Detected format string for pandoc
        :raises: UnsupportedFormatError if format cannot be detected
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()

        # Format mapping (only formats Pandoc actually supports)
        format_map = {
            ".docx": "docx",
            ".html": "html",
            ".htm": "html",
            ".odt": "odt",
            ".rtf": "rtf",
            ".epub": "epub",
            ".txt": "markdown",
            ".md": "markdown",
            ".markdown": "markdown",
            ".rst": "rst",
            ".org": "org",
            ".textile": "textile",
            ".mediawiki": "mediawiki",
            ".csv": "csv",
            ".tsv": "tsv",
            ".ipynb": "ipynb",
            ".tex": "latex",
            ".latex": "latex",
        }

        if extension in format_map:
            return format_map[extension]

        # Try to detect from file content
        try:
            with open(file_path, "rb") as f:
                header = f.read(8)

                # Check for common file signatures
                if header.startswith(b"PK\x03\x04"):
                    return "docx"  # ZIP-based format
                elif header.startswith(b"%PDF"):
                    return "pdf"
                elif header.startswith(b"<!DOCTYPE") or header.startswith(b"<html"):
                    return "html"
                elif header.startswith(b"From:") or header.startswith(b"Return-Path:"):
                    return "email"
                else:
                    return "markdown"  # Default to markdown

        except Exception as e:
            self.logger.warning(f"Could not detect format for {file_path}: {e}")
            raise UnsupportedFormatError(f"Cannot detect format for {file_path}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((ParserError, subprocess.CalledProcessError)),
    )
    def convert_file(
        self,
        input_path: Union[str, Path],
        input_format: Optional[str] = None,
        output_format: str = "markdown",
        options: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Convert a file using pandoc with retry logic.

        :param input_path: Path to input file
        :param input_format: Input format (auto-detected if None)
        :param output_format: Output format (default: markdown)
        :param options: Additional pandoc options
        :return: Converted content as string
        :raises: ParserError if conversion fails
        """
        input_path = Path(input_path)

        # Auto-detect input format if not specified
        if input_format is None:
            input_format = self.detect_format(input_path)

        # Setup options
        conversion_options = self.default_config["pandoc_config"][
            "markdown_settings"
        ].copy()
        if options:
            conversion_options.update(options)

        try:
            self.logger.info(
                f"Converting {input_path} from {input_format} to {output_format}"
            )
            self.logger.debug(f"Conversion options: {conversion_options}")

            result = pypandoc.convert_file(
                str(input_path),
                output_format,
                format=input_format,
                extra_args=self._build_extra_args(conversion_options),
            )
            self.logger.debug(f"String conversion result: {repr(result)}")
            return result

        except Exception as e:
            self.logger.error(f"Pandoc conversion failed for {input_path}: {e}")
            raise ParserError(f"Failed to convert {input_path}: {e}")

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

    def get_conversion_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get information about a file for conversion.

        :param file_path: Path to the file
        :return: Dictionary with conversion information
        """
        file_path = Path(file_path)
        stat = file_path.stat()
        detected_format = self.detect_format(file_path)

        return {
            "file_path": str(file_path),
            "file_size": stat.st_size,
            "detected_format": detected_format,
            "supported_formats": self.get_supported_formats(),
            "is_supported": self.validate_format_support(detected_format, "markdown"),
        }

    def validate_format_support(self, input_format: str, output_format: str) -> bool:
        """
        Validate that the specified formats are supported.

        :param input_format: Input format to check
        :param output_format: Output format to check
        :return: True if both formats are supported
        """
        formats = self.get_supported_formats()
        return input_format in formats and output_format in ["markdown", "md"]

    def can_parse(self, file_path: Union[str, Path]) -> bool:
        """
        Check if this parser can handle the given file.

        :param file_path: Path to the file
        :return: True if the file can be parsed
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()

        # Check if format is in our supported list
        if extension in self.default_config["supported_formats"]:
            return True

        # Also check if Pandoc can handle it
        try:
            info = self.get_conversion_info(file_path)
            return info["is_supported"]
        except Exception:
            return False

    def parse(self, file_path: Union[str, Path]) -> ParserResult:
        """
        Parse a document using Pandoc and extract its content.

        :param file_path: Path to the document
        :return: ParserResult with extracted content and metadata
        :raises: ParserError if parsing fails
        """
        file_path = Path(file_path)

        if not self.can_parse(file_path):
            raise UnsupportedFormatError(f"Cannot parse {file_path.suffix} files")

        self.logger.info(f"Parsing document with Pandoc: {file_path}")

        try:
            # Get conversion info
            conversion_info = self.get_conversion_info(file_path)

            # Convert to markdown
            content = self.convert_file(
                file_path,
                input_format=conversion_info["detected_format"],
                output_format="markdown",
            )

            # Extract metadata
            metadata = self._extract_metadata(file_path, conversion_info)

            self.logger.info(f"Successfully parsed {file_path} with Pandoc")

            return ParserResult(
                content=content, metadata=metadata, format="markdown", messages=[]
            )

        except Exception as e:
            self.logger.error(f"Pandoc parsing failed for {file_path}: {e}")
            raise ParserError(f"Failed to parse document {file_path}: {e}")

    def _extract_metadata(
        self, file_path: Path, conversion_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract metadata from the file and conversion info.

        :param file_path: Path to the file
        :param conversion_info: Information from Pandoc engine
        :return: Dictionary of metadata
        """
        metadata = {
            "parser": "pandoc",
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size,
            "format": conversion_info["detected_format"],
            "pandoc_supported": conversion_info["is_supported"],
            "supported_formats": conversion_info["supported_formats"],
        }

        # Add basic file metadata
        basic_metadata = self._extract_basic_metadata(file_path)
        metadata.update(basic_metadata)

        return metadata

    def _extract_basic_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract basic file metadata.

        :param file_path: Path to the file
        :return: Dictionary of basic metadata
        """
        stat = file_path.stat()
        return {
            "file_name": file_path.name,
            "file_extension": file_path.suffix.lower(),
            "file_size_bytes": stat.st_size,
            "file_size_mb": stat.st_size / (1024 * 1024),
            "modified_time": stat.st_mtime,
        }

    def get_supported_formats(self) -> List[str]:
        """
        Get list of supported file formats.

        :return: List of supported format extensions
        """
        return self.default_config["supported_formats"]

    def get_parser_info(self) -> Dict[str, Any]:
        """
        Get information about this parser.

        :return: Dictionary with parser information
        """
        return {
            "name": "PandocParser",
            "description": "Multi-format parser using Pandoc for document conversion",
            "supported_formats": self.get_supported_formats(),
            "dependencies": {"pandoc": self.pandoc_available, "pypandoc": True},
            "config": self.default_config,
        }
