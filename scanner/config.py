"""Configuration management for the scanner layer."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ScannerConfig:
    """Configuration for the scanner layer."""

    # Performance settings
    parallel: bool = False
    max_workers: int = 4

    # Scan defaults
    default_min_confidence: float = 0.5
    default_top_n: int = 10

    # Progress tracking
    show_progress: bool = True
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "ScannerConfig":
        """Create configuration from environment variables."""
        return cls(
            parallel=os.getenv("SCANNER_PARALLEL", "false").lower() == "true",
            max_workers=int(os.getenv("SCANNER_MAX_WORKERS", "4")),
            default_min_confidence=float(os.getenv("SCANNER_MIN_CONFIDENCE", "0.5")),
            default_top_n=int(os.getenv("SCANNER_TOP_N", "10")),
            show_progress=os.getenv("SCANNER_SHOW_PROGRESS", "true").lower() == "true",
            log_level=os.getenv("SCANNER_LOG_LEVEL", "INFO")
        )

    @classmethod
    def from_dict(cls, config_dict: dict) -> "ScannerConfig":
        """Create configuration from a dictionary."""
        return cls(**{k: v for k, v in config_dict.items() if k in cls.__annotations__})


# Global default configuration instance
_default_config: Optional[ScannerConfig] = None


def get_default_config() -> ScannerConfig:
    """Get the default configuration instance."""
    global _default_config
    if _default_config is None:
        _default_config = ScannerConfig.from_env()
    return _default_config


def set_default_config(config: ScannerConfig) -> None:
    """Set the default configuration instance."""
    global _default_config
    _default_config = config
