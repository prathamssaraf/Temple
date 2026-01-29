"""
Temple API - FastAPI server for pattern detection and scanning.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import patterns, scanner

app = FastAPI(
    title="Temple API",
    description="Temporal Pattern Engine for Stock Market Analysis",
    version="1.0.0"
)

# CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(patterns.router, prefix="/api/v1/patterns", tags=["patterns"])
app.include_router(scanner.router, prefix="/api/v1/scanner", tags=["scanner"])


@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "components": {
            "data_layer": False,  # Not yet implemented
            "pattern_matcher": True,
            "scanner": False  # Not yet implemented
        },
        "mode": "development"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
