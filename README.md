# Social Arena - Scrapper 🕷️

A comprehensive multi-platform social media data collection engine for real-time trend monitoring, content aggregation, and viral propagation analysis. Built for the Social Arena simulation ecosystem.

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/Social-Arena/Scrapper.git
cd Scrapper
pip install -r requirements.txt
```

### Basic Usage

```python
from scrapper.utils.logger import initialize_logging, get_logger

# Initialize logging system (NO console output)
initialize_logging(log_level="INFO")

# Get component-specific logger
logger = get_logger("TwitterScraper")

# Start scraping
logger.info("Starting social media data collection")
```

## 📊 Core Features

### 🌐 Multi-Platform Data Collection
- **Twitter/X**: Trending topics, hashtags, user timelines, real-time streams
- **TikTok**: Viral videos, trending sounds, hashtag challenges  
- **XiaoHongShu (小红书)**: Lifestyle content, product trends, user-generated content
- **YouTube**: Trending videos, channel analytics, comment sentiment
- **Instagram**: Stories, reels, trending hashtags (future support)

### 🔥 Real-Time Trend Detection
- **Viral Content Identification**: Early detection of trending content
- **Hashtag Lifecycle Tracking**: Monitor hashtag emergence and decay
- **Influencer Monitoring**: Track key opinion leaders and their impact
- **Sentiment Waves**: Real-time sentiment analysis across platforms

### ⚡ Data Processing Pipeline
- **Content Normalization**: Convert platform-specific data to unified Feed format
- **Duplicate Detection**: Advanced deduplication across platforms
- **Content Enrichment**: Add sentiment, topics, entities, virality scores
- **Quality Filtering**: Remove spam, low-quality, or inappropriate content

## 🛠️ System Architecture

### Core Components

```
Scrapper/
├── scrapper/                    # Main package
│   ├── sources/                 # Platform-specific scrapers
│   │   ├── twitter_scraper.py   # Twitter/X data collection
│   │   ├── tiktok_scraper.py    # TikTok video and trend data
│   │   ├── xiaohongshu_scraper.py # XHS lifestyle content
│   │   ├── youtube_scraper.py   # YouTube trending analysis
│   │   └── instagram_scraper.py # Instagram content (planned)
│   ├── data_processing/         # Data transformation pipeline
│   │   ├── content_normalizer.py # Unified format conversion
│   │   ├── trend_detector.py    # Viral content detection
│   │   ├── sentiment_analyzer.py # Multi-language sentiment
│   │   ├── entity_extractor.py  # Named entity recognition
│   │   └── quality_filter.py    # Content quality assessment
│   ├── feeds/                   # Feed management system
│   │   ├── feed_aggregator.py   # Cross-platform aggregation
│   │   ├── feed_enricher.py     # Content enhancement
│   │   └── feed_validator.py    # Data validation
│   ├── storage/                 # Data persistence layer
│   │   ├── raw_data_store.py    # Raw platform data storage
│   │   ├── processed_store.py   # Normalized data storage
│   │   ├── cache_manager.py     # Redis caching layer
│   │   └── backup_manager.py    # Data backup and recovery
│   ├── monitoring/              # System health and performance
│   │   ├── scraping_monitor.py  # Scraping performance tracking
│   │   ├── rate_limiter.py      # API quota management
│   │   ├── health_checker.py    # System health monitoring
│   │   └── anomaly_detector.py  # Data quality anomalies
│   ├── config/                  # Configuration management
│   │   ├── logging_config.py    # Centralized logging setup
│   │   ├── scraper_config.py    # Per-platform configuration
│   │   └── storage_config.py    # Database and cache config
│   └── utils/                   # Shared utilities
│       ├── logger.py            # Advanced logging system
│       ├── rate_utils.py        # Rate limiting utilities
│       ├── retry_utils.py       # Robust retry mechanisms
│       └── validation_utils.py   # Data validation helpers
└── trace/                       # Runtime logs (git-ignored)
    ├── scrapers/               # Per-platform scraping logs
    ├── processing/             # Data processing logs
    ├── feeds/                  # Feed management logs
    ├── storage/                # Database operation logs
    ├── monitoring/             # System monitoring logs
    ├── errors/                 # Centralized error logging
    ├── performance/            # Performance metrics
    └── audit/                  # Data audit trails
```

### Data Flow Architecture

```
[Platform APIs]
      ↓
[Platform Scrapers] → trace/scrapers/
      ↓
[Content Normalizer] → trace/processing/
      ↓
[Trend Detection] → trace/processing/
      ↓
[Content Enrichment] → trace/feeds/
      ↓
