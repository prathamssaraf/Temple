"""
Verification script demonstrating the Patterns Layer API with mock data.

This script shows how to define and detect temporal patterns using synthetic data.
No external dependencies required - patterns layer is fully self-contained.
"""

import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add current directory to path
sys.path.append(os.getcwd())

from patterns.mock_data import (
    create_mock_ohlcv,
    create_mean_reverting_data,
    create_volatile_data,
    create_support_resistance_data
)
from patterns import (
    create_pattern_matcher,
    PatternDefinition,
    SequenceStep,
    EventDefinition,
    ReferenceLevel,
    FrequencyConstraint,
    EventType,
    TimeframeUnit
)


def demo_support_bounce_pattern():
    """Demo 1: Support Bounce Pattern - Price touches support and recovers."""
    print("\n" + "="*70)
    print("DEMO 1: Support Bounce Pattern")
    print("="*70)
    print("Pattern: Stock touches support level and bounces back 5+ times in 6 months")

    # Define the pattern
    pattern = PatternDefinition(
        name="Support Bounce",
        description="Price touches support and bounces back repeatedly",
        sequence=[
            SequenceStep(
                event=EventDefinition(
                    type=EventType.PRICE_TOUCHES,
                    reference=ReferenceLevel(type="support", lookback=90),
                    tolerance=1.5
                ),
                name="Touch support"
            ),
            SequenceStep(
                event=EventDefinition(
                    type=EventType.PRICE_RISES_BY,
                    min_change=3.0
                ),
                max_duration_days=15,
                name="Bounce up"
            )
        ],
        frequency=FrequencyConstraint(
            min_occurrences=5,
            timeframe=6,
            timeframe_unit=TimeframeUnit.MONTHS
        ),
        tags=["mean-reversion", "support"]
    )

    # Generate mock data with support/resistance characteristics
    print("\nGenerating mock data with support/resistance levels...")
    df = create_support_resistance_data(
        days=500,
        support_level=95.0,
        resistance_level=105.0,
        seed=42
    )
    print(f"[OK] Generated {len(df)} rows of data")
    print(f"     Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")

    # Create matcher and find pattern
    print(f"\nSearching for '{pattern.name}' pattern...")
    matcher = create_pattern_matcher()
    match = matcher.match(df, "MOCK-SR", pattern)

    # Display results
    print(f"\n{'='*70}")
    print(f"RESULTS: {pattern.name}")
    print(f"{'='*70}")
    print(f"  Symbol: {match.symbol}")
    print(f"  Occurrences Found: {match.count}")
    print(f"  Confidence: {match.confidence:.2%}")
    print(f"  Timeframe: {match.timeframe_start[:10]} to {match.timeframe_end[:10]}")
    print(f"  Status: {'PASS' if match.count >= 5 else 'FAIL'}")

    if match.occurrences:
        print(f"\n  Sample Occurrences:")
        for i, occ in enumerate(match.occurrences[:3], 1):
            print(f"    {i}. {occ['start_date'].strftime('%Y-%m-%d')} -> {occ['end_date'].strftime('%Y-%m-%d')}")

    return match


def demo_mean_reversion_pattern():
    """Demo 2: Mean Reversion Pattern - Price deviates from average and returns."""
    print("\n" + "="*70)
    print("DEMO 2: Mean Reversion Pattern")
    print("="*70)
    print("Pattern: Price falls below SMA20, then recovers 8+ times in 1 year")

    # Define the pattern
    pattern = PatternDefinition(
        name="Mean Reversion",
        description="Price deviates below moving average and returns",
        sequence=[
            SequenceStep(
                event=EventDefinition(
                    type=EventType.PRICE_CROSSES_BELOW,
                    reference=ReferenceLevel(type="sma", period=20)
                ),
                name="Fall below SMA20"
            ),
            SequenceStep(
                event=EventDefinition(
                    type=EventType.PRICE_CROSSES_ABOVE,
                    reference=ReferenceLevel(type="sma", period=20)
                ),
                max_duration_days=20,
                name="Return to SMA20"
            )
        ],
        frequency=FrequencyConstraint(
            min_occurrences=8,
            timeframe=1,
            timeframe_unit=TimeframeUnit.YEARS
        ),
        tags=["mean-reversion", "sma"]
    )

    # Generate mean-reverting mock data
    print("\nGenerating mean-reverting mock data...")
    df = create_mean_reverting_data(
        days=500,
        base_price=100.0,
        mean_reversion_speed=0.1,
        seed=42
    )
    print(f"[OK] Generated {len(df)} rows of data")
    print(f"     Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")

    # Match pattern
    print(f"\nSearching for '{pattern.name}' pattern...")
    matcher = create_pattern_matcher()
    match = matcher.match(df, "MOCK-MR", pattern)

    # Display results
    print(f"\n{'='*70}")
    print(f"RESULTS: {pattern.name}")
    print(f"{'='*70}")
    print(f"  Symbol: {match.symbol}")
    print(f"  Occurrences Found: {match.count}")
    print(f"  Confidence: {match.confidence:.2%}")
    print(f"  Status: {'PASS' if match.count >= 8 else 'FAIL'}")

    return match


