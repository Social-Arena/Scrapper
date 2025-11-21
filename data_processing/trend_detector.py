"""
Trend Detector - Detect emerging trends and viral patterns
"""

from typing import List, Dict, Any
from collections import Counter
from datetime import datetime

from Scrapper.scrapper.utils.logger import get_logger


class TrendDetector:
    """Detect emerging trends from content stream"""
    
    def __init__(self):
        self.logger = get_logger("TrendDetector")
        self.historical_counts: Dict[str, int] = {}
    
    def detect_emerging_trends(self, content_stream: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect emerging trends
        
        Args:
            content_stream: Stream of content (Feed format)
            
        Returns:
            List of emerging trends
        """
        # Extract hashtags
        hashtag_counts = Counter()
        
        for content in content_stream:
            entities = content.get("entities", {})
            hashtags = entities.get("hashtags", [])
            
            for hashtag in hashtags:
                tag = hashtag.get("tag", "")
                if tag:
                    hashtag_counts[tag] += 1
        
        # Compare with historical
        emerging = []
        
        for hashtag, count in hashtag_counts.most_common(20):
            historical = self.historical_counts.get(hashtag, 0)
            
            # Check if emerging (significant growth)
            if count > historical * 2 and count > 5:
                growth_rate = (count - historical) / max(historical, 1)
                
                emerging.append({
                    "name": hashtag,
                    "current_volume": count,
                    "historical_volume": historical,
                    "growth_rate": growth_rate,
                    "detected_at": datetime.now().isoformat()
                })
        
        # Update historical
        for hashtag, count in hashtag_counts.items():
            self.historical_counts[hashtag] = count
        
        self.logger.info(f"Trends detected", extra={
            "content_count": len(content_stream),
            "unique_hashtags": len(hashtag_counts),
            "emerging_count": len(emerging)
        })
        
        return emerging

