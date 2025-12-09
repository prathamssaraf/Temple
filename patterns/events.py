"""
Event detection system for pattern matching.

This module detects specific events in price data such as crosses, touches,
and percentage moves.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from .schema import EventType, EventDefinition, ReferenceLevel
from .indicators import Indicators


logger = logging.getLogger(__name__)


class EventDetector:
    """Detects events in OHLCV data based on event definitions."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize event detector with price data.

        Args:
            df: DataFrame with OHLCV data and calculated indicators
        """
        self.df = df
        self.close = df['close']
        self.high = df['high']
        self.low = df['low']
        self.volume = df['volume']

    def get_reference_value(self, reference: ReferenceLevel, index: Optional[int] = None) -> Optional[float]:
        """
        Calculate the reference level value at a specific point or overall.

        Args:
            reference: Reference level definition
            index: Optional specific index in the dataframe

        Returns:
            Reference value or None if cannot be calculated
        """
        if reference.type == "fixed":
            return reference.value

        elif reference.type == "sma":
            if reference.period:
                sma = Indicators.sma(self.close, reference.period)
                return sma.iloc[index] if index is not None else sma
            return None

        elif reference.type == "ema":
            if reference.period:
                ema = Indicators.ema(self.close, reference.period)
                return ema.iloc[index] if index is not None else ema
            return None

        elif reference.type == "support":
            support, _ = Indicators.support_resistance(
                self.close,
                lookback=reference.lookback or 90
            )
            return support

        elif reference.type == "resistance":
            _, resistance = Indicators.support_resistance(
                self.close,
                lookback=reference.lookback or 90
            )
            return resistance

        elif reference.type == "vwap":
            vwap = Indicators.vwap(self.high, self.low, self.close, self.volume)
            return vwap.iloc[index] if index is not None else vwap

        else:
            logger.warning(f"Unknown reference type: {reference.type}")
            return None

    def detect_price_crosses_above(self, event: EventDefinition) -> List[Dict[str, Any]]:
        """
        Detect when price crosses above a reference level.

        Returns:
            List of detected events with timestamps and values
        """
        events = []
        ref_value = self.get_reference_value(event.reference)

        if ref_value is None:
            return events

        # Handle series reference (like SMA)
        if isinstance(ref_value, pd.Series):
            for i in range(1, len(self.close)):
                if self.close.iloc[i-1] <= ref_value.iloc[i-1] and self.close.iloc[i] > ref_value.iloc[i]:
                    events.append({
                        'date': self.df.index[i],
                        'price': self.close.iloc[i],
                        'reference': ref_value.iloc[i],
                        'type': 'cross_above'
                    })
        # Handle fixed reference value
        else:
            for i in range(1, len(self.close)):
                if self.close.iloc[i-1] <= ref_value and self.close.iloc[i] > ref_value:
                    events.append({
                        'date': self.df.index[i],
                        'price': self.close.iloc[i],
                        'reference': ref_value,
                        'type': 'cross_above'
                    })

        return events

    def detect_price_crosses_below(self, event: EventDefinition) -> List[Dict[str, Any]]:
        """Detect when price crosses below a reference level."""
        events = []
        ref_value = self.get_reference_value(event.reference)

        if ref_value is None:
            return events

        if isinstance(ref_value, pd.Series):
            for i in range(1, len(self.close)):
                if self.close.iloc[i-1] >= ref_value.iloc[i-1] and self.close.iloc[i] < ref_value.iloc[i]:
                    events.append({
                        'date': self.df.index[i],
                        'price': self.close.iloc[i],
                        'reference': ref_value.iloc[i],
                        'type': 'cross_below'
                    })
        else:
            for i in range(1, len(self.close)):
                if self.close.iloc[i-1] >= ref_value and self.close.iloc[i] < ref_value:
                    events.append({
                        'date': self.df.index[i],
                        'price': self.close.iloc[i],
                        'reference': ref_value,
                        'type': 'cross_below'
                    })

        return events

    def detect_price_touches(self, event: EventDefinition) -> List[Dict[str, Any]]:
        """
        Detect when price comes within tolerance of a reference level.

        This is useful for support/resistance touches.
        """
        events = []
        ref_value = self.get_reference_value(event.reference)

        if ref_value is None:
            return events

        tolerance_pct = event.tolerance / 100.0

        if isinstance(ref_value, pd.Series):
            for i in range(len(self.df)):
                ref = ref_value.iloc[i]
                if pd.isna(ref):
                    continue
                lower_bound = ref * (1 - tolerance_pct)
                upper_bound = ref * (1 + tolerance_pct)

                # Check if low touched or high touched within tolerance
                if (self.low.iloc[i] <= upper_bound and self.high.iloc[i] >= lower_bound):
                    events.append({
                        'date': self.df.index[i],
                        'price': self.close.iloc[i],
                        'reference': ref,
                        'type': 'touch',
                        'tolerance': event.tolerance
                    })
        else:
            lower_bound = ref_value * (1 - tolerance_pct)
            upper_bound = ref_value * (1 + tolerance_pct)

            for i in range(len(self.df)):
                if (self.low.iloc[i] <= upper_bound and self.high.iloc[i] >= lower_bound):
                    events.append({
                        'date': self.df.index[i],
                        'price': self.close.iloc[i],
                        'reference': ref_value,
                        'type': 'touch',
                        'tolerance': event.tolerance
                    })

        return events

    def detect_price_rises_by(self, event: EventDefinition) -> List[Dict[str, Any]]:
        """
        Detect when price rises by a minimum percentage.

        Returns events marking the END of the rise.
        """
        events = []
        min_change = event.min_change or 5.0  # Default 5%
        max_change = event.max_change  # Optional maximum

        for i in range(1, len(self.close)):
            # Look back to find local minimum
            lookback = min(20, i)  # Look back up to 20 days
            local_min = self.close.iloc[i-lookback:i].min()
            current_price = self.close.iloc[i]

            pct_change = ((current_price - local_min) / local_min) * 100

            if pct_change >= min_change:
                if max_change is None or pct_change <= max_change:
                    events.append({
                        'date': self.df.index[i],
                        'price': current_price,
                        'start_price': local_min,
                        'change_pct': pct_change,
                        'type': 'rise'
                    })

        return events

    def detect_price_falls_by(self, event: EventDefinition) -> List[Dict[str, Any]]:
        """
        Detect when price falls by a minimum percentage.

        Returns events marking the END of the fall.
        """
        events = []
        min_change = event.min_change or 5.0  # Default 5%
        max_change = event.max_change

        for i in range(1, len(self.close)):
            # Look back to find local maximum
            lookback = min(20, i)
            local_max = self.close.iloc[i-lookback:i].max()
            current_price = self.close.iloc[i]

            pct_change = ((local_max - current_price) / local_max) * 100

            if pct_change >= min_change:
                if max_change is None or pct_change <= max_change:
                    events.append({
                        'date': self.df.index[i],
                        'price': current_price,
                        'start_price': local_max,
                        'change_pct': pct_change,
                        'type': 'fall'
                    })

        return events

    def detect_volume_spike(self, event: EventDefinition) -> List[Dict[str, Any]]:
        """
        Detect volume spikes above average.

        Uses reference.value as multiplier (e.g., 2.0 = 2x average volume)
        """
        events = []
        multiplier = event.reference.value or 2.0
        period = event.reference.period or 20

        avg_volume = self.volume.rolling(window=period, min_periods=period).mean()

        for i in range(period, len(self.volume)):
            if self.volume.iloc[i] >= avg_volume.iloc[i] * multiplier:
                events.append({
                    'date': self.df.index[i],
                    'volume': self.volume.iloc[i],
                    'avg_volume': avg_volume.iloc[i],
                    'multiplier': self.volume.iloc[i] / avg_volume.iloc[i],
                    'type': 'volume_spike'
                })

        return events

    def detect_event(self, event: EventDefinition) -> List[Dict[str, Any]]:
        """
        Main method to detect any event type.

        Args:
            event: Event definition

        Returns:
            List of detected events
        """
        event_type = event.type

        if event_type == EventType.PRICE_CROSSES_ABOVE:
            return self.detect_price_crosses_above(event)
        elif event_type == EventType.PRICE_CROSSES_BELOW:
            return self.detect_price_crosses_below(event)
        elif event_type == EventType.PRICE_TOUCHES:
            return self.detect_price_touches(event)
        elif event_type == EventType.PRICE_RISES_BY:
            return self.detect_price_rises_by(event)
        elif event_type == EventType.PRICE_FALLS_BY:
            return self.detect_price_falls_by(event)
        elif event_type == EventType.VOLUME_SPIKE:
            return self.detect_volume_spike(event)
        else:
            logger.warning(f"Event type {event_type} not implemented yet")
            return []
