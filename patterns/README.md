# Patterns Component

**Temporal Pattern Detection Engine** for Temple.

Detects recurring time-based patterns in stock price data with a flexible, user-definable pattern language.

## Features

- **Generic Pattern Definition**: Define any temporal pattern without writing code
- **Sequence Matching**: Find multi-step sequences of events with timing constraints
- **Frequency Analysis**: Count pattern occurrences over configurable time windows
- **Technical Indicators**: Built-in calculations for RSI, SMA, Bollinger Bands, etc.
- **Event Detection**: Detect crosses, touches, percentage moves, volume spikes
- **Confidence Scoring**: Automatic confidence calculation for pattern matches

## Quick Start

### Basic Usage

```python
from data.repository import DataRepository
from patterns import (
    create_pattern_matcher,
    PatternDefinition,
    SequenceStep,
    EventDefinition,
    ReferenceLevel,
    FrequencyConstraint,
    EventType,
    TimeframeUnit
)

# Get price data
repo = DataRepository()
df = repo.get_ohlcv("AAPL")

# Define a pattern: Support bounce (touches support 5+ times in 6 months)
pattern = PatternDefinition(
    name="Support Bounce",
    description="Price touches support and bounces back repeatedly",
    sequence=[
        SequenceStep(
            event=EventDefinition(
                type=EventType.PRICE_TOUCHES,
                reference=ReferenceLevel(type="support", lookback=90),
                tolerance=1.5
            ),
            name="Touch support"
        ),
        SequenceStep(
            event=EventDefinition(
                type=EventType.PRICE_RISES_BY,
                min_change=3.0
            ),
            max_duration_days=15,
            name="Bounce up"
        )
    ],
    frequency=FrequencyConstraint(
        min_occurrences=5,
        timeframe=6,
        timeframe_unit=TimeframeUnit.MONTHS
    )
)

# Match pattern
matcher = create_pattern_matcher()
match = matcher.match(df, "AAPL", pattern)

# View results
print(f"Pattern: {match.pattern_name}")
print(f"Occurrences: {match.count}")
print(f"Confidence: {match.confidence:.2%}")
```

## Pattern Definition Language

Patterns are defined using a declarative schema with four main components:

### 1. Events

Events are specific occurrences in price data:

```python
# Price crosses above SMA20
EventDefinition(
    type=EventType.PRICE_CROSSES_ABOVE,
    reference=ReferenceLevel(type="sma", period=20)
)

# Price falls 10%
EventDefinition(
    type=EventType.PRICE_FALLS_BY,
    min_change=10.0
)

# Volume spike (2x average)
EventDefinition(
    type=EventType.VOLUME_SPIKE,
    reference=ReferenceLevel(type="fixed", value=2.0, period=20)
)
```

**Available Event Types:**
- `PRICE_CROSSES_ABOVE` - Price crosses above a level
- `PRICE_CROSSES_BELOW` - Price crosses below a level
- `PRICE_TOUCHES` - Price comes within tolerance of a level
- `PRICE_RISES_BY` - Price rises by X%
- `PRICE_FALLS_BY` - Price falls by X%
- `VOLUME_SPIKE` - Volume exceeds average by multiplier

### 2. Reference Levels

Reference levels define price targets or thresholds:

```python
# Fixed price
ReferenceLevel(type="fixed", value=150.0)

# Moving averages
ReferenceLevel(type="sma", period=20)
ReferenceLevel(type="ema", period=50)

# Support/Resistance
ReferenceLevel(type="support", lookback=90)
ReferenceLevel(type="resistance", lookback=90)

# VWAP
ReferenceLevel(type="vwap")
```

### 3. Sequences

Sequences define ordered steps with timing constraints:

```python
sequence=[
    SequenceStep(
        event=EventDefinition(...),
        min_duration_days=1,      # Optional: minimum days to next step
        max_duration_days=30,     # Optional: maximum days to next step
        name="Step description"
    ),
    SequenceStep(
        event=EventDefinition(...),
        max_duration_days=10,
        name="Next step"
    )
]
```