def demo_volatility_pattern():
    """Demo 3: Volatility Pattern - Large moves followed by reversals."""
    print("\n" + "="*70)
    print("DEMO 3: Volatility Spike Pattern")
    print("="*70)
    print("Pattern: Stock rises 8%, then falls 8%, repeating 3+ times in 6 months")

    # Define the pattern
    pattern = PatternDefinition(
        name="Volatility Cycle",
        description="Large swings up and down repeatedly",
        sequence=[
            SequenceStep(
                event=EventDefinition(
                    type=EventType.PRICE_RISES_BY,
                    min_change=8.0,
                    max_change=15.0
                ),
                name="Sharp rise"
            ),
            SequenceStep(
                event=EventDefinition(
                    type=EventType.PRICE_FALLS_BY,
                    min_change=8.0,
                    max_change=15.0
                ),
                max_duration_days=30,
                name="Sharp fall"
            )
        ],
        frequency=FrequencyConstraint(
            min_occurrences=3,
            timeframe=6,
            timeframe_unit=TimeframeUnit.MONTHS
        ),
        tags=["volatility"]
    )

    # Generate volatile mock data
    print("\nGenerating volatile mock data...")
    df = create_volatile_data(
        days=500,
        base_price=100.0,
        volatility=0.05,
        seed=42
    )
    print(f"[OK] Generated {len(df)} rows of data")
    print(f"     Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")

    # Match pattern
    print(f"\nSearching for '{pattern.name}' pattern...")
    matcher = create_pattern_matcher()
    match = matcher.match(df, "MOCK-VOL", pattern)

    # Display results
    print(f"\n{'='*70}")
    print(f"RESULTS: {pattern.name}")
    print(f"{'='*70}")
    print(f"  Symbol: {match.symbol}")
    print(f"  Occurrences Found: {match.count}")
    print(f"  Confidence: {match.confidence:.2%}")
    print(f"  Status: {'PASS' if match.count >= 3 else 'FAIL'}")

    return match


def demo_multiple_patterns():
    """Demo 4: Match multiple patterns at once."""
    print("\n" + "="*70)
    print("DEMO 4: Multiple Pattern Matching")
    print("="*70)
    print("Testing realistic stock data against 3 different patterns simultaneously")

    # Define patterns
    patterns = [
        PatternDefinition(
            name="Support Bounce",
            description="Support touches",
            sequence=[
                SequenceStep(
                    event=EventDefinition(
                        type=EventType.PRICE_TOUCHES,
                        reference=ReferenceLevel(type="support", lookback=90),
                        tolerance=2.0
                    )
                ),
            ],
            frequency=FrequencyConstraint(min_occurrences=3, timeframe=180, timeframe_unit=TimeframeUnit.DAYS)
        ),
        PatternDefinition(
            name="SMA Crossover",
            description="Price crosses SMA20",
            sequence=[
                SequenceStep(
                    event=EventDefinition(
                        type=EventType.PRICE_CROSSES_ABOVE,
                        reference=ReferenceLevel(type="sma", period=20)
                    )
                ),
            ],
            frequency=FrequencyConstraint(min_occurrences=5, timeframe=6, timeframe_unit=TimeframeUnit.MONTHS)
        ),
        PatternDefinition(
            name="Price Rise",
            description="5% gains",
            sequence=[
                SequenceStep(
                    event=EventDefinition(
                        type=EventType.PRICE_RISES_BY,
                        min_change=5.0
                    )
                ),
            ],
            frequency=FrequencyConstraint(min_occurrences=10, timeframe=1, timeframe_unit=TimeframeUnit.YEARS)
        ),
    ]

    # Generate realistic mock data
    print("\nGenerating realistic mock data...")
    df = create_mock_ohlcv(
        days=500,
        base_price=150.0,
        volatility=0.02,
        trend=0.0005,
        seed=42
    )
    print(f"[OK] Generated {len(df)} rows")
    print(f"     Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")

    # Match all patterns
    print(f"\nMatching {len(patterns)} patterns...")
    matcher = create_pattern_matcher()
    matches = matcher.match_multiple(df, "MOCK-REAL", patterns)

    # Display results
    print(f"\n{'='*70}")
    print(f"RESULTS: Multiple Patterns")
    print(f"{'='*70}")
    for match in matches:
        summary = matcher.get_summary(match)
        status = "PASS" if summary['passed'] else "FAIL"
        print(f"\n  {match.pattern_name}:")
        print(f"    Occurrences: {match.count}")
        print(f"    Confidence: {match.confidence:.2%}")
        print(f"    Status: {status}")

    # Find best matches
    best_matches = matcher.find_best_matches(matches, min_confidence=0.3)
    print(f"\n{'='*70}")
    print(f"  Best {len(best_matches)} matches (confidence >= 0.3):")
    for i, match in enumerate(best_matches, 1):
        print(f"    {i}. {match.pattern_name} - {match.confidence:.2%}")

    return matches


