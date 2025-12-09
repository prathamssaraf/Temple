"""
Verification script for Temple API.

This script demonstrates the API endpoints using HTTP requests.
Run the API server first: python -m uvicorn api.main:app --reload
"""

import requests
import json
from time import sleep


API_BASE_URL = "http://localhost:8000"


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"{title}")
    print(f"{'='*70}")


def demo_health_check():
    """Demo 1: Health check."""
    print_section("DEMO 1: Health Check")

    # API health
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"\nAPI Health: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

    # Scanner health
    response = requests.get(f"{API_BASE_URL}/api/v1/scanner/health")
    print(f"\nScanner Health: {response.status_code}")
    print(json.dumps(response.json(), indent=2))


def demo_list_universes():
    """Demo 2: List available universes."""
    print_section("DEMO 2: List Stock Universes")

    response = requests.get(f"{API_BASE_URL}/api/v1/scanner/universes")
    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\nAvailable Universes:")
        for universe in data['universes']:
            print(f"  - {universe['name']}: {universe['description']} ({universe['symbol_count']} stocks)")


def demo_example_patterns():
    """Demo 3: Get example patterns."""
    print_section("DEMO 3: Example Patterns")

    response = requests.get(f"{API_BASE_URL}/api/v1/patterns/examples")
    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        patterns = response.json()
        print(f"\nExample Patterns:")
        for i, pattern in enumerate(patterns, 1):
            print(f"\n{i}. {pattern['name']}")
            print(f"   {pattern['description']}")
            print(f"   Frequency: {pattern['frequency']['min_occurrences']} times in {pattern['frequency']['timeframe_days']} days")


def demo_pattern_match():
    """Demo 4: Match pattern against a single stock."""
    print_section("DEMO 4: Pattern Matching")

    pattern_request = {
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

    print(f"\nMatching pattern '{pattern_request['pattern']['name']}' against {pattern_request['symbol']}...")

    response = requests.post(
        f"{API_BASE_URL}/api/v1/patterns/match",
        json=pattern_request
    )

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"\nResults:")
        print(f"  Symbol: {result['symbol']}")
        print(f"  Matched: {result['matched']}")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  Occurrences: {result['occurrences']}")
        print(f"  Timeframe: {result['timeframe_start']} to {result['timeframe_end']}")

        if result['occurrence_details']:
            print(f"\n  Occurrence Details:")
            for i, occ in enumerate(result['occurrence_details'][:3], 1):
                print(f"    {i}. {occ['start_date']} to {occ['end_date']} (confidence: {occ['confidence']:.2%})")


def demo_scan_symbols():
    """Demo 5: Scan multiple symbols."""
    print_section("DEMO 5: Scan Multiple Symbols")

    scan_request = {
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
        "min_confidence": 0.6,
        "parallel": True
    }

    print(f"\nScanning {len(scan_request['symbols'])} symbols...")
    print(f"Pattern: {scan_request['pattern']['name']}")
    print(f"Min Confidence: {scan_request['min_confidence']}")

    response = requests.post(
        f"{API_BASE_URL}/api/v1/scanner/scan",
        json=scan_request
    )

    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"\nScan Results:")
        print(f"  Total Scanned: {result['total_symbols']}")
        print(f"  Successful: {result['successful_scans']}")
        print(f"  Failed: {result['failed_scans']}")
        print(f"  Matches Found: {result['matches_found']}")
        print(f"  Average Confidence: {result['average_confidence']:.2%}")
        print(f"  Duration: {result['duration_seconds']:.2f}s")

        if result['results']:
            print(f"\n  Top Matches:")
            matches = [r for r in result['results'] if r['matched']]
            matches.sort(key=lambda x: x['confidence'], reverse=True)
            for i, match in enumerate(matches[:5], 1):
                print(f"    {i}. {match['symbol']}: {match['confidence']:.2%} ({match['occurrences']} times)")


def demo_scan_universe():
    """Demo 6: Scan a universe."""
    print_section("DEMO 6: Scan Universe")

    scan_request = {
        "universe": "tech",
        "pattern": {
            "name": "Support Bounce",
            "description": "Price bounces off support",
            "sequence": [],
            "frequency": {
                "min_occurrences": 2,
                "timeframe_days": 90
            }
        },
        "min_confidence": 0.65,
        "parallel": True
    }

    print(f"\nScanning '{scan_request['universe']}' universe...")
    print(f"Pattern: {scan_request['pattern']['name']}")
    print(f"Min Confidence: {scan_request['min_confidence']}")

    response = requests.post(
        f"{API_BASE_URL}/api/v1/scanner/scan",
        json=scan_request
    )

    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"\nScan Results:")
        print(f"  Total Scanned: {result['total_symbols']}")
        print(f"  Matches Found: {result['matches_found']}")
        print(f"  Average Confidence: {result['average_confidence']:.2%}")
        print(f"  Duration: {result['duration_seconds']:.2f}s")

        if result['results']:
            print(f"\n  Top 5 Matches:")
            matches = [r for r in result['results'] if r['matched']]
            matches.sort(key=lambda x: x['confidence'], reverse=True)
            for i, match in enumerate(matches[:5], 1):
                print(f"    {i}. {match['symbol']}: {match['confidence']:.2%}")


def main():
    """Run all API verification demos."""
    print("\n" + "="*70)
    print("TEMPLE REST API - VERIFICATION")
    print("="*70)
    print(f"\nAPI Base URL: {API_BASE_URL}")
    print("\nMake sure the API server is running:")
    print("  python -m uvicorn api.main:app --reload")

    # Wait a moment for user to see message
    print("\nStarting demos in 2 seconds...")
    sleep(2)

    try:
        # Run all demos
        demo_health_check()
        demo_list_universes()
        demo_example_patterns()
        demo_pattern_match()
        demo_scan_symbols()
        demo_scan_universe()

        print("\n" + "="*70)
        print("[OK] ALL DEMOS COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\nThe Temple API is working correctly!")
        print("\nNext steps:")
        print("  1. Integrate with frontend dashboard")
        print("  2. Add authentication and rate limiting")
        print("  3. Deploy to production")

    except requests.exceptions.ConnectionError:
        print("\n[X] Error: Could not connect to API server")
        print("\nPlease start the API server first:")
        print("  python -m uvicorn api.main:app --reload")
    except Exception as e:
        print(f"\n[X] Error during verification: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
