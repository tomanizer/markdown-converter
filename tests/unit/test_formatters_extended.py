"""
Extended Unit Tests for Formatters

Additional unit tests to improve coverage for formatters with low coverage.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
import io
from typing import Any

from markdown_converter.formatters.base import BaseFormatter
from markdown_converter.formatters.markdown import MarkdownFormatter
from markdown_converter.core.exceptions import FormatterError


class TestBaseFormatterExtended:
    """Extended tests for BaseFormatter to improve coverage."""
    
    @pytest.fixture
    def base_formatter(self):
        """Create a BaseFormatter instance."""
        # Create a concrete implementation for testing
        class TestFormatter(BaseFormatter):
            def can_format(self, output_type: str, content: Any) -> bool:
                return True
            
            def format(self, output_type: str, content: Any, context=None) -> str:
                return str(content)
            
            def get_supported_output_types(self):
                return ['test']
        
        return TestFormatter()
    
    def test_format_with_complex_content(self, base_formatter):
        """Test formatting with complex content structure."""
        content = {
            'title': 'Test Document',
            'sections': [
                {
                    'heading': 'Section 1',
                    'content': 'This is section 1 content.',
                    'subsections': [
                        {'heading': 'Subsection 1.1', 'content': 'Subsection content.'}
                    ]
                },
                {
                    'heading': 'Section 2',
                    'content': 'This is section 2 content.',
                    'tables': [
                        {
                            'headers': ['Header 1', 'Header 2'],
                            'rows': [['Data 1', 'Data 2'], ['Data 3', 'Data 4']]
                        }
                    ]
                }
            ],
            'metadata': {
                'author': 'Test Author',
                'date': '2024-01-01',
                'keywords': ['test', 'document']
            }
        }
        
        result = base_formatter.format('test', content)
        
        assert result is not None
        assert "Test Document" in result
        assert "Section 1" in result
        assert "Section 2" in result
        assert "Test Author" in result
    
    def test_format_with_empty_content(self, base_formatter):
        """Test formatting with empty content."""
        content = {}
        
        result = base_formatter.format('test', content)
        
        assert result is not None
    
    def test_format_with_none_content(self, base_formatter):
        """Test formatting with None content."""
        result = base_formatter.format('test', None)
        
        assert result is not None
    
    def test_format_with_string_content(self, base_formatter):
        """Test formatting with string content."""
        content = "Simple string content"
        
        result = base_formatter.format('test', content)
        
        assert result is not None
        assert "Simple string content" in result
    
    def test_format_with_list_content(self, base_formatter):
        """Test formatting with list content."""
        content = [
            "Item 1",
            "Item 2",
            "Item 3"
        ]
        
        result = base_formatter.format('test', content)
        
        assert result is not None
        assert "Item 1" in result
        assert "Item 2" in result
        assert "Item 3" in result
    
    def test_format_with_nested_structure(self, base_formatter):
        """Test formatting with deeply nested structure."""
        content = {
            'level1': {
                'level2': {
                    'level3': {
                        'level4': {
                            'content': 'Deeply nested content'
                        }
                    }
                }
            }
        }
        
        result = base_formatter.format('test', content)
        
        assert result is not None
        assert "Deeply nested content" in result
    
    def test_format_with_special_characters(self, base_formatter):
        """Test formatting with special characters."""
        content = {
            'title': 'Document with Special Chars: & < > " \'',
            'content': 'Content with special chars: & < > " \'',
            'code': 'def test(): return "hello"'
        }
        
        result = base_formatter.format('test', content)
        
        assert result is not None
        assert "Document with Special Chars" in result
        assert "Content with special chars" in result
    
    def test_format_with_unicode_content(self, base_formatter):
        """Test formatting with unicode content."""
        content = {
            'title': 'Document with Unicode: éñüß',
            'content': 'Content with unicode: éñüß',
            'chinese': '中文内容',
            'japanese': '日本語の内容',
            'korean': '한국어 내용'
        }
        
        result = base_formatter.format('test', content)
        
        assert result is not None
        assert "Document with Unicode" in result
        assert "中文内容" in result
        assert "日本語の内容" in result
        assert "한국어 내용" in result
    
    def test_format_error_handling(self, base_formatter):
        """Test error handling in formatting."""
        # Test with non-serializable object
        class NonSerializable:
            def __init__(self):
                self.data = "test"
        
        content = {'test': NonSerializable()}
        
        result = base_formatter.format('test', content)
        
        # Should handle gracefully
        assert result is not None


class TestMarkdownFormatterExtended:
    """Extended tests for MarkdownFormatter to improve coverage."""
    
    @pytest.fixture
    def markdown_formatter(self):
        """Create a MarkdownFormatter instance."""
        return MarkdownFormatter()
    
    def test_format_markdown_with_headings(self, markdown_formatter):
        """Test markdown formatting with headings."""
        content = {
            'title': 'Main Title',
            'sections': [
                {'heading': 'Section 1', 'content': 'Section 1 content'},
                {'heading': 'Section 2', 'content': 'Section 2 content'},
                {'heading': 'Section 3', 'content': 'Section 3 content'}
            ]
        }
        
        result = markdown_formatter.format('markdown', content)
        
        assert result is not None
        assert "# Main Title" in result
        assert "## Section 1" in result
        assert "## Section 2" in result
        assert "## Section 3" in result
    
    def test_format_markdown_with_lists(self, markdown_formatter):
        """Test markdown formatting with lists."""
        content = {
            'title': 'List Document',
            'bullet_list': ['Item 1', 'Item 2', 'Item 3'],
            'numbered_list': ['First', 'Second', 'Third'],
            'nested_list': [
                'Parent 1',
                ['Child 1.1', 'Child 1.2'],
                'Parent 2',
                ['Child 2.1', 'Child 2.2']
            ]
        }
        
        result = markdown_formatter.format('markdown', content)
        
        assert result is not None
        assert "- Item 1" in result
        assert "- Item 2" in result
        assert "- Item 3" in result
        assert "1. First" in result
        assert "2. Second" in result
        assert "3. Third" in result
    
    def test_format_markdown_with_tables(self, markdown_formatter):
        """Test markdown formatting with tables."""
        content = {
            'title': 'Table Document',
            'tables': [
                {
                    'headers': ['Name', 'Age', 'City'],
                    'rows': [
                        ['John', '25', 'New York'],
                        ['Jane', '30', 'Los Angeles'],
                        ['Bob', '35', 'Chicago']
                    ]
                },
                {
                    'headers': ['Product', 'Price', 'Stock'],
                    'rows': [
                        ['Apple', '$1.00', '100'],
                        ['Orange', '$0.75', '50'],
                        ['Banana', '$0.50', '200']
                    ]
                }
            ]
        }
        
        result = markdown_formatter.format('markdown', content)
        
        assert result is not None
        assert "| Name | Age | City |" in result
        assert "| John | 25 | New York |" in result
        assert "| Product | Price | Stock |" in result
        assert "| Apple | $1.00 | 100 |" in result
    
    def test_format_markdown_with_links(self, markdown_formatter):
        """Test markdown formatting with links."""
        content = {
            'title': 'Link Document',
            'links': [
                {'text': 'Google', 'url': 'https://google.com'},
                {'text': 'GitHub', 'url': 'https://github.com'},
                {'text': 'Stack Overflow', 'url': 'https://stackoverflow.com'}
            ],
            'content': 'This document contains various links.'
        }
        
        result = markdown_formatter.format('markdown', content)
        
        assert result is not None
        assert "[Google](https://google.com)" in result
        assert "[GitHub](https://github.com)" in result
        assert "[Stack Overflow](https://stackoverflow.com)" in result
    
    def test_format_markdown_with_images(self, markdown_formatter):
        """Test markdown formatting with images."""
        content = {
            'title': 'Image Document',
            'images': [
                {'alt': 'Image 1', 'src': 'image1.jpg'},
                {'alt': 'Image 2', 'src': 'image2.png'},
                {'alt': 'Figure', 'src': 'figure.jpg', 'caption': 'Figure caption'}
            ],
            'content': 'This document contains various images.'
        }
        
        result = markdown_formatter.format('markdown', content)
        
        assert result is not None
        assert "![Image 1](image1.jpg)" in result
        assert "![Image 2](image2.png)" in result
        assert "![Figure](figure.jpg)" in result
        assert "Figure caption" in result
    
    def test_format_markdown_with_code(self, markdown_formatter):
        """Test markdown formatting with code blocks."""
        content = {
            'title': 'Code Document',
            'code_blocks': [
                {
                    'language': 'python',
                    'code': 'def hello_world():\n    print("Hello, World!")'
                },
                {
                    'language': 'javascript',
                    'code': 'function greet() {\n    console.log("Hello!");\n}'
                },
                {
                    'language': 'bash',
                    'code': 'echo "Hello from bash"'
                }
            ],
            'inline_code': 'This is `inline code` example.'
        }
        
        result = markdown_formatter.format('markdown', content)
        
        assert result is not None
        assert "```python" in result
        assert "def hello_world():" in result
        assert "```javascript" in result
        assert "function greet()" in result
        assert "```bash" in result
        assert "echo \"Hello from bash\"" in result
        assert "`inline code`" in result
    
    def test_format_markdown_with_blockquotes(self, markdown_formatter):
        """Test markdown formatting with blockquotes."""
        content = {
            'title': 'Quote Document',
            'quotes': [
                'This is a simple quote.',
                'This is a quote with **bold text** and *italic text*.',
                'This is a multi-line quote.\nIt spans multiple lines.'
            ]
        }
        
        result = markdown_formatter.format('markdown', content)
        
        assert result is not None
        assert "> This is a simple quote." in result
        assert "> This is a quote with **bold text** and *italic text*." in result
        assert "> This is a multi-line quote." in result
        assert "> It spans multiple lines." in result
    
    def test_format_markdown_with_emphasis(self, markdown_formatter):
        """Test markdown formatting with emphasis."""
        content = {
            'title': 'Emphasis Document',
            'content': 'This document contains **bold text**, *italic text*, and ***bold italic text***.',
            'highlighted': 'This text is ==highlighted==.',
            'strikethrough': 'This text is ~~struck through~~.'
        }
        
        result = markdown_formatter.format('markdown', content)
        
        assert result is not None
        assert "**bold text**" in result
        assert "*italic text*" in result
        assert "***bold italic text***" in result
        assert "==highlighted==" in result
        assert "~~struck through~~" in result
    
    def test_format_markdown_with_metadata(self, markdown_formatter):
        """Test markdown formatting with metadata."""
        content = {
            'title': 'Metadata Document',
            'metadata': {
                'author': 'John Doe',
                'date': '2024-01-01',
                'tags': ['markdown', 'documentation', 'test'],
                'description': 'A test document with metadata',
                'version': '1.0.0'
            },
            'content': 'This document has metadata.'
        }
        
        result = markdown_formatter.format('markdown', content)
        
        assert result is not None
        assert "author: John Doe" in result
        assert "date: 2024-01-01" in result
        assert "tags: markdown, documentation, test" in result
        assert "description: A test document with metadata" in result
        assert "version: 1.0.0" in result
    
    def test_format_markdown_with_footnotes(self, markdown_formatter):
        """Test markdown formatting with footnotes."""
        content = {
            'title': 'Footnote Document',
            'content': 'This document contains footnotes[^1] and more footnotes[^2].',
            'footnotes': [
                'This is the first footnote.',
                'This is the second footnote with **bold text**.'
            ]
        }
        
        result = markdown_formatter.format('markdown', content)
        
        assert result is not None
        assert "footnotes[^1]" in result
        assert "footnotes[^2]" in result
        assert "[^1]: This is the first footnote." in result
        assert "[^2]: This is the second footnote with **bold text**." in result
    
    def test_format_markdown_with_toc(self, markdown_formatter):
        """Test markdown formatting with table of contents."""
        content = {
            'title': 'TOC Document',
            'toc': True,
            'sections': [
                {'heading': 'Introduction', 'content': 'Introduction content'},
                {'heading': 'Methods', 'content': 'Methods content'},
                {'heading': 'Results', 'content': 'Results content'},
                {'heading': 'Conclusion', 'content': 'Conclusion content'}
            ]
        }
        
        result = markdown_formatter.format('markdown', content)
        
        assert result is not None
        assert "## Table of Contents" in result
        assert "- [Introduction](#introduction)" in result
        assert "- [Methods](#methods)" in result
        assert "- [Results](#results)" in result
        assert "- [Conclusion](#conclusion)" in result
    
    def test_format_markdown_with_complex_structure(self, markdown_formatter):
        """Test markdown formatting with complex document structure."""
        content = {
            'title': 'Complex Document',
            'metadata': {
                'author': 'Complex Author',
                'date': '2024-01-01'
            },
            'abstract': 'This is the abstract of the document.',
            'sections': [
                {
                    'heading': 'Introduction',
                    'content': 'Introduction content with **bold** and *italic* text.',
                    'subsections': [
                        {
                            'heading': 'Background',
                            'content': 'Background information.',
                            'code': 'print("Hello, World!")'
                        }
                    ]
                },
                {
                    'heading': 'Methods',
                    'content': 'Methods section content.',
                    'tables': [
                        {
                            'headers': ['Method', 'Description'],
                            'rows': [['Method 1', 'Description 1'], ['Method 2', 'Description 2']]
                        }
                    ]
                },
                {
                    'heading': 'Results',
                    'content': 'Results section content.',
                    'images': [
                        {'alt': 'Result Chart', 'src': 'chart.png', 'caption': 'Results chart'}
                    ]
                }
            ],
            'references': [
                {'author': 'Author 1', 'title': 'Paper 1', 'year': '2023'},
                {'author': 'Author 2', 'title': 'Paper 2', 'year': '2024'}
            ]
        }
        
        result = markdown_formatter.format('markdown', content)
        
        assert result is not None
        assert "# Complex Document" in result
        assert "author: Complex Author" in result
        assert "## Abstract" in result
        assert "This is the abstract of the document." in result
        assert "## Introduction" in result
        assert "**bold**" in result
        assert "*italic*" in result
        assert "### Background" in result
        assert "print(\"Hello, World!\")" in result
        assert "## Methods" in result
        assert "| Method | Description |" in result
        assert "## Results" in result
        assert "![Result Chart](chart.png)" in result
        assert "Results chart" in result
        assert "## References" in result
        assert "Author 1" in result
        assert "Author 2" in result
    
    def test_format_markdown_error_handling(self, markdown_formatter):
        """Test error handling in markdown formatting."""
        # Test with invalid content structure
        content = {
            'title': 'Error Test',
            'invalid_key': object()  # Non-serializable object
        }
        
        result = markdown_formatter.format('markdown', content)
        
        # Should handle gracefully
        assert result is not None
        assert "# Error Test" in result


class TestFormatterIntegration:
    """Integration tests for formatters."""
    
    def test_formatter_with_real_content(self):
        """Test formatter with realistic content structure."""
        formatter = MarkdownFormatter()
        
        # Simulate content from a real document
        content = {
            'title': 'Research Paper',
            'metadata': {
                'author': 'Dr. Smith',
                'institution': 'University of Science',
                'date': '2024-01-15',
                'keywords': ['research', 'science', 'analysis']
            },
            'abstract': 'This paper presents a comprehensive analysis of the topic.',
            'sections': [
                {
                    'heading': 'Introduction',
                    'content': 'The introduction provides background information.',
                    'subsections': [
                        {'heading': 'Problem Statement', 'content': 'The problem is...'},
                        {'heading': 'Objectives', 'content': 'The objectives are...'}
                    ]
                },
                {
                    'heading': 'Methodology',
                    'content': 'The methodology section describes the approach.',
                    'code_blocks': [
                        {
                            'language': 'python',
                            'code': 'import pandas as pd\n\ndf = pd.read_csv("data.csv")'
                        }
                    ]
                },
                {
                    'heading': 'Results',
                    'content': 'The results show significant findings.',
                    'tables': [
                        {
                            'headers': ['Metric', 'Value', 'Unit'],
                            'rows': [
                                ['Accuracy', '95.2', '%'],
                                ['Precision', '94.8', '%'],
                                ['Recall', '95.6', '%']
                            ]
                        }
                    ]
                }
            ],
            'conclusion': 'The study concludes with important findings.',
            'references': [
                {'author': 'Johnson et al.', 'title': 'Previous Work', 'year': '2023'},
                {'author': 'Williams', 'title': 'Related Study', 'year': '2024'}
            ]
        }
        
        result = formatter.format('markdown', content)
        
        assert result is not None
        
        # Check key elements are present
        assert "# Research Paper" in result
        assert "author: Dr. Smith" in result
        assert "## Abstract" in result
        assert "## Introduction" in result
        assert "### Problem Statement" in result
        assert "## Methodology" in result
        assert "```python" in result
        assert "## Results" in result
        assert "| Metric | Value | Unit |" in result
        assert "## Conclusion" in result
        assert "## References" in result
        assert "Johnson et al." in result 