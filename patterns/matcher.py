"""
Main pattern matching orchestrator.

This module provides the high-level API for pattern detection.
"""

import pandas as pd
from typing import List, Optional, Dict, Any
import logging

from .schema import PatternDefinition, PatternMatch
from .indicators import calculate_all_indicators
from .sequences import SequenceMatcher, match_multiple_patterns


logger = logging.getLogger(__name__)


class PatternMatcher:
    """
    Main pattern matching engine.

    This class orchestrates the pattern detection process:
    1. Enriches data with technical indicators
    2. Detects events based on pattern definitions
    3. Matches sequences of events
    4. Analyzes frequency and temporal patterns
    """

    def __init__(self, calculate_indicators: bool = True):
        """
        Initialize pattern matcher.

        Args:
            calculate_indicators: Whether to automatically calculate indicators
        """
        self.calculate_indicators = calculate_indicators
        self.logger = logging.getLogger(__name__)

    def match(
        self,
        df: pd.DataFrame,
        symbol: str,
        pattern: PatternDefinition
    ) -> PatternMatch:
        """
        Match a single pattern against price data.

        Args:
            df: DataFrame with OHLCV data
            symbol: Stock symbol
            pattern: Pattern definition to match

        Returns:
            PatternMatch result
        """
        self.logger.info(f"Matching pattern '{pattern.name}' for {symbol}")

        # Enrich data with indicators if needed
        if self.calculate_indicators:
            df = calculate_all_indicators(df)

        # Create matcher and find pattern
        matcher = SequenceMatcher(df, symbol)
        match = matcher.match_pattern(pattern)

        return match

    def match_multiple(
        self,
        df: pd.DataFrame,
        symbol: str,
        patterns: List[PatternDefinition]
    ) -> List[PatternMatch]:
        """
        Match multiple patterns against the same data.

        Args:
            df: DataFrame with OHLCV data
            symbol: Stock symbol
            patterns: List of patterns to match

        Returns:
            List of PatternMatch results
        """
        self.logger.info(f"Matching {len(patterns)} patterns for {symbol}")

        # Enrich data with indicators once
        if self.calculate_indicators:
            df = calculate_all_indicators(df)

        # Match all patterns
        matches = match_multiple_patterns(df, symbol, patterns)

        return matches

    def find_best_matches(
        self,
        matches: List[PatternMatch],
        min_confidence: float = 0.5,
        top_n: Optional[int] = None
    ) -> List[PatternMatch]:
        """
        Filter and rank pattern matches by confidence.

        Args:
            matches: List of pattern matches
            min_confidence: Minimum confidence threshold
            top_n: Return only top N matches

        Returns:
            Filtered and sorted list of matches
        """
        # Filter by confidence
        filtered = [m for m in matches if m.confidence >= min_confidence]

        # Sort by confidence descending
        sorted_matches = sorted(filtered, key=lambda m: m.confidence, reverse=True)

        # Return top N if specified
        if top_n:
            return sorted_matches[:top_n]

        return sorted_matches

    def get_summary(self, match: PatternMatch) -> Dict[str, Any]:
        """
        Get a summary of a pattern match.

        Args:
            match: Pattern match result

        Returns:
            Dictionary with summary information
        """
        return {
            'pattern_name': match.pattern_name,
            'symbol': match.symbol,
            'occurrences': match.count,
            'confidence': round(match.confidence, 3),
            'timeframe': f"{match.timeframe_start} to {match.timeframe_end}",
            'passed': match.count >= match.metadata.get('frequency_constraint', {}).get('min_occurrences', 1),
            'description': match.metadata.get('description', '')
        }
