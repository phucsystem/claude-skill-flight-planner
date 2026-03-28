#!/usr/bin/env python3
"""
Parallel flight search across Amadeus + Kiwi APIs.
Normalizes, deduplicates, and sorts results by true total price.

Usage:
    python parallel_search.py --origin HAN --dest SFO --date 2026-07-15 [--return-date 2026-07-25] [--adults 2] [--cabin ECONOMY]

Output: JSON array of unified flight objects to stdout.
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Add shared scripts to path
shared_scripts = str(Path(__file__).parent.parent.parent.parent / "scripts")
sys.path.insert(0, shared_scripts)

from config import AMADEUS_API_KEY, KIWI_API_KEY, DEFAULTS
from normalize import (
    normalize_amadeus_offer,
    normalize_kiwi_itinerary,
    deduplicate_flights,
    sort_by_price,
    format_results_table,
)


def search_amadeus(origin, dest, date, return_date=None, adults=1, cabin="ECONOMY"):
    """Search Amadeus API. Returns list of unified flight objects."""
    if not AMADEUS_API_KEY:
        return []

    try:
        from amadeus_client import search_flights
        result = search_flights(
            origin=origin,
            destination=dest,
            departure_date=date,
            return_date=return_date,
            adults=adults,
            cabin_class=cabin,
        )
        dictionaries = result.get("dictionaries", {})
        return [
            normalize_amadeus_offer(offer, dictionaries)
            for offer in result.get("data", [])
        ]
    except Exception as e:
        print(f"WARNING: Amadeus search failed: {e}", file=sys.stderr)
        return []


def search_kiwi(origin, dest, date, return_date=None, adults=1, cabin="M"):
    """Search Kiwi API with virtual interlining. Returns list of unified flight objects."""
    if not KIWI_API_KEY:
        return []

    try:
        from kiwi_client import search_flights

        # Convert YYYY-MM-DD to DD/MM/YYYY for Kiwi
        def to_kiwi_date(d):
            if not d:
                return None
            parts = d.split("-")
            return f"{parts[2]}/{parts[1]}/{parts[0]}"

        cabin_map = {"ECONOMY": "M", "PREMIUM_ECONOMY": "W", "BUSINESS": "C", "FIRST": "F"}

        result = search_flights(
            fly_from=origin,
            fly_to=dest,
            date_from=to_kiwi_date(date),
            date_to=to_kiwi_date(date),
            return_from=to_kiwi_date(return_date) if return_date else None,
            return_to=to_kiwi_date(return_date) if return_date else None,
            adults=adults,
            cabin_class=cabin_map.get(cabin, "M"),
        )
        return [
            normalize_kiwi_itinerary(itin)
            for itin in result.get("data", [])
        ]
    except Exception as e:
        print(f"WARNING: Kiwi search failed: {e}", file=sys.stderr)
        return []


def parallel_search(origin, dest, date, return_date=None, adults=1, cabin="ECONOMY"):
    """Run Amadeus + Kiwi searches in parallel, normalize, dedup, sort."""
    with ThreadPoolExecutor(max_workers=2) as executor:
        amadeus_future = executor.submit(
            search_amadeus, origin, dest, date, return_date, adults, cabin
        )
        kiwi_future = executor.submit(
            search_kiwi, origin, dest, date, return_date, adults, cabin
        )

        amadeus_results = amadeus_future.result()
        kiwi_results = kiwi_future.result()

    all_flights = amadeus_results + kiwi_results

    if not all_flights:
        return []

    # Deduplicate and sort
    deduped = deduplicate_flights(all_flights)
    sorted_flights = sort_by_price(deduped)

    return sorted_flights


def main():
    parser = argparse.ArgumentParser(description="Parallel flight search")
    parser.add_argument("--origin", required=True, help="Origin IATA code")
    parser.add_argument("--dest", required=True, help="Destination IATA code")
    parser.add_argument("--date", required=True, help="Departure date YYYY-MM-DD")
    parser.add_argument("--return-date", help="Return date YYYY-MM-DD")
    parser.add_argument("--adults", type=int, default=1, help="Number of adults")
    parser.add_argument("--cabin", default="ECONOMY", help="Cabin class")
    parser.add_argument("--format", choices=["json", "table"], default="table", help="Output format")
    parser.add_argument("--top", type=int, default=10, help="Top N results")
    args = parser.parse_args()

    results = parallel_search(
        origin=args.origin,
        dest=args.dest,
        date=args.date,
        return_date=args.return_date,
        adults=args.adults,
        cabin=args.cabin,
    )

    if not results:
        print("No flights found. Check API keys and parameters.", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        # Remove 'raw' field for cleaner output
        clean = [{k: v for k, v in f.items() if k != "raw"} for f in results[:args.top]]
        print(json.dumps(clean, indent=2, default=str))
    else:
        print(f"\nFound {len(results)} flights. Top {min(args.top, len(results))}:\n")
        print(format_results_table(results, top_n=args.top))

        # Summary
        if results:
            cheapest = results[0]
            vi_count = sum(1 for f in results if f.get("virtual_interlining"))
            print(f"\nCheapest: ${cheapest['price_total']:,.0f} ({', '.join(cheapest['airlines'])})")
            print(f"Virtual interlining options: {vi_count}")


if __name__ == "__main__":
    main()
