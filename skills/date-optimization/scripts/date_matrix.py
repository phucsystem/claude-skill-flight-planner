#!/usr/bin/env python3
"""
Build date-price matrix for finding optimal travel dates.

Usage:
    python date_matrix.py --origin HAN --dest SFO --date 2026-07-15 [--return-date 2026-07-25] [--flex 7] [--adults 1]

Output: JSON with date matrix and top 3 recommendations.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add shared scripts to path
shared_scripts = str(Path(__file__).parent.parent.parent.parent / "scripts")
sys.path.insert(0, shared_scripts)

from config import AMADEUS_API_KEY, KIWI_API_KEY, DEFAULTS


def build_date_range(center_date, flex_days):
    """Generate list of dates around center date."""
    center = datetime.strptime(center_date, "%Y-%m-%d")
    dates = []
    for offset in range(-flex_days, flex_days + 1):
        d = center + timedelta(days=offset)
        if d >= datetime.now():  # Don't include past dates
            dates.append(d.strftime("%Y-%m-%d"))
    return dates


def search_date_matrix_amadeus(origin, dest, departure_date):
    """Use Amadeus Flight Cheapest Date Search."""
    if not AMADEUS_API_KEY:
        return {}

    try:
        from amadeus_client import search_date_matrix
        result = search_date_matrix(origin, dest, departure_date)
        prices = {}
        for offer in result.get("data", []):
            date = offer.get("departureDate", "")
            price = float(offer.get("price", {}).get("total", 0))
            if date and price:
                prices[date] = price
        return prices
    except Exception as e:
        print(f"WARNING: Amadeus date matrix failed: {e}", file=sys.stderr)
        return {}


def search_date_range_kiwi(origin, dest, date_from, date_to, return_from=None,
                           return_to=None, adults=1):
    """Use Kiwi search with date range to get prices per date."""
    if not KIWI_API_KEY:
        return {}

    try:
        from kiwi_client import search_flights

        def to_kiwi(d):
            parts = d.split("-")
            return f"{parts[2]}/{parts[1]}/{parts[0]}"

        result = search_flights(
            fly_from=origin,
            fly_to=dest,
            date_from=to_kiwi(date_from),
            date_to=to_kiwi(date_to),
            return_from=to_kiwi(return_from) if return_from else None,
            return_to=to_kiwi(return_to) if return_to else None,
            adults=adults,
            limit=50,
        )

        prices = {}
        for itin in result.get("data", []):
            dep_date = itin.get("local_departure", "")[:10] if itin.get("local_departure") else ""
            # For Kiwi route data
            routes = itin.get("route", [])
            if routes:
                dep_date = routes[0].get("local_departure", "")[:10]
            price = float(itin.get("price", 0))
            if dep_date and price:
                if dep_date not in prices or price < prices[dep_date]:
                    prices[dep_date] = price
        return prices
    except Exception as e:
        print(f"WARNING: Kiwi date range search failed: {e}", file=sys.stderr)
        return {}


def apply_day_of_week_pattern(base_price, date_str):
    """Estimate price adjustment based on day of week (AI-knowledge fallback)."""
    day = datetime.strptime(date_str, "%Y-%m-%d").weekday()
    # 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    adjustments = {
        0: 0.95,   # Monday: slightly cheaper
        1: 0.85,   # Tuesday: cheapest
        2: 0.87,   # Wednesday: cheap
        3: 0.95,   # Thursday: slightly cheaper
        4: 1.15,   # Friday: expensive
        5: 1.05,   # Saturday: moderate
        6: 1.12,   # Sunday: expensive
    }
    return round(base_price * adjustments.get(day, 1.0), 2)


def build_matrix(origin, dest, depart_date, return_date, flex_days, adults=1):
    """Build the full date-price matrix."""
    depart_dates = build_date_range(depart_date, flex_days)

    # Try API-based search first
    api_prices = {}
    if KIWI_API_KEY and depart_dates:
        api_prices = search_date_range_kiwi(
            origin, dest,
            date_from=depart_dates[0],
            date_to=depart_dates[-1],
            adults=adults,
        )

    if not api_prices and AMADEUS_API_KEY:
        api_prices = search_date_matrix_amadeus(origin, dest, depart_date)

    # Build matrix
    matrix = {}
    for d in depart_dates:
        if d in api_prices:
            matrix[d] = api_prices[d]
        else:
            # Fallback: AI-knowledge pattern
            # Use average API price as base, or a reasonable estimate
            avg_price = sum(api_prices.values()) / len(api_prices) if api_prices else 500
            matrix[d] = apply_day_of_week_pattern(avg_price, d)

    return matrix


def find_top_combinations(matrix, return_matrix=None, top_n=3):
    """Find top N cheapest date combinations."""
    if return_matrix:
        combos = []
        for dep_date, dep_price in matrix.items():
            for ret_date, ret_price in return_matrix.items():
                if ret_date > dep_date:
                    combos.append({
                        "departure": dep_date,
                        "return": ret_date,
                        "total": round(dep_price + ret_price, 2),
                        "departure_price": dep_price,
                        "return_price": ret_price,
                        "departure_day": datetime.strptime(dep_date, "%Y-%m-%d").strftime("%A"),
                        "return_day": datetime.strptime(ret_date, "%Y-%m-%d").strftime("%A"),
                    })
        combos.sort(key=lambda x: x["total"])
        return combos[:top_n]
    else:
        # One-way
        sorted_dates = sorted(matrix.items(), key=lambda x: x[1])
        return [
            {
                "departure": d,
                "total": round(p, 2),
                "departure_day": datetime.strptime(d, "%Y-%m-%d").strftime("%A"),
            }
            for d, p in sorted_dates[:top_n]
        ]


def main():
    parser = argparse.ArgumentParser(description="Date optimization matrix")
    parser.add_argument("--origin", required=True, help="Origin IATA code")
    parser.add_argument("--dest", required=True, help="Destination IATA code")
    parser.add_argument("--date", required=True, help="Target departure date YYYY-MM-DD")
    parser.add_argument("--return-date", help="Target return date YYYY-MM-DD")
    parser.add_argument("--flex", type=int, default=7, help="Flexibility in days (default: 7)")
    parser.add_argument("--adults", type=int, default=1)
    parser.add_argument("--top", type=int, default=3, help="Top N recommendations")
    args = parser.parse_args()

    print(f"Building date matrix for {args.origin} → {args.dest}...")
    print(f"Target: {args.date}" + (f" / Return: {args.return_date}" if args.return_date else " (one-way)"))
    print(f"Flexibility: ±{args.flex} days\n")

    # Build outbound matrix
    matrix = build_matrix(args.origin, args.dest, args.date, args.return_date, args.flex, args.adults)

    # Build return matrix if round trip
    return_matrix = None
    if args.return_date:
        return_matrix = build_matrix(args.dest, args.origin, args.return_date, None, args.flex, args.adults)

    # Find top combinations
    top = find_top_combinations(matrix, return_matrix, args.top)

    # Output
    result = {
        "origin": args.origin,
        "destination": args.dest,
        "target_departure": args.date,
        "target_return": args.return_date,
        "flexibility_days": args.flex,
        "outbound_prices": matrix,
        "return_prices": return_matrix,
        "top_combinations": top,
        "data_source": "api" if (AMADEUS_API_KEY or KIWI_API_KEY) else "ai_knowledge_pattern",
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
