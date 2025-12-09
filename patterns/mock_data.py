"""
Mock data generator for testing patterns without external dependencies.

This module generates synthetic OHLCV data with configurable patterns
for testing the pattern detection engine.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional


def create_mock_ohlcv(
    days: int = 500,
    base_price: float = 100.0,
    volatility: float = 0.02,
    trend: float = 0.0005,
    seed: Optional[int] = None
) -> pd.DataFrame:
    """
    Generate realistic mock OHLCV data.

    Args:
        days: Number of days of data to generate
        base_price: Starting price
        volatility: Daily volatility (0.02 = 2%)
        trend: Daily trend (0.0005 = 0.05% daily growth)
        seed: Random seed for reproducibility

    Returns:
        DataFrame with OHLCV data and DatetimeIndex

    Example:
        ```python
        df = create_mock_ohlcv(days=365, base_price=150.0)
        matcher = create_pattern_matcher()
        match = matcher.match(df, "MOCK", pattern)
        ```
    """
    if seed is not None:
        np.random.seed(seed)

    # Create date range
    end_date = datetime.now()
    dates = pd.date_range(end=end_date, periods=days, freq='D')

    # Generate price with trend and volatility
    returns = np.random.randn(days) * volatility + trend
    price_multipliers = np.exp(returns)
    close_prices = base_price * np.cumprod(price_multipliers)

    # Generate OHLC from close prices
    daily_range = np.abs(np.random.randn(days)) * volatility * close_prices

    high = close_prices + daily_range * np.random.rand(days)
    low = close_prices - daily_range * np.random.rand(days)
    open_price = low + (high - low) * np.random.rand(days)

    # Ensure OHLC relationships are valid
    high = np.maximum(high, np.maximum(open_price, close_prices))
    low = np.minimum(low, np.minimum(open_price, close_prices))

    # Generate volume with some correlation to price movement
    base_volume = 50_000_000
    volume_volatility = 0.3
    volume = base_volume * (1 + np.random.randn(days) * volume_volatility)
    volume = np.abs(volume).astype(int)

    # Create DataFrame
    df = pd.DataFrame({
        'open': open_price,
        'high': high,
        'low': low,
        'close': close_prices,
        'volume': volume
    }, index=dates)

    return df


def create_mean_reverting_data(
    days: int = 500,
    base_price: float = 100.0,
    mean_reversion_speed: float = 0.1,
    seed: Optional[int] = None
) -> pd.DataFrame:
    """
    Generate mock data with strong mean-reversion characteristics.

    Perfect for testing mean-reversion patterns.

    Args:
        days: Number of days
        base_price: Average price level
        mean_reversion_speed: Speed of reversion to mean (0.1 = 10% per day)
        seed: Random seed

    Returns:
        DataFrame with mean-reverting OHLCV data
    """
    if seed is not None:
        np.random.seed(seed)

    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')

    # Generate mean-reverting price process
    prices = np.zeros(days)
    prices[0] = base_price

    for i in range(1, days):
        # Mean reversion: price pulls back toward base_price
        deviation = prices[i-1] - base_price
        reversion = -deviation * mean_reversion_speed
        random_shock = np.random.randn() * 2
        prices[i] = prices[i-1] + reversion + random_shock
        prices[i] = max(prices[i], base_price * 0.5)  # Floor at 50% of base

    close_prices = prices

    # Generate OHLC
    daily_range = np.abs(np.random.randn(days)) * 2
    high = close_prices + daily_range * np.random.rand(days)
    low = close_prices - daily_range * np.random.rand(days)
    open_price = low + (high - low) * np.random.rand(days)

    high = np.maximum(high, np.maximum(open_price, close_prices))
    low = np.minimum(low, np.minimum(open_price, close_prices))

    volume = np.random.randint(30_000_000, 80_000_000, days)

    df = pd.DataFrame({
        'open': open_price,
        'high': high,
        'low': low,
        'close': close_prices,
        'volume': volume
    }, index=dates)

    return df


def create_volatile_data(
    days: int = 500,
    base_price: float = 100.0,
    volatility: float = 0.05,
    seed: Optional[int] = None
) -> pd.DataFrame:
    """
    Generate highly volatile mock data with large swings.

    Perfect for testing volatility patterns.

    Args:
        days: Number of days
        base_price: Starting price
        volatility: High volatility (0.05 = 5% daily)
        seed: Random seed

    Returns:
        DataFrame with volatile OHLCV data
    """
    return create_mock_ohlcv(
        days=days,
        base_price=base_price,
        volatility=volatility,
        trend=0,
        seed=seed
    )


def create_trending_data(
    days: int = 500,
    base_price: float = 100.0,
    trend: float = 0.002,
    volatility: float = 0.015,
    seed: Optional[int] = None
) -> pd.DataFrame:
    """
    Generate trending mock data (uptrend or downtrend).

    Args:
        days: Number of days
        base_price: Starting price
        trend: Daily trend (0.002 = 0.2% per day = ~50% per year)
        volatility: Daily volatility
        seed: Random seed

    Returns:
        DataFrame with trending OHLCV data
    """
    return create_mock_ohlcv(
        days=days,
        base_price=base_price,
        volatility=volatility,
        trend=trend,
        seed=seed
    )


def create_support_resistance_data(
    days: int = 500,
    support_level: float = 95.0,
    resistance_level: float = 105.0,
    seed: Optional[int] = None
) -> pd.DataFrame:
    """
    Generate data that bounces between support and resistance levels.

    Perfect for testing support/resistance patterns.

    Args:
        days: Number of days
        support_level: Price floor
        resistance_level: Price ceiling
        seed: Random seed

    Returns:
        DataFrame with range-bound OHLCV data
    """
    if seed is not None:
        np.random.seed(seed)

    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    mid_point = (support_level + resistance_level) / 2

    prices = np.zeros(days)
    prices[0] = mid_point

    for i in range(1, days):
        # Bounce off support/resistance
        if prices[i-1] <= support_level:
            # Bounce up from support
            prices[i] = prices[i-1] + np.random.rand() * 3 + 1
        elif prices[i-1] >= resistance_level:
            # Bounce down from resistance
            prices[i] = prices[i-1] - np.random.rand() * 3 - 1
        else:
            # Random walk in the middle
            prices[i] = prices[i-1] + np.random.randn() * 1.5

        # Keep within bounds
        prices[i] = np.clip(prices[i], support_level - 2, resistance_level + 2)

    close_prices = prices

    # Generate OHLC
    daily_range = np.abs(np.random.randn(days)) * 1.5
    high = close_prices + daily_range * np.random.rand(days)
    low = close_prices - daily_range * np.random.rand(days)
    open_price = low + (high - low) * np.random.rand(days)

    high = np.maximum(high, np.maximum(open_price, close_prices))
    low = np.minimum(low, np.minimum(open_price, close_prices))

    volume = np.random.randint(40_000_000, 70_000_000, days)

    df = pd.DataFrame({
        'open': open_price,
        'high': high,
        'low': low,
        'close': close_prices,
        'volume': volume
    }, index=dates)

    return df
