#!/usr/bin/env python3
"""
Simple CLI for converting documents to Markdown.

This script provides a command-line interface for the markdown converter.
It demonstrates how to use the ConversionEngine from the command line.
"""

import argparse
import sys
from pathlib import Path
from typing import List

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.markdown_converter.core import MainConverter


def find_supported_files(directory: Path) -> List[Path]:
    """
    Find all supported files in a directory.
    
    :param directory: Directory to search
    :return: List of supported file paths
    """
    supported_extensions = [
        '.docx', '.doc', '.pdf', '.html', '.htm', '.xlsx', '.xls',
        '.odt', '.rtf', '.epub', '.txt', '.md', '.msg', '.eml'
    ]
    
    files = []
    for ext in supported_extensions:
        files.extend(directory.rglob(f"*{ext}"))
    
    # Filter out hidden files and ensure files are readable
    filtered_files = []
    for file_path in files:
        if not any(part.startswith('.') for part in file_path.parts):
            if file_path.is_file() and file_path.stat().st_size < 100 * 1024 * 1024:  # 100MB limit
                filtered_files.append(file_path)
    
    return sorted(filtered_files)


def convert_single_file(input_path: str, output_path: str = None) -> bool:
    """
    Convert a single file to markdown.
    
    :param input_path: Path to input file
    :param output_path: Path to output file (optional)
    :return: True if conversion was successful
    """
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"❌ Input file does not exist: {input_path}")
        return False
    
    if output_path is None:
        output_file = input_file.with_suffix('.md')
    else:
        output_file = Path(output_path)
    
    converter = MainConverter()
    
    try:
        print(f"🔄 Converting {input_file} to {output_file}...")
        result = converter.convert_file(input_file, output_file)
        
        if result.success:
            print(f"✅ Successfully converted {input_file} to {output_file}")
            return True
        else:
            print(f"❌ Conversion failed: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False


def convert_directory(input_dir: str, output_dir: str = None) -> bool:
    """
    Convert all supported files in a directory.
    
    :param input_dir: Path to input directory
    :param output_dir: Path to output directory (optional)
    :return: True if all conversions were successful
    """
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"❌ Input directory does not exist: {input_dir}")
        return False
    
    if not input_path.is_dir():
        print(f"❌ Input path is not a directory: {input_dir}")
        return False
    
    if output_dir is None:
        output_path = Path(f"{input_dir}_converted")
    else:
        output_path = Path(output_dir)
    
    converter = MainConverter()
    
    try:
        # Find all supported files
        files = find_supported_files(input_path)
        
        if not files:
            print(f"❌ No supported files found in {input_dir}")
            return False
        
        print(f"🔄 Found {len(files)} files to convert...")
        
        # Convert files in batch
        # Note: MainConverter doesn't have batch_convert, so we'll convert one by one
        results = []
        for file_path in files:
            try:
                output_file = output_path / f"{file_path.stem}.md"
                result = converter.convert_file(file_path, output_file)
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
        
    except Exception as e:
        print(f"❌ Directory conversion failed: {e}")
        return False


def show_supported_formats():
    """Show supported input and output formats."""
    converter = MainConverter()
    formats = converter.get_supported_formats()
    
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