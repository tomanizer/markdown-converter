"""
Image Processor

This module provides specialized processing for image extraction,
file management, and markdown link generation.
"""

import logging
import re
import shutil
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Tuple
from dataclasses import dataclass
import tempfile
import os

from .base import BaseProcessor, ProcessingResult
from ..core.exceptions import ProcessorError


@dataclass
class ImageInfo:
    """Information about an extracted image."""
    original_path: str
    extracted_path: str
    filename: str
    format: str
    size: int
    width: Optional[int] = None
    height: Optional[int] = None
    alt_text: Optional[str] = None


class ImageProcessor(BaseProcessor):
    """
    Specialized processor for image extraction and management.
    
    Extracts images from documents, saves them separately,
    and generates markdown image links.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the image processor.
        
        :param config: Configuration dictionary
        """
        super().__init__(config)
        self.logger = logging.getLogger("ImageProcessor")
        self._setup_default_config()
    
    def _setup_default_config(self) -> None:
        """Setup default configuration for image processing."""
        self.default_config = {
            # Image extraction settings
            "extract_images": True,
            "supported_formats": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp"],
            "max_image_size": 10 * 1024 * 1024,  # 10MB
            "min_image_size": 1024,  # 1KB
            
            # File management settings
            "output_dir": "images",
            "preserve_structure": True,
            "use_hash_names": False,
            "overwrite_existing": False,
            
            # Markdown link settings
            "generate_links": True,
            "use_relative_paths": True,
            "add_alt_text": True,
            "link_format": "markdown",  # 'markdown', 'html'
            
            # Processing settings
            "compress_images": False,
            "resize_large_images": False,
            "max_width": 1920,
            "max_height": 1080,
            "quality": 85,
            
            # Error handling
            "skip_failed_images": True,
            "log_failures": True,
        }
        
        # Merge with user config
        if self.config:
            self.default_config.update(self.config)
    
    def process(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        """
        Process content to extract and manage images.
        
        :param content: Input content
        :param metadata: Optional metadata
        :return: ProcessingResult with processed content
        """
        self.logger.info("Processing images in content")
        
        try:
            # Extract image references from content
            image_refs = self._extract_image_references(content)
            
            if not image_refs:
                self.logger.debug("No image references found")
                return ProcessingResult(
                    content=content,
                    metadata=metadata or {},
                    messages=["No image references found"]
                )
            
            # Process each image reference
            processed_content = content
            image_metadata = []
            
            for i, image_ref in enumerate(image_refs):
                self.logger.debug(f"Processing image {i+1}: {image_ref}")
                
                try:
                    # Extract and save image
                    image_info = self._extract_image(image_ref, i + 1)
                    
                    if image_info:
                        # Generate markdown link
                        markdown_link = self._generate_image_link(image_info)
                        
                        # Replace image reference in content
                        processed_content = processed_content.replace(
                            image_ref, markdown_link
                        )
                        
                        # Add image metadata
                        image_metadata.append({
                            "image_index": i + 1,
                            "original_path": image_info.original_path,
                            "extracted_path": image_info.extracted_path,
                            "filename": image_info.filename,
                            "format": image_info.format,
                            "size": image_info.size,
                            "width": image_info.width,
                            "height": image_info.height,
                            "alt_text": image_info.alt_text
                        })
                    
                except Exception as e:
                    self.logger.warning(f"Failed to process image {image_ref}: {e}")
                    if self.default_config["log_failures"]:
                        image_metadata.append({
                            "image_index": i + 1,
                            "original_path": image_ref,
                            "error": str(e)
                        })
            
            # Update metadata
            if metadata is None:
                metadata = {}
            metadata["images"] = image_metadata
            metadata["image_count"] = len(image_refs)
            
            messages = [f"Processed {len(image_refs)} images"]
            
            return ProcessingResult(
                content=processed_content,
                metadata=metadata,
                messages=messages
            )
            
        except Exception as e:
            self.logger.error(f"Image processing failed: {e}")
            raise ProcessorError(f"Failed to process images: {e}")
    
    def _extract_image_references(self, content: str) -> List[str]:
        """
        Extract image references from content.
        
        :param content: Input content
        :return: List of image references
        """
        image_refs = []
        seen_paths = set()
        
        # Look for markdown image links: ![alt](path)
        markdown_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        for match in re.finditer(markdown_pattern, content):
            alt_text, image_path = match.groups()
            if image_path not in seen_paths:
                image_refs.append(match.group(0))
                seen_paths.add(image_path)
        
        # Look for HTML img tags: <img src="path" alt="alt">
        html_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
        for match in re.finditer(html_pattern, content):
            image_path = match.group(1)
            if image_path not in seen_paths:
                image_refs.append(match.group(0))
                seen_paths.add(image_path)
        
        # Look for direct file paths (only if not already found)
        file_pattern = r'\b[\w\-\./]+\.(png|jpg|jpeg|gif|bmp|svg|webp)\b'
        for match in re.finditer(file_pattern, content, re.IGNORECASE):
            image_path = match.group(0)
            if self._is_valid_image_path(image_path) and image_path not in seen_paths:
                image_refs.append(image_path)
                seen_paths.add(image_path)
        
        return image_refs
    
    def _is_valid_image_path(self, path: str) -> bool:
        """
        Check if a path is a valid image file.
        
        :param path: File path
        :return: True if path is a valid image file
        """
        path_obj = Path(path)
        extension = path_obj.suffix.lower()
        
        return extension in self.default_config["supported_formats"]
    
    def _extract_image(self, image_ref: str, index: int) -> Optional[ImageInfo]:
        """
        Extract and save an image.
        
        :param image_ref: Image reference
        :param index: Image index
        :return: ImageInfo if successful, None otherwise
        """
        # Determine image path from reference
        image_path = self._extract_image_path(image_ref)
        if not image_path:
            return None
        
        # Check if image exists and is valid
        if not self._validate_image_file(image_path):
            return None
        
        # Create output directory
        output_dir = Path(self.default_config["output_dir"])
        output_dir.mkdir(exist_ok=True)
        
        # Generate output filename
        output_filename = self._generate_output_filename(image_path, index)
        output_path = output_dir / output_filename
        
        # Copy/save image
        try:
            shutil.copy2(image_path, output_path)
            
            # Get image information
            image_info = self._get_image_info(image_path, output_path, image_ref)
            
            self.logger.debug(f"Extracted image: {image_path} -> {output_path}")
            return image_info
            
        except Exception as e:
            self.logger.error(f"Failed to extract image {image_path}: {e}")
            return None
    
    def _extract_image_path(self, image_ref: str) -> Optional[str]:
        """
        Extract image path from various reference formats.
        
        :param image_ref: Image reference
        :return: Image path if found, None otherwise
        """
        # Markdown image link: ![alt](path)
        markdown_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', image_ref)
        if markdown_match:
            return markdown_match.group(2)
        
        # HTML img tag: <img src="path" alt="alt">
        html_match = re.search(r'src=["\']([^"\']+)["\']', image_ref)
        if html_match:
            return html_match.group(1)
        
        # Direct file path
        if self._is_valid_image_path(image_ref):
            return image_ref
        
        return None
    
    def _validate_image_file(self, image_path: str) -> bool:
        """
        Validate that an image file exists and meets requirements.
        
        :param image_path: Image file path
        :return: True if image is valid
        """
        try:
            path_obj = Path(image_path)
            
            # Check if file exists
            if not path_obj.exists():
                self.logger.warning(f"Image file not found: {image_path}")
                return False
            
            # Check file size
            file_size = path_obj.stat().st_size
            if file_size < self.default_config["min_image_size"]:
                self.logger.warning(f"Image file too small: {image_path} ({file_size} bytes)")
                return False
            
            if file_size > self.default_config["max_image_size"]:
                self.logger.warning(f"Image file too large: {image_path} ({file_size} bytes)")
                return False
            
            # Check file extension
            extension = path_obj.suffix.lower()
            if extension not in self.default_config["supported_formats"]:
                self.logger.warning(f"Unsupported image format: {image_path}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating image file {image_path}: {e}")
            return False
    
    def _generate_output_filename(self, image_path: str, index: int) -> str:
        """
        Generate output filename for extracted image.
        
        :param image_path: Original image path
        :param index: Image index
        :return: Output filename
        """
        path_obj = Path(image_path)
        extension = path_obj.suffix.lower()
        
        if self.default_config["use_hash_names"]:
            # Use hash-based naming
            with open(image_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()[:8]
            return f"image_{file_hash}{extension}"
        else:
            # Use original filename with index
            stem = path_obj.stem
            return f"image_{index:03d}_{stem}{extension}"
    
    def _get_image_info(self, original_path: str, extracted_path: str, image_ref: str) -> ImageInfo:
        """
        Get information about an image.
        
        :param original_path: Original image path
        :param extracted_path: Extracted image path
        :param image_ref: Original image reference
        :return: ImageInfo object
        """
        path_obj = Path(original_path)
        
        # Get basic information
        size = path_obj.stat().st_size
        format_ext = path_obj.suffix.lower()
        filename = path_obj.name
        
        # Extract alt text from reference
        alt_text = self._extract_alt_text(image_ref)
        
        # Try to get image dimensions (basic implementation)
        width, height = self._get_image_dimensions(original_path)
        
        return ImageInfo(
            original_path=original_path,
            extracted_path=str(extracted_path),
            filename=filename,
            format=format_ext,
            size=size,
            width=width,
            height=height,
            alt_text=alt_text
        )
    
    def _extract_alt_text(self, image_ref: str) -> Optional[str]:
        """
        Extract alt text from image reference.
        
        :param image_ref: Image reference
        :return: Alt text if found, None otherwise
        """
        # Markdown image link: ![alt](path)
        markdown_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', image_ref)
        if markdown_match:
            alt_text = markdown_match.group(1)
            return alt_text if alt_text else None
        
        # HTML img tag: <img src="path" alt="alt">
        html_match = re.search(r'alt=["\']([^"\']+)["\']', image_ref)
        if html_match:
            return html_match.group(1)
        
        return None
    
    def _get_image_dimensions(self, image_path: str) -> Tuple[Optional[int], Optional[int]]:
        """
        Get image dimensions (basic implementation).
        
        :param image_path: Image file path
        :return: Tuple of (width, height) or (None, None)
        """
        # This is a basic implementation
        # In a real implementation, you might use PIL/Pillow or other image libraries
        try:
            # For now, return None for dimensions
            # This could be enhanced with actual image processing
            return None, None
        except Exception as e:
            self.logger.debug(f"Could not get image dimensions for {image_path}: {e}")
            return None, None
    
    def _generate_image_link(self, image_info: ImageInfo) -> str:
        """
        Generate markdown image link.
        
        :param image_info: Image information
        :return: Markdown image link
        """
        if self.default_config["link_format"] == "html":
            return self._generate_html_image_link(image_info)
        else:
            return self._generate_markdown_image_link(image_info)
    
    def _generate_markdown_image_link(self, image_info: ImageInfo) -> str:
        """
        Generate markdown image link.
        
        :param image_info: Image information
        :return: Markdown image link
        """
        # Determine link path
        if self.default_config["use_relative_paths"]:
            link_path = f"{self.default_config['output_dir']}/{image_info.filename}"
        else:
            link_path = image_info.extracted_path
        
        # Generate alt text
        if image_info.alt_text:
            alt_text = image_info.alt_text
        else:
            alt_text = image_info.filename
        
        return f"![{alt_text}]({link_path})"
    
    def _generate_html_image_link(self, image_info: ImageInfo) -> str:
        """
        Generate HTML image tag.
        
        :param image_info: Image information
        :return: HTML image tag
        """
        # Determine link path
        if self.default_config["use_relative_paths"]:
            link_path = f"{self.default_config['output_dir']}/{image_info.filename}"
        else:
            link_path = image_info.extracted_path
        
        # Generate alt text
        if image_info.alt_text:
            alt_text = image_info.alt_text
        else:
            alt_text = image_info.filename
        
        # Generate HTML attributes
        attributes = [f'src="{link_path}"', f'alt="{alt_text}"']
        
        if image_info.width:
            attributes.append(f'width="{image_info.width}"')
        if image_info.height:
            attributes.append(f'height="{image_info.height}"')
        
        return f"<img {' '.join(attributes)} />"
    
    def get_processor_info(self) -> Dict[str, Any]:
        """
        Get information about this processor.
        
        :return: Dictionary with processor information
        """
        return {
            "name": "ImageProcessor",
            "description": "Specialized processor for image extraction and management",
            "supported_formats": self.default_config["supported_formats"],
            "config": self.default_config
        } 