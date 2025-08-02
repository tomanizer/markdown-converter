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
from .logging_system import setup_logging, get_logging_manager


def setup_cli_logging(verbose: bool = False, log_file: Optional[str] = None, structured: bool = False) -> None:
    """
    Setup logging configuration for CLI.
    
    :param verbose: Enable verbose logging
    :param log_file: Optional log file path
    :param structured: Enable structured JSON logging
    """
    config = {
        'log_level': 'DEBUG' if verbose else 'INFO',
        'log_file': log_file,
        'structured_logging': structured,
        'console_output': True,
        'max_retries': 3,
        'retry_delay': 1.0,
        'performance_check_interval': 30.0
    }
    
    logging_manager = setup_logging(config)
    return logging_manager


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
    logging_manager = setup_cli_logging(verbose, log_file, structured)
    
    # Load configuration
    config_data = load_config(config)
    ctx.obj = {
        'config': config_data,
        'logging_manager': logging_manager
    }
    
    # Start performance monitoring
    logging_manager.start_performance_monitoring()
    
    # Log CLI startup
    logging_manager.logger.info("Markdown Converter CLI started", extra={
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
    logging_manager = ctx.obj['logging_manager']
    
    # Generate output path if not provided
    if output_file is None:
        output_file = input_file.with_suffix(f'.{output_format}')
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with logging_manager.operation_context(
        "file_conversion",
        input_file=str(input_file),
        output_file=str(output_file),
        output_format=output_format,
        preserve_structure=preserve_structure,
        extract_images=extract_images,
        metadata=metadata
    ):
        try:
            # Initialize conversion engine
            engine = ConversionEngine()
            
            # Perform conversion with retry logic
            result = logging_manager.retry_operation(
                engine.convert_document,
                str(input_file),
                str(output_file),
                output_format=output_format
            )
            
            click.echo(f"✅ Successfully converted {input_file} to {output_file}")
            
            # Log success with file size info
            file_size = input_file.stat().st_size / (1024 * 1024)  # MB
            logging_manager.logger.info(
                f"File conversion completed successfully",
                extra={
                    'file_size_mb': file_size,
                    'output_size_mb': output_file.stat().st_size / (1024 * 1024) if output_file.exists() else 0
                }
            )
            
        except Exception as e:
            click.echo(f"❌ Conversion failed: {e}")
            raise click.Abort()


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
    """Show supported input formats."""
    print_supported_formats()


@cli.command()
@click.option('--json', is_flag=True, help='Output health check in JSON format')
@click.pass_context
def health(ctx: click.Context, json: bool) -> None:
    """Check system health and performance."""
    logging_manager = ctx.obj['logging_manager']
    
    # Perform health check
    health_status = logging_manager.health_check()
    
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
            click.echo(f"🧵 Active Threads: {perf['active_threads']}")
        
        if 'errors' in health_status:
            errors = health_status['errors']
            click.echo(f"🚨 Total Errors: {errors.get('total_errors', 0)}")
            
            if 'error_types' in errors and errors['error_types']:
                click.echo("📊 Error Types:")
                for error_type, count in errors['error_types'].items():
                    click.echo(f"  - {error_type}: {count}")
            
            if 'recent_errors' in errors and errors['recent_errors']:
                click.echo("🕒 Recent Errors:")
                for error in errors['recent_errors'][-3:]:  # Show last 3 errors
                    click.echo(f"  - {error['type']}: {error['message']}")


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
    finally:
        # Ensure performance monitoring is stopped
        try:
            from .logging_system import get_logging_manager
            logging_manager = get_logging_manager()
            logging_manager.stop_performance_monitoring()
        except:
            pass


if __name__ == '__main__':
    main() 