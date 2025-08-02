"""
Grid Processor

This module provides distributed computing capabilities for large-scale
document conversion using Dask for multi-node processing and cluster support.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Tuple
from dataclasses import dataclass
import time
import json

try:
    import dask
    import dask.distributed
    from dask.distributed import Client, LocalCluster
    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False

from .exceptions import GridProcessingError, DependencyError
from .batch_processor import BatchProcessor, ProcessingStats, ProcessingResult


@dataclass
class ClusterInfo:
    """Information about the Dask cluster."""
    scheduler_address: str
    dashboard_address: str
    n_workers: int
    n_threads: int
    memory_limit: str
    status: str


@dataclass
class JobInfo:
    """Information about a distributed job."""
    job_id: str
    status: str
    submitted_time: float
    completed_time: Optional[float] = None
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0


class GridProcessor:
    """
    Distributed grid processor for large-scale document conversion.
    
    Uses Dask for distributed processing across multiple nodes,
    with cluster management and job monitoring.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the grid processor.
        
        :param config: Configuration dictionary
        """
        if not DASK_AVAILABLE:
            raise DependencyError("Dask is required for grid processing. Install with: pip install dask[distributed]")
        
        self.config = config or {}
        self.logger = logging.getLogger("GridProcessor")
        self._setup_default_config()
        self._setup_components()
    
    def _setup_default_config(self) -> None:
        """Setup default configuration for grid processing."""
        self.default_config = {
            # Cluster settings
            "cluster_type": "local",  # 'local', 'remote', 'kubernetes'
            "scheduler_address": None,  # Remote scheduler address
            "n_workers": 4,
            "n_threads_per_worker": 2,
            "memory_limit_per_worker": "2GB",
            "dashboard_address": ":8787",
            
            # Job settings
            "job_timeout": 3600,  # 1 hour
            "max_jobs": 10,
            "job_retries": 3,
            
            # Resource monitoring
            "monitor_resources": True,
            "resource_check_interval": 30,  # seconds
            "max_memory_usage": 0.8,  # 80%
            "max_cpu_usage": 0.9,  # 90%
            
            # File distribution
            "chunk_size": 50,  # Files per task
            "max_file_size_mb": 50,  # Skip files larger than 50MB
            "supported_extensions": [
                '.docx', '.doc', '.pdf', '.xlsx', '.xls', '.xlsb',
                '.html', '.htm', '.txt', '.rtf', '.odt', '.ods', '.odp'
            ],
            
            # Output settings
            "preserve_directory_structure": True,
            "overwrite_existing": False,
            "create_backups": False,
            
            # Monitoring
            "enable_dashboard": True,
            "log_job_progress": True,
            "save_job_logs": True,
        }
        
        # Merge with user config
        if self.config:
            self.default_config.update(self.config)
    
    def _setup_components(self) -> None:
        """Setup processing components."""
        self.batch_processor = BatchProcessor(self.default_config)
        self.client = None
        self.cluster = None
        self.active_jobs = {}
    
    def start_cluster(self) -> ClusterInfo:
        """
        Start a Dask cluster.
        
        :return: Cluster information
        """
        try:
            if self.default_config["cluster_type"] == "local":
                self.cluster = LocalCluster(
                    n_workers=self.default_config["n_workers"],
                    threads_per_worker=self.default_config["n_threads_per_worker"],
                    memory_limit=self.default_config["memory_limit_per_worker"],
                    dashboard_address=self.default_config["dashboard_address"] if self.default_config["enable_dashboard"] else None
                )
                self.client = Client(self.cluster)
            elif self.default_config["cluster_type"] == "remote":
                if not self.default_config["scheduler_address"]:
                    raise GridProcessingError("Scheduler address required for remote cluster")
                self.client = Client(self.default_config["scheduler_address"])
            else:
                raise GridProcessingError(f"Unsupported cluster type: {self.default_config['cluster_type']}")
            
            # Get cluster information
            cluster_info = ClusterInfo(
                scheduler_address=self.client.scheduler.address,
                dashboard_address=self.client.dashboard_link,
                n_workers=len(self.client.scheduler_info()["workers"]),
                n_threads=self.default_config["n_workers"] * self.default_config["n_threads_per_worker"],
                memory_limit=self.default_config["memory_limit_per_worker"],
                status="running"
            )
            
            self.logger.info(f"Started cluster: {cluster_info}")
            return cluster_info
            
        except Exception as e:
            self.logger.error(f"Failed to start cluster: {e}")
            raise GridProcessingError(f"Failed to start cluster: {e}")
    
    def stop_cluster(self) -> None:
        """Stop the Dask cluster."""
        if self.client:
            self.client.close()
        if self.cluster:
            self.cluster.close()
        self.logger.info("Cluster stopped")
    
    def submit_job(self, input_dir: Union[str, Path], output_dir: Optional[Union[str, Path]] = None) -> JobInfo:
        """
        Submit a job for distributed processing.
        
        :param input_dir: Input directory path
        :param output_dir: Output directory path (optional)
        :return: Job information
        """
        if not self.client:
            raise GridProcessingError("No active cluster. Call start_cluster() first.")
        
        job_id = f"job_{int(time.time())}"
        
        # Create job info
        job_info = JobInfo(
            job_id=job_id,
            status="submitted",
            submitted_time=time.time()
        )
        
        # Submit the job
        try:
            future = self.client.submit(
                self._process_job_distributed,
                str(input_dir),
                str(output_dir) if output_dir else None,
                job_id,
                key=job_id
            )
            
            # Store job info
            self.active_jobs[job_id] = {
                "future": future,
                "info": job_info,
                "input_dir": input_dir,
                "output_dir": output_dir
            }
            
            self.logger.info(f"Submitted job {job_id} for processing {input_dir}")
            return job_info
            
        except Exception as e:
            self.logger.error(f"Failed to submit job {job_id}: {e}")
            raise GridProcessingError(f"Failed to submit job: {e}")
    
    def _process_job_distributed(self, input_dir: str, output_dir: Optional[str], job_id: str) -> Dict[str, Any]:
        """
        Process a job in the distributed environment.
        
        :param input_dir: Input directory path
        :param output_dir: Output directory path
        :param job_id: Job ID
        :return: Job results
        """
        try:
            # Update job status
            self._update_job_status(job_id, "running")
            
            # Process the directory
            stats = self.batch_processor.process_directory(input_dir, output_dir)
            
            # Update job status
            self._update_job_status(job_id, "completed")
            
            return {
                "job_id": job_id,
                "status": "completed",
                "stats": {
                    "total_files": stats.total_files,
                    "processed_files": stats.processed_files,
                    "failed_files": stats.failed_files,
                    "skipped_files": stats.skipped_files,
                    "processing_time": stats.end_time - stats.start_time if stats.end_time else 0
                }
            }
            
        except Exception as e:
            self._update_job_status(job_id, "failed")
            self.logger.error(f"Job {job_id} failed: {e}")
            return {
                "job_id": job_id,
                "status": "failed",
                "error": str(e)
            }
    
    def _update_job_status(self, job_id: str, status: str) -> None:
        """
        Update job status.
        
        :param job_id: Job ID
        :param status: New status
        """
        if job_id in self.active_jobs:
            self.active_jobs[job_id]["info"].status = status
            if status in ["completed", "failed"]:
                self.active_jobs[job_id]["info"].completed_time = time.time()
    
    def get_job_status(self, job_id: str) -> Optional[JobInfo]:
        """
        Get status of a specific job.
        
        :param job_id: Job ID
        :return: Job information or None if not found
        """
        if job_id in self.active_jobs:
            return self.active_jobs[job_id]["info"]
        return None
    
    def get_all_jobs(self) -> List[JobInfo]:
        """
        Get status of all active jobs.
        
        :return: List of job information
        """
        return [job["info"] for job in self.active_jobs.values()]
    
    def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a running job.
        
        :param job_id: Job ID
        :return: True if job was cancelled successfully
        """
        if job_id in self.active_jobs:
            try:
                future = self.active_jobs[job_id]["future"]
                future.cancel()
                self._update_job_status(job_id, "cancelled")
                self.logger.info(f"Cancelled job {job_id}")
                return True
            except Exception as e:
                self.logger.error(f"Failed to cancel job {job_id}: {e}")
                return False
        return False
    
    def get_cluster_info(self) -> Optional[ClusterInfo]:
        """
        Get information about the current cluster.
        
        :return: Cluster information or None if no cluster
        """
        if not self.client:
            return None
        
        try:
            scheduler_info = self.client.scheduler_info()
            return ClusterInfo(
                scheduler_address=self.client.scheduler.address,
                dashboard_address=self.client.dashboard_link,
                n_workers=len(scheduler_info["workers"]),
                n_threads=self.default_config["n_workers"] * self.default_config["n_threads_per_worker"],
                memory_limit=self.default_config["memory_limit_per_worker"],
                status="running"
            )
        except Exception as e:
            self.logger.error(f"Failed to get cluster info: {e}")
            return None
    
    def get_resource_usage(self) -> Dict[str, Any]:
        """
        Get current resource usage.
        
        :return: Resource usage information
        """
        if not self.client:
            return {}
        
        try:
            # Get cluster metrics
            metrics = self.client.get_worker_logs()
            
            # Calculate resource usage
            total_memory = 0
            total_cpu = 0
            worker_count = 0
            
            for worker_id, worker_info in self.client.scheduler_info()["workers"].items():
                total_memory += worker_info.get("memory", 0)
                total_cpu += worker_info.get("cpu", 0)
                worker_count += 1
            
            return {
                "total_workers": worker_count,
                "total_memory_gb": total_memory / (1024**3),
                "total_cpu_percent": total_cpu,
                "active_jobs": len(self.active_jobs),
                "dashboard_url": self.client.dashboard_link
            }
        except Exception as e:
            self.logger.error(f"Failed to get resource usage: {e}")
            return {}
    
    def cleanup_completed_jobs(self) -> int:
        """
        Clean up completed jobs from memory.
        
        :return: Number of jobs cleaned up
        """
        cleaned_count = 0
        jobs_to_remove = []
        
        for job_id, job_data in self.active_jobs.items():
            future = job_data["future"]
            if future.done():
                jobs_to_remove.append(job_id)
                cleaned_count += 1
        
        for job_id in jobs_to_remove:
            del self.active_jobs[job_id]
        
        if cleaned_count > 0:
            self.logger.info(f"Cleaned up {cleaned_count} completed jobs")
        
        return cleaned_count
    
    def get_processor_info(self) -> Dict[str, Any]:
        """
        Get information about this processor.
        
        :return: Dictionary with processor information
        """
        return {
            "name": "GridProcessor",
            "description": "Distributed grid processor for large-scale document conversion",
            "cluster_type": self.default_config["cluster_type"],
            "n_workers": self.default_config["n_workers"],
            "dask_available": DASK_AVAILABLE,
            "config": self.default_config
        } 