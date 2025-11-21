"""
Scrapper Manager - Orchestrates data collection from multiple platforms
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from Scrapper.config.scrapper_config import ScrapperConfig
from Scrapper.sources.twitter_scraper import TwitterScraper
from Scrapper.data_processing.content_normalizer import ContentNormalizer
from Scrapper.data_processing.trend_detector import TrendDetector
from Scrapper.storage.raw_data_store import RawDataStore
from Scrapper.scrapper.utils.logger import get_logger


class ScrapperManager:
    """Main scrapper manager orchestrating data collection"""
    
    def __init__(self, config: Optional[ScrapperConfig] = None):
        self.config = config or ScrapperConfig()
        self.logger = get_logger("ScrapperManager")
        
        # Initialize scrapers
        self.twitter_scraper = TwitterScraper(self.config)
        
        # Initialize processing
        self.content_normalizer = ContentNormalizer()
        self.trend_detector = TrendDetector()
        
        # Initialize storage
        self.raw_data_store = RawDataStore(self.config)
        
        # State
        self.is_initialized = False
        self.scraping_stats = {
            "total_scraped": 0,
            "by_platform": {}
        }
        
        self.logger.info("ScrapperManager created")
    
    async def initialize(self) -> None:
        """Initialize scrapper"""
        if self.is_initialized:
            return
        
        self.logger.info("Initializing Scrapper")
        
        # Create directories
        self.config.file_storage_path.mkdir(parents=True, exist_ok=True)
        self.config.trace_dir.mkdir(parents=True, exist_ok=True)
        
        self.is_initialized = True
        self.logger.info("Scrapper initialized")
    
    async def scrape_twitter_trending(self, location: str = "global") -> List[Dict[str, Any]]:
        """
        Scrape Twitter trending topics
        
        Args:
            location: Location for trends
            
        Returns:
            List of normalized Feed objects
        """
        # Scrape raw data
        raw_tweets = await self.twitter_scraper.scrape_trending_topics(location)
        
        # Store raw data
        for tweet in raw_tweets:
            await self.raw_data_store.store_raw_content("twitter", tweet)
        
        # Normalize to Feed format
        normalized = []
        for tweet in raw_tweets:
            feed = self.content_normalizer.normalize_twitter_data(tweet)
            normalized.append(feed)
        
        # Update stats
        self.scraping_stats["total_scraped"] += len(normalized)
        self.scraping_stats["by_platform"]["twitter"] = \
            self.scraping_stats["by_platform"].get("twitter", 0) + len(normalized)
        
        self.logger.info(f"Twitter scraping complete", extra={
            "location": location,
            "count": len(normalized)
        })
        
        return normalized
    
    async def detect_trends(self, content_stream: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect trends from content stream
        
        Args:
            content_stream: Stream of content
            
        Returns:
            List of detected trends
        """
        trends = self.trend_detector.detect_emerging_trends(content_stream)
        
        self.logger.info(f"Trends detected", extra={
            "content_count": len(content_stream),
            "trend_count": len(trends)
        })
        
        return trends
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get scraping statistics"""
        return self.scraping_stats.copy()

