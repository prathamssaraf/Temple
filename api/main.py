"""Main FastAPI application for Temple."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from .config import get_config
from .routers import patterns_router, scanner_router


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    config = get_config()

    app = FastAPI(
        title="Temple API",
        description="REST API for Temple - Temporal Pattern Engine",
        version="0.1.0",
        docs_url=config.docs_url,
        redoc_url=config.redoc_url
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allow_origins,
        allow_credentials=config.allow_credentials,
        allow_methods=config.allow_methods,
        allow_headers=config.allow_headers,
    )

    # Include routers
    app.include_router(patterns_router, prefix=config.api_prefix)
    app.include_router(scanner_router, prefix=config.api_prefix)

    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        return {
            "name": "Temple API",
            "version": "0.1.0",
            "description": "Temporal Pattern Engine for Stock Market Analysis",
            "docs": config.docs_url,
            "endpoints": {
                "patterns": f"{config.api_prefix}/patterns",
                "scanner": f"{config.api_prefix}/scanner"
            }
        }

    # Health check endpoint
    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy", "service": "Temple API"}

    # Exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Global exception handler."""
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

    logger.info("Temple API initialized successfully")
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    config = get_config()

    uvicorn.run(
        "api.main:app",
        host=config.host,
        port=config.port,
        reload=config.reload,
        log_level="info"
    )
