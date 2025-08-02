"""
Parsers module for the markdown converter.

This module contains all document parsers for different file formats.
"""

from .base import BaseParser, ParserRegistry, ParserResult, parser_registry
from .excel_parser import ExcelParser
from .html_parser import HTMLParser
from .pandoc_parser import PandocParser
from .pdf_parser import PDFParser
from .word_parser import WordParser

__all__ = [
    "BaseParser",
    "ParserRegistry",
    "ParserResult",
    "parser_registry",
    "WordParser",
    "PDFParser",
    "ExcelParser",
    "HTMLParser",
    "PandocParser",
]
