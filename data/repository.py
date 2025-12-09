import logging
import pandas as pd
from .provider import DataProvider, YahooDataProvider
from .cache import DataCache

class DataRepository:
    """
    Main entry point for the Data Layer.
    Orchestrates data fetching and caching.
    """
    
    def __init__(self, provider: DataProvider = None, cache: DataCache = None):
        self.provider = provider or YahooDataProvider()
        self.cache = cache or DataCache()
        self.logger = logging.getLogger(__name__)

    def get_ohlcv(self, symbol: str, force_refresh: bool = False) -> pd.DataFrame:
        """
        Get OHLCV data for a symbol.
        Checks cache first unless force_refresh is True.
        """
        if not force_refresh:
            cached_data = self.cache.get_ohlcv(symbol)
            if cached_data is not None:
                return cached_data
                
        # Fetch from provider
        try:
            df = self.provider.fetch_ohlcv(symbol)
            if not df.empty:
                self.cache.save_ohlcv(symbol, df)
            return df
        except Exception as e:
            self.logger.error(f"Failed to get OHLCV for {symbol}: {e}")
            raise

    def get_fundamentals(self, symbol: str, force_refresh: bool = False) -> dict:
        """
        Get fundamental data for a symbol.
        Checks cache first unless force_refresh is True.
        """
        if not force_refresh:
            cached_data = self.cache.get_fundamentals(symbol)
            if cached_data is not None:
                return cached_data
                
        # Fetch from provider
        try:
            data = self.provider.fetch_fundamentals(symbol)
            if data:
                self.cache.save_fundamentals(symbol, data)
            return data
        except Exception as e:
            self.logger.error(f"Failed to get fundamentals for {symbol}: {e}")
            return {}
