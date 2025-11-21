"""
Scrapper Example - Demonstrates data collection and processing
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from Scrapper import ScrapperManager, ScrapperConfig


async def main():
    """Main example function"""
    
    print("=" * 80)
    print("Scrapper - Multi-Platform Data Collection Example")
    print("=" * 80)
    print()
    
    # 1. Create configuration
    print("1. Creating Configuration...")
    config = ScrapperConfig(
        enable_sentiment_analysis=True,
        enable_entity_extraction=True,
        enable_trend_detection=True
    )
    print("✓ Configuration created")
    print()
    
    # 2. Initialize scrapper
    print("2. Initializing Scrapper...")
    scrapper = ScrapperManager(config)
    await scrapper.initialize()
    print("✓ Scrapper initialized")
    print()
    
    # 3. Scrape Twitter trending
    print("3. Scraping Twitter Trending Topics...")
    normalized_feeds = await scrapper.scrape_twitter_trending(location="global")
    print(f"✓ Scraped {len(normalized_feeds)} trending tweets")
    print()
    
    # 4. Show sample feeds
    print("4. Sample Normalized Feeds:")
    for i, feed in enumerate(normalized_feeds[:3], 1):
        print(f"\n   Feed {i}:")
        print(f"   - ID: {feed['id']}")
        print(f"   - Text: {feed['text'][:60]}...")
        print(f"   - Platform: {feed['platform']}")
        print(f"   - Likes: {feed['public_metrics']['like_count']}")
        print(f"   - Retweets: {feed['public_metrics']['retweet_count']}")
        
        hashtags = feed.get('entities', {}).get('hashtags', [])
        if hashtags:
            tags = [h['tag'] for h in hashtags]
            print(f"   - Hashtags: {', '.join(tags)}")
    
    print()
    
    # 5. Detect trends
    print("5. Detecting Trends...")
    trends = await scrapper.detect_trends(normalized_feeds)
    print(f"✓ Detected {len(trends)} emerging trends")
    
    if trends:
        print("\n   Top Trends:")
        for i, trend in enumerate(trends[:5], 1):
            print(f"   {i}. #{trend['name']}")
            print(f"      Volume: {trend['current_volume']}")
            print(f"      Growth: {trend['growth_rate']:.1%}")
    
    print()
    
    # 6. Get statistics
    print("6. Scraping Statistics:")
    stats = scrapper.get_statistics()
    print(f"   - Total scraped: {stats['total_scraped']}")
    print(f"   - By platform:")
    for platform, count in stats['by_platform'].items():
        print(f"      {platform}: {count}")
    print()
    
    print("=" * 80)
    print("Scrapper Example Complete!")
    print("=" * 80)
    print()
    print("Data Collection Pipeline:")
    print("  1. Platform Scraping ✓")
    print("  2. Data Normalization ✓")
    print("  3. Trend Detection ✓")
    print("  4. Storage ✓")
    print()


if __name__ == "__main__":
    asyncio.run(main())

