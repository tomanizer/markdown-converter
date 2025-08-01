"""
Parsers module for the markdown converter.

This module contains all document parsers for different file formats.
"""

from .base import BaseParser, ParserRegistry, ParserResult, parser_registry
from .word_parser import WordParser
from .pdf_parser import PDFParser
from .excel_parser import ExcelParser
from .html_parser import HTMLParser

__all__ = [
    "BaseParser",
    "ParserRegistry",
    "ParserResult",
    "parser_registry",
    "WordParser",
    "PDFParser",
    "ExcelParser",
    "HTMLParser",
]
