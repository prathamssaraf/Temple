"""API routes for pattern matching."""

from fastapi import APIRouter, HTTPException, status
from typing import List
import logging

from ..models.pattern import PatternMatchRequest, PatternMatchResponse
from ..services import get_temple_service


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/patterns", tags=["patterns"])


@router.post(
    "/match",
    response_model=PatternMatchResponse,
    status_code=status.HTTP_200_OK,
    summary="Match pattern against a symbol",
    description="Analyze a single stock symbol to find pattern matches"
)
async def match_pattern(request: PatternMatchRequest) -> PatternMatchResponse:
    """
    Match a pattern against a single stock symbol.

    - **symbol**: Stock ticker symbol (e.g., "AAPL")
    - **pattern**: Pattern definition with sequence and frequency
    - **lookback_days**: Number of days of historical data to analyze

    Returns the match result with confidence score and occurrence details.
    """
    try:
        service = get_temple_service()
        result = service.match_pattern(
            symbol=request.symbol,
            pattern=request.pattern,
            lookback_days=request.lookback_days
        )
        return result

    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error matching pattern: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during pattern matching"
        )


@router.get(
    "/examples",
    response_model=List[dict],
    summary="Get example patterns",
    description="Get a list of example pattern definitions"
)
async def get_example_patterns() -> List[dict]:
    """
    Get example pattern definitions.

    Returns a list of pre-configured pattern examples that can be used
    as templates for creating custom patterns.
    """
    examples = [
        {
            "name": "Mean Reversion",
            "description": "Price deviates significantly from average and returns",
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
        },
        {
            "name": "Support Bounce",
            "description": "Price touches support level and bounces up",
            "sequence": [
                {
                    "event": {
                        "event_type": "price_touches",
                        "parameters": {"indicator": "support", "tolerance": 0.02}
                    }
                },
                {
                    "event": {
                        "event_type": "price_rises_by",
                        "parameters": {"percentage": 5.0}
                    },
                    "min_interval_days": 1,
                    "max_interval_days": 10
                }
            ],
            "frequency": {
                "min_occurrences": 2,
                "timeframe_days": 90
            }
        },
        {
            "name": "Volatility Cycle",
            "description": "Periods of high volatility followed by consolidation",
            "sequence": [
                {
                    "event": {
                        "event_type": "volatility_spike",
                        "parameters": {"threshold": 2.0}
                    }
                },
                {
                    "event": {
                        "event_type": "volatility_drop",
                        "parameters": {"threshold": 0.5}
                    },
                    "min_interval_days": 5,
                    "max_interval_days": 30
                }
            ],
            "frequency": {
                "min_occurrences": 3,
                "timeframe_days": 180
            }
        }
    ]
    return examples
