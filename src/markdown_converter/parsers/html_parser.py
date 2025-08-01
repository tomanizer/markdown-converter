"""
HTML Document Parser

This module provides specialized parsing for HTML documents (.html, .htm)
using beautifulsoup4 for HTML parsing and cleaning.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import tempfile
import os

from .base import BaseParser, ParserResult
from ..core.exceptions import ParserError, UnsupportedFormatError


class HTMLParser(BaseParser):
    """
    Specialized parser for HTML documents (.html, .htm).
    
    Uses beautifulsoup4 for HTML parsing and cleaning.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the HTML parser.
        
        :param config: Configuration dictionary
        """
        super().__init__(config)
        self.logger = logging.getLogger("HTMLParser")
        self._setup_default_config()
        self._validate_dependencies()
    
    def _setup_default_config(self) -> None:
        """Setup default configuration for HTML parsing."""
        self.default_config = {
            # BeautifulSoup options
            "parser": "html.parser",  # or "lxml", "html5lib"
            "extract_text": True,
            "extract_tables": True,
            "extract_images": True,
            "extract_links": True,
            # Cleaning options
            "remove_scripts": True,
            "remove_styles": True,
            "remove_comments": True,
            "remove_meta": False,
            "preserve_structure": True,
            # Output options
            "convert_to_markdown": True,
            "include_metadata": True,
        }
        
        # Merge with user config
        if self.config:
            self.default_config.update(self.config)
    
    def _validate_dependencies(self) -> None:
        """Validate that required dependencies are available."""
        try:
            import bs4
            self.beautifulsoup_available = True
        except ImportError:
            self.beautifulsoup_available = False
            self.logger.warning("beautifulsoup4 not available")
        
        if not self.beautifulsoup_available:
            raise ParserError("beautifulsoup4 is required for HTML parsing")
    
    def can_parse(self, file_path: Union[str, Path]) -> bool:
        """
        Check if this parser can handle the given file.
        
        :param file_path: Path to the file
        :return: True if the file can be parsed
        """
        file_path = Path(file_path)
        return file_path.suffix.lower() in ['.html', '.htm']
    
    def parse(self, file_path: Union[str, Path]) -> ParserResult:
        """
        Parse an HTML document and extract its content.
        
        :param file_path: Path to the HTML document
        :return: ParserResult with extracted content and metadata
        :raises: ParserError if parsing fails
        """
        file_path = Path(file_path)
        
        if not self.can_parse(file_path):
            raise UnsupportedFormatError(f"Cannot parse {file_path.suffix} files")
        
        self.logger.info(f"Parsing HTML document: {file_path}")
        
        try:
            return self._parse_with_beautifulsoup(file_path)
        except Exception as e:
            self.logger.error(f"HTML parsing failed for {file_path}: {e}")
            raise ParserError(f"Failed to parse HTML document {file_path}: {e}")
    
    def _parse_with_beautifulsoup(self, file_path: Path) -> ParserResult:
        """
        Parse HTML document using beautifulsoup4.
        
        :param file_path: Path to the HTML document
        :return: ParserResult with extracted content
        """
        from bs4 import BeautifulSoup
        
        self.logger.debug(f"Using beautifulsoup4 to parse {file_path}")
        
        # Read HTML file
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Parse HTML
        soup = BeautifulSoup(html_content, self.default_config["parser"])
        
        # Extract metadata
        metadata = self._extract_metadata(soup, file_path)
        
        # Clean HTML if needed
        if self.default_config["remove_scripts"]:
            for script in soup(["script", "style"]):
                script.decompose()
        
        # Extract content
        content = self._extract_content(soup)
        
        return ParserResult(
            content=content,
            metadata=metadata,
            format="markdown" if self.default_config["convert_to_markdown"] else "html",
            messages=[]
        )
    
    def _extract_metadata(self, soup, file_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from HTML document.
        
        :param soup: BeautifulSoup object
        :param file_path: Path to the HTML file
        :return: Dictionary of metadata
        """
        metadata = {
            "parser": "beautifulsoup4",
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size,
            "format": "html"
        }
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            metadata["title"] = title_tag.get_text().strip()
        
        # Extract meta tags
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name', meta.get('property', ''))
            content = meta.get('content', '')
            if name and content:
                metadata[f"meta_{name}"] = content
        
        # Extract document structure info
        metadata["headings"] = {
            "h1": len(soup.find_all('h1')),
            "h2": len(soup.find_all('h2')),
            "h3": len(soup.find_all('h3')),
            "h4": len(soup.find_all('h4')),
            "h5": len(soup.find_all('h5')),
            "h6": len(soup.find_all('h6')),
        }
        
        metadata["links"] = len(soup.find_all('a'))
        metadata["images"] = len(soup.find_all('img'))
        metadata["tables"] = len(soup.find_all('table'))
        
        return metadata
    
    def _extract_content(self, soup) -> str:
        """
        Extract content from HTML document.
        
        :param soup: BeautifulSoup object
        :return: Extracted content as markdown or HTML
        """
        if self.default_config["convert_to_markdown"]:
            return self._convert_to_markdown(soup)
        else:
            return self._extract_clean_html(soup)
    
    def _convert_to_markdown(self, soup) -> str:
        """
        Convert HTML to markdown.
        
        :param soup: BeautifulSoup object
        :return: Markdown content
        """
        content_parts = []
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()
            if title:
                content_parts.append(f"# {title}")
                content_parts.append("")
        
        # Extract headings and content
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'table', 'ul', 'ol']):
            if element.name.startswith('h'):
                level = int(element.name[1])
                text = element.get_text().strip()
                if text:
                    content_parts.append(f"{'#' * level} {text}")
                    content_parts.append("")
            
            elif element.name == 'p':
                text = element.get_text().strip()
                if text:
                    content_parts.append(text)
                    content_parts.append("")
            
            elif element.name == 'table':
                table_markdown = self._convert_table_to_markdown(element)
                if table_markdown:
                    content_parts.append(table_markdown)
                    content_parts.append("")
            
            elif element.name in ['ul', 'ol']:
                list_markdown = self._convert_list_to_markdown(element)
                if list_markdown:
                    content_parts.append(list_markdown)
                    content_parts.append("")
        
        return "\n".join(content_parts)
    
    def _convert_table_to_markdown(self, table_element) -> str:
        """
        Convert HTML table to markdown.
        
        :param table_element: BeautifulSoup table element
        :return: Markdown table string
        """
        rows = table_element.find_all('tr')
        if not rows:
            return ""
        
        markdown_lines = []
        
        for i, row in enumerate(rows):
            cells = row.find_all(['td', 'th'])
            if not cells:
                continue
            
            # Convert cells to text
            cell_texts = []
            for cell in cells:
                text = cell.get_text().strip().replace('|', '\\|')
                cell_texts.append(text)
            
            # Create markdown row
            markdown_row = "| " + " | ".join(cell_texts) + " |"
            markdown_lines.append(markdown_row)
            
            # Add separator row after header
            if i == 0:
                separator = "| " + " | ".join(["---"] * len(cell_texts)) + " |"
                markdown_lines.append(separator)
        
        return "\n".join(markdown_lines)
    
    def _convert_list_to_markdown(self, list_element) -> str:
        """
        Convert HTML list to markdown.
        
        :param list_element: BeautifulSoup list element
        :return: Markdown list string
        """
        items = list_element.find_all('li')
        if not items:
            return ""
        
        markdown_lines = []
        marker = "- " if list_element.name == 'ul' else "1. "
        
        for item in items:
            text = item.get_text().strip()
            if text:
                markdown_lines.append(f"{marker}{text}")
        
        return "\n".join(markdown_lines)
    
    def _extract_clean_html(self, soup) -> str:
        """
        Extract clean HTML content.
        
        :param soup: BeautifulSoup object
        :return: Clean HTML content
        """
        # Remove unwanted elements
        for element in soup.find_all(['script', 'style', 'meta', 'link']):
            element.decompose()
        
        # Get body content
        body = soup.find('body')
        if body:
            return str(body)
        else:
            return str(soup)
    
    def get_supported_formats(self) -> List[str]:
        """
        Get list of supported file formats.
        
        :return: List of supported format extensions
        """
        return ['.html', '.htm']
    
    def get_parser_info(self) -> Dict[str, Any]:
        """
        Get information about this parser.
        
        :return: Dictionary with parser information
        """
        return {
            "name": "HTMLParser",
            "description": "Specialized parser for HTML documents",
            "supported_formats": self.get_supported_formats(),
            "dependencies": {
                "beautifulsoup4": self.beautifulsoup_available
            },
            "config": self.default_config
        } 