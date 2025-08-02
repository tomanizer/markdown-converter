# Markdown Converter - Development Context

## Project Overview
A Python-based tool for converting various document formats (Word, PDF, Excel, HTML, email) to clean, readable markdown optimized for LLM processing. Primary focus is information extraction with formatting as secondary concern.

## Core Requirements
- **Input Formats**: Word (.docx), PDF (.pdf), Excel (.xlsx), HTML, Outlook emails (.msg)
- **Output**: Clean markdown optimized for LLM processing
- **Scale**: Process 5GB of documents (100s of files) in parallel
- **File Size**: Support up to 70MB individual files
- **Performance**: Utilize all CPU cores, grid computing support
- **Reliability**: Never lose content, retry with fallback strategies

## Key Design Principles
1. **Information Preservation**: Extract ALL information, formatting secondary
2. **Parallel Processing**: Use all available CPU cores
3. **Error Recovery**: Retry with different methods, skip if all fail
4. **LLM Optimization**: Clean, readable markdown output
5. **Scalability**: Support grid computing and large batches

## Architecture
```
markdown_converter/
├── src/markdown_converter/     # Source code
├── tests/                      # Test suite
├── docs/                       # Documentation
├── requirements/               # Dependency management
├── setup.py                   # Package configuration
└── pyproject.toml            # Modern Python packaging
```

## Core Dependencies
- **pandoc** - Universal document converter (primary engine)
- **fsspec** - File system abstraction
- **pathlib** - Path handling
- **python-docx** - Word document parsing
- **pdfplumber** - PDF text extraction
- **openpyxl** - Excel spreadsheet parsing
- **click** - CLI framework
- **pytest** - Testing framework

## Integration Strategy
1. **Pandoc as Primary Engine**: Use for reliable format conversion
2. **Format-Specific Fallbacks**: python-docx, pdfplumber, openpyxl
3. **Parallel Processing**: multiprocessing with all CPU cores
4. **Grid Computing**: Dask for distributed processing
5. **Error Handling**: Retry logic with tenacity
6. **Memory Management**: psutil for monitoring and cleanup

## Development Standards
- **Python 3.12+** with venv
- **Code Quality**: Black, flake8, mypy, pre-commit
- **Testing**: pytest with >90% coverage
- **Documentation**: Sphinx/mkdocs
- **CI/CD**: GitHub Actions
- **License**: MIT

## Implementation Phases
1. **Phase 1**: Professional project setup
2. **Phase 2**: Core architecture and pandoc integration
3. **Phase 3**: Format-specific parsers (Word, PDF)
4. **Phase 4**: Parallel processing and batch operations
5. **Phase 5**: CLI, API, and deployment

## Success Criteria
- Convert Word and PDF documents to markdown
- Process 5GB of documents in parallel
- Preserve table structures and extract images
- >90% test coverage
- PyPI-ready package

## Research & Planning
All research and planning documents are organized in the `research/` folder:
- `research/PROJECT_PLAN.md` - High-level project overview
- `research/REQUIREMENTS.md` - Detailed requirements specification
- `research/EXISTING_TOOLS_RESEARCH.md` - Market analysis
- `research/PANDOC_IMPROVEMENTS.md` - Value proposition analysis
- `research/IMPLEMENTATION_PLAN.md` - 10-step development roadmap
- `research/INTEGRATION_STRATEGY.md` - Technical integration approach

## Current Focus
We are implementing Step 1: Professional Project Setup ✅
- Project structure created
- Development environment configured
- Dependencies defined
- Code quality tools set up

**Next**: Step 2: Core Architecture Foundation
