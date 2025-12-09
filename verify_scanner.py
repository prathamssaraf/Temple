"""
Verification script demonstrating the Scanner Layer API with mock data.

This script shows how to scan multiple stocks for pattern matches.
Uses mock data to demonstrate scanner functionality independently.
"""

import sys
import os
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add current directory to path
sys.path.append(os.getcwd())

from scanner import (
    create_scanner,
    ScannerConfig,
    create_custom_universe
)


# Mock data and pattern classes for demonstration
def create_mock_ohlcv(symbol: str) -> pd.DataFrame:
    """Generate mock OHLCV data for a symbol."""
    np.random.seed(hash(symbol) % 2**32)  # Consistent data per symbol
    days = 500
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')

    base_price = np.random.uniform(50, 200)
    returns = np.random.randn(days) * 0.02
    close = base_price * np.exp(np.cumsum(returns))

    daily_range = np.abs(np.random.randn(days)) * 0.02 * close
    high = close + daily_range * np.random.rand(days)
    low = close - daily_range * np.random.rand(days)
    open_price = low + (high - low) * np.random.rand(days)
    volume = np.random.randint(1e6, 1e8, days)

    return pd.DataFrame({
        'open': open_price,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    }, index=dates)


@dataclass
class MockPattern:
    """Mock pattern for demonstration."""
    name: str
    description: str


@dataclass
class MockPatternMatch:
    """Mock pattern match result."""
    pattern_name: str
    symbol: str
    count: int
    confidence: float
    timeframe_start: str
    timeframe_end: str


class MockPatternMatcher:
    """Mock pattern matcher for demonstration."""

    def match(self, df: pd.DataFrame, symbol: str, pattern: MockPattern) -> MockPatternMatch:
        """Simulate pattern matching with random results."""
        # Simulate realistic matching
        np.random.seed(hash(symbol + pattern.name) % 2**32)

        # Some symbols match better than others
        base_confidence = np.random.uniform(0.3, 0.9)
        count = int(np.random.uniform(1, 20))

        return MockPatternMatch(
            pattern_name=pattern.name,
            symbol=symbol,
            count=count,
            confidence=base_confidence,
            timeframe_start=str(df.index[0]),
            timeframe_end=str(df.index[-1])
        )


def demo_basic_scan():
    """Demo 1: Basic stock scanning."""
    print("\n" + "="*70)
    print("DEMO 1: Basic Stock Scanning")
    print("="*70)
    print("Scanning 5 stocks for mean reversion pattern")

    # Setup mock components
    data_fetcher = create_mock_ohlcv
    matcher = MockPatternMatcher()
    pattern = MockPattern(
        name="Mean Reversion",
        description="Price deviates and returns to average"
    )

    # Create scanner
    scanner = create_scanner(
        data_fetcher=data_fetcher,
        pattern_matcher=matcher
    )

    # Define symbols
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]

    # Scan
    print(f"\nScanning {len(symbols)} symbols...")
    results = scanner.scan(
        symbols=symbols,
        pattern=pattern,
        min_confidence=0.5
    )

    # Display results
    print(f"\n{'='*70}")
    print(f"SCAN RESULTS")
    print(f"{'='*70}")
    print(f"  Total Scanned: {results.total_symbols}")
    print(f"  Successful: {results.successful_scans}")
    print(f"  Failed: {results.failed_scans}")
    print(f"  Matches Found: {results.matches_found}")
    print(f"  Average Confidence: {results.average_confidence:.2%}")
    print(f"  Duration: {results.duration_seconds:.2f}s")

    print(f"\n  Top Matches:")
    top_matches = scanner.get_best_matches(results, top_n=3)
    for i, match in enumerate(top_matches, 1):
        print(f"    {i}. {match.symbol}: {match.confidence:.2%} ({match.occurrences} occurrences)")

    return results


