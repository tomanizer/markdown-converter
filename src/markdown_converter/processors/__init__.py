"""
Processors module for the markdown converter.

This module contains content processors for enhancing and optimizing
extracted content for LLM readability.
"""

from .base import BaseProcessor, ProcessingResult, ProcessorRegistry, ProcessingPipeline, processor_registry
from .table_processor import TableProcessor, TableInfo
from .image_processor import ImageProcessor, ImageInfo
from .metadata_processor import MetadataProcessor, MetadataInfo

__all__ = [
    "BaseProcessor",
    "ProcessingResult",
    "ProcessorRegistry",
    "ProcessingPipeline",
    "processor_registry",
    "TableProcessor",
    "TableInfo",
    "ImageProcessor",
    "ImageInfo",
    "MetadataProcessor",
    "MetadataInfo",
]
