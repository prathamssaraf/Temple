"""
Data fetching service for stock market data.
"""
import yfinance as yf
import pandas as pd
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DataFetcher:
    """Fetches stock data from Yahoo Finance."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_stock_data(
        self,
        symbol: str,
        period: str = "1y",
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Fetch OHLCV data for a symbol.

        Args:
            symbol: Stock ticker symbol
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)

        Returns:
            DataFrame with OHLCV data or None if fetch fails
        """
        try:
            self.logger.info(f"Fetching {period} data for {symbol}")

            # Download data from yfinance
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)

            if df.empty:
                self.logger.warning(f"No data returned for {symbol}")
                return None

            # Standardize column names (yfinance uses capitalized names)
            df.columns = [col.lower() for col in df.columns]

            self.logger.info(f"Successfully fetched {len(df)} rows for {symbol}")
            return df

        except Exception as e:
            self.logger.error(f"Failed to fetch data for {symbol}: {e}")
            return None


def create_data_fetcher() -> DataFetcher:
    """Create a DataFetcher instance."""
    return DataFetcher()
