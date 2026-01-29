"""
Test script for pivot mean reversion pattern detection.
"""
import sys
import logging
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
from api.services import create_data_fetcher

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_pivot_mean_reversion(symbol: str, pivot_type: str):
    """
    Test pivot mean reversion pattern on a stock.

    Args:
        symbol: Stock ticker
        pivot_type: Type of pivot ('mode', 'median', 'volume', or 'fixed')
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"Testing Pivot Mean Reversion ({pivot_type.upper()}) on {symbol}")
    logger.info(f"{'='*60}\n")

    # Fetch data
    data_fetcher = create_data_fetcher()
    df = data_fetcher.get_stock_data(symbol, period="365d")

    if df is None or df.empty:
        logger.error(f"Failed to fetch data for {symbol}")
        return

    logger.info(f"Fetched {len(df)} days of data")
    logger.info(f"Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")

    # Define pivot reference based on type
    if pivot_type == "mode":
        reference = ReferenceLevel(type="pivot_mode", lookback=365, tolerance=5.0)
    elif pivot_type == "median":
        reference = ReferenceLevel(type="pivot_median", lookback=365, tolerance=5.0)
    elif pivot_type == "volume":
        reference = ReferenceLevel(type="pivot_volume", lookback=365, tolerance=5.0)
    elif pivot_type == "fixed":
        # Use median as fixed value for testing
        fixed_price = df['close'].median()
        reference = ReferenceLevel(type="fixed", value=fixed_price, tolerance=5.0)
        logger.info(f"Using fixed pivot: ${fixed_price:.2f}")
    else:
        logger.error(f"Unknown pivot type: {pivot_type}")
        return

    # Create pattern definition
    pattern = PatternDefinition(
        name=f"Pivot Mean Reversion ({pivot_type})",
        description=f"Price oscillates around {pivot_type} pivot point",
        sequence=[
            SequenceStep(
                event=EventDefinition(
                    type=EventType.PIVOT_DEVIATION,
                    reference=reference,
                    tolerance=5.0
                ),
                name="Deviation from pivot"
            ),
            SequenceStep(
                event=EventDefinition(
                    type=EventType.PIVOT_RETURN,
                    reference=reference,
                    tolerance=5.0
                ),
                max_duration_days=28,  # Must return within 4 weeks
                name="Return to pivot"
            )
        ],
        frequency=FrequencyConstraint(
            min_occurrences=8,
            timeframe=365,
            timeframe_unit=TimeframeUnit.DAYS
        )
    )

    # Run pattern matching
    matcher = create_pattern_matcher()
    result = matcher.match(df, symbol, pattern)

    # Print results
    logger.info(f"\n{'='*60}")
    logger.info(f"RESULTS for {symbol}")
    logger.info(f"{'='*60}")
    logger.info(f"Pattern: {result.pattern_name}")
    logger.info(f"Occurrences: {result.count}")
    logger.info(f"Confidence: {result.confidence:.2%}")
    logger.info(f"Timeframe: {result.timeframe_start} to {result.timeframe_end}")

    if result.count > 0:
        logger.info(f"\nPattern MATCHED! ✓")
        logger.info(f"Found {result.count} complete cycles (deviation + return)")
        logger.info(f"Required: {pattern.frequency.min_occurrences} cycles in {pattern.frequency.timeframe} days")

        # Show first few occurrences
        logger.info(f"\nFirst 5 occurrences:")
        for i, occ in enumerate(result.occurrences[:5], 1):
            start = occ['start_date']
            end = occ['end_date']
            days = (end - start).days
            logger.info(f"  {i}. {start.date()} → {end.date()} ({days} days)")
    else:
        logger.info(f"\nPattern NOT matched ✗")
        logger.info(f"Required at least {pattern.frequency.min_occurrences} occurrences")

    return result


if __name__ == "__main__":
    # Test on a few stocks with different pivot detection methods
    test_stocks = ["AAPL", "MSFT", "TSLA"]
    pivot_types = ["mode", "median", "volume"]

    for stock in test_stocks:
        for ptype in pivot_types:
            try:
                test_pivot_mean_reversion(stock, ptype)
                print("\n")
            except Exception as e:
                logger.error(f"Error testing {stock} with {ptype}: {e}", exc_info=True)
