"""
Scanner API router - endpoints for scanning multiple stocks.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import time
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

from api.services import create_pattern_service
from api.data import get_universe_tickers, UNIVERSE_MAP

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize pattern service
pattern_service = create_pattern_service()

# Thread pool for parallel scanning
executor = ThreadPoolExecutor(max_workers=10)


# Pydantic models
class EventDefinition(BaseModel):
    event_type: str
    parameters: Dict[str, Any]


class SequenceStep(BaseModel):
    event: EventDefinition
    min_interval_days: Optional[int] = None
    max_interval_days: Optional[int] = None


class FrequencyConstraint(BaseModel):
    min_occurrences: int
    timeframe_days: int


class PatternDefinition(BaseModel):
    name: str
    description: str
    sequence: List[SequenceStep]
    frequency: FrequencyConstraint


class ScanRequest(BaseModel):
    symbols: Optional[List[str]] = None
    universe: Optional[str] = None
    pattern: PatternDefinition
    min_confidence: float
    parallel: bool
    lookback_days: int = 365  # Default to 1 year


class ScanResultItem(BaseModel):
    symbol: str
    pattern_name: str
    matched: bool
    confidence: float
    occurrences: int
    timeframe_start: str
    timeframe_end: str


class ScanResponse(BaseModel):
    total_symbols: int
    successful_scans: int
    failed_scans: int
    matches_found: int
    average_confidence: float
    duration_seconds: float
    results: List[ScanResultItem]


class UniverseInfo(BaseModel):
    name: str
    description: str
    symbol_count: int


class UniverseListResponse(BaseModel):
    universes: List[UniverseInfo]


def scan_single_stock(symbol: str, pattern_dict: dict, min_confidence: float, lookback_days: int = 365) -> Optional[ScanResultItem]:
    """
    Scan a single stock for a pattern. Used in thread pool.

    Args:
        symbol: Stock ticker
        pattern_dict: Pattern definition
        min_confidence: Minimum confidence threshold
        lookback_days: Number of days to analyze

    Returns:
        ScanResultItem if match found, None otherwise
    """
    try:
        logger.info(f"Scanning {symbol}...")

        # Match pattern against stock
        match_result = pattern_service.match_pattern(
            symbol=symbol,
            pattern_dict=pattern_dict,
            lookback_days=lookback_days
        )

        if match_result is None:
            logger.warning(f"No data available for {symbol}")
            return None

        # Check if pattern matched and meets confidence threshold
        # PatternMatch doesn't have 'matched' attribute, so check count > 0
        if match_result.count > 0 and match_result.confidence >= min_confidence:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=lookback_days)

            logger.info(
                f"{symbol}: MATCH with {match_result.confidence:.2f} confidence, "
                f"{match_result.count} occurrences"
            )

            return ScanResultItem(
                symbol=symbol,
                pattern_name=match_result.pattern_name,
                matched=True,
                confidence=round(match_result.confidence, 2),
                occurrences=match_result.count,
                timeframe_start=start_date.strftime("%Y-%m-%d"),
                timeframe_end=end_date.strftime("%Y-%m-%d")
            )
        else:
            logger.info(
                f"{symbol}: No match "
                f"(confidence: {match_result.confidence:.2f}, "
                f"count: {match_result.count})"
            )
            return None

    except Exception as e:
        logger.error(f"Error scanning {symbol}: {e}")
        return None


@router.post("/scan", response_model=ScanResponse)
async def scan_stocks(request: ScanRequest):
    """
    Scan multiple stocks for a pattern using real pattern engine.

    This endpoint:
    1. Fetches stock data for each symbol (yfinance)
    2. Runs pattern detection (patterns engine)
    3. Aggregates and ranks results
    """
    start_time = time.time()
    logger.info(f"Starting scan for pattern '{request.pattern.name}'")

    # Get symbols to scan
    if request.symbols:
        symbols = request.symbols
    elif request.universe:
        # Use predefined universe
        symbols = get_universe_symbols(request.universe)
    else:
        raise HTTPException(status_code=400, detail="Must provide either symbols or universe")

    logger.info(f"Scanning {len(symbols)} symbols (parallel={request.parallel})")

    # Convert pattern to dict format
    pattern_dict = request.pattern.dict()

    results = []
    successful_scans = 0
    failed_scans = 0

    if request.parallel:
        # Parallel scanning using thread pool
        futures = {
            executor.submit(scan_single_stock, symbol, pattern_dict, request.min_confidence, request.lookback_days): symbol
            for symbol in symbols
        }

        for future in as_completed(futures):
            symbol = futures[future]
            try:
                result = future.result()
                if result is not None:
                    results.append(result)
                successful_scans += 1
            except Exception as e:
                logger.error(f"Failed to scan {symbol}: {e}")
                failed_scans += 1
    else:
        # Sequential scanning
        for symbol in symbols:
            result = scan_single_stock(symbol, pattern_dict, request.min_confidence, request.lookback_days)
            if result is not None:
                results.append(result)
                successful_scans += 1
            else:
                successful_scans += 1  # Count as successful even if no match

    # Sort results by confidence descending
    results.sort(key=lambda x: x.confidence, reverse=True)

    duration = time.time() - start_time
    matches_found = len(results)
    avg_confidence = sum(r.confidence for r in results) / len(results) if results else 0

    logger.info(
        f"Scan complete: {matches_found} matches found in {duration:.2f}s "
        f"({successful_scans} successful, {failed_scans} failed)"
    )

    return ScanResponse(
        total_symbols=len(symbols),
        successful_scans=successful_scans,
        failed_scans=failed_scans,
        matches_found=matches_found,
        average_confidence=round(avg_confidence, 2),
        duration_seconds=round(duration, 2),
        results=results
    )


@router.get("/universes", response_model=UniverseListResponse)
async def get_universes():
    """
    Get available stock universes with accurate counts.
    """
    universe_descriptions = {
        "sp500": "S&P 500 companies",
        "tech": "Technology sector stocks",
        "energy": "Energy sector stocks",
        "healthcare": "Healthcare sector stocks",
        "finance": "Financial sector stocks",
        "consumer": "Consumer goods and services",
        "defensive": "Defensive stocks (utilities, staples, healthcare)",
        "growth": "High-growth stocks (tech and consumer)"
    }

    universes = []
    for name, tickers in UNIVERSE_MAP.items():
        universes.append(UniverseInfo(
            name=name,
            description=universe_descriptions.get(name, f"{name.title()} stocks"),
            symbol_count=len(tickers)
        ))

    return UniverseListResponse(universes=universes)


@router.get("/health")
async def scanner_health():
    """
    Health check for scanner service.
    """
    return {
        "status": "healthy",
        "data_layer_connected": False,
        "mode": "mock"
    }


def get_universe_symbols(universe: str) -> List[str]:
    """
    Get symbols for a given universe.
    Returns comprehensive ticker lists from universe data.
    """
    return get_universe_tickers(universe)
