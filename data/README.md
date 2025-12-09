# Data Component

Data acquisition and caching layer for Temple.

## Features

- **Abstract Provider Pattern**: Easily swap data sources (Yahoo Finance supported)
- **Smart Caching**: TTL-based file cache with configurable expiration
- **Type Safety**: Full type hints throughout
- **Clean API**: Simple factory pattern for easy instantiation
- **Configurable**: Environment-based or programmatic configuration

## Quick Start

### Basic Usage (Recommended)

```python
from data import create_data_repository

# Create repository with default configuration
repo = create_data_repository()

# Fetch OHLCV data
df = repo.get_ohlcv("AAPL")
print(df.head())

# Fetch fundamentals
fundamentals = repo.get_fundamentals("AAPL")
print(fundamentals)
```

### Custom Configuration

```python
from data import DataConfig, create_data_repository

# Create custom config
config = DataConfig(
    cache_dir="./custom_cache",
    ohlcv_ttl_hours=48,        # Cache OHLCV for 2 days
    fundamentals_ttl_days=14,  # Cache fundamentals for 2 weeks
    provider="yahoo"
)

repo = create_data_repository(config)
df = repo.get_ohlcv("MSFT")
```

### Environment-Based Configuration

Set environment variables:

```bash
export CACHE_DIR=./cache
export OHLCV_TTL_HOURS=24
export FUNDAMENTALS_TTL_DAYS=7
export DATA_PROVIDER=yahoo
```

Then use default configuration:

```python
from data import create_data_repository

repo = create_data_repository()  # Automatically reads from environment
```

### Advanced Usage (Dependency Injection)

```python
from data import DataFactory, YahooDataProvider, DataCache, DataConfig

# Create components explicitly
config = DataConfig(cache_dir="./cache")
provider = YahooDataProvider()
cache = DataCache(
    cache_dir=config.cache_dir,
    ohlcv_ttl_hours=config.ohlcv_ttl_hours,
    fundamentals_ttl_days=config.fundamentals_ttl_days
)

# Inject dependencies
repo = DataFactory.create_repository(
    config=config,
    provider=provider,
    cache=cache
)
```

## API Reference

### DataRepository

Main entry point for data operations.

**Methods:**

- `get_ohlcv(symbol: str, force_refresh: bool = False) -> pd.DataFrame`
  - Get OHLCV data for a symbol
  - Checks cache first unless `force_refresh=True`
  - Returns DataFrame with DatetimeIndex and columns: open, high, low, close, volume

- `get_fundamentals(symbol: str, force_refresh: bool = False) -> dict`
  - Get fundamental data for a symbol
  - Checks cache first unless `force_refresh=True`
  - Returns dict with keys: symbol, name, sector, industry, market_cap, pe_ratio, etc.

### DataConfig

Configuration dataclass.

**Fields:**

- `cache_dir: str` - Directory for cache files (default: "./cache")
- `ohlcv_ttl_hours: int` - OHLCV cache TTL in hours (default: 24)
- `fundamentals_ttl_days: int` - Fundamentals cache TTL in days (default: 7)
- `provider: str` - Data provider name (default: "yahoo")
- `default_period: str` - Default fetch period (default: "2y")

**Methods:**

- `DataConfig.from_env()` - Create from environment variables
- `DataConfig.from_dict(config_dict)` - Create from dictionary

### Factory Functions

**`create_data_repository(config: Optional[DataConfig] = None) -> DataRepository`**

Recommended way to create a repository. Uses default configuration if not provided.

**`DataFactory.create_repository(...) -> DataRepository`**

Create repository with full control over dependencies.

**`DataFactory.create_provider(provider_name: str) -> DataProvider`**

Create a data provider instance.

**`DataFactory.create_cache(config: Optional[DataConfig] = None) -> DataCache`**

Create a cache instance.

## Architecture

```
data/
├── __init__.py          # Public API exports
├── config.py            # Configuration management
├── factory.py           # Factory for creating instances
├── repository.py        # Main orchestration layer
├── provider.py          # Data provider abstraction
└── cache.py             # Caching layer
```

### Design Patterns

- **Repository Pattern**: `DataRepository` provides unified interface
- **Abstract Factory**: `DataProvider` is abstract, `YahooDataProvider` is concrete
- **Factory Pattern**: `DataFactory` and `create_data_repository()` for clean instantiation
- **Dependency Injection**: All components accept injected dependencies
- **Configuration Object**: `DataConfig` centralizes settings

## Testing

Run the verification script:

```bash
python verify_data_layer.py
```

This demonstrates all three usage patterns and verifies the cache structure.

## Cache Structure

```
cache/
├── ohlcv/
│   ├── AAPL.csv
│   ├── MSFT.csv
│   └── GOOGL.csv
└── fundamentals/
    ├── AAPL.json
    ├── MSFT.json
    └── GOOGL.json
```

- OHLCV data stored as CSV with DatetimeIndex
- Fundamentals stored as JSON
- TTL checked via file modification time

## Extending with New Providers

To add a new data provider:

1. Subclass `DataProvider`:

```python
from data import DataProvider
import pandas as pd

class MyCustomProvider(DataProvider):
    def fetch_ohlcv(self, symbol: str, start_date: Optional[str] = None,
                    end_date: Optional[str] = None, period: str = "2y") -> pd.DataFrame:
        # Your implementation
        pass

    def fetch_fundamentals(self, symbol: str) -> dict:
        # Your implementation
        pass
```

2. Register in `DataFactory.create_provider()`:

```python
# In factory.py
if provider_name.lower() == "mycustom":
    return MyCustomProvider()
```

3. Use it:

```python
from data import DataConfig, create_data_repository

config = DataConfig(provider="mycustom")
repo = create_data_repository(config)
```

## Dependencies

- `yfinance` - Yahoo Finance data provider
- `pandas` - DataFrame handling
- `python-dotenv` - Environment variable loading

## Usage in Other Components

When using this module in other Temple components (patterns, scanner, dashboard):

```python
# In patterns component
from data import create_data_repository

class PatternDetector:
    def __init__(self):
        self.data_repo = create_data_repository()

    def detect(self, symbol: str):
        df = self.data_repo.get_ohlcv(symbol)
        # Pattern detection logic...
```

This ensures clean separation of concerns and testability.
