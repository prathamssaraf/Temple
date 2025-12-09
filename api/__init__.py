"""Temple REST API."""

from .main import app, create_app
from .config import APIConfig, get_config, set_config

__all__ = ["app", "create_app", "APIConfig", "get_config", "set_config"]
__version__ = "0.1.0"
