"""
Temple Scanner Layer - Pattern scanning across multiple stocks.

This module provides tools for scanning large numbers of stocks to find
pattern matches. It works seamlessly with the data and patterns layers.

Quick Start
-----------
The simplest way to use the scanner layer:

    from data.repository import DataRepository
    from patterns import create_pattern_matcher, PatternDefinition
    from scanner import create_scanner

    # Setup dependencies
    data_repo = DataRepository()
    matcher = create_pattern_matcher()

    # Create scanner
    scanner = create_scanner(
        data_fetcher=data_repo.get_ohlcv,
        pattern_matcher=matcher
    )

    # Define a pattern
    pattern = PatternDefinition(...)

    # Scan stocks
    results = scanner.scan(
        symbols=["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"],
        pattern=pattern,
        min_confidence=0.7
    )

    # Get best matches
    top_matches = scanner.get_best_matches(results, top_n=3)

    for match in top_matches:
        print(f"{match.symbol}: {match.confidence:.2%} confidence")

Universe Scanning
-----------------
Scan pre-defined stock universes:

    # Scan S&P 500
    results = scanner.scan_universe(
        universe_name="sp500",
        pattern=pattern,
        min_confidence=0.7
    )

    # Scan NASDAQ-100
    results = scanner.scan_universe("nasdaq100", pattern)

    # Scan Tech stocks
    results = scanner.scan_universe("tech", pattern)

Custom Universes
----------------
Create and scan custom watchlists:

    # Create custom universe
    my_stocks = scanner.create_custom_universe(
        name="My Portfolio",
        symbols=["AAPL", "TSLA", "NVDA"]
    )

    # List available universes
    universes = scanner.list_universes()

Progress Tracking
-----------------
Track scan progress with callbacks:

    def progress(completed, total, symbol):
        pct = (completed / total) * 100
        print(f"[{pct:.1f}%] Scanned {symbol}")

    results = scanner.scan(
        symbols=my_symbols,
        pattern=pattern,
        progress_callback=progress
    )

Parallel Processing
-------------------
Enable parallel scanning for faster results:

    from scanner import create_scanner, ScannerConfig

    config = ScannerConfig(
        parallel=True,
        max_workers=8
    )

    scanner = create_scanner(
        data_fetcher=data_repo.get_ohlcv,
        pattern_matcher=matcher,
        config=config
    )

Export Results
--------------
Export scan results in different formats:

    # Export as dictionary
    data = scanner.export_results(results, format="dict")

    # Export as JSON
    json_data = scanner.export_results(results, format="json")

    # Export as CSV
    csv_data = scanner.export_results(results, format="csv")
"""

# Public API - Configuration
from .config import (
    ScannerConfig,
    get_default_config,
    set_default_config
)

# Public API - Core Components
from .scanner import PatternScanner
from .engine import (
    ScanEngine,
    ScanResult,
    ScanSummary,
    ProgressTracker,
    filter_results,
    rank_results
)
from .universe import (
    StockUniverse,
    UniverseManager,
    create_custom_universe
)

# Public API - Factory (recommended entry point)
from .factory import (
    ScannerFactory,
    create_scanner
)

# Define public interface
__all__ = [
    # Configuration
    "ScannerConfig",
    "get_default_config",
    "set_default_config",
    # Core components
    "PatternScanner",
    "ScanEngine",
    "ScanResult",
    "ScanSummary",
    "ProgressTracker",
    "filter_results",
    "rank_results",
    # Universe management
    "StockUniverse",
    "UniverseManager",
    "create_custom_universe",
    # Factory (recommended)
    "ScannerFactory",
    "create_scanner",
]

# Version
__version__ = "0.1.0"
