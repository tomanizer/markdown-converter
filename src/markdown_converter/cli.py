"""
Command Line Interface for Markdown Converter

This module provides a comprehensive CLI for the markdown converter with support
for single file conversion and batch processing.
"""

import click
import logging
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
import yaml
import os

from .core.converter import MainConverter, ConversionResult, DirectoryConversionResult
from .core.exceptions import ConversionError


def setup_cli_logging(verbose: bool = False, log_file: Optional[str] = None, structured: bool = False) -> None:
    """
    Setup logging configuration for CLI.
    
    :param verbose: Enable verbose logging
    :param log_file: Optional log file path
    :param structured: Enable structured JSON logging
    """
    # Configure logging level
    level = logging.DEBUG if verbose else logging.INFO
    
    # Create formatter
    if structured:
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        )
    else:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def load_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from file or use defaults.
    
    :param config_file: Path to configuration file
    :return: Configuration dictionary
    """
    config = {}
    
    # Load from file if provided
    if config_file and Path(config_file).exists():
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f) or {}
        except Exception as e:
            click.echo(f"Warning: Could not load config file {config_file}: {e}")
    
    # Load from environment variables
    env_config = {
        'max_workers': os.getenv('MDC_MAX_WORKERS'),
        'max_memory_mb': os.getenv('MDC_MAX_MEMORY_MB'),
        'batch_size': os.getenv('MDC_BATCH_SIZE'),
        'output_format': os.getenv('MDC_OUTPUT_FORMAT', 'markdown'),
        'preserve_structure': os.getenv('MDC_PRESERVE_STRUCTURE', 'true').lower() == 'true',
    }
    
    # Update config with environment variables (only if set)
    for key, value in env_config.items():
        if value is not None:
            config[key] = value
    
    return config


def print_supported_formats() -> None:
    """Print list of supported input formats."""
    formats = [
        ("Word Documents", [".docx", ".doc", ".rtf", ".odt"]),
        ("PDF Documents", [".pdf"]),
        ("Excel Spreadsheets", [".xlsx", ".xls", ".xlsb", ".ods"]),
        ("HTML Documents", [".html", ".htm"]),
        ("Plain Text", [".txt"]),
        ("Email Messages", [".msg", ".eml"]),
        ("PowerPoint", [".pptx", ".ppt", ".odp"]),
    ]
    
    click.echo("📄 Supported Input Formats:")
    for category, extensions in formats:
        click.echo(f"  {category}: {', '.join(extensions)}")


def print_processing_stats(stats: Any) -> None:
    """
    Print processing statistics.
    
    :param stats: Processing statistics object
    """
    if hasattr(stats, 'total_files'):
        click.echo(f"\n📊 Processing Statistics:")
        click.echo(f"  Total files: {stats.total_files}")
        click.echo(f"  Processed: {stats.processed_files}")
        click.echo(f"  Failed: {stats.failed_files}")
        click.echo(f"  Skipped: {stats.skipped_files}")
        
        if stats.end_time and stats.start_time:
            duration = stats.end_time - stats.start_time
            click.echo(f"  Duration: {duration:.2f} seconds")
            if stats.processed_files > 0:
                rate = stats.processed_files / duration
                click.echo(f"  Rate: {rate:.2f} files/second")


@click.group()
@click.version_option(version="0.1.0")
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--log-file', help='Log file path')
@click.option('--structured', is_flag=True, help='Enable structured JSON logging')
@click.option('--config', help='Configuration file path')
@click.pass_context
def cli(ctx: click.Context, verbose: bool, log_file: Optional[str], structured: bool, config: Optional[str]) -> None:
    """Markdown Converter - Convert documents to markdown format."""
    # Setup logging
    setup_cli_logging(verbose, log_file, structured)
    
    # Load configuration
    config_data = load_config(config)
    ctx.obj = {
        'config': config_data,
    }
    
    # Log CLI startup
    logging.info("Markdown Converter CLI started", extra={
        'verbose': verbose,
        'log_file': log_file,
        'structured': structured,
        'config_file': config
    })


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.argument('output_file', type=click.Path(path_type=Path), required=False)
@click.option('--format', '-f', 'output_format', default='markdown', 
              help='Output format (markdown, html, pdf)')
@click.option('--preserve-structure/--no-preserve-structure', default=True,
              help='Preserve document structure and formatting')
@click.option('--extract-images/--no-extract-images', default=True,
              help='Extract and save images separately')
@click.option('--metadata/--no-metadata', default=True,
              help='Include document metadata')
@click.pass_context
def convert(ctx: click.Context, input_file: Path, output_file: Optional[Path], 
           output_format: str, preserve_structure: bool, extract_images: bool, 
           metadata: bool) -> None:
    """Convert a single file to markdown."""
    
    # Generate output path if not provided
    if output_file is None:
        output_file = input_file.with_suffix(f'.{output_format}')
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Create converter
        converter = MainConverter()
        
        # Perform conversion
        result = converter.convert_file(input_file, output_file, output_format)
        
        if result.success:
            # Log success with file size info
            file_size = input_file.stat().st_size / (1024 * 1024)  # MB
            logging.info(
                f"File conversion completed successfully",
                extra={
                    'input_file': str(input_file),
                    'output_file': str(output_file),
                    'file_size_mb': file_size,
                    'processing_time': result.processing_time
                }
            )
            click.echo(f"✅ Converted {input_file} to {output_file}")
        else:
            logging.error(f"Conversion failed: {result.error_message}")
            click.echo(f"❌ Conversion failed: {result.error_message}")
            sys.exit(1)
            
    except Exception as e:
        logging.error(f"Unexpected error during conversion: {e}")
        click.echo(f"❌ Unexpected error: {e}")
        sys.exit(1)


@cli.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument('output_dir', type=click.Path(path_type=Path), required=False)
@click.option('--workers', '-w', default=None, type=int,
              help='Number of worker processes (default: CPU count, max 8)')
@click.option('--batch-size', default=100, type=int,
              help='Number of files to process in each batch')
@click.option('--max-memory', default=2048, type=int,
              help='Maximum memory usage per worker in MB')
@click.option('--file-size-limit', default=70, type=int,
              help='Skip files larger than this size in MB')
@click.option('--continue-on-error', is_flag=True, default=True,
              help='Continue processing even if some files fail')
@click.option('--progress/--no-progress', default=True,
              help='Show progress bar')
@click.pass_context
def batch(ctx: click.Context, input_dir: Path, output_dir: Optional[Path],
          workers: Optional[int], batch_size: int, max_memory: int,
          file_size_limit: int, continue_on_error: bool, progress: bool) -> None:
    """
    Convert all supported files in a directory using parallel processing.
    
    INPUT_DIR: Directory containing files to convert
    OUTPUT_DIR: Output directory (optional, auto-generated if not provided)
    """
    try:
        # Generate output directory if not provided
        if output_dir is None:
            output_dir = input_dir.parent / f"{input_dir.name}_converted"
        
        click.echo(f"🔄 Starting batch conversion from {input_dir} to {output_dir}...")
        
        # Setup batch processor configuration
        config = ctx.obj['config'].copy()
        if workers:
            config['max_workers'] = min(workers, 8)
        config.update({
            'batch_size': batch_size,
            'max_memory_mb': max_memory,
            'file_size_limit_mb': file_size_limit,
            'continue_on_error': continue_on_error,
            'show_progress_bar': progress,
        })
        
        # Create converter and process directory
        converter = MainConverter(config)
        result = converter.convert_directory(
            input_dir=input_dir,
            output_dir=output_dir,
            max_workers=workers,
            continue_on_error=continue_on_error
        )
        
        # Print results
        print_processing_stats(result)
        
        if result.failed_files > 0:
            click.echo(f"\n⚠️  {result.failed_files} files failed to convert")
            if not continue_on_error:
                sys.exit(1)
        else:
            click.echo(f"\n✅ All files converted successfully!")
            
    except ConversionError as e:
        click.echo(f"❌ Batch processing error: {e}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        if ctx.obj['verbose']:
            import traceback
            traceback.print_exc()
        sys.exit(1)





@cli.command()
@click.option('--detailed', is_flag=True, help='Show detailed information')
def info(detailed: bool) -> None:
    """Show information about the markdown converter."""
    click.echo("📄 Markdown Converter v0.1.0")
    click.echo("=" * 40)
    
    # Show supported formats
    print_supported_formats()
    
    if detailed:
        click.echo("\n🔧 System Information:")
        
        # Check pandoc
        try:
            import pypandoc
            version = pypandoc.get_pandoc_version()
            click.echo(f"  Pandoc: {version}")
        except Exception:
            click.echo("  Pandoc: Not available")
        
        # Check Dask
        try:
            import dask
            click.echo(f"  Dask: {dask.__version__}")
        except ImportError:
            click.echo("  Dask: Not installed")
        
        # Check other dependencies
        dependencies = [
            ('python-docx', 'docx'),
            ('pdfplumber', 'pdfplumber'),
            ('openpyxl', 'openpyxl'),
            ('beautifulsoup4', 'bs4'),
            ('extract-msg', 'extract_msg'),
        ]
        
        for name, module in dependencies:
            try:
                __import__(module)
                click.echo(f"  {name}: Available")
            except ImportError:
                click.echo(f"  {name}: Not installed")


@cli.command()
def formats() -> None:
    """Show supported input formats."""
    print_supported_formats()


@cli.command()
@click.option('--json', is_flag=True, help='Output health check in JSON format')
@click.pass_context
def health(ctx: click.Context, json: bool) -> None:
    """Check system health and performance."""
    
    # Simple health check
    import psutil
    from datetime import datetime
    
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'performance': {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'memory_used_mb': psutil.virtual_memory().used / (1024 * 1024),
            'disk_usage_percent': psutil.disk_usage('/').percent,
            'active_threads': 0  # Not easily available without threading module
        }
    }
    
    if json:
        import json as json_module
        click.echo(json_module.dumps(health_status, indent=2))
    else:
        # Display health status in a user-friendly format
        status_emoji = {
            "healthy": "✅",
            "warning": "⚠️",
            "critical": "🚨",
            "error": "❌"
        }
        
        click.echo(f"{status_emoji.get(health_status['status'], '❓')} System Health: {health_status['status'].upper()}")
        click.echo(f"📅 Timestamp: {health_status['timestamp']}")
        
        if 'performance' in health_status:
            perf = health_status['performance']
            click.echo(f"💻 CPU Usage: {perf['cpu_percent']:.1f}%")
            click.echo(f"🧠 Memory Usage: {perf['memory_percent']:.1f}% ({perf['memory_used_mb']:.1f} MB)")
            click.echo(f"💾 Disk Usage: {perf['disk_usage_percent']:.1f}%")


@cli.command()
@click.argument('file_path', type=click.Path(exists=True, path_type=Path))
@click.option('--json', is_flag=True, help='Output in JSON format')
@click.pass_context
def analyze(ctx: click.Context, file_path: Path, json: bool) -> None:
    """Analyze a file for conversion capabilities."""
    try:
        converter = MainConverter()
        info = converter.get_conversion_info(file_path)
        
        if json:
            import json as json_module
            click.echo(json_module.dumps(info, indent=2))
        else:
            click.echo(f"📄 File Analysis: {file_path}")
            click.echo(f"  Size: {info['file_size'] / (1024*1024):.2f} MB")
            click.echo(f"  Extension: {info['extension']}")
            click.echo(f"  Can Convert: {'✅' if info['can_convert'] else '❌'}")
            if info['parser_found']:
                click.echo(f"  Parser: {info['parser_name']}")
            else:
                click.echo("  Parser: None found")
            click.echo(f"  Registered Parsers: {', '.join(info['registered_parsers'])}")
            
    except Exception as e:
        click.echo(f"❌ Analysis failed: {e}")
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True, path_type=Path))
@click.option('--json', is_flag=True, help='Output in JSON format')
@click.pass_context
def file_info(ctx: click.Context, file_path: Path, json: bool) -> None:
    """Get detailed information about a file."""
    try:
        converter = MainConverter()
        info = converter.get_file_info(file_path)
        
        if json:
            import json as json_module
            click.echo(json_module.dumps(info, indent=2))
        else:
            click.echo(f"📄 File Information: {file_path}")
            click.echo(f"  Name: {info['name']}")
            click.echo(f"  Size: {info['size_mb']:.2f} MB ({info['size_bytes']} bytes)")
            click.echo(f"  Extension: {info['extension']}")
            click.echo(f"  Supported: {'✅' if info['is_supported'] else '❌'}")
            click.echo(f"  Modified: {info['modified_time']}")
            
    except FileNotFoundError:
        click.echo(f"❌ File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error getting file info: {e}")
        sys.exit(1)


@cli.command()
@click.argument('input_format', type=str)
@click.argument('output_format', type=str)
@click.pass_context
def validate(ctx: click.Context, input_format: str, output_format: str) -> None:
    """Validate if a format combination is supported."""
    try:
        converter = MainConverter()
        is_supported = converter.validate_format_support(input_format, output_format)
        
        if is_supported:
            click.echo(f"✅ {input_format} → {output_format} is supported")
        else:
            click.echo(f"❌ {input_format} → {output_format} is not supported")
            formats = converter.get_supported_formats()
            click.echo(f"Supported input formats: {', '.join(formats['input'])}")
            click.echo(f"Supported output formats: {', '.join(formats['output'])}")
            
    except Exception as e:
        click.echo(f"❌ Validation failed: {e}")
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True, path_type=Path))
@click.pass_context
def can_convert(ctx: click.Context, file_path: Path) -> None:
    """Check if a file can be converted."""
    try:
        converter = MainConverter()
        can_convert = converter.can_convert(file_path)
        
        if can_convert:
            click.echo(f"✅ {file_path} can be converted")
        else:
            click.echo(f"❌ {file_path} cannot be converted")
            
    except Exception as e:
        click.echo(f"❌ Check failed: {e}")
        sys.exit(1)


@cli.command()
@click.option('--json', is_flag=True, help='Output in JSON format')
@click.pass_context
def list_parsers(ctx: click.Context, json: bool) -> None:
    """List all available parsers."""
    try:
        converter = MainConverter()
        formats = converter.get_supported_formats()
        
        if json:
            import json as json_module
            click.echo(json_module.dumps(formats, indent=2))
        else:
            click.echo("🔧 Available Parsers:")
            for parser_name in formats['input']:
                click.echo(f"  • {parser_name}")
            click.echo(f"\n📤 Output Formats:")
            for output_format in formats['output']:
                click.echo(f"  • {output_format}")
                
    except Exception as e:
        click.echo(f"❌ Failed to list parsers: {e}")
        sys.exit(1)


@cli.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option('--output-dir', type=click.Path(path_type=Path), help='Output directory for test results')
@click.option('--max-files', default=5, type=int, help='Maximum number of files to test')
@click.pass_context
def test(ctx: click.Context, input_dir: Path, output_dir: Optional[Path], max_files: int) -> None:
    """Test conversion capabilities with sample files."""
    try:
        converter = MainConverter()
        
        # Find test files
        test_files = []
        for file_path in input_dir.iterdir():
            if file_path.is_file() and converter.can_convert(file_path):
                test_files.append(file_path)
                if len(test_files) >= max_files:
                    break
        
        if not test_files:
            click.echo(f"❌ No convertible files found in {input_dir}")
            return
        
        click.echo(f"🧪 Testing conversion with {len(test_files)} files...")
        
        # Setup output directory
        if output_dir is None:
            output_dir = Path("test_output")
        output_dir.mkdir(exist_ok=True)
        
        results = []
        for file_path in test_files:
            output_file = output_dir / f"{file_path.stem}_test.md"
            result = converter.convert_file(file_path, output_file)
            results.append(result)
            
            status = "✅" if result.success else "❌"
            click.echo(f"  {status} {file_path.name}")
        
        # Summary
        successful = sum(1 for r in results if r.success)
        click.echo(f"\n📊 Test Results: {successful}/{len(results)} successful")
        
        if successful == len(results):
            click.echo("🎉 All tests passed!")
        else:
            click.echo("⚠️  Some tests failed")
            
    except Exception as e:
        click.echo(f"❌ Test failed: {e}")
        sys.exit(1)


@cli.command()
@click.option('--temp-dirs', is_flag=True, help='Clean temporary directories')
@click.option('--log-files', is_flag=True, help='Clean log files')
@click.option('--all', is_flag=True, help='Clean all temporary files')
@click.pass_context
def clean(ctx: click.Context, temp_dirs: bool, log_files: bool, all: bool) -> None:
    """Clean up temporary files and directories."""
    import shutil
    import glob
    
    cleaned_count = 0
    
    if all or temp_dirs:
        # Clean temp directories
        temp_patterns = ["temp_*", "*_converted", "test_output"]
        for pattern in temp_patterns:
            for path in Path(".").glob(pattern):
                if path.is_dir():
                    try:
                        shutil.rmtree(path)
                        click.echo(f"🗑️  Removed directory: {path}")
                        cleaned_count += 1
                    except Exception as e:
                        click.echo(f"⚠️  Failed to remove {path}: {e}")
    
    if all or log_files:
        # Clean log files
        log_patterns = ["*.log", "*.json"]
        for pattern in log_patterns:
            for path in Path(".").glob(pattern):
                if path.is_file():
                    try:
                        path.unlink()
                        click.echo(f"🗑️  Removed file: {path}")
                        cleaned_count += 1
                    except Exception as e:
                        click.echo(f"⚠️  Failed to remove {path}: {e}")
    
    if cleaned_count == 0:
        click.echo("✨ No files to clean")
    else:
        click.echo(f"🧹 Cleaned {cleaned_count} items")


def main() -> None:
    """Main entry point for the CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n🛑 Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 