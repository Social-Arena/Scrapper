"""
Raw Data Store - Store and manage raw scraped data
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import json
from pathlib import Path

from Scrapper.config.scrapper_config import ScrapperConfig
from Scrapper.scrapper.utils.logger import get_logger


class RawDataStore:
    """Store and manage raw scraped data"""
    
    def __init__(self, config: ScrapperConfig):
        self.config = config
        self.logger = get_logger("RawDataStore")
        
        # File storage
        self.storage_path = config.file_storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # In-memory index (for mock database)
        self.index: Dict[str, Dict[str, Any]] = {}
    
    async def store_raw_content(self, platform: str, content: Dict[str, Any]) -> str:
        """
        Store raw content
        
        Args:
            platform: Platform name
            content: Raw content data
            
        Returns:
            Content ID
        """
        # Generate unique ID
        content_id = self._generate_id(platform, content)
        
        # Add metadata
        storage_data = {
            "id": content_id,
            "platform": platform,
            "data": content,
            "scraped_at": datetime.now().isoformat()
        }
        
        # Store in file
        await self._store_to_file(content_id, storage_data)
        
        # Store in index
        self.index[content_id] = storage_data
        
        self.logger.debug(f"Raw content stored", extra={
            "content_id": content_id,
            "platform": platform
        })
        
        return content_id
    
    async def retrieve_raw_content(self, content_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve raw content by ID
        
        Args:
            content_id: Content ID
            
        Returns:
            Raw content data or None
        """
        if content_id in self.index:
            return self.index[content_id]["data"]
        
        # Try loading from file
        file_path = self.storage_path / f"{content_id}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data["data"]
        
        return None
    
    async def cleanup_old_data(self, retention_days: int = 30) -> int:
        """
        Clean up old data
        
        Args:
            retention_days: Retention period
            
        Returns:
            Number of items deleted
        """
        cutoff = datetime.now() - timedelta(days=retention_days)
        removed = 0
        
        for content_id, data in list(self.index.items()):
            scraped_at = datetime.fromisoformat(data["scraped_at"])
            
            if scraped_at < cutoff:
                # Remove from index
                del self.index[content_id]
                
                # Remove file
                file_path = self.storage_path / f"{content_id}.json"
                if file_path.exists():
                    file_path.unlink()
                
                removed += 1
        
        self.logger.info(f"Cleaned up old data", extra={
            "removed_count": removed,
            "retention_days": retention_days
        })
        
        return removed
    
    def _generate_id(self, platform: str, content: Dict[str, Any]) -> str:
        """Generate unique content ID"""
        import hashlib
        
        # Use platform + original ID if available
        original_id = content.get("id", "")
        if original_id:
            combined = f"{platform}_{original_id}"
        else:
            combined = f"{platform}_{datetime.now().timestamp()}_{hash(str(content))}"
        
        return hashlib.md5(combined.encode()).hexdigest()
    
    async def _store_to_file(self, content_id: str, data: Dict[str, Any]) -> None:
        """Store data to file"""
        file_path = self.storage_path / f"{content_id}.json"
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

