"""
Python API for Markdown Converter

This module provides a high-level Python API for the markdown converter,
making it easy to integrate into other Python applications.
"""

import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Union, Tuple
from dataclasses import dataclass

from .core.engine import ConversionEngine
from .core.batch_processor import BatchProcessor, ProcessingStats
from .core.grid_processor import GridProcessor, JobInfo
from .core.filesystem import FilesystemManager
from .core.exceptions import (
    ConversionError, 
    BatchProcessingError, 
    GridProcessingError,
    DependencyError
)


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
class BatchResult:
    """Result of batch processing."""
    stats: ProcessingStats
    results: List[ConversionResult]
    config: Dict[str, Any]


@dataclass
class GridResult:
    """Result of grid processing."""
    job_info: JobInfo
    results: List[ConversionResult]
    cluster_info: Optional[Any] = None


class MarkdownConverter:
    """
    High-level API for markdown conversion.
    
    Provides simple methods for converting files and directories
    with comprehensive error handling and progress tracking.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the markdown converter.
        
        :param config: Configuration dictionary
        """
        self.config = config or {}
        self.engine = ConversionEngine()
        self.logger = logging.getLogger("MarkdownConverter")
    
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
        Convert a single file to markdown.
        
        :param input_file: Path to input file
        :param output_file: Path to output file (auto-generated if not provided)
        :param output_format: Output format (markdown, html, pdf)
        :param preserve_structure: Preserve document structure
        :param extract_images: Extract and save images separately
        :param include_metadata: Include document metadata
        :return: Conversion result
        """
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file does not exist: {input_file}")
        
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
            if not self.validate_file(input_path):
                return ConversionResult(
                    input_file=input_path,
                    output_file=output_path,
                    success=False,
                    error_message=f"Unsupported file format: {input_path.suffix}",
                    file_size_mb=input_path.stat().st_size / (1024 * 1024)
                )
            
            result = self.engine.convert_document(
                str(input_path),
                str(output_path),
                output_format=output_format
            )
            
            # Verify the conversion actually produced content
            # Note: pypandoc returns empty string when writing to file, but file is created
            if output_path and output_path.exists():
                # File was created, check if it has content
                if output_path.stat().st_size == 0:
                    return ConversionResult(
                        input_file=input_path,
                        output_file=output_path,
                        success=False,
                        error_message="Conversion produced empty file",
                        file_size_mb=input_path.stat().st_size / (1024 * 1024)
                    )
            elif not result or len(result.strip()) == 0:
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
            self.logger.error(f"Conversion failed: {e}")
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
        batch_size: int = 100,
        max_memory_mb: int = 2048,
        file_size_limit_mb: int = 70,
        continue_on_error: bool = True,
        show_progress: bool = True
    ) -> BatchResult:
        """
        Convert all supported files in a directory using parallel processing.
        
        :param input_dir: Input directory path
        :param output_dir: Output directory path (auto-generated if not provided)
        :param max_workers: Number of worker processes
        :param batch_size: Number of files per batch
        :param max_memory_mb: Maximum memory per worker in MB
        :param file_size_limit_mb: Skip files larger than this size
        :param continue_on_error: Continue processing if some files fail
        :param show_progress: Show progress bar
        :return: Batch processing result
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir) if output_dir else input_path.parent / f"{input_path.name}_converted"
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input directory does not exist: {input_dir}")
        
        # Setup batch processor configuration
        config = self.config.copy()
        if max_workers:
            config['max_workers'] = min(max_workers, 8)
        config.update({
            'batch_size': batch_size,
            'max_memory_mb': max_memory_mb,
            'file_size_limit_mb': file_size_limit_mb,
            'continue_on_error': continue_on_error,
            'show_progress_bar': show_progress,
        })
        
        try:
            self.logger.info(f"Starting batch conversion: {input_path} -> {output_path}")
            
            processor = BatchProcessor(config)
            stats = processor.process_directory(input_path, output_path)
            
            # Convert results to our format
            results = []
            # TODO: Convert BatchProcessor results to ConversionResult format
            
            return BatchResult(
                stats=stats,
                results=results,
                config=config
            )
            
        except BatchProcessingError as e:
            self.logger.error(f"Batch processing failed: {e}")
            raise
    
    def convert_with_grid(
        self,
        input_dir: Union[str, Path],
        output_dir: Optional[Union[str, Path]] = None,
        cluster_type: str = 'local',
        scheduler_address: Optional[str] = None,
        n_workers: int = 4,
        memory_limit: str = '2GB',
        job_timeout: int = 3600
    ) -> GridResult:
        """
        Convert files using distributed grid processing with Dask.
        
        :param input_dir: Input directory path
        :param output_dir: Output directory path (auto-generated if not provided)
        :param cluster_type: Type of Dask cluster ('local' or 'remote')
        :param scheduler_address: Remote scheduler address
        :param n_workers: Number of worker processes
        :param memory_limit: Memory limit per worker
        :param job_timeout: Job timeout in seconds
        :return: Grid processing result
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir) if output_dir else input_path.parent / f"{input_path.name}_converted"
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input directory does not exist: {input_dir}")
        
        # Check if Dask is available
        try:
            import dask
            import dask.distributed
        except ImportError:
            raise DependencyError("Dask is required for grid processing. Install with: pip install dask[distributed]")
        
        # Setup grid processor configuration
        config = self.config.copy()
        config.update({
            'cluster_type': cluster_type,
            'scheduler_address': scheduler_address,
            'n_workers': n_workers,
            'memory_limit_per_worker': memory_limit,
            'job_timeout': job_timeout,
        })
        
        try:
            self.logger.info(f"Starting grid conversion: {input_path} -> {output_path}")
            
            processor = GridProcessor(config)
            
            # Start cluster
            cluster_info = processor.start_cluster()
            
            try:
                # Submit job
                job_info = processor.submit_job(input_path, output_path)
                
                # Wait for completion
                while True:
                    status = processor.get_job_status(job_info.job_id)
                    if status and status.status in ['completed', 'failed', 'cancelled']:
                        break
                    
                    import time
                    time.sleep(5)
                
                # Get final status
                final_status = processor.get_job_status(job_info.job_id)
                
                # Convert results to our format
                results = []
                # TODO: Convert GridProcessor results to ConversionResult format
                
                return GridResult(
                    job_info=final_status or job_info,
                    results=results,
                    cluster_info=cluster_info
                )
                
            finally:
                # Stop cluster
                processor.stop_cluster()
                
        except GridProcessingError as e:
            self.logger.error(f"Grid processing failed: {e}")
            raise
    
    def get_supported_formats(self) -> Dict[str, List[str]]:
        """
        Get list of supported input and output formats.
        
        :return: Dictionary with 'input' and 'output' format lists
        """
        return {
            'input': [
                '.docx', '.doc', '.pdf', '.xlsx', '.xls', '.xlsb',
                '.html', '.htm', '.txt', '.rtf', '.odt', '.ods', '.odp',
                '.msg', '.eml', '.pptx', '.ppt'
            ],
            'output': ['markdown', 'html', 'pdf', 'txt']
        }
    
    def validate_file(self, file_path: Union[str, Path]) -> bool:
        """
        Check if a file is supported for conversion.
        
        :param file_path: Path to the file
        :return: True if file is supported
        """
        path = Path(file_path)
        supported_formats = self.get_supported_formats()['input']
        return path.suffix.lower() in supported_formats
    
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
            'is_supported': self.validate_file(path),
            'modified_time': stat.st_mtime,
        }


# Convenience functions for simple use cases
def convert_file(
    input_file: Union[str, Path],
    output_file: Optional[Union[str, Path]] = None,
    **kwargs
) -> ConversionResult:
    """
    Convert a single file to markdown.
    
    :param input_file: Path to input file
    :param output_file: Path to output file (auto-generated if not provided)
    :param kwargs: Additional conversion options
    :return: Conversion result
    """
    converter = MarkdownConverter()
    return converter.convert_file(input_file, output_file, **kwargs)


def convert_directory(
    input_dir: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    **kwargs
) -> BatchResult:
    """
    Convert all supported files in a directory.
    
    :param input_dir: Input directory path
    :param output_dir: Output directory path (auto-generated if not provided)
    :param kwargs: Additional batch processing options
    :return: Batch processing result
    """
    converter = MarkdownConverter()
    return converter.convert_directory(input_dir, output_dir, **kwargs)


def convert_with_grid(
    input_dir: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    **kwargs
) -> GridResult:
    """
    Convert files using distributed grid processing.
    
    :param input_dir: Input directory path
    :param output_dir: Output directory path (auto-generated if not provided)
    :param kwargs: Additional grid processing options
    :return: Grid processing result
    """
    converter = MarkdownConverter()
    return converter.convert_with_grid(input_dir, output_dir, **kwargs) 