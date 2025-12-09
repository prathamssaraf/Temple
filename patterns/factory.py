"""Factory for creating pattern detection components."""

from typing import Optional
import logging

from .config import PatternsConfig, get_default_config
from .matcher import PatternMatcher


class PatternsFactory:
    """Factory for creating configured pattern detection instances."""

    @staticmethod
    def create_matcher(config: Optional[PatternsConfig] = None) -> PatternMatcher:
        """
        Create a PatternMatcher instance.

        Args:
            config: Configuration object (uses default if not provided)

        Returns:
            PatternMatcher instance
        """
        if config is None:
            config = get_default_config()

        return PatternMatcher(
            calculate_indicators=config.calculate_indicators
        )


def create_pattern_matcher(config: Optional[PatternsConfig] = None) -> PatternMatcher:
    """
    Convenience function to create a PatternMatcher with default configuration.

    This is the recommended way to instantiate the patterns layer for most use cases.

    Args:
        config: Optional configuration (uses environment-based defaults if not provided)

    Returns:
        Fully configured PatternMatcher instance

    Example:
        ```python
        from patterns import create_pattern_matcher
        from data import create_data_repository

        # Get data
        repo = create_data_repository()
        df = repo.get_ohlcv("AAPL")

        # Create pattern matcher
        matcher = create_pattern_matcher()

        # Define and match pattern
        pattern = PatternDefinition(...)
        match = matcher.match(df, "AAPL", pattern)
        ```
    """
    return PatternsFactory.create_matcher(config=config)
