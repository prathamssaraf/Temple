"""Configuration for the Temple API."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class APIConfig:
    """Configuration for the Temple REST API."""

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    reload: bool = False

    # CORS settings
    allow_origins: list = None
    allow_credentials: bool = True
    allow_methods: list = None
    allow_headers: list = None

    # API settings
    api_prefix: str = "/api/v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_calls: int = 100
    rate_limit_period: int = 60  # seconds

    def __post_init__(self):
        """Set default values for lists."""
        if self.allow_origins is None:
            self.allow_origins = ["http://localhost:3000", "http://localhost:5173"]
        if self.allow_methods is None:
            self.allow_methods = ["*"]
        if self.allow_headers is None:
            self.allow_headers = ["*"]

    @classmethod
    def from_env(cls) -> "APIConfig":
        """Create configuration from environment variables."""
        return cls(
            host=os.getenv("API_HOST", "0.0.0.0"),
            port=int(os.getenv("API_PORT", "8000")),
            debug=os.getenv("API_DEBUG", "false").lower() == "true",
            reload=os.getenv("API_RELOAD", "false").lower() == "true",
            allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(","),
            rate_limit_enabled=os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true",
            rate_limit_calls=int(os.getenv("RATE_LIMIT_CALLS", "100")),
            rate_limit_period=int(os.getenv("RATE_LIMIT_PERIOD", "60"))
        )


# Global configuration instance
_config: Optional[APIConfig] = None


def get_config() -> APIConfig:
    """Get the API configuration instance."""
    global _config
    if _config is None:
        _config = APIConfig.from_env()
    return _config


def set_config(config: APIConfig) -> None:
    """Set the API configuration instance."""
    global _config
    _config = config
