"""
Unit tests for Python API.

Tests the high-level Python API functions including file conversion,
batch processing, and grid processing.
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

from src.markdown_converter.api import (
    MarkdownConverter, 
    convert_file, 
    convert_directory, 
    convert_with_grid,
    ConversionResult,
    BatchResult,
    GridResult
)
from src.markdown_converter.core.exceptions import ConversionError, BatchProcessingError, GridProcessingError


class TestMarkdownConverter:
    """Test cases for MarkdownConverter class."""
    
    @pytest.fixture
    def converter(self):
        """Create a MarkdownConverter instance."""
        return MarkdownConverter()
    
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
    
    def test_convert_file_success(self, converter, sample_file, temp_dir):
        """Test successful file conversion."""
        output_file = temp_dir / "output.md"
        
        with patch('src.markdown_converter.core.engine.ConversionEngine') as mock_engine:
            mock_engine.return_value.convert_document.return_value = True
            
            result = converter.convert_file(
                input_file=sample_file,
                output_file=output_file,
                output_format='markdown'
            )
            
            assert isinstance(result, ConversionResult)
            assert result.success is True
            assert result.input_file == sample_file
            assert result.output_file == output_file
            assert result.error_message is None
            assert result.file_size_mb > 0
    
    def test_convert_file_auto_output(self, converter, sample_file):
        """Test file conversion with auto-generated output path."""
        with patch('src.markdown_converter.core.engine.ConversionEngine') as mock_engine:
            mock_engine.return_value.convert_document.return_value = True
            
            result = converter.convert_file(
                input_file=sample_file,
                output_format='html'
            )
            
            assert isinstance(result, ConversionResult)
            assert result.success is True
            assert result.input_file == sample_file
            assert result.output_file.suffix == '.html'
    
    def test_convert_file_error(self, converter, sample_file):
        """Test file conversion with error."""
        with patch('src.markdown_converter.core.engine.ConversionEngine') as mock_engine:
            mock_engine.return_value.convert_document.side_effect = ConversionError("Test error")
            
            result = converter.convert_file(input_file=sample_file)
            
            assert isinstance(result, ConversionResult)
            assert result.success is False
            assert result.error_message == "Test error"
    
    def test_convert_file_not_found(self, converter):
        """Test file conversion with non-existent file."""
        non_existent_file = Path("/non/existent/file.txt")
        
        with pytest.raises(FileNotFoundError):
            converter.convert_file(input_file=non_existent_file)
    
    def test_convert_directory_success(self, converter, sample_dir, temp_dir):
        """Test successful directory conversion."""
        output_dir = temp_dir / "output"
        
        with patch('src.markdown_converter.core.batch_processor.BatchProcessor') as mock_processor:
            mock_processor.return_value.process_directory.return_value = MagicMock(
                total_files=3,
                processed_files=2,
                failed_files=1,
                skipped_files=0,
                start_time=0.0,
                end_time=1.0
            )
            
            result = converter.convert_directory(
                input_dir=sample_dir,
                output_dir=output_dir,
                max_workers=4,
                batch_size=10,
                max_memory_mb=1024,
                continue_on_error=True
            )
            
            assert isinstance(result, BatchResult)
            assert result.stats.total_files == 3
            assert result.stats.processed_files == 2
            assert result.stats.failed_files == 1
            assert result.stats.skipped_files == 0
    
    def test_convert_directory_error(self, converter, sample_dir):
        """Test directory conversion with error."""
        with patch('src.markdown_converter.core.batch_processor.BatchProcessor') as mock_processor:
            mock_processor.return_value.process_directory.side_effect = BatchProcessingError("Test error")
            
            with pytest.raises(BatchProcessingError):
                converter.convert_directory(input_dir=sample_dir)
    
    def test_convert_directory_not_found(self, converter):
        """Test directory conversion with non-existent directory."""
        non_existent_dir = Path("/non/existent/directory")
        
        with pytest.raises(FileNotFoundError):
            converter.convert_directory(input_dir=non_existent_dir)
    
    def test_convert_with_grid_success(self, converter, sample_dir, temp_dir):
        """Test successful grid conversion."""
        output_dir = temp_dir / "output"
        
        with patch('dask') as mock_dask:
            with patch('src.markdown_converter.core.grid_processor.GridProcessor') as mock_processor:
                mock_processor.return_value.start_cluster.return_value = MagicMock(
                    scheduler_address='tcp://localhost:8786',
                    dashboard_address='http://localhost:8787',
                    n_workers=4,
                    n_threads=8,
                    memory_limit='2GB',
                    status='running'
                )
                mock_processor.return_value.submit_job.return_value = MagicMock(
                    job_id='test-job-123',
                    status='submitted',
                    submitted_time=0.0,
                    total_tasks=10,
                    completed_tasks=0,
                    failed_tasks=0
                )
                mock_processor.return_value.get_job_status.return_value = MagicMock(
                    job_id='test-job-123',
                    status='completed',
                    submitted_time=0.0,
                    completed_time=1.0,
                    total_tasks=10,
                    completed_tasks=8,
                    failed_tasks=2
                )
                
                result = converter.convert_with_grid(
                    input_dir=sample_dir,
                    output_dir=output_dir,
                    cluster_type='local',
                    n_workers=4,
                    memory_limit='2GB'
                )
                
                assert isinstance(result, GridResult)
                assert result.job_info.job_id == 'test-job-123'
                assert result.job_info.status == 'completed'
                assert result.cluster_info is not None
    
    def test_convert_with_grid_no_dask(self, converter, sample_dir):
        """Test grid conversion when Dask is not available."""
        with patch('src.markdown_converter.core.grid_processor.DASK_AVAILABLE', False):
            with pytest.raises(Exception) as exc_info:
                converter.convert_with_grid(input_dir=sample_dir)
            
            assert "Dask is required" in str(exc_info.value)
    
    def test_convert_with_grid_error(self, converter, sample_dir):
        """Test grid conversion with error."""
        with patch('dask') as mock_dask:
            with patch('src.markdown_converter.core.grid_processor.GridProcessor') as mock_processor:
                mock_processor.return_value.start_cluster.side_effect = GridProcessingError("Test error")
                
                with pytest.raises(GridProcessingError):
                    converter.convert_with_grid(input_dir=sample_dir)
    
    def test_get_supported_formats(self, converter):
        """Test getting supported formats."""
        formats = converter.get_supported_formats()
        
        assert isinstance(formats, dict)
        assert 'input' in formats
        assert 'output' in formats
        assert '.docx' in formats['input']
        assert '.pdf' in formats['input']
        assert 'markdown' in formats['output']
        assert 'html' in formats['output']
    
    def test_validate_file_supported(self, converter, sample_file):
        """Test file validation for supported file."""
        assert converter.validate_file(sample_file) is True
    
    def test_validate_file_unsupported(self, converter, temp_dir):
        """Test file validation for unsupported file."""
        unsupported_file = temp_dir / "test.xyz"
        unsupported_file.write_text("Test content")
        
        assert converter.validate_file(unsupported_file) is False
    
    def test_get_file_info(self, converter, sample_file):
        """Test getting file information."""
        info = converter.get_file_info(sample_file)
        
        assert isinstance(info, dict)
        assert info['path'] == str(sample_file)
        assert info['name'] == sample_file.name
        assert info['extension'] == '.txt'
        assert info['size_bytes'] > 0
        assert info['size_mb'] > 0
        assert info['is_supported'] is True
        assert 'modified_time' in info
    
    def test_get_file_info_not_found(self, converter):
        """Test getting file information for non-existent file."""
        non_existent_file = Path("/non/existent/file.txt")
        
        with pytest.raises(FileNotFoundError):
            converter.get_file_info(non_existent_file)


class TestAPIFunctions:
    """Test cases for convenience API functions."""
    
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
    
    def test_convert_file_function(self, sample_file, temp_dir):
        """Test convert_file convenience function."""
        output_file = temp_dir / "output.md"
        
        with patch('src.markdown_converter.core.engine.ConversionEngine') as mock_engine:
            mock_engine.return_value.convert_document.return_value = True
            
            result = convert_file(
                input_file=sample_file,
                output_file=output_file,
                output_format='markdown'
            )
            
            assert isinstance(result, ConversionResult)
            assert result.success is True
            assert result.input_file == sample_file
            assert result.output_file == output_file
    
    def test_convert_directory_function(self, sample_dir, temp_dir):
        """Test convert_directory convenience function."""
        output_dir = temp_dir / "output"
        
        with patch('src.markdown_converter.core.batch_processor.BatchProcessor') as mock_processor:
            mock_processor.return_value.process_directory.return_value = MagicMock(
                total_files=3,
                processed_files=2,
                failed_files=1,
                skipped_files=0,
                start_time=0.0,
                end_time=1.0
            )
            
            result = convert_directory(
                input_dir=sample_dir,
                output_dir=output_dir,
                max_workers=4,
                batch_size=10,
                max_memory_mb=1024,
                continue_on_error=True
            )
            
            assert isinstance(result, BatchResult)
            assert result.stats.total_files == 3
            assert result.stats.processed_files == 2
    
    def test_convert_with_grid_function(self, sample_dir, temp_dir):
        """Test convert_with_grid convenience function."""
        output_dir = temp_dir / "output"
        
        with patch('src.markdown_converter.core.grid_processor.DASK_AVAILABLE', True):
            with patch('src.markdown_converter.core.grid_processor.GridProcessor') as mock_processor:
                mock_processor.return_value.start_cluster.return_value = MagicMock()
                mock_processor.return_value.submit_job.return_value = MagicMock(
                    job_id='test-job-123',
                    status='submitted'
                )
                mock_processor.return_value.get_job_status.return_value = MagicMock(
                    job_id='test-job-123',
                    status='completed'
                )
                
                result = convert_with_grid(
                    input_dir=sample_dir,
                    output_dir=output_dir,
                    cluster_type='local',
                    n_workers=4,
                    memory_limit='2GB'
                )
                
                assert isinstance(result, GridResult)
                assert result.job_info.job_id == 'test-job-123'
                assert result.job_info.status == 'completed'


class TestConversionResult:
    """Test cases for ConversionResult dataclass."""
    
    def test_conversion_result_creation(self):
        """Test creating a ConversionResult instance."""
        input_file = Path("/test/input.txt")
        output_file = Path("/test/output.md")
        
        result = ConversionResult(
            input_file=input_file,
            output_file=output_file,
            success=True,
            error_message=None,
            processing_time=1.5,
            file_size_mb=2.5
        )
        
        assert result.input_file == input_file
        assert result.output_file == output_file
        assert result.success is True
        assert result.error_message is None
        assert result.processing_time == 1.5
        assert result.file_size_mb == 2.5
    
    def test_conversion_result_with_error(self):
        """Test creating a ConversionResult instance with error."""
        input_file = Path("/test/input.txt")
        output_file = Path("/test/output.md")
        
        result = ConversionResult(
            input_file=input_file,
            output_file=output_file,
            success=False,
            error_message="Test error",
            processing_time=0.0,
            file_size_mb=0.0
        )
        
        assert result.input_file == input_file
        assert result.output_file == output_file
        assert result.success is False
        assert result.error_message == "Test error"
        assert result.processing_time == 0.0
        assert result.file_size_mb == 0.0


class TestBatchResult:
    """Test cases for BatchResult dataclass."""
    
    def test_batch_result_creation(self):
        """Test creating a BatchResult instance."""
        from src.markdown_converter.core.batch_processor import ProcessingStats
        
        stats = ProcessingStats(
            total_files=10,
            processed_files=8,
            failed_files=1,
            skipped_files=1,
            start_time=0.0,
            end_time=5.0
        )
        
        results = [
            ConversionResult(
                input_file=Path("/test/file1.txt"),
                output_file=Path("/test/file1.md"),
                success=True
            ),
            ConversionResult(
                input_file=Path("/test/file2.txt"),
                output_file=Path("/test/file2.md"),
                success=False,
                error_message="Test error"
            )
        ]
        
        config = {'max_workers': 4, 'batch_size': 10}
        
        batch_result = BatchResult(
            stats=stats,
            results=results,
            config=config
        )
        
        assert batch_result.stats == stats
        assert batch_result.results == results
        assert batch_result.config == config
        assert len(batch_result.results) == 2


class TestGridResult:
    """Test cases for GridResult dataclass."""
    
    def test_grid_result_creation(self):
        """Test creating a GridResult instance."""
        from src.markdown_converter.core.grid_processor import JobInfo
        
        job_info = JobInfo(
            job_id='test-job-123',
            status='completed',
            submitted_time=0.0,
            completed_time=1.0,
            total_tasks=10,
            completed_tasks=8,
            failed_tasks=2
        )
        
        results = [
            ConversionResult(
                input_file=Path("/test/file1.txt"),
                output_file=Path("/test/file1.md"),
                success=True
            )
        ]
        
        cluster_info = MagicMock(
            scheduler_address='tcp://localhost:8786',
            n_workers=4
        )
        
        grid_result = GridResult(
            job_info=job_info,
            results=results,
            cluster_info=cluster_info
        )
        
        assert grid_result.job_info == job_info
        assert grid_result.results == results
        assert grid_result.cluster_info == cluster_info
        assert len(grid_result.results) == 1 