"""
Pattern matching service that integrates data fetching and pattern detection.
"""
import sys
import os
from typing import Optional
import logging

# Add parent directory to path to import patterns module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from patterns import (
    create_pattern_matcher,
    PatternDefinition,
    SequenceStep,
    EventDefinition,
    ReferenceLevel,
    FrequencyConstraint,
    EventType,
    TimeframeUnit,
    PatternMatch
)
from .data_fetcher import DataFetcher

logger = logging.getLogger(__name__)


class PatternService:
    """Service for pattern matching against stock data."""

    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.pattern_matcher = create_pattern_matcher()
        self.logger = logging.getLogger(__name__)

    def convert_api_pattern_to_engine_pattern(self, api_pattern: dict) -> PatternDefinition:
        """
        Convert API pattern format to pattern engine format.

        Args:
            api_pattern: Pattern from API request

        Returns:
            PatternDefinition for engine
        """
        # Convert sequence steps
        sequence = []
        for step in api_pattern['sequence']:
            event_def = step['event']
            event_type = event_def['event_type']

            # Parse reference level if present
            reference = None
            if 'reference' in event_def['parameters']:
                ref_str = event_def['parameters']['reference']
                if ref_str.startswith('SMA'):
                    period = int(ref_str[3:])
                    reference = ReferenceLevel(type="sma", period=period)
                elif ref_str.startswith('EMA'):
                    period = int(ref_str[3:])
                    reference = ReferenceLevel(type="ema", period=period)
                elif ref_str == 'support':
                    lookback = event_def['parameters'].get('lookback', 90)
                    tolerance = event_def['parameters'].get('tolerance', 1.5)
                    reference = ReferenceLevel(
                        type="support",
                        lookback=lookback,
                        tolerance=tolerance
                    )
                elif ref_str == 'resistance':
                    lookback = event_def['parameters'].get('lookback', 90)
                    tolerance = event_def['parameters'].get('tolerance', 1.5)
                    reference = ReferenceLevel(
                        type="resistance",
                        lookback=lookback,
                        tolerance=tolerance
                    )
                elif ref_str == 'pivot_mode':
                    lookback = event_def['parameters'].get('lookback', 365)
                    tolerance = event_def['parameters'].get('tolerance', 5.0)
                    reference = ReferenceLevel(
                        type="pivot_mode",
                        lookback=lookback,
                        tolerance=tolerance
                    )
                elif ref_str == 'pivot_median':
                    lookback = event_def['parameters'].get('lookback', 365)
                    tolerance = event_def['parameters'].get('tolerance', 5.0)
                    reference = ReferenceLevel(
                        type="pivot_median",
                        lookback=lookback,
                        tolerance=tolerance
                    )
                elif ref_str == 'pivot_volume':
                    lookback = event_def['parameters'].get('lookback', 365)
                    tolerance = event_def['parameters'].get('tolerance', 5.0)
                    reference = ReferenceLevel(
                        type="pivot_volume",
                        lookback=lookback,
                        tolerance=tolerance
                    )
                elif ref_str == 'fixed':
                    # User-specified fixed price pivot
                    value = event_def['parameters'].get('value')
                    tolerance = event_def['parameters'].get('tolerance', 5.0)
                    reference = ReferenceLevel(
                        type="fixed",
                        value=value,
                        tolerance=tolerance
                    )

            # Create event definition
            event = EventDefinition(
                type=EventType(event_type.lower()),
                reference=reference,
                min_change=event_def['parameters'].get('min_change'),
                max_change=event_def['parameters'].get('max_change'),
                tolerance=event_def['parameters'].get('tolerance', 1.0)
            )

            # Create sequence step
            seq_step = SequenceStep(
                event=event,
                min_duration_days=step.get('min_interval_days'),
                max_duration_days=step.get('max_interval_days')
            )
            sequence.append(seq_step)

        # Convert frequency constraint
        frequency = FrequencyConstraint(
            min_occurrences=api_pattern['frequency']['min_occurrences'],
            timeframe=api_pattern['frequency']['timeframe_days'],
            timeframe_unit=TimeframeUnit.DAYS
        )

        # Create pattern definition
        return PatternDefinition(
            name=api_pattern['name'],
            description=api_pattern['description'],
            sequence=sequence,
            frequency=frequency
        )

    def match_pattern(
        self,
        symbol: str,
        pattern_dict: dict,
        lookback_days: int = 365
    ) -> Optional[PatternMatch]:
        """
        Match a pattern against a stock symbol.

        Args:
            symbol: Stock ticker symbol
            pattern_dict: Pattern definition (API format)
            lookback_days: How many days of data to analyze

        Returns:
            PatternMatch result or None if data fetch failed
        """
        self.logger.info(f"Starting pattern match for {symbol}")

        # Step 1: Fetch data
        period = f"{lookback_days}d"
        df = self.data_fetcher.get_stock_data(symbol, period=period)

        if df is None or df.empty:
            self.logger.error(f"No data available for {symbol}")
            return None

        # Step 2: Convert pattern to engine format
        try:
            pattern = self.convert_api_pattern_to_engine_pattern(pattern_dict)
        except Exception as e:
            self.logger.error(f"Failed to convert pattern: {e}")
            raise

        # Step 3: Run pattern matching
        try:
            match_result = self.pattern_matcher.match(df, symbol, pattern)
            self.logger.info(
                f"Pattern match complete for {symbol}: "
                f"{match_result.count} occurrences, "
                f"{match_result.confidence:.2f} confidence"
            )
            return match_result
        except Exception as e:
            self.logger.error(f"Pattern matching failed for {symbol}: {e}")
            raise


def create_pattern_service() -> PatternService:
    """Create a PatternService instance."""
    return PatternService()
