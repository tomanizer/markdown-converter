"""
Unit tests for CLI interface.

Tests the command-line interface functionality including argument parsing,
command execution, and error handling.
"""

import os
import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from markdown_converter.cli import cli
from markdown_converter.core.exceptions import ConversionError


class TestCLI:
    """Test cases for CLI functionality."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_file(self, temp_dir):
        """Create a sample file for testing."""
        sample_file = temp_dir / "test.txt"
        sample_file.write_text("This is a test file.")
        return sample_file
    
    @pytest.fixture
    def sample_dir(self, temp_dir):
        """Create a sample directory with files for testing."""
        sample_dir = temp_dir / "sample_dir"
        sample_dir.mkdir()
        
        # Create some test files
        (sample_dir / "file1.txt").write_text("File 1 content")
        (sample_dir / "file2.txt").write_text("File 2 content")
        (sample_dir / "file3.docx").write_text("Word document content")
        
        return sample_dir
    
    def test_cli_help(self):
        """Test that CLI help works."""
        with patch('sys.argv', ['markdown-converter', '--help']):
            try:
                cli()
            except SystemExit:
                pass  # Expected behavior
    
    def test_convert_single_file(self, sample_file, temp_dir):
        """Test single file conversion command."""
        output_file = temp_dir / "output.md"
        
        with patch('sys.argv', [
            'markdown-converter', 'convert', 
            str(sample_file), str(output_file)
        ]):
            with patch('markdown_converter.cli.MainConverter') as mock_converter:
                mock_converter.return_value.convert_file.return_value = MagicMock(
                    success=True,
                    input_file=sample_file,
                    output_file=output_file,
                    error_message=None
                )
                
                try:
                    cli()
                except SystemExit:
                    pass  # Expected behavior
                
                mock_converter.return_value.convert_file.assert_called_once()
    
    def test_convert_single_file_auto_output(self, sample_file):
        """Test single file conversion with auto-generated output path."""
        with patch('sys.argv', [
            'markdown-converter', 'convert', str(sample_file)
        ]):
            with patch('markdown_converter.cli.MainConverter') as mock_converter:
                mock_converter.return_value.convert_file.return_value = MagicMock(
                    success=True,
                    input_file=sample_file,
                    output_file=sample_file.with_suffix('.md'),
                    error_message=None
                )
                
                try:
                    cli()
                except SystemExit:
                    pass  # Expected behavior
                
                mock_converter.return_value.convert_file.assert_called_once()
    
    def test_convert_single_file_error(self, sample_file):
        """Test single file conversion with error."""
        with patch('sys.argv', [
            'markdown-converter', 'convert', str(sample_file)
        ]):
            with patch('markdown_converter.cli.MainConverter') as mock_converter:
                mock_converter.return_value.convert_file.return_value = MagicMock(
                    success=False,
                    error_message="Test error"
                )
                
                with pytest.raises(SystemExit):
                    cli()
    
    def test_batch_conversion(self, sample_dir, temp_dir):
        """Test batch conversion command."""
        output_dir = temp_dir / "output"
        
        with patch('sys.argv', [
            'markdown-converter', 'batch', 
            str(sample_dir), str(output_dir)
        ]):
            with patch('markdown_converter.cli.MainConverter') as mock_converter:
                mock_converter.return_value.convert_directory.return_value = MagicMock(
                    total_files=3,
                    processed_files=2,
                    failed_files=1,
                    skipped_files=0,
                    start_time=0.0,
                    end_time=1.0,
                    processing_time=1.0,
                    results=[]
                )
                
                try:
                    cli()
                except SystemExit:
                    pass  # Expected behavior
                
                mock_converter.return_value.convert_directory.assert_called_once()
    
    def test_batch_conversion_error(self, sample_dir):
        """Test batch conversion with error."""
        with patch('sys.argv', [
            'markdown-converter', 'batch', str(sample_dir)
        ]):
            with patch('markdown_converter.cli.MainConverter') as mock_converter:
                mock_converter.return_value.convert_directory.side_effect = ConversionError("Test error")
                
                with pytest.raises(SystemExit):
                    cli()
    
    def test_info_command(self):
        """Test info command."""
        with patch('sys.argv', ['markdown-converter', 'info']):
            try:
                cli()
            except SystemExit:
                pass  # Expected behavior
    
    def test_info_command_detailed(self):
        """Test info command with detailed flag."""
        with patch('sys.argv', ['markdown-converter', 'info', '--detailed']):
            try:
                cli()
            except SystemExit:
                pass  # Expected behavior
    
    def test_formats_command(self):
        """Test formats command."""
        with patch('sys.argv', ['markdown-converter', 'formats']):
            try:
                cli()
            except SystemExit:
                pass  # Expected behavior
    
    def test_verbose_logging(self):
        """Test verbose logging option."""
        with patch('sys.argv', ['markdown-converter', '--verbose', 'info']):
            try:
                cli()
            except SystemExit:
                pass  # Expected behavior
    
    def test_config_file_loading(self, temp_dir):
        """Test config file loading."""
        config_file = temp_dir / "config.yml"
        config_file.write_text("output_format: html\npreserve_structure: true")
        
        with patch('sys.argv', [
            'markdown-converter', '--config', str(config_file), 'info'
        ]):
            try:
                cli()
            except SystemExit:
                pass  # Expected behavior
    
    def test_log_file_option(self, temp_dir):
        """Test log file option."""
        log_file = temp_dir / "test.log"
        
        with patch('sys.argv', [
            'markdown-converter', '--log-file', str(log_file), 'info'
        ]):
            try:
                cli()
            except SystemExit:
                pass  # Expected behavior
    
    def test_batch_conversion_options(self, sample_dir):
        """Test batch conversion with various options."""
        with patch('sys.argv', [
            'markdown-converter', 'batch', str(sample_dir),
            '--workers', '4', '--batch-size', '50', '--max-memory', '1024'
        ]):
            with patch('markdown_converter.cli.MainConverter') as mock_converter:
                mock_converter.return_value.convert_directory.return_value = MagicMock(
                    total_files=3,
                    processed_files=3,
                    failed_files=0,
                    skipped_files=0,
                    start_time=0.0,
                    end_time=1.0,
                    processing_time=1.0,
                    results=[]
                )
                
                try:
                    cli()
                except SystemExit:
                    pass  # Expected behavior
                
                mock_converter.return_value.convert_directory.assert_called_once()


class TestCLIHelpers:
    """Test CLI helper functions."""
    
    def test_setup_logging(self):
        """Test logging setup."""
        from markdown_converter.cli import setup_cli_logging
        setup_cli_logging(verbose=True, log_file=None, structured=False)
        # Just test that it doesn't raise an exception
    
    def test_load_config(self):
        """Test config loading."""
        from markdown_converter.cli import load_config
        config = load_config()
        assert isinstance(config, dict)
    
    def test_print_supported_formats(self, capsys):
        """Test printing supported formats."""
        from markdown_converter.cli import print_supported_formats
        print_supported_formats()
        captured = capsys.readouterr()
        assert "Supported Input Formats" in captured.out
    
    def test_print_processing_stats(self, capsys):
        """Test printing processing statistics."""
        from markdown_converter.cli import print_processing_stats
        stats = MagicMock(
            total_files=10,
            processed_files=8,
            failed_files=2,
            skipped_files=0,
            start_time=0.0,
            end_time=1.0,
            processing_time=1.0
        )
        print_processing_stats(stats)
        captured = capsys.readouterr()
        assert "Processing Statistics" in captured.out
        assert "Total files: 10" in captured.out
        assert "Processed: 8" in captured.out
        assert "Failed: 2" in captured.out 