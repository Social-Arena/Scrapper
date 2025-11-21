"""
Scrapper Configuration Management
"""

from typing import Dict, Any
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RateLimit:
    """Rate limit configuration"""
    max_requests: int
    window_seconds: int


@dataclass
class ScrapperConfig:
    """Configuration for scrapper system"""
    
    # Platform credentials (mock for now)
    twitter_api_key: str = "mock_key"
    twitter_api_secret: str = "mock_secret"
    
    # Rate limits
    rate_limits: Dict[str, RateLimit] = field(default_factory=lambda: {
        "twitter_search": RateLimit(180, 900),
        "twitter_timeline": RateLimit(900, 900),
        "tiktok_trending": RateLimit(100, 3600)
    })
    
    # Storage
    database_url: str = "postgresql://localhost/scrapper"
    redis_url: str = "redis://localhost:6379"
    file_storage_path: Path = field(default_factory=lambda: Path("./scraped_data"))
    retention_days: int = 30
    
    # Processing
    enable_sentiment_analysis: bool = True
    enable_entity_extraction: bool = True
    enable_trend_detection: bool = True
    
    # Monitoring
    health_check_interval: int = 60  # seconds
    alert_threshold_errors: int = 10
    
    # Trace logging
    log_level: str = "INFO"
    log_retention_days: int = 30
    trace_dir: Path = field(default_factory=lambda: Path("trace"))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "twitter_api_key": "***",  # Don't expose keys
            "enable_sentiment_analysis": self.enable_sentiment_analysis,
            "enable_entity_extraction": self.enable_entity_extraction,
            "enable_trend_detection": self.enable_trend_detection,
            "retention_days": self.retention_days
        }


def get_default_config() -> ScrapperConfig:
    """Get default scrapper configuration"""
    return ScrapperConfig()

