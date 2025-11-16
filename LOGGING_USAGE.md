# Logging Usage Guide

Complete guide for using the Scrapper logging system. **Remember: NO console output - all logs are written to files in the `trace/` directory.**

## Table of Contents

1. [Quick Start](#quick-start)
2. [Basic Usage](#basic-usage)
3. [Advanced Usage](#advanced-usage)
4. [Best Practices](#best-practices)
5. [Complete Examples](#complete-examples)

## Quick Start

### Initialize Logging (Do this once at startup)

```python
from scrapper.utils.logger import initialize_logging

# Initialize with default INFO level
initialize_logging()

# Or with custom level
initialize_logging(log_level="DEBUG")
```

### Get a Logger

```python
from scrapper.utils.logger import get_logger

# Get a logger for your component
logger = get_logger("TwitterScraper")

# Use the logger
logger.info("Starting scraping session")
logger.debug("Fetching data from API")
logger.warning("Rate limit approaching")
logger.error("Failed to fetch data", exc_info=True)
```

## Basic Usage

### 1. Simple Logging

```python
from scrapper.utils.logger import get_logger

class TwitterScraper:
    def __init__(self):
        # Get a logger for this component
        self.logger = get_logger("TwitterScraper")

    def scrape_trending_topics(self, location: str = "global"):
        self.logger.info(f"Starting to scrape trending topics for location: {location}")

        try:
            # Your scraping logic here
            topics = self._fetch_topics(location)
            self.logger.info(f"Successfully scraped {len(topics)} trending topics")
            return topics

        except Exception as e:
            self.logger.error(f"Failed to scrape trending topics: {str(e)}", exc_info=True)
            raise
```

### 2. Logging with Context

```python
from scrapper.utils.logger import get_logger

logger = get_logger("ContentNormalizer")

def normalize_tweet(tweet_data: dict):
    # Log with extra context
    logger.debug(
        "Normalizing tweet",
        extra={"extra_data": {
            "tweet_id": tweet_data.get("id"),
            "user_id": tweet_data.get("user", {}).get("id"),
            "has_media": bool(tweet_data.get("media"))
        }}
    )

    # Normalization logic...
```

### 3. Logging Errors with Context

```python
from scrapper.utils.logger import get_logger, log_error_with_context

logger = get_logger("TikTokScraper")

def scrape_video(video_id: str):
    try:
        video_data = fetch_video_data(video_id)
        return video_data

    except Exception as e:
        # Log error with context for better debugging
        log_error_with_context(
            logger,
            e,
            context={
                "video_id": video_id,
                "endpoint": "/video/detail",
                "user_agent": "TikTokBot/1.0"
            }
        )
        raise
```

## Advanced Usage

### 1. Performance Logging

```python
from scrapper.utils.logger import get_logger, log_performance

logger = get_logger("FeedAggregator")

def aggregate_feeds(platforms: list):
    # Automatically log operation start, end, and duration
    with log_performance(logger, "aggregate_feeds", platforms=platforms, count=len(platforms)):
        # Your aggregation logic here
        feeds = []
        for platform in platforms:
            platform_feeds = fetch_platform_feeds(platform)
            feeds.extend(platform_feeds)

        return feeds
```

Output in `trace/feeds/aggregator.log`:
```
[2025-11-16 10:30:45] [INFO] [FeedAggregator] Starting operation: aggregate_feeds
[2025-11-16 10:30:48] [INFO] [FeedAggregator] Operation completed: aggregate_feeds (elapsed: 3.45s)
```

And in `trace/performance/metrics.log`:
```
[2025-11-16 10:30:48] [INFO] [performance] aggregate_feeds: 3.45s
```

### 2. Using Decorators for Automatic Logging

```python
from scrapper.utils.logger import get_logger, log_decorator

class DataProcessor:
    def __init__(self):
        self.logger = get_logger("ContentNormalizer")

    @log_decorator("normalize_content")
    def normalize(self, raw_content: dict):
        # Function automatically logs entry, exit, and performance
        # Your normalization logic here
        return normalized_content

    @log_decorator()  # Uses function name as operation name
    async def async_process(self, content_list: list):
        # Works with async functions too
        results = []
        for content in content_list:
            result = await self.process_single(content)
            results.append(result)
        return results
```

### 3. Specialized Logging Functions

#### Log API Calls

```python
from scrapper.utils.logger import get_logger, log_api_call

logger = get_logger("TwitterScraper")

def fetch_trends(location_id: str):
    endpoint = "/trends/place.json"
    params = {"id": location_id}

    # Log the API call
    log_api_call(logger, endpoint, method="GET", **params)

    response = api_client.get(endpoint, params=params)
    return response.json()
```

Output:
```
[2025-11-16 10:30:45] [DEBUG] [TwitterScraper] API call: GET /trends/place.json
```

#### Log Data Operations

```python
from scrapper.utils.logger import get_logger, log_data_operation

logger = get_logger("RawDataStore")

def save_tweets(tweets: list):
    # Log the data operation
    log_data_operation(
        logger,
        operation="save",
        data_type="tweets",
        count=len(tweets),
        platform="twitter",
        timestamp=datetime.now().isoformat()
    )

    # Save logic...
    db.insert_many(tweets)
```

Output:
```
[2025-11-16 10:30:45] [INFO] [RawDataStore] Data operation: save 150 tweets
```

#### Log Scraping Sessions

```python
from scrapper.utils.logger import get_logger, log_scraping_session

logger = get_logger("YouTubeScraper")

def scrape_trending_videos():
    # Log session start
    log_scraping_session(
        logger,
        platform="youtube",
        session_type="trending_videos",
        status="started",
        region="US"
    )

    try:
        videos = fetch_trending_videos()

        # Log session completion
        log_scraping_session(
            logger,
            platform="youtube",
            session_type="trending_videos",
            status="completed",
            items_scraped=len(videos),
            duration=duration,
            errors=0
        )

        return videos

    except Exception as e:
        # Log session failure
        log_scraping_session(
            logger,
            platform="youtube",
            session_type="trending_videos",
            status="failed",
            error=str(e)
        )
        raise
```

### 4. JSON Structured Logging

```python
from scrapper.utils.logger import get_logger

# Get logger with JSON formatting
logger = get_logger("TrendDetector", use_json=True)

logger.info(
    "Detected emerging trend",
    extra={"extra_data": {
        "trend_id": "trend_123",
        "keyword": "#viral",
        "velocity": 145.3,
        "platforms": ["twitter", "tiktok"],
        "confidence": 0.89
    }}
)
```

Output in JSON format:
```json
{
  "timestamp": "2025-11-16 10:30:45",
  "level": "INFO",
  "logger": "TrendDetector",
  "message": "Detected emerging trend",
  "extra": {
    "trend_id": "trend_123",
    "keyword": "#viral",
    "velocity": 145.3,
    "platforms": ["twitter", "tiktok"],
    "confidence": 0.89
  }
}
```

## Best Practices

### 1. Choose the Right Log Level

```python
# DEBUG - Detailed diagnostic info (API parameters, data transformations)
logger.debug(f"Fetching user timeline with params: {params}")

# INFO - General flow and operations
logger.info(f"Scraped {count} tweets from user timeline")

# WARNING - Concerning but not critical issues
logger.warning(f"Rate limit at 80%, slowing down requests")

# ERROR - Errors that need attention
logger.error(f"Failed to connect to API: {error}", exc_info=True)

# CRITICAL - System-threatening errors
logger.critical("Database connection lost, unable to save data")
```

### 2. Include Relevant Context

```python
# Bad - Not enough context
logger.error("Failed to save data")

# Good - Includes context for debugging
logger.error(
    "Failed to save tweet data to database",
    extra={"extra_data": {
        "tweet_id": tweet_id,
        "user_id": user_id,
        "platform": "twitter",
        "error_code": error_code,
        "retry_count": retry_count
    }}
)
```

### 3. Log at Decision Points

```python
def process_content(content: dict):
    if content.get("engagement_score", 0) > 10000:
        logger.info(
            "High-engagement content detected",
            extra={"extra_data": {
                "content_id": content["id"],
                "engagement_score": content["engagement_score"]
            }}
        )
        return process_as_viral(content)
    else:
        logger.debug(f"Processing normal content: {content['id']}")
        return process_normal(content)
```

### 4. Always Log Exceptions

```python
# Use exc_info=True to include full traceback
try:
    result = risky_operation()
except SpecificException as e:
    logger.error("Specific error occurred", exc_info=True)
    # Handle specifically
except Exception as e:
    logger.error("Unexpected error", exc_info=True)
    # Handle generally
```

### 5. Use Consistent Naming

```python
# Component loggers should match class names
class TwitterScraper:
    def __init__(self):
        self.logger = get_logger("TwitterScraper")  # ✓ Good

class FeedAggregator:
    def __init__(self):
        self.logger = get_logger("FeedAggregator")  # ✓ Good

# Or use helper functions
from scrapper.utils.logger import get_scraper_logger

class TikTokScraper:
    def __init__(self):
        self.logger = get_scraper_logger("tiktok")  # Also good
```

## Complete Examples

### Example 1: Complete Scraper Implementation

```python
from scrapper.utils.logger import (
    get_logger,
    log_performance,
    log_error_with_context,
    log_api_call,
    log_scraping_session
)

class TwitterScraper:
    """Twitter data scraper with comprehensive logging."""

    def __init__(self, api_config):
        self.logger = get_logger("TwitterScraper")
        self.api_client = TwitterAPI(api_config)
        self.logger.info("TwitterScraper initialized", extra={"extra_data": {
            "api_version": api_config.version,
            "rate_limit": api_config.rate_limit
        }})

    async def scrape_trending_topics(self, location: str = "global", max_results: int = 50):
        """Scrape trending topics with full logging."""

        # Log session start
        log_scraping_session(
            self.logger,
            platform="twitter",
            session_type="trending_topics",
            status="started",
            location=location,
            max_results=max_results
        )

        # Use performance logging
        with log_performance(self.logger, "scrape_trending_topics", location=location):
            try:
                # Log API call
                endpoint = "/trends/place.json"
                log_api_call(self.logger, endpoint, method="GET", id=location)

                # Fetch data
                response = await self.api_client.get(endpoint, params={"id": location})

                # Parse response
                topics = self._parse_trending_topics(response)

                self.logger.info(
                    f"Successfully scraped {len(topics)} trending topics",
                    extra={"extra_data": {
                        "location": location,
                        "topic_count": len(topics),
                        "top_topic": topics[0]["name"] if topics else None
                    }}
                )

                # Log session completion
                log_scraping_session(
                    self.logger,
                    platform="twitter",
                    session_type="trending_topics",
                    status="completed",
                    items_scraped=len(topics),
                    errors=0
                )

                return topics

            except RateLimitError as e:
                self.logger.warning("Rate limit reached, will retry after cooldown")
                log_scraping_session(
                    self.logger,
                    platform="twitter",
                    session_type="trending_topics",
                    status="rate_limited",
                    retry_after=e.reset_time
                )
                raise

            except Exception as e:
                # Log error with full context
                log_error_with_context(
                    self.logger,
                    e,
                    context={
                        "operation": "scrape_trending_topics",
                        "location": location,
                        "max_results": max_results,
                        "endpoint": endpoint
                    }
                )

                log_scraping_session(
                    self.logger,
                    platform="twitter",
                    session_type="trending_topics",
                    status="failed",
                    error=str(e)
                )
                raise

    def _parse_trending_topics(self, response):
        """Parse API response with logging."""
        self.logger.debug(f"Parsing trending topics from response")

        try:
            topics = []
            for trend in response[0]["trends"]:
                topic = {
                    "name": trend["name"],
                    "tweet_volume": trend.get("tweet_volume", 0),
                    "url": trend["url"]
                }
                topics.append(topic)

            self.logger.debug(f"Parsed {len(topics)} topics successfully")
            return topics

        except (KeyError, IndexError) as e:
            self.logger.error(
                "Failed to parse trending topics response",
                exc_info=True,
                extra={"extra_data": {"response_keys": list(response.keys())}}
            )
            raise
```

### Example 2: Data Processing Pipeline

```python
from scrapper.utils.logger import get_logger, log_performance, log_data_operation

class ContentNormalizer:
    """Normalize content from different platforms."""

    def __init__(self):
        self.logger = get_logger("ContentNormalizer")

    def normalize_batch(self, raw_contents: list, platform: str):
        """Normalize a batch of content."""

        self.logger.info(
            f"Starting batch normalization",
            extra={"extra_data": {
                "platform": platform,
                "batch_size": len(raw_contents)
            }}
        )

        normalized = []
        errors = []

        with log_performance(self.logger, "normalize_batch", platform=platform, count=len(raw_contents)):
            for idx, content in enumerate(raw_contents):
                try:
                    norm_content = self._normalize_single(content, platform)
                    normalized.append(norm_content)

                except Exception as e:
                    self.logger.warning(
                        f"Failed to normalize content {idx}",
                        extra={"extra_data": {
                            "content_id": content.get("id"),
                            "error": str(e)
                        }}
                    )
                    errors.append({"index": idx, "error": str(e)})

            # Log the operation
            log_data_operation(
                self.logger,
                operation="normalize",
                data_type="content",
                count=len(normalized),
                platform=platform,
                success_rate=len(normalized) / len(raw_contents) if raw_contents else 0,
                error_count=len(errors)
            )

            if errors:
                self.logger.warning(
                    f"Batch normalization completed with {len(errors)} errors",
                    extra={"extra_data": {"errors": errors[:10]}}  # Log first 10 errors
                )

        return normalized, errors

    def _normalize_single(self, content: dict, platform: str):
        """Normalize a single content item."""
        self.logger.debug(
            f"Normalizing {platform} content",
            extra={"extra_data": {"content_id": content.get("id")}}
        )

        # Normalization logic...
        normalized = {
            "id": self._generate_id(),
            "platform": platform,
            "text": content.get("text"),
            # ... more fields
        }

        return normalized
```

### Example 3: Application Startup

```python
# main.py
from scrapper.utils.logger import initialize_logging, get_logger

def main():
    """Application entry point."""

    # Initialize logging system
    initialize_logging(log_level="INFO")

    # Get main application logger
    logger = get_logger("Main")

    logger.info("="*60)
    logger.info("Scrapper Application Starting")
    logger.info("="*60)

    try:
        # Initialize components
        logger.info("Initializing components...")

        twitter_scraper = TwitterScraper(config.twitter)
        logger.info("✓ Twitter scraper initialized")

        feed_aggregator = FeedAggregator()
        logger.info("✓ Feed aggregator initialized")

        # Start scraping
        logger.info("Starting scraping sessions...")
        run_scraping_loop()

    except Exception as e:
        logger.critical("Application failed to start", exc_info=True)
        raise

if __name__ == "__main__":
    main()
```

## Debugging with Logs

When you encounter an issue:

1. **Get the timestamp** from the user or system
2. **Check error logs**:
   ```bash
   grep "2025-11-16 10:30" trace/errors/errors.log
   ```

3. **Follow the flow**:
   ```bash
   # Check what the scraper did
   grep "2025-11-16 10:30" trace/scrapers/twitter.log

   # Check processing
   grep "2025-11-16 10:30" trace/processing/normalizer.log

   # Check storage
   grep "2025-11-16 10:30" trace/storage/raw_data.log
   ```

4. **Check performance** if it's slow:
   ```bash
   grep "2025-11-16 10:30" trace/performance/metrics.log
   ```

5. **Review full context** around the error:
   ```bash
   grep -A 10 -B 10 "ERROR_MESSAGE" trace/scrapers/twitter.log
   ```

## Remember

- **NO CONSOLE OUTPUT** - All logs go to files
- **Always initialize** logging at startup
- **Use appropriate log levels** for different messages
- **Include context** in your log messages
- **Log exceptions** with `exc_info=True`
- **Use performance logging** for operations
- **Check trace/ folder** for all debugging needs

Happy logging! 🎯
