# Temple REST API

REST API for Temple - Temporal Pattern Engine for Stock Market Analysis.

## Overview

The Temple API provides RESTful endpoints for pattern matching and stock scanning. It integrates the Data Layer, Patterns Layer, and Scanner Layer into a unified HTTP interface.

## Features

- **Pattern Matching**: Match patterns against individual stocks
- **Batch Scanning**: Scan multiple stocks or universes for patterns
- **Pre-defined Universes**: Access S&P 500, NASDAQ-100, and Tech stock lists
- **Example Patterns**: Get pre-configured pattern templates
- **Parallel Processing**: Optional parallel scanning for better performance
- **CORS Support**: Configured for frontend integration
- **Auto-generated Documentation**: Interactive API docs via Swagger UI
- **Mock Mode**: Fallback mode for testing without data layer dependencies

## Installation

```bash
# Install API dependencies
pip install -r requirements-api.txt

# Optional: Install Temple components for full functionality
pip install -r requirements.txt
```

## Quick Start

### Starting the Server

```bash
# Development mode with auto-reload
python -m uvicorn api.main:app --reload

# Production mode
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Configuration

### Environment Variables

```bash
# Server settings
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false
API_RELOAD=false

# CORS settings
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Rate limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_CALLS=100
RATE_LIMIT_PERIOD=60
```

### Programmatic Configuration

```python
from api import create_app, APIConfig, set_config

config = APIConfig(
    host="0.0.0.0",
    port=8000,
    debug=True,
    allow_origins=["http://localhost:3000"]
)

set_config(config)
app = create_app()
```

## API Endpoints

### Root & Health

#### GET /
Get API information and available endpoints.

**Response:**
```json
{
  "name": "Temple API",
  "version": "0.1.0",
  "description": "Temporal Pattern Engine for Stock Market Analysis",
  "docs": "/docs",
  "endpoints": {
    "patterns": "/api/v1/patterns",
    "scanner": "/api/v1/scanner"
  }
}
```

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Temple API"
}
```

### Pattern Endpoints

#### POST /api/v1/patterns/match
Match a pattern against a single stock symbol.

**Request Body:**
```json
{
  "symbol": "AAPL",
  "pattern": {
    "name": "Mean Reversion",
    "description": "Price deviates and returns to average",
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
  "lookback_days": 365
}
```

**Response:**
```json
{
  "symbol": "AAPL",
  "pattern_name": "Mean Reversion",
  "matched": true,
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
```

#### GET /api/v1/patterns/examples
Get example pattern definitions.

**Response:**
```json
[
  {
    "name": "Mean Reversion",
    "description": "Price deviates significantly from average and returns",
    "sequence": [...],
    "frequency": {
      "min_occurrences": 3,
      "timeframe_days": 180
    }
  }
]
```

### Scanner Endpoints

#### POST /api/v1/scanner/scan
Scan multiple stocks or a universe for pattern matches.

**Request Body (with symbols):**
```json
{
  "symbols": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"],
  "pattern": {
    "name": "Mean Reversion",
    "description": "Price deviates and returns",
    "sequence": [],
    "frequency": {
      "min_occurrences": 3,
      "timeframe_days": 180
    }
  },
  "min_confidence": 0.7,
  "parallel": true
}
```

**Request Body (with universe):**
```json
{
  "universe": "tech",
  "pattern": {...},
  "min_confidence": 0.7,
  "parallel": true
}
```

**Response:**
```json
{
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
      "matched": true,
      "confidence": 0.85,
      "occurrences": 12,
      "timeframe_start": "2024-01-01",
      "timeframe_end": "2024-12-31"
    }
  ]
}
```

#### GET /api/v1/scanner/universes
List all available stock universes.

**Response:**
```json
{
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
```

#### GET /api/v1/scanner/health
Check scanner service health and component availability.

**Response:**
```json
{
  "status": "healthy",
  "components": {
    "data_layer": true,
    "pattern_matcher": true,
    "scanner": true
  },
  "mode": "live"
}
```

## Usage Examples

### Python

```python
import requests

API_BASE_URL = "http://localhost:8000"

# Match pattern against a single stock
pattern_request = {
    "symbol": "AAPL",
    "pattern": {
        "name": "Mean Reversion",
        "description": "Price deviates and returns",
        "sequence": [],
        "frequency": {
            "min_occurrences": 3,
            "timeframe_days": 180
        }
    },
    "lookback_days": 365
}

response = requests.post(
    f"{API_BASE_URL}/api/v1/patterns/match",
    json=pattern_request
)

result = response.json()
print(f"Matched: {result['matched']}")
print(f"Confidence: {result['confidence']:.2%}")
```

### JavaScript/TypeScript

```typescript
const API_BASE_URL = 'http://localhost:8000';

// Scan multiple stocks
const scanRequest = {
  symbols: ['AAPL', 'MSFT', 'GOOGL'],
  pattern: {
    name: 'Mean Reversion',
    description: 'Price deviates and returns',
    sequence: [],
    frequency: {
      min_occurrences: 3,
      timeframe_days: 180
    }
  },
  min_confidence: 0.7,
  parallel: true
};

const response = await fetch(`${API_BASE_URL}/api/v1/scanner/scan`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(scanRequest)
});

const result = await response.json();
console.log(`Matches found: ${result.matches_found}/${result.total_symbols}`);
```

