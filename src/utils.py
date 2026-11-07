"""
Utility functions for logging, file integrity, checksum verification,
and configuration management across the agribusiness data science pipeline.
"""

import hashlib
import json
import logging
import os
import sys
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, Optional


def setup_logger(
    name: str = "agribusiness_pipeline",
    log_file: Optional[Path] = None,
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Configures and returns a standardized logger with consistent formatting.

    Args:
        name: Name of the logger instance.
        log_file: Optional Path to write logs to disk.
        level: Logging verbosity level (default INFO).

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding duplicate handlers if setup is called multiple times
    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | [%(filename)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(str(log_file), encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger


logger = setup_logger()


def calculate_sha256(filepath: Path) -> str:
    """
    Calculates the SHA-256 cryptographic hash of a file for data provenance.

    Args:
        filepath: Path to the file.

    Returns:
        str: Hexadecimal SHA-256 digest string.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"File not found for checksum: {filepath}")

    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def update_data_manifest(
    manifest_path: Path,
    file_path: Path,
    source_name: str,
    source_url: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Updates or creates an immutable audit manifest for tracking raw data downloads.

    Args:
        manifest_path: Path to the JSON manifest file.
        file_path: Path to the ingested dataset.
        source_name: Human-readable identifier for the dataset.
        source_url: Source URL or API endpoint.
        metadata: Optional dictionary with additional metadata (rows, columns, encoding).
    """
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_data = {}

    if manifest_path.exists():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
        except json.JSONDecodeError:
            logger.warning(f"Could not parse manifest at {manifest_path}. Creating new manifest.")

    sha256 = calculate_sha256(file_path)
    file_stat = file_path.stat()

    manifest_data[file_path.name] = {
        "source_name": source_name,
        "source_url": source_url,
        "file_size_bytes": file_stat.st_size,
        "sha256": sha256,
        "ingested_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(file_stat.st_mtime)),
        "metadata": metadata or {},
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)

    logger.info(f"Manifest updated for {file_path.name} (SHA-256: {sha256[:12]}...)")


def timeit(func: Callable) -> Callable:
    """
    Decorator to log execution time of computational or ingestion steps.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"Starting execution of '{func.__name__}'...")
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        logger.info(f"Completed '{func.__name__}' in {elapsed:.3f} seconds.")
        return result
    return wrapper


def ensure_directory(path: Path) -> Path:
    """
    Ensures that a specified directory exists, creating parents if necessary.

    Args:
        path: Path object representing the directory.

    Returns:
        Path: The confirmed directory path.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path