[Quality Filtering] → trace/feeds/
      ↓
[Unified Storage] → trace/storage/
      ↓
[Feed System/Arena Integration]
```

## 🔍 Advanced Logging System

**CRITICAL**: All operations use file-based logging with **ZERO console output**.

### Log Structure
```
trace/
├── scrapers/
│   ├── twitter/           # Twitter-specific logs
│   ├── tiktok/           # TikTok scraping logs
│   ├── xiaohongshu/      # XHS scraping logs
│   └── youtube/          # YouTube scraping logs
├── processing/
│   ├── normalization/    # Data transformation logs
│   ├── enrichment/       # Content enhancement logs
│   └── quality/          # Quality filtering logs
├── feeds/
│   ├── aggregation/      # Cross-platform aggregation
│   └── validation/       # Feed validation logs
├── storage/
│   ├── database/         # Database operation logs
│   ├── cache/            # Cache operation logs
│   └── backup/           # Backup and recovery logs
├── monitoring/
│   ├── performance/      # System performance metrics
│   ├── health/           # Health check results
│   └── anomalies/        # Anomaly detection logs
├── errors/               # Centralized error logging
└── audit/                # Data audit and compliance
```

### Debugging Workflow

```bash
# Test logging system
python test_logging.py

# Monitor specific platform
tail -f trace/scrapers/twitter/scraping.log

# Check for errors across all components
python scrapper/utils/log_analyzer.py errors --last-hour

# Performance analysis
python scrapper/utils/log_analyzer.py performance --component twitter

# Data quality monitoring
python scrapper/utils/log_analyzer.py quality --timeframe 24h
```

### Advanced Usage Example

```python
from scrapper.utils.logger import get_logger, log_performance
from scrapper.utils.retry_utils import retry_with_backoff

logger = get_logger("TwitterScraper", component="scrapers")

class TwitterScraper:
    def __init__(self):
        self.logger = get_logger("TwitterScraper")
    
    @log_performance(threshold_ms=1000)
    @retry_with_backoff(max_retries=3)
    async def scrape_trending_topics(self, location_id=1):
        """Scrape trending topics with comprehensive logging"""
        self.logger.info(f"Starting trending topics scrape for location {location_id}")
        
        try:
            # API call with rate limiting
            async with self.rate_limiter.acquire():
                topics = await self.api_client.get_trending(location_id)
                
            self.logger.info(f"Successfully scraped {len(topics)} trending topics", 
                           extra={"metrics": {"topic_count": len(topics)}})
            
            return topics
            
        except RateLimitError as e:
            self.logger.warning(f"Rate limited, waiting {e.retry_after} seconds")
            raise
        except Exception as e:
            self.logger.error(f"Failed to scrape trending topics", 
                            extra={"error_details": str(e)})
            raise
```

## 📈 Supported Platforms

### Twitter/X Integration
- **Real-time streaming**: Live tweet collection with filters
- **Trending topics**: Location-based trending hashtags and topics  
- **User timelines**: Historical and real-time user content
- **Search API**: Keyword and hashtag-based content discovery
- **Rate limiting**: Intelligent quota management and backoff

### TikTok Integration  
- **Trending videos**: Viral video identification and collection
- **Hashtag challenges**: Challenge lifecycle tracking
- **Sound trends**: Popular audio and music trends
- **Creator content**: Influencer and content creator monitoring
- **Engagement metrics**: Likes, shares, comments, views

### XiaoHongShu (小红书) Integration
- **Lifestyle content**: Fashion, beauty, travel, food trends
- **Product trends**: E-commerce and product discovery
- **KOL monitoring**: Key Opinion Leader content tracking
- **User-generated content**: Community-driven content analysis
- **Regional trends**: Location-specific trending content

### YouTube Integration
- **Trending videos**: Platform trending and viral content
- **Channel analytics**: Creator performance and growth
- **Comment sentiment**: Video comment analysis
- **Metadata extraction**: Video descriptions, tags, categories
- **Engagement tracking**: Views, likes, comments, subscriber growth

## 🧰 Usage Examples

### Basic Multi-Platform Scraping

```python
from scrapper import MultiPlatformScraper

scraper = MultiPlatformScraper(
    platforms=["twitter", "tiktok", "xiaohongshu"],
    config_path="config/production.yaml"
)

# Start real-time scraping
async with scraper:
    results = await scraper.scrape_trending_content(
        topics=["AI", "technology", "innovation"],
        timeframe="1h",
        max_items_per_platform=1000
    )
    
    print(f"Collected {len(results)} items across platforms")
