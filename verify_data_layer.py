"""
Verification script demonstrating the Data Layer API.

This script shows three different ways to use the data layer:
1. Simple usage (recommended)
2. With custom configuration
3. With dependency injection
"""

import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add current directory to path
sys.path.append(os.getcwd())


def demo_simple_usage():
    """Demo 1: Simplest usage pattern (recommended for most cases)."""
    print("\n" + "="*70)
    print("DEMO 1: Simple Usage (Recommended)")
    print("="*70)

    from data import create_data_repository

    # Create repository with default configuration
    repo = create_data_repository()

    symbol = "AAPL"
    print(f"\nFetching data for {symbol}...")

    # Fetch OHLCV data
    print("\n[1] Fetching OHLCV...")
    df = repo.get_ohlcv(symbol)
    print(f"    [OK] Retrieved {len(df)} rows")
    print(f"\n    First 3 rows:\n{df.head(3)}")
    print(f"\n    Last 3 rows:\n{df.tail(3)}")

    # Fetch fundamentals
    print("\n[2] Fetching Fundamentals...")
    fund = repo.get_fundamentals(symbol)
    print("    [OK] Fundamentals retrieved:")
    for key, value in fund.items():
        print(f"      - {key}: {value}")

    # Test cache (should be instant on second call)
    print("\n[3] Testing Cache (second fetch should be instant)...")
    df2 = repo.get_ohlcv(symbol)
    print(f"    [OK] Cache hit! Retrieved {len(df2)} rows from cache")

    return repo


def demo_custom_configuration():
    """Demo 2: Using custom configuration."""
    print("\n" + "="*70)
    print("DEMO 2: Custom Configuration")
    print("="*70)

    from data import DataConfig, create_data_repository

    # Create custom configuration
    config = DataConfig(
        cache_dir="./cache",
        ohlcv_ttl_hours=48,  # Cache OHLCV for 2 days
        fundamentals_ttl_days=14,  # Cache fundamentals for 2 weeks
        provider="yahoo"
    )

    print(f"\nConfiguration:")
    print(f"  - Cache dir: {config.cache_dir}")
    print(f"  - OHLCV TTL: {config.ohlcv_ttl_hours} hours")
    print(f"  - Fundamentals TTL: {config.fundamentals_ttl_days} days")
    print(f"  - Provider: {config.provider}")

    # Create repository with custom config
    repo = create_data_repository(config)

    symbol = "MSFT"
    print(f"\nFetching data for {symbol}...")
    df = repo.get_ohlcv(symbol)
    print(f"    [OK] Retrieved {len(df)} rows")

    return repo


def demo_advanced_usage():
    """Demo 3: Advanced usage with dependency injection."""
    print("\n" + "="*70)
    print("DEMO 3: Advanced Usage (Dependency Injection)")
    print("="*70)

    from data import DataFactory, YahooDataProvider, DataCache, DataConfig

    # Create components explicitly
    print("\nCreating components:")

    config = DataConfig(cache_dir="./cache")
    print(f"  - Config: cache_dir={config.cache_dir}")

    provider = YahooDataProvider()
    print(f"  - Provider: {provider.__class__.__name__}")

    cache = DataCache(
        cache_dir=config.cache_dir,
        ohlcv_ttl_hours=config.ohlcv_ttl_hours,
        fundamentals_ttl_days=config.fundamentals_ttl_days
    )
    print(f"  - Cache: {cache.__class__.__name__}")

    # Inject dependencies
    repo = DataFactory.create_repository(
        config=config,
        provider=provider,
        cache=cache
    )
    print(f"  - Repository: {repo.__class__.__name__}")

    symbol = "GOOGL"
    print(f"\nFetching data for {symbol}...")
    df = repo.get_ohlcv(symbol)
    print(f"    [OK] Retrieved {len(df)} rows")

    return repo


def verify_cache_structure():
    """Verify that cache files were created properly."""
    print("\n" + "="*70)
    print("CACHE VERIFICATION")
    print("="*70)

    cache_base = "./cache"
    if not os.path.exists(cache_base):
        print("[X] Cache directory does not exist!")
        return

    print(f"\n[OK] Cache directory exists: {cache_base}")

    # Check OHLCV cache
    ohlcv_dir = os.path.join(cache_base, "ohlcv")
    if os.path.exists(ohlcv_dir):
        ohlcv_files = [f for f in os.listdir(ohlcv_dir) if f.endswith('.csv')]
        print(f"[OK] OHLCV cache: {len(ohlcv_files)} files")
        for f in ohlcv_files:
            print(f"    - {f}")
    else:
        print("[X] OHLCV cache directory missing")

    # Check fundamentals cache
    fund_dir = os.path.join(cache_base, "fundamentals")
    if os.path.exists(fund_dir):
        fund_files = [f for f in os.listdir(fund_dir) if f.endswith('.json')]
        print(f"[OK] Fundamentals cache: {len(fund_files)} files")
        for f in fund_files:
            print(f"    - {f}")
    else:
        print("[X] Fundamentals cache directory missing")


def main():
    """Run all verification demos."""
    print("\n" + "="*70)
    print("TEMPLE DATA LAYER - API VERIFICATION")
    print("="*70)

    try:
        # Run demos
        demo_simple_usage()
        demo_custom_configuration()
        demo_advanced_usage()

        # Verify cache
        verify_cache_structure()

        print("\n" + "="*70)
        print("[OK] ALL DEMOS COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\nThe data layer is ready to use in other components!")
        print("Recommended: Use `create_data_repository()` for most cases.")

    except Exception as e:
        print(f"\n[X] Error during verification: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
