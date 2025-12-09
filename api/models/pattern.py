"""Pydantic models for pattern-related API endpoints."""

from pydantic import BaseModel, Field
from typing import List, Optional


class EventDefinitionModel(BaseModel):
    """Event definition for pattern matching."""
    event_type: str = Field(..., description="Type of event (price_crosses_above, price_rises_by, etc.)")
    parameters: dict = Field(..., description="Event-specific parameters")


class SequenceStepModel(BaseModel):
    """Sequence step for pattern definition."""
    event: EventDefinitionModel
    min_interval_days: Optional[int] = Field(None, description="Minimum days after previous step")
    max_interval_days: Optional[int] = Field(None, description="Maximum days after previous step")


class FrequencyConstraintModel(BaseModel):
    """Frequency constraint for pattern occurrences."""
    min_occurrences: int = Field(1, description="Minimum number of times pattern must occur")
    timeframe_days: int = Field(30, description="Timeframe in days")


class PatternDefinitionRequest(BaseModel):
    """Request model for creating a pattern definition."""
    name: str = Field(..., description="Pattern name", min_length=1, max_length=100)
    description: str = Field(..., description="Pattern description", max_length=500)
    sequence: List[SequenceStepModel] = Field(..., description="Sequence of events")
    frequency: FrequencyConstraintModel = Field(..., description="Frequency constraint")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mean Reversion",
                "description": "Price deviates from average and returns",
                "sequence": [
                    {
                        "event": {
                            "event_type": "price_rises_by",
                            "parameters": {"percentage": 10.0}
                        }
                    },
                    {
                        "event": {
                            "event_type": "price_crosses_below",
                            "parameters": {"indicator": "sma", "period": 20}
                        },
                        "min_interval_days": 1,
                        "max_interval_days": 30
                    }
                ],
                "frequency": {
                    "min_occurrences": 3,
                    "timeframe_days": 180
                }
            }
        }


class PatternDefinitionResponse(BaseModel):
    """Response model for pattern definition."""
    id: str = Field(..., description="Pattern ID")
    name: str
    description: str
    created_at: str


class PatternMatchRequest(BaseModel):
    """Request model for matching a pattern against a symbol."""
    symbol: str = Field(..., description="Stock symbol", min_length=1, max_length=10)
    pattern: PatternDefinitionRequest
    lookback_days: int = Field(365, description="Days of historical data to analyze", ge=30, le=3650)

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "pattern": {
                    "name": "Mean Reversion",
                    "description": "Price deviates and returns",
                    "sequence": [],
                    "frequency": {"min_occurrences": 3, "timeframe_days": 180}
                },
                "lookback_days": 365
            }
        }


class OccurrenceDetail(BaseModel):
    """Details of a single pattern occurrence."""
    start_date: str
    end_date: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class PatternMatchResponse(BaseModel):
    """Response model for pattern matching result."""
    symbol: str
    pattern_name: str
    matched: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    occurrences: int
    occurrence_details: List[OccurrenceDetail]
    timeframe_start: str
    timeframe_end: str

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "pattern_name": "Mean Reversion",
                "matched": True,
                "confidence": 0.85,
                "occurrences": 5,
                "occurrence_details": [
                    {
                        "start_date": "2024-01-15",
                        "end_date": "2024-02-10",
                        "confidence": 0.87
                    }
                ],
                "timeframe_start": "2024-01-01",
                "timeframe_end": "2024-12-31"
            }
        }
