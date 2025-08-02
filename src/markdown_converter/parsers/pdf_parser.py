"""
PDF Document Parser

This module provides specialized parsing for PDF documents (.pdf)
using pdfplumber as the primary processor and PyMuPDF as a fallback.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ..core.exceptions import ParserError, UnsupportedFormatError
from .base import BaseParser, ParserResult


class PDFParser(BaseParser):
    """
    Specialized parser for PDF documents (.pdf).

    Uses pdfplumber as the primary processor for text and table extraction,
    with PyMuPDF as a fallback for complex PDFs.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the PDF parser.

        :param config: Configuration dictionary
        """
        super().__init__(config)
        self.logger = logging.getLogger("PDFParser")
        self._setup_default_config()
        self._validate_dependencies()

    def _setup_default_config(self) -> None:
        """Setup default configuration for PDF parsing."""
        self.default_config = {
            # Primary processor (pdfplumber)
            "use_pdfplumber": True,
            "pdfplumber_options": {
                "extract_tables": True,
                "extract_images": False,
                "extract_text": True,
                "table_settings": {
                    "vertical_strategy": "text",
                    "horizontal_strategy": "text",
                    "intersection_tolerance": 3,
                },
            },
            # Fallback processor (PyMuPDF)
            "use_pymupdf": True,
            "pymupdf_options": {
                "extract_text": True,
                "extract_images": False,
                "extract_tables": False,
                "ocr_enabled": False,
            },
            # Output settings
            "preserve_page_breaks": True,
            "extract_tables": True,
            "extract_images": False,
            "ocr_fallback": False,
        }

        # Merge with user config
        if self.config:
            self.default_config.update(self.config)

    def _validate_dependencies(self) -> None:
        """Validate that required dependencies are available."""
        try:
            import pdfplumber

            self.pdfplumber_available = True
        except ImportError:
            self.pdfplumber_available = False
            self.logger.warning("pdfplumber not available, will use PyMuPDF fallback")

        try:
            import fitz  # PyMuPDF

            self.pymupdf_available = True
        except ImportError:
            self.pymupdf_available = False
            self.logger.warning("PyMuPDF not available")

        if not self.pdfplumber_available and not self.pymupdf_available:
            raise ParserError("Neither pdfplumber nor PyMuPDF are available")

    def can_parse(self, file_path: Union[str, Path]) -> bool:
        """
        Check if this parser can handle the given file.

        :param file_path: Path to the file
        :return: True if the file can be parsed
        """
        file_path = Path(file_path)
        return file_path.suffix.lower() == ".pdf"

    def parse(self, file_path: Union[str, Path]) -> ParserResult:
        """
        Parse a PDF document and extract its content.

        :param file_path: Path to the PDF document
        :return: ParserResult with extracted content and metadata
        :raises: ParserError if parsing fails
        """
        file_path = Path(file_path)

        if not self.can_parse(file_path):
            raise UnsupportedFormatError(f"Cannot parse {file_path.suffix} files")

        self.logger.info(f"Parsing PDF document: {file_path}")

        try:
            # Try pdfplumber first (preferred for text and tables)
            if self.default_config["use_pdfplumber"] and self.pdfplumber_available:
                try:
                    return self._parse_with_pdfplumber(file_path)
                except Exception as e:
                    self.logger.warning(
                        f"pdfplumber parsing failed: {e}, trying PyMuPDF"
                    )

            # Fallback to PyMuPDF
            if self.default_config["use_pymupdf"] and self.pymupdf_available:
                return self._parse_with_pymupdf(file_path)

            raise ParserError("No available PDF parser found")

        except Exception as e:
            self.logger.error(f"PDF parsing failed for {file_path}: {e}")
            raise ParserError(f"Failed to parse PDF document {file_path}: {e}")

    def _parse_with_pdfplumber(self, file_path: Path) -> ParserResult:
        """
        Parse PDF document using pdfplumber.

        :param file_path: Path to the PDF document
        :return: ParserResult with extracted content
        """
        import pdfplumber

        self.logger.debug(f"Using pdfplumber to parse {file_path}")

        content_parts = []
        tables = []
        metadata = {
            "parser": "pdfplumber",
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size,
            "format": "pdf",
        }

        # Open PDF and extract content
        with pdfplumber.open(file_path) as pdf:
            metadata["page_count"] = len(pdf.pages)

            for page_num, page in enumerate(pdf.pages, 1):
                self.logger.debug(f"Processing page {page_num}")

                # Extract text
                text = page.extract_text()
                if text and text.strip():
                    content_parts.append(f"## Page {page_num}")
                    content_parts.append(text.strip())
                    content_parts.append("")  # Add blank line

                # Extract tables if enabled
                if self.default_config["extract_tables"]:
                    page_tables = page.extract_tables()
                    for table_num, table in enumerate(page_tables, 1):
                        if table:
                            table_markdown = self._convert_table_to_markdown(table)
                            if table_markdown:
                                content_parts.append(
                                    f"### Table {table_num} (Page {page_num})"
                                )
                                content_parts.append(table_markdown)
                                content_parts.append("")  # Add blank line
                                tables.append(
                                    {
                                        "page": page_num,
                                        "table_num": table_num,
                                        "content": table_markdown,
                                    }
                                )

        # Combine all content
        content = "\n".join(content_parts)

        # Add table metadata
        if tables:
            metadata["tables"] = tables

        return ParserResult(
            content=content, metadata=metadata, format="markdown", messages=[]
        )

    def _parse_with_pymupdf(self, file_path: Path) -> ParserResult:
        """
        Parse PDF document using PyMuPDF.

        :param file_path: Path to the PDF document
        :return: ParserResult with extracted content
        """
        import fitz  # PyMuPDF

        self.logger.debug(f"Using PyMuPDF to parse {file_path}")

        content_parts = []
        metadata = {
            "parser": "pymupdf",
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size,
            "format": "pdf",
        }

        # Open PDF and extract content
        doc = fitz.open(file_path)
        metadata["page_count"] = len(doc)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            # Extract text
            text = page.get_text()
            if text and text.strip():
                if self.default_config["preserve_page_breaks"]:
                    content_parts.append(f"## Page {page_num + 1}")
                content_parts.append(text.strip())
                content_parts.append("")  # Add blank line

        # Extract document metadata
        doc_metadata = doc.metadata
        if doc_metadata:
            metadata.update(
                {
                    "title": doc_metadata.get("title", ""),
                    "author": doc_metadata.get("author", ""),
                    "subject": doc_metadata.get("subject", ""),
                    "creator": doc_metadata.get("creator", ""),
                    "producer": doc_metadata.get("producer", ""),
                    "creation_date": doc_metadata.get("creationDate", ""),
                    "modification_date": doc_metadata.get("modDate", ""),
                }
            )

        doc.close()

        # Combine all content
        content = "\n".join(content_parts)

        return ParserResult(
            content=content, metadata=metadata, format="markdown", messages=[]
        )

    def _convert_table_to_markdown(self, table: List[List[str]]) -> str:
        """
        Convert a table to markdown format.

        :param table: List of table rows (each row is a list of cells)
        :return: Markdown table string
        """
        if not table or not table[0]:
            return ""

        markdown_lines = []

        # Process each row
        for i, row in enumerate(table):
            # Clean and escape cell content
            cells = []
            for cell in row:
                if cell is None:
                    cell_text = ""
                else:
                    cell_text = str(cell).strip().replace("|", "\\|")
                cells.append(cell_text)

            # Create markdown row
            markdown_row = "| " + " | ".join(cells) + " |"
            markdown_lines.append(markdown_row)

            # Add separator row after header
            if i == 0:
                separator = "| " + " | ".join(["---"] * len(cells)) + " |"
                markdown_lines.append(separator)

        return "\n".join(markdown_lines)

    def get_supported_formats(self) -> List[str]:
        """
        Get list of supported file formats.

        :return: List of supported format extensions
        """
        return [".pdf"]

    def get_parser_info(self) -> Dict[str, Any]:
        """
        Get information about this parser.

        :return: Dictionary with parser information
        """
        return {
            "name": "PDFParser",
            "description": "Specialized parser for PDF documents",
            "supported_formats": self.get_supported_formats(),
            "dependencies": {
                "pdfplumber": self.pdfplumber_available,
                "pymupdf": self.pymupdf_available,
            },
            "config": self.default_config,
        }