def demo_custom_pattern():
    """Demo 5: User-defined custom pattern."""
    print("\n" + "="*70)
    print("DEMO 5: Custom Pattern - User Defined")
    print("="*70)
    print("Pattern: 'Stock rises 10% twice, then falls' - repeating 5 times in 1 year")

    # Define custom pattern
    pattern = PatternDefinition(
        name="Double Rise Then Fall",
        description="Two consecutive 10% rises followed by a fall",
        sequence=[
            SequenceStep(
                event=EventDefinition(
                    type=EventType.PRICE_RISES_BY,
                    min_change=10.0
                ),
                name="First rise"
            ),
            SequenceStep(
                event=EventDefinition(
                    type=EventType.PRICE_RISES_BY,
                    min_change=10.0
                ),
                max_duration_days=60,
                name="Second rise"
            ),
            SequenceStep(
                event=EventDefinition(
                    type=EventType.PRICE_FALLS_BY,
                    min_change=5.0
                ),
                max_duration_days=30,
                name="Fall"
            )
        ],
        frequency=FrequencyConstraint(
            min_occurrences=2,  # Lowered for demonstration
            timeframe=1,
            timeframe_unit=TimeframeUnit.YEARS
        ),
        tags=["custom", "user-defined"]
    )

    # Generate trending data
    print("\nGenerating trending mock data...")
    df = create_mock_ohlcv(
        days=500,
        base_price=100.0,
        volatility=0.03,
        trend=0.001,  # Uptrend
        seed=42
    )
    print(f"[OK] Generated {len(df)} rows of data")
    print(f"     Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")

    # Match pattern
    print(f"\nSearching for custom pattern...")
    matcher = create_pattern_matcher()
    match = matcher.match(df, "MOCK-CUSTOM", pattern)

    # Display results
    print(f"\n{'='*70}")
    print(f"RESULTS: {pattern.name}")
    print(f"{'='*70}")
    print(f"  Description: {pattern.description}")
    print(f"  Symbol: {match.symbol}")
    print(f"  Occurrences Found: {match.count}")
    print(f"  Confidence: {match.confidence:.2%}")
    print(f"  Status: {'PASS' if match.count >= 2 else 'FAIL'}")
    print(f"\n  This demonstrates that users can define ANY temporal pattern!")

    return match


def main():
    """Run all verification demos."""
    print("\n" + "="*70)
    print("TEMPLE PATTERNS LAYER - API VERIFICATION (MOCK DATA)")
    print("="*70)
    print("\nUsing synthetic data - no external dependencies required!")

    try:
        # Run demos
        demo_support_bounce_pattern()
        demo_mean_reversion_pattern()
        demo_volatility_pattern()
        demo_multiple_patterns()
        demo_custom_pattern()

        print("\n" + "="*70)
        print("[OK] ALL DEMOS COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\nThe patterns layer is fully self-contained and ready to use!")
        print("Users can define ANY temporal pattern without writing code.")
        print("\nNext steps:")
        print("  1. Integrate with data layer for real stock data")
        print("  2. Build scanner to find patterns across multiple stocks")
        print("  3. Create dashboard for pattern visualization")

    except Exception as e:
        print(f"\n[X] Error during verification: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
