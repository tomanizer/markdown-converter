#!/usr/bin/env python3
"""
Verify pandoc version and installation.

This script checks that we're using the correct pandoc version
and that it's properly accessible from Python.
"""

import subprocess
import sys
from pathlib import Path


def check_pandoc_version() -> None:
    """Check the pandoc version and installation."""
    
    print("🔍 Checking pandoc installation...")
    
    # Check system pandoc
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, text=True, check=True)
        version_line = result.stdout.split('\n')[0]
        print(f"✅ System pandoc: {version_line}")
        
        # Extract version number
        if 'pandoc' in version_line:
            version = version_line.split()[1]
            print(f"   Version: {version}")
            
            # Check if it's 3.7 or newer
            major, minor = map(int, version.split('.')[:2])
            if major > 3 or (major == 3 and minor >= 7):
                print("✅ Pandoc version is 3.7+ (compatible)")
            else:
                print("⚠️  Pandoc version is older than 3.7")
                
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running pandoc: {e}")
        return
    except FileNotFoundError:
        print("❌ Pandoc not found in PATH")
        return
    
    # Check Python pypandoc
    try:
        import pypandoc
        py_version = pypandoc.get_pandoc_version()
        print(f"✅ Python pypandoc version: {py_version}")
        
        # Check if Python version matches system version
        if py_version == version:
            print("✅ Python and system pandoc versions match")
        else:
            print(f"⚠️  Version mismatch: Python={py_version}, System={version}")
            
    except ImportError:
        print("❌ pypandoc not installed")
    except Exception as e:
        print(f"❌ Error checking pypandoc: {e}")
    
    # Check pandoc location
    try:
        result = subprocess.run(['which', 'pandoc'], 
                              capture_output=True, text=True, check=True)
        pandoc_path = result.stdout.strip()
        print(f"📍 Pandoc location: {pandoc_path}")
        
        if '/usr/local/bin/pandoc' in pandoc_path:
            print("✅ Using Homebrew pandoc (preferred)")
        elif '/opt/anaconda3/bin/pandoc' in pandoc_path:
            print("⚠️  Using Anaconda pandoc (may be older)")
        else:
            print(f"ℹ️  Using pandoc from: {pandoc_path}")
            
    except subprocess.CalledProcessError:
        print("❌ Could not determine pandoc location")


def test_pandoc_conversion() -> None:
    """Test a simple pandoc conversion."""
    
    print("\n🧪 Testing pandoc conversion...")
    
    # Create a simple test file
    test_content = """# Test Document

This is a test document for pandoc conversion.

## Features

- Simple formatting
- Basic structure
- Easy to parse

End of document.
"""
    
    test_file = Path("test_pandoc_input.md")
    output_file = Path("test_pandoc_output.html")
    
    try:
        # Write test file
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        # Run pandoc conversion
        result = subprocess.run([
            'pandoc', str(test_file), 
            '-o', str(output_file),
            '--from', 'markdown',
            '--to', 'html'
        ], capture_output=True, text=True, check=True)
        
        print("✅ Pandoc conversion successful")
        
        # Check output
        if output_file.exists():
            with open(output_file, 'r') as f:
                output_content = f.read()
                if '<h1>' in output_content and '<h2>' in output_content:
                    print("✅ HTML output contains expected elements")
                else:
                    print("⚠️  HTML output may be incomplete")
        
        # Cleanup
        test_file.unlink(missing_ok=True)
        output_file.unlink(missing_ok=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Pandoc conversion failed: {e}")
        print(f"   Error output: {e.stderr}")
    except Exception as e:
        print(f"❌ Error during conversion test: {e}")


def main() -> None:
    """Main function."""
    
    print("🔧 Pandoc Version Verification")
    print("=" * 40)
    
    check_pandoc_version()
    test_pandoc_conversion()
    
    print("\n✅ Pandoc verification complete!")


if __name__ == "__main__":
    main() 