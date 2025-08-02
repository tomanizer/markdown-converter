#!/usr/bin/env python3
"""
Generate test documents for the markdown converter.

This script creates sample documents in various formats (Word, Excel, HTML, etc.)
to test the conversion functionality.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any
import json

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.markdown_converter.utils.document_generator import DocumentGenerator


def main() -> None:
    """Generate test documents for the markdown converter."""
    
    # Create test documents directory
    test_dir = Path("test_documents")
    test_dir.mkdir(exist_ok=True)
    
    print("🔧 Generating test documents...")
    
    # Initialize document generator
    generator = DocumentGenerator()
    
    # Generate sample documents
    documents = [
        {
            "name": "sample_report.docx",
            "type": "word",
            "content": {
                "title": "Sample Business Report",
                "sections": [
                    {
                        "heading": "Executive Summary",
                        "content": "This is a sample business report with multiple sections and formatting."
                    },
                    {
                        "heading": "Financial Overview",
                        "content": "The company achieved 15% growth in Q3 with strong performance across all divisions.",
                        "table": [
                            ["Quarter", "Revenue", "Growth"],
                            ["Q1", "$1.2M", "8%"],
                            ["Q2", "$1.4M", "12%"],
                            ["Q3", "$1.6M", "15%"]
                        ]
                    },
                    {
                        "heading": "Key Findings",
                        "content": "• Customer satisfaction increased by 20%\n• Market share grew to 25%\n• New product line launched successfully"
                    }
                ]
            }
        },
        {
            "name": "data_analysis.xlsx",
            "type": "excel",
            "content": {
                "sheets": [
                    {
                        "name": "Sales Data",
                        "data": [
                            ["Product", "Region", "Sales", "Units"],
                            ["Widget A", "North", 12500, 250],
                            ["Widget B", "South", 8900, 178],
                            ["Widget C", "East", 15600, 312],
                            ["Widget D", "West", 11200, 224]
                        ]
                    },
                    {
                        "name": "Summary",
                        "data": [
                            ["Metric", "Value"],
                            ["Total Sales", "$48,200"],
                            ["Total Units", "964"],
                            ["Average Price", "$50.00"]
                        ]
                    }
                ]
            }
        },
        {
            "name": "sample_webpage.html",
            "type": "html",
            "content": {
                "title": "Sample Web Page",
                "body": """
                <h1>Welcome to Our Website</h1>
                <p>This is a sample HTML document with various elements.</p>
                
                <h2>Features</h2>
                <ul>
                    <li>Responsive design</li>
                    <li>Modern interface</li>
                    <li>Fast loading</li>
                </ul>
                
                <h2>Contact Information</h2>
                <table>
                    <tr><th>Name</th><th>Email</th><th>Phone</th></tr>
                    <tr><td>John Doe</td><td>john@example.com</td><td>555-1234</td></tr>
                    <tr><td>Jane Smith</td><td>jane@example.com</td><td>555-5678</td></tr>
                </table>
                
                <h2>About Us</h2>
                <p>We are a leading technology company focused on innovation and customer satisfaction.</p>
                """
            }
        },
        {
            "name": "sample_email.msg",
            "type": "outlook",
            "content": {
                "subject": "Project Update - Q3 Review",
                "from": "manager@company.com",
                "to": "team@company.com",
                "date": "2024-01-15",
                "body": """
                Hi Team,
                
                I wanted to provide an update on our Q3 project status.
                
                Key Achievements:
                - Completed Phase 1 implementation
                - Reduced processing time by 40%
                - Customer satisfaction score: 4.8/5
                
                Next Steps:
                1. Begin Phase 2 planning
                2. Schedule stakeholder review
                3. Prepare budget proposal
                
                Please let me know if you have any questions.
                
                Best regards,
                Project Manager
                """
            }
        },
        {
            "name": "technical_spec.txt",
            "type": "text",
            "content": {
                "content": """
            TECHNICAL SPECIFICATION
            =======================
            
            Project: Markdown Converter
            Version: 1.0.0
            Date: 2024-01-15
            
            OVERVIEW
            --------
            This document outlines the technical specifications for the markdown converter tool.
            
            REQUIREMENTS
            ------------
            1. Support multiple input formats
            2. Preserve document structure
            3. Handle large files efficiently
            4. Provide clean markdown output
            
            TECHNICAL DETAILS
            -----------------
            - Python 3.12+
            - Pandoc integration
            - Parallel processing support
            - Memory-efficient processing
            
            IMPLEMENTATION NOTES
            --------------------
            The converter uses a modular architecture with format-specific parsers
            and a unified output formatter.
            """
            }
        }
    ]
    
    # Generate each document
    for doc in documents:
        try:
            output_path = test_dir / doc["name"]
            generator.create_document(doc["type"], doc["content"], output_path)
            print(f"✅ Created: {output_path}")
        except Exception as e:
            print(f"❌ Failed to create {doc['name']}: {e}")
    
    # Create a simple test document manually (fallback)
    create_simple_test_files(test_dir)
    
    print(f"\n📁 Test documents created in: {test_dir.absolute()}")
    print("📋 Available test files:")
    for file in test_dir.glob("*"):
        print(f"   - {file.name}")


def create_simple_test_files(test_dir: Path) -> None:
    """Create simple test files as fallback."""
    
    # Simple HTML file
    html_content = """<!DOCTYPE html>
<html>
<head><title>Test Document</title></head>
<body>
<h1>Test Document</h1>
<p>This is a simple test document.</p>
<ul>
<li>Item 1</li>
<li>Item 2</li>
<li>Item 3</li>
</ul>
</body>
</html>"""
    
    with open(test_dir / "simple_test.html", "w") as f:
        f.write(html_content)
    
    # Simple text file
    text_content = """Test Document
=============

This is a simple text document for testing.

Features:
- Simple formatting
- Basic structure
- Easy to parse

End of document."""
    
    with open(test_dir / "simple_test.txt", "w") as f:
        f.write(text_content)


if __name__ == "__main__":
    main() 