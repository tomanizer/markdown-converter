"""
Batch Processor

This module provides parallel processing capabilities for large-scale
document conversion with worker pools, memory management, and progress tracking.
"""

import logging
import multiprocessing as mp
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Callable, Tuple
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import psutil
import threading
from queue import Queue, Empty
import signal
import sys

from .exceptions import BatchProcessingError, MemoryError
from .filesystem import FilesystemManager
from .engine import ConversionEngine


@dataclass
class ProcessingStats:
    """Statistics for batch processing."""
    total_files: int
    processed_files: int
    failed_files: int
    skipped_files: int
    start_time: float
    end_time: Optional[float] = None
    memory_usage_mb: Optional[float] = None
    cpu_usage_percent: Optional[float] = None


@dataclass
class ProcessingResult:
    """Result of processing a single file."""
    file_path: Path
    success: bool
    output_path: Optional[Path] = None
    error_message: Optional[str] = None
    processing_time: float = 0.0
    file_size_mb: float = 0.0


class BatchProcessor:
    """
    Parallel batch processor for document conversion.
    
    Handles large-scale processing with worker pools, memory management,
    progress tracking, and error isolation.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the batch processor.
        
        :param config: Configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger("BatchProcessor")
        self._setup_default_config()
        self._setup_components()
    
    def _setup_default_config(self) -> None:
        """Setup default configuration for batch processing."""
        self.default_config = {
            # Worker pool settings
            "max_workers": min(mp.cpu_count(), 8),  # Cap at 8 workers
            "worker_timeout": 300,  # 5 minutes per file
            "chunk_size": 10,  # Files per worker batch
            
            # Memory management
            "max_memory_mb": 2048,  # 2GB memory limit
            "memory_check_interval": 5,  # Check memory every 5 seconds
            "memory_threshold": 0.8,  # 80% memory usage threshold
            
            # Progress tracking
            "progress_update_interval": 1,  # Update progress every second
            "show_progress_bar": True,
            "log_progress": True,
            
            # Error handling
            "continue_on_error": True,
            "max_retries": 3,
            "retry_delay": 1,  # seconds
            
            # File processing
            "batch_size": 100,  # Process files in batches
            "file_size_limit_mb": 70,  # Skip files larger than 70MB
            "supported_extensions": [
                '.docx', '.doc', '.pdf', '.xlsx', '.xls', '.xlsb',
                '.html', '.htm', '.txt', '.rtf', '.odt', '.ods', '.odp'
            ],
            
            # Output settings
            "preserve_directory_structure": True,
            "overwrite_existing": False,
            "create_backups": False,
        }
        
        # Merge with user config
        if self.config:
            self.default_config.update(self.config)
    
    def _setup_components(self) -> None:
        """Setup processing components."""
        self.filesystem_manager = FilesystemManager(self.default_config)
        self.conversion_engine = ConversionEngine(self.default_config)
        
        # Initialize progress tracking
        self._progress_queue = Queue()
        self._stats = ProcessingStats(
            total_files=0,
            processed_files=0,
            failed_files=0,
            skipped_files=0,
            start_time=time.time()
        )
        
        # Initialize shutdown flag
        self._shutdown_requested = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum: int, frame: Any) -> None:
        """Handle shutdown signals gracefully."""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self._shutdown_requested = True
    
    def process_directory(self, input_dir: Union[str, Path], output_dir: Optional[Union[str, Path]] = None) -> ProcessingStats:
        """
        Process all files in a directory in parallel.
        
        :param input_dir: Input directory path
        :param output_dir: Output directory path (optional)
        :return: Processing statistics
        """
        input_path = Path(input_dir)
        if not input_path.exists():
            raise BatchProcessingError(f"Input directory does not exist: {input_path}")
        
        if output_dir is None:
            output_dir = input_path.parent / f"{input_path.name}_converted"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Store input directory for path preservation
        self._input_directory = input_path
        
        # Find all files to process
        files_to_process = self._discover_files(input_path)
        self._stats.total_files = len(files_to_process)
        
        if not files_to_process:
            self.logger.warning(f"No files found to process in {input_path}")
            return self._stats
        
        self.logger.info(f"Found {len(files_to_process)} files to process")
        
        # Process files in parallel
        results = self._process_files_parallel(files_to_process, output_path)
        
        # Update statistics
        self._update_stats(results)
        
        return self._stats
    
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
                if file_path.is_file() and self._should_process_file(file_path):
                    files.append(file_path)
        
        return sorted(files)
    
    def _should_process_file(self, file_path: Path) -> bool:
        """
        Check if a file should be processed.
        
        :param file_path: File path to check
        :return: True if file should be processed
        """
        # Check file extension
        if file_path.suffix.lower() not in self.default_config["supported_extensions"]:
            return False
        
        # Check file size
        try:
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            if file_size_mb > self.default_config["file_size_limit_mb"]:
                self.logger.warning(f"Skipping large file: {file_path} ({file_size_mb:.1f}MB)")
                return False
        except OSError:
            self.logger.warning(f"Cannot access file: {file_path}")
            return False
        
        return True
    
    def _process_files_parallel(self, files: List[Path], output_dir: Path) -> List[ProcessingResult]:
        """
        Process files in parallel using worker processes.
        
        :param files: List of files to process
        :param output_dir: Output directory
        :return: List of processing results
        """
        results = []
        
        # Create batches
        batches = self._create_batches(files)
        
        # Use ProcessPoolExecutor for parallel processing
        max_workers = min(self.default_config["max_workers"], len(batches))
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit batch processing jobs
            future_to_batch = {
                executor.submit(self._process_batch_worker, batch, str(output_dir)): batch
                for batch in batches
            }
            
            # Collect results
            for future in as_completed(future_to_batch):
                if self._shutdown_requested:
                    self.logger.info("Shutdown requested, stopping processing")
                    break
                
                try:
                    batch_results = future.result()
                    results.extend(batch_results)
                    
                    # Update progress
                    self._update_progress(len(batch_results))
                    
                except Exception as e:
                    self.logger.error(f"Batch processing failed: {e}")
                    # Add failed results for the batch
                    batch = future_to_batch[future]
                    for file_path in batch:
                        results.append(ProcessingResult(
                            file_path=file_path,
                            success=False,
                            error_message=str(e)
                        ))
        
        return results
    
    @staticmethod
    def _process_batch_worker(batch: List[Path], output_dir_str: str) -> List[ProcessingResult]:
        """
        Process a batch of files (runs in worker process).
        
        :param batch: List of files to process
        :param output_dir_str: Output directory as string
        :return: List of processing results
        """
        # Create a fresh conversion engine in this process to avoid pickle issues
        from .engine import ConversionEngine
        conversion_engine = ConversionEngine()
        
        results = []
        output_dir = Path(output_dir_str)
        
        for file_path in batch:
            start_time = time.time()
            
            try:
                # Process the file
                output_path = BatchProcessor._get_output_path_worker(file_path, output_dir)
                conversion_engine.convert_document(str(file_path), str(output_path))
                
                # Calculate processing time and file size
                processing_time = time.time() - start_time
                file_size_mb = file_path.stat().st_size / (1024 * 1024)
                
                results.append(ProcessingResult(
                    file_path=file_path,
                    success=True,
                    output_path=output_path,
                    processing_time=processing_time,
                    file_size_mb=file_size_mb
                ))
                
            except Exception as e:
                processing_time = time.time() - start_time
                results.append(ProcessingResult(
                    file_path=file_path,
                    success=False,
                    error_message=str(e),
                    processing_time=processing_time
                ))
        
        return results
    
    @staticmethod
    def _get_output_path_worker(input_file: Path, output_dir: Path) -> Path:
        """
        Generate output path for a file (worker version).
        
        :param input_file: Input file path
        :param output_dir: Output directory
        :return: Output file path
        """
        # Simple output path generation for worker processes
        output_filename = input_file.stem + '.md'
        return output_dir / output_filename
    
    def _create_batches(self, files: List[Path]) -> List[List[Path]]:
        """
        Create batches of files for processing.
        
        :param files: List of files
        :return: List of file batches
        """
        batch_size = self.default_config["batch_size"]
        return [files[i:i + batch_size] for i in range(0, len(files), batch_size)]
    
    def _check_memory_usage(self) -> bool:
        """
        Check if memory usage is within limits.
        
        :return: True if memory usage is too high
        """
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / (1024 * 1024)
            
            return memory_mb > self.default_config["max_memory_mb"]
        except Exception as e:
            self.logger.warning(f"Could not check memory usage: {e}")
            return False
    
    def _update_progress(self, processed_count: int) -> None:
        """
        Update progress tracking.
        
        :param processed_count: Number of files processed in this batch
        """
        self._stats.processed_files += processed_count
        
        if self.default_config["log_progress"]:
            progress = (self._stats.processed_files / self._stats.total_files) * 100
            self.logger.info(f"Progress: {progress:.1f}% ({self._stats.processed_files}/{self._stats.total_files})")
    
    def _update_stats(self, results: List[ProcessingResult]) -> None:
        """
        Update processing statistics.
        
        :param results: List of processing results
        """
        self._stats.end_time = time.time()
        
        for result in results:
            if result.success:
                self._stats.processed_files += 1
            else:
                self._stats.failed_files += 1
        
        # Calculate memory and CPU usage
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            self._stats.memory_usage_mb = memory_info.rss / (1024 * 1024)
            self._stats.cpu_usage_percent = process.cpu_percent()
        except Exception as e:
            self.logger.warning(f"Could not get system stats: {e}")
    
    def get_processing_stats(self) -> ProcessingStats:
        """
        Get current processing statistics.
        
        :return: Processing statistics
        """
        return self._stats
    
    def get_processor_info(self) -> Dict[str, Any]:
        """
        Get information about this processor.
        
        :return: Dictionary with processor information
        """
        return {
            "name": "BatchProcessor",
            "description": "Parallel batch processor for large-scale document conversion",
            "max_workers": self.default_config["max_workers"],
            "supported_extensions": self.default_config["supported_extensions"],
            "config": self.default_config
        } 