"""
Content Normalizer - Convert platform data to Feed format
"""

from typing import Dict, Any, List
from datetime import datetime
import uuid

from Scrapper.scrapper.utils.logger import get_logger


class ContentNormalizer:
    """Normalize content from different platforms to Feed format"""
    
    def __init__(self):
        self.logger = get_logger("ContentNormalizer")
    
    def normalize_twitter_data(self, raw_tweet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standardize Twitter data to Feed format
        
        Args:
            raw_tweet: Raw tweet data
            
        Returns:
            Normalized Feed dictionary
        """
        feed_id = self.generate_feed_id()
        
        feed = {
            "id": feed_id,
            "text": raw_tweet.get("text", ""),
            "author_id": raw_tweet.get("user", {}).get("id", "unknown"),
            "platform": "twitter",
            "created_at": raw_tweet.get("created_at", datetime.now().isoformat() + "Z"),
            "feed_type": "post",
            "public_metrics": {
                "like_count": raw_tweet.get("like_count", 0),
                "retweet_count": raw_tweet.get("retweet_count", 0),
                "reply_count": raw_tweet.get("reply_count", 0),
                "quote_count": raw_tweet.get("quote_count", 0),
                "bookmark_count": 0
            },
            "entities": self.extract_entities(raw_tweet.get("text", "")),
            "platform_specific_data": {
                "twitter_id": raw_tweet.get("id"),
                "twitter_metrics": raw_tweet.get("public_metrics", {})
            },
            "lang": "en",
            "source": "Twitter Web App"
        }
        
        return feed
    
    def generate_feed_id(self) -> str:
        """Generate unique feed ID"""
        return str(uuid.uuid4()).replace("-", "")[:16]
    
    def extract_entities(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """Extract entities from text"""
        import re
        
        entities = {
            "hashtags": [],
            "mentions": [],
            "urls": []
        }
        
        # Extract hashtags
        hashtags = re.findall(r'#(\w+)', text)
        for tag in hashtags:
            entities["hashtags"].append({"tag": tag})
        
        # Extract mentions
        mentions = re.findall(r'@(\w+)', text)
        for username in mentions:
            entities["mentions"].append({"username": username})
        
        # Extract URLs
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+', text)
        for url in urls:
            entities["urls"].append({"url": url})
        
        return entities

