# Development Rules & Guidelines

## Code Quality Standards

### Python Code Style
- **Formatting**: Use Black for code formatting
- **Linting**: Use flake8 for linting
- **Type Checking**: Use mypy for type annotations
- **Line Length**: 88 characters (Black default)
- **Imports**: Use absolute imports, organize with isort

### Documentation Standards
- **Docstrings**: Use reStructuredText format docstrings
- **Type Hints**: Include type hints for all functions and methods
- **README**: Comprehensive project documentation
- **API Docs**: Auto-generated from docstrings

### Testing Standards
- **Coverage**: >90% test coverage required
- **Unit Tests**: Test all functions independently
- **Integration Tests**: Test component interactions
- **Performance Tests**: Test memory usage and speed
- **Error Tests**: Test error handling scenarios

## Project Structure Rules

### File Organization
- **Source Code**: All code in `src/markdown_converter/`
- **Tests**: All tests in `tests/` directory
- **Documentation**: All docs in `docs/` directory
- **Examples**: Sample files in `examples/` directory
- **Scripts**: Build scripts in `scripts/` directory

### Import Organization
```python
# Standard library imports
import os
import sys
from pathlib import Path
from typing import List, Optional, Dict, Tuple, Union

# Third-party imports
import click
import fsspec
import pypandoc

# Local imports
from markdown_converter.core.converter import DocumentConverter
from markdown_converter.parsers.word_parser import WordParser
```

### Type Hints Standards
- **All functions**: Must have type hints for parameters and return values
- **All methods**: Must have type hints for parameters and return values
- **Complex types**: Use typing module (List, Dict, Optional, Union, etc.)
- **Generic types**: Use proper generic type annotations
- **Type aliases**: Create type aliases for complex types

```python
from typing import List, Dict, Optional, Union, Tuple
from pathlib import Path

# Type aliases for complex types
FileResult = Tuple[str, Optional[str], str]  # (file_path, output_path, status)
ConversionConfig = Dict[str, Union[str, int, bool]]

def convert_batch(
    file_list: List[Path], 
    output_dir: Path, 
    config: Optional[ConversionConfig] = None
) -> List[FileResult]:
    """Convert multiple files with type hints."""
    pass
```

## Development Workflow

### Git Workflow
- **Branches**: main, develop, feature branches
- **Commits**: Conventional commit messages
- **PRs**: Require tests and documentation
- **Releases**: Semantic versioning

### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass with >90% coverage
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed

## Error Handling Guidelines

### Exception Handling
- **Custom Exceptions**: Use domain-specific exceptions
- **Graceful Degradation**: Never crash on recoverable errors
- **User Feedback**: Provide clear error messages

### Logging Guidelines
- **Use logging module**: Throughout the codebase for all output
- **No print statements**: Except for CLI output and user-facing messages
- **Structured logging**: Use structlog for consistent log formatting
- **Log levels**: Use appropriate levels (DEBUG, INFO, WARNING, ERROR)
- **Context**: Include relevant context in log messages

```python
import logging
import structlog

# Setup structured logging
logger = structlog.get_logger()

def process_document(file_path: str) -> str:
    """Process a document with proper logging."""
    logger.info("Starting document processing", file_path=file_path)
    
    try:
        result = convert_document(file_path)
        logger.info("Document processed successfully", file_path=file_path)
        return result
    except Exception as e:
        logger.error("Document processing failed", file_path=file_path, error=str(e))
        raise
```

### Retry Logic
```python
@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=4, max=10)
)
def convert_with_retry(file_path: str) -> str:
    """Convert file with retry logic"""
    try:
        return convert_document(file_path)
    except Exception as e:
        logger.warning(f"Conversion failed, retrying: {e}")
        raise
```

## Performance Guidelines

### Memory Management
- **Monitoring**: Use psutil for memory tracking
- **Cleanup**: Force garbage collection after large operations
- **Chunking**: Process large files in chunks
- **Streaming**: Use streaming for large file operations

### Parallel Processing
- **Worker Safety**: Each worker gets its own resources
- **Error Isolation**: Worker errors don't crash the pool
- **Progress Tracking**: Real-time progress reporting
- **Resource Limits**: Monitor CPU and memory usage

## Security Guidelines

### File Handling
- **Path Validation**: Validate all file paths
- **Permission Checks**: Check file permissions
- **Safe Operations**: Use safe file operations
- **Input Validation**: Validate all user inputs

### Dependencies
- **Version Pinning**: Pin dependency versions
- **Security Updates**: Regular security updates
- **Vulnerability Scanning**: Scan for vulnerabilities
- **License Compliance**: Check license compatibility

## Documentation Standards

### Docstring Standards (reStructuredText)
- **Format**: Use reStructuredText format for all docstrings
- **Required sections**: param, type, return, rtype, raises
- **Optional sections**: note, warning, example, seealso
- **Class docstrings**: Include class purpose and usage
- **Method docstrings**: Include parameter descriptions and return values

```python
class DocumentConverter:
    """Convert various document formats to markdown.
    
    This class provides functionality to convert Word, PDF, Excel, and other
    document formats to clean, readable markdown optimized for LLM processing.
    
    :param config: Configuration options for conversion
    :type config: Optional[Dict[str, Any]]
    :param logger: Logger instance for output
    :type logger: Optional[structlog.BoundLogger]
    """
    
    def convert_file(self, file_path: str, output_path: Optional[str] = None) -> str:
        """Convert a single file to markdown format.
        
        :param file_path: Path to the input document
        :type file_path: str
        :param output_path: Optional path for output file
        :type output_path: Optional[str]
        :return: The converted markdown content
        :rtype: str
        :raises ConversionError: If conversion fails
        :raises FileNotFoundError: If input file doesn't exist
        :raises ValueError: If file format is not supported
        
        :note: This method will attempt multiple conversion strategies
               if the primary method fails.
        
        :example:
            >>> converter = DocumentConverter()
            >>> result = converter.convert_file("document.docx")
            >>> print(result)
            # Document Title
            ...
        """
```

### Project Documentation
- **README.md**: Project overview and quick start
- **API Reference**: Complete API documentation
- **User Guide**: Step-by-step usage guide
- **Contributing Guide**: Development guidelines

## Testing Guidelines

### Test Structure
```python
class TestWordParser:
    """Test cases for Word document parser."""
    
    def test_basic_conversion(self):
        """Test basic Word to markdown conversion."""
        # Arrange
        input_file = "test_files/sample.docx"
        expected_content = "# Sample Document"
        
        # Act
        result = WordParser().convert(input_file)
        
        # Assert
        assert expected_content in result
```

### Test Categories
- **Unit Tests**: Test individual functions
- **Integration Tests**: Test component interactions
- **Performance Tests**: Test speed and memory usage
- **Error Tests**: Test error handling
- **Format Tests**: Test all supported formats

## Release Guidelines

### Version Management
- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Changelog**: Document all changes
- **Release Notes**: Comprehensive release notes
- **Migration Guide**: Guide for breaking changes

### Quality Gates
- [ ] All tests pass
- [ ] Code coverage >90%
- [ ] No security vulnerabilities
- [ ] Documentation updated
- [ ] Performance benchmarks met 