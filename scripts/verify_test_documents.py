#!/usr/bin/env python3
"""
Verify test documents for the markdown converter.

This script checks that all test documents are valid and can be processed
by the markdown converter components.
"""

import mimetypes
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))


def get_file_info(file_path: Path) -> Dict[str, Any]:
    """
    Get information about a file.

    :param file_path: Path to the file
    :return: Dictionary with file information
    """
    stat = file_path.stat()
    mime_type, _ = mimetypes.guess_type(str(file_path))

    return {
        "name": file_path.name,
        "size": stat.st_size,
        "mime_type": mime_type,
        "extension": file_path.suffix.lower(),
        "exists": file_path.exists(),
        "readable": os.access(file_path, os.R_OK)
    }


def verify_html_files(test_dir: Path) -> List[Dict[str, Any]]:
    """Verify HTML files can be parsed."""
    results = []

    for html_file in test_dir.glob("*.html"):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Basic HTML validation
            has_doctype = '<!DOCTYPE' in content
            has_html_tag = '<html' in content
            has_body_tag = '<body' in content
            has_head_tag = '<head' in content

            results.append({
                "file": html_file.name,
                "status": "✅ Valid",
                "size": len(content),
                "has_doctype": has_doctype,
                "has_html_tag": has_html_tag,
                "has_body_tag": has_body_tag,
                "has_head_tag": has_head_tag,
                "error": None
            })
        except Exception as e:
            results.append({
                "file": html_file.name,
                "status": "❌ Error",
                "error": str(e)
            })

    return results


def verify_text_files(test_dir: Path) -> List[Dict[str, Any]]:
    """Verify text files can be read."""
    results = []

    for text_file in test_dir.glob("*.txt"):
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Basic text analysis
            lines = content.split('\n')
            words = content.split()

            results.append({
                "file": text_file.name,
                "status": "✅ Valid",
                "size": len(content),
                "lines": len(lines),
                "words": len(words),
                "error": None
            })
        except Exception as e:
            results.append({
                "file": text_file.name,
                "status": "❌ Error",
                "error": str(e)
            })

    return results


def verify_csv_files(test_dir: Path) -> List[Dict[str, Any]]:
    """Verify CSV files can be parsed."""
    results = []

    for csv_file in test_dir.glob("*.csv"):
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            if lines and lines[0]:
                headers = lines[0].split(',')
                data_rows = [line for line in lines[1:] if line.strip()]
            else:
                headers = []
                data_rows = []

            results.append({
                "file": csv_file.name,
                "status": "✅ Valid",
                "size": len(content),
                "headers": len(headers),
                "data_rows": len(data_rows),
                "error": None
            })
        except Exception as e:
            results.append({
                "file": csv_file.name,
                "status": "❌ Error",
                "error": str(e)
            })

    return results


def verify_office_files(test_dir: Path) -> List[Dict[str, Any]]:
    """Verify Office files exist and have correct extensions."""
    results = []

    office_extensions = ['.docx', '.xlsx', '.msg']

    for ext in office_extensions:
        for file_path in test_dir.glob(f"*{ext}"):
            file_info = get_file_info(file_path)

            if file_info["exists"] and file_info["readable"]:
                results.append({
                    "file": file_path.name,
                    "status": "✅ Valid",
                    "size": file_info["size"],
                    "mime_type": file_info["mime_type"],
                    "error": None
                })
            else:
                results.append({
                    "file": file_path.name,
                    "status": "❌ Error",
                    "error": "File not readable or doesn't exist"
                })

    return results


def main() -> None:
    """Main function to verify test documents."""

    test_dir = Path("test_documents")

    if not test_dir.exists():
        print("❌ Test documents directory not found!")
        return

    print("🔍 Verifying test documents...")
    print(f"📁 Checking directory: {test_dir.absolute()}")
    print()

    # Get all files
    all_files = list(test_dir.glob("*"))
    print(f"📋 Found {len(all_files)} test files:")

    for file in sorted(all_files):
        file_info = get_file_info(file)
        status = "✅" if file_info["exists"] and file_info["readable"] else "❌"
        print(f"   {status} {file.name} ({file_info['size']} bytes)")

    print()

    # Verify by type
    print("🔍 Detailed verification by file type:")
    print()

    # HTML files
    html_results = verify_html_files(test_dir)
    if html_results:
        print("📄 HTML Files:")
        for result in html_results:
            print(f"   {result['status']} {result['file']}")
            if result.get('error'):
                print(f"      Error: {result['error']}")
        print()

    # Text files
    text_results = verify_text_files(test_dir)
    if text_results:
        print("📝 Text Files:")
        for result in text_results:
            print(f"   {result['status']} {result['file']} ({result.get('words', 0)} words)")
            if result.get('error'):
                print(f"      Error: {result['error']}")
        print()

    # CSV files
    csv_results = verify_csv_files(test_dir)
    if csv_results:
        print("📊 CSV Files:")
        for result in csv_results:
            print(f"   {result['status']} {result['file']} ({result.get('data_rows', 0)} rows)")
            if result.get('error'):
                print(f"      Error: {result['error']}")
        print()

    # Office files
    office_results = verify_office_files(test_dir)
    if office_results:
        print("📄 Office Files:")
        for result in office_results:
            print(f"   {result['status']} {result['file']} ({result.get('size', 0)} bytes)")
            if result.get('error'):
                print(f"      Error: {result['error']}")
        print()

    # Summary
    total_files = len(all_files)
    valid_files = sum(1 for file in all_files if get_file_info(file)["exists"] and get_file_info(file)["readable"])

    print("📊 Summary:")
    print(f"   Total files: {total_files}")
    print(f"   Valid files: {valid_files}")
    print(f"   Success rate: {(valid_files/total_files)*100:.1f}%")

    if valid_files == total_files:
        print("\n🎉 All test documents are ready for testing!")
    else:
        print(f"\n⚠️  {total_files - valid_files} files have issues.")


if __name__ == "__main__":
    main()
