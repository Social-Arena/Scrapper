"""
Scrapper - Multi-Platform Data Collection Engine
"""

__version__ = "0.1.0"

from .core.scrapper_manager import ScrapperManager
from .config.scrapper_config import ScrapperConfig

__all__ = [
    '__version__',
    'ScrapperManager',
    'ScrapperConfig',
]

