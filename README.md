# Markdown Converter

A Python-based tool for converting various document formats to clean, readable markdown optimized for LLM processing. Primary focus is information extraction with formatting as secondary concern.

## Features

- **Multiple Format Support**: Word (.docx), PDF (.pdf), Excel (.xlsx), HTML, Outlook emails (.msg)
- **Parallel Processing**: Process large document collections efficiently
- **Information Preservation**: Extract ALL information, never lose content
- **LLM Optimization**: Clean, readable markdown output
- **Robust Error Handling**: Retry with fallback strategies
- **Memory Management**: Efficient handling of large files (up to 70MB)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/tomanizer/markdown-converter.git
cd markdown-converter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Note: pandoc 3.7+ needs to be installed separately
# macOS: brew install pandoc
# Ubuntu: sudo apt-get install pandoc
# Windows: Download from https://pandoc.org/installing.html
```

### Basic Usage

```python
from markdown_converter.core.converter import MainConverter

# Convert a single file
converter = MainConverter()
result = converter.convert_file('document.docx', 'output.md')

# Convert a directory of files
results = converter.convert_directory(
    input_dir='documents/',
    output_dir='markdown/',
    parallel=True
)
```

### Command Line

```bash
# Convert a single file
markdown-converter convert document.docx -o output.md

# Convert a directory
markdown-converter batch documents/ -o markdown/ --workers 8

# Process with progress reporting
markdown-converter batch documents/ -o markdown/ --progress --workers 8
```

## Architecture

```
markdown_converter/
├── src/markdown_converter/
│   ├── core/              # Core conversion logic
│   │   ├── converter.py   # Main conversion engine
│   │   ├── file_converter.py # File handling utilities
│   │   └── exceptions.py  # Custom exceptions
│   ├── parsers/           # Format-specific parsers
│   │   ├── base.py        # Base parser interface
│   │   ├── word_parser.py # Word document parser
│   │   ├── pdf_parser.py  # PDF document parser
│   │   ├── excel_parser.py # Excel spreadsheet parser
│   │   ├── html_parser.py # HTML document parser
│   │   └── pandoc_parser.py # Pandoc integration
│   ├── utils/             # Utility functions
│   │   └── document_generator.py # Document generation utilities
│   └── cli.py            # Command line interface
├── tests/                 # Test suite
├── examples/              # Sample files and usage examples
└── docs/                  # Documentation
```

## Supported Formats

| Format | Primary Parser | Fallback Parser | Status |
|--------|---------------|-----------------|--------|
| Word (.docx) | python-docx | pandoc | ✅ |
| PDF (.pdf) | pdfplumber | pandoc | ✅ |
| Excel (.xlsx) | openpyxl | pandas | ✅ |
| HTML | beautifulsoup4 | pandoc | ✅ |
| Email (.msg) | extract-msg | - | ✅ |

## Performance

- **Parallel Processing**: Utilize all available CPU cores
- **Memory Efficient**: Handle files up to 70MB
- **Batch Processing**: Process large document collections
- **Progress Reporting**: Real-time progress tracking

## Development

### Setup Development Environment

```bash
# Install development dependencies
make install-dev

# Run tests
make test

# Run linting
make lint

# Format code
make format
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/markdown_converter

# Run performance tests
pytest -m performance

# Run integration tests
pytest -m integration
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/
```

## Configuration

### Environment Variables

```bash
# Set number of workers
export MDC_MAX_WORKERS=8

# Set memory limit
export MDC_MAX_MEMORY_MB=2048

# Set batch size
export MDC_BATCH_SIZE=100

# Set output format
export MDC_OUTPUT_FORMAT=markdown

# Set structure preservation
export MDC_PRESERVE_STRUCTURE=true
```

### YAML Configuration

```yaml
# config/default.yaml
conversion:
  parallel: true
  workers: 8
  memory_limit: 2048  # MB

formats:
  word:
    preserve_tables: true
    extract_images: true
  pdf:
    extract_tables: true
    ocr_enabled: false

output:
  markdown_format: "clean"
  include_metadata: true
  image_extraction: true
```

## API Reference

### Core Classes

```python
class MainConverter:
    """Main conversion engine for document processing."""

class FileConverter:
    """Handles individual file conversion operations."""

class BaseParser:
    """Base class for all document parsers."""
```

### Parser Classes

```python
class WordParser:
    """Parse Word documents to markdown."""

class PDFParser:
    """Parse PDF documents to markdown."""

class ExcelParser:
    """Parse Excel spreadsheets to markdown."""

class HTMLParser:
    """Parse HTML documents to markdown."""

class PandocParser:
    """Universal parser using pandoc."""
```

## CLI Commands

The tool provides a comprehensive command-line interface:

- `convert` - Convert a single file
- `batch` - Convert a directory of files
- `info` - Show system information
- `formats` - List supported formats
- `health` - Health check
- `analyze` - Analyze file content
- `file-info` - Get file information
- `validate` - Validate conversion
- `can-convert` - Check if file can be converted
- `list-parsers` - List available parsers
- `test` - Test conversion on sample files
- `clean` - Clean temporary files

## Error Handling

The tool implements robust error handling with multiple fallback strategies:

1. **Primary Method**: Try format-specific parser
2. **Pandoc Fallback**: Try pandoc conversion
3. **Generic Extraction**: Extract all text content
4. **Skip and Continue**: Skip failed files, continue processing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings
- Maintain >90% test coverage
- Update documentation for new features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Pandoc](https://pandoc.org/) - Universal document converter
- [python-docx](https://python-docx.readthedocs.io/) - Word document parsing
- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF text extraction
- [fsspec](https://filesystem-spec.readthedocs.io/) - File system abstraction

## Roadmap

- [ ] Web service API
- [ ] Docker containerization
- [ ] Cloud storage integration
- [ ] Advanced table formatting
- [ ] OCR support for scanned PDFs
- [ ] More document formats (PowerPoint, LaTeX, RTF)

## Support

- **Documentation**: [https://markdown-converter.readthedocs.io](https://markdown-converter.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/yourusername/markdown-converter/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/markdown-converter/discussions) 