def demo_universe_scan():
    """Demo 2: Scanning a stock universe."""
    print("\n" + "="*70)
    print("DEMO 2: Universe Scanning")
    print("="*70)
    print("Scanning pre-defined stock universe (Tech Stocks)")

    # Setup
    data_fetcher = create_mock_ohlcv
    matcher = MockPatternMatcher()
    pattern = MockPattern(
        name="Support Bounce",
        description="Price bounces off support levels"
    )

    scanner = create_scanner(
        data_fetcher=data_fetcher,
        pattern_matcher=matcher
    )

    # List available universes
    print(f"\nAvailable universes:")
    for name in scanner.list_universes():
        print(f"  - {name}")

    # Scan tech universe
    print(f"\nScanning 'tech' universe...")
    results = scanner.scan_universe(
        universe_name="tech",
        pattern=pattern,
        min_confidence=0.6
    )

    # Display results
    print(f"\n{'='*70}")
    print(f"RESULTS: Tech Stocks Universe")
    print(f"{'='*70}")
    print(f"  Matches: {results.matches_found}/{results.total_symbols}")
    print(f"  Average Confidence: {results.average_confidence:.2%}")
    print(f"  Duration: {results.duration_seconds:.2f}s")

    print(f"\n  Top 5 Matches:")
    for i, match in enumerate(scanner.get_best_matches(results, top_n=5), 1):
        print(f"    {i}. {match.symbol}: {match.confidence:.2%}")

    return results


def demo_custom_universe():
    """Demo 3: Creating and scanning custom universe."""
    print("\n" + "="*70)
    print("DEMO 3: Custom Universe")
    print("="*70)
    print("Create custom watchlist and scan")

    # Setup
    data_fetcher = create_mock_ohlcv
    matcher = MockPatternMatcher()
    pattern = MockPattern(
        name="Volatility Cycle",
        description="Large price swings"
    )

    scanner = create_scanner(
        data_fetcher=data_fetcher,
        pattern_matcher=matcher
    )

    # Create custom universe
    my_portfolio = ["AAPL", "TSLA", "NVDA", "AMD", "PLTR"]
    universe = scanner.create_custom_universe(
        name="My Portfolio",
        symbols=my_portfolio
    )

    print(f"\nCreated custom universe: '{universe.name}'")
    print(f"  Symbols: {', '.join(universe.symbols)}")

    # Scan custom universe
    print(f"\nScanning custom universe...")
    results = scanner.scan(
        symbols=list(universe.symbols),
        pattern=pattern,
        min_confidence=0.5
    )

    print(f"\n{'='*70}")
    print(f"RESULTS: {universe.name}")
    print(f"{'='*70}")
    print(f"  Matches: {results.matches_found}/{results.total_symbols}")

    for match in scanner.get_best_matches(results, top_n=10):
        print(f"  - {match.symbol}: {match.confidence:.2%} confidence")

    return results


def demo_progress_tracking():
    """Demo 4: Progress tracking during scan."""
    print("\n" + "="*70)
    print("DEMO 4: Progress Tracking")
    print("="*70)
    print("Scan with live progress updates")

    # Progress callback
    def progress_callback(completed, total, symbol):
        pct = (completed / total) * 100
        print(f"  [{pct:5.1f}%] Scanned {symbol}")

    # Setup
    data_fetcher = create_mock_ohlcv
    matcher = MockPatternMatcher()
    pattern = MockPattern(
        name="Mean Reversion",
        description="Price returns to mean"
    )

    scanner = create_scanner(
        data_fetcher=data_fetcher,
        pattern_matcher=matcher
    )

    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "NFLX"]

    print(f"\nScanning {len(symbols)} symbols with progress tracking...\n")
    results = scanner.scan(
        symbols=symbols,
        pattern=pattern,
        min_confidence=0.6,
        progress_callback=progress_callback
    )

    print(f"\n{'='*70}")
    print(f"Scan complete: {results.matches_found} matches found")
    print(f"{'='*70}")

    return results


