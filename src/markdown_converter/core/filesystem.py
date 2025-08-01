"""
Filesystem Integration Module

This module provides robust filesystem operations using fsspec and pathlib
for handling files across local, remote, and cloud storage systems.
"""

import os
import glob
from pathlib import Path
from typing import List, Union, Optional, Dict, Any, Iterator
import logging

import fsspec
from fsspec import AbstractFileSystem

from .exceptions import FilesystemError
from .utils import ensure_directory_exists, get_file_info, is_large_file


class FilesystemManager:
    """
    Manages filesystem operations across different storage systems.
    
    This class provides a unified interface for file operations using
    fsspec for various storage backends and pathlib for path handling.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the filesystem manager.
        
        :param config: Configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger("FilesystemManager")
        self._setup_default_config()
    
    def _setup_default_config(self) -> None:
        """Setup default configuration for filesystem operations."""
        self.default_config = {
            # File discovery
            "recursive_search": True,
            "follow_symlinks": False,
            "include_hidden": False,
            # File filtering
            "max_file_size_mb": 100.0,
            "supported_extensions": [
                '.docx', '.doc', '.pdf', '.html', '.htm', '.xlsx', '.xls',
                '.odt', '.rtf', '.epub', '.txt', '.md', '.msg', '.eml'
            ],
            # Batch processing
            "batch_size": 100,
            "max_concurrent_files": 10,
        }
        
        # Merge with user config
        self.default_config.update(self.config)
    
    def get_filesystem(self, path: Union[str, Path]) -> AbstractFileSystem:
        """
        Get the appropriate filesystem for a path.
        
        :param path: Path to determine filesystem for
        :return: Filesystem instance
        """
        path_str = str(path)
        
        # Check for remote storage protocols
        if path_str.startswith(('s3://', 'gs://', 'azure://', 'http://', 'https://')):
            return fsspec.filesystem(path_str.split('://')[0])
        else:
            return fsspec.filesystem('file')
    
    def find_files(self, search_path: Union[str, Path], 
                   pattern: Optional[str] = None,
                   recursive: Optional[bool] = None) -> List[Path]:
        """
        Find files matching criteria.
        
        :param search_path: Path to search in
        :param pattern: File pattern to match (e.g., '*.docx')
        :param recursive: Whether to search recursively
        :return: List of matching file paths
        """
        search_path = Path(search_path)
        recursive = recursive if recursive is not None else self.default_config["recursive_search"]
        
        if not search_path.exists():
            raise FilesystemError(f"Search path does not exist: {search_path}")
        
        if pattern:
            # Use glob pattern
            if recursive:
                files = list(search_path.rglob(pattern))
            else:
                files = list(search_path.glob(pattern))
        else:
            # Use supported extensions
            files = []
            if recursive:
                for ext in self.default_config["supported_extensions"]:
                    files.extend(search_path.rglob(f"*{ext}"))
            else:
                for ext in self.default_config["supported_extensions"]:
                    files.extend(search_path.glob(f"*{ext}"))
        
        # Filter files
        filtered_files = []
        for file_path in files:
            if self._should_include_file(file_path):
                filtered_files.append(file_path)
        
        self.logger.info(f"Found {len(filtered_files)} files in {search_path}")
        return filtered_files
    
    def _should_include_file(self, file_path: Path) -> bool:
        """
        Check if a file should be included in processing.
        
        :param file_path: Path to the file
        :return: True if file should be included
        """
        # Check if file is hidden
        if not self.default_config["include_hidden"]:
            if any(part.startswith('.') for part in file_path.parts):
                return False
        
        # Check file size
        if is_large_file(file_path, self.default_config["max_file_size_mb"]):
            self.logger.warning(f"Skipping large file: {file_path}")
            return False
        
        # Check if file is readable
        if not os.access(file_path, os.R_OK):
            self.logger.warning(f"Skipping unreadable file: {file_path}")
            return False
        
        return True
    
    def get_file_batches(self, file_paths: List[Path], 
                        batch_size: Optional[int] = None) -> Iterator[List[Path]]:
        """
        Split files into batches for processing.
        
        :param file_paths: List of file paths
        :param batch_size: Size of each batch
        :return: Iterator of file batches
        """
        batch_size = batch_size or self.default_config["batch_size"]
        
        for i in range(0, len(file_paths), batch_size):
            yield file_paths[i:i + batch_size]
    
    def create_output_directory(self, output_path: Union[str, Path]) -> Path:
        """
        Create output directory safely.
        
        :param output_path: Path to output directory
        :return: Path to created directory
        """
        output_path = Path(output_path)
        
        try:
            ensure_directory_exists(output_path)
            self.logger.info(f"Created output directory: {output_path}")
            return output_path
        except Exception as e:
            raise FilesystemError(f"Cannot create output directory {output_path}: {e}")
    
    def get_output_path(self, input_path: Path, output_dir: Path, 
                       output_format: str = 'md') -> Path:
        """
        Generate output path for a converted file.
        
        :param input_path: Path to input file
        :param output_dir: Output directory
        :param output_format: Output format extension
        :return: Output file path
        """
        from .utils import get_safe_output_path
        
        return get_safe_output_path(input_path, output_dir, output_format)
    
    def copy_file(self, source_path: Union[str, Path], 
                  dest_path: Union[str, Path]) -> None:
        """
        Copy a file safely.
        
        :param source_path: Source file path
        :param dest_path: Destination file path
        """
        source_path = Path(source_path)
        dest_path = Path(dest_path)
        
        # Ensure destination directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Use fsspec for cross-platform compatibility
            fs_source = self.get_filesystem(source_path)
            fs_dest = self.get_filesystem(dest_path)
            
            with fs_source.open(str(source_path), 'rb') as src:
                with fs_dest.open(str(dest_path), 'wb') as dst:
                    dst.write(src.read())
                    
            self.logger.debug(f"Copied {source_path} to {dest_path}")
            
        except Exception as e:
            raise FilesystemError(f"Failed to copy {source_path} to {dest_path}: {e}")
    
    def move_file(self, source_path: Union[str, Path], 
                  dest_path: Union[str, Path]) -> None:
        """
        Move a file safely.
        
        :param source_path: Source file path
        :param dest_path: Destination file path
        """
        source_path = Path(source_path)
        dest_path = Path(dest_path)
        
        # Ensure destination directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            source_path.rename(dest_path)
            self.logger.debug(f"Moved {source_path} to {dest_path}")
            
        except Exception as e:
            raise FilesystemError(f"Failed to move {source_path} to {dest_path}: {e}")
    
    def delete_file(self, file_path: Union[str, Path]) -> None:
        """
        Delete a file safely.
        
        :param file_path: Path to file to delete
        """
        file_path = Path(file_path)
        
        try:
            if file_path.exists():
                file_path.unlink()
                self.logger.debug(f"Deleted {file_path}")
            
        except Exception as e:
            raise FilesystemError(f"Failed to delete {file_path}: {e}")
    
    def get_directory_size(self, directory_path: Union[str, Path]) -> int:
        """
        Calculate total size of a directory.
        
        :param directory_path: Path to directory
        :return: Total size in bytes
        """
        directory_path = Path(directory_path)
        total_size = 0
        
        try:
            for file_path in directory_path.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
                    
            return total_size
            
        except Exception as e:
            raise FilesystemError(f"Failed to calculate directory size for {directory_path}: {e}")
    
    def get_file_count(self, directory_path: Union[str, Path]) -> int:
        """
        Count files in a directory.
        
        :param directory_path: Path to directory
        :return: Number of files
        """
        directory_path = Path(directory_path)
        count = 0
        
        try:
            for file_path in directory_path.rglob('*'):
                if file_path.is_file():
                    count += 1
                    
            return count
            
        except Exception as e:
            raise FilesystemError(f"Failed to count files in {directory_path}: {e}")
    
    def list_directory_contents(self, directory_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get detailed information about directory contents.
        
        :param directory_path: Path to directory
        :return: Dictionary with directory information
        """
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            raise FilesystemError(f"Directory does not exist: {directory_path}")
        
        if not directory_path.is_dir():
            raise FilesystemError(f"Path is not a directory: {directory_path}")
        
        files = []
        directories = []
        total_size = 0
        
        try:
            for item in directory_path.iterdir():
                if item.is_file():
                    file_info = get_file_info(item)
                    files.append(file_info)
                    total_size += file_info['size']
                elif item.is_dir():
                    directories.append({
                        'name': item.name,
                        'path': str(item),
                        'file_count': self.get_file_count(item)
                    })
            
            return {
                'directory': str(directory_path),
                'files': files,
                'directories': directories,
                'total_files': len(files),
                'total_directories': len(directories),
                'total_size': total_size,
                'supported_files': [f for f in files if f['suffix'] in self.default_config["supported_extensions"]]
            }
            
        except Exception as e:
            raise FilesystemError(f"Failed to list directory contents for {directory_path}: {e}")
    
    def validate_storage_space(self, directory_path: Union[str, Path], 
                             required_size_mb: float) -> bool:
        """
        Check if there's enough storage space.
        
        :param directory_path: Path to check
        :param required_size_mb: Required space in MB
        :return: True if enough space is available
        """
        directory_path = Path(directory_path)
        
        try:
            # Get available space
            stat = os.statvfs(directory_path)
            available_bytes = stat.f_frsize * stat.f_bavail
            available_mb = available_bytes / (1024 * 1024)
            
            return available_mb >= required_size_mb
            
        except Exception as e:
            self.logger.warning(f"Could not check storage space: {e}")
            return True  # Assume enough space if we can't check 