#!/usr/bin/env python3
"""
Example: Using the Python API to convert a document to Markdown.

This example demonstrates how to use the ConversionEngine to convert
various document formats to clean, readable markdown.
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.markdown_converter.core import MainConverter


def convert_single_file():
    """Convert a single file to markdown."""
    # Path to your test document (change as needed)
    input_file = "test_documents/simple_test.html"
    output_file = "test_documents/simple_test.md"

    # Initialize the conversion engine
    converter = MainConverter()

    # Convert the document
    try:
        result = converter.convert_document(input_file, output_file)
        print("✅ Conversion successful!")
        print("Markdown output (first 20 lines):")
        print("\n".join(result.splitlines()[:20]))
        print(f"\nSaved to: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False


def convert_multiple_files():
    """Convert multiple files in batch."""
    # List of test files to convert
    test_files = [
        "test_documents/simple_test.html",
        "test_documents/simple_test.txt",
        "test_documents/comprehensive_test.html",
        "test_documents/comprehensive_test.txt",
    ]
    
    # Filter to only existing files
    existing_files = [f for f in test_files if Path(f).exists()]
    
    if not existing_files:
        print("❌ No test files found!")
        return False

    converter = MainConverter()
    output_dir = Path("test_documents/converted")
    output_dir.mkdir(exist_ok=True)

    print(f"🔄 Converting {len(existing_files)} files...")
    
    # Convert files in batch
    # Note: MainConverter doesn't have batch_convert, so we'll convert one by one
    results = []
    for file_path in existing_files:
        try:
            output_file = output_dir / f"{Path(file_path).stem}.md"
            result = converter.convert_document(file_path, str(output_file))
            results.append({
                'input_file': file_path,
                'output_file': str(output_file),
                'success': True,
                'content': result,
                'error': None
            })
        except Exception as e:
            results.append({
                'input_file': file_path,
                'output_file': None,
                'success': False,
                'content': None,
                'error': str(e)
            })
    
    # Report results
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"\n📊 Conversion Results:")
    print(f"   ✅ Successful: {len(successful)}")
    print(f"   ❌ Failed: {len(failed)}")
    
    if successful:
        print(f"\n✅ Successfully converted files:")
        for result in successful:
            print(f"   - {result['input_file']} -> {result['output_file']}")
    
    if failed:
        print(f"\n❌ Failed conversions:")
        for result in failed:
            print(f"   - {result['input_file']}: {result['error']}")
    
    return len(failed) == 0


def show_engine_info():
    """Show information about the conversion engine."""
    converter = MainConverter()
    
    print("🔧 Conversion Engine Information:")
    print(f"   - Main Converter: {type(converter).__name__}")
    print(f"   - Supported formats: {converter.get_supported_formats()}")


def main():
    """Main function to demonstrate the conversion engine."""
    print("🚀 Markdown Converter - Python API Example")
    print("=" * 50)
    
    # Show engine information
    show_engine_info()
    print()
    
    # Convert single file
    print("📄 Single File Conversion:")
    success1 = convert_single_file()
    print()
    
    # Convert multiple files
    print("📁 Batch File Conversion:")
    success2 = convert_multiple_files()
    print()
    
    # Summary
    if success1 and success2:
        print("🎉 All conversions completed successfully!")
    else:
        print("⚠️  Some conversions failed. Check the output above for details.")


if __name__ == "__main__":
    main() 