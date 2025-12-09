from abc import ABC, abstractmethod
from typing import Optional

import yfinance as yf
import pandas as pd

from datetime import date, datetime
import logging

class DataProvider(ABC):
    """Abstract base class for data providers."""

    @abstractmethod
    def fetch_ohlcv(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None, period: str = "2y") -> pd.DataFrame:
        """
        Fetch OHLCV data for a symbol.
        
        Args:
            symbol: Ticker symbol (e.g., "AAPL")
            start_date: Start date in "YYYY-MM-DD" format (optional)
            end_date: End date in "YYYY-MM-DD" format (optional)
            period: Period to fetch if dates not provided (default "2y")
            
        Returns:
            pd.DataFrame: OHLCV data with DatetimeIndex
        """
        pass

    @abstractmethod
    def fetch_fundamentals(self, symbol: str) -> dict:
        """
        Fetch fundamental data for a symbol.
        
        Args:
            symbol: Ticker symbol
            
        Returns:
            dict: Dictionary of fundamental data
        """
        pass


class YahooDataProvider(DataProvider):
    """Data provider using Yahoo Finance (yfinance)."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def fetch_ohlcv(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None, period: str = "2y") -> pd.DataFrame:
        """Fetch OHLCV data using yfinance."""
        self.logger.info(f"Fetching OHLCV for {symbol} (Period: {period}, Start: {start_date}, End: {end_date})")
        
        try:
            ticker = yf.Ticker(symbol)
            
            # yfinance history parameters
            history_params = {"auto_adjust": True}
            
            if start_date and end_date:
                history_params["start"] = start_date
                history_params["end"] = end_date
            else:
                history_params["period"] = period
                
            df = ticker.history(**history_params)
            
            if df.empty:
                self.logger.warning(f"No data found for {symbol}")
                return pd.DataFrame()
                
            # Ensure standard columns (lower case)
            df = df.rename(columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume"
            })
            
            # Keep only OHLCV columns + index
            required_cols = ["open", "high", "low", "close", "volume"]
            # Filter columns that actually exist
            available_cols = [c for c in required_cols if c in df.columns]
            df = df[available_cols]
            
            if df.empty:
                 self.logger.warning(f"Data found but missing required columns for {symbol}")
                 return pd.DataFrame()

            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching OHLCV for {symbol}: {e}")
            return pd.DataFrame()

    def fetch_fundamentals(self, symbol: str) -> dict:
        """Fetch fundamentals using yfinance."""
        self.logger.info(f"Fetching fundamentals for {symbol}")
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Extract key fundamental metrics safely
            fundamentals = {
                "symbol": symbol,
                "name": info.get("longName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "dividend_yield": info.get("dividendYield"),
                "beta": info.get("beta"),
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
                "average_volume": info.get("averageVolume"),
                "currency": info.get("currency")
            }
            return fundamentals
            
        except Exception as e:
            self.logger.error(f"Error fetching fundamentals for {symbol}: {e}")
            return {}
