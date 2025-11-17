"""
Logging Configuration Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Centralized logging configuration for the Scrapper system.
All logs are written to files in the trace/ directory with NO console output.
"""

import os
from pathlib import Path
from typing import Dict, Any

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
TRACE_DIR = PROJECT_ROOT / "trace"

# Ensure trace directories exist
TRACE_SUBDIRS = [
    "scrapers",      # Logs from individual platform scrapers
    "processing",    # Data processing and normalization logs
    "feeds",         # Feed aggregation and enrichment logs
    "storage",       # Database and cache operation logs
    "monitoring",    # System monitoring and health checks
    "errors",        # Error and exception logs
    "performance"    # Performance metrics and benchmarks
]

for subdir in TRACE_SUBDIRS:
    (TRACE_DIR / subdir).mkdir(parents=True, exist_ok=True)


class LoggingConfig:
    """Centralized logging configuration."""

    # Log levels
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    # Default log level
    DEFAULT_LEVEL = INFO

    # Log file paths
    LOG_PATHS = {
        # Scraper logs
        "twitter": TRACE_DIR / "scrapers" / "twitter.log",
        "tiktok": TRACE_DIR / "scrapers" / "tiktok.log",
        "xiaohongshu": TRACE_DIR / "scrapers" / "xiaohongshu.log",
        "youtube": TRACE_DIR / "scrapers" / "youtube.log",
        "scraper_general": TRACE_DIR / "scrapers" / "general.log",

        # Processing logs
        "normalizer": TRACE_DIR / "processing" / "normalizer.log",
        "trend_detector": TRACE_DIR / "processing" / "trend_detector.log",
        "sentiment_analyzer": TRACE_DIR / "processing" / "sentiment_analyzer.log",
        "processing_general": TRACE_DIR / "processing" / "general.log",

        # Feed logs
        "feed_aggregator": TRACE_DIR / "feeds" / "aggregator.log",
        "feed_enricher": TRACE_DIR / "feeds" / "enricher.log",
        "feed_general": TRACE_DIR / "feeds" / "general.log",

        # Storage logs
        "raw_data_store": TRACE_DIR / "storage" / "raw_data.log",
        "cache_manager": TRACE_DIR / "storage" / "cache.log",
        "storage_general": TRACE_DIR / "storage" / "general.log",

        # Monitoring logs
        "scraping_monitor": TRACE_DIR / "monitoring" / "scraping.log",
        "rate_limiter": TRACE_DIR / "monitoring" / "rate_limiter.log",
        "health_check": TRACE_DIR / "monitoring" / "health.log",
        "monitoring_general": TRACE_DIR / "monitoring" / "general.log",

        # Error logs
        "errors": TRACE_DIR / "errors" / "errors.log",
        "exceptions": TRACE_DIR / "errors" / "exceptions.log",

        # Performance logs
        "performance": TRACE_DIR / "performance" / "metrics.log",
        "benchmark": TRACE_DIR / "performance" / "benchmark.log",

        # Main application log
        "main": TRACE_DIR / "main.log",
    }

    # Log rotation settings
    MAX_BYTES = 10 * 1024 * 1024  # 10 MB per log file
    BACKUP_COUNT = 5  # Keep 5 backup files

    # Log format
    LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    # JSON log format (for structured logging)
    JSON_LOG_FORMAT = {
        "timestamp": "%(asctime)s",
        "level": "%(levelname)s",
        "logger": "%(name)s",
        "module": "%(module)s",
        "function": "%(funcName)s",
        "line": "%(lineno)d",
        "message": "%(message)s",
        "process": "%(process)d",
        "thread": "%(thread)d"
    }

    # Component to log path mapping
    COMPONENT_LOG_MAP = {
        # Scrapers
        "TwitterScraper": "twitter",
        "TikTokScraper": "tiktok",
        "XiaoHongShuScraper": "xiaohongshu",
        "YouTubeScraper": "youtube",

        # Processing
        "ContentNormalizer": "normalizer",
        "TrendDetector": "trend_detector",
        "SentimentAnalyzer": "sentiment_analyzer",

        # Feeds
        "FeedAggregator": "feed_aggregator",
        "FeedEnricher": "feed_enricher",

        # Storage
        "RawDataStore": "raw_data_store",
        "CacheManager": "cache_manager",

        # Monitoring
        "ScrapingMonitor": "scraping_monitor",
        "RateLimiter": "rate_limiter",
    }

    @classmethod
    def get_log_path(cls, component_name: str) -> Path:
        """
        Get the log file path for a specific component.

        Args:
            component_name: Name of the component

        Returns:
            Path to the log file
        """
        log_key = cls.COMPONENT_LOG_MAP.get(component_name, "main")
        return cls.LOG_PATHS.get(log_key, cls.LOG_PATHS["main"])

    @classmethod
    def get_log_config_dict(cls) -> Dict[str, Any]:
        """
        Get logging configuration as a dictionary for logging.config.dictConfig.

        Returns:
            Dictionary with logging configuration
        """
        # Ensure all log directories exist
        for log_path in cls.LOG_PATHS.values():
            log_path.parent.mkdir(parents=True, exist_ok=True)

        handlers = {}
        loggers = {}

        # Create a file handler for each log path
        for name, path in cls.LOG_PATHS.items():
            handler_name = f"{name}_file"
            handlers[handler_name] = {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(path),
                "maxBytes": cls.MAX_BYTES,
                "backupCount": cls.BACKUP_COUNT,
                "formatter": "standard",
                "level": cls.DEFAULT_LEVEL,
            }

        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": cls.LOG_FORMAT,
                    "datefmt": cls.DATE_FORMAT,
                },
                "json": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(timestamp)s %(level)s %(name)s %(message)s",
                },
            },
            "handlers": handlers,
            "loggers": loggers,
            "root": {
                "handlers": ["main_file"],
                "level": cls.DEFAULT_LEVEL,
            },
        }
