"""
Stock universe management for the scanner.

This module manages collections of stock symbols (watchlists, indices, custom lists).
"""

from typing import List, Optional, Set, Dict
from dataclasses import dataclass
import logging


logger = logging.getLogger(__name__)


# Pre-defined stock universes
SP500_SYMBOLS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK.B", "UNH", "JNJ",
    "V", "XOM", "WMT", "JPM", "LLY", "MA", "PG", "AVGO", "HD", "CVX",
    "MRK", "ABBV", "KO", "COST", "PEP", "ADBE", "CRM", "MCD", "CSCO", "ACN",
    "TMO", "ABT", "NFLX", "NKE", "LIN", "DHR", "TXN", "WFC", "VZ", "PM",
    "NEE", "UPS", "RTX", "ORCL", "MS", "BMY", "INTC", "QCOM", "HON", "COP",
    # Add more S&P 500 symbols as needed - this is a subset
]

NASDAQ100_SYMBOLS = [
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA", "AVGO", "COST",
    "NFLX", "ADBE", "AMD", "PEP", "CSCO", "CMCSA", "INTC", "TMUS", "TXN", "INTU",
    "QCOM", "AMGN", "HON", "AMAT", "SBUX", "BKNG", "ISRG", "GILD", "ADI", "VRTX",
    # Add more NASDAQ-100 symbols as needed - this is a subset
]

TECH_STOCKS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "ADBE", "CRM", "ORCL",
    "CSCO", "INTC", "AMD", "QCOM", "AVGO", "NOW", "SNOW", "UBER", "ABNB", "SHOP"
]


@dataclass
class StockUniverse:
    """Represents a collection of stock symbols."""

    name: str
    symbols: List[str]
    description: Optional[str] = None

    def __post_init__(self):
        # Remove duplicates and sort
        self.symbols = sorted(list(set(self.symbols)))

    def __len__(self) -> int:
        return len(self.symbols)

    def __iter__(self):
        return iter(self.symbols)

    def add_symbol(self, symbol: str):
        """Add a symbol to the universe."""
        if symbol not in self.symbols:
            self.symbols.append(symbol)
            self.symbols.sort()

    def remove_symbol(self, symbol: str):
        """Remove a symbol from the universe."""
        if symbol in self.symbols:
            self.symbols.remove(symbol)

    def filter(self, predicate) -> "StockUniverse":
        """Create a new universe with filtered symbols."""
        filtered_symbols = [s for s in self.symbols if predicate(s)]
        return StockUniverse(
            name=f"{self.name} (filtered)",
            symbols=filtered_symbols,
            description=f"Filtered from {self.name}"
        )


class UniverseManager:
    """Manages multiple stock universes and watchlists."""

    def __init__(self):
        self.universes: Dict[str, StockUniverse] = {}
        self._load_default_universes()

    def _load_default_universes(self):
        """Load pre-defined stock universes."""
        self.universes["sp500"] = StockUniverse(
            name="S&P 500",
            symbols=SP500_SYMBOLS,
            description="S&P 500 index stocks"
        )

        self.universes["nasdaq100"] = StockUniverse(
            name="NASDAQ-100",
            symbols=NASDAQ100_SYMBOLS,
            description="NASDAQ-100 index stocks"
        )

        self.universes["tech"] = StockUniverse(
            name="Tech Stocks",
            symbols=TECH_STOCKS,
            description="Major technology companies"
        )

    def get_universe(self, name: str) -> Optional[StockUniverse]:
        """Get a universe by name."""
        return self.universes.get(name.lower())

    def list_universes(self) -> List[str]:
        """List all available universe names."""
        return list(self.universes.keys())

    def create_universe(self, name: str, symbols: List[str], description: Optional[str] = None) -> StockUniverse:
        """Create a custom universe."""
        universe = StockUniverse(name=name, symbols=symbols, description=description)
        self.universes[name.lower()] = universe
        logger.info(f"Created universe '{name}' with {len(symbols)} symbols")
        return universe

    def delete_universe(self, name: str):
        """Delete a custom universe."""
        if name.lower() in self.universes:
            del self.universes[name.lower()]
            logger.info(f"Deleted universe '{name}'")

    def combine_universes(self, names: List[str], new_name: str) -> StockUniverse:
        """Combine multiple universes into one."""
        all_symbols: Set[str] = set()

        for name in names:
            universe = self.get_universe(name)
            if universe:
                all_symbols.update(universe.symbols)

        return self.create_universe(
            name=new_name,
            symbols=list(all_symbols),
            description=f"Combined from: {', '.join(names)}"
        )


def create_custom_universe(symbols: List[str], name: str = "Custom") -> StockUniverse:
    """
    Convenience function to create a custom stock universe.

    Args:
        symbols: List of stock symbols
        name: Name for the universe

    Returns:
        StockUniverse instance

    Example:
        ```python
        my_stocks = create_custom_universe(["AAPL", "MSFT", "GOOGL"], "My Portfolio")
        ```
    """
    return StockUniverse(name=name, symbols=symbols)
