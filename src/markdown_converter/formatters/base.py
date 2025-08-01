"""
Base Formatter Interface

This module defines the abstract base class for all output formatters.
Formatters handle the final formatting and optimization of markdown output.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import logging

from ..core.exceptions import FormatterError


class BaseFormatter(ABC):
    """
    Abstract base class for all output formatters.
    
    Formatters handle the final formatting and optimization of content
    for specific output targets (e.g., LLM-optimized markdown).
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the formatter with optional configuration.
        
        :param config: Configuration dictionary for the formatter
        """
        self.config = config or {}
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self._validate_config()
    
    @abstractmethod
    def can_format(self, output_type: str, content: Any) -> bool:
        """
        Check if this formatter can handle the given output type.
        
        :param output_type: Type of output (e.g., 'markdown', 'llm_optimized')
        :param content: The content to format
        :return: True if the formatter can handle this output type
        """
        pass
    
    @abstractmethod
    def format(self, output_type: str, content: Any, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Format the content for the specified output type.
        
        :param output_type: Type of output format
        :param content: The content to format
        :param context: Additional context information
        :return: Formatted content as string
        :raises: FormatterError if formatting fails
        """
        pass
    
    @abstractmethod
    def get_supported_output_types(self) -> List[str]:
        """
        Get list of output types this formatter supports.
        
        :return: List of supported output types (e.g., ['markdown', 'llm_optimized'])
        """
        pass
    
    def _validate_config(self) -> None:
        """
        Validate the formatter configuration.
        
        :raises: ValueError if configuration is invalid
        """
        # Subclasses can override this to add specific validation
        pass
    
    def _log_formatting_start(self, output_type: str) -> None:
        """Log the start of formatting operation."""
        self.logger.info(f"Starting to format for {output_type}")
    
    def _log_formatting_success(self, output_type: str) -> None:
        """Log successful formatting completion."""
        self.logger.info(f"Successfully formatted for {output_type}")
    
    def _log_formatting_error(self, output_type: str, error: Exception) -> None:
        """Log formatting error."""
        self.logger.error(f"Failed to format for {output_type}: {error}")
    
    def _optimize_for_llm(self, markdown_content: str) -> str:
        """
        Optimize markdown content for LLM processing.
        
        :param markdown_content: Raw markdown content
        :return: LLM-optimized markdown content
        """
        # Remove excessive whitespace
        lines = markdown_content.split('\n')
        optimized_lines = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            optimized_lines.append(line)
        
        # Remove excessive blank lines
        result_lines = []
        prev_blank = False
        
        for line in optimized_lines:
            if line.strip() == '':
                if not prev_blank:
                    result_lines.append(line)
                prev_blank = True
            else:
                result_lines.append(line)
                prev_blank = False
        
        return '\n'.join(result_lines)
    
    def _ensure_proper_heading_structure(self, markdown_content: str) -> str:
        """
        Ensure proper heading structure in markdown.
        
        :param markdown_content: Markdown content
        :return: Markdown with proper heading structure
        """
        lines = markdown_content.split('\n')
        result_lines = []
        heading_levels = []
        
        for line in lines:
            if line.startswith('#'):
                # Count heading level
                level = len(line) - len(line.lstrip('#'))
                
                # Ensure proper nesting
                while heading_levels and heading_levels[-1] >= level:
                    heading_levels.pop()
                
                heading_levels.append(level)
                result_lines.append(line)
            else:
                result_lines.append(line)
        
        return '\n'.join(result_lines)


class FormatterRegistry:
    """
    Registry for managing all available formatters.
    
    This class maintains a registry of all formatter instances and
    provides methods to find the appropriate formatter for given output types.
    """
    
    def __init__(self) -> None:
        """Initialize the formatter registry."""
        self._formatters: List[BaseFormatter] = []
        self.logger = logging.getLogger("FormatterRegistry")
    
    def register_formatter(self, formatter: BaseFormatter) -> None:
        """
        Register a formatter with the registry.
        
        :param formatter: Formatter instance to register
        """
        self._formatters.append(formatter)
        self.logger.info(f"Registered formatter: {formatter.__class__.__name__}")
    
    def get_formatter_for_output(self, output_type: str, content: Any) -> Optional[BaseFormatter]:
        """
        Find the appropriate formatter for given output type and content.
        
        :param output_type: Type of output format
        :param content: The content to format
        :return: Formatter instance that can handle the output, or None
        """
        for formatter in self._formatters:
            if formatter.can_format(output_type, content):
                return formatter
        
        return None
    
    def get_supported_output_types(self) -> List[str]:
        """
        Get all supported output types from registered formatters.
        
        :return: List of all supported output types
        """
        output_types = []
        for formatter in self._formatters:
            output_types.extend(formatter.get_supported_output_types())
        return list(set(output_types))  # Remove duplicates
    
    def list_formatters(self) -> List[str]:
        """
        Get list of registered formatter class names.
        
        :return: List of formatter class names
        """
        return [formatter.__class__.__name__ for formatter in self._formatters]


class FormattingPipeline:
    """
    Pipeline for formatting content through multiple formatters.
    
    This class manages the formatting of content through a series
    of formatters in a defined order.
    """
    
    def __init__(self, formatters: Optional[List[BaseFormatter]] = None) -> None:
        """
        Initialize the formatting pipeline.
        
        :param formatters: List of formatters to use in the pipeline
        """
        self.formatters = formatters or []
        self.logger = logging.getLogger("FormattingPipeline")
    
    def add_formatter(self, formatter: BaseFormatter) -> None:
        """
        Add a formatter to the pipeline.
        
        :param formatter: Formatter to add
        """
        self.formatters.append(formatter)
        self.logger.info(f"Added formatter to pipeline: {formatter.__class__.__name__}")
    
    def format_content(self, output_type: str, content: Any, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Format content through the pipeline.
        
        :param output_type: Type of output format
        :param content: The content to format
        :param context: Additional context information
        :return: Formatted content as string
        """
        formatted_content = content
        
        for formatter in self.formatters:
            if formatter.can_format(output_type, formatted_content):
                try:
                    formatted_content = formatter.format(output_type, formatted_content, context)
                    self.logger.debug(f"Formatted with {formatter.__class__.__name__}")
                except Exception as e:
                    self.logger.warning(f"Formatter {formatter.__class__.__name__} failed: {e}")
                    # Continue with other formatters
                    continue
        
        return formatted_content


# Global formatter registry instance
formatter_registry = FormatterRegistry() 