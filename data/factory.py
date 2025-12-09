"""Factory for creating data layer components."""

from typing import Optional
import logging

from .config import DataConfig, get_default_config
from .provider import DataProvider, YahooDataProvider
from .cache import DataCache
from .repository import DataRepository


class DataFactory:
    """Factory for creating configured data layer instances."""

    @staticmethod
    def create_provider(provider_name: str = "yahoo") -> DataProvider:
        """
        Create a data provider instance.

        Args:
            provider_name: Name of the provider ("yahoo" is currently supported)

        Returns:
            DataProvider instance

        Raises:
            ValueError: If provider_name is not supported
        """
        if provider_name.lower() == "yahoo":
            return YahooDataProvider()
        else:
            raise ValueError(f"Unsupported provider: {provider_name}. Supported: yahoo")

    @staticmethod
    def create_cache(config: Optional[DataConfig] = None) -> DataCache:
        """
        Create a cache instance.

        Args:
            config: Configuration object (uses default if not provided)

        Returns:
            DataCache instance
        """
        if config is None:
            config = get_default_config()

        return DataCache(
            cache_dir=config.cache_dir,
            ohlcv_ttl_hours=config.ohlcv_ttl_hours,
            fundamentals_ttl_days=config.fundamentals_ttl_days
        )

    @staticmethod
    def create_repository(
        config: Optional[DataConfig] = None,
        provider: Optional[DataProvider] = None,
        cache: Optional[DataCache] = None
    ) -> DataRepository:
        """
        Create a fully configured DataRepository.

        Args:
            config: Configuration object (uses default if not provided)
            provider: Custom provider instance (creates default if not provided)
            cache: Custom cache instance (creates default if not provided)

        Returns:
            DataRepository instance
        """
        if config is None:
            config = get_default_config()

        if provider is None:
            provider = DataFactory.create_provider(config.provider)

        if cache is None:
            cache = DataFactory.create_cache(config)

        return DataRepository(provider=provider, cache=cache)


def create_data_repository(config: Optional[DataConfig] = None) -> DataRepository:
    """
    Convenience function to create a DataRepository with default configuration.

    This is the recommended way to instantiate the data layer for most use cases.

    Args:
        config: Optional configuration (uses environment-based defaults if not provided)

    Returns:
        Fully configured DataRepository instance

    Example:
        ```python
        from data import create_data_repository

        repo = create_data_repository()
        df = repo.get_ohlcv("AAPL")
        ```
    """
    return DataFactory.create_repository(config=config)
