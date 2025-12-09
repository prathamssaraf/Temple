"""
Sequence matching engine for temporal pattern detection.

This module matches sequences of events and counts their occurrences over time.
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

from .schema import PatternDefinition, SequenceStep, PatternMatch, FrequencyConstraint, TimeframeUnit
from .events import EventDetector


logger = logging.getLogger(__name__)


class SequenceMatcher:
    """Matches multi-step sequences in detected events."""

    def __init__(self, df: pd.DataFrame, symbol: str):
        """
        Initialize sequence matcher.

        Args:
            df: DataFrame with OHLCV data and indicators
            symbol: Stock symbol being analyzed
        """
        self.df = df
        self.symbol = symbol
        self.detector = EventDetector(df)

    def match_pattern(self, pattern: PatternDefinition) -> PatternMatch:
        """
        Match a complete pattern definition against the data.

        Args:
            pattern: Pattern definition to match

        Returns:
            PatternMatch with results
        """
        logger.info(f"Matching pattern '{pattern.name}' on {self.symbol}")

        # Step 1: Detect all events for each step in the sequence
        step_events = []
        for step in pattern.sequence:
            events = self.detector.detect_event(step.event)
            step_events.append({
                'step': step,
                'events': events
            })

        # Step 2: Find valid sequences
        sequences = self._find_sequences(step_events, pattern.sequence)

        # Step 3: Apply frequency constraints
        valid_sequences = self._apply_frequency_constraints(
            sequences,
            pattern.frequency
        )

        # Step 4: Calculate confidence score
        confidence = self._calculate_confidence(valid_sequences, pattern.frequency)

        # Create match result
        timeframe_start = str(self.df.index[0])
        timeframe_end = str(self.df.index[-1])

        match = PatternMatch(
            pattern_name=pattern.name,
            symbol=self.symbol,
            occurrences=valid_sequences,
            count=len(valid_sequences),
            timeframe_start=timeframe_start,
            timeframe_end=timeframe_end,
            confidence=confidence,
            metadata={
                'description': pattern.description,
                'sequence_length': len(pattern.sequence),
                'frequency_constraint': {
                    'min_occurrences': pattern.frequency.min_occurrences,
                    'timeframe': pattern.frequency.timeframe,
                    'unit': pattern.frequency.timeframe_unit.value
                }
            }
        )

        logger.info(f"Pattern '{pattern.name}': found {match.count} occurrences (confidence: {confidence:.2f})")

        return match

    def _find_sequences(self, step_events: List[Dict], steps: List[SequenceStep]) -> List[Dict[str, Any]]:
        """
        Find valid sequences of events matching the pattern steps.

        Args:
            step_events: List of detected events for each step
            steps: Sequence step definitions

        Returns:
            List of valid sequences
        """
        if not step_events or not steps:
            return []

        sequences = []

        # Start with events from first step
        first_step_events = step_events[0]['events']

        for first_event in first_step_events:
            # Try to build a sequence starting from this event
            sequence = self._build_sequence(first_event, step_events, steps, 0)
            if sequence:
                sequences.append(sequence)

        return sequences

    def _build_sequence(
        self,
        current_event: Dict[str, Any],
        step_events: List[Dict],
        steps: List[SequenceStep],
        step_index: int
    ) -> Optional[Dict[str, Any]]:
        """
        Recursively build a sequence starting from current event.

        Args:
            current_event: Current event in the sequence
            step_events: All detected events for each step
            steps: Sequence step definitions
            step_index: Current step index

        Returns:
            Complete sequence dict or None if invalid
        """
        # Base case: we've matched all steps
        if step_index >= len(steps) - 1:
            return {
                'events': [current_event],
                'start_date': current_event['date'],
                'end_date': current_event['date']
            }

        # Get next step's events
        next_step_index = step_index + 1
        next_step = steps[next_step_index]
        next_events = step_events[next_step_index]['events']

        # Find next event that satisfies duration constraints
        for next_event in next_events:
            if next_event['date'] <= current_event['date']:
                continue

            # Check duration constraints
            days_between = (next_event['date'] - current_event['date']).days

            if next_step.min_duration_days and days_between < next_step.min_duration_days:
                continue
            if next_step.max_duration_days and days_between > next_step.max_duration_days:
                continue

            # Recursively try to complete the sequence
            rest_of_sequence = self._build_sequence(next_event, step_events, steps, next_step_index)

            if rest_of_sequence:
                # Successfully built the rest, prepend current event
                return {
                    'events': [current_event] + rest_of_sequence['events'],
                    'start_date': current_event['date'],
                    'end_date': rest_of_sequence['end_date']
                }

        # Could not find a valid next event
        return None

    def _apply_frequency_constraints(
        self,
        sequences: List[Dict[str, Any]],
        frequency: FrequencyConstraint
    ) -> List[Dict[str, Any]]:
        """
        Filter sequences based on frequency constraints.

        Args:
            sequences: All matched sequences
            frequency: Frequency constraint

        Returns:
            Filtered sequences that meet frequency requirements
        """
        if not sequences:
            return []

        # Calculate timeframe in days
        timeframe_days = self._get_timeframe_days(frequency.timeframe, frequency.timeframe_unit)

        # Use sliding window to find periods with sufficient occurrences
        valid_sequences = []

        for i, seq in enumerate(sequences):
            window_start = seq['start_date']
            window_end = window_start + timedelta(days=timeframe_days)

            # Count sequences in this window
            sequences_in_window = [
                s for s in sequences
                if window_start <= s['start_date'] < window_end
            ]

            count_in_window = len(sequences_in_window)

            # Check if frequency constraint is met
            if count_in_window >= frequency.min_occurrences:
                if frequency.max_occurrences is None or count_in_window <= frequency.max_occurrences:
                    # Add window info to sequence
                    seq['window_count'] = count_in_window
                    seq['window_start'] = window_start
                    seq['window_end'] = window_end
                    if seq not in valid_sequences:
                        valid_sequences.append(seq)

        return valid_sequences

    def _get_timeframe_days(self, timeframe: int, unit: TimeframeUnit) -> int:
        """Convert timeframe to days."""
        if unit == TimeframeUnit.DAYS:
            return timeframe
        elif unit == TimeframeUnit.WEEKS:
            return timeframe * 7
        elif unit == TimeframeUnit.MONTHS:
            return timeframe * 30  # Approximate
        elif unit == TimeframeUnit.YEARS:
            return timeframe * 365
        else:
            return timeframe

    def _calculate_confidence(
        self,
        sequences: List[Dict[str, Any]],
        frequency: FrequencyConstraint
    ) -> float:
        """
        Calculate confidence score for the pattern match.

        Confidence is based on:
        - Number of occurrences vs minimum required
        - Consistency of occurrences over time
        - Quality of individual sequences

        Returns:
            Confidence score from 0.0 to 1.0
        """
        if not sequences:
            return 0.0

        count = len(sequences)
        min_required = frequency.min_occurrences

        # Base confidence: how much we exceed minimum
        if count >= min_required:
            base_confidence = min(1.0, (count / min_required) * 0.5)  # Cap at 0.5
        else:
            return 0.0

        # Bonus for consistency: check if sequences are evenly distributed
        if count > 1:
            dates = [seq['start_date'] for seq in sequences]
            dates.sort()
            intervals = [(dates[i+1] - dates[i]).days for i in range(len(dates) - 1)]
            avg_interval = sum(intervals) / len(intervals)
            std_interval = (sum((x - avg_interval) ** 2 for x in intervals) / len(intervals)) ** 0.5
            consistency_score = max(0, 1 - (std_interval / avg_interval)) * 0.3 if avg_interval > 0 else 0
        else:
            consistency_score = 0

        # Bonus for exceeding requirements
        excess_bonus = min(0.2, (count - min_required) / min_required * 0.2) if count > min_required else 0

        total_confidence = base_confidence + consistency_score + excess_bonus

        return min(1.0, total_confidence)


def match_multiple_patterns(
    df: pd.DataFrame,
    symbol: str,
    patterns: List[PatternDefinition]
) -> List[PatternMatch]:
    """
    Match multiple patterns against the same data.

    Args:
        df: DataFrame with OHLCV data
        symbol: Stock symbol
        patterns: List of pattern definitions

    Returns:
        List of pattern matches
    """
    matcher = SequenceMatcher(df, symbol)
    matches = []

    for pattern in patterns:
        try:
            match = matcher.match_pattern(pattern)
            matches.append(match)
        except Exception as e:
            logger.error(f"Error matching pattern '{pattern.name}': {e}")

    return matches
