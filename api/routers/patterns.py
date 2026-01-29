"""
Pattern API router - endpoints for pattern matching.
Includes pivot-based mean reversion patterns.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from api.services import create_pattern_service

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize pattern service
pattern_service = create_pattern_service()


# Pydantic models for request/response
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


class OccurrenceDetail(BaseModel):
    start_date: str
    end_date: str
    confidence: float


class PatternMatchRequest(BaseModel):
    symbol: str
    pattern: PatternDefinition
    lookback_days: int


class PricePoint(BaseModel):
    date: str
    close: float
    open: float
    high: float
    low: float
    volume: int


class PatternMatchResponse(BaseModel):
    symbol: str
    pattern_name: str
    matched: bool
    confidence: float
    occurrences: int
    occurrence_details: List[OccurrenceDetail]
    timeframe_start: str
    timeframe_end: str
    price_data: Optional[List[PricePoint]] = []

    class Config:
        # Ensure None/empty fields are included in JSON response
        use_enum_values = True


@router.post("/match", response_model=PatternMatchResponse, response_model_exclude_none=False)
async def match_pattern(request: PatternMatchRequest):
    """
    Match a pattern against a single stock symbol using real pattern engine.
    """
    logger.info(f"Matching pattern '{request.pattern.name}' against {request.symbol}")

    try:
        # Convert pattern to dict format for service
        pattern_dict = request.pattern.dict()

        # Call pattern service (this fetches data and runs pattern matching)
        match_result = pattern_service.match_pattern(
            symbol=request.symbol,
            pattern_dict=pattern_dict,
            lookback_days=request.lookback_days
        )

        if match_result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Unable to fetch data for symbol {request.symbol}"
            )

        # Convert occurrences to API format
        occurrences = []
        for occ in match_result.occurrences:
            occurrences.append(OccurrenceDetail(
                start_date=occ['start_date'].strftime("%Y-%m-%d"),
                end_date=occ['end_date'].strftime("%Y-%m-%d"),
                confidence=occ.get('confidence', match_result.confidence)
            ))

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=request.lookback_days)

        # Get price data from pattern service
        from api.services import create_data_fetcher
        data_fetcher = create_data_fetcher()
        df = data_fetcher.get_stock_data(request.symbol, period=f"{request.lookback_days}d")

        price_data = []
        if df is not None and not df.empty:
            for idx, row in df.iterrows():
                price_data.append(PricePoint(
                    date=idx.strftime("%Y-%m-%d"),
                    close=float(row['close']),
                    open=float(row['open']),
                    high=float(row['high']),
                    low=float(row['low']),
                    volume=int(row['volume'])
                ))

        return PatternMatchResponse(
            symbol=request.symbol,
            pattern_name=match_result.pattern_name,
            matched=(match_result.count > 0),
            confidence=round(match_result.confidence, 2),
            occurrences=match_result.count,
            occurrence_details=occurrences,
            timeframe_start=start_date.strftime("%Y-%m-%d"),
            timeframe_end=end_date.strftime("%Y-%m-%d"),
            price_data=price_data
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error matching pattern for {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/examples")
async def get_example_patterns():
    """
    Get example pattern definitions.
    """
    examples = [
        {
            "name": "Support Bounce",
            "description": "Price touches support level and bounces back repeatedly",
            "sequence": [
                {
                    "event": {
                        "event_type": "PRICE_TOUCHES",
                        "parameters": {
                            "reference": "support",
                            "lookback": 90,
                            "tolerance": 1.5
                        }
                    }
                },
                {
                    "event": {
                        "event_type": "PRICE_RISES_BY",
                        "parameters": {
                            "min_change": 3.0
                        }
                    },
                    "max_interval_days": 15
                }
            ],
            "frequency": {
                "min_occurrences": 5,
                "timeframe_days": 180
            }
        },
        {
            "name": "Mean Reversion",
            "description": "Price falls below moving average and returns",
            "sequence": [
                {
                    "event": {
                        "event_type": "PRICE_CROSSES_BELOW",
                        "parameters": {
                            "reference": "SMA20"
                        }
                    }
                },
                {
                    "event": {
                        "event_type": "PRICE_CROSSES_ABOVE",
                        "parameters": {
                            "reference": "SMA20"
                        }
                    },
                    "min_interval_days": 3,
                    "max_interval_days": 30
                }
            ],
            "frequency": {
                "min_occurrences": 8,
                "timeframe_days": 365
            }
        },
        {
            "name": "Volatility Cycle",
            "description": "Large price swings up and down",
            "sequence": [
                {
                    "event": {
                        "event_type": "PRICE_RISES_BY",
                        "parameters": {
                            "min_change": 8.0
                        }
                    }
                },
                {
                    "event": {
                        "event_type": "PRICE_FALLS_BY",
                        "parameters": {
                            "min_change": 8.0
                        }
                    },
                    "max_interval_days": 30
                }
            ],
            "frequency": {
                "min_occurrences": 4,
                "timeframe_days": 180
            }
        },
        {
            "name": "Pivot Mean Reversion (Mode)",
            "description": "Price oscillates around most frequent price level, deviating and returning repeatedly",
            "sequence": [
                {
                    "event": {
                        "event_type": "PIVOT_DEVIATION",
                        "parameters": {
                            "reference": "pivot_mode",
                            "lookback": 365,
                            "tolerance": 5.0
                        }
                    }
                },
                {
                    "event": {
                        "event_type": "PIVOT_RETURN",
                        "parameters": {
                            "reference": "pivot_mode",
                            "lookback": 365,
                            "tolerance": 5.0
                        }
                    },
                    "max_interval_days": 28
                }
            ],
            "frequency": {
                "min_occurrences": 8,
                "timeframe_days": 365
            }
        },
        {
            "name": "Pivot Mean Reversion (Median)",
            "description": "Price oscillates around median price level with consistent returns",
            "sequence": [
                {
                    "event": {
                        "event_type": "PIVOT_DEVIATION",
                        "parameters": {
                            "reference": "pivot_median",
                            "lookback": 365,
                            "tolerance": 5.0
                        }
                    }
                },
                {
                    "event": {
                        "event_type": "PIVOT_RETURN",
                        "parameters": {
                            "reference": "pivot_median",
                            "lookback": 365,
                            "tolerance": 5.0
                        }
                    },
                    "max_interval_days": 28
                }
            ],
            "frequency": {
                "min_occurrences": 8,
                "timeframe_days": 365
            }
        },
        {
            "name": "Pivot Mean Reversion (Volume)",
            "description": "Price oscillates around volume-weighted pivot point",
            "sequence": [
                {
                    "event": {
                        "event_type": "PIVOT_DEVIATION",
                        "parameters": {
                            "reference": "pivot_volume",
                            "lookback": 365,
                            "tolerance": 5.0
                        }
                    }
                },
                {
                    "event": {
                        "event_type": "PIVOT_RETURN",
                        "parameters": {
                            "reference": "pivot_volume",
                            "lookback": 365,
                            "tolerance": 5.0
                        }
                    },
                    "max_interval_days": 28
                }
            ],
            "frequency": {
                "min_occurrences": 8,
                "timeframe_days": 365
            }
        },
        {
            "name": "Pivot Mean Reversion (Custom)",
            "description": "Price oscillates around user-specified price level (e.g., $150)",
            "sequence": [
                {
                    "event": {
                        "event_type": "PIVOT_DEVIATION",
                        "parameters": {
                            "reference": "fixed",
                            "value": 150.0,
                            "tolerance": 5.0
                        }
                    }
                },
                {
                    "event": {
                        "event_type": "PIVOT_RETURN",
                        "parameters": {
                            "reference": "fixed",
                            "value": 150.0,
                            "tolerance": 5.0
                        }
                    },
                    "max_interval_days": 28
                }
            ],
            "frequency": {
                "min_occurrences": 8,
                "timeframe_days": 365
            }
        }
    ]

    return {"patterns": examples}
