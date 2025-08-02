#!/usr/bin/env python3
"""
CLI and API Example

This script demonstrates how to use the markdown converter CLI and Python API
for various conversion scenarios.
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.markdown_converter.api import (
    MarkdownConverter, 
    convert_file, 
    convert_directory, 
    convert_with_grid
)
from src.markdown_converter.config import create_default_config_file


def example_single_file_conversion():
    """Example of converting a single file."""
    print("📄 Example 1: Single File Conversion")
    print("=" * 50)
    
    # Create a test file
    test_file = Path("test_documents/sample_report.docx")
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return
    
    # Convert using the API
    result = convert_file(
        input_file=test_file,
        output_format='markdown',
        preserve_structure=True,
        extract_images=True
    )
    
    if result.success:
        print(f"✅ Successfully converted {result.input_file} to {result.output_file}")
        print(f"   File size: {result.file_size_mb:.2f} MB")
        print(f"   Processing time: {result.processing_time:.2f} seconds")
    else:
        print(f"❌ Conversion failed: {result.error_message}")


def example_batch_conversion():
    """Example of batch conversion."""
    print("\n📁 Example 2: Batch Conversion")
    print("=" * 50)
    
    # Create converter instance
    converter = MarkdownConverter()
    
    # Convert directory
    input_dir = Path("test_documents")
    if not input_dir.exists():
        print(f"❌ Test directory not found: {input_dir}")
        return
    
    result = converter.convert_directory(
        input_dir=input_dir,
        max_workers=4,
        batch_size=10,
        max_memory_mb=1024,
        continue_on_error=True
    )
    
    print(f"📊 Batch Processing Results:")
    print(f"   Total files: {result.stats.total_files}")
    print(f"   Processed: {result.stats.processed_files}")
    print(f"   Failed: {result.stats.failed_files}")
    print(f"   Skipped: {result.stats.skipped_files}")
    
    if result.stats.end_time and result.stats.start_time:
        duration = result.stats.end_time - result.stats.start_time
        print(f"   Duration: {duration:.2f} seconds")
        if result.stats.processed_files > 0:
            rate = result.stats.processed_files / duration
            print(f"   Rate: {rate:.2f} files/second")


def example_grid_conversion():
    """Example of grid conversion (requires Dask)."""
    print("\n🌐 Example 3: Grid Conversion")
    print("=" * 50)
    
    try:
        # Check if Dask is available
        import dask
        print("✅ Dask is available for grid processing")
        
        # Convert using grid processing
        input_dir = Path("test_documents")
        if not input_dir.exists():
            print(f"❌ Test directory not found: {input_dir}")
            return
        
        result = convert_with_grid(
            input_dir=input_dir,
            cluster_type='local',
            n_workers=2,
            memory_limit='1GB'
        )
        
        print(f"📊 Grid Processing Results:")
        print(f"   Job ID: {result.job_info.job_id}")
        print(f"   Status: {result.job_info.status}")
        print(f"   Total tasks: {result.job_info.total_tasks}")
        print(f"   Completed tasks: {result.job_info.completed_tasks}")
        print(f"   Failed tasks: {result.job_info.failed_tasks}")
        
    except ImportError:
        print("❌ Dask not available. Install with: pip install dask[distributed]")
    except Exception as e:
        print(f"❌ Grid processing failed: {e}")


def example_configuration():
    """Example of configuration management."""
    print("\n⚙️  Example 4: Configuration Management")
    print("=" * 50)
    
    # Create default configuration file
    config_file = "markdown_converter_config.yaml"
    create_default_config_file(config_file)
    print(f"✅ Created default configuration file: {config_file}")
    
    # Load configuration
    from src.markdown_converter.config import load_config
    config_manager = load_config(config_file)
    
    # Validate configuration
    errors = config_manager.validate()
    if errors:
        print("❌ Configuration validation errors:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✅ Configuration is valid")
    
    # Show configuration
    config = config_manager.get_config()
    print(f"\n📋 Current Configuration:")
    print(f"   Output format: {config.conversion.output_format}")
    print(f"   Max workers: {config.batch.max_workers}")
    print(f"   Max memory: {config.batch.max_memory_mb} MB")
    print(f"   File size limit: {config.batch.file_size_limit_mb} MB")
    
    # Clean up
    if Path(config_file).exists():
        Path(config_file).unlink()
        print(f"🗑️  Cleaned up configuration file")


def example_cli_usage():
    """Example of CLI usage."""
    print("\n🖥️  Example 5: CLI Usage")
    print("=" * 50)
    
    print("The markdown converter provides a comprehensive CLI:")
    print()
    print("📄 Convert a single file:")
    print("   markdown-converter convert input.docx output.md")
    print()
    print("📁 Convert all files in a directory:")
    print("   markdown-converter batch input_dir output_dir --workers 4")
    print()
    print("🌐 Convert using grid processing:")
    print("   markdown-converter grid input_dir output_dir --workers 8")
    print()
    print("ℹ️  Show supported formats:")
    print("   markdown-converter formats")
    print()
    print("📊 Show system information:")
    print("   markdown-converter info --detailed")
    print()
    print("⚙️  Create configuration file:")
    print("   markdown-converter config create")


def example_environment_variables():
    """Example of environment variable configuration."""
    print("\n🔧 Example 6: Environment Variables")
    print("=" * 50)
    
    print("You can configure the converter using environment variables:")
    print()
    print("📄 Conversion settings:")
    print("   export MDC_OUTPUT_FORMAT=markdown")
    print("   export MDC_PRESERVE_STRUCTURE=true")
    print("   export MDC_EXTRACT_IMAGES=true")
    print()
    print("📁 Batch processing settings:")
    print("   export MDC_MAX_WORKERS=4")
    print("   export MDC_BATCH_SIZE=100")
    print("   export MDC_MAX_MEMORY_MB=2048")
    print("   export MDC_FILE_SIZE_LIMIT_MB=70")
    print()
    print("🌐 Grid processing settings:")
    print("   export MDC_CLUSTER_TYPE=local")
    print("   export MDC_N_WORKERS=4")
    print("   export MDC_MEMORY_LIMIT_PER_WORKER=2GB")
    print()
    print("📝 Logging settings:")
    print("   export MDC_LOG_LEVEL=INFO")
    print("   export MDC_LOG_FILE=converter.log")
    print("   export MDC_LOG_CONSOLE=true")


def main():
    """Run all examples."""
    print("🚀 Markdown Converter CLI and API Examples")
    print("=" * 60)
    
    # Check if test documents exist
    test_dir = Path("test_documents")
    if not test_dir.exists():
        print("❌ Test documents directory not found.")
        print("   Please run the download script first:")
        print("   python scripts/download_sample_documents.py")
        return
    
    # Run examples
    example_single_file_conversion()
    example_batch_conversion()
    example_grid_conversion()
    example_configuration()
    example_cli_usage()
    example_environment_variables()
    
    print("\n✅ All examples completed!")
    print("\n📚 Next Steps:")
    print("   1. Try the CLI commands shown above")
    print("   2. Explore the Python API in your own scripts")
    print("   3. Customize configuration for your needs")
    print("   4. Check the documentation for advanced features")


if __name__ == '__main__':
    main() 