"""
Command Line Interface for Markdown Converter

This module provides a comprehensive CLI for the markdown converter with support
for single file conversion, batch processing, and grid processing.
"""

import click
import logging
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
import yaml
import os

from .core.engine import ConversionEngine
from .core.batch_processor import BatchProcessor
from .core.grid_processor import GridProcessor
from .core.filesystem import FilesystemManager
from .core.exceptions import (
    ConversionError, 
    BatchProcessingError, 
    GridProcessingError,
    DependencyError
)


def setup_logging(verbose: bool = False, log_file: Optional[str] = None) -> None:
    """
    Setup logging configuration.
    
    :param verbose: Enable verbose logging
    :param log_file: Optional log file path
    """
    level = logging.DEBUG if verbose else logging.INFO
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=[
            logging.StreamHandler(sys.stdout),
            *([logging.FileHandler(log_file)] if log_file else [])
        ]
    )


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
@click.option('--config', help='Configuration file path')
@click.pass_context
def cli(ctx: click.Context, verbose: bool, log_file: Optional[str], config: Optional[str]) -> None:
    """
    Markdown Converter - Convert documents to clean, readable markdown.
    
    A powerful tool for converting various document formats to markdown
    optimized for LLM processing with support for batch and grid processing.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Setup logging
    setup_logging(verbose, log_file)
    
    # Load configuration
    ctx.obj['config'] = load_config(config)
    
    # Store options
    ctx.obj['verbose'] = verbose


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
    """
    Convert a single file to markdown.
    
    INPUT_FILE: Path to the input document
    OUTPUT_FILE: Path for the output file (optional, auto-generated if not provided)
    """
    try:
        # Generate output path if not provided
        if output_file is None:
            output_file = input_file.with_suffix(f'.{output_format}')
        
        click.echo(f"🔄 Converting {input_file} to {output_file}...")
        
        # Create conversion engine
        engine = ConversionEngine()
        
        # Convert the document
        result = engine.convert_document(
            str(input_file),
            str(output_file),
            output_format=output_format
        )
        
        if result:
            click.echo(f"✅ Successfully converted {input_file} to {output_file}")
        else:
            click.echo(f"❌ Failed to convert {input_file}")
            sys.exit(1)
            
    except ConversionError as e:
        click.echo(f"❌ Conversion error: {e}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        if ctx.obj['verbose']:
            import traceback
            traceback.print_exc()
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
        
        # Create batch processor
        processor = BatchProcessor(config)
        
        # Process the directory
        stats = processor.process_directory(input_dir, output_dir)
        
        # Print results
        print_processing_stats(stats)
        
        if stats.failed_files > 0:
            click.echo(f"\n⚠️  {stats.failed_files} files failed to convert")
            if not continue_on_error:
                sys.exit(1)
        else:
            click.echo(f"\n✅ All files converted successfully!")
            
    except BatchProcessingError as e:
        click.echo(f"❌ Batch processing error: {e}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        if ctx.obj['verbose']:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument('output_dir', type=click.Path(path_type=Path), required=False)
@click.option('--cluster-type', default='local', type=click.Choice(['local', 'remote']),
              help='Type of Dask cluster to use')
@click.option('--scheduler-address', help='Remote scheduler address')
@click.option('--workers', '-w', default=4, type=int,
              help='Number of worker processes')
@click.option('--memory-limit', default='2GB', help='Memory limit per worker')
@click.option('--dashboard/--no-dashboard', default=True,
              help='Enable Dask dashboard')
@click.option('--job-timeout', default=3600, type=int,
              help='Job timeout in seconds')
@click.pass_context
def grid(ctx: click.Context, input_dir: Path, output_dir: Optional[Path],
         cluster_type: str, scheduler_address: Optional[str], workers: int,
         memory_limit: str, dashboard: bool, job_timeout: int) -> None:
    """
    Convert files using distributed grid processing with Dask.
    
    INPUT_DIR: Directory containing files to convert
    OUTPUT_DIR: Output directory (optional, auto-generated if not provided)
    """
    try:
        # Check if Dask is available
        try:
            import dask
        except ImportError:
            click.echo("❌ Dask is required for grid processing. Install with: pip install dask[distributed]")
            sys.exit(1)
        
        # Generate output directory if not provided
        if output_dir is None:
            output_dir = input_dir.parent / f"{input_dir.name}_converted"
        
        click.echo(f"🔄 Starting grid conversion from {input_dir} to {output_dir}...")
        
        # Setup grid processor configuration
        config = ctx.obj['config'].copy()
        config.update({
            'cluster_type': cluster_type,
            'scheduler_address': scheduler_address,
            'n_workers': workers,
            'memory_limit_per_worker': memory_limit,
            'dashboard_address': ':8787' if dashboard else None,
            'job_timeout': job_timeout,
        })
        
        # Create grid processor
        processor = GridProcessor(config)
        
        # Start cluster
        cluster_info = processor.start_cluster()
        click.echo(f"🚀 Started cluster: {cluster_info.scheduler_address}")
        if dashboard:
            click.echo(f"📊 Dashboard available at: http://localhost:8787")
        
        try:
            # Submit job
            job_info = processor.submit_job(input_dir, output_dir)
            click.echo(f"📋 Submitted job: {job_info.job_id}")
            
            # Monitor job
            while True:
                status = processor.get_job_status(job_info.job_id)
                if status and status.status in ['completed', 'failed', 'cancelled']:
                    break
                
                click.echo(f"⏳ Job status: {status.status if status else 'unknown'}")
                import time
                time.sleep(5)
            
            # Get final status
            final_status = processor.get_job_status(job_info.job_id)
            if final_status:
                if final_status.status == 'completed':
                    click.echo(f"✅ Job completed successfully!")
                    click.echo(f"   Processed: {final_status.completed_tasks} tasks")
                    click.echo(f"   Failed: {final_status.failed_tasks} tasks")
                else:
                    click.echo(f"❌ Job {final_status.status}")
                    sys.exit(1)
            
        finally:
            # Stop cluster
            processor.stop_cluster()
            click.echo("🛑 Stopped cluster")
            
    except GridProcessingError as e:
        click.echo(f"❌ Grid processing error: {e}")
        sys.exit(1)
    except DependencyError as e:
        click.echo(f"❌ Dependency error: {e}")
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
    """Show supported input and output formats."""
    print_supported_formats()
    
    click.echo("\n📤 Supported Output Formats:")
    output_formats = [
        ("Markdown", "markdown", "Clean, readable markdown optimized for LLM processing"),
        ("HTML", "html", "HTML with preserved formatting"),
        ("PDF", "pdf", "PDF output (requires LaTeX)"),
        ("Plain Text", "txt", "Plain text with basic formatting"),
    ]
    
    for name, format_id, description in output_formats:
        click.echo(f"  {name} ({format_id}): {description}")


def main() -> None:
    """Main entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main() 