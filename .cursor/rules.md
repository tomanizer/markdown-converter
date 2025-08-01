# Development Rules & Guidelines

## Code Quality Standards

### Python Code Style
- **Formatting**: Use Black for code formatting
- **Linting**: Use flake8 for linting
- **Type Checking**: Use mypy for type annotations
- **Line Length**: 88 characters (Black default)
- **Imports**: Use absolute imports, organize with isort

### Documentation Standards
- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Include type hints for all functions
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
from typing import List, Optional

# Third-party imports
import click
import fsspec
import pypandoc

# Local imports
from markdown_converter.core.converter import DocumentConverter
from markdown_converter.parsers.word_parser import WordParser
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
- **Logging**: Log all errors with context
- **User Feedback**: Provide clear error messages

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

### Code Documentation
```python
def convert_document(file_path: str, output_path: Optional[str] = None) -> str:
    """Convert a document to markdown format.
    
    Args:
        file_path: Path to the input document
        output_path: Optional path for output file
        
    Returns:
        str: The converted markdown content
        
    Raises:
        ConversionError: If conversion fails
        FileNotFoundError: If input file doesn't exist
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