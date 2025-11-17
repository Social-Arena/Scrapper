"""
Centralized Logger Utility
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provides a unified logging interface for all Scrapper components.
ALL logs are written to files in the trace/ directory with NO console output.

Usage Example:
    from scrapper.utils.logger import get_logger, log_performance, log_error_with_context

    # Get a logger for your component
    logger = get_logger("TwitterScraper")

    # Log messages
    logger.info("Starting to scrape trending topics")
    logger.debug(f"API request to endpoint: {endpoint}")
    logger.warning("Rate limit approaching")
    logger.error("Failed to fetch data", exc_info=True)

    # Log performance metrics
    with log_performance(logger, "scrape_trending_topics"):
        # Your code here
        pass

    # Log errors with context
    try:
        # Your code
        pass
    except Exception as e:
        log_error_with_context(logger, e, {"user_id": user_id, "endpoint": endpoint})
"""

import logging
import logging.handlers
import functools
import time
import json
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from contextlib import contextmanager

from scrapper.config.logging_config import LoggingConfig

# Global registry of loggers
_logger_registry: Dict[str, logging.Logger] = {}
_initialized = False


def initialize_logging(log_level: str = LoggingConfig.DEFAULT_LEVEL) -> None:
    """
    Initialize the logging system.
    This should be called once at application startup.

    Args:
        log_level: The default log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    global _initialized

    if _initialized:
        return

    # Set the default log level
    LoggingConfig.DEFAULT_LEVEL = log_level

    # Ensure all trace directories exist
    for log_path in LoggingConfig.LOG_PATHS.values():
        log_path.parent.mkdir(parents=True, exist_ok=True)

    _initialized = True


def get_logger(
    component_name: str,
    log_level: Optional[str] = None,
    use_json: bool = False
) -> logging.Logger:
    """
    Get or create a logger for a specific component.
    All logs are written to files with NO console output.

    Args:
        component_name: Name of the component (e.g., "TwitterScraper")
        log_level: Optional log level override
        use_json: Whether to use JSON formatting

    Returns:
        Configured logger instance
    """
    global _initialized

    if not _initialized:
        initialize_logging()

    # Return existing logger if already created
    if component_name in _logger_registry:
        return _logger_registry[component_name]

    # Create new logger
    logger = logging.Logger(component_name)
    logger.setLevel(log_level or LoggingConfig.DEFAULT_LEVEL)

    # Get the appropriate log file path
    log_path = LoggingConfig.get_log_path(component_name)

    # Create rotating file handler
    handler = logging.handlers.RotatingFileHandler(
        filename=str(log_path),
        maxBytes=LoggingConfig.MAX_BYTES,
        backupCount=LoggingConfig.BACKUP_COUNT,
        encoding='utf-8'
    )

    # Set formatter
    if use_json:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            LoggingConfig.LOG_FORMAT,
            datefmt=LoggingConfig.DATE_FORMAT
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Also add to errors log for ERROR and above
    if log_level != "DEBUG":
        error_handler = logging.handlers.RotatingFileHandler(
            filename=str(LoggingConfig.LOG_PATHS["errors"]),
            maxBytes=LoggingConfig.MAX_BYTES,
            backupCount=LoggingConfig.BACKUP_COUNT,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)

    # Store in registry
    _logger_registry[component_name] = logger

    return logger


class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
            "process": record.process,
            "thread": record.thread,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info)
            }

        # Add extra fields if present
        if hasattr(record, 'extra_data'):
            log_data["extra"] = record.extra_data

        return json.dumps(log_data, ensure_ascii=False)


@contextmanager
def log_performance(logger: logging.Logger, operation_name: str, **extra_context):
    """
    Context manager to log performance metrics for an operation.

    Args:
        logger: Logger instance
        operation_name: Name of the operation being timed
        **extra_context: Additional context to include in logs

    Usage:
        with log_performance(logger, "scrape_tweets", user_id=123):
            # Your code here
            pass
    """
    start_time = time.time()
    logger.info(f"Starting operation: {operation_name}", extra={"extra_data": extra_context})

    try:
        yield
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(
            f"Operation failed: {operation_name} (elapsed: {elapsed:.2f}s)",
            exc_info=True,
            extra={"extra_data": {**extra_context, "elapsed_seconds": elapsed}}
        )
        raise
    else:
        elapsed = time.time() - start_time
        logger.info(
            f"Operation completed: {operation_name} (elapsed: {elapsed:.2f}s)",
            extra={"extra_data": {**extra_context, "elapsed_seconds": elapsed}}
        )

        # Also log to performance log
        perf_logger = get_logger("performance")
        perf_logger.info(
            f"{operation_name}: {elapsed:.2f}s",
            extra={"extra_data": {**extra_context, "elapsed_seconds": elapsed}}
        )


def log_error_with_context(
    logger: logging.Logger,
    error: Exception,
    context: Optional[Dict[str, Any]] = None,
    include_traceback: bool = True
) -> None:
    """
    Log an error with additional context information.

    Args:
        logger: Logger instance
        error: The exception that occurred
        context: Additional context information
        include_traceback: Whether to include full traceback
    """
    error_data = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context or {}
    }

    if include_traceback:
        error_data["traceback"] = traceback.format_exc()

    logger.error(
        f"Error occurred: {type(error).__name__}: {str(error)}",
        extra={"extra_data": error_data},
        exc_info=include_traceback
    )

    # Also log to exceptions log
    exc_logger = get_logger("exceptions")
    exc_logger.error(
        f"Exception in {logger.name}: {type(error).__name__}: {str(error)}",
        extra={"extra_data": error_data},
        exc_info=include_traceback
    )


def log_api_call(
    logger: logging.Logger,
    endpoint: str,
    method: str = "GET",
    **params
) -> None:
    """
    Log an API call with parameters.

    Args:
        logger: Logger instance
        endpoint: API endpoint
        method: HTTP method
        **params: API parameters
    """
    logger.debug(
        f"API call: {method} {endpoint}",
        extra={"extra_data": {"method": method, "endpoint": endpoint, "params": params}}
    )


def log_data_operation(
    logger: logging.Logger,
    operation: str,
    data_type: str,
    count: int,
    **metadata
) -> None:
    """
    Log a data operation (save, load, delete, etc.).

    Args:
        logger: Logger instance
        operation: Operation name (e.g., "save", "load", "delete")
        data_type: Type of data (e.g., "tweets", "videos", "feeds")
        count: Number of items affected
        **metadata: Additional metadata
    """
    logger.info(
        f"Data operation: {operation} {count} {data_type}",
        extra={"extra_data": {"operation": operation, "data_type": data_type, "count": count, **metadata}}
    )


def log_scraping_session(
    logger: logging.Logger,
    platform: str,
    session_type: str,
    status: str,
    **metrics
) -> None:
    """
    Log a scraping session summary.

    Args:
        logger: Logger instance
        platform: Platform name (e.g., "twitter", "tiktok")
        session_type: Type of scraping session
        status: Session status (e.g., "started", "completed", "failed")
        **metrics: Session metrics (items_scraped, duration, errors, etc.)
    """
    logger.info(
        f"Scraping session {status}: {platform} - {session_type}",
        extra={"extra_data": {"platform": platform, "session_type": session_type, "status": status, **metrics}}
    )


def log_decorator(operation_name: Optional[str] = None):
    """
    Decorator to automatically log function entry, exit, and performance.

    Args:
        operation_name: Optional name for the operation (defaults to function name)

    Usage:
        @log_decorator("scrape_trending_topics")
        def scrape_trending(self):
            pass
    """
    def decorator(func: Callable) -> Callable:
        op_name = operation_name or func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Try to get logger from self (for class methods)
            logger = None
            if args and hasattr(args[0], 'logger'):
                logger = args[0].logger
            else:
                # Fall back to a generic logger
                logger = get_logger("decorator")

            with log_performance(logger, op_name, function=func.__name__):
                return func(*args, **kwargs)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Try to get logger from self (for class methods)
            logger = None
            if args and hasattr(args[0], 'logger'):
                logger = args[0].logger
            else:
                # Fall back to a generic logger
                logger = get_logger("decorator")

            start_time = time.time()
            logger.info(f"Starting async operation: {op_name}")

            try:
                result = await func(*args, **kwargs)
                elapsed = time.time() - start_time
                logger.info(f"Async operation completed: {op_name} (elapsed: {elapsed:.2f}s)")
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                log_error_with_context(
                    logger, e,
                    {"operation": op_name, "elapsed_seconds": elapsed}
                )
                raise

        # Return appropriate wrapper based on whether function is async
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return wrapper

    return decorator


def cleanup_old_logs(days_to_keep: int = 7) -> None:
    """
    Clean up log files older than the specified number of days.

    Args:
        days_to_keep: Number of days to keep logs
    """
    logger = get_logger("cleanup")
    cutoff_time = time.time() - (days_to_keep * 24 * 60 * 60)
    deleted_count = 0

    for log_path in LoggingConfig.LOG_PATHS.values():
        # Check all rotated log files
        log_dir = log_path.parent
        for log_file in log_dir.glob(f"{log_path.stem}*.log*"):
            if log_file.stat().st_mtime < cutoff_time:
                try:
                    log_file.unlink()
                    deleted_count += 1
                    logger.info(f"Deleted old log file: {log_file}")
                except Exception as e:
                    logger.error(f"Failed to delete log file {log_file}: {e}")

    logger.info(f"Cleanup complete. Deleted {deleted_count} old log files.")


# Convenience function to get common loggers
def get_scraper_logger(platform: str) -> logging.Logger:
    """Get a logger for a specific scraper platform."""
    component_name = f"{platform.title()}Scraper"
    return get_logger(component_name)


def get_processing_logger(processor_type: str) -> logging.Logger:
    """Get a logger for a specific data processor."""
    return get_logger(processor_type)


def get_storage_logger(storage_type: str) -> logging.Logger:
    """Get a logger for a specific storage component."""
    return get_logger(storage_type)
