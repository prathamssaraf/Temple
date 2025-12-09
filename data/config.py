"""Configuration management for the data layer."""

import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class DataConfig:
    """Configuration for the data layer."""

    # Cache settings
    cache_dir: str = "./cache"
    ohlcv_ttl_hours: int = 24
    fundamentals_ttl_days: int = 7

    # Provider settings
    provider: str = "yahoo"  # Currently only "yahoo" is supported

    # Data fetching defaults
    default_period: str = "2y"

    @classmethod
    def from_env(cls) -> "DataConfig":
        """Create configuration from environment variables."""
        return cls(
            cache_dir=os.getenv("CACHE_DIR", "./cache"),
            ohlcv_ttl_hours=int(os.getenv("OHLCV_TTL_HOURS", "24")),
            fundamentals_ttl_days=int(os.getenv("FUNDAMENTALS_TTL_DAYS", "7")),
            provider=os.getenv("DATA_PROVIDER", "yahoo"),
            default_period=os.getenv("DEFAULT_PERIOD", "2y")
        )

    @classmethod
    def from_dict(cls, config_dict: dict) -> "DataConfig":
        """Create configuration from a dictionary."""
        return cls(**{k: v for k, v in config_dict.items() if k in cls.__annotations__})


# Global default configuration instance
_default_config: Optional[DataConfig] = None


def get_default_config() -> DataConfig:
    """Get the default configuration instance."""
    global _default_config
    if _default_config is None:
        _default_config = DataConfig.from_env()
    return _default_config


def set_default_config(config: DataConfig) -> None:
    """Set the default configuration instance."""
    global _default_config
    _default_config = config