```

### Real-time Trend Monitoring

```python
from scrapper.monitoring import TrendMonitor

monitor = TrendMonitor(
    platforms=["twitter", "tiktok"],
    trend_threshold=0.8,
    notification_webhook="https://alerts.socialarena.com/trends"
)

# Monitor for viral content
@monitor.on_trend_detected
async def handle_viral_content(trend_data):
    logger.info(f"Viral trend detected: {trend_data['hashtag']}")
    
    # Collect related content
    related_content = await scraper.collect_related_content(
        hashtag=trend_data['hashtag'],
        platforms=trend_data['platforms'],
        max_items=5000
    )
    
    # Send to Feed system
    await feed_system.ingest_trending_content(related_content)

await monitor.start_monitoring()
```

### Content Quality Analysis

```python
from scrapper.data_processing import QualityAnalyzer

analyzer = QualityAnalyzer(
    toxicity_threshold=0.8,
    spam_threshold=0.7,
    quality_threshold=0.6
)

# Process and filter content
async def process_content_batch(raw_content):
    # Normalize across platforms
    normalized = await normalizer.normalize_batch(raw_content)
    
    # Analyze quality
    quality_scores = await analyzer.analyze_batch(normalized)
    
    # Filter high-quality content
    high_quality = [
        item for item, score in zip(normalized, quality_scores)
        if score.overall_quality > 0.6
    ]
    
    logger.info(f"Filtered {len(high_quality)}/{len(raw_content)} items")
    return high_quality
```

### Custom Platform Integration

```python
from scrapper.sources.base import BaseScraper

class CustomPlatformScraper(BaseScraper):
    """Example custom platform scraper"""
    
    def __init__(self, api_key, rate_limit=100):
        super().__init__(platform="custom_platform")
        self.api_key = api_key
        self.rate_limit = rate_limit
        
    @log_performance()
    async def scrape_trending_content(self, limit=100):
        """Implement platform-specific scraping logic"""
        self.logger.info(f"Scraping trending content, limit={limit}")
        
        try:
            # Your custom scraping logic here
            content = await self._fetch_trending_data(limit)
            
            # Normalize to Feed format
            normalized = await self.normalize_content(content)
            
            self.logger.info(f"Successfully scraped {len(normalized)} items")
            return normalized
            
        except Exception as e:
            self.logger.error(f"Scraping failed: {e}")
            raise

# Register custom scraper
scraper_registry.register("custom_platform", CustomPlatformScraper)
```

## 🔧 Configuration

### Platform Configuration

```yaml
# config/scrapers.yaml
platforms:
  twitter:
    api_version: "v2"
    rate_limits:
      search: 300  # requests per 15 min
      streaming: 50  # concurrent connections
    filters:
      min_followers: 100
      languages: ["en", "zh", "ja"]
      content_types: ["text", "media"]
    
  tiktok:
    rate_limits:
      trending: 100  # requests per hour
      search: 200    # requests per hour
    filters:
      min_views: 1000
      max_content_age_hours: 24
      verified_creators_only: false
    
  xiaohongshu:
    rate_limits:
      search: 150
      user_content: 100
    filters:
      min_likes: 50
      categories: ["fashion", "beauty", "travel", "food"]
      language: "zh"
```

### Storage Configuration

```yaml
# config/storage.yaml
database:
  postgres:
    host: "localhost"
    port: 5432
    database: "social_arena"
    connection_pool_size: 20
    
  redis:
    host: "localhost" 
    port: 6379
    db: 0
    max_connections: 50
    
storage_policies:
  raw_data_retention_days: 30
  processed_data_retention_days: 90
  cache_ttl_seconds: 3600
  backup_frequency_hours: 6
```

### Monitoring Configuration

```yaml
# config/monitoring.yaml
health_checks:
  interval_seconds: 60
  timeout_seconds: 30
  failure_threshold: 3

performance_monitoring:
  enable_profiling: true
  slow_query_threshold_ms: 1000
  memory_alert_threshold_mb: 1024

alerts:
  webhook_url: "https://alerts.socialarena.com/webhook"
  alert_levels: ["error", "critical"]
  notification_channels: ["slack", "email"]
```

## 🧪 Extending the System

### Adding New Platform Support

```python
# 1. Create scraper class
from scrapper.sources.base import BaseScraper

class NewPlatformScraper(BaseScraper):
    platform = "new_platform"
    
    async def scrape_trending_content(self, **kwargs):
        # Implement scraping logic
        pass
    
    async def normalize_content(self, raw_content):
        # Convert to Feed format
        pass

