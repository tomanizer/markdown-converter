#!/usr/bin/env python3
"""
CLI Example - Using the Markdown Converter from Command Line

This example demonstrates how to use the markdown converter CLI
for single file and batch conversions.
"""

import os
import sys
from pathlib import Path

# Add the project root to the path so we can import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.markdown_converter.core.converter import (
    ConversionResult,
    DirectoryConversionResult,
    MainConverter,
)
from src.markdown_converter.core.exceptions import ConversionError


def example_single_file_conversion():
    """Example of single file conversion."""
    print("=== Single File Conversion Example ===")

    # Create converter
    converter = MainConverter()

    # Example file path (you would use your actual file)
    input_file = Path("test_documents/sample_report.docx")
    output_file = Path("output/sample_report.md")

    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        return

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Convert the file
        result = converter.convert_file(input_file, output_file)

        if result.success:
            print(f"✅ Successfully converted {input_file} to {output_file}")
            print(f"   File size: {result.file_size_mb:.2f} MB")
            print(f"   Processing time: {result.processing_time:.2f} seconds")
        else:
            print(f"❌ Conversion failed: {result.error_message}")

    except Exception as e:
        print(f"❌ Error during conversion: {e}")


def example_batch_conversion():
    """Example of batch directory conversion."""
    print("\n=== Batch Conversion Example ===")

    # Create converter
    converter = MainConverter()

    # Example directory paths
    input_dir = Path("test_documents")
    output_dir = Path("output/batch_converted")

    if not input_dir.exists():
        print(f"❌ Input directory not found: {input_dir}")
        return

    try:
        # Convert all files in the directory
        result = converter.convert_directory(
            input_dir=input_dir,
            output_dir=output_dir,
            max_workers=2,  # Use 2 worker processes
            continue_on_error=True
        )

        # Print results
        print(f"📊 Batch Conversion Results:")
        print(f"   Total files: {result.total_files}")
        print(f"   Processed: {result.processed_files}")
        print(f"   Failed: {result.failed_files}")
        print(f"   Skipped: {result.skipped_files}")
        print(f"   Processing time: {result.processing_time:.2f} seconds")

        if result.failed_files > 0:
            print(f"⚠️  {result.failed_files} files failed to convert")
        else:
            print("✅ All files converted successfully!")

    except Exception as e:
        print(f"❌ Error during batch conversion: {e}")


def example_cli_usage():
    """Example of how to use the CLI programmatically."""
    print("\n=== CLI Usage Example ===")

    # Example of how the CLI would be used
    print("To use the CLI, you would run commands like:")
    print("  python -m src.markdown_converter.cli convert input.docx output.md")
    print("  python -m src.markdown_converter.cli batch input_dir output_dir")
    print("  python -m src.markdown_converter.cli --help")


def example_config_usage():
    """Example of configuration usage."""
    print("\n=== Configuration Example ===")

    # Example configuration
    config = {
        'max_workers': 4,
        'max_memory_mb': 2048,
        'batch_size': 100,
        'output_format': 'markdown',
        'preserve_structure': True
    }

    print("Configuration options:")
    for key, value in config.items():
        print(f"  {key}: {value}")

    print("\nYou can also use environment variables:")
    print("  MDC_MAX_WORKERS=4")
    print("  MDC_MAX_MEMORY_MB=2048")
    print("  MDC_OUTPUT_FORMAT=markdown")


if __name__ == "__main__":
    print("🚀 Markdown Converter CLI Examples")
    print("=" * 50)

    # Run examples
    example_single_file_conversion()
    example_batch_conversion()
    example_cli_usage()
    example_config_usage()

    print("\n✨ Examples completed!")
