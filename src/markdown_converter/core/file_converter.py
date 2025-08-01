"""
File Converter Utility

This module provides utilities for converting binary file formats to readable formats
that can be processed by our parsers. Handles cases like .xlsb -> .xlsx, .doc -> .docx, etc.
"""

import logging
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import shutil

from .exceptions import ConversionError, UnsupportedFormatError


class FileConverter:
    """
    Utility for converting binary file formats to readable formats.
    
    Handles conversion of binary formats like .xlsb, .doc, .ppt to their
    XML-based equivalents (.xlsx, .docx, .pptx) that can be read by our parsers.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the file converter.
        
        :param config: Configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger("FileConverter")
        self._setup_default_config()
        self._validate_dependencies()
    
    def _setup_default_config(self) -> None:
        """Setup default configuration for file conversion."""
        self.default_config = {
            # Conversion settings
            "use_libreoffice": True,
            "use_pandoc": True,
            "use_python_converters": True,
            
            # LibreOffice settings
            "libreoffice_path": None,  # Auto-detect
            "libreoffice_timeout": 60,  # seconds
            "libreoffice_headless": True,
            
            # Pandoc settings
            "pandoc_timeout": 30,  # seconds
            
            # Output settings
            "preserve_original": True,
            "cleanup_temp_files": True,
            "output_dir": None,  # Use temp directory
        }
        
        # Merge with user config
        if self.config:
            self.default_config.update(self.config)
    
    def _validate_dependencies(self) -> None:
        """Validate that required dependencies are available."""
        # Check LibreOffice
        self.libreoffice_available = self._check_libreoffice()
        if not self.libreoffice_available:
            self.logger.warning("LibreOffice not available for file conversion")
        
        # Check Pandoc
        self.pandoc_available = self._check_pandoc()
        if not self.pandoc_available:
            self.logger.warning("Pandoc not available for file conversion")
        
        if not self.libreoffice_available and not self.pandoc_available:
            self.logger.warning("No file conversion tools available")
    
    def _check_libreoffice(self) -> bool:
        """Check if LibreOffice is available."""
        try:
            # Try to find LibreOffice
            if self.default_config["libreoffice_path"]:
                path = Path(self.default_config["libreoffice_path"])
                if path.exists() and path.is_file():
                    return True
            
            # Try common locations
            common_paths = [
                "/usr/bin/libreoffice",
                "/usr/bin/soffice",
                "/Applications/LibreOffice.app/Contents/MacOS/soffice",
                "C:\\Program Files\\LibreOffice\\program\\soffice.exe",
            ]
            
            for path in common_paths:
                if Path(path).exists():
                    self.default_config["libreoffice_path"] = path
                    return True
            
            # Try to find in PATH
            result = subprocess.run(
                ["which", "libreoffice"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                self.default_config["libreoffice_path"] = result.stdout.strip()
                return True
            
            result = subprocess.run(
                ["which", "soffice"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                self.default_config["libreoffice_path"] = result.stdout.strip()
                return True
            
            return False
        except Exception as e:
            self.logger.warning(f"Error checking LibreOffice: {e}")
            return False
    
    def _check_pandoc(self) -> bool:
        """Check if Pandoc is available."""
        try:
            result = subprocess.run(
                ["pandoc", "--version"], 
                capture_output=True, 
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            self.logger.warning(f"Error checking Pandoc: {e}")
            return False
    
    def needs_conversion(self, file_path: Union[str, Path]) -> bool:
        """
        Check if a file needs conversion before parsing.
        
        :param file_path: Path to the file
        :return: True if the file needs conversion
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        # Binary formats that need conversion
        binary_formats = {
            '.xlsb',  # Excel Binary
            '.doc',   # Word Binary
            '.ppt',   # PowerPoint Binary
            '.xls',   # Excel 97-2003
            '.rtf',   # Rich Text Format
            '.odt',   # OpenDocument Text
            '.ods',   # OpenDocument Spreadsheet
            '.odp',   # OpenDocument Presentation
        }
        
        return extension in binary_formats
    
    def get_target_format(self, file_path: Union[str, Path]) -> str:
        """
        Get the target format for conversion.
        
        :param file_path: Path to the file
        :return: Target file extension
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        # Mapping of binary formats to target formats
        format_mapping = {
            '.xlsb': '.xlsx',  # Excel Binary -> Excel XML
            '.xls': '.xlsx',    # Excel 97-2003 -> Excel XML
            '.doc': '.docx',    # Word Binary -> Word XML
            '.ppt': '.pptx',    # PowerPoint Binary -> PowerPoint XML
            '.rtf': '.docx',    # Rich Text -> Word XML
            '.odt': '.docx',    # OpenDocument Text -> Word XML
            '.ods': '.xlsx',    # OpenDocument Spreadsheet -> Excel XML
            '.odp': '.pptx',    # OpenDocument Presentation -> PowerPoint XML
        }
        
        return format_mapping.get(extension, extension)
    
    def convert_file(self, file_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None) -> Path:
        """
        Convert a binary file to a readable format.
        
        :param file_path: Path to the input file
        :param output_path: Path for the output file (optional)
        :return: Path to the converted file
        :raises: ConversionError if conversion fails
        """
        file_path = Path(file_path)
        
        if not self.needs_conversion(file_path):
            return file_path
        
        self.logger.info(f"Converting {file_path} to readable format")
        
        # Determine output path
        if output_path is None:
            target_format = self.get_target_format(file_path)
            output_path = file_path.with_suffix(target_format)
        
        output_path = Path(output_path)
        
        try:
            # Try LibreOffice first (most comprehensive)
            if self.libreoffice_available:
                try:
                    return self._convert_with_libreoffice(file_path, output_path)
                except Exception as e:
                    self.logger.warning(f"LibreOffice conversion failed: {e}")
            
            # Try Pandoc as fallback
            if self.pandoc_available:
                try:
                    return self._convert_with_pandoc(file_path, output_path)
                except Exception as e:
                    self.logger.warning(f"Pandoc conversion failed: {e}")
            
            raise ConversionError(f"No conversion method available for {file_path}")
            
        except Exception as e:
            self.logger.error(f"File conversion failed for {file_path}: {e}")
            raise ConversionError(f"Failed to convert {file_path}: {e}")
    
    def _convert_with_libreoffice(self, input_path: Path, output_path: Path) -> Path:
        """
        Convert file using LibreOffice.
        
        :param input_path: Path to input file
        :param output_path: Path to output file
        :return: Path to converted file
        """
        self.logger.debug(f"Using LibreOffice to convert {input_path}")
        
        # Prepare command
        cmd = [
            self.default_config["libreoffice_path"],
            "--headless" if self.default_config["libreoffice_headless"] else "",
            "--convert-to", self._get_libreoffice_format(output_path),
            "--outdir", str(output_path.parent),
            str(input_path)
        ]
        
        # Remove empty strings
        cmd = [arg for arg in cmd if arg]
        
        # Run conversion
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=self.default_config["libreoffice_timeout"]
        )
        
        if result.returncode != 0:
            raise ConversionError(f"LibreOffice conversion failed: {result.stderr}")
        
        # Check if output file exists
        if not output_path.exists():
            raise ConversionError(f"LibreOffice did not create output file: {output_path}")
        
        self.logger.info(f"Successfully converted {input_path} to {output_path}")
        return output_path
    
    def _convert_with_pandoc(self, input_path: Path, output_path: Path) -> Path:
        """
        Convert file using Pandoc.
        
        :param input_path: Path to input file
        :param output_path: Path to output file
        :return: Path to converted file
        """
        self.logger.debug(f"Using Pandoc to convert {input_path}")
        
        # Prepare command
        cmd = [
            "pandoc",
            str(input_path),
            "-o", str(output_path)
        ]
        
        # Run conversion
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=self.default_config["pandoc_timeout"]
        )
        
        if result.returncode != 0:
            raise ConversionError(f"Pandoc conversion failed: {result.stderr}")
        
        # Check if output file exists
        if not output_path.exists():
            raise ConversionError(f"Pandoc did not create output file: {output_path}")
        
        self.logger.info(f"Successfully converted {input_path} to {output_path}")
        return output_path
    
    def _get_libreoffice_format(self, output_path: Path) -> str:
        """
        Get LibreOffice format string for conversion.
        
        :param output_path: Path to output file
        :return: LibreOffice format string
        """
        extension = output_path.suffix.lower()
        
        format_mapping = {
            '.xlsx': 'Calc MS Excel 2007 XML',
            '.docx': 'MS Word 2007 XML',
            '.pptx': 'Impress MS PowerPoint 2007 XML',
            '.pdf': 'writer_pdf_Export',
            '.html': 'HTML (StarWriter)',
            '.txt': 'Text',
        }
        
        return format_mapping.get(extension, 'Calc MS Excel 2007 XML')
    
    def convert_directory(self, input_dir: Union[str, Path], output_dir: Optional[Union[str, Path]] = None) -> List[Path]:
        """
        Convert all files in a directory that need conversion.
        
        :param input_dir: Input directory path
        :param output_dir: Output directory path (optional)
        :return: List of converted file paths
        """
        input_dir = Path(input_dir)
        
        if output_dir is None:
            output_dir = input_dir / "converted"
        
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        converted_files = []
        
        for file_path in input_dir.iterdir():
            if file_path.is_file() and self.needs_conversion(file_path):
                try:
                    output_path = output_dir / file_path.name
                    converted_file = self.convert_file(file_path, output_path)
                    converted_files.append(converted_file)
                except Exception as e:
                    self.logger.error(f"Failed to convert {file_path}: {e}")
        
        return converted_files
    
    def get_supported_conversions(self) -> Dict[str, str]:
        """
        Get mapping of supported binary formats to target formats.
        
        :return: Dictionary mapping source formats to target formats
        """
        return {
            '.xlsb': '.xlsx',  # Excel Binary -> Excel XML
            '.xls': '.xlsx',    # Excel 97-2003 -> Excel XML
            '.doc': '.docx',    # Word Binary -> Word XML
            '.ppt': '.pptx',    # PowerPoint Binary -> PowerPoint XML
            '.rtf': '.docx',    # Rich Text -> Word XML
            '.odt': '.docx',    # OpenDocument Text -> Word XML
            '.ods': '.xlsx',    # OpenDocument Spreadsheet -> Excel XML
            '.odp': '.pptx',    # OpenDocument Presentation -> PowerPoint XML
        }
    
    def get_converter_info(self) -> Dict[str, Any]:
        """
        Get information about the file converter.
        
        :return: Dictionary with converter information
        """
        return {
            "name": "FileConverter",
            "description": "Utility for converting binary file formats to readable formats",
            "supported_conversions": self.get_supported_conversions(),
            "dependencies": {
                "libreoffice": self.libreoffice_available,
                "pandoc": self.pandoc_available
            },
            "config": self.default_config
        } 