# 2. Register scraper
from scrapper.registry import register_scraper
register_scraper("new_platform", NewPlatformScraper)

# 3. Add configuration
# Add platform config to config/scrapers.yaml

# 4. Add tests
# Create tests/sources/test_new_platform.py
```

### Custom Content Processing

```python
from scrapper.data_processing.base import BaseProcessor

class CustomContentProcessor(BaseProcessor):
    """Custom content processing pipeline"""
    
    async def process(self, content_batch):
        # Custom processing logic
        processed = []
        
        for item in content_batch:
            # Apply custom transformations
            enhanced_item = await self.enhance_content(item)
            processed.append(enhanced_item)
            
        return processed
    
    async def enhance_content(self, content):
        # Your enhancement logic
        return content

# Register processor
processor_registry.register("custom_processor", CustomContentProcessor)
```

## 📋 Development Guidelines

### Code Standards
- **File-only logging**: Never use print() or console output
- **Async/await**: Use async programming for I/O operations  
- **Type hints**: Full type annotation for all functions
- **Error handling**: Comprehensive exception handling with logging
- **Performance**: Monitor and log all slow operations

### Testing Guidelines
```bash
# Run comprehensive tests
python -m pytest tests/ -v

# Test specific platform
python -m pytest tests/sources/test_twitter.py

# Test logging system
python test_logging.py

# Integration tests
python -m pytest tests/integration/ -v

# Performance benchmarks  
python -m pytest tests/performance/ -v --benchmark-only
```

### Adding Components

1. **Create component** in appropriate module directory
2. **Add logging** with component-specific logger
3. **Include performance monitoring** with @log_performance  
4. **Add comprehensive tests** in tests/ directory
5. **Update configuration** files if needed
6. **Document** in this README and inline comments
7. **Add error handling** with proper logging context

## 📚 Data Compliance & Ethics

### Privacy Protection
- **No PII collection**: Strictly avoid personal identifiable information
- **Data anonymization**: Remove user identifiers from stored content
- **Consent compliance**: Respect platform terms of service
- **Data retention**: Automatic cleanup of old data per policy

### API Compliance
- **Rate limiting**: Respect all platform API limits
- **Terms of service**: Comply with platform usage policies
- **Attribution**: Proper content attribution where required
- **Monitoring**: Track API usage and compliance metrics

## 🚨 Monitoring & Alerting

### System Health Monitoring

```python
from scrapper.monitoring import HealthMonitor

health_monitor = HealthMonitor(
    check_interval=60,
    alert_thresholds={
        "scraping_success_rate": 0.95,
        "data_quality_score": 0.8,
        "api_error_rate": 0.05,
        "processing_latency_p95": 5000  # ms
    }
)

# Setup alerts
@health_monitor.on_alert("low_success_rate")
async def handle_scraping_issues(alert_data):
    logger.critical(f"Scraping success rate below threshold: {alert_data}")
    await notify_operations_team(alert_data)

await health_monitor.start_monitoring()
```

### Performance Metrics

Key metrics tracked automatically:
- **Scraping throughput**: Items per second per platform
- **Data quality score**: Percentage of high-quality content  
- **API success rate**: Successful API calls / total calls
- **Processing latency**: Time from collection to storage
- **Storage efficiency**: Compression and deduplication rates
- **Cache hit ratio**: Cache performance metrics

## 🤝 Contributing

1. **Follow logging guidelines**: Use centralized logging system
2. **Add comprehensive tests**: Unit, integration, and performance tests
3. **Update documentation**: Keep README and inline docs current
4. **Respect privacy**: Never collect or log PII
5. **Monitor performance**: Add performance tracking to new features
6. **Handle errors gracefully**: Comprehensive exception handling

## 🗓️ Roadmap

### Phase 1: Core Platform Support ✅
- [x] Logging infrastructure
- [x] Twitter/X scraper foundation  
- [x] Data normalization pipeline
- [x] Basic storage layer
- [x] Configuration management

### Phase 2: Multi-Platform Expansion 🚧
- [ ] TikTok scraper implementation
- [ ] XiaoHongShu integration
- [ ] YouTube trending analysis  
- [ ] Advanced trend detection
- [ ] Real-time streaming pipelines

### Phase 3: Intelligence & Scale 🔮
- [ ] AI-powered content classification
- [ ] Predictive trend analysis
- [ ] Distributed scraping architecture
- [ ] Advanced analytics dashboard
- [ ] Machine learning content scoring

## 📄 License

See [LICENSE](LICENSE) file for details.

---

**Part of the Social Arena ecosystem** - Powering next-generation social media research and simulation through intelligent data collection.