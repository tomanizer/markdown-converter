"""
Unit tests for configuration management.

Tests the configuration loading, validation, and saving functionality.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.markdown_converter.config import (
    ConfigManager,
    ConversionConfig,
    BatchConfig,
    GridConfig,
    LoggingConfig,
    Config,
    load_config,
    create_default_config_file
)
from src.markdown_converter.core.exceptions import ConfigurationError


class TestConfigClasses:
    """Test cases for configuration dataclasses."""
    
    def test_conversion_config_defaults(self):
        """Test ConversionConfig default values."""
        config = ConversionConfig()
        
        assert config.output_format == 'markdown'
        assert config.preserve_structure is True
        assert config.extract_images is True
        assert config.include_metadata is True
        assert config.image_format == 'png'
        assert config.image_quality == 85
        assert config.max_image_size == 1024
    
    def test_conversion_config_custom(self):
        """Test ConversionConfig with custom values."""
        config = ConversionConfig(
            output_format='html',
            preserve_structure=False,
            extract_images=False,
            include_metadata=False,
            image_format='jpg',
            image_quality=90,
            max_image_size=2048
        )
        
        assert config.output_format == 'html'
        assert config.preserve_structure is False
        assert config.extract_images is False
        assert config.include_metadata is False
        assert config.image_format == 'jpg'
        assert config.image_quality == 90
        assert config.max_image_size == 2048
    
    def test_batch_config_defaults(self):
        """Test BatchConfig default values."""
        config = BatchConfig()
        
        assert config.max_workers == 4
        assert config.batch_size == 100
        assert config.max_memory_mb == 2048
        assert config.file_size_limit_mb == 70
        assert config.continue_on_error is True
        assert config.show_progress_bar is True
        assert config.worker_timeout == 300
        assert config.chunk_size == 10
        assert config.memory_check_interval == 5
        assert config.memory_threshold == 0.8
        assert config.progress_update_interval == 1
        assert config.max_retries == 3
        assert config.retry_delay == 1
    
    def test_batch_config_custom(self):
        """Test BatchConfig with custom values."""
        config = BatchConfig(
            max_workers=8,
            batch_size=50,
            max_memory_mb=4096,
            file_size_limit_mb=100,
            continue_on_error=False,
            show_progress_bar=False,
            worker_timeout=600,
            chunk_size=20,
            memory_check_interval=10,
            memory_threshold=0.9,
            progress_update_interval=2,
            max_retries=5,
            retry_delay=2
        )
        
        assert config.max_workers == 8
        assert config.batch_size == 50
        assert config.max_memory_mb == 4096
        assert config.file_size_limit_mb == 100
        assert config.continue_on_error is False
        assert config.show_progress_bar is False
        assert config.worker_timeout == 600
        assert config.chunk_size == 20
        assert config.memory_check_interval == 10
        assert config.memory_threshold == 0.9
        assert config.progress_update_interval == 2
        assert config.max_retries == 5
        assert config.retry_delay == 2
    
    def test_grid_config_defaults(self):
        """Test GridConfig default values."""
        config = GridConfig()
        
        assert config.cluster_type == 'local'
        assert config.scheduler_address is None
        assert config.n_workers == 4
        assert config.n_threads_per_worker == 2
        assert config.memory_limit_per_worker == '2GB'
        assert config.dashboard_address == ':8787'
        assert config.job_timeout == 3600
        assert config.max_jobs == 10
        assert config.job_retries == 3
        assert config.monitor_resources is True
        assert config.resource_check_interval == 30
        assert config.max_memory_usage == 0.8
        assert config.max_cpu_usage == 0.9
        assert config.chunk_size == 50
        assert config.max_file_size_mb == 50
    
    def test_grid_config_custom(self):
        """Test GridConfig with custom values."""
        config = GridConfig(
            cluster_type='remote',
            scheduler_address='tcp://remote:8786',
            n_workers=8,
            n_threads_per_worker=4,
            memory_limit_per_worker='4GB',
            dashboard_address=':8788',
            job_timeout=7200,
            max_jobs=20,
            job_retries=5,
            monitor_resources=False,
            resource_check_interval=60,
            max_memory_usage=0.9,
            max_cpu_usage=0.95,
            chunk_size=100,
            max_file_size_mb=100
        )
        
        assert config.cluster_type == 'remote'
        assert config.scheduler_address == 'tcp://remote:8786'
        assert config.n_workers == 8
        assert config.n_threads_per_worker == 4
        assert config.memory_limit_per_worker == '4GB'
        assert config.dashboard_address == ':8788'
        assert config.job_timeout == 7200
        assert config.max_jobs == 20
        assert config.job_retries == 5
        assert config.monitor_resources is False
        assert config.resource_check_interval == 60
        assert config.max_memory_usage == 0.9
        assert config.max_cpu_usage == 0.95
        assert config.chunk_size == 100
        assert config.max_file_size_mb == 100
    
    def test_logging_config_defaults(self):
        """Test LoggingConfig default values."""
        config = LoggingConfig()
        
        assert config.level == 'INFO'
        assert config.format == '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        assert config.file is None
        assert config.console is True
        assert config.structured is False
    
    def test_logging_config_custom(self):
        """Test LoggingConfig with custom values."""
        config = LoggingConfig(
            level='DEBUG',
            format='%(levelname)s: %(message)s',
            file='/tmp/test.log',
            console=False,
            structured=True
        )
        
        assert config.level == 'DEBUG'
        assert config.format == '%(levelname)s: %(message)s'
        assert config.file == '/tmp/test.log'
        assert config.console is False
        assert config.structured is True
    
    def test_config_defaults(self):
        """Test Config default values."""
        config = Config()
        
        assert isinstance(config.conversion, ConversionConfig)
        assert isinstance(config.batch, BatchConfig)
        assert isinstance(config.grid, GridConfig)
        assert isinstance(config.logging, LoggingConfig)
        assert len(config.supported_extensions) > 0
        assert config.output_directory is None
        assert config.temp_directory is None
        assert config.cache_directory is None
    
    def test_config_custom(self):
        """Test Config with custom values."""
        config = Config(
            output_directory='/tmp/output',
            temp_directory='/tmp/temp',
            cache_directory='/tmp/cache'
        )
        
        assert config.output_directory == '/tmp/output'
        assert config.temp_directory == '/tmp/temp'
        assert config.cache_directory == '/tmp/cache'


class TestConfigManager:
    """Test cases for ConfigManager class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_config_manager_init(self):
        """Test ConfigManager initialization."""
        manager = ConfigManager()
        
        assert isinstance(manager._config, Config)
        assert manager.config_file is None
    
    def test_config_manager_with_file(self, temp_dir):
        """Test ConfigManager initialization with config file."""
        config_file = temp_dir / "config.yaml"
        config_file.write_text("""
conversion:
  output_format: html
  preserve_structure: false
batch:
  max_workers: 8
  batch_size: 50
""")
        
        manager = ConfigManager(str(config_file))
        
        assert manager.config_file == str(config_file)
        assert manager._config.conversion.output_format == 'html'
        assert manager._config.conversion.preserve_structure is False
        assert manager._config.batch.max_workers == 8
        assert manager._config.batch.batch_size == 50
    
    def test_load_from_file_invalid_yaml(self, temp_dir):
        """Test loading invalid YAML file."""
        config_file = temp_dir / "invalid.yaml"
        config_file.write_text("invalid: yaml: content: [")
        
        # Should not raise an exception, just log a warning
        manager = ConfigManager(str(config_file))
        
        # Should use default values
        assert manager._config.conversion.output_format == 'markdown'
    
    def test_load_from_file_nonexistent(self):
        """Test loading non-existent config file."""
        manager = ConfigManager("nonexistent.yaml")
        
        # Should use default values
        assert manager._config.conversion.output_format == 'markdown'
    
    def test_load_from_environment(self):
        """Test loading configuration from environment variables."""
        env_vars = {
            'MDC_OUTPUT_FORMAT': 'html',
            'MDC_PRESERVE_STRUCTURE': 'false',
            'MDC_MAX_WORKERS': '8',
            'MDC_BATCH_SIZE': '50',
            'MDC_MAX_MEMORY_MB': '4096',
            'MDC_LOG_LEVEL': 'DEBUG',
            'MDC_OUTPUT_DIRECTORY': '/tmp/output'
        }
        
        with patch.dict(os.environ, env_vars):
            manager = ConfigManager()
            
            assert manager._config.conversion.output_format == 'html'
            assert manager._config.conversion.preserve_structure is False
            assert manager._config.batch.max_workers == 8
            assert manager._config.batch.batch_size == 50
            assert manager._config.batch.max_memory_mb == 4096
            assert manager._config.logging.level == 'DEBUG'
            assert manager._config.output_directory == '/tmp/output'
    
    def test_load_from_environment_invalid_values(self):
        """Test loading invalid environment variable values."""
        env_vars = {
            'MDC_MAX_WORKERS': 'invalid',
            'MDC_BATCH_SIZE': 'not_a_number',
            'MDC_MAX_MEMORY_MB': 'negative'
        }
        
        with patch.dict(os.environ, env_vars):
            manager = ConfigManager()
            
            # Should use default values for invalid ones
            assert manager._config.batch.max_workers == 4  # default
            assert manager._config.batch.batch_size == 100  # default
            assert manager._config.batch.max_memory_mb == 2048  # default
    
    def test_get_config(self):
        """Test getting configuration."""
        manager = ConfigManager()
        config = manager.get_config()
        
        assert isinstance(config, Config)
        assert config.conversion.output_format == 'markdown'
    
    def test_get_conversion_config(self):
        """Test getting conversion configuration."""
        manager = ConfigManager()
        config = manager.get_conversion_config()
        
        assert isinstance(config, ConversionConfig)
        assert config.output_format == 'markdown'
    
    def test_get_batch_config(self):
        """Test getting batch configuration."""
        manager = ConfigManager()
        config = manager.get_batch_config()
        
        assert isinstance(config, BatchConfig)
        assert config.max_workers == 4
    
    def test_get_grid_config(self):
        """Test getting grid configuration."""
        manager = ConfigManager()
        config = manager.get_grid_config()
        
        assert isinstance(config, GridConfig)
        assert config.cluster_type == 'local'
    
    def test_get_logging_config(self):
        """Test getting logging configuration."""
        manager = ConfigManager()
        config = manager.get_logging_config()
        
        assert isinstance(config, LoggingConfig)
        assert config.level == 'INFO'
    
    def test_get_dict(self):
        """Test getting configuration as dictionary."""
        manager = ConfigManager()
        config_dict = manager.get_dict()
        
        assert isinstance(config_dict, dict)
        assert 'conversion' in config_dict
        assert 'batch' in config_dict
        assert 'grid' in config_dict
        assert 'logging' in config_dict
        assert config_dict['conversion']['output_format'] == 'markdown'
        assert config_dict['batch']['max_workers'] == 4
    
    def test_validate_valid_config(self):
        """Test validation of valid configuration."""
        manager = ConfigManager()
        errors = manager.validate()
        
        assert len(errors) == 0
    
    def test_validate_invalid_config(self):
        """Test validation of invalid configuration."""
        manager = ConfigManager()
        
        # Set invalid values
        manager._config.conversion.output_format = 'invalid'
        manager._config.conversion.image_quality = 150
        manager._config.batch.max_workers = 0
        manager._config.batch.max_memory_mb = 50
        manager._config.batch.file_size_limit_mb = 0
        manager._config.grid.cluster_type = 'invalid'
        manager._config.grid.n_workers = 0
        manager._config.logging.level = 'INVALID'
        
        errors = manager.validate()
        
        assert len(errors) > 0
        assert any('Invalid output format' in error for error in errors)
        assert any('Image quality must be between' in error for error in errors)
        assert any('Max workers must be at least' in error for error in errors)
        assert any('Max memory must be at least' in error for error in errors)
        assert any('File size limit must be at least' in error for error in errors)
        assert any('Invalid cluster type' in error for error in errors)
        assert any('Number of workers must be at least' in error for error in errors)
        assert any('Invalid log level' in error for error in errors)
    
    def test_save_to_file(self, temp_dir):
        """Test saving configuration to file."""
        manager = ConfigManager()
        config_file = temp_dir / "saved_config.yaml"
        
        manager.save_to_file(str(config_file))
        
        assert config_file.exists()
        
        # Verify the file contains valid YAML
        with open(config_file, 'r') as f:
            import yaml
            saved_config = yaml.safe_load(f)
        
        assert saved_config['conversion']['output_format'] == 'markdown'
        assert saved_config['batch']['max_workers'] == 4
    
    def test_save_to_file_error(self, temp_dir):
        """Test saving configuration to file with error."""
        manager = ConfigManager()
        
        # Try to save to a directory (should fail)
        config_file = temp_dir
        
        with pytest.raises(ConfigurationError):
            manager.save_to_file(str(config_file))
    
    def test_create_default_config(self, temp_dir):
        """Test creating default configuration file."""
        config_file = temp_dir / "default_config.yaml"
        
        manager = ConfigManager()
        manager.create_default_config(str(config_file))
        
        assert config_file.exists()
        
        # Verify the file contains valid YAML
        with open(config_file, 'r') as f:
            import yaml
            saved_config = yaml.safe_load(f)
        
        assert saved_config['conversion']['output_format'] == 'markdown'
        assert saved_config['batch']['max_workers'] == 4