### cURL

```bash
# Health check
curl http://localhost:8000/health

# List universes
curl http://localhost:8000/api/v1/scanner/universes

# Match pattern
curl -X POST http://localhost:8000/api/v1/patterns/match \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "pattern": {
      "name": "Test Pattern",
      "description": "Test",
      "sequence": [],
      "frequency": {
        "min_occurrences": 1,
        "timeframe_days": 30
      }
    },
    "lookback_days": 365
  }'

# Scan stocks
curl -X POST http://localhost:8000/api/v1/scanner/scan \
  -H "Content-Type": "application/json" \
  -d '{
    "symbols": ["AAPL", "MSFT", "GOOGL"],
    "pattern": {
      "name": "Test Pattern",
      "description": "Test",
      "sequence": [],
      "frequency": {
        "min_occurrences": 1,
        "timeframe_days": 30
      }
    },
    "min_confidence": 0.5
  }'
```

## Pattern Definition

### Event Types

- **price_crosses_above**: Price crosses above a value or indicator
- **price_crosses_below**: Price crosses below a value or indicator
- **price_touches**: Price touches a value or indicator
- **price_rises_by**: Price rises by a percentage
- **price_falls_by**: Price falls by a percentage
- **volatility_spike**: Volatility increases significantly
- **volatility_drop**: Volatility decreases significantly

### Indicators

- **sma**: Simple Moving Average (requires `period` parameter)
- **ema**: Exponential Moving Average (requires `period` parameter)
- **support**: Support level
- **resistance**: Resistance level
- **upper_band**: Bollinger Band upper
- **lower_band**: Bollinger Band lower

### Example Patterns

**Mean Reversion:**
```json
{
  "name": "Mean Reversion",
  "description": "Price deviates significantly and returns to average",
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
```

**Support Bounce:**
```json
{
  "name": "Support Bounce",
  "description": "Price bounces off support level",
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
}
```

## Testing

### Run Verification Script

```bash
# Start the API server in one terminal
python -m uvicorn api.main:app --reload

# Run verification script in another terminal
python verify_api.py
```

The verification script demonstrates:
1. Health checks
2. Listing universes
3. Getting example patterns
4. Matching patterns against stocks
5. Scanning multiple symbols
6. Scanning universes

## Architecture

```
api/
├── __init__.py          # Package initialization
├── main.py              # FastAPI application
├── config.py            # Configuration management
├── models/              # Pydantic request/response models
│   ├── __init__.py
│   ├── pattern.py       # Pattern-related models
│   └── scan.py          # Scanner-related models
├── routers/             # API route handlers
│   ├── __init__.py
│   ├── patterns.py      # Pattern matching endpoints
│   └── scanner.py       # Scanning endpoints
└── services/            # Business logic layer
    ├── __init__.py
    └── temple_service.py # Temple component integration
```

## Mock Mode

When Temple components (data, patterns, scanner) are not available, the API operates in **mock mode**, returning realistic dummy data for development and testing purposes.

Check the mode with:
```bash
curl http://localhost:8000/api/v1/scanner/health
```

Response will show:
```json
{
  "status": "healthy",
  "components": {
    "data_layer": false,
    "pattern_matcher": false,
    "scanner": false
  },
  "mode": "mock"
}
```

## Error Handling

The API uses standard HTTP status codes:

- **200 OK**: Successful request
- **400 Bad Request**: Invalid input parameters
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

Error responses include details:
```json
{
  "detail": "Must provide either 'symbols' or 'universe'"
}
```

## Performance

- **Parallel Scanning**: Enable with `"parallel": true` for faster results
- **CORS**: Pre-configured for common frontend ports
- **Response Times**: Typical response times:
  - Pattern match (single stock): 100-500ms
  - Scan 10 stocks (sequential): 1-3 seconds
  - Scan 10 stocks (parallel): 300-800ms
  - Scan universe (100+ stocks, parallel): 5-15 seconds

## Integration with Frontend

The API is configured to work with React/Vue/Angular frontends:

```typescript
// Example React hook
const usePatternMatch = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const matchPattern = async (symbol, pattern) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/patterns/match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol, pattern, lookback_days: 365 })
      });
      const data = await response.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  };

  return { matchPattern, loading, result };
};
```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt requirements-api.txt ./
RUN pip install -r requirements.txt -r requirements-api.txt

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Settings

```bash
# Use production ASGI server
pip install gunicorn

# Run with Gunicorn
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Security

- **CORS**: Configured for specific origins
- **Rate Limiting**: Optional rate limiting (configurable)
- **Input Validation**: All inputs validated via Pydantic
- **Error Handling**: Generic error messages to prevent information leakage

## Contributing

The Temple API is part of the Temple project. See the main project README for contribution guidelines.

## License

See main project LICENSE file.
