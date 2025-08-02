"""
Markdown Formatter

This module provides a formatter specifically for markdown output.
"""

from typing import Dict, Any, Optional, List, Union
import re
from pathlib import Path

from .base import BaseFormatter
from ..core.exceptions import FormatterError


class MarkdownFormatter(BaseFormatter):
    """
    Formatter for markdown output with LLM optimization.
    
    This formatter handles the conversion of content to clean, readable markdown
    that is optimized for LLM processing.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the markdown formatter.
        
        :param config: Configuration dictionary
        """
        default_config = {
            'optimize_for_llm': True,
            'preserve_structure': True,
            'clean_whitespace': True,
            'add_toc': False,
            'max_line_length': 88,
            'preserve_links': True,
            'preserve_images': True,
            'preserve_tables': True,
            'preserve_code_blocks': True
        }
        
        if config:
            default_config.update(config)
        
        super().__init__(default_config)
    
    def can_format(self, output_type: str, content: Any) -> bool:
        """
        Check if this formatter can handle the given output type.
        
        :param output_type: Type of output
        :param content: The content to format
        :return: True if the formatter can handle this output type
        """
        return output_type.lower() in ['markdown', 'md', 'llm_optimized']
    
    def format(self, output_type: str, content: Any, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Format the content for markdown output.
        
        :param output_type: Type of output format
        :param content: The content to format
        :param context: Additional context information
        :return: Formatted markdown content
        :raises: FormatterError if formatting fails
        """
        try:
            self._log_formatting_start(output_type)
            
            # Convert content to string if it's not already
            if not isinstance(content, str):
                content = self._convert_content_to_string(content)
            
            # Apply markdown formatting
            formatted_content = self._apply_markdown_formatting(content)
            
            # Optimize for LLM if configured
            if self.config.get('optimize_for_llm', True):
                formatted_content = self._optimize_for_llm(formatted_content)
            
            # Add table of contents if requested
            if self.config.get('add_toc', False):
                formatted_content = self._add_table_of_contents(formatted_content)
            
            self._log_formatting_success(output_type)
            return formatted_content
            
        except Exception as e:
            self._log_formatting_error(output_type, e)
            raise FormatterError(f"Failed to format content for {output_type}: {e}")
    
    def get_supported_output_types(self) -> List[str]:
        """
        Get list of output types this formatter supports.
        
        :return: List of supported output types
        """
        return ['markdown', 'md', 'llm_optimized']
    
    def _convert_content_to_string(self, content: Any) -> str:
        """
        Convert various content types to string.
        
        :param content: Content to convert
        :return: String representation of content
        """
        if isinstance(content, str):
            return content
        elif isinstance(content, dict):
            return self._dict_to_markdown(content)
        elif isinstance(content, list):
            return self._list_to_markdown(content)
        else:
            return str(content)
    
    def _dict_to_markdown(self, content: Dict[str, Any]) -> str:
        """
        Convert dictionary to markdown format.
        
        :param content: Dictionary content
        :return: Markdown string
        """
        markdown_lines = []
        
        for key, value in content.items():
            if key == 'title':
                markdown_lines.append(f"# {value}")
            elif key == 'sections':
                markdown_lines.extend(self._format_sections(value))
            elif key == 'metadata':
                markdown_lines.extend(self._format_metadata(value))
            elif key == 'tables':
                markdown_lines.extend(self._format_tables(value))
            elif key == 'images':
                markdown_lines.extend(self._format_images(value))
            elif key == 'links':
                markdown_lines.extend(self._format_links(value))
            elif key == 'code_blocks':
                markdown_lines.extend(self._format_code_blocks(value))
            elif key == 'quotes':
                markdown_lines.extend(self._format_quotes(value))
            elif key == 'footnotes':
                markdown_lines.extend(self._format_footnotes(value))
            elif key == 'bullet_list':
                markdown_lines.extend(self._format_bullet_list(value))
            elif key == 'numbered_list':
                markdown_lines.extend(self._format_numbered_list(value))
            elif key == 'nested_list':
                markdown_lines.extend(self._format_nested_list(value))
            elif key == 'toc':
                if value:
                    markdown_lines.extend(self._add_table_of_contents_to_dict(content))
            elif key == 'abstract':
                markdown_lines.append("## Abstract")
                markdown_lines.append(str(value))
                markdown_lines.append("")
            elif key == 'conclusion':
                markdown_lines.append("## Conclusion")
                markdown_lines.append(str(value))
                markdown_lines.append("")
            elif key == 'references':
                markdown_lines.append("## References")
                markdown_lines.extend(self._format_references(value))
                markdown_lines.append("")
            else:
                markdown_lines.append(f"## {key.title()}")
                markdown_lines.append(str(value))
                markdown_lines.append("")
        
        return "\n".join(markdown_lines)
    
    def _list_to_markdown(self, content: List[Any]) -> str:
        """
        Convert list to markdown format.
        
        :param content: List content
        :return: Markdown string
        """
        markdown_lines = []
        
        for item in content:
            if isinstance(item, dict):
                markdown_lines.append(self._dict_to_markdown(item))
            elif isinstance(item, list):
                markdown_lines.extend([f"- {subitem}" for subitem in item])
            else:
                markdown_lines.append(f"- {item}")
        
        return "\n".join(markdown_lines)
    
    def _format_sections(self, sections: List[Dict[str, Any]]) -> List[str]:
        """
        Format sections as markdown.
        
        :param sections: List of section dictionaries
        :return: List of markdown lines
        """
        lines = []
        
        for section in sections:
            if 'heading' in section:
                lines.append(f"## {section['heading']}")
            
            if 'content' in section:
                lines.append(section['content'])
                lines.append("")
            
            if 'subsections' in section:
                for subsection in section['subsections']:
                    if 'heading' in subsection:
                        lines.append(f"### {subsection['heading']}")
                    if 'content' in subsection:
                        lines.append(subsection['content'])
                        lines.append("")
                    if 'code' in subsection:
                        lines.append(f"```")
                        lines.append(subsection['code'])
                        lines.append("```")
                        lines.append("")
            
            if 'tables' in section:
                lines.extend(self._format_tables(section['tables']))
            
            if 'images' in section:
                lines.extend(self._format_images(section['images']))
            
            if 'code_blocks' in section:
                lines.extend(self._format_code_blocks(section['code_blocks']))
        
        return lines
    
    def _format_metadata(self, metadata: Dict[str, Any]) -> List[str]:
        """
        Format metadata as markdown.
        
        :param metadata: Metadata dictionary
        :return: List of markdown lines
        """
        lines = []
        
        for key, value in metadata.items():
            if isinstance(value, list):
                lines.append(f"{key}: {', '.join(map(str, value))}")
            else:
                lines.append(f"{key}: {value}")
        
        if lines:
            lines.append("")
        
        return lines
    
    def _format_tables(self, tables: List[Dict[str, Any]]) -> List[str]:
        """
        Format tables as markdown.
        
        :param tables: List of table dictionaries
        :return: List of markdown lines
        """
        lines = []
        
        for table in tables:
            if 'headers' in table and 'rows' in table:
                # Add headers
                header_line = "| " + " | ".join(table['headers']) + " |"
                lines.append(header_line)
                
                # Add separator
                separator = "| " + " | ".join(["---"] * len(table['headers'])) + " |"
                lines.append(separator)
                
                # Add rows
                for row in table['rows']:
                    row_line = "| " + " | ".join(map(str, row)) + " |"
                    lines.append(row_line)
                
                lines.append("")
        
        return lines
    
    def _format_images(self, images: List[Dict[str, Any]]) -> List[str]:
        """
        Format images as markdown.
        
        :param images: List of image dictionaries
        :return: List of markdown lines
        """
        lines = []
        
        for image in images:
            if 'alt' in image and 'src' in image:
                image_markdown = f"![{image['alt']}]({image['src']})"
                lines.append(image_markdown)
                
                if 'caption' in image:
                    lines.append(f"*{image['caption']}*")
                
                lines.append("")
        
        return lines
    
    def _format_links(self, links: List[Dict[str, Any]]) -> List[str]:
        """
        Format links as markdown.
        
        :param links: List of link dictionaries
        :return: List of markdown lines
        """
        lines = []
        
        for link in links:
            if 'text' in link and 'url' in link:
                link_markdown = f"[{link['text']}]({link['url']})"
                lines.append(link_markdown)
        
        return lines
    
    def _format_code_blocks(self, code_blocks: List[Dict[str, Any]]) -> List[str]:
        """
        Format code blocks as markdown.
        
        :param code_blocks: List of code block dictionaries
        :return: List of markdown lines
        """
        lines = []
        
        for code_block in code_blocks:
            language = code_block.get('language', '')
            code = code_block.get('code', '')
            
            if language:
                lines.append(f"```{language}")
            else:
                lines.append("```")
            
            lines.append(code)
            lines.append("```")
            lines.append("")
        
        return lines
    
    def _format_quotes(self, quotes: List[str]) -> List[str]:
        """
        Format quotes as markdown.
        
        :param quotes: List of quote strings
        :return: List of markdown lines
        """
        lines = []
        
        for quote in quotes:
            # Handle multi-line quotes
            quote_lines = quote.split('\n')
            for line in quote_lines:
                lines.append(f"> {line}")
            lines.append("")
        
        return lines
    
    def _format_footnotes(self, footnotes: List[str]) -> List[str]:
        """
        Format footnotes as markdown.
        
        :param footnotes: List of footnote strings
        :return: List of markdown lines
        """
        lines = []
        
        for i, footnote in enumerate(footnotes, 1):
            lines.append(f"[^{i}]: {footnote}")
        
        return lines
    
    def _format_bullet_list(self, items: List[str]) -> List[str]:
        """
        Format bullet list as markdown.
        
        :param items: List of items
        :return: List of markdown lines
        """
        lines = []
        for item in items:
            lines.append(f"- {item}")
        lines.append("")
        return lines
    
    def _format_numbered_list(self, items: List[str]) -> List[str]:
        """
        Format numbered list as markdown.
        
        :param items: List of items
        :return: List of markdown lines
        """
        lines = []
        for i, item in enumerate(items, 1):
            lines.append(f"{i}. {item}")
        lines.append("")
        return lines
    
    def _format_nested_list(self, items: List[Any]) -> List[str]:
        """
        Format nested list as markdown.
        
        :param items: List of items (can be strings or nested lists)
        :return: List of markdown lines
        """
        lines = []
        for item in items:
            if isinstance(item, list):
                for subitem in item:
                    lines.append(f"  - {subitem}")
            else:
                lines.append(f"- {item}")
        lines.append("")
        return lines
    
    def _format_references(self, references: List[Dict[str, Any]]) -> List[str]:
        """
        Format references as markdown.
        
        :param references: List of reference dictionaries
        :return: List of markdown lines
        """
        lines = []
        for i, ref in enumerate(references, 1):
            if 'author' in ref and 'title' in ref:
                year = ref.get('year', '')
                lines.append(f"{i}. {ref['author']}, \"{ref['title']}\" ({year})")
            else:
                lines.append(f"{i}. {str(ref)}")
        return lines
    
    def _add_table_of_contents_to_dict(self, content: Dict[str, Any]) -> List[str]:
        """
        Add table of contents based on content structure.
        
        :param content: Content dictionary
        :return: List of markdown lines for TOC
        """
        lines = ["## Table of Contents", ""]
        
        # Add sections to TOC
        if 'sections' in content:
            for section in content['sections']:
                if 'heading' in section:
                    title = section['heading']
                    anchor = title.lower().replace(' ', '-').replace('_', '-')
                    lines.append(f"- [{title}](#{anchor})")
                    
                    # Add subsections
                    if 'subsections' in section:
                        for subsection in section['subsections']:
                            if 'heading' in subsection:
                                sub_title = subsection['heading']
                                sub_anchor = sub_title.lower().replace(' ', '-').replace('_', '-')
                                lines.append(f"  - [{sub_title}](#{sub_anchor})")
        
        lines.append("")
        return lines
    
    def _apply_markdown_formatting(self, content: str) -> str:
        """
        Apply markdown-specific formatting.
        
        :param content: Raw content
        :return: Formatted markdown content
        """
        # Clean up excessive whitespace
        if self.config.get('clean_whitespace', True):
            content = self._clean_whitespace(content)
        
        # Ensure proper heading structure
        if self.config.get('preserve_structure', True):
            content = self._ensure_proper_heading_structure(content)
        
        # Preserve links
        if self.config.get('preserve_links', True):
            content = self._preserve_links(content)
        
        # Preserve images
        if self.config.get('preserve_images', True):
            content = self._preserve_images(content)
        
        # Preserve tables
        if self.config.get('preserve_tables', True):
            content = self._preserve_tables(content)
        
        # Preserve code blocks
        if self.config.get('preserve_code_blocks', True):
            content = self._preserve_code_blocks(content)
        
        return content
    
    def _clean_whitespace(self, content: str) -> str:
        """
        Clean up excessive whitespace in content.
        
        :param content: Raw content
        :return: Cleaned content
        """
        # Remove trailing whitespace from lines
        lines = [line.rstrip() for line in content.split('\n')]
        
        # Remove excessive blank lines
        cleaned_lines = []
        prev_blank = False
        
        for line in lines:
            if line.strip() == "":
                if not prev_blank:
                    cleaned_lines.append(line)
                prev_blank = True
            else:
                cleaned_lines.append(line)
                prev_blank = False
        
        return "\n".join(cleaned_lines)
    
    def _preserve_links(self, content: str) -> str:
        """
        Ensure links are properly formatted.
        
        :param content: Content with links
        :return: Content with preserved links
        """
        # This is a placeholder - in a real implementation, you might
        # want to validate and fix link formatting
        return content
    
    def _preserve_images(self, content: str) -> str:
        """
        Ensure images are properly formatted.
        
        :param content: Content with images
        :return: Content with preserved images
        """
        # This is a placeholder - in a real implementation, you might
        # want to validate and fix image formatting
        return content
    
    def _preserve_tables(self, content: str) -> str:
        """
        Ensure tables are properly formatted.
        
        :param content: Content with tables
        :return: Content with preserved tables
        """
        # This is a placeholder - in a real implementation, you might
        # want to validate and fix table formatting
        return content
    
    def _preserve_code_blocks(self, content: str) -> str:
        """
        Ensure code blocks are properly formatted.
        
        :param content: Content with code blocks
        :return: Content with preserved code blocks
        """
        # This is a placeholder - in a real implementation, you might
        # want to validate and fix code block formatting
        return content
    
    def _add_table_of_contents(self, content: str) -> str:
        """
        Add a table of contents to the content.
        
        :param content: Markdown content
        :return: Content with table of contents
        """
        lines = content.split('\n')
        toc_lines = ["## Table of Contents", ""]
        
        for line in lines:
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                anchor = title.lower().replace(' ', '-').replace('_', '-')
                
                indent = "  " * (level - 1)
                toc_lines.append(f"{indent}- [{title}](#{anchor})")
        
        if len(toc_lines) > 2:  # More than just the header
            toc_lines.append("")
            return "\n".join(toc_lines) + content
        else:
            return content 