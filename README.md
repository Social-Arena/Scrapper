# Scrapper - Multi-Platform Data Collection Engine 🕷️

**Real-time Social Media Data Acquisition & Processing**

A comprehensive data collection engine for gathering and processing social media content from multiple platforms. Scrapper provides real-world data to fuel the Social-Arena simulation ecosystem.

---

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Supported Platforms](#supported-platforms)
- [Directory Structure](#directory-structure)
- [Data Pipeline](#data-pipeline)
- [Core Components](#core-components)
- [Data Normalization](#data-normalization)
- [Trend Detection](#trend-detection)
- [Storage System](#storage-system)
- [Monitoring & Rate Limiting](#monitoring--rate-limiting)
- [Integration](#integration)
- [Configuration](#configuration)
- [Development Guide](#development-guide)

---

## 🎯 Overview

Scrapper is the **data acquisition engine** of Social-Arena, responsible for:

- **Multi-platform data collection**: Twitter, TikTok, XiaoHongShu (小红书), YouTube
- **Real-time trend monitoring**: Detecting and tracking viral content and trending topics
- **Data normalization**: Converting platform-specific data into unified Feed format
- **Data enrichment**: Adding sentiment analysis, entity recognition, topic classification
- **Trend analysis**: Identifying emerging trends and viral content patterns
- **Compliance & Ethics**: Respecting platform ToS, rate limits, and user privacy

### Key Features

✅ **Currently Implemented:**
- Comprehensive logging system (file-based, NO console output)
- Component-specific logs for easy debugging
- Automatic log rotation
- Performance tracking
- Structured logging with JSON support
- Error tracking with full context

🚧 **In Development:**
- Platform-specific scrapers
- Data processing pipeline
- Storage layer
- Monitoring systems

---

## 🏗️ System Architecture

```
        ┌───────────────────────────┐
        │    Multi-Platform Scrapers │
        │ ┌───────────────┐        │
        │ │ Twitter Scraper │       │
        │ │ TikTok Scraper  │       │
        │ │ XiaoHongShu     │       │
        │ │ YouTube Scraper │       │
        │ └───────────────┘        │
        └─────────┬────────────────┘
                  │ Raw Data
                  ▼
        ┌───────────────────────────┐
        │   Data Processing Pipeline │
        │ ┌───────────────┐        │
        │ │ ContentNormalizer │     │
        │ │ TrendDetector     │     │
        │ │ SentimentAnalyzer │     │
        │ │ EntityExtractor   │     │
        │ └───────────────┘        │
        └─────────┬────────────────┘
                  │ Processed Data
                  ▼
        ┌───────────────────────────┐
        │     Feed Processing        │
        │ ┌───────────────┐        │
        │ │ FeedAggregator │       │
        │ │ FeedValidator  │       │
        │ │ FeedEnricher   │       │
        │ └───────────────┘        │
        └─────────┬────────────────┘
                  │
   ┌──────────────┼──────────────┐
   ▼              ▼              ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Feed    │  │ Arena   │  │ Recomm  │
│ System  │  │ System  │  │ System  │
└─────────┘  └─────────┘  └─────────┘

        ┌───────────────────────────┐
        │   Storage & Cache System   │
        │  RawDataStore + Redis      │
        └───────────────────────────┘

        ┌───────────────────────────┐
        │  Monitoring & Rate Limiting│
        │  ScrapingMonitor + RateLimiter │
        └───────────────────────────┘
```

---

## 🌐 Supported Platforms

### 1. Twitter / X 🐦

**Data Collected:**
- Trending topics and hashtags
- Hashtag timelines
- User timelines
- Viral content (high engagement)
- Real-time streams

**API Features:**
- Twitter API v2
- Rate-limited requests
- Filtered streams
- User mentions

### 2. TikTok 📱

**Data Collected:**
- Trending videos
- Hashtag videos
- User-generated content
- Video engagement metrics
- Virality factors

**Features:**
- Video metadata extraction
- Engagement velocity analysis
- Music/sound trends
- Creator analytics

### 3. XiaoHongShu (小红书) 📝

**Data Collected:**
- Trending notes/posts
- Topic-based content
- Lifestyle trends
- Product reviews
- User engagement

**Features:**
- Chinese social commerce
- Lifestyle content focus
- Image-heavy posts
- E-commerce integration

### 4. YouTube 🎥

**Data Collected:**
- Trending videos
- Channel content
- Video statistics
- Comments and engagement
- Recommendation patterns

**Features:**
- Video metadata
- Channel analytics
- Engagement patterns
- Viewer demographics

---

## 📁 Directory Structure

```
scrapper/
│
├── sources/                      # Platform-specific scrapers
│   ├── __init__.py
│   ├── twitter_scraper.py       # Twitter data collection
│   ├── tiktok_scraper.py        # TikTok data collection
│   ├── xiaohongshu_scraper.py   # XiaoHongShu data collection
│   └── youtube_scraper.py       # YouTube data collection
│
├── data_processing/             # Data processing pipeline
│   ├── __init__.py
│   ├── content_normalizer.py   # Content standardization
│   ├── trend_detector.py       # Trend detection
│   ├── entity_extractor.py     # Entity extraction
│   └── sentiment_analyzer.py   # Sentiment analysis
│
├── feeds/                       # Feed management
│   ├── __init__.py
│   ├── feed_aggregator.py      # Feed aggregation
│   ├── feed_validator.py       # Feed validation
│   └── feed_enricher.py        # Feed enrichment
│
├── storage/                     # Data storage
│   ├── __init__.py
│   ├── raw_data_store.py       # Raw data storage
│   ├── processed_data_store.py # Processed data storage
│   └── cache_manager.py        # Cache management
│
├── monitoring/                  # System monitoring
│   ├── __init__.py
│   ├── scraping_monitor.py     # Scraping health monitoring
│   ├── rate_limiter.py         # Rate limiting
│   └── error_handler.py        # Error handling
│
├── api/                         # API interfaces
│   ├── __init__.py
│   ├── scraper_api.py          # Scraper API
│   └── data_pipeline.py        # Data pipeline orchestration
│
├── config/                      # Configuration
│   ├── __init__.py
│   └── logging_config.py       # Logging configuration
│
├── utils/                       # Utilities
│   ├── __init__.py
│   └── logger.py               # Centralized logging
│
├── tests/                       # Test suite
│   ├── test_scrapers.py
│   ├── test_processing.py
│   └── test_storage.py
│
└── README.md                    # This file
```

---

## 🔄 Data Pipeline

### End-to-End Flow

```
1. Platform APIs / Web Scraping
   ↓ [Raw Data Collection]
2. Raw Data Storage
   ↓ [Data Validation]
3. Content Normalization
   ↓ [Standardization to Feed format]
4. Data Enrichment
   ├─ Sentiment Analysis
   ├─ Entity Extraction
   ├─ Topic Classification
   └─ Trend Detection
   ↓ [Enhanced Metadata]
5. Feed Aggregation
   ↓ [Deduplication & Validation]
6. Feed System Integration
   ↓ [Distribution to other modules]
7. Arena / Agent / Recommendation
```

---

## 🧩 Core Components

### 1. Twitter Scraper (`sources/twitter_scraper.py`)

```python
class TwitterScraper:
    """Twitter data collection engine"""
    
    def __init__(self, api_config: TwitterAPIConfig):
        self.api_client = TwitterAPI(api_config)
        self.rate_limiter = RateLimiter(api_config.rate_limits)
    
    async def scrape_trending_topics(self, location: str = "global") -> List[TrendingTopic]:
        """Scrape trending topics"""
        await self.rate_limiter.wait_if_needed("trending")
        
        response = await self.api_client.get_trends(location)
        trends = self._parse_trending_response(response)
        
        self._log_scraping_activity("trending", len(trends))
        return trends
    
    async def scrape_hashtag_timeline(self, hashtag: str, max_results: int = 100) -> List[RawTweet]:
        """Scrape tweets for specific hashtag"""
        await self.rate_limiter.wait_if_needed("search")
        
        tweets = []
        async for tweet in self.api_client.search_tweets(f"#{hashtag}", max_results):
            tweets.append(self._parse_tweet(tweet))
        
        self._log_scraping_activity(f"hashtag_{hashtag}", len(tweets))
        return tweets
    
    async def scrape_user_timeline(self, user_id: str, max_results: int = 100) -> List[RawTweet]:
        """Scrape user's timeline"""
        await self.rate_limiter.wait_if_needed("user_timeline")
        
        tweets = await self.api_client.get_user_tweets(user_id, max_results)
        parsed = [self._parse_tweet(t) for t in tweets]
        
        self._log_scraping_activity(f"user_{user_id}", len(parsed))
        return parsed
    
    async def scrape_viral_content(self, min_engagement: int = 10000) -> List[RawTweet]:
        """Scrape highly engaging content"""
        # Query for high-engagement tweets
        query = f"min_faves:{min_engagement} OR min_retweets:{min_engagement//2}"
        
        viral_tweets = []
        async for tweet in self.api_client.search_tweets(query, max_results=500):
            if self._is_viral(tweet, min_engagement):
                viral_tweets.append(self._parse_tweet(tweet))
        
        return viral_tweets
    
    async def monitor_real_time_stream(self, keywords: List[str]) -> AsyncIterator[RawTweet]:
        """Monitor real-time tweet stream"""
        async for tweet in self.api_client.stream_tweets(keywords):
            yield self._parse_tweet(tweet)
```

**Key Features:**
- Rate limiting integration
- Multiple scraping modes
- Real-time streaming support
- Viral content detection

---

### 2. Content Normalizer (`data_processing/content_normalizer.py`)

```python
class ContentNormalizer:
    """Normalize content from different platforms to Feed format"""
    
    def normalize_twitter_data(self, raw_tweet: RawTweet) -> Feed:
        """Standardize Twitter data to Feed format"""
        return Feed(
            id=self.generate_feed_id(),
            text=raw_tweet.text,
            author_id=raw_tweet.user.id,
            platform="twitter",
            created_at=raw_tweet.created_at,
            feed_type=self._determine_feed_type(raw_tweet),
            public_metrics=PublicMetrics(
                like_count=raw_tweet.like_count,
                retweet_count=raw_tweet.retweet_count,
                reply_count=raw_tweet.reply_count,
                quote_count=raw_tweet.quote_count
            ),
            entities=self.extract_entities(raw_tweet.text),
            platform_specific_data={
                "twitter_id": raw_tweet.id,
                "twitter_metrics": raw_tweet.public_metrics
            }
        )
    
    def normalize_tiktok_data(self, raw_video: RawTikTokVideo) -> Feed:
        """Standardize TikTok data to Feed format"""
        return Feed(
            id=self.generate_feed_id(),
            text=raw_video.description,
            author_id=raw_video.author.id,
            platform="tiktok",
            created_at=raw_video.create_time,
            feed_type=FeedType.POST,
            public_metrics=PublicMetrics(
                like_count=raw_video.like_count,
                retweet_count=raw_video.share_count,  # Map shares to retweets
                reply_count=raw_video.comment_count,
                quote_count=0,
                bookmark_count=0,
                impression_count=raw_video.view_count
            ),
            entities=self.extract_entities(raw_video.description),
            platform_specific_data={
                "tiktok_id": raw_video.id,
                "video_url": raw_video.video_url,
                "music": raw_video.music_info,
                "duration": raw_video.duration
            }
        )
    
    def normalize_xhs_data(self, raw_note: RawXHSNote) -> Feed:
        """Standardize XiaoHongShu data to Feed format"""
        return Feed(
            id=self.generate_feed_id(),
            text=raw_note.title + "\n\n" + raw_note.content,
            author_id=raw_note.user.id,
            platform="xiaohongshu",
            created_at=raw_note.create_time,
            feed_type=FeedType.POST,
            public_metrics=PublicMetrics(
                like_count=raw_note.likes,
                retweet_count=raw_note.shares,
                reply_count=raw_note.comments,
                quote_count=0,
                bookmark_count=raw_note.collects
            ),
            entities=self.extract_entities(raw_note.content),
            platform_specific_data={
                "xhs_note_id": raw_note.id,
                "images": raw_note.images,
                "tags": raw_note.tags,
                "topic": raw_note.topic
            }
        )
    
    def normalize_youtube_data(self, raw_video: RawYouTubeVideo) -> Feed:
        """Standardize YouTube data to Feed format"""
        return Feed(
            id=self.generate_feed_id(),
            text=raw_video.title + "\n\n" + raw_video.description,
            author_id=raw_video.channel.id,
            platform="youtube",
            created_at=raw_video.published_at,
            feed_type=FeedType.POST,
            public_metrics=PublicMetrics(
                like_count=raw_video.like_count,
                retweet_count=0,
                reply_count=raw_video.comment_count,
                quote_count=0,
                bookmark_count=0,
                impression_count=raw_video.view_count
            ),
            entities=self.extract_entities(raw_video.description),
            platform_specific_data={
                "youtube_id": raw_video.id,
                "video_url": raw_video.url,
                "duration": raw_video.duration,
                "category": raw_video.category,
                "tags": raw_video.tags
            }
        )
```

---

### 3. Trend Detector (`data_processing/trend_detector.py`)

```python
class TrendDetector:
    """Detect emerging trends and viral patterns"""
    
    def detect_emerging_trends(self, content_stream: List[Feed]) -> List[EmergingTrend]:
        """Detect new emerging trends from content stream"""
        # Extract hashtags and topics
        hashtag_counts = self._count_hashtags(content_stream)
        topic_counts = self._count_topics(content_stream)
        
        # Compare with historical data
        historical_averages = self._get_historical_averages()
        
        emerging = []
        for hashtag, count in hashtag_counts.items():
            if self._is_emerging(hashtag, count, historical_averages.get(hashtag, 0)):
                trend = EmergingTrend(
                    name=hashtag,
                    current_volume=count,
                    growth_rate=self._calculate_growth_rate(hashtag, count),
                    detected_at=datetime.now()
                )
                emerging.append(trend)
        
        return emerging
    
    def analyze_trend_lifecycle(self, trend: str, time_window: int = 24) -> TrendLifecycle:
        """Analyze trend lifecycle over time window (hours)"""
        # Get trend data over time
        timeline_data = self._get_trend_timeline(trend, time_window)
        
        # Identify lifecycle phases
        phases = self._identify_lifecycle_phases(timeline_data)
        
        return TrendLifecycle(
            trend=trend,
            emergence_time=phases.emergence,
            peak_time=phases.peak,
            current_phase=phases.current,
            momentum=self._calculate_momentum(timeline_data)
        )
    
    def predict_trend_virality(self, trend_data: TrendData) -> ViralityPrediction:
        """Predict if trend will go viral"""
        features = self._extract_trend_features(trend_data)
        
        # Predictive model
        virality_score = self.virality_model.predict(features)
        
        return ViralityPrediction(
            trend=trend_data.name,
            virality_probability=virality_score,
            estimated_peak_reach=self._estimate_reach(virality_score),
            time_to_peak=self._estimate_time_to_peak(features)
        )
    
    def identify_trend_accelerators(self, trend: str) -> List[TrendAccelerator]:
        """Identify influencers/events accelerating the trend"""
        # Find high-influence users posting about trend
        trend_posts = self._get_posts_by_trend(trend)
        
        accelerators = []
        for post in trend_posts:
            if self._is_accelerator(post):
                accelerators.append(TrendAccelerator(
                    user_id=post.author_id,
                    influence_score=self._calculate_influence(post.author_id),
                    contribution=self._calculate_contribution(post, trend)
                ))
        
        return sorted(accelerators, key=lambda x: x.contribution, reverse=True)
```

---

### 4. Storage System (`storage/raw_data_store.py`)

```python
class RawDataStore:
    """Store and manage raw scraped data"""
    
    def __init__(self, storage_config: StorageConfig):
        self.db_connection = self.create_connection(storage_config)
        self.file_storage = FileStorage(storage_config.file_path)
    
    async def store_raw_content(self, platform: str, content: Dict) -> str:
        """Store raw content from platform"""
        # Generate unique ID
        content_id = self._generate_id(platform, content)
        
        # Store in database
        await self.db_connection.execute(
            "INSERT INTO raw_content (id, platform, data, scraped_at) VALUES (?, ?, ?, ?)",
            (content_id, platform, json.dumps(content), datetime.now())
        )
        
        # Also store in file system for backup
        await self.file_storage.save(content_id, content)
        
        return content_id
    
    async def retrieve_raw_content(self, content_id: str) -> Dict:
        """Retrieve raw content by ID"""
        result = await self.db_connection.fetch_one(
            "SELECT data FROM raw_content WHERE id = ?",
            (content_id,)
        )
        
        return json.loads(result['data']) if result else None
    
    async def cleanup_old_data(self, retention_days: int = 30) -> int:
        """Clean up data older than retention period"""
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        result = await self.db_connection.execute(
            "DELETE FROM raw_content WHERE scraped_at < ?",
            (cutoff_date,)
        )
        
        return result.rowcount
```

---

### 5. Rate Limiter (`monitoring/rate_limiter.py`)

```python
class RateLimiter:
    """Enforce platform API rate limits"""
    
    def __init__(self, limits: Dict[str, RateLimit]):
        self.limits = limits
        self.request_counters = {}
    
    async def wait_if_needed(self, platform: str, endpoint: str) -> None:
        """Wait if rate limit is reached"""
        limit_key = f"{platform}:{endpoint}"
        limit = self.limits.get(limit_key)
        
        if not limit:
            return
        
        # Check current count
        current_count = self._get_current_count(limit_key)
        
        if current_count >= limit.max_requests:
            # Calculate wait time
            wait_time = self._calculate_wait_time(limit_key, limit)
            
            self.logger.warning(f"Rate limit reached for {limit_key}, waiting {wait_time}s")
            await asyncio.sleep(wait_time)
            
            # Reset counter
            self._reset_counter(limit_key)
    
    async def check_rate_limit(self, platform: str, endpoint: str) -> bool:
        """Check if within rate limit"""
        limit_key = f"{platform}:{endpoint}"
        limit = self.limits.get(limit_key)
        
        if not limit:
            return True
        
        current_count = self._get_current_count(limit_key)
        return current_count < limit.max_requests
    
    def increment_counter(self, platform: str, endpoint: str) -> None:
        """Increment request counter"""
        limit_key = f"{platform}:{endpoint}"
        
        if limit_key not in self.request_counters:
            self.request_counters[limit_key] = {
                'count': 0,
                'window_start': time.time()
            }
        
        self.request_counters[limit_key]['count'] += 1
```

---

## 🔌 Integration

### With Feed System

```python
async def publish_to_feed_system(self, normalized_feeds: List[Feed]) -> List[str]:
    """Publish normalized feeds to Feed system"""
    feed_ids = []
    
    for feed in normalized_feeds:
        # Save to Feed system
        feed_id = await self.feed_manager.save_feed(feed)
        feed_ids.append(feed_id)
        
        self.logger.info(f"Published feed {feed_id} to Feed system")
    
    return feed_ids
```

### With Arena System

```python
async def provide_trend_data_to_arena(self) -> TrendData:
    """Provide trend data to Arena for simulation"""
    # Get current trends
    trends = await self.trend_detector.get_current_trends()
    
    # Get viral content
    viral_content = await self.get_viral_content(threshold=0.7)
    
    return TrendData(
        trending_topics=trends,
        viral_content=viral_content,
        sentiment_overview=self._get_sentiment_overview(),
        platform_activity=self._get_platform_activity()
    )
```

---

## ⚙️ Configuration

```python
from scrapper.config import ScrapperConfig

config = ScrapperConfig(
    # Platform credentials
    twitter_api_key="your_api_key",
    twitter_api_secret="your_api_secret",
    
    # Rate limits
    rate_limits={
        "twitter:search": RateLimit(max_requests=180, window=900),
        "twitter:user_timeline": RateLimit(max_requests=900, window=900),
        "tiktok:trending": RateLimit(max_requests=100, window=3600)
    },
    
    # Storage
    database_url="postgresql://localhost/scrapper",
    redis_url="redis://localhost:6379",
    file_storage_path="./scraped_data",
    retention_days=30,
    
    # Processing
    enable_sentiment_analysis=True,
    enable_entity_extraction=True,
    enable_trend_detection=True,
    
    # Monitoring
    health_check_interval=60,  # seconds
    alert_threshold_errors=10,
    
    # Trace logging
    log_level="INFO",
    log_retention_days=30
)
```

---

## 🛠️ Development Guide

### Development Priority

#### Phase 1: Twitter Scraper (Priority) 🚧
1. Implement TwitterScraper basic functionality
2. Complete data normalization pipeline
3. Establish basic storage system
4. Add rate limiting

#### Phase 2: Trend Detection
1. Implement TrendDetector
2. Complete sentiment analysis
3. Build entity extraction
4. Add monitoring and health checks

#### Phase 3: Multi-Platform Support
1. Implement TikTok scraper
2. Implement XiaoHongShu scraper
3. Implement YouTube scraper
4. Unified API across platforms

#### Phase 4: Advanced Features
1. Real-time streaming
2. Advanced analytics
3. Machine learning integration
4. Distributed scraping

### Quick Start Example

```python
from scrapper import TwitterScraper, ContentNormalizer, FeedAggregator

# Initialize scraper
config = TwitterAPIConfig(api_key="...", api_secret="...")
scraper = TwitterScraper(config)

# Scrape trending topics
trends = await scraper.scrape_trending_topics()

# Scrape content for trend
content = []
for trend in trends[:5]:
    tweets = await scraper.scrape_hashtag_timeline(trend.name, max_results=100)
    content.extend(tweets)

# Normalize to Feed format
normalizer = ContentNormalizer()
feeds = [normalizer.normalize_twitter_data(tweet) for tweet in content]

# Aggregate and publish
aggregator = FeedAggregator(feed_manager)
feed_ids = await aggregator.aggregate_and_publish(feeds)

print(f"Published {len(feed_ids)} feeds to system")
```

---

## 📝 Trace Logging

**CRITICAL**: Use file-based trace logging. **NO console logs**.

### Log Structure

```
trace/
├── scrapers/          # Platform scraper logs
│   ├── twitter/
│   ├── tiktok/
│   └── youtube/
├── processing/        # Data processing logs
│   ├── normalization/
│   ├── enrichment/
│   └── trend_detection/
├── feeds/             # Feed system logs
├── storage/           # Storage operation logs
├── monitoring/        # Monitoring and health logs
├── errors/            # Error and exception logs
└── performance/       # Performance metrics
```

### Usage

   ```python
   from scrapper.utils.logger import get_logger

logger = get_logger(__name__, component="twitter_scraper")

# Log scraping activity
logger.info("Scraping trending topics", extra={
    "platform": "twitter",
    "location": "global",
    "max_results": 50
})

# Log success
logger.debug("Scraping completed", extra={
    "platform": "twitter",
    "items_scraped": len(tweets),
    "duration_ms": duration * 1000
})

# Log rate limit
logger.warning("Rate limit approaching", extra={
    "platform": "twitter",
    "endpoint": "search",
    "remaining": remaining_requests
})
```

---

## 🤝 Contributing

When contributing to Scrapper module:

1. **Respect Platform ToS** - Follow all platform guidelines
2. **Use Trace Logging** - Never use console logs
3. **Handle Rate Limits** - Implement proper rate limiting
4. **Privacy First** - Don't collect PII
5. **Test Thoroughly** - Mock API responses in tests

---

## 📖 Related Documentation

- [Arena Module](../Arena/README.md)
- [Feed Module](../Feed/README.md)
- [Logging Usage Guide](./LOGGING_USAGE.md)
- [Project Overview](../README.md)

---

**Scrapper - The Data Engine of Social-Arena** 🕷️📊

*Collecting real-world social media data to fuel realistic simulations*
