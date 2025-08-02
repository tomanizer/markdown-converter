"""
Advanced Logging System

This module provides comprehensive logging capabilities for the markdown converter,
including structured JSON logging, retry logic, monitoring, and error tracking.
"""

import json
import logging
import logging.handlers
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Callable
from dataclasses import dataclass, asdict
from contextlib import contextmanager
import threading
import psutil
import os

from .core.exceptions import (
    MarkdownConverterError, 
    RetryableError, 
    ConversionError,
    BatchProcessingError,
    GridProcessingError
)


@dataclass
class LogEntry:
    """Structured log entry for JSON logging."""
    timestamp: str
    level: str
    logger: str
    message: str
    module: str
    function: str
    line: int
    thread_id: int
    process_id: int
    extra: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        if result['extra'] is None:
            result['extra'] = {}
        return result


@dataclass
class PerformanceMetrics:
    """Performance metrics for monitoring."""
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_usage_percent: float
    active_threads: int
    timestamp: str


@dataclass
class ErrorReport:
    """Detailed error report for tracking."""
    error_type: str
    error_message: str
    stack_trace: str
    context: Dict[str, Any]
    timestamp: str
    retry_count: int = 0
    max_retries: int = 3
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def __init__(self, include_extra: bool = True):
        super().__init__()
        self.include_extra = include_extra
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        # Get extra fields from the record
        extra_fields = {}
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename', 
                          'module', 'lineno', 'funcName', 'created', 'msecs', 'relativeCreated', 
                          'thread', 'threadName', 'processName', 'process', 'getMessage', 'exc_info', 
                          'exc_text', 'stack_info', 'msg', 'args']:
                extra_fields[key] = value
        
        log_entry = LogEntry(
            timestamp=datetime.fromtimestamp(record.created).isoformat(),
            level=record.levelname,
            logger=record.name,
            message=record.getMessage(),
            module=record.module,
            function=record.funcName,
            line=record.lineno,
            thread_id=record.thread,
            process_id=record.process,
            extra=extra_fields
        )
        
        # Add exception info if present
        if record.exc_info:
            log_entry.extra['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        return json.dumps(log_entry.to_dict(), default=str)


class RetryHandler:
    """Handler for retryable operations with exponential backoff."""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.logger = logging.getLogger("RetryHandler")
    
    def retry(self, operation: Callable, *args, **kwargs) -> Any:
        """
        Execute operation with retry logic.
        
        :param operation: Function to execute
        :param args: Positional arguments for operation
        :param kwargs: Keyword arguments for operation
        :return: Result of operation
        :raises: Last exception if all retries fail
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return operation(*args, **kwargs)
            except RetryableError as e:
                last_exception = e
                if attempt < self.max_retries:
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    self.logger.warning(
                        f"Retryable error on attempt {attempt + 1}/{self.max_retries + 1}: {e.message}. "
                        f"Retrying in {delay:.2f} seconds..."
                    )
                    time.sleep(delay)
                else:
                    self.logger.error(f"Operation failed after {self.max_retries + 1} attempts")
                    raise
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    self.logger.warning(
                        f"Unexpected error on attempt {attempt + 1}/{self.max_retries + 1}: {str(e)}. "
                        f"Retrying in {delay:.2f} seconds..."
                    )
                    time.sleep(delay)
                else:
                    self.logger.error(f"Operation failed after {self.max_retries + 1} attempts")
                    raise
        
        raise last_exception


class PerformanceMonitor:
    """Monitor system performance and resource usage."""
    
    def __init__(self, check_interval: float = 30.0):
        self.check_interval = check_interval
        self.logger = logging.getLogger("PerformanceMonitor")
        self.metrics_history: List[PerformanceMetrics] = []
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self) -> None:
        """Start performance monitoring in background thread."""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Performance monitoring started")
    
    def stop_monitoring(self) -> None:
        """Stop performance monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        self.logger.info("Performance monitoring stopped")
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring:
            try:
                metrics = self._collect_metrics()
                self.metrics_history.append(metrics)
                
                # Log if resource usage is high
                if metrics.cpu_percent > 80 or metrics.memory_percent > 80:
                    self.logger.warning(
                        f"High resource usage detected: CPU {metrics.cpu_percent:.1f}%, "
                        f"Memory {metrics.memory_percent:.1f}%"
                    )
                
                time.sleep(self.check_interval)
            except Exception as e:
                self.logger.error(f"Error in performance monitoring: {e}")
                time.sleep(self.check_interval)
    
    def _collect_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics."""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return PerformanceMetrics(
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / (1024 * 1024),
            disk_usage_percent=disk.percent,
            active_threads=threading.active_count(),
            timestamp=datetime.now().isoformat()
        )
    
    def get_current_metrics(self) -> PerformanceMetrics:
        """Get current performance metrics."""
        return self._collect_metrics()
    
    def get_metrics_history(self) -> List[PerformanceMetrics]:
        """Get performance metrics history."""
        return self.metrics_history.copy()


class ErrorTracker:
    """Track and analyze errors for monitoring and debugging."""
    
    def __init__(self):
        self.errors: List[ErrorReport] = []
        self.logger = logging.getLogger("ErrorTracker")
        self.lock = threading.Lock()
    
    def track_error(self, error: Exception, context: Dict[str, Any] = None, retry_count: int = 0) -> None:
        """
        Track an error for analysis.
        
        :param error: The exception that occurred
        :param context: Additional context information
        :param retry_count: Current retry attempt number
        """
        with self.lock:
            error_report = ErrorReport(
                error_type=type(error).__name__,
                error_message=str(error),
                stack_trace=traceback.format_exc(),
                context=context or {},
                timestamp=datetime.now().isoformat(),
                retry_count=retry_count
            )
            
            self.errors.append(error_report)
            
            # Log error with structured information
            self.logger.error(
                f"Error tracked: {error_report.error_type} - {error_report.error_message}",
                extra={
                    'error_report': error_report.to_dict(),
                    'context': context
                }
            )
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of tracked errors."""
        with self.lock:
            if not self.errors:
                return {"total_errors": 0}
            
            error_types = {}
            for error in self.errors:
                error_type = error.error_type
                error_types[error_type] = error_types.get(error_type, 0) + 1
            
            return {
                "total_errors": len(self.errors),
                "error_types": error_types,
                "recent_errors": [
                    {
                        "type": e.error_type,
                        "message": e.error_message,
                        "timestamp": e.timestamp,
                        "retry_count": e.retry_count
                    }
                    for e in self.errors[-10:]  # Last 10 errors
                ]
            }
    
    def clear_errors(self) -> None:
        """Clear tracked errors."""
        with self.lock:
            self.errors.clear()


class LoggingManager:
    """Centralized logging management for the markdown converter."""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("MarkdownConverter")
        self.retry_handler = RetryHandler(
            max_retries=self.config.get('max_retries', 3),
            base_delay=self.config.get('retry_delay', 1.0)
        )
        self.performance_monitor = PerformanceMonitor(
            check_interval=self.config.get('performance_check_interval', 30.0)
        )
        self.error_tracker = ErrorTracker()
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        # Clear existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Get logging configuration
        log_level = getattr(logging, self.config.get('log_level', 'INFO').upper())
        log_format = self.config.get('log_format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_file = self.config.get('log_file')
        structured = self.config.get('structured_logging', False)
        console_output = self.config.get('console_output', True)
        
        # Create formatter
        if structured:
            formatter = StructuredFormatter()
        else:
            formatter = logging.Formatter(log_format)
        
        # Console handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # File handler
        if log_file:
            # Ensure log directory exists
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        
        self.logger.setLevel(log_level)
    
    def log_operation_start(self, operation: str, **kwargs) -> None:
        """Log the start of an operation."""
        self.logger.info(f"Starting operation: {operation}", extra=kwargs)
    
    def log_operation_success(self, operation: str, duration: float = None, **kwargs) -> None:
        """Log the successful completion of an operation."""
        message = f"Operation completed successfully: {operation}"
        if duration is not None:
            message += f" (duration: {duration:.2f}s)"
        self.logger.info(message, extra=kwargs)
    
    def log_operation_error(self, operation: str, error: Exception, **kwargs) -> None:
        """Log an operation error."""
        self.error_tracker.track_error(error, kwargs)
        self.logger.error(f"Operation failed: {operation} - {error}", extra=kwargs)
    
    @contextmanager
    def operation_context(self, operation: str, **kwargs):
        """Context manager for logging operations."""
        start_time = time.time()
        self.log_operation_start(operation, **kwargs)
        
        try:
            yield
            duration = time.time() - start_time
            self.log_operation_success(operation, duration, **kwargs)
        except Exception as e:
            duration = time.time() - start_time
            self.log_operation_error(operation, e, duration=duration, **kwargs)
            raise
    
    def retry_operation(self, operation: Callable, *args, **kwargs) -> Any:
        """Execute operation with retry logic."""
        return self.retry_handler.retry(operation, *args, **kwargs)
    
    def start_performance_monitoring(self) -> None:
        """Start performance monitoring."""
        self.performance_monitor.start_monitoring()
    
    def stop_performance_monitoring(self) -> None:
        """Stop performance monitoring."""
        self.performance_monitor.stop_monitoring()
    
    def get_performance_metrics(self) -> PerformanceMetrics:
        """Get current performance metrics."""
        return self.performance_monitor.get_current_metrics()
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get error summary."""
        return self.error_tracker.get_error_summary()
    
    def health_check(self) -> Dict[str, Any]:
        """Perform a health check of the system."""
        try:
            metrics = self.get_performance_metrics()
            error_summary = self.get_error_summary()
            
            # Determine health status
            health_status = "healthy"
            if metrics.cpu_percent > 90 or metrics.memory_percent > 90:
                health_status = "critical"
            elif metrics.cpu_percent > 80 or metrics.memory_percent > 80:
                health_status = "warning"
            
            return {
                "status": health_status,
                "timestamp": datetime.now().isoformat(),
                "performance": {
                    "cpu_percent": metrics.cpu_percent,
                    "memory_percent": metrics.memory_percent,
                    "memory_used_mb": metrics.memory_used_mb,
                    "disk_usage_percent": metrics.disk_usage_percent,
                    "active_threads": metrics.active_threads
                },
                "errors": error_summary
            }
        except Exception as e:
            return {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }


# Global logging manager instance
_logging_manager: Optional[LoggingManager] = None


def get_logging_manager(config: Dict[str, Any] = None) -> LoggingManager:
    """Get or create the global logging manager."""
    global _logging_manager
    if _logging_manager is None:
        _logging_manager = LoggingManager(config)
    return _logging_manager


def setup_logging(config: Dict[str, Any] = None) -> LoggingManager:
    """Setup logging system with configuration."""
    return get_logging_manager(config)


def log_operation(operation: str):
    """Decorator for logging operations."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            manager = get_logging_manager()
            with manager.operation_context(operation):
                return func(*args, **kwargs)
        return wrapper
    return decorator 