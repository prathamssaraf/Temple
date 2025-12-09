"""
Technical indicators for pattern detection.

This module provides calculations for common technical indicators used in
pattern analysis.
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple
import logging


logger = logging.getLogger(__name__)


class Indicators:
    """Calculator for technical indicators on OHLCV data."""

    @staticmethod
    def sma(data: pd.Series, period: int) -> pd.Series:
        """
        Simple Moving Average.

        Args:
            data: Price series (usually close prices)
            period: Number of periods for the average

        Returns:
            Series with SMA values
        """
        return data.rolling(window=period, min_periods=period).mean()

    @staticmethod
    def ema(data: pd.Series, period: int) -> pd.Series:
        """
        Exponential Moving Average.

        Args:
            data: Price series
            period: Number of periods

        Returns:
            Series with EMA values
        """
        return data.ewm(span=period, adjust=False, min_periods=period).mean()

    @staticmethod
    def bollinger_bands(data: pd.Series, period: int = 20, std_dev: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Bollinger Bands.

        Args:
            data: Price series
            period: Period for moving average
            std_dev: Number of standard deviations

        Returns:
            Tuple of (upper_band, middle_band, lower_band)
        """
        middle = Indicators.sma(data, period)
        std = data.rolling(window=period, min_periods=period).std()
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)
        return upper, middle, lower

    @staticmethod
    def rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """
        Relative Strength Index.

        Args:
            data: Price series
            period: RSI period (default 14)

        Returns:
            Series with RSI values (0-100)
        """
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period, min_periods=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period, min_periods=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    @staticmethod
    def macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Moving Average Convergence Divergence.

        Args:
            data: Price series
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period

        Returns:
            Tuple of (macd_line, signal_line, histogram)
        """
        ema_fast = Indicators.ema(data, fast)
        ema_slow = Indicators.ema(data, slow)
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    @staticmethod
    def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Average True Range.

        Args:
            high: High prices
            low: Low prices
            close: Close prices
            period: ATR period

        Returns:
            Series with ATR values
        """
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())

        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=period, min_periods=period).mean()
        return atr

    @staticmethod
    def vwap(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series) -> pd.Series:
        """
        Volume Weighted Average Price.

        Args:
            high: High prices
            low: Low prices
            close: Close prices
            volume: Volume

        Returns:
            Series with VWAP values
        """
        typical_price = (high + low + close) / 3
        return (typical_price * volume).cumsum() / volume.cumsum()

    @staticmethod
    def stochastic(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> Tuple[pd.Series, pd.Series]:
        """
        Stochastic Oscillator.

        Args:
            high: High prices
            low: Low prices
            close: Close prices
            period: Lookback period

        Returns:
            Tuple of (%K, %D)
        """
        lowest_low = low.rolling(window=period, min_periods=period).min()
        highest_high = high.rolling(window=period, min_periods=period).max()

        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=3).mean()

        return k_percent, d_percent

    @staticmethod
    def support_resistance(close: pd.Series, lookback: int = 90, tolerance: float = 0.02) -> Tuple[Optional[float], Optional[float]]:
        """
        Find support and resistance levels using local minima/maxima.

        Args:
            close: Close price series
            lookback: Number of days to look back
            tolerance: Percentage tolerance for clustering levels

        Returns:
            Tuple of (support_level, resistance_level)
        """
        recent_data = close.tail(lookback)

        if len(recent_data) < 10:
            return None, None

        # Find local minima (support candidates)
        local_mins = []
        for i in range(1, len(recent_data) - 1):
            if recent_data.iloc[i] < recent_data.iloc[i-1] and recent_data.iloc[i] < recent_data.iloc[i+1]:
                local_mins.append(recent_data.iloc[i])

        # Find local maxima (resistance candidates)
        local_maxs = []
        for i in range(1, len(recent_data) - 1):
            if recent_data.iloc[i] > recent_data.iloc[i-1] and recent_data.iloc[i] > recent_data.iloc[i+1]:
                local_maxs.append(recent_data.iloc[i])

        # Cluster nearby levels
        support = np.mean(local_mins) if local_mins else None
        resistance = np.mean(local_maxs) if local_maxs else None

        return support, resistance

    @staticmethod
    def percent_change(data: pd.Series, periods: int = 1) -> pd.Series:
        """
        Calculate percentage change over specified periods.

        Args:
            data: Price series
            periods: Number of periods to look back

        Returns:
            Series with percentage changes
        """
        return data.pct_change(periods=periods) * 100

    @staticmethod
    def volume_ratio(volume: pd.Series, period: int = 20) -> pd.Series:
        """
        Volume relative to moving average.

        Args:
            volume: Volume series
            period: Period for average volume

        Returns:
            Series with volume ratios
        """
        avg_volume = volume.rolling(window=period, min_periods=period).mean()
        return volume / avg_volume


def calculate_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate all common indicators and add them to the dataframe.

    Args:
        df: DataFrame with OHLCV data (columns: open, high, low, close, volume)

    Returns:
        DataFrame with additional indicator columns
    """
    result = df.copy()

    try:
        # Moving averages
        result['sma_20'] = Indicators.sma(df['close'], 20)
        result['sma_50'] = Indicators.sma(df['close'], 50)
        result['sma_200'] = Indicators.sma(df['close'], 200)
        result['ema_12'] = Indicators.ema(df['close'], 12)
        result['ema_26'] = Indicators.ema(df['close'], 26)

        # Bollinger Bands
        upper, middle, lower = Indicators.bollinger_bands(df['close'])
        result['bb_upper'] = upper
        result['bb_middle'] = middle
        result['bb_lower'] = lower

        # RSI
        result['rsi'] = Indicators.rsi(df['close'])

        # MACD
        macd_line, signal_line, histogram = Indicators.macd(df['close'])
        result['macd'] = macd_line
        result['macd_signal'] = signal_line
        result['macd_hist'] = histogram

        # ATR
        result['atr'] = Indicators.atr(df['high'], df['low'], df['close'])

        # Stochastic
        k, d = Indicators.stochastic(df['high'], df['low'], df['close'])
        result['stoch_k'] = k
        result['stoch_d'] = d

        # Volume indicators
        result['volume_ratio'] = Indicators.volume_ratio(df['volume'])

        # Price changes
        result['pct_change_1d'] = Indicators.percent_change(df['close'], 1)
        result['pct_change_5d'] = Indicators.percent_change(df['close'], 5)

        logger.info(f"Calculated {len(result.columns) - len(df.columns)} indicators")

    except Exception as e:
        logger.error(f"Error calculating indicators: {e}")

    return result
