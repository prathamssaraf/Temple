import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add current directory to path to allow imports
sys.path.append(os.getcwd())

from data.repository import DataRepository

def main():
    print("Initializing Data Repository...")
    repo = DataRepository()
    
    symbol = "AAPL"
    print(f"\n--- Fetching Data for {symbol} ---")
    
    # 1. Fetch OHLCV
    print("\n1. Fetching OHLCV...")
    try:
        df = repo.get_ohlcv(symbol)
        print(f"Success! Retrieved {len(df)} rows.")
        print(df.head())
        print(df.tail())
    except Exception as e:
        print(f"Error fetching OHLCV: {e}")

    # 2. Fetch Fundamentals
    print("\n2. Fetching Fundamentals...")
    try:
        fund = repo.get_fundamentals(symbol)
        print("Success! Fundamentals:")
        for k, v in fund.items():
            print(f"  {k}: {v}")
    except Exception as e:
        print(f"Error fetching fundamentals: {e}")
        
    # 3. Verify Cache
    print("\n3. Verifying Cache...")
    cache_path = os.path.join("cache", "ohlcv", f"{symbol}.csv")
    if os.path.exists(cache_path):
        print(f"Cache file exists: {cache_path}")
    else:
        print(f"Cache file missing: {cache_path}")

if __name__ == "__main__":
    main()
