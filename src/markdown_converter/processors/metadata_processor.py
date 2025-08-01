"""
Metadata Processor

This module provides specialized processing for metadata extraction,
format detection, and YAML front matter generation.
"""

import logging
import re
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
import yaml
from datetime import datetime

from .base import BaseProcessor, ProcessingResult
from ..core.exceptions import ProcessorError


@dataclass
class MetadataInfo:
    """Information about extracted metadata."""
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    keywords: Optional[List[str]] = None
    created_date: Optional[str] = None
    modified_date: Optional[str] = None
    creator: Optional[str] = None
    producer: Optional[str] = None
    language: Optional[str] = None
    page_count: Optional[int] = None
    word_count: Optional[int] = None
    file_size: Optional[int] = None
    format: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None


class MetadataProcessor(BaseProcessor):
    """
    Specialized processor for metadata extraction and management.
    
    Extracts document metadata and adds it as YAML front matter
    to markdown output for better LLM processing.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the metadata processor.
        
        :param config: Configuration dictionary
        """
        super().__init__(config)
        self.logger = logging.getLogger("MetadataProcessor")
        self._setup_default_config()
    
    def _setup_default_config(self) -> None:
        """Setup default configuration for metadata processing."""
        self.default_config = {
            # Metadata extraction settings
            "extract_metadata": True,
            "extract_title": True,
            "extract_author": True,
            "extract_dates": True,
            "extract_keywords": True,
            "extract_statistics": True,
            
            # YAML front matter settings
            "add_front_matter": True,
            "front_matter_format": "yaml",  # 'yaml', 'json'
            "include_file_info": True,
            "include_processing_info": True,
            
            # Content analysis settings
            "analyze_content": True,
            "extract_headings": True,
            "count_words": True,
            "detect_language": False,
            
            # Custom fields
            "custom_fields": {},
            "preserve_original_metadata": True,
            
            # Output settings
            "yaml_style": "block",  # 'block', 'flow'
            "escape_special_chars": True,
            "max_field_length": 1000,
        }
        
        # Merge with user config
        if self.config:
            self.default_config.update(self.config)
    
    def process(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        """
        Process content to extract and add metadata.
        
        :param content: Input content
        :param metadata: Optional metadata
        :return: ProcessingResult with processed content
        """
        self.logger.info("Processing metadata")
        
        try:
            # Extract metadata from content and existing metadata
            metadata_info = self._extract_metadata(content, metadata)
            
            if not metadata_info:
                self.logger.debug("No metadata extracted")
                return ProcessingResult(
                    content=content,
                    metadata=metadata or {},
                    messages=["No metadata extracted"]
                )
            
            # Generate YAML front matter
            front_matter = self._generate_front_matter(metadata_info)
            
            # Add front matter to content
            processed_content = self._add_front_matter_to_content(content, front_matter)
            
            # Update metadata
            if metadata is None:
                metadata = {}
            metadata["extracted_metadata"] = self._metadata_to_dict(metadata_info)
            metadata["front_matter_added"] = True
            
            messages = ["Metadata extracted and front matter added"]
            
            return ProcessingResult(
                content=processed_content,
                metadata=metadata,
                messages=messages
            )
            
        except Exception as e:
            self.logger.error(f"Metadata processing failed: {e}")
            raise ProcessorError(f"Failed to process metadata: {e}")
    
    def _extract_metadata(self, content: str, existing_metadata: Optional[Dict[str, Any]]) -> Optional[MetadataInfo]:
        """
        Extract metadata from content and existing metadata.
        
        :param content: Input content
        :param existing_metadata: Existing metadata dictionary
        :return: MetadataInfo object
        """
        metadata_info = MetadataInfo()
        
        # Extract from existing metadata
        if existing_metadata:
            metadata_info = self._extract_from_existing_metadata(existing_metadata, metadata_info)
        
        # Extract from content
        if self.default_config["analyze_content"]:
            metadata_info = self._extract_from_content(content, metadata_info)
        
        # Add custom fields
        if self.default_config["custom_fields"]:
            metadata_info.custom_fields = self.default_config["custom_fields"].copy()
        
        # Add processing information
        if self.default_config["include_processing_info"]:
            metadata_info = self._add_processing_info(metadata_info)
        
        return metadata_info
    
    def _extract_from_existing_metadata(self, existing_metadata: Dict[str, Any], metadata_info: MetadataInfo) -> MetadataInfo:
        """
        Extract metadata from existing metadata dictionary.
        
        :param existing_metadata: Existing metadata
        :param metadata_info: MetadataInfo object to update
        :return: Updated MetadataInfo object
        """
        # Map common metadata fields
        field_mapping = {
            "title": "title",
            "author": "author",
            "subject": "subject",
            "keywords": "keywords",
            "created": "created_date",
            "modified": "modified_date",
            "creator": "creator",
            "producer": "producer",
            "language": "language",
            "page_count": "page_count",
            "word_count": "word_count",
            "file_size": "file_size",
            "format": "format",
        }
        
        for source_field, target_field in field_mapping.items():
            if source_field in existing_metadata and getattr(metadata_info, target_field) is None:
                value = existing_metadata[source_field]
                if self._is_valid_metadata_value(value):
                    setattr(metadata_info, target_field, value)
        
        # Handle custom fields
        if self.default_config["preserve_original_metadata"]:
            custom_fields = {}
            for key, value in existing_metadata.items():
                if key not in field_mapping and self._is_valid_metadata_value(value):
                    custom_fields[key] = value
            
            if custom_fields:
                metadata_info.custom_fields = custom_fields
        
        return metadata_info
    
    def _extract_from_content(self, content: str, metadata_info: MetadataInfo) -> MetadataInfo:
        """
        Extract metadata from content analysis.
        
        :param content: Input content
        :param metadata_info: MetadataInfo object to update
        :return: Updated MetadataInfo object
        """
        lines = content.split('\n')
        
        # Extract title from first heading
        if self.default_config["extract_title"] and metadata_info.title is None:
            title = self._extract_title_from_content(lines)
            if title:
                metadata_info.title = title
        
        # Extract headings
        if self.default_config["extract_headings"]:
            headings = self._extract_headings_from_content(lines)
            if headings:
                if metadata_info.custom_fields is None:
                    metadata_info.custom_fields = {}
                metadata_info.custom_fields["headings"] = headings
        
        # Count words
        if self.default_config["count_words"] and metadata_info.word_count is None:
            word_count = self._count_words(content)
            metadata_info.word_count = word_count
        
        # Detect language (basic implementation)
        if self.default_config["detect_language"] and metadata_info.language is None:
            language = self._detect_language(content)
            if language:
                metadata_info.language = language
        
        return metadata_info
    
    def _extract_title_from_content(self, lines: List[str]) -> Optional[str]:
        """
        Extract title from content.
        
        :param lines: Content lines
        :return: Extracted title or None
        """
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for first heading
            if line.startswith('# '):
                title = line[2:].strip()
                return self._clean_metadata_value(title)
            elif line.startswith('## '):
                title = line[3:].strip()
                return self._clean_metadata_value(title)
        
        # Look for first non-empty line as potential title
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Simple heuristic: if line is short and doesn't end with punctuation
                if len(line) < 100 and not line.endswith(('.', '!', '?')):
                    return self._clean_metadata_value(line)
        
        return None
    
    def _extract_headings_from_content(self, lines: List[str]) -> List[str]:
        """
        Extract headings from content.
        
        :param lines: Content lines
        :return: List of headings
        """
        headings = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                # Extract heading text
                heading_text = re.sub(r'^#+\s*', '', line).strip()
                if heading_text:
                    headings.append(heading_text)
        
        return headings[:10]  # Limit to first 10 headings
    
    def _count_words(self, content: str) -> int:
        """
        Count words in content.
        
        :param content: Input content
        :return: Word count
        """
        # Remove markdown formatting
        clean_content = re.sub(r'[#*_`~\[\]()]', '', content)
        
        # Split into words and count
        words = re.findall(r'\b\w+\b', clean_content)
        return len(words)
    
    def _detect_language(self, content: str) -> Optional[str]:
        """
        Detect language from content (basic implementation).
        
        :param content: Input content
        :return: Language code or None
        """
        # This is a basic implementation
        # In a real implementation, you might use language detection libraries
        
        # Simple heuristic based on common words
        content_lower = content.lower()
        
        # English indicators
        english_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
        english_count = sum(1 for word in english_words if word in content_lower)
        
        if english_count > 3:
            return 'en'
        
        return None
    
    def _add_processing_info(self, metadata_info: MetadataInfo) -> MetadataInfo:
        """
        Add processing information to metadata.
        
        :param metadata_info: MetadataInfo object to update
        :return: Updated MetadataInfo object
        """
        if metadata_info.custom_fields is None:
            metadata_info.custom_fields = {}
        
        # Add processing timestamp
        metadata_info.custom_fields["processed_at"] = datetime.now().isoformat()
        
        # Add processor information
        metadata_info.custom_fields["processor"] = "markdown_converter"
        metadata_info.custom_fields["processor_version"] = "1.0.0"
        
        return metadata_info
    
    def _generate_front_matter(self, metadata_info: MetadataInfo) -> str:
        """
        Generate YAML front matter from metadata.
        
        :param metadata_info: Metadata information
        :return: YAML front matter string
        """
        # Convert metadata to dictionary
        metadata_dict = self._metadata_to_dict(metadata_info)
        
        if not metadata_dict:
            return ""
        
        # Generate YAML
        try:
            if self.default_config["yaml_style"] == "flow":
                yaml_content = yaml.dump(metadata_dict, default_flow_style=True, allow_unicode=True)
            else:
                yaml_content = yaml.dump(metadata_dict, default_flow_style=False, allow_unicode=True)
            
            # Wrap in front matter delimiters
            return f"---\n{yaml_content}---\n\n"
            
        except Exception as e:
            self.logger.warning(f"Failed to generate YAML front matter: {e}")
            return ""
    
    def _metadata_to_dict(self, metadata_info: MetadataInfo) -> Dict[str, Any]:
        """
        Convert MetadataInfo to dictionary.
        
        :param metadata_info: MetadataInfo object
        :return: Dictionary representation
        """
        metadata_dict = {}
        
        # Add standard fields
        if metadata_info.title:
            metadata_dict["title"] = metadata_info.title
        if metadata_info.author:
            metadata_dict["author"] = metadata_info.author
        if metadata_info.subject:
            metadata_dict["subject"] = metadata_info.subject
        if metadata_info.keywords:
            metadata_dict["keywords"] = metadata_info.keywords
        if metadata_info.created_date:
            metadata_dict["created_date"] = metadata_info.created_date
        if metadata_info.modified_date:
            metadata_dict["modified_date"] = metadata_info.modified_date
        if metadata_info.creator:
            metadata_dict["creator"] = metadata_info.creator
        if metadata_info.producer:
            metadata_dict["producer"] = metadata_info.producer
        if metadata_info.language:
            metadata_dict["language"] = metadata_info.language
        if metadata_info.page_count:
            metadata_dict["page_count"] = metadata_info.page_count
        if metadata_info.word_count:
            metadata_dict["word_count"] = metadata_info.word_count
        if metadata_info.file_size:
            metadata_dict["file_size"] = metadata_info.file_size
        if metadata_info.format:
            metadata_dict["format"] = metadata_info.format
        
        # Add custom fields
        if metadata_info.custom_fields:
            metadata_dict.update(metadata_info.custom_fields)
        
        return metadata_dict
    
    def _add_front_matter_to_content(self, content: str, front_matter: str) -> str:
        """
        Add front matter to content.
        
        :param content: Input content
        :param front_matter: Front matter to add
        :return: Content with front matter
        """
        if not front_matter:
            return content
        
        # Check if content already has front matter
        if content.startswith('---'):
            # Find end of existing front matter
            lines = content.split('\n')
            end_index = -1
            
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    end_index = i
                    break
            
            if end_index > 0:
                # Replace existing front matter
                return front_matter + '\n'.join(lines[end_index + 1:])
        
        # Add front matter at beginning
        return front_matter + content
    
    def _is_valid_metadata_value(self, value: Any) -> bool:
        """
        Check if a metadata value is valid.
        
        :param value: Value to check
        :return: True if value is valid
        """
        if value is None:
            return False
        
        if isinstance(value, str):
            # Check length limit
            if len(value) > self.default_config["max_field_length"]:
                return False
            
            # Check for empty or whitespace-only strings
            if not value.strip():
                return False
        
        return True
    
    def _clean_metadata_value(self, value: str) -> str:
        """
        Clean a metadata value.
        
        :param value: Value to clean
        :return: Cleaned value
        """
        if not value:
            return ""
        
        # Remove extra whitespace
        value = re.sub(r'\s+', ' ', value.strip())
        
        # Truncate if too long
        max_length = self.default_config["max_field_length"]
        if len(value) > max_length:
            value = value[:max_length-3] + "..."
        
        return value
    
    def get_processor_info(self) -> Dict[str, Any]:
        """
        Get information about this processor.
        
        :return: Dictionary with processor information
        """
        return {
            "name": "MetadataProcessor",
            "description": "Specialized processor for metadata extraction and YAML front matter",
            "config": self.default_config
        } 