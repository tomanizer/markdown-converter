"""
Configuration Management

This module provides comprehensive configuration management for the markdown converter,
supporting YAML files, environment variables, and CLI arguments with validation.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
import logging

from .core.exceptions import ConfigurationError


@dataclass
class ConversionConfig:
    """Configuration for document conversion."""
    output_format: str = 'markdown'
    preserve_structure: bool = True
    extract_images: bool = True
    include_metadata: bool = True
    image_format: str = 'png'
    image_quality: int = 85
    max_image_size: int = 1024  # pixels


@dataclass
class BatchConfig:
    """Configuration for batch processing."""
    max_workers: int = 4
    batch_size: int = 100
    max_memory_mb: int = 2048
    file_size_limit_mb: int = 70
    continue_on_error: bool = True
    show_progress_bar: bool = True
    worker_timeout: int = 300
    chunk_size: int = 10
    memory_check_interval: int = 5
    memory_threshold: float = 0.8
    progress_update_interval: int = 1
    max_retries: int = 3
    retry_delay: int = 1


@dataclass
class GridConfig:
    """Configuration for grid processing."""
    cluster_type: str = 'local'
    scheduler_address: Optional[str] = None
    n_workers: int = 4
    n_threads_per_worker: int = 2
    memory_limit_per_worker: str = '2GB'
    dashboard_address: str = ':8787'
    job_timeout: int = 3600
    max_jobs: int = 10
    job_retries: int = 3
    monitor_resources: bool = True
    resource_check_interval: int = 30
    max_memory_usage: float = 0.8
    max_cpu_usage: float = 0.9
    chunk_size: int = 50
    max_file_size_mb: int = 50


@dataclass
class LoggingConfig:
    """Configuration for logging."""
    level: str = 'INFO'
    format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    file: Optional[str] = None
    console: bool = True
    structured: bool = False


@dataclass
class Config:
    """Main configuration class."""
    conversion: ConversionConfig = field(default_factory=ConversionConfig)
    batch: BatchConfig = field(default_factory=BatchConfig)
    grid: GridConfig = field(default_factory=GridConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    supported_extensions: List[str] = field(default_factory=lambda: [
        '.docx', '.doc', '.pdf', '.xlsx', '.xls', '.xlsb',
        '.html', '.htm', '.txt', '.rtf', '.odt', '.ods', '.odp',
        '.msg', '.eml', '.pptx', '.ppt'
    ])
    output_directory: Optional[str] = None
    temp_directory: Optional[str] = None
    cache_directory: Optional[str] = None


class ConfigManager:
    """
    Configuration manager for the markdown converter.
    
    Handles loading configuration from multiple sources with precedence:
    1. CLI arguments (highest priority)
    2. Environment variables
    3. Configuration file
    4. Default values (lowest priority)
    """
    
    def __init__(self, config_file: Optional[str] = None) -> None:
        """
        Initialize the configuration manager.
        
        :param config_file: Path to configuration file
        """
        self.config_file = config_file
        self.logger = logging.getLogger("ConfigManager")
        self._config = Config()
        self._load_configuration()
    
    def _load_configuration(self) -> None:
        """Load configuration from all sources."""
        # Load defaults first
        self._load_defaults()
        
        # Load from file
        if self.config_file:
            self._load_from_file()
        
        # Load from environment
        self._load_from_environment()
    
    def _load_defaults(self) -> None:
        """Load default configuration."""
        # Default configuration is already set in the dataclass
        pass
    
    def _load_from_file(self) -> None:
        """Load configuration from YAML file."""
        if not self.config_file or not Path(self.config_file).exists():
            return
        
        try:
            with open(self.config_file, 'r') as f:
                data = yaml.safe_load(f) or {}
            
            self._update_config_from_dict(data)
            self.logger.info(f"Loaded configuration from {self.config_file}")
            
        except Exception as e:
            self.logger.warning(f"Could not load configuration file {self.config_file}: {e}")
    
    def _load_from_environment(self) -> None:
        """Load configuration from environment variables."""
        env_mappings = {
            # Conversion settings
            'MDC_OUTPUT_FORMAT': ('conversion.output_format', str),
            'MDC_PRESERVE_STRUCTURE': ('conversion.preserve_structure', lambda x: x.lower() == 'true'),
            'MDC_EXTRACT_IMAGES': ('conversion.extract_images', lambda x: x.lower() == 'true'),
            'MDC_INCLUDE_METADATA': ('conversion.include_metadata', lambda x: x.lower() == 'true'),
            
            # Batch processing settings
            'MDC_MAX_WORKERS': ('batch.max_workers', int),
            'MDC_BATCH_SIZE': ('batch.batch_size', int),
            'MDC_MAX_MEMORY_MB': ('batch.max_memory_mb', int),
            'MDC_FILE_SIZE_LIMIT_MB': ('batch.file_size_limit_mb', int),
            'MDC_CONTINUE_ON_ERROR': ('batch.continue_on_error', lambda x: x.lower() == 'true'),
            
            # Grid processing settings
            'MDC_CLUSTER_TYPE': ('grid.cluster_type', str),
            'MDC_SCHEDULER_ADDRESS': ('grid.scheduler_address', str),
            'MDC_N_WORKERS': ('grid.n_workers', int),
            'MDC_MEMORY_LIMIT_PER_WORKER': ('grid.memory_limit_per_worker', str),
            
            # Logging settings
            'MDC_LOG_LEVEL': ('logging.level', str),
            'MDC_LOG_FILE': ('logging.file', str),
            'MDC_LOG_CONSOLE': ('logging.console', lambda x: x.lower() == 'true'),
            
            # General settings
            'MDC_OUTPUT_DIRECTORY': ('output_directory', str),
            'MDC_TEMP_DIRECTORY': ('temp_directory', str),
            'MDC_CACHE_DIRECTORY': ('cache_directory', str),
        }
        
        for env_var, (config_path, converter) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    converted_value = converter(value)
                    self._set_config_value(config_path, converted_value)
                except (ValueError, TypeError) as e:
                    self.logger.warning(f"Invalid value for {env_var}: {value} ({e})")
    
    def _update_config_from_dict(self, data: Dict[str, Any]) -> None:
        """Update configuration from dictionary."""
        for key, value in data.items():
            if key == 'conversion' and isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if hasattr(self._config.conversion, subkey):
                        setattr(self._config.conversion, subkey, subvalue)
            
            elif key == 'batch' and isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if hasattr(self._config.batch, subkey):
                        setattr(self._config.batch, subkey, subvalue)
            
            elif key == 'grid' and isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if hasattr(self._config.grid, subkey):
                        setattr(self._config.grid, subkey, subvalue)
            
            elif key == 'logging' and isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if hasattr(self._config.logging, subkey):
                        setattr(self._config.logging, subkey, subvalue)
            
            elif hasattr(self._config, key):
                setattr(self._config, key, value)
    
    def _set_config_value(self, path: str, value: Any) -> None:
        """Set a configuration value using dot notation."""
        parts = path.split('.')
        obj = self._config
        
        for part in parts[:-1]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                return
        
        if hasattr(obj, parts[-1]):
            setattr(obj, parts[-1], value)
    
    def get_config(self) -> Config:
        """Get the current configuration."""
        return self._config
    
    def get_conversion_config(self) -> ConversionConfig:
        """Get conversion configuration."""
        return self._config.conversion
    
    def get_batch_config(self) -> BatchConfig:
        """Get batch processing configuration."""
        return self._config.batch
    
    def get_grid_config(self) -> GridConfig:
        """Get grid processing configuration."""
        return self._config.grid
    
    def get_logging_config(self) -> LoggingConfig:
        """Get logging configuration."""
        return self._config.logging
    
    def get_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary."""
        return {
            'conversion': {
                'output_format': self._config.conversion.output_format,
                'preserve_structure': self._config.conversion.preserve_structure,
                'extract_images': self._config.conversion.extract_images,
                'include_metadata': self._config.conversion.include_metadata,
                'image_format': self._config.conversion.image_format,
                'image_quality': self._config.conversion.image_quality,
                'max_image_size': self._config.conversion.max_image_size,
            },
            'batch': {
                'max_workers': self._config.batch.max_workers,
                'batch_size': self._config.batch.batch_size,
                'max_memory_mb': self._config.batch.max_memory_mb,
                'file_size_limit_mb': self._config.batch.file_size_limit_mb,
                'continue_on_error': self._config.batch.continue_on_error,
                'show_progress_bar': self._config.batch.show_progress_bar,
                'worker_timeout': self._config.batch.worker_timeout,
                'chunk_size': self._config.batch.chunk_size,
                'memory_check_interval': self._config.batch.memory_check_interval,
                'memory_threshold': self._config.batch.memory_threshold,
                'progress_update_interval': self._config.batch.progress_update_interval,
                'max_retries': self._config.batch.max_retries,
                'retry_delay': self._config.batch.retry_delay,
            },
            'grid': {
                'cluster_type': self._config.grid.cluster_type,
                'scheduler_address': self._config.grid.scheduler_address,
                'n_workers': self._config.grid.n_workers,
                'n_threads_per_worker': self._config.grid.n_threads_per_worker,
                'memory_limit_per_worker': self._config.grid.memory_limit_per_worker,
                'dashboard_address': self._config.grid.dashboard_address,
                'job_timeout': self._config.grid.job_timeout,
                'max_jobs': self._config.grid.max_jobs,
                'job_retries': self._config.grid.job_retries,
                'monitor_resources': self._config.grid.monitor_resources,
                'resource_check_interval': self._config.grid.resource_check_interval,
                'max_memory_usage': self._config.grid.max_memory_usage,
                'max_cpu_usage': self._config.grid.max_cpu_usage,
                'chunk_size': self._config.grid.chunk_size,
                'max_file_size_mb': self._config.grid.max_file_size_mb,
            },
            'logging': {
                'level': self._config.logging.level,
                'format': self._config.logging.format,
                'file': self._config.logging.file,
                'console': self._config.logging.console,
                'structured': self._config.logging.structured,
            },
            'supported_extensions': self._config.supported_extensions,
            'output_directory': self._config.output_directory,
            'temp_directory': self._config.temp_directory,
            'cache_directory': self._config.cache_directory,
        }
    
    def validate(self) -> List[str]:
        """
        Validate the current configuration.
        
        :return: List of validation errors (empty if valid)
        """
        errors = []
        
        # Validate conversion config
        if self._config.conversion.output_format not in ['markdown', 'html', 'pdf', 'txt']:
            errors.append(f"Invalid output format: {self._config.conversion.output_format}")
        
        if self._config.conversion.image_quality < 1 or self._config.conversion.image_quality > 100:
            errors.append(f"Image quality must be between 1 and 100: {self._config.conversion.image_quality}")
        
        # Validate batch config
        if self._config.batch.max_workers < 1:
            errors.append(f"Max workers must be at least 1: {self._config.batch.max_workers}")
        
        if self._config.batch.max_memory_mb < 100:
            errors.append(f"Max memory must be at least 100MB: {self._config.batch.max_memory_mb}")
        
        if self._config.batch.file_size_limit_mb < 1:
            errors.append(f"File size limit must be at least 1MB: {self._config.batch.file_size_limit_mb}")
        
        # Validate grid config
        if self._config.grid.cluster_type not in ['local', 'remote']:
            errors.append(f"Invalid cluster type: {self._config.grid.cluster_type}")
        
        if self._config.grid.n_workers < 1:
            errors.append(f"Number of workers must be at least 1: {self._config.grid.n_workers}")
        
        # Validate logging config
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self._config.logging.level.upper() not in valid_log_levels:
            errors.append(f"Invalid log level: {self._config.logging.level}")
        
        return errors
    
    def save_to_file(self, file_path: str) -> None:
        """
        Save current configuration to file.
        
        :param file_path: Path to save configuration
        """
        try:
            config_dict = self.get_dict()
            
            # Create directory if it doesn't exist
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
            
            self.logger.info(f"Configuration saved to {file_path}")
            
        except Exception as e:
            raise ConfigurationError(f"Could not save configuration to {file_path}: {e}")
    
    def create_default_config(self, file_path: str) -> None:
        """
        Create a default configuration file.
        
        :param file_path: Path to create the configuration file
        """
        self.save_to_file(file_path)


def load_config(config_file: Optional[str] = None) -> ConfigManager:
    """
    Load configuration from file and environment.
    
    :param config_file: Path to configuration file
    :return: Configuration manager
    """
    return ConfigManager(config_file)


def create_default_config_file(file_path: str = "markdown_converter_config.yaml") -> None:
    """
    Create a default configuration file.
    
    :param file_path: Path to create the configuration file
    """
    config_manager = ConfigManager()
    config_manager.create_default_config(file_path) 