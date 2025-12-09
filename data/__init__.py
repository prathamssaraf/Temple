"""
Temple Data Layer - Stock data acquisition and caching.

This module provides a clean, cacheable interface for fetching stock market data.

Quick Start
-----------
The simplest way to use the data layer:

    from data import create_data_repository

    repo = create_data_repository()
    df = repo.get_ohlcv("AAPL")
    fundamentals = repo.get_fundamentals("AAPL")

Configuration
-------------
Configure via environment variables or programmatically:

    from data import DataConfig, create_data_repository

    config = DataConfig(
        cache_dir="./my_cache",
        ohlcv_ttl_hours=12,
        fundamentals_ttl_days=3
    )
    repo = create_data_repository(config)

Advanced Usage
--------------
For custom providers or caches:

    from data import DataFactory, YahooDataProvider, DataCache

    provider = YahooDataProvider()
    cache = DataCache(cache_dir="./custom_cache")
    repo = DataFactory.create_repository(provider=provider, cache=cache)
"""

# Public API - Configuration
from .config import (
    DataConfig,
    get_default_config,
    set_default_config
)

# Public API - Core Components
from .repository import DataRepository
from .provider import DataProvider, YahooDataProvider
from .cache import DataCache

# Public API - Factory (recommended entry point)
from .factory import (
    DataFactory,
    create_data_repository
)

# Define public interface
__all__ = [
    # Configuration
    "DataConfig",
    "get_default_config",
    "set_default_config",
    # Core components
    "DataRepository",
    "DataProvider",
    "YahooDataProvider",
    "DataCache",
    # Factory (recommended)
    "DataFactory",
    "create_data_repository",
]

# Version
__version__ = "0.1.0"
