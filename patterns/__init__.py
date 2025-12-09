"""
Temple Patterns Layer - Temporal pattern detection engine.

This module provides a flexible system for detecting recurring temporal patterns
in stock price data. Users can define custom patterns or use pre-built templates.

Quick Start
-----------
The simplest way to use the patterns layer:

    from data import create_data_repository
    from patterns import create_pattern_matcher, PatternDefinition, EventDefinition, EventType

    # Get data
    repo = create_data_repository()
    df = repo.get_ohlcv("AAPL")

    # Create matcher
    matcher = create_pattern_matcher()

    # Define a pattern
    pattern = PatternDefinition(
        name="Support Bounce",
        description="Price bounces off support multiple times",
        sequence=[...],  # Define sequence steps
        frequency=FrequencyConstraint(min_occurrences=5, timeframe=180)
    )

    # Match pattern
    match = matcher.match(df, "AAPL", pattern)
    print(f"Found {match.count} occurrences with {match.confidence:.2f} confidence")

Pattern Definition
------------------
Patterns are defined using a declarative schema:

    from patterns import (
        PatternDefinition, SequenceStep, EventDefinition,
        ReferenceLevel, FrequencyConstraint, EventType, TimeframeUnit
    )

    pattern = PatternDefinition(
        name="Mean Reversion",
        description="Price falls below SMA20, then recovers",
        sequence=[
            SequenceStep(
                event=EventDefinition(
                    type=EventType.PRICE_CROSSES_BELOW,
                    reference=ReferenceLevel(type="sma", period=20)
                ),
                name="Fall below average"
            ),
            SequenceStep(
                event=EventDefinition(
                    type=EventType.PRICE_RISES_BY,
                    min_change=5.0
                ),
                max_duration_days=10,
                name="Recovery"
            )
        ],
        frequency=FrequencyConstraint(
            min_occurrences=8,
            timeframe=1,
            timeframe_unit=TimeframeUnit.YEARS
        )
    )

"""

# Public API - Configuration
from .config import (
    PatternsConfig,
    get_default_config,
    set_default_config
)

# Public API - Schema (Pattern Definition)
from .schema import (
    PatternDefinition,
    SequenceStep,
    EventDefinition,
    ReferenceLevel,
    FrequencyConstraint,
    PatternMatch,
    EventType,
    Operator,
    TimeframeUnit
)

# Public API - Core Components
from .matcher import PatternMatcher
from .indicators import Indicators, calculate_all_indicators
from .events import EventDetector
from .sequences import SequenceMatcher, match_multiple_patterns

# Public API - Mock Data (for testing without data layer)
from .mock_data import (
    create_mock_ohlcv,
    create_mean_reverting_data,
    create_volatile_data,
    create_trending_data,
    create_support_resistance_data
)

# Public API - Factory (recommended entry point)
from .factory import (
    PatternsFactory,
    create_pattern_matcher
)

# Define public interface
__all__ = [
    # Configuration
    "PatternsConfig",
    "get_default_config",
    "set_default_config",
    # Schema
    "PatternDefinition",
    "SequenceStep",
    "EventDefinition",
    "ReferenceLevel",
    "FrequencyConstraint",
    "PatternMatch",
    "EventType",
    "Operator",
    "TimeframeUnit",
    # Core components
    "PatternMatcher",
    "Indicators",
    "calculate_all_indicators",
    "EventDetector",
    "SequenceMatcher",
    "match_multiple_patterns",
    # Mock data
    "create_mock_ohlcv",
    "create_mean_reverting_data",
    "create_volatile_data",
    "create_trending_data",
    "create_support_resistance_data",
    # Factory (recommended)
    "PatternsFactory",
    "create_pattern_matcher",
]

# Version
__version__ = "0.1.0"
