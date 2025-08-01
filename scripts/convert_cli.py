#!/usr/bin/env python3
"""
Simple CLI for converting documents to Markdown.

This script provides a command-line interface for the markdown converter.
It demonstrates how to use the ConversionEngine from the command line.
"""

import argparse
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.markdown_converter.core import ConversionEngine, FilesystemManager


def convert_single_file(input_path: str, output_path: str = None) -> bool:
    """
    Convert a single file to markdown.
    
    :param input_path: Path to input file
    :param output_path: Path to output file (optional)
    :return: True if conversion successful, False otherwise
    """
    if not Path(input_path).exists():
        print(f"❌ Input file does not exist: {input_path}")
        return False
    
    # Generate output path if not provided
    if output_path is None:
        input_file = Path(input_path)
        output_path = str(input_file.with_suffix('.md'))
    
    engine = ConversionEngine()
    
    try:
        result = engine.convert_document(input_path, output_path)
        print(f"✅ Successfully converted {input_path} to {output_path}")
        return True
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False


def convert_directory(input_dir: str, output_dir: str = None) -> bool:
    """
    Convert all supported files in a directory.
    
    :param input_dir: Input directory path
    :param output_dir: Output directory path (optional)
    :return: True if all conversions successful, False otherwise
    """
    if not Path(input_dir).exists():
        print(f"❌ Input directory does not exist: {input_dir}")
        return False
    
    # Generate output directory if not provided
    if output_dir is None:
        output_dir = f"{input_dir}_converted"
    
    fs_manager = FilesystemManager()
    engine = ConversionEngine()
    
    try:
        # Find all supported files
        files = fs_manager.find_files(input_dir)
        
        if not files:
            print(f"❌ No supported files found in {input_dir}")
            return False
        
        print(f"🔄 Found {len(files)} files to convert...")
        
        # Convert files in batch
        results = engine.batch_convert(files, output_dir)
        
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
        
    except Exception as e:
        print(f"❌ Directory conversion failed: {e}")
        return False


def show_supported_formats():
    """Show supported input and output formats."""
    engine = ConversionEngine()
    formats = engine.pandoc_engine.get_supported_formats()
    
    print("📋 Supported Formats:")
    print("   Input formats:")
    for fmt in formats["input"]:
        print(f"     - {fmt}")
    print("   Output formats:")
    for fmt in formats["output"]:
        print(f"     - {fmt}")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Convert documents to Markdown using the markdown converter engine.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.html                    # Convert single file
  %(prog)s document.html -o output.md       # Convert with custom output
  %(prog)s -d input_folder                  # Convert all files in directory
  %(prog)s -d input_folder -o output_dir   # Convert with custom output dir
  %(prog)s --formats                        # Show supported formats
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument("input", nargs="?", help="Input file path")
    input_group.add_argument("-d", "--directory", help="Input directory path")
    
    # Output options
    parser.add_argument("-o", "--output", help="Output file or directory path")
    
    # Other options
    parser.add_argument("--formats", action="store_true", help="Show supported formats")
    
    args = parser.parse_args()
    
    # Show formats if requested
    if args.formats:
        show_supported_formats()
        return
    
    # Check if input is provided
    if not args.input and not args.directory:
        parser.print_help()
        return
    
    # Convert based on input type
    if args.input:
        success = convert_single_file(args.input, args.output)
    elif args.directory:
        success = convert_directory(args.directory, args.output)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 