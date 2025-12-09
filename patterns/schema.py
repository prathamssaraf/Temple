"""
Pattern definition schema for Temple.

This module defines the structure for user-defined patterns that can detect
temporal sequences and recurring behaviors in stock price data.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Literal
from enum import Enum


class EventType(Enum):
    """Types of detectable events in price data."""
    PRICE_CROSSES_ABOVE = "price_crosses_above"
    PRICE_CROSSES_BELOW = "price_crosses_below"
    PRICE_TOUCHES = "price_touches"
    PRICE_RISES_BY = "price_rises_by"
    PRICE_FALLS_BY = "price_falls_by"
    INDICATOR_CROSSES_ABOVE = "indicator_crosses_above"
    INDICATOR_CROSSES_BELOW = "indicator_crosses_below"
    INDICATOR_EQUALS = "indicator_equals"
    VOLUME_SPIKE = "volume_spike"


class Operator(Enum):
    """Comparison operators for conditions."""
    GREATER_THAN = ">"
    LESS_THAN = "<"
    EQUALS = "=="
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    NOT_EQUALS = "!="


class TimeframeUnit(Enum):
    """Time units for pattern frequency analysis."""
    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"
    YEARS = "years"


@dataclass
class ReferenceLevel:
    """
    Defines a reference level (price point) in the data.

    Examples:
        - Fixed price: ReferenceLevel(type="fixed", value=150.0)
        - Moving average: ReferenceLevel(type="sma", period=20)
        - Support/resistance: ReferenceLevel(type="support", lookback=90)
    """
    type: str  # "fixed", "sma", "ema", "support", "resistance", "vwap"
    value: Optional[float] = None
    period: Optional[int] = None
    lookback: Optional[int] = None
    tolerance: float = 0.5  # Percentage tolerance for "touches"


@dataclass
class EventDefinition:
    """
    Defines a single event to detect in price data.

    Examples:
        - Price falls to support: EventDefinition(
            type=EventType.PRICE_CROSSES_BELOW,
            reference=ReferenceLevel(type="support", lookback=90),
            tolerance=1.0
          )
        - RSI oversold: EventDefinition(
            type=EventType.INDICATOR_CROSSES_BELOW,
            indicator="rsi",
            reference=ReferenceLevel(type="fixed", value=30)
          )
    """
    type: EventType
    reference: Optional[ReferenceLevel] = None
    indicator: Optional[str] = None  # For indicator-based events
    min_change: Optional[float] = None  # Minimum % change for rise/fall events
    max_change: Optional[float] = None  # Maximum % change
    tolerance: float = 0.5  # Default tolerance


@dataclass
class SequenceStep:
    """
    A single step in a pattern sequence.

    Example:
        SequenceStep(
            event=EventDefinition(...),
            min_duration_days=1,
            max_duration_days=30
        )
    """
    event: EventDefinition
    min_duration_days: Optional[int] = None  # Min days between this and next event
    max_duration_days: Optional[int] = None  # Max days between this and next event
    name: Optional[str] = None  # Human-readable name for this step


@dataclass
class FrequencyConstraint:
    """
    Defines how often a pattern should occur to be valid.

    Example:
        FrequencyConstraint(
            min_occurrences=5,
            max_occurrences=20,
            timeframe=90,
            timeframe_unit=TimeframeUnit.DAYS
        )
    """
    min_occurrences: int = 1
    max_occurrences: Optional[int] = None
    timeframe: int = 365  # Size of the time window
    timeframe_unit: TimeframeUnit = TimeframeUnit.DAYS


@dataclass
class PatternDefinition:
    """
    Complete pattern definition for temporal pattern detection.

    Example - Support Bounce Pattern:
        PatternDefinition(
            name="Support Bounce",
            description="Price touches support and bounces back multiple times",
            sequence=[
                SequenceStep(
                    event=EventDefinition(
                        type=EventType.PRICE_TOUCHES,
                        reference=ReferenceLevel(type="support", lookback=90)
                    ),
                    name="Touch support"
                ),
                SequenceStep(
                    event=EventDefinition(
                        type=EventType.PRICE_RISES_BY,
                        min_change=3.0
                    ),
                    max_duration_days=10,
                    name="Bounce up"
                )
            ],
            frequency=FrequencyConstraint(
                min_occurrences=5,
                timeframe=180,
                timeframe_unit=TimeframeUnit.DAYS
            )
        )
    """
    name: str
    description: str
    sequence: List[SequenceStep]
    frequency: FrequencyConstraint
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PatternMatch:
    """
    Represents a detected pattern match in the data.
    """
    pattern_name: str
    symbol: str
    occurrences: List[Dict[str, Any]]  # List of matched sequences
    count: int
    timeframe_start: str
    timeframe_end: str
    confidence: float  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
