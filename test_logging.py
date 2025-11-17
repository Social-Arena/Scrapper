#!/usr/bin/env python3
"""
Test script to demonstrate the logging system.
Run this to verify that logs are being written to trace/ folder.

Usage:
    python test_logging.py
"""

import time
import asyncio
from scrapper.utils.logger import (
    initialize_logging,
    get_logger,
    log_performance,
    log_error_with_context,
    log_api_call,
    log_data_operation,
    log_scraping_session,
)


def test_basic_logging():
    """Test basic logging at different levels."""
    logger = get_logger("TestComponent")

    print("\n=== Testing Basic Logging ===")
    print("Check trace/main.log for output\n")

    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")


def test_logging_with_context():
    """Test logging with extra context."""
    logger = get_logger("TestComponent")

    print("\n=== Testing Logging with Context ===")
    print("Check trace/main.log for structured output\n")

    logger.info(
        "Processing user data",
        extra={"extra_data": {
            "user_id": 12345,
            "platform": "twitter",
            "action": "scrape_timeline",
            "items_found": 42
        }}
    )


def test_performance_logging():
    """Test performance logging."""
    logger = get_logger("TestComponent")

    print("\n=== Testing Performance Logging ===")
    print("Check trace/main.log and trace/performance/metrics.log\n")

    with log_performance(logger, "test_operation", user_id=123, platform="twitter"):
        # Simulate some work
        time.sleep(1.5)


def test_error_logging():
    """Test error logging with context."""
    logger = get_logger("TestComponent")

    print("\n=== Testing Error Logging ===")
    print("Check trace/errors/errors.log and trace/errors/exceptions.log\n")

    try:
        # Simulate an error
        raise ValueError("This is a test error for demonstration")
    except Exception as e:
        log_error_with_context(
            logger,
            e,
            context={
                "operation": "test_operation",
                "user_id": 12345,
                "endpoint": "/api/test"
            }
        )


def test_api_logging():
    """Test API call logging."""
    logger = get_logger("TestScraper")

    print("\n=== Testing API Call Logging ===")
    print("Check trace/scrapers/general.log\n")

    log_api_call(
        logger,
        endpoint="/trends/place.json",
        method="GET",
        id=1,
        count=50
    )


def test_data_operation_logging():
    """Test data operation logging."""
    logger = get_logger("TestStorage")

    print("\n=== Testing Data Operation Logging ===")
    print("Check trace/storage/general.log\n")

    log_data_operation(
        logger,
        operation="save",
        data_type="tweets",
        count=150,
        platform="twitter",
        database="postgresql"
    )


def test_scraping_session_logging():
    """Test scraping session logging."""
    logger = get_logger("TestScraper")

    print("\n=== Testing Scraping Session Logging ===")
    print("Check trace/scrapers/general.log\n")

    # Session start
    log_scraping_session(
        logger,
        platform="twitter",
        session_type="trending_topics",
        status="started",
        location="global"
    )

    # Simulate work
    time.sleep(0.5)

    # Session complete
    log_scraping_session(
        logger,
        platform="twitter",
        session_type="trending_topics",
        status="completed",
        items_scraped=50,
        duration=0.5,
        errors=0
    )


async def test_async_logging():
    """Test async logging."""
    logger = get_logger("TestAsync")

    print("\n=== Testing Async Logging ===")
    print("Check trace/main.log\n")

    logger.info("Starting async operation")

    # Simulate async work
    await asyncio.sleep(1)

    logger.info("Async operation completed")


def test_multiple_components():
    """Test logging from multiple components."""
    print("\n=== Testing Multiple Components ===")
    print("Check different log files in trace/ subdirectories\n")

    # Create loggers for different components
    twitter_logger = get_logger("TwitterScraper")
    tiktok_logger = get_logger("TikTokScraper")
    normalizer_logger = get_logger("ContentNormalizer")
    feed_logger = get_logger("FeedAggregator")

    # Log from each component
    twitter_logger.info("Scraping Twitter trending topics")
    tiktok_logger.info("Scraping TikTok viral videos")
    normalizer_logger.info("Normalizing content from multiple platforms")
    feed_logger.info("Aggregating feeds")

    print("Check:")
    print("  - trace/scrapers/twitter.log")
    print("  - trace/scrapers/tiktok.log")
    print("  - trace/processing/normalizer.log")
    print("  - trace/feeds/aggregator.log")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("SCRAPPER LOGGING SYSTEM TEST")
    print("="*60)
    print("\nAll logs are written to files in trace/ directory")
    print("NO console output from the logging system itself")
    print("="*60)

    # Initialize logging system
    initialize_logging(log_level="DEBUG")

    # Run tests
    test_basic_logging()
    test_logging_with_context()
    test_performance_logging()
    test_error_logging()
    test_api_logging()
    test_data_operation_logging()
    test_scraping_session_logging()
    test_multiple_components()

    # Run async test
    print("\nRunning async test...")
    asyncio.run(test_async_logging())

    print("\n" + "="*60)
    print("TESTS COMPLETE")
    print("="*60)
    print("\nPlease check the trace/ directory for all log files:")
    print("  - trace/main.log")
    print("  - trace/scrapers/")
    print("  - trace/processing/")
    print("  - trace/feeds/")
    print("  - trace/storage/")
    print("  - trace/errors/")
    print("  - trace/performance/")
    print("\nYou can also read trace/README.md for debugging guidance")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
