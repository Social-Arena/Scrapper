# Scrapper System Architecture

> Software Engineering Architecture Documentation  
> Generated: 2025-11-21

## Table of Contents

1. [Overview](#overview)
2. [Architecture Diagram](#architecture-diagram)
3. [System Layers](#system-layers)
4. [Design Patterns](#design-patterns)
5. [Data Flow](#data-flow)
6. [Component Specifications](#component-specifications)
7. [Technology Stack](#technology-stack)
8. [Implementation Status](#implementation-status)

---

## Overview

**Scrapper** is a comprehensive social media data collection engine designed to gather, process, and normalize content from multiple platforms (Twitter, TikTok, XiaoHongShu, YouTube). It follows an ETL (Extract, Transform, Load) pipeline architecture with robust monitoring and logging capabilities.

### Key Characteristics

- **Multi-platform Support**: Unified interface for diverse social media platforms
- **Scalable Architecture**: Async/await patterns for concurrent operations
- **Comprehensive Observability**: File-based structured logging with performance tracking
- **Modular Design**: Clear separation of concerns across layers
- **Production-Ready**: Rate limiting, health checks, and error handling

---

## Architecture Diagram

See [`Structure.mermaid`](./Structure.mermaid) for the visual representation.

### Legend

- 🟢 **Green**: Fully implemented components
- 🟡 **Orange**: Planned/In-progress components
- 🔴 **Pink**: External dependencies (APIs)
- 🔵 **Blue**: Infrastructure components
- 🟣 **Purple**: Logging/trace system

---

## System Layers

### 1. **Data Collection Layer** (`sources/`)

**Purpose**: Extract raw data from social media platforms

**Components**:
- `TwitterScraper`: Scrapes tweets, trends, user timelines
- `TikTokScraper`: Collects viral videos and trends
- `XiaoHongShuScraper`: Gathers lifestyle content
- `YouTubeScraper`: Fetches trending videos

**Responsibilities**:
- Platform-specific API communication
- Authentication and session management
- Rate limit adherence
- Raw data extraction

**Key Features**:
- Async/await for concurrent scraping
- Automatic retry with exponential backoff
- Request/response logging
- Platform-specific error handling

---

### 2. **Core Orchestration Layer** (`core/`)

**Purpose**: Coordinate and manage scraping operations

**Components**:
- `ScrapperManager`: Central orchestrator for all scrapers

**Responsibilities**:
- Scraper lifecycle management
- Task scheduling and prioritization
- Resource allocation
- Cross-platform coordination

**Key Features**:
- Dynamic scraper registration
- Concurrent session management
- Graceful shutdown handling
- Health monitoring integration

---

### 3. **Data Processing Layer** (`data_processing/`)

**Purpose**: Transform and enrich raw data

**Components**:
- `ContentNormalizer`: Converts platform-specific data to unified format
- `TrendDetector`: Identifies viral content and trending topics
- `SentimentAnalyzer`: Performs sentiment analysis and emotional classification

**Responsibilities**:
- Data validation and sanitization
- Format normalization
- Feature extraction
- Metadata enrichment

**Key Features**:
- Schema validation
- Data quality scoring
- Duplicate detection
- Anomaly identification

---

### 4. **Feed System Layer** (`feeds/`)

**Purpose**: Aggregate and enrich normalized content

**Components**:
- `FeedAggregator`: Combines content from multiple platforms
- `FeedEnricher`: Adds analysis, tags, and metadata

**Responsibilities**:
- Multi-platform feed synthesis
- Chronological ordering
- Relevance scoring
- Topic classification

**Key Features**:
- Smart deduplication
- Cross-platform correlation
- Temporal analysis
- Virality prediction

---

### 5. **Storage Layer** (`storage/`)

**Purpose**: Persist and cache data

**Components**:
- `RawDataStore`: PostgreSQL-based persistent storage
- `CacheManager`: Redis-based caching layer

**Responsibilities**:
- Data persistence
- Query optimization
- Cache invalidation
- Data retention policies

**Key Features**:
- Connection pooling
- Automatic data archival
- Cache warming strategies
- Query performance optimization

---

### 6. **Monitoring Layer** (`monitoring/`)

**Purpose**: Observe system health and performance

**Components**:
- `ScrapingMonitor`: Tracks scraper health and data quality
- `RateLimiter`: Controls API request rates
- `HealthCheck`: System-wide health monitoring

**Responsibilities**:
- Performance metric collection
- Rate limit enforcement
- Anomaly detection
- Alert generation

**Key Features**:
- Real-time metrics
- Adaptive rate limiting
- SLA monitoring
- Resource utilization tracking

---

### 7. **Configuration & Utilities Layer** (`config/`, `utils/`)

**Purpose**: Provide cross-cutting concerns

**Components**:
- `Configuration`: System-wide configuration management
- `Logger`: Centralized logging utility ✅ **IMPLEMENTED**
- `LoggingConfig`: Logging system configuration ✅ **IMPLEMENTED**

**Responsibilities**:
- Configuration loading and validation
- Structured logging
- Log rotation and archival
- Performance instrumentation

**Key Features**:
- File-based logging (NO console output)
- Component-specific log routing
- Automatic log rotation (10MB files, 5 backups)
- JSON structured logging support
- Performance tracking context managers

---

### 8. **Trace System** (`trace/`)

**Purpose**: Store and organize runtime logs ✅ **IMPLEMENTED**

**Structure**:
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

**Features**:
- Automatic directory creation
- Log rotation per component
- Structured error tracking
- Performance profiling

---

## Design Patterns

### 1. **ETL Pipeline Pattern**

```
Extract (Scrapers) → Transform (Normalizers/Analyzers) → Load (Storage)
```

**Benefits**:
- Clear data flow
- Easy to test each stage
- Scalable processing
- Fault isolation

### 2. **Repository Pattern**

`RawDataStore` and `CacheManager` abstract data access

**Benefits**:
- Database independence
- Easy mocking for tests
- Centralized data access logic
- Cache transparency

### 3. **Observer Pattern**

`ScrapingMonitor` observes scrapers without tight coupling

**Benefits**:
- Loose coupling
- Dynamic monitoring
- Easy to add new monitors
- Separation of concerns

### 4. **Decorator Pattern**

`@log_decorator` for automatic performance logging

**Benefits**:
- Reduces boilerplate
- Consistent logging
- Easy to apply/remove
- Non-invasive instrumentation

### 5. **Factory Pattern**

Dynamic scraper instantiation based on platform

**Benefits**:
- Flexible scraper creation
- Easy to add new platforms
- Configuration-driven
- Centralized instantiation logic

### 6. **Strategy Pattern**

Platform-specific scraping strategies

**Benefits**:
- Algorithm encapsulation
- Runtime strategy selection
- Easy to test strategies
- Platform isolation

---

## Data Flow

### Primary Pipeline

```
1. API Request
   ├─> Platform APIs receive requests
   └─> Return raw JSON/XML data

2. Data Collection
   ├─> Scrapers fetch data
   ├─> RateLimiter controls request rate
   └─> ScrapingMonitor tracks progress

3. Orchestration
   ├─> ScrapperManager coordinates scrapers
   └─> Routes data to processing

4. Transformation
   ├─> ContentNormalizer creates unified format
   ├─> TrendDetector identifies patterns
   └─> SentimentAnalyzer adds sentiment

5. Aggregation
   ├─> FeedAggregator combines platforms
   └─> FeedEnricher adds metadata

6. Persistence
   ├─> RawDataStore saves to PostgreSQL
   └─> CacheManager updates Redis

7. Output
   └─> Unified Feed System for downstream consumers
```

### Monitoring Flow

```
All Components
   ├─> Logger (utils/logger.py)
   ├─> Component-specific logs (trace/)
   ├─> Error logs (trace/errors/)
   └─> Performance metrics (trace/performance/)
```

---

## Component Specifications

### ScrapperManager (Orchestrator)

**File**: `core/scrapper_manager.py`

**Interface**:
```python
class ScrapperManager:
    def __init__(self, config: Config)
    async def start(self) -> None
    async def stop(self) -> None
    def register_scraper(self, scraper: BaseScraper) -> None
    async def scrape_all(self) -> Dict[str, List[Feed]]
    def get_status(self) -> Dict[str, Any]
```

**Key Methods**:
- `start()`: Initialize and start all scrapers
- `stop()`: Graceful shutdown
- `register_scraper()`: Dynamic scraper registration
- `scrape_all()`: Coordinate multi-platform scraping
- `get_status()`: System health snapshot

---

### ContentNormalizer (Transformer)

**File**: `data_processing/content_normalizer.py`

**Interface**:
```python
class ContentNormalizer:
    def __init__(self)
    def normalize(self, raw_data: dict, platform: str) -> Feed
    def normalize_batch(self, raw_data_list: List[dict], platform: str) -> List[Feed]
    def validate(self, feed: Feed) -> bool
```

**Normalization Schema**:
```python
Feed = {
    "id": str,              # Unique identifier
    "platform": str,        # Source platform
    "content_type": str,    # tweet, video, post, etc.
    "text": str,           # Main content
    "author": {            # Author info
        "id": str,
        "name": str,
        "followers": int
    },
    "metrics": {           # Engagement metrics
        "views": int,
        "likes": int,
        "shares": int,
        "comments": int
    },
    "metadata": {          # Additional metadata
        "created_at": datetime,
        "language": str,
        "location": str,
        "hashtags": List[str],
        "mentions": List[str]
    },
    "media": List[MediaItem],
    "normalized_at": datetime
}
```

---

### Logger (Utility) ✅

**File**: `scrapper/utils/logger.py`

**Interface**:
```python
def initialize_logging(log_level: str = "INFO") -> None
def get_logger(component_name: str, log_level: Optional[str] = None, use_json: bool = False) -> logging.Logger
def log_performance(logger: Logger, operation_name: str, **context) -> ContextManager
def log_error_with_context(logger: Logger, error: Exception, context: Dict, include_traceback: bool = True) -> None
def log_api_call(logger: Logger, endpoint: str, method: str = "GET", **params) -> None
def log_data_operation(logger: Logger, operation: str, data_type: str, count: int, **metadata) -> None
def log_scraping_session(logger: Logger, platform: str, session_type: str, status: str, **metrics) -> None
```

**Features**:
- NO console output (all logs to files)
- Automatic log rotation
- Component-specific routing
- Performance tracking
- Structured logging with JSON support

---

### RateLimiter (Monitor)

**File**: `monitoring/rate_limiter.py`

**Interface**:
```python
class RateLimiter:
    def __init__(self, config: Dict[str, RateLimit])
    async def acquire(self, platform: str, endpoint: str) -> None
    async def release(self, platform: str, endpoint: str) -> None
    def get_remaining(self, platform: str) -> int
    def reset_time(self, platform: str) -> datetime
```

**Rate Limiting Strategy**:
- Token bucket algorithm
- Per-platform limits
- Per-endpoint granularity
- Automatic backoff
- Redis-backed state (distributed)

---

## Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.9+ | Core implementation |
| **Async Runtime** | asyncio | Concurrent operations |
| **HTTP Client** | aiohttp | Async HTTP requests |
| **Database** | PostgreSQL | Persistent storage |
| **Cache** | Redis | In-memory caching |
| **Logging** | Python logging | Structured logging |

### Data Processing

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Data Processing** | pandas | Data manipulation |
| **HTML Parsing** | BeautifulSoup4 | Web scraping |
| **NLP** | spaCy | Entity recognition |
| **ML** | scikit-learn | Classification |
| **Transformers** | Hugging Face | Sentiment analysis |

### Development Tools

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Testing** | pytest | Unit/integration tests |
| **Formatting** | black | Code formatting |
| **Linting** | flake8 | Code quality |
| **Type Checking** | mypy | Static type checking |

---

## Implementation Status

### ✅ Fully Implemented

- [x] Centralized logging system
- [x] Log rotation and management
- [x] Component-specific log routing
- [x] Performance tracking utilities
- [x] Error logging with context
- [x] Structured logging (JSON support)
- [x] Trace directory structure
- [x] Configuration framework

### 🚧 In Progress (Bytecode Present)

Based on compiled `.pyc` files found:
- [x] `ScrapperManager` (core/scrapper_manager.py)
- [x] `ContentNormalizer` (data_processing/content_normalizer.py)
- [x] `TrendDetector` (data_processing/trend_detector.py)
- [x] `RawDataStore` (storage/raw_data_store.py)
- [x] `TwitterScraper` (sources/twitter_scraper.py)
- [x] `scrapper_config` (config/scrapper_config.py)

### 📋 Planned Features

- [ ] TikTok scraper implementation
- [ ] XiaoHongShu scraper implementation
- [ ] YouTube scraper implementation
- [ ] Sentiment analyzer implementation
- [ ] Feed aggregator implementation
- [ ] Feed enricher implementation
- [ ] Cache manager implementation
- [ ] Scraping monitor implementation
- [ ] Rate limiter implementation
- [ ] Health check system
- [ ] Real-time streaming support
- [ ] Distributed scraping
- [ ] ML model integration
- [ ] Advanced analytics

---

## Development Roadmap

### Phase 1: Foundation ✅ (Current)
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

---

## Integration Points

### Upstream (Data Sources)

- Twitter API v2
- TikTok Research API
- XiaoHongShu (unofficial API)
- YouTube Data API v3

### Downstream (Consumers)

- **Arena System**: Viral propagation simulation
- **Analytics Dashboard**: Real-time metrics
- **Feed API**: RESTful feed access
- **ML Pipeline**: Training data source

---

## Performance Characteristics

### Target Metrics

| Metric | Target | Status |
|--------|--------|--------|
| **Scraping Throughput** | 10K items/hour | 📋 Planned |
| **Normalization Latency** | < 100ms/item | 📋 Planned |
| **Storage Write Rate** | 1K writes/sec | 📋 Planned |
| **Cache Hit Rate** | > 90% | 📋 Planned |
| **API Error Rate** | < 1% | 📋 Planned |

### Scalability

- **Horizontal Scaling**: Multiple scraper instances
- **Vertical Scaling**: Async concurrency within instances
- **Database Scaling**: Read replicas, connection pooling
- **Cache Scaling**: Redis cluster

---

## Security Considerations

- API credentials stored in environment variables
- Rate limiting to prevent abuse
- No PII collection
- Data anonymization support
- GDPR compliance features
- Secure credential rotation

---

## Monitoring and Observability

### Logging ✅

- File-based logging (NO console output)
- Component-specific logs
- Error tracking with full tracebacks
- Performance profiling
- Structured JSON logging

### Metrics (Planned)

- Scraping throughput
- API response times
- Error rates
- Cache hit rates
- Storage latency

### Alerts (Planned)

- API rate limit exceeded
- Scraper failures
- Data quality degradation
- System resource exhaustion

---

## Testing Strategy

### Unit Tests

- Component isolation
- Mock external dependencies
- Test coverage > 80%

### Integration Tests

- End-to-end pipeline
- Database interactions
- API mocking

### Performance Tests

- Load testing
- Stress testing
- Endurance testing

---

## References

- [README.md](./README.md) - Project overview
- [LOGGING_USAGE.md](./LOGGING_USAGE.md) - Logging guide
- [trace/README.md](./trace/README.md) - Debugging guide
- [Structure.mermaid](./Structure.mermaid) - Architecture diagram

---

**Last Updated**: 2025-11-21  
**Version**: 0.1.0  
**Status**: Active Development

