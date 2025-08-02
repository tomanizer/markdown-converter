"""
PDF Document Parser

This module provides specialized parsing for PDF documents (.pdf)
using pdfplumber as the primary processor and PyMuPDF as a fallback.
"""

import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple

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
                "extract_images": True,  # Enhanced image extraction
                "extract_text": True,
                "table_settings": {
                    "vertical_strategy": "text",
                    "horizontal_strategy": "text",
                    "intersection_tolerance": 3,
                    "min_words_vertical": 3,
                    "min_words_horizontal": 1,
                },
            },
            # Fallback processor (PyMuPDF)
            "use_pymupdf": True,
            "pymupdf_options": {
                "extract_text": True,
                "extract_images": True,
                "extract_tables": True,
                "ocr_enabled": False,
            },
            # Output settings
            "preserve_page_breaks": False,
            "extract_tables": True,
            "extract_images": True,
            "preserve_layout": True,
            "extract_metadata": True,
            "extract_fonts": True,
            # Performance settings
            "max_pages_per_batch": 10,
            "memory_limit_mb": 512,
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
        images = []
        metadata = {
            "parser": "pdfplumber",
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size,
            "format": "pdf",
        }

        # Open PDF and extract content
        with pdfplumber.open(file_path) as pdf:
            metadata["page_count"] = len(pdf.pages)
            
            # Extract document metadata
            if hasattr(pdf, 'metadata') and pdf.metadata:
                metadata.update(self._extract_pdf_metadata(pdf.metadata))

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

                # Extract images if enabled
                if self.default_config["extract_images"]:
                    page_images = self._extract_images_from_page(page, page_num)
                    images.extend(page_images)

        # Combine all content
        content = "\n".join(content_parts)

        # Add metadata
        if tables:
            metadata["tables"] = tables
        if images:
            metadata["images"] = images

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
        tables = []
        images = []
        metadata = {
            "parser": "pymupdf",
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size,
            "format": "pdf",
        }

        # Open PDF and extract content
        doc = fitz.open(file_path)
        metadata["page_count"] = len(doc)

        # Extract document metadata
        doc_metadata = doc.metadata
        if doc_metadata:
            metadata.update(self._extract_pdf_metadata(doc_metadata))

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            # Extract text
            text = page.get_text()
            if text and text.strip():
                if self.default_config["preserve_page_breaks"]:
                    content_parts.append(f"## Page {page_num + 1}")
                content_parts.append(text.strip())
                content_parts.append("")  # Add blank line

            # Extract tables using PyMuPDF
            if self.default_config["extract_tables"]:
                page_tables = self._extract_tables_pymupdf(page, page_num + 1)
                tables.extend(page_tables)

            # Extract images
            if self.default_config["extract_images"]:
                page_images = self._extract_images_pymupdf(page, page_num + 1)
                images.extend(page_images)

        doc.close()

        # Combine all content
        content = "\n".join(content_parts)

        # Add metadata
        if tables:
            metadata["tables"] = tables
        if images:
            metadata["images"] = images

        return ParserResult(
            content=content, metadata=metadata, format="markdown", messages=[]
        )

    def _extract_images_from_page(self, page, page_num: int) -> List[Dict]:
        """
        Extract images from a page using pdfplumber.

        :param page: pdfplumber page object
        :param page_num: Page number
        :return: List of image metadata
        """
        images = []
        
        try:
            # pdfplumber doesn't directly support image extraction
            # This is a placeholder for future implementation
            pass
        except Exception as e:
            self.logger.warning(f"Image extraction failed: {e}")
            
        return images

    def _extract_tables_pymupdf(self, page, page_num: int) -> List[Dict]:
        """
        Extract tables using PyMuPDF.

        :param page: PyMuPDF page object
        :param page_num: Page number
        :return: List of table dictionaries
        """
        tables = []
        
        try:
            # PyMuPDF doesn't have built-in table extraction
            # We'll use a simple approach based on text positioning
            text_dict = page.get_text("dict")
            
            if "blocks" in text_dict:
                # Group text by vertical position to identify potential tables
                text_blocks = []
                for block in text_dict["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                text_blocks.append({
                                    "text": span["text"],
                                    "bbox": span["bbox"],
                                    "y": span["bbox"][1]
                                })
                
                # Simple table detection based on alignment
                if text_blocks:
                    tables = self._detect_tables_from_text_blocks(text_blocks, page_num)
                    
        except Exception as e:
            self.logger.warning(f"PyMuPDF table extraction failed: {e}")
            
        return tables

    def _extract_images_pymupdf(self, page, page_num: int) -> List[Dict]:
        """
        Extract images from a page using PyMuPDF.

        :param page: PyMuPDF page object
        :param page_num: Page number
        :return: List of image metadata
        """
        images = []
        
        try:
            import fitz  # PyMuPDF
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    pix = fitz.Pixmap(page.parent, xref)
                    
                    if pix.n - pix.alpha < 4:  # GRAY or RGB
                        img_data = {
                            "page": page_num,
                            "image_index": img_index,
                            "width": pix.width,
                            "height": pix.height,
                            "colorspace": pix.colorspace.name if pix.colorspace else "unknown",
                            "size_bytes": len(pix.tobytes()),
                        }
                        images.append(img_data)
                    
                    pix = None  # Free memory
                    
                except Exception as e:
                    self.logger.warning(f"Failed to extract image {img_index}: {e}")
                    
        except Exception as e:
            self.logger.warning(f"PyMuPDF image extraction failed: {e}")
            
        return images

    def _detect_tables_from_text_blocks(self, text_blocks: List[Dict], page_num: int) -> List[Dict]:
        """
        Detect tables from text blocks based on positioning.

        :param text_blocks: List of text blocks with positioning
        :param page_num: Page number
        :return: List of detected tables
        """
        tables = []
        
        try:
            # Group text by similar Y positions (rows)
            y_tolerance = 5
            rows = {}
            
            for block in text_blocks:
                y_key = round(block["y"] / y_tolerance) * y_tolerance
                if y_key not in rows:
                    rows[y_key] = []
                rows[y_key].append(block)
            
            # Sort rows by Y position
            sorted_rows = sorted(rows.items(), key=lambda x: x[0])
            
            # Convert to table format
            if len(sorted_rows) > 1:  # At least 2 rows for a table
                table_data = []
                for _, row_blocks in sorted_rows:
                    # Sort blocks in row by X position
                    row_blocks.sort(key=lambda b: b["bbox"][0])
                    row = [block["text"] for block in row_blocks]
                    table_data.append(row)
                
                if table_data:
                    table_markdown = self._convert_table_to_markdown(table_data)
                    tables.append({
                        "page": page_num,
                        "table_num": len(tables) + 1,
                        "content": table_markdown,
                        "detection_method": "text_positioning"
                    })
                    
        except Exception as e:
            self.logger.warning(f"Table detection failed: {e}")
            
        return tables

    def _extract_pdf_metadata(self, metadata: Dict) -> Dict:
        """
        Extract and clean PDF metadata.

        :param metadata: Raw PDF metadata
        :return: Cleaned metadata dictionary
        """
        cleaned_metadata = {}
        
        # Common metadata fields
        metadata_fields = [
            "title", "author", "subject", "creator", "producer",
            "creationDate", "modDate", "keywords"
        ]
        
        for field in metadata_fields:
            if field in metadata and metadata[field]:
                # Clean the value
                value = str(metadata[field]).strip()
                if value and value != "null":
                    cleaned_metadata[field] = value
        
        return cleaned_metadata

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
