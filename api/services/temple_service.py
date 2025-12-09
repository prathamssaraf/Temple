"""Service layer integrating Temple components."""

import logging
from typing import Optional
from dataclasses import asdict

# Temple component imports (will work when components are merged)
try:
    from data import create_data_repository
    from patterns import create_pattern_matcher, PatternDefinition, EventDefinition, SequenceStep, FrequencyConstraint
    from scanner import create_scanner, ScannerConfig
    DATA_AVAILABLE = True
except ImportError:
    DATA_AVAILABLE = False

from ..models.pattern import PatternDefinitionRequest, PatternMatchResponse, OccurrenceDetail
from ..models.scan import ScanRequest, ScanResponse, ScanResultItem, UniverseInfo


logger = logging.getLogger(__name__)


class TempleService:
    """Service for Temple pattern detection and scanning."""

    def __init__(self):
        """Initialize Temple service with all components."""
        if not DATA_AVAILABLE:
            logger.warning("Temple components not available - using mock mode")
            self.data_repo = None
            self.pattern_matcher = None
            self.scanner = None
        else:
            self.data_repo = create_data_repository()
            self.pattern_matcher = create_pattern_matcher()
            self.scanner = create_scanner(
                data_fetcher=self.data_repo.get_ohlcv,
                pattern_matcher=self.pattern_matcher
            )

    def _convert_api_pattern_to_temple(self, api_pattern: PatternDefinitionRequest) -> 'PatternDefinition':
        """Convert API pattern model to Temple PatternDefinition."""
        if not DATA_AVAILABLE:
            raise RuntimeError("Temple components not available")

        # Convert sequence steps
        sequence = []
        for step in api_pattern.sequence:
            event = EventDefinition(
                event_type=step.event.event_type,
                parameters=step.event.parameters
            )
            sequence.append(SequenceStep(
                event=event,
                min_interval_days=step.min_interval_days,
                max_interval_days=step.max_interval_days
            ))

        # Convert frequency
        frequency = FrequencyConstraint(
            min_occurrences=api_pattern.frequency.min_occurrences,
            timeframe_days=api_pattern.frequency.timeframe_days
        )

        return PatternDefinition(
            name=api_pattern.name,
            description=api_pattern.description,
            sequence=sequence,
            frequency=frequency
        )

    def match_pattern(
        self,
        symbol: str,
        pattern: PatternDefinitionRequest,
        lookback_days: int = 365
    ) -> PatternMatchResponse:
        """
        Match a pattern against a single symbol.

        Args:
            symbol: Stock symbol
            pattern: Pattern definition
            lookback_days: Days of historical data to analyze

        Returns:
            Pattern match result
        """
        if not DATA_AVAILABLE:
            # Mock response for development
            return PatternMatchResponse(
                symbol=symbol,
                pattern_name=pattern.name,
                matched=True,
                confidence=0.75,
                occurrences=3,
                occurrence_details=[
                    OccurrenceDetail(
                        start_date="2024-01-15",
                        end_date="2024-02-10",
                        confidence=0.80
                    ),
                    OccurrenceDetail(
                        start_date="2024-03-20",
                        end_date="2024-04-15",
                        confidence=0.72
                    ),
                    OccurrenceDetail(
                        start_date="2024-06-01",
                        end_date="2024-06-25",
                        confidence=0.73
                    )
                ],
                timeframe_start="2024-01-01",
                timeframe_end="2024-12-31"
            )

        # Convert API pattern to Temple pattern
        temple_pattern = self._convert_api_pattern_to_temple(pattern)

        # Fetch data
        df = self.data_repo.get_ohlcv(symbol, lookback_days=lookback_days)

        # Match pattern
        match_result = self.pattern_matcher.match(df, temple_pattern)

        # Convert to API response
        occurrence_details = [
            OccurrenceDetail(
                start_date=str(occ.start_date),
                end_date=str(occ.end_date),
                confidence=occ.confidence
            )
            for occ in match_result.occurrences
        ]

        return PatternMatchResponse(
            symbol=symbol,
            pattern_name=match_result.pattern_name,
            matched=match_result.matched,
            confidence=match_result.confidence,
            occurrences=match_result.occurrence_count,
            occurrence_details=occurrence_details,
            timeframe_start=str(df.index[0]),
            timeframe_end=str(df.index[-1])
        )

    def scan_stocks(self, request: ScanRequest) -> ScanResponse:
        """
        Scan multiple stocks for pattern matches.

        Args:
            request: Scan request with symbols/universe and pattern

        Returns:
            Scan results summary
        """
        if not DATA_AVAILABLE:
            # Mock response for development
            return ScanResponse(
                total_symbols=3 if request.symbols else 10,
                successful_scans=3 if request.symbols else 10,
                failed_scans=0,
                matches_found=2,
                average_confidence=0.78,
                duration_seconds=1.5,
                results=[
                    ScanResultItem(
                        symbol="AAPL",
                        pattern_name=request.pattern.name,
                        matched=True,
                        confidence=0.85,
                        occurrences=5,
                        timeframe_start="2024-01-01",
                        timeframe_end="2024-12-31"
                    ),
                    ScanResultItem(
                        symbol="MSFT",
                        pattern_name=request.pattern.name,
                        matched=True,
                        confidence=0.72,
                        occurrences=3,
                        timeframe_start="2024-01-01",
                        timeframe_end="2024-12-31"
                    )
                ]
            )

        # Convert API pattern to Temple pattern
        temple_pattern = self._convert_api_pattern_to_temple(request.pattern)

        # Configure scanner
        if request.parallel:
            config = ScannerConfig(parallel=True, max_workers=4)
            scanner = create_scanner(
                data_fetcher=self.data_repo.get_ohlcv,
                pattern_matcher=self.pattern_matcher,
                config=config
            )
        else:
            scanner = self.scanner

        # Scan stocks
        if request.universe:
            results = scanner.scan_universe(
                universe_name=request.universe,
                pattern=temple_pattern,
                min_confidence=request.min_confidence
            )
        elif request.symbols:
            results = scanner.scan(
                symbols=request.symbols,
                pattern=temple_pattern,
                min_confidence=request.min_confidence
            )
        else:
            raise ValueError("Must provide either 'symbols' or 'universe'")

        # Convert to API response
        result_items = [
            ScanResultItem(
                symbol=r.symbol,
                pattern_name=r.pattern_name,
                matched=r.matched,
                confidence=r.confidence,
                occurrences=r.occurrences,
                timeframe_start=r.timeframe_start,
                timeframe_end=r.timeframe_end
            )
            for r in results.results
        ]

        return ScanResponse(
            total_symbols=results.total_symbols,
            successful_scans=results.successful_scans,
            failed_scans=results.failed_scans,
            matches_found=results.matches_found,
            average_confidence=results.average_confidence,
            duration_seconds=results.duration_seconds,
            results=result_items
        )

    def list_universes(self) -> list[UniverseInfo]:
        """List available stock universes."""
        if not DATA_AVAILABLE:
            # Mock universes for development
            return [
                UniverseInfo(name="sp500", description="S&P 500 Index", symbol_count=500),
                UniverseInfo(name="nasdaq100", description="NASDAQ-100 Index", symbol_count=100),
                UniverseInfo(name="tech", description="Major Technology Stocks", symbol_count=20)
            ]

        universe_names = self.scanner.list_universes()
        universes = []

        # Map universe names to descriptions
        descriptions = {
            "sp500": "S&P 500 Index",
            "nasdaq100": "NASDAQ-100 Index",
            "tech": "Major Technology Stocks"
        }

        for name in universe_names:
            universe = self.scanner.universe_manager.get_universe(name)
            universes.append(UniverseInfo(
                name=name,
                description=descriptions.get(name, ""),
                symbol_count=len(universe.symbols) if universe else 0
            ))

        return universes


# Global service instance
_service: Optional[TempleService] = None


def get_temple_service() -> TempleService:
    """Get the Temple service instance."""
    global _service
    if _service is None:
        _service = TempleService()
    return _service