### 4. Frequency Constraints

Define how often the pattern must occur:

```python
FrequencyConstraint(
    min_occurrences=8,            # Minimum times pattern must occur
    max_occurrences=20,           # Optional maximum
    timeframe=1,                  # Time window size
    timeframe_unit=TimeframeUnit.YEARS  # DAYS, WEEKS, MONTHS, YEARS
)
```

## Example Patterns

### Mean Reversion Pattern

```python
PatternDefinition(
    name="Mean Reversion",
    description="Price deviates below SMA20 and returns",
    sequence=[
        SequenceStep(
            event=EventDefinition(
                type=EventType.PRICE_CROSSES_BELOW,
                reference=ReferenceLevel(type="sma", period=20)
            ),
            name="Fall below average"
        ),
        SequenceStep(
            event=EventDefinition(
                type=EventType.PRICE_CROSSES_ABOVE,
                reference=ReferenceLevel(type="sma", period=20)
            ),
            max_duration_days=20,
            name="Return to average"
        )
    ],
    frequency=FrequencyConstraint(
        min_occurrences=8,
        timeframe=1,
        timeframe_unit=TimeframeUnit.YEARS
    )
)
```

### Volatility Cycle Pattern

```python
PatternDefinition(
    name="Volatility Cycle",
    description="Large swings up and down repeatedly",
    sequence=[
        SequenceStep(
            event=EventDefinition(
                type=EventType.PRICE_RISES_BY,
                min_change=10.0
            ),
            name="Sharp rise"
        ),
        SequenceStep(
            event=EventDefinition(
                type=EventType.PRICE_FALLS_BY,
                min_change=10.0
            ),
            max_duration_days=30,
            name="Sharp fall"
        )
    ],
    frequency=FrequencyConstraint(
        min_occurrences=3,
        timeframe=6,
        timeframe_unit=TimeframeUnit.MONTHS
    )
)
```

### Custom Pattern: 5% Gains Repeating

"Stock rises 5% at least 10 times in a year"

```python
PatternDefinition(
    name="Frequent Gains",
    description="Consistent 5% gains throughout the year",
    sequence=[
        SequenceStep(
            event=EventDefinition(
                type=EventType.PRICE_RISES_BY,
                min_change=5.0,
                max_change=15.0  # Cap at 15% to avoid outliers
            ),
            name="5% gain"
        )
    ],
    frequency=FrequencyConstraint(
        min_occurrences=10,
        timeframe=1,
        timeframe_unit=TimeframeUnit.YEARS
    )
)
```

## API Reference

### PatternMatcher

Main pattern detection engine.

**Methods:**

- `match(df, symbol, pattern) -> PatternMatch`
  - Match a single pattern against price data
  - Returns PatternMatch with results

- `match_multiple(df, symbol, patterns) -> List[PatternMatch]`
  - Match multiple patterns against the same data
  - More efficient than calling match() repeatedly

- `find_best_matches(matches, min_confidence, top_n) -> List[PatternMatch]`
  - Filter and rank matches by confidence
  - Returns top N matches above confidence threshold

- `get_summary(match) -> Dict`
  - Get human-readable summary of a match

### PatternMatch

Result object returned by pattern matching.

**Fields:**

- `pattern_name: str` - Name of the pattern
- `symbol: str` - Stock symbol
- `occurrences: List[Dict]` - List of matched sequences with dates
- `count: int` - Number of occurrences found
- `confidence: float` - Confidence score (0.0 to 1.0)
- `timeframe_start: str` - Start of analysis period
- `timeframe_end: str` - End of analysis period
- `metadata: Dict` - Additional information

### Indicators

Technical indicator calculations.

**Available Indicators:**

