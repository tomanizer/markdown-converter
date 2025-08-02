#!/usr/bin/env python3
"""
Example: Using the Python API to convert a document to Markdown.

This example demonstrates how to use the MainConverter to convert
various document formats to clean, readable markdown.
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.markdown_converter.core.converter import MainConverter


def convert_single_file():
    """Convert a single file to markdown."""
    # Path to your test document (change as needed)
    input_file = "test_documents/simple_test.html"
    output_file = "test_documents/simple_test.md"

    # Initialize the conversion engine
    converter = MainConverter()

    # Convert the document
    try:
        result = converter.convert_file(input_file, output_file)
        if result.success:
            print("✅ Conversion successful!")
            print(f"Saved to: {output_file}")

            # Read and show the first 20 lines of output
            if Path(output_file).exists():
                content = Path(output_file).read_text()
                print("Markdown output (first 20 lines):")
                print("\n".join(content.splitlines()[:20]))
            return True
        else:
            print(f"❌ Conversion failed: {result.error_message}")
            return False
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

    # Convert files one by one
    results = []
    for file_path in existing_files:
        try:
            output_file = output_dir / f"{Path(file_path).stem}.md"
            result = converter.convert_file(file_path, str(output_file))
            results.append({
                'input_file': file_path,
                'output_file': str(output_file),
                'success': result.success,
                'error': result.error_message
            })
        except Exception as e:
            results.append({
                'input_file': file_path,
                'output_file': None,
                'success': False,
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


def convert_directory():
    """Convert all files in a directory."""
    converter = MainConverter()
    input_dir = Path("test_documents")
    output_dir = Path("test_documents/converted")

    if not input_dir.exists():
        print("❌ Input directory not found!")
        return False

    try:
        result = converter.convert_directory(input_dir, output_dir)

        print(f"\n📊 Directory Conversion Results:")
        print(f"   Total files: {result.total_files}")
        print(f"   Processed: {result.processed_files}")
        print(f"   Failed: {result.failed_files}")
        print(f"   Skipped: {result.skipped_files}")
        print(f"   Processing time: {result.processing_time:.2f} seconds")

        return result.failed_files == 0
    except Exception as e:
        print(f"❌ Directory conversion failed: {e}")
        return False


def show_converter_info():
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
    show_converter_info()
    print()

    # Convert single file
    print("📄 Single File Conversion:")
    success1 = convert_single_file()
    print()

    # Convert multiple files
    print("📁 Multiple File Conversion:")
    success2 = convert_multiple_files()
    print()

    # Convert directory
    print("📂 Directory Conversion:")
    success3 = convert_directory()
    print()

    # Summary
    if success1 and success2 and success3:
        print("🎉 All conversions completed successfully!")
    else:
        print("⚠️  Some conversions failed. Check the output above for details.")


if __name__ == "__main__":
    main()
