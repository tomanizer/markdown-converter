"""
File Converter Utility

This module provides utilities for converting binary file formats to readable formats
that can be processed by our parsers. Handles cases like .xlsb -> .xlsx, .doc -> .docx, etc.
"""

import logging
import platform
import subprocess
from pathlib import Path
from typing import Optional, Union

from .exceptions import ConversionError


class FileConverter:
    """
    Utility for converting binary file formats to readable formats.

    Handles conversion of binary formats like .xlsb, .doc, .ppt to their
    XML-based equivalents (.xlsx, .docx, .pptx) that can be read by our parsers.
    """

    def __init__(self) -> None:
        """Initialize the file converter."""
        self.logger = logging.getLogger("FileConverter")
        self._check_dependencies()

    def _check_dependencies(self) -> None:
        """Check if required dependencies are available."""
        # Check Microsoft Office (highest priority)
        self.ms_office_available = self._check_ms_office()
        if self.ms_office_available:
            self.logger.info("Microsoft Office available for file conversion")

        # Check LibreOffice
        self.libreoffice_available = self._check_libreoffice()
        if not self.libreoffice_available:
            self.logger.warning("LibreOffice not available for file conversion")

        # Check Pandoc
        self.pandoc_available = self._check_pandoc()
        if not self.pandoc_available:
            self.logger.warning("Pandoc not available for file conversion")

    def _check_ms_office(self) -> bool:
        """Check if Microsoft Office is available."""
        system = platform.system()

        if system == "Windows":
            return self._check_ms_office_windows()
        elif system == "Darwin":  # macOS
            return self._check_ms_office_macos()
        else:  # Linux
            return self._check_ms_office_linux()

    def _check_ms_office_windows(self) -> bool:
        """Check Microsoft Office availability on Windows."""
        try:
            import win32com.client

            # Try to create Excel application
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Quit()
            return True
        except Exception:
            return False

    def _check_ms_office_macos(self) -> bool:
        """Check Microsoft Office availability on macOS."""
        try:
            # Check if Microsoft Office apps are installed
            office_apps = [
                "/Applications/Microsoft Excel.app",
                "/Applications/Microsoft Word.app",
                "/Applications/Microsoft PowerPoint.app",
            ]

            for app in office_apps:
                if Path(app).exists():
                    return True

            return False
        except Exception:
            return False

    def _check_ms_office_linux(self) -> bool:
        """Check Microsoft Office availability on Linux."""
        # Microsoft Office is not typically available on Linux
        return False

    def _check_libreoffice(self) -> bool:
        """Check if LibreOffice is available."""
        try:
            # Try common locations
            common_paths = [
                "/usr/bin/libreoffice",
                "/usr/bin/soffice",
                "/Applications/LibreOffice.app/Contents/MacOS/soffice",
                "C:\\Program Files\\LibreOffice\\program\\soffice.exe",
            ]

            for path in common_paths:
                if Path(path).exists():
                    return True

            # Try to find in PATH
            result = subprocess.run(
                ["which", "libreoffice"], capture_output=True, text=True
            )
            if result.returncode == 0:
                return True

            result = subprocess.run(
                ["which", "soffice"], capture_output=True, text=True
            )
            return result.returncode == 0

        except Exception:
            return False

    def _check_pandoc(self) -> bool:
        """Check if Pandoc is available."""
        try:
            result = subprocess.run(
                ["pandoc", "--version"], capture_output=True, text=True
            )
            return result.returncode == 0
        except Exception:
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
            ".xlsb",  # Excel Binary
            ".doc",  # Word Binary
            ".xls",  # Excel 97-2003
            ".rtf",  # Rich Text Format
            ".odt",  # OpenDocument Text
            ".ods",  # OpenDocument Spreadsheet
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
            ".xlsb": ".xlsx",  # Excel Binary -> Excel XML
            ".xls": ".xlsx",  # Excel 97-2003 -> Excel XML
            ".doc": ".docx",  # Word Binary -> Word XML
            ".rtf": ".docx",  # Rich Text -> Word XML
            ".odt": ".docx",  # OpenDocument Text -> Word XML
            ".ods": ".xlsx",  # OpenDocument Spreadsheet -> Excel XML
        }

        return format_mapping.get(extension, extension)

    def convert_file(
        self,
        file_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
    ) -> Path:
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
            # Try Microsoft Office first (best quality)
            if self.ms_office_available:
                try:
                    return self._convert_with_ms_office(file_path, output_path)
                except Exception as e:
                    self.logger.warning(f"Microsoft Office conversion failed: {e}")

            # Try LibreOffice as fallback
            if self.libreoffice_available:
                try:
                    return self._convert_with_libreoffice(file_path, output_path)
                except Exception as e:
                    self.logger.warning(f"LibreOffice conversion failed: {e}")

            # Try Pandoc as last resort
            if self.pandoc_available:
                try:
                    return self._convert_with_pandoc(file_path, output_path)
                except Exception as e:
                    self.logger.warning(f"Pandoc conversion failed: {e}")

            raise ConversionError(f"No conversion method available for {file_path}")

        except Exception as e:
            raise ConversionError(f"Failed to convert {file_path}: {e}")

    def _convert_with_ms_office(self, input_path: Path, output_path: Path) -> Path:
        """
        Convert file using Microsoft Office.

        :param input_path: Path to input file
        :param output_path: Path to output file
        :return: Path to converted file
        """
        system = platform.system()

        if system == "Windows":
            return self._convert_with_ms_office_windows(input_path, output_path)
        elif system == "Darwin":  # macOS
            return self._convert_with_ms_office_macos(input_path, output_path)
        else:
            raise ConversionError(
                "Microsoft Office conversion not supported on this platform"
            )

    def _convert_with_ms_office_windows(
        self, input_path: Path, output_path: Path
    ) -> Path:
        """Convert file using Microsoft Office on Windows via COM automation."""
        try:
            import win32com.client

            file_extension = input_path.suffix.lower()

            if file_extension in [".xls", ".xlsb"]:
                # Use Excel
                excel = win32com.client.Dispatch("Excel.Application")
                excel.Visible = False
                excel.DisplayAlerts = False

                try:
                    # Open the workbook
                    workbook = excel.Workbooks.Open(str(input_path.absolute()))

                    # Save as new format
                    if output_path.suffix.lower() == ".xlsx":
                        workbook.SaveAs(
                            str(output_path.absolute()), FileFormat=51
                        )  # xlOpenXMLWorkbook
                    else:
                        workbook.SaveAs(str(output_path.absolute()))

                    workbook.Close()

                finally:
                    excel.Quit()

            elif file_extension in [".doc", ".rtf"]:
                # Use Word
                word = win32com.client.Dispatch("Word.Application")
                word.Visible = False
                word.DisplayAlerts = False

                try:
                    # Open the document
                    doc = word.Documents.Open(str(input_path.absolute()))

                    # Save as new format
                    if output_path.suffix.lower() == ".docx":
                        doc.SaveAs2(
                            str(output_path.absolute()), FileFormat=16
                        )  # wdFormatDocumentDefault
                    else:
                        doc.SaveAs(str(output_path.absolute()))

                    doc.Close()

                finally:
                    word.Quit()

            else:
                raise ConversionError(
                    f"Unsupported file format for MS Office conversion: {file_extension}"
                )

            if not output_path.exists():
                raise ConversionError(
                    f"Microsoft Office did not create output file: {output_path}"
                )

            self.logger.info(
                f"Successfully converted {input_path} to {output_path} using Microsoft Office"
            )
            return output_path

        except Exception as e:
            raise ConversionError(f"Microsoft Office conversion failed: {e}")

    def _convert_with_ms_office_macos(
        self, input_path: Path, output_path: Path
    ) -> Path:
        """Convert file using Microsoft Office on macOS via AppleScript."""
        try:
            file_extension = input_path.suffix.lower()

            if file_extension in [".xls", ".xlsb"]:
                # Use Excel via AppleScript
                script = f"""
                tell application "Microsoft Excel"
                    open POSIX file "{input_path.absolute()}"
                    set activeWorkbook to active workbook
                    save activeWorkbook as active workbook in POSIX file "{output_path.absolute()}"
                    close activeWorkbook
                end tell
                """

            elif file_extension in [".doc", ".rtf"]:
                # Use Word via AppleScript
                script = f"""
                tell application "Microsoft Word"
                    open POSIX file "{input_path.absolute()}"
                    set activeDocument to active document
                    save activeDocument as active document in POSIX file "{output_path.absolute()}"
                    close activeDocument
                end tell
                """

            else:
                raise ConversionError(
                    f"Unsupported file format for MS Office conversion: {file_extension}"
                )

            # Execute AppleScript
            result = subprocess.run(
                ["osascript", "-e", script], capture_output=True, text=True, timeout=60
            )

            if result.returncode != 0:
                raise ConversionError(f"AppleScript conversion failed: {result.stderr}")

            if not output_path.exists():
                raise ConversionError(
                    f"Microsoft Office did not create output file: {output_path}"
                )

            self.logger.info(
                f"Successfully converted {input_path} to {output_path} using Microsoft Office"
            )
            return output_path

        except Exception as e:
            raise ConversionError(f"Microsoft Office conversion failed: {e}")

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
            "libreoffice",
            "--headless",
            "--convert-to",
            self._get_libreoffice_format(output_path),
            "--outdir",
            str(output_path.parent),
            str(input_path),
        ]

        # Run conversion
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode != 0:
            raise ConversionError(f"LibreOffice conversion failed: {result.stderr}")

        # Check if output file exists
        if not output_path.exists():
            raise ConversionError(
                f"LibreOffice did not create output file: {output_path}"
            )

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
        cmd = ["pandoc", str(input_path), "-o", str(output_path)]

        # Run conversion
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

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
            ".xlsx": "Calc MS Excel 2007 XML",
            ".docx": "MS Word 2007 XML",
        }

        return format_mapping.get(extension, "Calc MS Excel 2007 XML")
