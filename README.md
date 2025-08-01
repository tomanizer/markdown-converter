# Markdown Converter

A Python-based tool for converting various document formats to clean, readable markdown optimized for LLM processing. Primary focus is information extraction with formatting as secondary concern.

## Features

- **Multiple Format Support**: Word (.docx), PDF (.pdf), Excel (.xlsx), HTML, Outlook emails (.msg)
- **Parallel Processing**: Process large document collections efficiently
- **Information Preservation**: Extract ALL information, never lose content
- **LLM Optimization**: Clean, readable markdown output
- **Robust Error Handling**: Retry with fallback strategies
- **Grid Computing Support**: Distributed processing capabilities
- **Memory Management**: Efficient handling of large files (up to 70MB)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/markdown-converter.git
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
from markdown_converter import convert_file, convert_directory

# Convert a single file
result = convert_file('document.docx', 'output.md')

# Convert a directory of files
results = convert_directory(
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
markdown-converter convert documents/ -o markdown/ --parallel

# Process with progress reporting
markdown-converter convert documents/ -o markdown/ --progress --workers 8
```

## Architecture

```
markdown_converter/
├── src/markdown_converter/
│   ├── core/              # Core conversion logic
│   ├── parsers/           # Format-specific parsers
│   ├── processors/        # Content processors
│   └── formatters/        # Output formatters
├── tests/                 # Test suite
├── docs/                  # Documentation
└── examples/              # Sample files
```

## Supported Formats

| Format | Primary Parser | Fallback Parser | Status |
|--------|---------------|-----------------|--------|
| Word (.docx) | mammoth | python-docx | ✅ |
| PDF (.pdf) | pdfplumber | PyMuPDF | ✅ |
| Excel (.xlsx) | openpyxl | pandas | ✅ |
| HTML | beautifulsoup4 | - | ✅ |
| Email (.msg) | extract-msg | - | ✅ |

## Performance

- **Parallel Processing**: Utilize all available CPU cores
- **Memory Efficient**: Handle files up to 70MB
- **Batch Processing**: Process 5GB+ document collections
- **Progress Reporting**: Real-time progress tracking
- **Grid Computing**: Distributed processing support

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
# Set log level
export MARKDOWN_CONVERTER_LOG_LEVEL=INFO

# Set number of workers
export MARKDOWN_CONVERTER_WORKERS=8

# Set cache directory
export MARKDOWN_CONVERTER_CACHE_DIR=./cache
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

### Core Functions

```python
def convert_file(
    input_path: str,
    output_path: Optional[str] = None,
    config: Optional[Dict] = None
) -> str:
    """Convert a single file to markdown."""

def convert_directory(
    input_dir: str,
    output_dir: str,
    parallel: bool = True,
    workers: Optional[int] = None,
    progress: bool = True
) -> List[Tuple[str, str, str]]:
    """Convert all files in a directory to markdown."""
```

### Parser Classes

```python
class WordParser:
    """Parse Word documents to markdown."""

class PDFParser:
    """Parse PDF documents to markdown."""

class ExcelParser:
    """Parse Excel spreadsheets to markdown."""
```

## Error Handling

The tool implements robust error handling with multiple fallback strategies:

1. **Primary Method**: Try pandoc conversion
2. **Format-Specific**: Try format-specific parsers
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