"""
Main scanner class for Temple.

This module provides the high-level API for scanning stocks for patterns.
"""

import pandas as pd
from typing import List, Optional, Callable, Any
import logging

from .engine import ScanEngine, ScanSummary, ScanResult, filter_results, rank_results
from .universe import StockUniverse, UniverseManager


logger = logging.getLogger(__name__)


class PatternScanner:
    """
    Main scanner for finding pattern matches across multiple stocks.

    This is the primary interface for the scanner layer.
    """

    def __init__(
        self,
        data_fetcher: Callable[[str], pd.DataFrame],
        pattern_matcher: Any,
        parallel: bool = False,
        max_workers: int = 4
    ):
        """
        Initialize pattern scanner.

        Args:
            data_fetcher: Function to fetch OHLCV data for a symbol
            pattern_matcher: PatternMatcher instance from patterns module
            parallel: Whether to use parallel processing
            max_workers: Number of parallel workers
        """
        self.data_fetcher = data_fetcher
        self.pattern_matcher = pattern_matcher
        self.engine = ScanEngine(data_fetcher, pattern_matcher, parallel, max_workers)
        self.universe_manager = UniverseManager()

    def scan(
        self,
        symbols: List[str],
        pattern: Any,
        min_confidence: float = 0.5,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> ScanSummary:
        """
        Scan symbols for pattern matches.

        Args:
            symbols: List of stock symbols to scan
            pattern: Pattern definition to match
            min_confidence: Minimum confidence threshold (0.0 to 1.0)
            progress_callback: Optional callback(completed, total, symbol) for progress

        Returns:
            ScanSummary with results

        Example:
            ```python
            scanner = create_scanner()
            results = scanner.scan(
                symbols=["AAPL", "MSFT", "GOOGL"],
                pattern=my_pattern,
                min_confidence=0.7
            )
            ```
        """
        logger.info(f"Starting scan: {len(symbols)} symbols, pattern '{pattern.name}'")

        summary = self.engine.scan_batch(
            symbols=symbols,
            pattern=pattern,
            min_confidence=min_confidence,
            progress_callback=progress_callback
        )

        return summary

    def scan_universe(
        self,
        universe_name: str,
        pattern: Any,
        min_confidence: float = 0.5,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> ScanSummary:
        """
        Scan a pre-defined universe for pattern matches.

        Args:
            universe_name: Name of universe ("sp500", "nasdaq100", "tech")
            pattern: Pattern definition to match
            min_confidence: Minimum confidence threshold
            progress_callback: Progress callback

        Returns:
            ScanSummary with results

        Example:
            ```python
            scanner = create_scanner()
            results = scanner.scan_universe(
                universe_name="sp500",
                pattern=mean_reversion_pattern,
                min_confidence=0.7
            )
            ```
        """
        universe = self.universe_manager.get_universe(universe_name)

        if not universe:
            raise ValueError(f"Unknown universe: {universe_name}")

        logger.info(f"Scanning universe '{universe.name}' ({len(universe)} symbols)")

        return self.scan(
            symbols=list(universe.symbols),
            pattern=pattern,
            min_confidence=min_confidence,
            progress_callback=progress_callback
        )

    def get_best_matches(
        self,
        summary: ScanSummary,
        top_n: int = 10,
        sort_by: str = "confidence"
    ) -> List[ScanResult]:
        """
        Get top N matches from scan results.

        Args:
            summary: Scan summary with results
            top_n: Number of top results to return
            sort_by: Ranking criteria ("confidence" or "occurrences")

        Returns:
            List of top scan results
        """
        # Filter to matched only
        matched = filter_results(summary.results, matched_only=True)

        # Rank by criteria
        ranked = rank_results(matched, sort_by=sort_by)

        # Return top N
        return ranked[:top_n]

    def list_universes(self) -> List[str]:
        """List available stock universes."""
        return self.universe_manager.list_universes()

    def create_custom_universe(
        self,
        name: str,
        symbols: List[str]
    ) -> StockUniverse:
        """
        Create a custom stock universe.

        Args:
            name: Name for the universe
            symbols: List of stock symbols

        Returns:
            Created StockUniverse
        """
        return self.universe_manager.create_universe(name, symbols)

    def export_results(
        self,
        summary: ScanSummary,
        format: str = "dict"
    ) -> Any:
        """
        Export scan results in different formats.

        Args:
            summary: Scan summary with results
            format: Export format ("dict", "json", "csv")

        Returns:
            Exported data in requested format
        """
        if format == "dict":
            return {
                "summary": {
                    "total_symbols": summary.total_symbols,
                    "successful_scans": summary.successful_scans,
                    "failed_scans": summary.failed_scans,
                    "matches_found": summary.matches_found,
                    "average_confidence": summary.average_confidence,
                    "duration_seconds": summary.duration_seconds
                },
                "results": [r.to_dict() for r in summary.results]
            }
        elif format == "json":
            import json
            return json.dumps(self.export_results(summary, "dict"), indent=2)
        elif format == "csv":
            import csv
            import io
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=[
                "symbol", "pattern_name", "matched", "confidence",
                "occurrences", "timeframe_start", "timeframe_end"
            ])
            writer.writeheader()
            for result in summary.results:
                writer.writerow({
                    "symbol": result.symbol,
                    "pattern_name": result.pattern_name,
                    "matched": result.matched,
                    "confidence": result.confidence,
                    "occurrences": result.occurrences,
                    "timeframe_start": result.timeframe_start,
                    "timeframe_end": result.timeframe_end
                })
            return output.getvalue()
        else:
            raise ValueError(f"Unknown format: {format}")
