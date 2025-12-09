"""Factory for creating scanner components."""

from typing import Optional, Callable, Any
import pandas as pd
import logging

from .config import ScannerConfig, get_default_config
from .scanner import PatternScanner


class ScannerFactory:
    """Factory for creating configured scanner instances."""

    @staticmethod
    def create_scanner(
        data_fetcher: Callable[[str], pd.DataFrame],
        pattern_matcher: Any,
        config: Optional[ScannerConfig] = None
    ) -> PatternScanner:
        """
        Create a PatternScanner instance.

        Args:
            data_fetcher: Function to fetch OHLCV data for a symbol
            pattern_matcher: PatternMatcher instance from patterns module
            config: Configuration object (uses default if not provided)

        Returns:
            PatternScanner instance
        """
        if config is None:
            config = get_default_config()

        return PatternScanner(
            data_fetcher=data_fetcher,
            pattern_matcher=pattern_matcher,
            parallel=config.parallel,
            max_workers=config.max_workers
        )


def create_scanner(
    data_fetcher: Callable[[str], pd.DataFrame],
    pattern_matcher: Any,
    config: Optional[ScannerConfig] = None
) -> PatternScanner:
    """
    Convenience function to create a PatternScanner with default configuration.

    This is the recommended way to instantiate the scanner layer for most use cases.

    Args:
        data_fetcher: Function that takes a symbol and returns OHLCV DataFrame
        pattern_matcher: PatternMatcher instance from patterns module
        config: Optional configuration (uses environment-based defaults if not provided)

    Returns:
        Fully configured PatternScanner instance

    Example:
        ```python
        from data.repository import DataRepository
        from patterns import create_pattern_matcher
        from scanner import create_scanner

        # Setup dependencies
        data_repo = DataRepository()
        matcher = create_pattern_matcher()

        # Create scanner
        scanner = create_scanner(
            data_fetcher=data_repo.get_ohlcv,
            pattern_matcher=matcher
        )

        # Scan stocks
        results = scanner.scan(
            symbols=["AAPL", "MSFT", "GOOGL"],
            pattern=my_pattern,
            min_confidence=0.7
        )
        ```
    """
    return ScannerFactory.create_scanner(data_fetcher, pattern_matcher, config)
