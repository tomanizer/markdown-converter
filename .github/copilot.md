# GitHub Copilot Instructions

This document provides instructions for using GitHub Copilot effectively with the markdown-converter project.

## Project Context for Copilot

### **Project Overview**
- **Purpose**: Convert various document formats to clean, readable markdown for LLM processing
- **Primary Focus**: Information extraction over visual fidelity
- **Scale**: Process 5GB of documents (100s of files) in parallel
- **Key Formats**: Word (.docx), PDF (.pdf), Excel (.xlsx), HTML, Outlook emails (.msg)

### **Architecture Principles**
1. **Information Preservation**: Never lose content, formatting secondary
2. **Parallel Processing**: Utilize all CPU cores for large batches
3. **Error Recovery**: Retry with different methods, skip if all fail
4. **LLM Optimization**: Clean, readable markdown output
5. **Professional Standards**: >90% test coverage, proper documentation

### **Technology Stack**
- **Primary Engine**: Pandoc for reliable format conversion
- **File System**: fsspec + pathlib for universal file handling
- **Format Parsers**: python-docx, pdfplumber, openpyxl
- **Parallel Processing**: multiprocessing with all CPU cores
- **Error Handling**: tenacity for retry logic
- **Memory Management**: psutil for monitoring

## Copilot Prompts for Common Tasks

### **When Implementing Parsers**
```
# Context: Implementing a document parser for markdown-converter
# Requirements: Extract ALL information, preserve tables, handle errors gracefully
# Architecture: Use pandoc as primary, format-specific parsers as fallback
# Code Style: Type hints, reStructuredText docstrings, logging (no print), error handling with tenacity
```

### **When Adding Error Handling**
```
# Context: Adding error handling to markdown-converter
# Requirements: Never lose content, retry with different methods, skip if all fail
# Pattern: Use tenacity for retry logic, log errors with context
# Example: Try pandoc first, then format-specific parser, then generic extraction
```

### **When Implementing Parallel Processing**
```
# Context: Implementing parallel processing for markdown-converter
# Requirements: Use all CPU cores, handle 5GB of documents, memory efficient
# Pattern: Use multiprocessing.Pool, monitor memory with psutil
# Safety: Worker error isolation, progress reporting, graceful degradation
```

### **When Writing Tests**
```
# Context: Writing tests for markdown-converter
# Requirements: >90% coverage, test all formats, error scenarios
# Pattern: Use pytest, mock external dependencies, test error handling
# Files: Test with sample Word/PDF files, corrupted files, large files
```

### **When Adding Documentation**
```
# Context: Adding documentation for markdown-converter
# Style: Google docstrings, type hints, comprehensive examples
# Focus: LLM processing use cases, large-scale batch processing
# Examples: Show 5GB processing workflows, error handling patterns
```

## Key Files to Reference

### **Research Documents** (`research/`)
- `PROJECT_PLAN.md` - High-level project overview
- `REQUIREMENTS.md` - Detailed requirements specification
- `INTEGRATION_STRATEGY.md` - Technical integration approach
- `IMPLEMENTATION_PLAN.md` - 10-step development roadmap

### **Development Rules** (`.cursor/rules.md`)
- Code quality standards
- Testing requirements
- Documentation guidelines
- Error handling patterns

### **Project Structure**
```
src/markdown_converter/
├── core/              # Core conversion logic
├── parsers/           # Format-specific parsers
├── processors/        # Content processors
└── formatters/        # Output formatters
```

## Common Development Patterns

### **Parser Implementation Pattern**
```python
import structlog
from typing import Optional

logger = structlog.get_logger()

class WordParser:
    """Parse Word documents to markdown with fallback strategies."""

    def convert(self, file_path: str) -> str:
        """Convert Word document to markdown.

        :param file_path: Path to Word document
        :type file_path: str
        :return: Markdown content
        :rtype: str
        :raises ConversionError: If all conversion methods fail
        """
        logger.info("Starting Word document conversion", file_path=file_path)

        # Try pandoc first
        try:
            result = self._convert_with_pandoc(file_path)
            logger.info("Word conversion successful with pandoc", file_path=file_path)
            return result
        except Exception as e:
            logger.warning("Pandoc failed, trying python-docx", file_path=file_path, error=str(e))

        # Try format-specific parser
        try:
            result = self._convert_with_python_docx(file_path)
            logger.info("Word conversion successful with python-docx", file_path=file_path)
            return result
        except Exception as e:
            logger.warning("python-docx failed, extracting all text", file_path=file_path, error=str(e))

        # Last resort: extract all text
        result = self._extract_all_text(file_path)
        logger.info("Word conversion completed with text extraction", file_path=file_path)
        return result
```

### **Error Handling Pattern**
```python
@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=4, max=10)
)
def convert_with_retry(file_path: str) -> str:
    """Convert file with retry logic."""
    try:
        return convert_document(file_path)
    except Exception as e:
        logger.warning(f"Conversion failed, retrying: {e}")
        raise
```

### **Parallel Processing Pattern**
```python
def process_batch_parallel(file_list: List[str], output_dir: str) -> List[Tuple[str, str, str]]:
    """Process files in parallel with progress reporting."""
    with Pool(processes=cpu_count()) as pool:
        args = [(file_path, output_dir) for file_path in file_list]
        results = pool.map(convert_single_file_parallel, args)
    return results
```

## Copilot Best Practices

### **1. Always Reference Context**
- Mention the project's focus on information extraction
- Reference the 5GB processing scale
- Emphasize LLM optimization over visual fidelity

### **2. Follow Error Handling Patterns**
- Use tenacity for retry logic
- Implement multiple fallback strategies
- Never lose content due to formatting issues

### **3. Consider Performance**
- Use parallel processing for large batches
- Monitor memory usage with psutil
- Implement progress reporting

### **4. Maintain Quality Standards**
- Add type hints to all functions
- Write comprehensive docstrings
- Include error handling scenarios
- Add tests for new functionality

### **5. Focus on LLM Use Cases**
- Clean, readable markdown output
- Preserve table structures
- Extract images with links
- Include metadata when possible

## Example Copilot Prompts

### **For New Parser**
```
Help me implement a PDF parser for markdown-converter that:
- Uses pdfplumber as primary parser
- Falls back to PyMuPDF if pdfplumber fails
- Extracts tables and preserves structure
- Handles multi-page documents
- Follows the project's error handling patterns
```

### **For Parallel Processing**
```
Help me implement parallel processing for markdown-converter that:
- Uses all available CPU cores
- Handles 5GB of documents efficiently
- Provides real-time progress reporting
- Implements worker error isolation
- Monitors memory usage to prevent crashes
```

### **For Error Handling**
```
Help me add robust error handling to markdown-converter that:
- Retries failed conversions with different methods
- Never loses content due to formatting issues
- Provides detailed error logging
- Continues processing even if some files fail
- Uses tenacity for retry logic
```

## Getting Started with Copilot

1. **Read the Research Documents**: Understand the project goals and requirements
2. **Review the Development Rules**: Follow the established patterns and standards
3. **Reference the Architecture**: Use the established module structure
4. **Focus on Information Preservation**: Never lose content, formatting is secondary
5. **Consider Scale**: Design for 5GB processing, not just single files

Remember: The primary goal is **information extraction for LLM processing**, not perfect visual formatting!
