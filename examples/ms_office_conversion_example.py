"""
Microsoft Office Conversion Example

This example demonstrates how the FileConverter can use Microsoft Office
applications for high-quality file format conversion.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.markdown_converter.core.file_converter import FileConverter


def demonstrate_ms_office_conversion():
    """Demonstrate Microsoft Office conversion capabilities."""
    print("=== Microsoft Office File Conversion Demo ===")
    
    # Create converter
    converter = FileConverter()
    
    # Check available conversion methods
    print(f"Microsoft Office available: {converter.ms_office_available}")
    print(f"LibreOffice available: {converter.libreoffice_available}")
    print(f"Pandoc available: {converter.pandoc_available}")
    
    # Show conversion priority
    print("\n📋 Conversion Priority:")
    if converter.ms_office_available:
        print("  1. Microsoft Office (highest quality)")
    if converter.libreoffice_available:
        print("  2. LibreOffice (good quality)")
    if converter.pandoc_available:
        print("  3. Pandoc (basic conversion)")
    
    # Show supported formats
    print("\n📄 Supported Binary Formats:")
    binary_formats = ['.xlsb', '.xls', '.doc', '.rtf', '.odt', '.ods']
    for fmt in binary_formats:
        target = converter.get_target_format(f"test{fmt}")
        print(f"  {fmt} → {target}")
    
    # Example conversion (if test files exist)
    test_files = [
        "test_documents/data_analysis.xls",
        "test_documents/sample_report.doc",
        "test_documents/fsi-2018.xlsb"
    ]
    
    print("\n🔄 Testing Conversions:")
    for test_file in test_files:
        file_path = Path(test_file)
        if file_path.exists():
            print(f"  Testing: {file_path.name}")
            
            if converter.needs_conversion(file_path):
                try:
                    # Convert the file
                    converted_path = converter.convert_file(file_path)
                    print(f"    ✅ Converted to: {converted_path.name}")
                except Exception as e:
                    print(f"    ❌ Conversion failed: {e}")
            else:
                print(f"    ℹ️  No conversion needed")
        else:
            print(f"  ⚠️  Test file not found: {file_path}")


def show_platform_specific_info():
    """Show platform-specific Microsoft Office information."""
    import platform
    
    system = platform.system()
    print(f"\n💻 Platform: {system}")
    
    if system == "Windows":
        print("  Microsoft Office integration via COM automation")
        print("  Requires: pywin32 package")
        print("  Supports: Excel (.xls, .xlsb) and Word (.doc, .rtf)")
        
    elif system == "Darwin":  # macOS
        print("  Microsoft Office integration via AppleScript")
        print("  Requires: Microsoft Office apps installed")
        print("  Supports: Excel (.xls, .xlsb) and Word (.doc, .rtf)")
        
    else:  # Linux
        print("  Microsoft Office not typically available on Linux")
        print("  Fallback to LibreOffice or Pandoc")


def show_installation_instructions():
    """Show installation instructions for Microsoft Office integration."""
    print("\n📦 Installation Instructions:")
    print("  Windows:")
    print("    pip install pywin32>=306")
    print("    Ensure Microsoft Office is installed")
    print()
    print("  macOS:")
    print("    Install Microsoft Office from App Store or Microsoft website")
    print("    No additional Python packages needed")
    print()
    print("  Linux:")
    print("    Microsoft Office not available")
    print("    Use LibreOffice: sudo apt-get install libreoffice")


if __name__ == "__main__":
    print("🚀 Microsoft Office File Conversion Example")
    print("=" * 50)
    
    # Show platform info
    show_platform_specific_info()
    
    # Show installation instructions
    show_installation_instructions()
    
    # Demonstrate conversion
    demonstrate_ms_office_conversion()
    
    print("\n✨ Example completed!")
    print("\n💡 Tips:")
    print("  - Microsoft Office provides the highest quality conversions")
    print("  - LibreOffice is a good fallback option")
    print("  - Pandoc is the last resort for basic conversions")
    print("  - The converter automatically chooses the best available method") 