def demo_export_results():
    """Demo 5: Exporting scan results."""
    print("\n" + "="*70)
    print("DEMO 5: Export Results")
    print("="*70)
    print("Export scan results in different formats")

    # Setup and scan
    data_fetcher = create_mock_ohlcv
    matcher = MockPatternMatcher()
    pattern = MockPattern(name="Test Pattern", description="Test")

    scanner = create_scanner(
        data_fetcher=data_fetcher,
        pattern_matcher=matcher
    )

    results = scanner.scan(
        symbols=["AAPL", "MSFT", "GOOGL"],
        pattern=pattern,
        min_confidence=0.5
    )

    # Export as dictionary
    print("\n[1] Export as Dictionary:")
    dict_export = scanner.export_results(results, format="dict")
    print(f"    Keys: {list(dict_export.keys())}")
    print(f"    Results count: {len(dict_export['results'])}")

    # Export as JSON
    print("\n[2] Export as JSON:")
    json_export = scanner.export_results(results, format="json")
    print(f"    Length: {len(json_export)} characters")
    print(f"    Sample: {json_export[:100]}...")

    # Export as CSV
    print("\n[3] Export as CSV:")
    csv_export = scanner.export_results(results, format="csv")
    lines = csv_export.split('\n')
    print(f"    Lines: {len(lines)}")
    print(f"    Header: {lines[0]}")
    if len(lines) > 1:
        print(f"    Sample: {lines[1]}")

    return results


def demo_parallel_scanning():
    """Demo 6: Parallel scanning for better performance."""
    print("\n" + "="*70)
    print("DEMO 6: Parallel Scanning")
    print("="*70)
    print("Compare sequential vs parallel scanning")

    data_fetcher = create_mock_ohlcv
    matcher = MockPatternMatcher()
    pattern = MockPattern(name="Test Pattern", description="Test")
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "NFLX", "AMD", "INTC"]

    # Sequential scan
    print(f"\n[1] Sequential Scan ({len(symbols)} symbols):")
    scanner_seq = create_scanner(
        data_fetcher=data_fetcher,
        pattern_matcher=matcher,
        config=ScannerConfig(parallel=False)
    )
    results_seq = scanner_seq.scan(symbols, pattern, min_confidence=0.5)
    print(f"    Duration: {results_seq.duration_seconds:.2f}s")
    print(f"    Matches: {results_seq.matches_found}")

    # Parallel scan
    print(f"\n[2] Parallel Scan ({len(symbols)} symbols, 4 workers):")
    scanner_par = create_scanner(
        data_fetcher=data_fetcher,
        pattern_matcher=matcher,
        config=ScannerConfig(parallel=True, max_workers=4)
    )
    results_par = scanner_par.scan(symbols, pattern, min_confidence=0.5)
    print(f"    Duration: {results_par.duration_seconds:.2f}s")
    print(f"    Matches: {results_par.matches_found}")

    speedup = results_seq.duration_seconds / results_par.duration_seconds if results_par.duration_seconds > 0 else 1
    print(f"\n    Speedup: {speedup:.2f}x")

    return results_par


def main():
    """Run all verification demos."""
    print("\n" + "="*70)
    print("TEMPLE SCANNER LAYER - API VERIFICATION (MOCK DATA)")
    print("="*70)
    print("\nUsing synthetic data - no external dependencies required!")

    try:
        # Run demos
        demo_basic_scan()
        demo_universe_scan()
        demo_custom_universe()
        demo_progress_tracking()
        demo_export_results()
        demo_parallel_scanning()

        print("\n" + "="*70)
        print("[OK] ALL DEMOS COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\nThe scanner layer is ready to scan stocks for patterns!")
        print("Next steps:")
        print("  1. Integrate with data layer for real stock data")
        print("  2. Integrate with patterns layer for real pattern detection")
        print("  3. Build backend API to expose scanner functionality")
        print("  4. Connect to frontend dashboard")

    except Exception as e:
        print(f"\n[X] Error during verification: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
