"""
Pattern scanning engine for Temple.

This module scans multiple stocks for pattern matches in batch.
"""

import pandas as pd
from typing import List, Optional, Callable, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed


logger = logging.getLogger(__name__)


@dataclass
class ScanResult:
    """Result from scanning a single stock for a pattern."""

    symbol: str
    pattern_name: str
    matched: bool
    confidence: float
    occurrences: int
    timeframe_start: str
    timeframe_end: str
    scan_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "symbol": self.symbol,
            "pattern_name": self.pattern_name,
            "matched": self.matched,
            "confidence": self.confidence,
            "occurrences": self.occurrences,
            "timeframe_start": self.timeframe_start,
            "timeframe_end": self.timeframe_end,
            "scan_timestamp": self.scan_timestamp,
            "error": self.error,
            "metadata": self.metadata
        }


@dataclass
class ScanSummary:
    """Summary of a complete scan operation."""

    total_symbols: int
    successful_scans: int
    failed_scans: int
    matches_found: int
    average_confidence: float
    duration_seconds: float
    results: List[ScanResult]


class ProgressTracker:
    """Tracks progress during batch scanning."""

    def __init__(self, total: int, callback: Optional[Callable[[int, int, str], None]] = None):
        self.total = total
        self.completed = 0
        self.callback = callback

    def update(self, symbol: str):
        """Update progress with completed symbol."""
        self.completed += 1
        if self.callback:
            self.callback(self.completed, self.total, symbol)
        else:
            logger.info(f"Progress: {self.completed}/{self.total} - Scanned {symbol}")

    def get_percentage(self) -> float:
        """Get completion percentage."""
        return (self.completed / self.total * 100) if self.total > 0 else 0


