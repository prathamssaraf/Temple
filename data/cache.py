import os
import json
import pandas as pd
from datetime import datetime, timedelta
import logging
from pathlib import Path
from typing import Optional

class DataCache:
    """Local file-based cache for stock data."""
    
    def __init__(self, cache_dir: str = "./cache", ohlcv_ttl_hours: int = 24, fundamentals_ttl_days: int = 7):
        """
        Initialize the cache.
        
        Args:
            cache_dir: Directory to store cache files
            ohlcv_ttl_hours: Time-to-live for OHLCV data in hours
            fundamentals_ttl_days: Time-to-live for fundamental data in days
        """
        self.cache_dir = Path(cache_dir)
        self.ohlcv_dir = self.cache_dir / "ohlcv"
        self.fundamentals_dir = self.cache_dir / "fundamentals"
        self.ohlcv_ttl = timedelta(hours=ohlcv_ttl_hours)
        self.fundamentals_ttl = timedelta(days=fundamentals_ttl_days)
        self.logger = logging.getLogger(__name__)
        
        # Ensure directories exist
        self.ohlcv_dir.mkdir(parents=True, exist_ok=True)
        self.fundamentals_dir.mkdir(parents=True, exist_ok=True)

    def _is_fresh(self, filepath: Path, ttl: timedelta) -> bool:
        """Check if a file is fresh (younger than ttl)."""
        if not filepath.exists():
            return False
        
        file_mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
        age = datetime.now() - file_mtime
        return age < ttl

    def get_ohlcv(self, symbol: str) -> Optional[pd.DataFrame]:
        """Retrieve OHLCV data from cache if valid."""
        filepath = self.ohlcv_dir / f"{symbol}.csv"
        
        if self._is_fresh(filepath, self.ohlcv_ttl):
            try:
                self.logger.info(f"Cache hit: {symbol} OHLCV")
                df = pd.read_csv(filepath, index_col=0, parse_dates=True)
                return df
            except Exception as e:
                self.logger.error(f"Error reading OHLCV cache for {symbol}: {e}")
                return None
        
        return None

    def save_ohlcv(self, symbol: str, df: pd.DataFrame):
        """Save OHLCV data to cache."""
        if df is None or df.empty:
            return
            
        filepath = self.ohlcv_dir / f"{symbol}.csv"
        try:
            df.to_csv(filepath)
            self.logger.info(f"Cached OHLCV for {symbol}")
        except Exception as e:
            self.logger.error(f"Error saving OHLCV cache for {symbol}: {e}")

    def get_fundamentals(self, symbol: str) -> Optional[dict]:
        """Retrieve fundamental data from cache if valid."""
        filepath = self.fundamentals_dir / f"{symbol}.json"
        
        if self._is_fresh(filepath, self.fundamentals_ttl):
            try:
                self.logger.info(f"Cache hit: {symbol} fundamentals")
                with open(filepath, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error reading fundamental cache for {symbol}: {e}")
                return None
        
        return None

    def save_fundamentals(self, symbol: str, data: dict):
        """Save fundamental data to cache."""
        if not data:
            return
            
        filepath = self.fundamentals_dir / f"{symbol}.json"
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            self.logger.info(f"Cached fundamentals for {symbol}")
        except Exception as e:
            self.logger.error(f"Error saving fundamental cache for {symbol}: {e}")
