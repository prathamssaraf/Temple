"""Pydantic models for scanner-related API endpoints."""

from pydantic import BaseModel, Field
from typing import List, Optional
from .pattern import PatternDefinitionRequest


class ScanRequest(BaseModel):
    """Request model for scanning stocks."""
    symbols: Optional[List[str]] = Field(None, description="List of stock symbols")
    universe: Optional[str] = Field(None, description="Pre-defined universe name")
    pattern: PatternDefinitionRequest = Field(..., description="Pattern to match")
    min_confidence: float = Field(0.5, description="Minimum confidence threshold", ge=0.0, le=1.0)
    parallel: bool = Field(False, description="Enable parallel processing")

    class Config:
        json_schema_extra = {
            "example": {
                "symbols": ["AAPL", "MSFT", "GOOGL"],
                "pattern": {
                    "name": "Mean Reversion",
                    "description": "Price deviates and returns",
                    "sequence": [],
                    "frequency": {"min_occurrences": 3, "timeframe_days": 180}
                },
                "min_confidence": 0.7,
                "parallel": True
            }
        }


class ScanResultItem(BaseModel):
    """Individual scan result for a symbol."""
    symbol: str
    pattern_name: str
    matched: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    occurrences: int
    timeframe_start: str
    timeframe_end: str


class ScanResponse(BaseModel):
    """Response model for scan results."""
    total_symbols: int
    successful_scans: int
    failed_scans: int
    matches_found: int
    average_confidence: float
    duration_seconds: float
    results: List[ScanResultItem]

    class Config:
        json_schema_extra = {
            "example": {
                "total_symbols": 5,
                "successful_scans": 5,
                "failed_scans": 0,
                "matches_found": 3,
                "average_confidence": 0.75,
                "duration_seconds": 2.5,
                "results": [
                    {
                        "symbol": "AAPL",
                        "pattern_name": "Mean Reversion",
                        "matched": True,
                        "confidence": 0.85,
                        "occurrences": 12,
                        "timeframe_start": "2024-01-01",
                        "timeframe_end": "2024-12-31"
                    }
                ]
            }
        }


class UniverseInfo(BaseModel):
    """Information about a stock universe."""
    name: str
    description: str
    symbol_count: int


class UniverseListResponse(BaseModel):
    """Response model for listing available universes."""
    universes: List[UniverseInfo]

    class Config:
        json_schema_extra = {
            "example": {
                "universes": [
                    {
                        "name": "sp500",
                        "description": "S&P 500 Index",
                        "symbol_count": 500
                    },
                    {
                        "name": "nasdaq100",
                        "description": "NASDAQ-100 Index",
                        "symbol_count": 100
                    },
                    {
                        "name": "tech",
                        "description": "Major Technology Stocks",
                        "symbol_count": 20
                    }
                ]
            }
        }
