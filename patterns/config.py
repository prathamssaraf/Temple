"""Configuration management for the patterns layer."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class PatternsConfig:
    """Configuration for the patterns layer."""

    # Indicator calculation
    calculate_indicators: bool = True

    # Pattern matching
    min_confidence: float = 0.5
    default_lookback_days: int = 365

    # Performance
    cache_indicators: bool = True
    parallel_matching: bool = False

    @classmethod
    def from_env(cls) -> "PatternsConfig":
        """Create configuration from environment variables."""
        return cls(
            calculate_indicators=os.getenv("PATTERNS_CALCULATE_INDICATORS", "true").lower() == "true",
            min_confidence=float(os.getenv("PATTERNS_MIN_CONFIDENCE", "0.5")),
            default_lookback_days=int(os.getenv("PATTERNS_LOOKBACK_DAYS", "365")),
            cache_indicators=os.getenv("PATTERNS_CACHE_INDICATORS", "true").lower() == "true",
            parallel_matching=os.getenv("PATTERNS_PARALLEL_MATCHING", "false").lower() == "true"
        )

    @classmethod
    def from_dict(cls, config_dict: dict) -> "PatternsConfig":
        """Create configuration from a dictionary."""
        return cls(**{k: v for k, v in config_dict.items() if k in cls.__annotations__})


# Global default configuration instance
_default_config: Optional[PatternsConfig] = None


def get_default_config() -> PatternsConfig:
    """Get the default configuration instance."""
    global _default_config
    if _default_config is None:
        _default_config = PatternsConfig.from_env()
    return _default_config


def set_default_config(config: PatternsConfig) -> None:
    """Set the default configuration instance."""
    global _default_config
    _default_config = config
