#!/usr/bin/env python3
"""
Download sample documents from public sources for testing.

This script downloads sample documents in various formats from public repositories
and websites to provide realistic test cases for the markdown converter.
"""

import os
import sys
from pathlib import Path
import urllib.request
import urllib.error
from typing import Dict, List, Optional


def download_file(url: str, local_path: Path) -> bool:
    """
    Download a file from URL to local path.
    
    :param url: URL to download from
    :param local_path: Local path to save to
    :return: True if successful, False otherwise
    """
    try:
        print(f"📥 Downloading: {url}")
        urllib.request.urlretrieve(url, local_path)
        print(f"✅ Downloaded: {local_path}")
        return True
    except urllib.error.URLError as e:
        print(f"❌ Failed to download {url}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")
        return False


def create_sample_documents() -> None:
    """Create sample documents manually since web downloads may not be reliable."""
    
    test_dir = Path("test_documents")
    test_dir.mkdir(exist_ok=True)
    
    # Create a more comprehensive HTML document
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive Test Document</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Comprehensive Test Document</h1>
    
    <h2>Introduction</h2>
    <p>This is a comprehensive test document with various HTML elements to test the markdown converter.</p>
    
    <h2>Features</h2>
    <ul>
        <li><strong>Bold text</strong> and <em>italic text</em></li>
        <li><a href="https://example.com">Links</a> and <code>code snippets</code></li>
        <li>Lists and nested elements</li>
    </ul>
    
    <h2>Data Table</h2>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Department</th>
                <th>Salary</th>
                <th>Start Date</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>John Smith</td>
                <td>Engineering</td>
                <td>$85,000</td>
                <td>2023-01-15</td>
            </tr>
            <tr>
                <td>Sarah Johnson</td>
                <td>Marketing</td>
                <td>$72,000</td>
                <td>2023-03-20</td>
            </tr>
            <tr>
                <td>Michael Brown</td>
                <td>Sales</td>
                <td>$68,000</td>
                <td>2023-02-10</td>
            </tr>
        </tbody>
    </table>
    
    <h2>Code Example</h2>
    <pre><code>def hello_world():
    print("Hello, World!")
    return "Success"</code></pre>
    
    <h2>Conclusion</h2>
    <p>This document contains various HTML elements including:</p>
    <ol>
        <li>Headings of different levels</li>
        <li>Paragraphs with formatting</li>
        <li>Unordered and ordered lists</li>
        <li>Tables with headers and data</li>
        <li>Code blocks and inline code</li>
        <li>Links and emphasis</li>
    </ol>
    
    <hr>
    <p><small>Generated for testing purposes</small></p>
</body>
</html>"""
    
    with open(test_dir / "comprehensive_test.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Create a complex text document
    text_content = """COMPREHENSIVE TEST DOCUMENT
===============================

Project: Markdown Converter Testing
Version: 1.0.0
Date: 2024-01-15
Author: Test Team

OVERVIEW
--------
This document is designed to test the markdown converter's ability to handle
various text formatting and structures commonly found in real-world documents.

SECTION 1: BASIC FORMATTING
---------------------------
This section tests basic text formatting including:

* Bullet points with asterisks
* Multiple levels of indentation
* Mixed content types

1. Numbered lists
2. With multiple items
3. And sub-items

SECTION 2: TABLES AND DATA
--------------------------
The following table demonstrates data structure:

Product    | Price  | Stock | Category
-----------|--------|-------|----------
Widget A   | $10.00 | 150   | Hardware
Widget B   | $15.50 | 75    | Software
Widget C   | $8.25  | 200   | Hardware

SECTION 3: CODE AND TECHNICAL CONTENT
------------------------------------
Here's a sample code block:

```python
def process_document(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return parse_content(content)
```

SECTION 4: SPECIAL CHARACTERS
-----------------------------
Testing special characters: © ® ™ € £ ¥ § ¶ † ‡

SECTION 5: LONG PARAGRAPHS
--------------------------
This is a longer paragraph designed to test how the converter handles
extended text blocks. It contains multiple sentences and should be
preserved as a single paragraph in the output markdown. The content
includes various punctuation marks and formatting that should be
handled appropriately by the conversion process.

CONCLUSION
----------
This document provides a comprehensive test suite for the markdown
converter, covering various formatting styles and content types that
are commonly encountered in real-world documents.

---
End of Document
"""
    
    with open(test_dir / "comprehensive_test.txt", "w", encoding="utf-8") as f:
        f.write(text_content)
    
    # Create a CSV file (Excel-like)
    csv_content = """Product,Category,Price,Stock,Rating,Description
Laptop Pro,Electronics,1299.99,45,4.8,High-performance laptop for professionals
Wireless Mouse,Accessories,29.99,120,4.5,Ergonomic wireless mouse
USB Cable,Accessories,9.99,200,4.2,High-speed USB 3.0 cable
Monitor 27",Electronics,299.99,30,4.7,27-inch 4K monitor
Keyboard,Accessories,89.99,60,4.6,Mechanical gaming keyboard
Headphones,Electronics,199.99,25,4.9,Noise-cancelling wireless headphones"""
    
    with open(test_dir / "product_catalog.csv", "w", encoding="utf-8") as f:
        f.write(csv_content)
    
    print("✅ Created comprehensive test documents")


def main() -> None:
    """Main function to download/create sample documents."""
    
    print("🔧 Setting up sample documents for testing...")
    
    # Create comprehensive test documents
    create_sample_documents()
    
    # List available test files
    test_dir = Path("test_documents")
    print(f"\n📁 Test documents available in: {test_dir.absolute()}")
    print("📋 Available test files:")
    
    for file in sorted(test_dir.glob("*")):
        size = file.stat().st_size
        print(f"   - {file.name} ({size} bytes)")
    
    print("\n🎯 Ready for testing!")
    print("💡 You can now use these files to test the markdown converter functionality.")


if __name__ == "__main__":
    main() 