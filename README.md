# Temple - Temporal Pattern Engine

A modular, extensible system for detecting repeatable stock market price behavior patterns using temporal sequence analysis.

## Overview

Temple enables traders and analysts to define custom patterns declaratively and scan entire stock universes to find matching securities. Instead of writing code, users describe patterns using a simple schema (e.g., "price falls below SMA20, then returns within 20 days") and Temple finds all historical occurrences.

## Key Features

- **Declarative Pattern Definition** - Define patterns without code using event sequences and frequency constraints
- **Multiple Pattern Types** - Support for price crosses, indicator events, pivot mean reversion, volume spikes
- **Temporal Sequence Matching** - Find multi-step patterns with timing constraints between events
- **Universe Scanning** - Scan S&P 500, NASDAQ-100, sector-specific lists, or custom watchlists
- **Parallel Processing** - Multi-threaded scanning for analyzing hundreds of stocks efficiently
- **Technical Indicators** - Built-in SMA, EMA, RSI, Bollinger Bands, VWAP, support/resistance
- **Pivot Analysis** - Unique pivot-based patterns using mode, median, or volume-weighted price levels
- **REST API** - Full-featured FastAPI backend for integration
- **Modern Dashboard** - React/TypeScript frontend for visual pattern exploration

## Architecture

```
                    +-------------------+
                    |   React Frontend  |
                    |  (Dashboard UI)   |
                    +--------+----------+
                             |
                             v
                    +-------------------+
                    |   FastAPI REST    |
                    |      Server       |
                    +--------+----------+
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
   +-------------+    +-------------+    +-------------+
   |   Scanner   |    |  Patterns   |    |    Data     |
   |   Layer     |    |   Engine    |    |   Layer     |
   +-------------+    +-------------+    +-------------+
```

## Components

| Component | Status | Description |
|-----------|--------|-------------|
| **Data Layer** | Complete | Fetch & cache OHLCV data from Yahoo Finance with TTL-based caching |
| **Patterns Engine** | Complete | Core detection engine with events, sequences, indicators, and matching |
| **Scanner Layer** | Complete | Batch scanning across stock universes with parallel processing |
| **REST API** | Complete | FastAPI backend exposing all functionality via HTTP endpoints |
| **Dashboard** | Complete | React/Vite/TypeScript frontend with scanner UI and pattern builder |

## Development Progress

### Completed Features

- [x] Data acquisition with Yahoo Finance provider
- [x] Smart caching with configurable TTL
- [x] Pattern definition schema (events, sequences, frequency)
- [x] Technical indicator calculations
- [x] Event detection system
- [x] Temporal sequence matching
- [x] Confidence scoring
- [x] Pivot mean reversion patterns (mode, median, volume-weighted)
- [x] Stock universe management
- [x] Parallel batch scanning
- [x] REST API with pattern matching endpoints
- [x] REST API with scanner endpoints
- [x] React dashboard with scanner interface
- [x] Real-time API integration
- [x] Stock detail modal with charts

### Roadmap

- [ ] Pattern backtesting framework
- [ ] Pattern optimization (find best parameters)
- [ ] Alert/notification system
- [ ] User authentication
- [ ] Pattern library/marketplace
- [ ] Real-time streaming updates
- [ ] Machine learning pattern discovery

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Clone and enter the repository
git clone https://github.com/yourusername/Temple.git
cd Temple

# Install Python dependencies
pip install -r requirements.txt

# Start the API server
python -m uvicorn api.main:app --reload --port 8000
```

### Frontend Setup

```bash
# Enter frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The dashboard will be available at `http://localhost:5173` and the API at `http://localhost:8000`.

### API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Usage Examples

### Define a Pattern (Python)

```python
from patterns import (
    PatternDefinition, SequenceStep, EventDefinition,
    ReferenceLevel, FrequencyConstraint, EventType, TimeframeUnit
)

# Mean reversion pattern: price falls below SMA20, returns within 20 days
pattern = PatternDefinition(
    name="Mean Reversion",
    description="Price deviates below average and returns",
    sequence=[
        SequenceStep(
            event=EventDefinition(
                type=EventType.PRICE_CROSSES_BELOW,
                reference=ReferenceLevel(type="sma", period=20)
            ),
            name="Fall below SMA20"
        ),
        SequenceStep(
            event=EventDefinition(
                type=EventType.PRICE_CROSSES_ABOVE,
                reference=ReferenceLevel(type="sma", period=20)
            ),
            max_duration_days=20,
            name="Return to SMA20"
        )
    ],
    frequency=FrequencyConstraint(
        min_occurrences=8,
        timeframe=1,
        timeframe_unit=TimeframeUnit.YEARS
    )
)
```

### Scan via REST API

```bash
curl -X POST http://localhost:8000/api/v1/scanner/scan \
  -H "Content-Type: application/json" \
  -d '{
    "universe": "tech",
    "pattern": {
      "name": "Mean Reversion",
      "sequence": [...],
      "frequency": {"min_occurrences": 5, "timeframe_days": 180}
    },
    "min_confidence": 0.7
  }'
```

### Use the Dashboard

1. Open http://localhost:5173
2. Navigate to the Scanner tab
3. Select a stock universe (e.g., "S&P 500 Top 100")
4. Choose a pattern from the presets or define custom
5. Click "Run Scan" to find matching stocks
6. Click any result to view detailed chart and pattern occurrences

## Branch Structure

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code (integration point) |
| `component/data` | Data layer development |
| `component/patterns` | Pattern engine development |
| `component/scanner` | Scanner layer development |
| `component/backend` | REST API development |
| `component/dashboard` | Frontend dashboard development |

## Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** - REST API framework
- **Uvicorn** - ASGI server
- **yfinance** - Stock data provider
- **pandas/numpy** - Data processing
- **python-dotenv** - Configuration

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Recharts** - Charting library
- **Lucide React** - Icons

## Project Structure

```
Temple/
├── api/                    # FastAPI REST server
│   ├── main.py            # Application entry point
│   ├── routers/           # API endpoints
│   │   ├── patterns.py    # Pattern matching routes
│   │   └── scanner.py     # Scanner routes
│   ├── services/          # Business logic
│   └── data/              # Universe definitions
├── patterns/              # Core pattern engine
│   ├── schema.py          # Pattern definition types
│   ├── events.py          # Event detection
│   ├── sequences.py       # Sequence matching
│   ├── matcher.py         # Pattern matcher
│   ├── indicators.py      # Technical indicators
│   └── mock_data.py       # Test data generators
├── frontend/              # React dashboard
│   └── src/
│       ├── components/    # React components
│       ├── hooks/         # Custom hooks
│       ├── services/      # API service
│       └── types/         # TypeScript types
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Configuration

### Environment Variables

```bash
# API Server
API_HOST=0.0.0.0
API_PORT=8000

# Data Layer
CACHE_DIR=./cache
OHLCV_TTL_HOURS=24
DATA_PROVIDER=yahoo

# Frontend
VITE_API_URL=http://localhost:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch from the appropriate component branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

---

**Temple** - Discover patterns. Find opportunities.
