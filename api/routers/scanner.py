"""API routes for stock scanning."""

from fastapi import APIRouter, HTTPException, status
import logging

from ..models.scan import ScanRequest, ScanResponse, UniverseListResponse
from ..services import get_temple_service


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/scanner", tags=["scanner"])


@router.post(
    "/scan",
    response_model=ScanResponse,
    status_code=status.HTTP_200_OK,
    summary="Scan stocks for pattern matches",
    description="Scan multiple stocks or a universe for pattern matches"
)
async def scan_stocks(request: ScanRequest) -> ScanResponse:
    """
    Scan multiple stocks for pattern matches.

    You must provide either:
    - **symbols**: List of stock ticker symbols
    - **universe**: Name of a pre-defined universe (e.g., "sp500", "nasdaq100", "tech")

    Additional parameters:
    - **pattern**: Pattern definition to match
    - **min_confidence**: Minimum confidence threshold (0.0-1.0)
    - **parallel**: Enable parallel processing for faster results

    Returns scan summary with all matches.
    """
    try:
        # Validate input
        if not request.symbols and not request.universe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Must provide either 'symbols' or 'universe'"
            )

        if request.symbols and request.universe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot provide both 'symbols' and 'universe'"
            )

        service = get_temple_service()
        result = service.scan_stocks(request)
        return result

    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error scanning stocks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during scanning"
        )


@router.get(
    "/universes",
    response_model=UniverseListResponse,
    summary="List available stock universes",
    description="Get a list of all pre-defined stock universes"
)
async def list_universes() -> UniverseListResponse:
    """
    List all available stock universes.

    Returns information about each universe including name,
    description, and number of symbols.
    """
    try:
        service = get_temple_service()
        universes = service.list_universes()
        return UniverseListResponse(universes=universes)

    except Exception as e:
        logger.error(f"Error listing universes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error listing universes"
        )


@router.get(
    "/health",
    summary="Health check",
    description="Check if the scanner service is healthy"
)
async def health_check():
    """
    Health check endpoint.

    Returns service status and component availability.
    """
    try:
        service = get_temple_service()

        # Check if components are available
        from ..services.temple_service import DATA_AVAILABLE

        return {
            "status": "healthy",
            "components": {
                "data_layer": DATA_AVAILABLE,
                "pattern_matcher": DATA_AVAILABLE,
                "scanner": DATA_AVAILABLE
            },
            "mode": "live" if DATA_AVAILABLE else "mock"
        }

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
