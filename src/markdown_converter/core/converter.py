"""
Main Document Converter

This module provides the main conversion pipeline that uses a plugin-based
architecture with parsers registered in the ParserRegistry. It tries Pandoc
first, then falls back to custom parsers.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import tempfile
from dataclasses import dataclass
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from .exceptions import ConversionError, UnsupportedFormatError
from ..parsers.base import parser_registry, ParserResult


@dataclass
class ConversionResult:
    """Result of a single file conversion."""
    input_file: Path
    output_file: Path
    success: bool
    error_message: Optional[str] = None
    processing_time: float = 0.0
    file_size_mb: float = 0.0


@dataclass
class DirectoryConversionResult:
    """Result of directory conversion."""
    total_files: int
    processed_files: int
    failed_files: int
    skipped_files: int
    results: List[ConversionResult]
    start_time: float
    end_time: float
    processing_time: float = 0.0


class MainConverter:
    """
    Main document converter that uses a plugin-based architecture.
    
    This class provides a unified interface for converting documents to markdown,
    using Pandoc for supported formats and falling back to custom parsers
    registered in the ParserRegistry.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the main converter.
        
        :param config: Configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger("MainConverter")
        
        # Register all available parsers
        self._register_parsers()
    
    def _register_parsers(self) -> None:
        """Register all available parsers with the registry."""
        from ..parsers.pdf_parser import PDFParser
        from ..parsers.excel_parser import ExcelParser
        from ..parsers.word_parser import WordParser
        from ..parsers.html_parser import HTMLParser
        from ..parsers.pandoc_parser import PandocParser
        
        # Create and register parsers
        parsers = [
            PDFParser(self.config),
            ExcelParser(self.config),
            WordParser(self.config),
            HTMLParser(self.config),
            PandocParser(self.config),
        ]
        
        for parser in parsers:
            parser_registry.register_parser(parser)
            self.logger.info(f"Registered parser: {parser.__class__.__name__}")
    
    def can_convert(self, file_path: Union[str, Path]) -> bool:
        """
        Check if the converter can handle the given file.
        
        :param file_path: Path to the file
        :return: True if the file can be converted
        """
        file_path = Path(file_path)
        
        # Check if we have a parser for this format
        return parser_registry.get_parser_for_file(file_path) is not None
    
    def convert_file(
        self,
        input_file: Union[str, Path],
        output_file: Optional[Union[str, Path]] = None,
        output_format: str = 'markdown',
        preserve_structure: bool = True,
        extract_images: bool = True,
        include_metadata: bool = True
    ) -> ConversionResult:
        """
        Convert a single file to markdown with comprehensive error handling.
        
        :param input_file: Path to input file
        :param output_file: Path to output file (auto-generated if not provided)
        :param output_format: Output format (markdown, html, pdf)
        :param preserve_structure: Preserve document structure
        :param extract_images: Extract and save images separately
        :param include_metadata: Include document metadata
        :return: Conversion result with success status and error details
        """
        input_path = Path(input_file)
        
        if not input_path.exists():
            return ConversionResult(
                input_file=input_path,
                output_file=Path(output_file) if output_file else input_path.with_suffix(f'.{output_format}'),
                success=False,
                error_message=f"Input file does not exist: {input_file}",
                file_size_mb=0.0
            )
        
        # Generate output path if not provided
        if output_file is None:
            output_path = input_path.with_suffix(f'.{output_format}')
        else:
            output_path = Path(output_file)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            self.logger.info(f"Converting {input_path} to {output_path}")
            
            # Check if format is supported before attempting conversion
            if not self.can_convert(input_path):
                return ConversionResult(
                    input_file=input_path,
                    output_file=output_path,
                    success=False,
                    error_message=f"Unsupported file format: {input_path.suffix}",
                    file_size_mb=input_path.stat().st_size / (1024 * 1024)
                )
            
            # Find appropriate parser from registry
            parser = parser_registry.get_parser_for_file(input_path)
            
            if not parser:
                return ConversionResult(
                    input_file=input_path,
                    output_file=output_path,
                    success=False,
                    error_message=f"No parser found for {input_path}",
                    file_size_mb=input_path.stat().st_size / (1024 * 1024)
                )
            
            self.logger.info(f"Using parser {parser.__class__.__name__} for {input_path}")
            
            # Parse the document
            result = parser.parse(input_path)
            
            # Convert to the target format
            if output_format == 'markdown':
                content = result.content
            else:
                # For other formats, we might need additional conversion
                # For now, we'll just return the content as-is
                content = result.content
            
            # Write to output file
            output_path.write_text(content, encoding='utf-8')
            
            # Verify the conversion actually produced content
            if output_path.exists():
                # File was created, check if it has content
                if output_path.stat().st_size == 0:
                    return ConversionResult(
                        input_file=input_path,
                        output_file=output_path,
                        success=False,
                        error_message="Conversion produced empty file",
                        file_size_mb=input_path.stat().st_size / (1024 * 1024)
                    )
            elif not content or len(content.strip()) == 0:
                return ConversionResult(
                    input_file=input_path,
                    output_file=output_path,
                    success=False,
                    error_message="Conversion produced empty result",
                    file_size_mb=input_path.stat().st_size / (1024 * 1024)
                )
            
            return ConversionResult(
                input_file=input_path,
                output_file=output_path,
                success=True,
                processing_time=0.0,  # TODO: Add timing
                file_size_mb=input_path.stat().st_size / (1024 * 1024)
            )
                
        except Exception as e:
            self.logger.error(f"Conversion failed for {input_path}: {e}")
            return ConversionResult(
                input_file=input_path,
                output_file=output_path,
                success=False,
                error_message=str(e),
                file_size_mb=input_path.stat().st_size / (1024 * 1024)
            )
    
    def convert_directory(
        self,
        input_dir: Union[str, Path],
        output_dir: Optional[Union[str, Path]] = None,
        max_workers: Optional[int] = None,
        continue_on_error: bool = True
    ) -> DirectoryConversionResult:
        """
        Convert all supported files in a directory.
        
        :param input_dir: Input directory path
        :param output_dir: Output directory path (auto-generated if not provided)
        :param max_workers: Number of worker processes (default: CPU count)
        :param continue_on_error: Continue processing if some files fail
        :return: Directory conversion result with statistics
        """
        input_path = Path(input_dir)
        if not input_path.exists():
            raise ConversionError(f"Input directory does not exist: {input_dir}")
        
        if output_dir is None:
            output_path = input_path.parent / f"{input_path.name}_converted"
        else:
            output_path = Path(output_dir)
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find all files to process
        files_to_process = self._discover_files(input_path)
        total_files = len(files_to_process)
        
        if not files_to_process:
            self.logger.warning(f"No files found to process in {input_path}")
            return DirectoryConversionResult(
                total_files=0,
                processed_files=0,
                failed_files=0,
                skipped_files=0,
                results=[],
                start_time=time.time(),
                end_time=time.time()
            )
        
        self.logger.info(f"Found {total_files} files to process")
        
        start_time = time.time()
        results = []
        
        if max_workers and max_workers > 1:
            # Process files in parallel
            results = self._process_files_parallel(files_to_process, output_path, max_workers)
        else:
            # Process files sequentially
            results = self._process_files_sequential(files_to_process, output_path)
        
        end_time = time.time()
        
        # Calculate statistics
        processed_files = sum(1 for r in results if r.success)
        failed_files = sum(1 for r in results if not r.success)
        skipped_files = total_files - len(results)
        
        return DirectoryConversionResult(
            total_files=total_files,
            processed_files=processed_files,
            failed_files=failed_files,
            skipped_files=skipped_files,
            results=results,
            start_time=start_time,
            end_time=end_time,
            processing_time=end_time - start_time
        )
    
    def _discover_files(self, input_path: Path) -> List[Path]:
        """
        Discover files to process.
        
        :param input_path: Input path (file or directory)
        :return: List of files to process
        """
        files = []
        
        if input_path.is_file():
            files.append(input_path)
        elif input_path.is_dir():
            # Find all files recursively
            for file_path in input_path.rglob("*"):
                if file_path.is_file() and self.can_convert(file_path):
                    files.append(file_path)
        
        return sorted(files)
    
    def _process_files_sequential(self, files: List[Path], output_dir: Path) -> List[ConversionResult]:
        """
        Process files sequentially.
        
        :param files: List of files to process
        :param output_dir: Output directory
        :return: List of conversion results
        """
        results = []
        
        for file_path in files:
            output_file = output_dir / f"{file_path.stem}.md"
            result = self.convert_file(file_path, output_file)
            results.append(result)
            
            if result.success:
                self.logger.info(f"✅ Converted {file_path.name}")
            else:
                self.logger.warning(f"❌ Failed to convert {file_path.name}: {result.error_message}")
        
        return results
    
    def _process_files_parallel(self, files: List[Path], output_dir: Path, max_workers: int) -> List[ConversionResult]:
        """
        Process files in parallel.
        
        :param files: List of files to process
        :param output_dir: Output directory
        :param max_workers: Number of worker processes
        :return: List of conversion results
        """
        results = []
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit conversion jobs
            future_to_file = {
                executor.submit(self._convert_file_worker, file_path, str(output_dir)): file_path
                for file_path in files
            }
            
            # Collect results
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    if result.success:
                        self.logger.info(f"✅ Converted {file_path.name}")
                    else:
                        self.logger.warning(f"❌ Failed to convert {file_path.name}: {result.error_message}")
                        
                except Exception as e:
                    self.logger.error(f"❌ Error processing {file_path.name}: {e}")
                    results.append(ConversionResult(
                        input_file=file_path,
                        output_file=output_dir / f"{file_path.stem}.md",
                        success=False,
                        error_message=str(e),
                        file_size_mb=file_path.stat().st_size / (1024 * 1024)
                    ))
        
        return results
    
    @staticmethod
    def _convert_file_worker(input_file: Path, output_dir_str: str) -> ConversionResult:
        """
        Worker function for parallel file conversion.
        
        :param input_file: Input file path
        :param output_dir_str: Output directory as string
        :return: Conversion result
        """
        # Create a fresh converter in this process
        converter = MainConverter()
        output_dir = Path(output_dir_str)
        output_file = output_dir / f"{input_file.stem}.md"
        
        return converter.convert_file(input_file, output_file)
    
    def convert_document(self, input_path: Union[str, Path], 
                        output_path: Optional[Union[str, Path]] = None,
                        output_format: str = 'markdown') -> str:
        """
        Convert a document to the specified format (legacy method).
        
        :param input_path: Path to input document
        :param output_path: Path to output file (optional)
        :param output_format: Output format (default: markdown)
        :return: Converted content as string
        :raises: ConversionError if conversion fails
        """
        result = self.convert_file(input_path, output_path, output_format)
        
        if not result.success:
            raise ConversionError(result.error_message or "Conversion failed",
                               input_file=str(result.input_file),
                               output_file=str(result.output_file))
        
        # Read the content from the output file
        if result.output_file.exists():
            return result.output_file.read_text(encoding='utf-8')
        else:
            return ""
    
    def get_supported_formats(self) -> Dict[str, List[str]]:
        """
        Get supported input and output formats.
        
        :return: Dictionary with input and output format lists
        """
        # Get all parser formats
        input_formats = parser_registry.get_supported_formats()
        
        # Output formats (all parsers output markdown)
        output_formats = ['markdown', 'md']
        
        return {
            'input': input_formats,
            'output': output_formats
        }
    
    def validate_format_support(self, input_format: str, output_format: str) -> bool:
        """
        Validate that the specified formats are supported.
        
        :param input_format: Input format to check
        :param output_format: Output format to check
        :return: True if both formats are supported
        """
        formats = self.get_supported_formats()
        return (input_format in formats['input'] and 
                output_format in formats['output'])
    
    def get_conversion_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get information about a file for conversion.
        
        :param file_path: Path to the file
        :return: Dictionary with conversion information
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        # Find appropriate parser
        parser = parser_registry.get_parser_for_file(file_path)
        
        return {
            'file_path': str(file_path),
            'file_size': file_path.stat().st_size,
            'extension': extension,
            'parser_found': parser is not None,
            'parser_name': parser.__class__.__name__ if parser else None,
            'can_convert': parser is not None,
            'registered_parsers': parser_registry.list_parsers()
        }
    
    def get_file_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get information about a file.
        
        :param file_path: Path to the file
        :return: Dictionary with file information
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")
        
        stat = path.stat()
        
        return {
            'path': str(path),
            'name': path.name,
            'extension': path.suffix.lower(),
            'size_bytes': stat.st_size,
            'size_mb': stat.st_size / (1024 * 1024),
            'is_supported': self.can_convert(path),
            'modified_time': stat.st_mtime,
        } 