class ScanEngine:
    """
    Core scanning engine that applies patterns across multiple stocks.

    This engine handles:
    - Batch data fetching
    - Pattern matching across stocks
    - Progress tracking
    - Error handling
    - Parallel processing (optional)
    """

    def __init__(
        self,
        data_fetcher: Callable[[str], pd.DataFrame],
        pattern_matcher: Any,  # PatternMatcher from patterns module
        parallel: bool = False,
        max_workers: int = 4
    ):
        """
        Initialize scan engine.

        Args:
            data_fetcher: Function to fetch OHLCV data for a symbol
            pattern_matcher: PatternMatcher instance from patterns module
            parallel: Whether to use parallel processing
            max_workers: Number of parallel workers
        """
        self.data_fetcher = data_fetcher
        self.pattern_matcher = pattern_matcher
        self.parallel = parallel
        self.max_workers = max_workers

    def scan_symbol(
        self,
        symbol: str,
        pattern: Any,  # PatternDefinition
        min_confidence: float = 0.0
    ) -> ScanResult:
        """
        Scan a single symbol for pattern matches.

        Args:
            symbol: Stock symbol to scan
            pattern: Pattern definition to match
            min_confidence: Minimum confidence threshold

        Returns:
            ScanResult with match information
        """
        try:
            # Fetch data
            df = self.data_fetcher(symbol)

            if df is None or df.empty:
                return ScanResult(
                    symbol=symbol,
                    pattern_name=pattern.name,
                    matched=False,
                    confidence=0.0,
                    occurrences=0,
                    timeframe_start="",
                    timeframe_end="",
                    error="No data available"
                )

            # Match pattern
            match = self.pattern_matcher.match(df, symbol, pattern)

            # Determine if matched based on confidence
            matched = match.confidence >= min_confidence

            return ScanResult(
                symbol=symbol,
                pattern_name=pattern.name,
                matched=matched,
                confidence=match.confidence,
                occurrences=match.count,
                timeframe_start=match.timeframe_start,
                timeframe_end=match.timeframe_end,
                metadata={
                    "pattern_description": pattern.description,
                    "min_confidence_threshold": min_confidence
                }
            )

        except Exception as e:
            logger.error(f"Error scanning {symbol}: {e}")
            return ScanResult(
                symbol=symbol,
                pattern_name=pattern.name,
                matched=False,
                confidence=0.0,
                occurrences=0,
                timeframe_start="",
                timeframe_end="",
                error=str(e)
            )

    def scan_batch(
        self,
        symbols: List[str],
        pattern: Any,
        min_confidence: float = 0.5,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> ScanSummary:
        """
        Scan multiple symbols for pattern matches.

        Args:
            symbols: List of stock symbols
            pattern: Pattern definition to match
            min_confidence: Minimum confidence threshold
            progress_callback: Optional callback for progress updates

        Returns:
            ScanSummary with results
        """
        start_time = datetime.now()
        tracker = ProgressTracker(len(symbols), progress_callback)

        results: List[ScanResult] = []

        if self.parallel and len(symbols) > 1:
            # Parallel scanning
            results = self._scan_parallel(symbols, pattern, min_confidence, tracker)
        else:
            # Sequential scanning
            results = self._scan_sequential(symbols, pattern, min_confidence, tracker)

        # Calculate summary statistics
        duration = (datetime.now() - start_time).total_seconds()
        successful = sum(1 for r in results if r.error is None)
        failed = len(results) - successful
        matches = sum(1 for r in results if r.matched)
        avg_confidence = sum(r.confidence for r in results) / len(results) if results else 0.0

        summary = ScanSummary(
            total_symbols=len(symbols),
            successful_scans=successful,
            failed_scans=failed,
            matches_found=matches,
            average_confidence=avg_confidence,
            duration_seconds=duration,
            results=results
        )

        logger.info(
            f"Scan complete: {matches}/{len(symbols)} matches found in {duration:.2f}s"
        )

        return summary

    def _scan_sequential(
        self,
        symbols: List[str],
        pattern: Any,
        min_confidence: float,
        tracker: ProgressTracker
    ) -> List[ScanResult]:
        """Scan symbols sequentially."""
        results = []
        for symbol in symbols:
            result = self.scan_symbol(symbol, pattern, min_confidence)
            results.append(result)
            tracker.update(symbol)
        return results

    def _scan_parallel(
        self,
        symbols: List[str],
        pattern: Any,
        min_confidence: float,
        tracker: ProgressTracker
    ) -> List[ScanResult]:
        """Scan symbols in parallel."""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_symbol = {
                executor.submit(self.scan_symbol, symbol, pattern, min_confidence): symbol
                for symbol in symbols
            }

            # Collect results as they complete
            for future in as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    result = future.result()
                    results.append(result)
                    tracker.update(symbol)
                except Exception as e:
                    logger.error(f"Failed to scan {symbol}: {e}")
                    results.append(ScanResult(
                        symbol=symbol,
                        pattern_name=pattern.name,
                        matched=False,
                        confidence=0.0,
                        occurrences=0,
                        timeframe_start="",
                        timeframe_end="",
                        error=str(e)
                    ))

        return results


def filter_results(
    results: List[ScanResult],
    min_confidence: Optional[float] = None,
    min_occurrences: Optional[int] = None,
    matched_only: bool = True
) -> List[ScanResult]:
    """
    Filter scan results based on criteria.

    Args:
        results: List of scan results
        min_confidence: Minimum confidence threshold
        min_occurrences: Minimum number of pattern occurrences
        matched_only: Only return matched results

    Returns:
        Filtered list of results
    """
    filtered = results

    if matched_only:
        filtered = [r for r in filtered if r.matched]

    if min_confidence is not None:
        filtered = [r for r in filtered if r.confidence >= min_confidence]

    if min_occurrences is not None:
        filtered = [r for r in filtered if r.occurrences >= min_occurrences]

    return filtered


def rank_results(
    results: List[ScanResult],
    sort_by: str = "confidence"
) -> List[ScanResult]:
    """
    Rank scan results by specified criteria.

    Args:
        results: List of scan results
        sort_by: Field to sort by ("confidence", "occurrences")

    Returns:
        Sorted list of results (descending)
    """
    if sort_by == "confidence":
        return sorted(results, key=lambda r: r.confidence, reverse=True)
    elif sort_by == "occurrences":
        return sorted(results, key=lambda r: r.occurrences, reverse=True)
    else:
        return results
