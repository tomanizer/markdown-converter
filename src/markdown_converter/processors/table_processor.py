"""
Table Processor

This module provides specialized processing for table structures,
including detection, formatting, and markdown conversion.
"""

import logging
import re
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Tuple
from dataclasses import dataclass

from .base import BaseProcessor, ProcessingResult
from ..core.exceptions import ProcessorError


@dataclass
class TableInfo:
    """Information about a detected table."""
    content: str
    rows: int
    columns: int
    has_header: bool
    format: str  # 'markdown', 'text', 'html'
    position: Optional[int] = None


class TableProcessor(BaseProcessor):
    """
    Specialized processor for table structures.
    
    Detects table structures in content and converts them to
    properly formatted markdown tables with fallback strategies.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the table processor.
        
        :param config: Configuration dictionary
        """
        super().__init__(config)
        self.logger = logging.getLogger("TableProcessor")
        self._setup_default_config()
    
    def _setup_default_config(self) -> None:
        """Setup default configuration for table processing."""
        self.default_config = {
            # Table detection settings
            "detect_tables": True,
            "min_rows": 2,
            "min_columns": 2,
            "max_columns": 20,
            
            # Markdown table settings
            "use_markdown_tables": True,
            "align_columns": False,
            "escape_pipes": True,
            "preserve_formatting": True,
            
            # Fallback settings
            "text_fallback": True,
            "html_fallback": False,
            "separator_chars": ["|", "\t", ","],
            
            # Processing settings
            "clean_whitespace": True,
            "normalize_cells": True,
            "remove_empty_rows": True,
            "remove_empty_columns": True,
        }
        
        # Merge with user config
        if self.config:
            self.default_config.update(self.config)
    
    def process(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        """
        Process content to detect and format tables.
        
        :param content: Input content
        :param metadata: Optional metadata
        :return: ProcessingResult with processed content
        """
        self.logger.info("Processing tables in content")
        
        try:
            # Detect tables in content
            tables = self._detect_tables(content)
            
            if not tables:
                self.logger.debug("No tables detected")
                return ProcessingResult(
                    content=content,
                    metadata=metadata or {},
                    messages=["No tables detected"]
                )
            
            # Process each table
            processed_content = content
            table_metadata = []
            
            for i, table_info in enumerate(tables):
                self.logger.debug(f"Processing table {i+1}: {table_info.rows}x{table_info.columns}")
                
                # Convert table to markdown
                markdown_table = self._convert_table_to_markdown(table_info)
                
                # Replace table in content
                if table_info.position is not None:
                    # Replace at specific position
                    start_pos = table_info.position
                    end_pos = start_pos + len(table_info.content)
                    processed_content = (
                        processed_content[:start_pos] +
                        markdown_table +
                        processed_content[end_pos:]
                    )
                else:
                    # Replace by content matching
                    processed_content = processed_content.replace(
                        table_info.content, markdown_table
                    )
                
                # Add table metadata
                table_metadata.append({
                    "table_index": i + 1,
                    "rows": table_info.rows,
                    "columns": table_info.columns,
                    "has_header": table_info.has_header,
                    "format": table_info.format,
                    "position": table_info.position
                })
            
            # Update metadata
            if metadata is None:
                metadata = {}
            metadata["tables"] = table_metadata
            metadata["table_count"] = len(tables)
            
            messages = [f"Processed {len(tables)} tables"]
            
            return ProcessingResult(
                content=processed_content,
                metadata=metadata,
                messages=messages
            )
            
        except Exception as e:
            self.logger.error(f"Table processing failed: {e}")
            raise ProcessorError(f"Failed to process tables: {e}")
    
    def _detect_tables(self, content: str) -> List[TableInfo]:
        """
        Detect table structures in content.
        
        :param content: Input content
        :return: List of detected table information
        """
        tables = []
        
        # Split content into lines
        lines = content.split('\n')
        
        # Look for table patterns
        table_start = None
        current_table_lines = []
        
        for i, line in enumerate(lines):
            # Check if line looks like a table row
            if self._is_table_row(line):
                if table_start is None:
                    table_start = i
                current_table_lines.append(line)
            else:
                # End of potential table
                if table_start is not None and len(current_table_lines) >= self.default_config["min_rows"]:
                    table_info = self._analyze_table_lines(current_table_lines, table_start)
                    if table_info:
                        tables.append(table_info)
                
                # Reset for next table
                table_start = None
                current_table_lines = []
        
        # Check for table at end of content
        if table_start is not None and len(current_table_lines) >= self.default_config["min_rows"]:
            table_info = self._analyze_table_lines(current_table_lines, table_start)
            if table_info:
                tables.append(table_info)
        
        return tables
    
    def _is_table_row(self, line: str) -> bool:
        """
        Check if a line looks like a table row.
        
        :param line: Line to check
        :return: True if line appears to be a table row
        """
        line = line.strip()
        if not line:
            return False
        
        # Check for pipe-separated values (markdown table)
        if '|' in line and line.count('|') >= 1:
            return True
        
        # Check for tab-separated values
        if '\t' in line and line.count('\t') >= 1:
            return True
        
        # Check for comma-separated values (CSV-like)
        if ',' in line and line.count(',') >= 1:
            return True
        
        # Check for consistent spacing (space-separated) - very strict
        parts = line.split()
        if len(parts) >= self.default_config["min_columns"]:
            # Only consider it a table row if it has consistent spacing
            # and doesn't look like regular text
            if (len(parts) <= 8 and 
                all(len(part) < 15 for part in parts) and
                not any(part.endswith('.') for part in parts) and
                not any(part.endswith('!') for part in parts) and
                not any(part.endswith('?') for part in parts)):
                return True
        
        return False
    
    def _analyze_table_lines(self, lines: List[str], start_position: int) -> Optional[TableInfo]:
        """
        Analyze lines to determine if they form a table.
        
        :param lines: Lines to analyze
        :param start_position: Position in original content
        :return: TableInfo if valid table, None otherwise
        """
        if len(lines) < self.default_config["min_rows"]:
            return None
        
        # Determine table format and structure
        format_type = self._detect_table_format(lines)
        if not format_type:
            return None
        
        # Parse table structure
        table_data = self._parse_table_lines(lines, format_type)
        if not table_data:
            return None
        
        rows, columns = len(table_data), len(table_data[0]) if table_data else 0
        
        if columns < self.default_config["min_columns"] or columns > self.default_config["max_columns"]:
            return None
        
        # Determine if first row is header
        has_header = self._has_header_row(table_data)
        
        # Reconstruct original content
        original_content = '\n'.join(lines)
        
        return TableInfo(
            content=original_content,
            rows=rows,
            columns=columns,
            has_header=has_header,
            format=format_type,
            position=start_position
        )
    
    def _detect_table_format(self, lines: List[str]) -> Optional[str]:
        """
        Detect the format of table lines.
        
        :param lines: Lines to analyze
        :return: Format type ('markdown', 'csv', 'tsv', 'space')
        """
        if not lines:
            return None
        
        # Check for markdown table format
        if any('|' in line for line in lines):
            return 'markdown'
        
        # Check for CSV format
        if any(',' in line for line in lines):
            return 'csv'
        
        # Check for TSV format
        if any('\t' in line for line in lines):
            return 'tsv'
        
        # Check for space-separated format
        return 'space'
    
    def _parse_table_lines(self, lines: List[str], format_type: str) -> List[List[str]]:
        """
        Parse table lines into structured data.
        
        :param lines: Lines to parse
        :param format_type: Format type
        :return: List of rows, each row is a list of cells
        """
        table_data = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if format_type == 'markdown':
                # Remove leading/trailing pipes and split
                cells = [cell.strip() for cell in line.strip('|').split('|')]
            elif format_type == 'csv':
                # Simple CSV parsing (no escaping for now)
                cells = [cell.strip() for cell in line.split(',')]
            elif format_type == 'tsv':
                # Tab-separated values
                cells = [cell.strip() for cell in line.split('\t')]
            else:  # space
                # Space-separated values
                cells = line.split()
            
            # Clean and normalize cells
            if self.default_config["normalize_cells"]:
                cells = [self._normalize_cell(cell) for cell in cells]
            
            if cells:
                table_data.append(cells)
        
        # Remove empty rows
        if self.default_config["remove_empty_rows"]:
            table_data = [row for row in table_data if any(cell.strip() for cell in row)]
        
        # Remove empty columns
        if self.default_config["remove_empty_columns"] and table_data:
            table_data = self._remove_empty_columns(table_data)
        
        return table_data
    
    def _normalize_cell(self, cell: str) -> str:
        """
        Normalize cell content.
        
        :param cell: Cell content
        :return: Normalized cell content
        """
        cell = cell.strip()
        
        if self.default_config["clean_whitespace"]:
            # Replace multiple spaces with single space
            cell = re.sub(r'\s+', ' ', cell)
        
        return cell
    
    def _remove_empty_columns(self, table_data: List[List[str]]) -> List[List[str]]:
        """
        Remove columns that are entirely empty.
        
        :param table_data: Table data
        :return: Table data with empty columns removed
        """
        if not table_data:
            return table_data
        
        max_cols = max(len(row) for row in table_data)
        empty_columns = []
        
        # Find empty columns
        for col in range(max_cols):
            is_empty = True
            for row in table_data:
                if col < len(row) and row[col].strip():
                    is_empty = False
                    break
            if is_empty:
                empty_columns.append(col)
        
        # Remove empty columns (in reverse order)
        for col in reversed(empty_columns):
            for row in table_data:
                if col < len(row):
                    del row[col]
        
        return table_data
    
    def _has_header_row(self, table_data: List[List[str]]) -> bool:
        """
        Determine if the first row is a header.
        
        :param table_data: Table data
        :return: True if first row appears to be a header
        """
        if not table_data or len(table_data) < 2:
            return False
        
        first_row = table_data[0]
        second_row = table_data[1]
        
        # Check if first row contains typical header words
        header_words = ['name', 'title', 'description', 'column', 'header', 'field', 'property', 'attribute']
        first_row_text = ' '.join(cell.lower() for cell in first_row)
        
        if any(word in first_row_text for word in header_words):
            return True
        
        # Simple heuristic: if first row has more text content than second row
        first_text = sum(len(cell.strip()) for cell in first_row)
        second_text = sum(len(cell.strip()) for cell in second_row)
        
        return first_text > second_text
    
    def _convert_table_to_markdown(self, table_info: TableInfo) -> str:
        """
        Convert table to markdown format.
        
        :param table_info: Table information
        :return: Markdown table string
        """
        if table_info.format == 'markdown':
            # Already in markdown format, just clean up
            return self._clean_markdown_table(table_info.content)
        
        # Parse table data
        lines = table_info.content.split('\n')
        table_data = self._parse_table_lines(lines, table_info.format)
        
        if not table_data:
            return table_info.content  # Return original if parsing fails
        
        # Convert to markdown
        markdown_lines = []
        
        for i, row in enumerate(table_data):
            # Escape pipes in cell content
            if self.default_config["escape_pipes"]:
                cells = [cell.replace('|', '\\|') for cell in row]
            else:
                cells = row
            
            # Create markdown row
            markdown_row = "| " + " | ".join(cells) + " |"
            markdown_lines.append(markdown_row)
            
            # Add separator row after header
            if i == 0 and table_info.has_header:
                separator = "| " + " | ".join(["---"] * len(cells)) + " |"
                markdown_lines.append(separator)
        
        return '\n'.join(markdown_lines)
    
    def _clean_markdown_table(self, content: str) -> str:
        """
        Clean up an existing markdown table.
        
        :param content: Markdown table content
        :return: Cleaned markdown table
        """
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Handle separator lines (dashes)
            if (line.startswith('|') and line.endswith('|') and 
                all(cell.strip() in ['', '-', '--', '---', '--------', '------------'] for cell in line.strip('|').split('|')) and
                not any('|' in cell for cell in line.strip('|').split('|'))):
                # This is a separator line, keep it as is
                cleaned_lines.append(line)
                continue
            
            # Ensure proper pipe formatting
            if line.startswith('|') and line.endswith('|'):
                # Clean up spacing around pipes and escape pipes in content
                cells = [cell.strip() for cell in line.strip('|').split('|')]
                if self.default_config["escape_pipes"]:
                    cells = [cell.replace('|', '\\|') for cell in cells]
                cleaned_line = "| " + " | ".join(cells) + " |"
                cleaned_lines.append(cleaned_line)
            elif '|' in line:
                # Add missing pipes
                if not line.startswith('|'):
                    line = '| ' + line
                if not line.endswith('|'):
                    line = line + ' |'
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def get_processor_info(self) -> Dict[str, Any]:
        """
        Get information about this processor.
        
        :return: Dictionary with processor information
        """
        return {
            "name": "TableProcessor",
            "description": "Specialized processor for table structures",
            "config": self.default_config
        } 