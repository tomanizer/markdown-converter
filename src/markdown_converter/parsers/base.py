"""
Base Parser Interface

This module defines the abstract base class for all document parsers.
All format-specific parsers must implement this interface.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import logging
import os
from dataclasses import dataclass

from ..core.exceptions import ParserError, UnsupportedFormatError


@dataclass
class ParserResult:
    """
    Result of a document parsing operation.
    
    This class encapsulates the parsed content and metadata
    returned by a parser.
    """
    content: str
    metadata: Dict[str, Any]
    format: str
    messages: List[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.messages is None:
            self.messages = []


class BaseParser(ABC):
    """
    Abstract base class for all document parsers.
    
    This class defines the interface that all format-specific parsers
    must implement. It provides common functionality and error handling.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the parser with optional configuration.
        
        :param config: Configuration dictionary for the parser
        """
        self.config = config or {}
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.supported_formats: List[str] = []
        self._validate_config()
    
    @abstractmethod
    def can_parse(self, file_path: Union[str, Path]) -> bool:
        """
        Check if this parser can handle the given file.
        
        :param file_path: Path to the file to check
        :return: True if the parser can handle this file type
        """
        pass
    
    @abstractmethod
    def parse(self, file_path: Union[str, Path]) -> ParserResult:
        """
        Parse the document and extract its content.
        
        :param file_path: Path to the file to parse
        :return: ParserResult containing parsed content and metadata
        :raises: ParserError if parsing fails
        """
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """
        Get list of file formats this parser supports.
        
        :return: List of supported file extensions (e.g., ['.docx', '.doc'])
        """
        pass
    
    def validate_file(self, file_path: Union[str, Path]) -> None:
        """
        Validate that the file exists and is readable.
        
        :param file_path: Path to the file to validate
        :raises: ParserError if file is invalid
        """
        path = Path(file_path)
        
        if not path.exists():
            raise ParserError(f"File does not exist: {path}")
        
        if not path.is_file():
            raise ParserError(f"Path is not a file: {path}")
        
        if not os.access(path, os.R_OK):
            raise ParserError(f"File is not readable: {path}")
    
    def _validate_config(self) -> None:
        """
        Validate the parser configuration.
        
        :raises: ValueError if configuration is invalid
        """
        # Subclasses can override this to add specific validation
        pass
    
    def _log_parsing_start(self, file_path: Union[str, Path]) -> None:
        """Log the start of parsing operation."""
        self.logger.info(f"Starting to parse: {file_path}")
    
    def _log_parsing_success(self, file_path: Union[str, Path]) -> None:
        """Log successful parsing completion."""
        self.logger.info(f"Successfully parsed: {file_path}")
    
    def _log_parsing_error(self, file_path: Union[str, Path], error: Exception) -> None:
        """Log parsing error."""
        self.logger.error(f"Failed to parse {file_path}: {error}")
    
    def _extract_metadata(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Extract basic metadata from the file.
        
        :param file_path: Path to the file
        :return: Dictionary containing basic metadata
        """
        path = Path(file_path)
        stat = path.stat()
        
        return {
            "filename": path.name,
            "file_size": stat.st_size,
            "file_extension": path.suffix.lower(),
            "created_time": stat.st_ctime,
            "modified_time": stat.st_mtime,
        }


class ParserRegistry:
    """
    Registry for managing all available parsers.
    
    This class maintains a registry of all parser instances and
    provides methods to find the appropriate parser for a given file.
    """
    
    def __init__(self) -> None:
        """Initialize the parser registry."""
        self._parsers: List[BaseParser] = []
        self.logger = logging.getLogger("ParserRegistry")
    
    def register_parser(self, parser: BaseParser) -> None:
        """
        Register a parser with the registry.
        
        :param parser: Parser instance to register
        """
        self._parsers.append(parser)
        self.logger.info(f"Registered parser: {parser.__class__.__name__}")
    
    def get_parser_for_file(self, file_path: Union[str, Path]) -> Optional[BaseParser]:
        """
        Find the appropriate parser for a given file.
        
        :param file_path: Path to the file
        :return: Parser instance that can handle the file, or None
        """
        for parser in self._parsers:
            if parser.can_parse(file_path):
                return parser
        
        return None
    
    def get_supported_formats(self) -> List[str]:
        """
        Get all supported file formats from registered parsers.
        
        :return: List of all supported file extensions
        """
        formats = []
        for parser in self._parsers:
            formats.extend(parser.get_supported_formats())
        return list(set(formats))  # Remove duplicates
    
    def list_parsers(self) -> List[str]:
        """
        Get list of registered parser class names.
        
        :return: List of parser class names
        """
        return [parser.__class__.__name__ for parser in self._parsers]
    
    def get_parsers(self) -> List[BaseParser]:
        """
        Get list of registered parser instances.
        
        :return: List of parser instances
        """
        return self._parsers.copy()


# Global parser registry instance
parser_registry = ParserRegistry() 