class TestConfigFunctions:
    """Test cases for configuration utility functions."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_load_config_function(self):
        """Test load_config function."""
        manager = load_config()
        
        assert isinstance(manager, ConfigManager)
        assert manager._config.conversion.output_format == 'markdown'
    
    def test_load_config_function_with_file(self, temp_dir):
        """Test load_config function with config file."""
        config_file = temp_dir / "test_config.yaml"
        config_file.write_text("""
conversion:
  output_format: html
batch:
  max_workers: 8
""")
        
        manager = load_config(str(config_file))
        
        assert isinstance(manager, ConfigManager)
        assert manager._config.conversion.output_format == 'html'
        assert manager._config.batch.max_workers == 8
    
    def test_create_default_config_file(self, temp_dir):
        """Test create_default_config_file function."""
        config_file = temp_dir / "default_config.yaml"
        
        create_default_config_file(str(config_file))
        
        assert config_file.exists()
        
        # Verify the file contains valid YAML
        with open(config_file, 'r') as f:
            import yaml
            saved_config = yaml.safe_load(f)
        
        assert saved_config['conversion']['output_format'] == 'markdown'
        assert saved_config['batch']['max_workers'] == 4
    
    def test_create_default_config_file_default_path(self, temp_dir):
        """Test create_default_config_file function with default path."""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            
            with patch('builtins.open', create=True) as mock_open:
                mock_file = MagicMock()
                mock_open.return_value.__enter__.return_value = mock_file
                
                create_default_config_file()
                
                mock_open.assert_called_once()
                mock_file.write.assert_called()  # At least once, not exactly once


class TestConfigurationIntegration:
    """Integration tests for configuration system."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_configuration_precedence(self, temp_dir):
        """Test configuration precedence (CLI > ENV > FILE > DEFAULTS)."""
        # Create config file
        config_file = temp_dir / "config.yaml"
        config_file.write_text("""
conversion:
  output_format: html
  preserve_structure: false
batch:
  max_workers: 6
  batch_size: 75
""")
        
        # Set environment variables (should override file)
        env_vars = {
            'MDC_OUTPUT_FORMAT': 'pdf',
            'MDC_MAX_WORKERS': '8',
            'MDC_BATCH_SIZE': '100'
        }
        
        with patch.dict(os.environ, env_vars):
            manager = ConfigManager(str(config_file))
            
            # Environment should override file
            assert manager._config.conversion.output_format == 'pdf'
            assert manager._config.batch.max_workers == 8
            assert manager._config.batch.batch_size == 100
            
            # File should override defaults for values not in env
            assert manager._config.conversion.preserve_structure is False
    
    def test_configuration_validation_integration(self):
        """Test configuration validation in integration."""
        manager = ConfigManager()
        
        # Valid configuration
        errors = manager.validate()
        assert len(errors) == 0
        
        # Invalid configuration
        manager._config.conversion.output_format = 'invalid'
        manager._config.batch.max_workers = -1
        
        errors = manager.validate()
        assert len(errors) > 0
        assert any('Invalid output format' in error for error in errors)
        assert any('Max workers must be at least' in error for error in errors)
    
    def test_configuration_save_load_cycle(self, temp_dir):
        """Test saving and loading configuration."""
        manager1 = ConfigManager()
        
        # Modify some values
        manager1._config.conversion.output_format = 'html'
        manager1._config.batch.max_workers = 8
        manager1._config.logging.level = 'DEBUG'
        
        # Save configuration
        config_file = temp_dir / "test_config.yaml"
        manager1.save_to_file(str(config_file))
        
        # Load configuration in new manager
        manager2 = ConfigManager(str(config_file))
        
        # Verify values are preserved
        assert manager2._config.conversion.output_format == 'html'
        assert manager2._config.batch.max_workers == 8
        assert manager2._config.logging.level == 'DEBUG' 