- `sma(data, period)` - Simple Moving Average
- `ema(data, period)` - Exponential Moving Average
- `bollinger_bands(data, period, std_dev)` - Bollinger Bands
- `rsi(data, period)` - Relative Strength Index
- `macd(data, fast, slow, signal)` - MACD
- `atr(high, low, close, period)` - Average True Range
- `stochastic(high, low, close, period)` - Stochastic Oscillator
- `support_resistance(close, lookback)` - Support/Resistance levels

**Helper Function:**

- `calculate_all_indicators(df)` - Add all indicators to dataframe

## Architecture

```
patterns/
├── __init__.py          # Public API exports
├── schema.py            # Pattern definition schema
├── config.py            # Configuration management
├── factory.py           # Factory for creating instances
├── matcher.py           # Main pattern matching orchestrator
├── indicators.py        # Technical indicator calculations
├── events.py            # Event detection system
└── sequences.py         # Sequence matching and frequency analysis
```

### Design Patterns

- **Builder Pattern**: `PatternDefinition` for declarative pattern construction
- **Strategy Pattern**: Pluggable event detectors for different event types
- **Factory Pattern**: `create_pattern_matcher()` for clean instantiation
- **Composite Pattern**: Sequences composed of multiple steps

## Testing

Run the verification script:

```bash
python verify_patterns.py
```

This demonstrates:
- Support bounce pattern detection
- Mean reversion pattern detection
- Volatility cycle pattern detection
- Multiple pattern matching

## Configuration

Configure via environment variables or programmatically:

```python
from patterns import PatternsConfig, create_pattern_matcher

config = PatternsConfig(
    calculate_indicators=True,
    min_confidence=0.6,
    default_lookback_days=365
)

matcher = create_pattern_matcher(config)
```

**Environment Variables:**

- `PATTERNS_CALCULATE_INDICATORS` - Auto-calculate indicators (default: true)
- `PATTERNS_MIN_CONFIDENCE` - Minimum confidence threshold (default: 0.5)
- `PATTERNS_LOOKBACK_DAYS` - Default lookback period (default: 365)

## Integration with Data Layer

The patterns layer is designed to work seamlessly with the data layer:

```python
from data.repository import DataRepository
from patterns import create_pattern_matcher, PatternDefinition

# Get data
repo = DataRepository()
df = repo.get_ohlcv("AAPL")

# Match pattern
matcher = create_pattern_matcher()
pattern = PatternDefinition(...)  # Your pattern
match = matcher.match(df, "AAPL", pattern)
```

## Usage in Scanner Component

The scanner will use patterns like this:

```python
from patterns import create_pattern_matcher, PatternDefinition

class Scanner:
    def __init__(self):
        self.matcher = create_pattern_matcher()

    def scan_stocks(self, symbols, pattern):
        results = []
        for symbol in symbols:
            df = self.get_data(symbol)
            match = self.matcher.match(df, symbol, pattern)
            if match.confidence > 0.7:
                results.append(match)
        return results
```

## Advanced: Custom Event Types

To add new event types, extend the `EventDetector` class:

```python
from patterns.events import EventDetector

class CustomEventDetector(EventDetector):
    def detect_custom_event(self, event: EventDefinition):
        # Your custom detection logic
        events = []
        # ... detection code ...
        return events
```

## Performance Considerations

- **Indicator Caching**: Indicators are calculated once per dataframe
- **Parallel Matching**: Use `match_multiple()` for multiple patterns
- **Data Lookback**: Limit lookback period for faster processing

## Limitations

- Minimum data requirement: 200 days for reliable pattern detection
- Support/resistance detection is approximate (uses local minima/maxima)
- Confidence scores are heuristic-based, not statistical

## Future Enhancements

- [ ] Backtesting framework
- [ ] Pattern optimization (find best parameters)
- [ ] Machine learning for pattern discovery
- [ ] Real-time pattern monitoring
- [ ] Pattern library/marketplace

## Dependencies

- `pandas` - DataFrame handling
- `numpy` - Numerical calculations
- Temple `data` layer - Price data acquisition

---

The patterns layer enables users to define and detect any temporal pattern in stock price data without writing code. It's the core of Temple's pattern detection engine.
