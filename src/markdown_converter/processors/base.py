"""
Base Processor Interface

This module defines the abstract base class for all content processors.
Processors handle specific content types like tables, images, and metadata.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
import logging

from ..core.exceptions import ProcessorError


@dataclass
class ProcessingResult:
    """
    Result of a content processing operation.
    
    This class encapsulates the processed content and metadata
    returned by a processor.
    """
    content: str
    metadata: Dict[str, Any]
    messages: List[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.messages is None:
            self.messages = []


class BaseProcessor(ABC):
    """
    Abstract base class for all content processors.
    
    Processors handle specific content types and enhance the conversion
    process. Examples include table processors, image processors, etc.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the processor with optional configuration.
        
        :param config: Configuration dictionary for the processor
        """
        self.config = config or {}
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self._validate_config()
    
    def can_process(self, content: str) -> bool:
        """
        Check if this processor can handle the given content.
        
        :param content: The content to check
        :return: True if the processor can handle this content
        """
        # Default implementation - subclasses can override
        return True
    
    @abstractmethod
    def process(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        """
        Process the content and return enhanced/transformed content.
        
        :param content: The content to process
        :param metadata: Optional metadata
        :return: ProcessingResult with processed content and metadata
        :raises: ProcessorError if processing fails
        """
        pass
    
    def get_supported_content_types(self) -> List[str]:
        """
        Get list of content types this processor supports.
        
        :return: List of supported content types (e.g., ['table', 'image'])
        """
        # Default implementation - subclasses can override
        return []
    
    def _validate_config(self) -> None:
        """
        Validate the processor configuration.
        
        :raises: ValueError if configuration is invalid
        """
        # Subclasses can override this to add specific validation
        pass
    
    def _log_processing_start(self, content_type: str) -> None:
        """Log the start of processing operation."""
        self.logger.info(f"Starting to process {content_type}")
    
    def _log_processing_success(self, content_type: str) -> None:
        """Log successful processing completion."""
        self.logger.info(f"Successfully processed {content_type}")
    
    def _log_processing_error(self, content_type: str, error: Exception) -> None:
        """Log processing error."""
        self.logger.error(f"Failed to process {content_type}: {error}")
    
    def _get_output_path(self, base_path: Path, suffix: str) -> Path:
        """
        Generate output path for processed content.
        
        :param base_path: Base path for the original file
        :param suffix: Suffix to add to the filename
        :return: Generated output path
        """
        stem = base_path.stem
        return base_path.parent / f"{stem}_{suffix}"


class ProcessorRegistry:
    """
    Registry for managing all available processors.
    
    This class maintains a registry of all processor instances and
    provides methods to find the appropriate processor for given content.
    """
    
    def __init__(self) -> None:
        """Initialize the processor registry."""
        self._processors: List[BaseProcessor] = []
        self.logger = logging.getLogger("ProcessorRegistry")
    
    def register_processor(self, processor: BaseProcessor) -> None:
        """
        Register a processor with the registry.
        
        :param processor: Processor instance to register
        """
        self._processors.append(processor)
        self.logger.info(f"Registered processor: {processor.__class__.__name__}")
    
    def get_processors_for_content(self, content: str) -> List[BaseProcessor]:
        """
        Find processors that can handle the given content.
        
        :param content: The content to process
        :return: List of processor instances that can handle the content
        """
        processors = []
        for processor in self._processors:
            if processor.can_process(content):
                processors.append(processor)
        return processors
    
    def get_supported_content_types(self) -> List[str]:
        """
        Get all supported content types from registered processors.
        
        :return: List of all supported content types
        """
        content_types = []
        for processor in self._processors:
            content_types.extend(processor.get_supported_content_types())
        return list(set(content_types))  # Remove duplicates
    
    def list_processors(self) -> List[str]:
        """
        Get list of registered processor class names.
        
        :return: List of processor class names
        """
        return [processor.__class__.__name__ for processor in self._processors]


class ProcessingPipeline:
    """
    Pipeline for processing content through multiple processors.
    
    This class manages the processing of content through a series
    of processors in a defined order.
    """
    
    def __init__(self, processors: Optional[List[BaseProcessor]] = None) -> None:
        """
        Initialize the processing pipeline.
        
        :param processors: List of processors to use in the pipeline
        """
        self.processors = processors or []
        self.logger = logging.getLogger("ProcessingPipeline")
    
    def add_processor(self, processor: BaseProcessor) -> None:
        """
        Add a processor to the pipeline.
        
        :param processor: Processor to add
        """
        self.processors.append(processor)
        self.logger.info(f"Added processor to pipeline: {processor.__class__.__name__}")
    
    def process_content(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        """
        Process content through the pipeline.
        
        :param content: The content to process
        :param metadata: Optional metadata
        :return: ProcessingResult with processed content and metadata
        """
        processed_content = content
        processed_metadata = metadata or {}
        all_messages = []
        
        for processor in self.processors:
            if processor.can_process(processed_content):
                try:
                    result = processor.process(processed_content, processed_metadata)
                    processed_content = result.content
                    processed_metadata.update(result.metadata)
                    all_messages.extend(result.messages)
                    self.logger.debug(f"Processed with {processor.__class__.__name__}")
                except Exception as e:
                    self.logger.warning(f"Processor {processor.__class__.__name__} failed: {e}")
                    # Continue with other processors
                    continue
        
        return ProcessingResult(
            content=processed_content,
            metadata=processed_metadata,
            messages=all_messages
        )


# Global processor registry instance
processor_registry = ProcessorRegistry() 