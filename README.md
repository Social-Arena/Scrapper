# Scrapper - Social Media Data Collection Engine

A comprehensive data collection engine for gathering and processing social media content from multiple platforms. Part of a larger social media viral propagation agent simulation system.

## Overview

Scrapper is responsible for:
- **Multi-platform data collection**: Twitter, TikTok, XiaoHongShu (小红书), YouTube, and more
- **Real-time trend monitoring**: Detecting and tracking viral content and trending topics
- **Data normalization**: Converting platform-specific data into a unified Feed format
- **Data enrichment**: Adding sentiment analysis, entity recognition, and topic classification

## Project Structure

```
Scrapper/
├── scrapper/                 # Main package
│   ├── sources/              # Platform-specific scrapers
│   │   ├── twitter_scraper.py
│   │   ├── tiktok_scraper.py
│   │   ├── xiaohongshu_scraper.py
│   │   └── youtube_scraper.py
│   ├── data_processing/      # Data processing pipeline
│   │   ├── content_normalizer.py
│   │   ├── trend_detector.py
│   │   └── sentiment_analyzer.py
│   ├── feeds/                # Feed management
│   │   ├── feed_aggregator.py
│   │   └── feed_enricher.py
│   ├── storage/              # Data storage
│   │   ├── raw_data_store.py
│   │   └── cache_manager.py
│   ├── monitoring/           # System monitoring
│   │   ├── scraping_monitor.py
│   │   └── rate_limiter.py
│   ├── config/               # Configuration
│   │   └── logging_config.py
│   └── utils/                # Utilities
│       └── logger.py         # Centralized logging
├── trace/                    # Runtime logs (git-ignored)
│   ├── scrapers/
│   ├── processing/
│   ├── feeds/
│   ├── storage/
│   ├── monitoring/
│   ├── errors/
│   ├── performance/
│   └── README.md            # Logging documentation
├── test_logging.py          # Logging system test
├── LOGGING_USAGE.md         # Logging usage guide
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Features

### ✅ Implemented

#### Comprehensive Logging System
- **File-based logging** (NO console output)
- **Component-specific logs** for easy debugging
- **Automatic log rotation** to prevent disk space issues
- **Performance tracking** for all operations
- **Structured logging** with JSON support
- **Error tracking** with full tracebacks and context

See [LOGGING_USAGE.md](LOGGING_USAGE.md) for detailed usage instructions.

### 🚧 Planned Features

#### Data Collection
- [ ] Twitter scraper with trending topics, hashtags, and user timelines
- [ ] TikTok scraper for viral videos and trends
- [ ] XiaoHongShu (小红书) scraper for lifestyle content
- [ ] YouTube scraper for trending videos and channels
- [ ] Real-time content streaming
- [ ] Rate limiting and API quota management

#### Data Processing
- [ ] Content normalization to unified Feed format
- [ ] Trend detection and lifecycle analysis
- [ ] Sentiment analysis and emotional triggers
- [ ] Entity recognition and topic classification
- [ ] Virality prediction algorithms

#### Storage & Caching
- [ ] PostgreSQL for persistent storage
- [ ] Redis for caching and rate limiting
- [ ] Data deduplication
- [ ] Automatic cleanup of old data

#### Monitoring & Health
- [ ] Scraping health monitoring
- [ ] Data quality tracking
- [ ] Anomaly detection
- [ ] Performance metrics and benchmarks

## Getting Started

### Prerequisites

- Python 3.9 or higher
- (Additional dependencies to be added as features are implemented)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Scrapper

# Install dependencies
pip install -r requirements.txt

# Test the logging system
python test_logging.py
```

### Quick Start

```python
from scrapper.utils.logger import initialize_logging, get_logger

# Initialize logging system
initialize_logging(log_level="INFO")

# Get a logger for your component
logger = get_logger("MyComponent")

# Start logging
logger.info("Application started")
```

## Logging System

### NO Console Output

All logs are written to files in the `trace/` directory. This ensures:
- Complete debugging capability after the fact
- No log loss due to terminal closure
- Easy log analysis with standard tools
- Structured logging for machine parsing

### Log Files

```
trace/
├── scrapers/          # Platform scraper logs
├── processing/        # Data processing logs
├── feeds/             # Feed system logs
├── storage/           # Storage operation logs
├── monitoring/        # Monitoring and health logs
├── errors/            # Error and exception logs
├── performance/       # Performance metrics
└── main.log          # Main application log
```

### Usage Example

```python
from scrapper.utils.logger import get_logger, log_performance

logger = get_logger("TwitterScraper")

# Log messages
logger.info("Starting to scrape trending topics")
logger.debug(f"API request to endpoint: {endpoint}")
logger.warning("Rate limit approaching")

# Log performance
with log_performance(logger, "scrape_trending_topics"):
    topics = scrape_trending_topics()

# Log errors with context
try:
    result = risky_operation()
except Exception as e:
    log_error_with_context(logger, e, {"user_id": user_id})
```

### Debugging Workflow

1. **Identify the component** involved in the issue
2. **Check error logs** first: `trace/errors/errors.log`
3. **Follow the execution flow** across component logs
4. **Check performance** if needed: `trace/performance/metrics.log`
5. **Analyze with standard tools**: `grep`, `tail`, `awk`, etc.

See [trace/README.md](trace/README.md) for detailed debugging instructions.

## Development Guidelines

### Adding New Components

1. Create your component in the appropriate directory
2. Get a logger for your component:
   ```python
   from scrapper.utils.logger import get_logger

   class MyComponent:
       def __init__(self):
           self.logger = get_logger("MyComponent")
   ```

3. Log at appropriate levels:
   - `DEBUG`: Detailed diagnostic information
   - `INFO`: General flow and operations
   - `WARNING`: Concerning but not critical issues
   - `ERROR`: Errors that need attention
   - `CRITICAL`: System-threatening errors

4. Include context in logs:
   ```python
   logger.info("Operation completed", extra={"extra_data": {
       "items_processed": count,
       "duration": elapsed,
       "platform": platform
   }})
   ```

### Testing

Always test your logging:

```bash
# Run the logging test
python test_logging.py

# Check that logs are created
ls -lh trace/**/*.log

# Verify log content
tail -50 trace/main.log
```

## Compliance and Ethics

- Respects platform API terms of service
- Implements rate limiting to avoid abuse
- Does not collect personal identifiable information
- Supports data deletion requests
- Includes data anonymization features

## Architecture

### Data Flow

```
[Platform APIs]
      ↓
[Platform Scrapers] → logs to trace/scrapers/
      ↓
[Content Normalizer] → logs to trace/processing/
      ↓
[Feed Enricher] → logs to trace/feeds/
      ↓
[Storage Layer] → logs to trace/storage/
      ↓
[Feed System / Arena System]
```

### Key Components

- **Scrapers**: Platform-specific data collection
- **Normalizers**: Convert to unified format
- **Enrichers**: Add metadata and analysis
- **Storage**: Persist and cache data
- **Monitors**: Track health and performance

## Performance Considerations

- Async/await for concurrent operations
- Connection pooling for database access
- Redis caching for frequently accessed data
- Rate limiting to respect API quotas
- Automatic log rotation to manage disk space

## Contributing

1. Follow the logging guidelines
2. Add appropriate tests
3. Document new features
4. Ensure logs are helpful for debugging

## Roadmap

### Phase 1: Foundation (Current)
- [x] Logging infrastructure
- [ ] Twitter scraper
- [ ] Data normalization pipeline
- [ ] Basic storage

### Phase 2: Expansion
- [ ] Additional platform scrapers
- [ ] Trend detection
- [ ] Sentiment analysis
- [ ] Performance optimization

### Phase 3: Advanced Features
- [ ] Real-time streaming
- [ ] Advanced analytics
- [ ] Machine learning integration
- [ ] Distributed scraping

## Support

- **Documentation**: See [LOGGING_USAGE.md](LOGGING_USAGE.md)
- **Debugging**: See [trace/README.md](trace/README.md)
- **Issues**: Check logs in `trace/` directory

## License

See [LICENSE](LICENSE) file for details.

---

**Note**: This project is under active development. The logging system is fully functional. Other features are being implemented according to the roadmap
