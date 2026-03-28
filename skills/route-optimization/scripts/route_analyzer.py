#!/usr/bin/env python3
"""
Analyze alternative routes through connecting hubs.
Compares hub-based itineraries against direct flights with savings/hour metric.

Usage:
    python route_analyzer.py --origin HAN --dest SFO --baseline-price 1100 --baseline-duration 810 [--adults 1]

Output: JSON with hub alternatives and savings analysis.
"""

import argparse
import json
import sys
from pathlib import Path

# Add shared scripts to path
shared_scripts = str(Path(__file__).parent.parent.parent.parent / "scripts")
sys.path.insert(0, shared_scripts)

from config import AMADEUS_API_KEY, KIWI_API_KEY
from normalize import calculate_savings, format_duration

# Strategic hub database keyed by region pair
HUB_DATABASE = {
    # Vietnam → US West Coast
    ("VN", "US_WEST"): [
        {"hub": "ICN", "name": "Seoul Incheon", "typical_extra_hours": 3.0, "typical_savings_pct": 25},
        {"hub": "NRT", "name": "Tokyo Narita", "typical_extra_hours": 2.5, "typical_savings_pct": 20},
        {"hub": "TPE", "name": "Taipei Taoyuan", "typical_extra_hours": 4.0, "typical_savings_pct": 28},
        {"hub": "HKG", "name": "Hong Kong", "typical_extra_hours": 3.5, "typical_savings_pct": 15},
    ],
    # Vietnam → US East Coast
    ("VN", "US_EAST"): [
        {"hub": "ICN", "name": "Seoul Incheon", "typical_extra_hours": 4.0, "typical_savings_pct": 22},
        {"hub": "DOH", "name": "Doha", "typical_extra_hours": 5.0, "typical_savings_pct": 25},
        {"hub": "IST", "name": "Istanbul", "typical_extra_hours": 6.0, "typical_savings_pct": 30},
    ],
    # Vietnam → Europe
    ("VN", "EU"): [
        {"hub": "IST", "name": "Istanbul", "typical_extra_hours": 4.0, "typical_savings_pct": 30},
        {"hub": "DOH", "name": "Doha", "typical_extra_hours": 3.5, "typical_savings_pct": 25},
        {"hub": "BKK", "name": "Bangkok", "typical_extra_hours": 3.0, "typical_savings_pct": 20},
        {"hub": "DXB", "name": "Dubai", "typical_extra_hours": 4.5, "typical_savings_pct": 22},
    ],
    # Vietnam → Oceania
    ("VN", "OC"): [
        {"hub": "SIN", "name": "Singapore", "typical_extra_hours": 2.5, "typical_savings_pct": 25},
        {"hub": "KUL", "name": "Kuala Lumpur", "typical_extra_hours": 3.0, "typical_savings_pct": 30},
        {"hub": "BKK", "name": "Bangkok", "typical_extra_hours": 3.5, "typical_savings_pct": 20},
    ],
    # Vietnam → Japan/Korea
    ("VN", "JP_KR"): [
        {"hub": "TPE", "name": "Taipei", "typical_extra_hours": 2.0, "typical_savings_pct": 20},
        {"hub": "HKG", "name": "Hong Kong", "typical_extra_hours": 2.5, "typical_savings_pct": 15},
    ],
}

# Region classification for common airports
AIRPORT_REGIONS = {
    "HAN": "VN", "SGN": "VN", "DAD": "VN", "CXR": "VN", "PQC": "VN",
    "SFO": "US_WEST", "LAX": "US_WEST", "SEA": "US_WEST", "SJC": "US_WEST",
    "JFK": "US_EAST", "EWR": "US_EAST", "IAD": "US_EAST", "BOS": "US_EAST",
    "ORD": "US_EAST", "ATL": "US_EAST", "MIA": "US_EAST",
    "CDG": "EU", "LHR": "EU", "FRA": "EU", "AMS": "EU", "FCO": "EU",
    "SYD": "OC", "MEL": "OC", "BNE": "OC", "AKL": "OC",
    "NRT": "JP_KR", "HND": "JP_KR", "KIX": "JP_KR", "ICN": "JP_KR",
}

# Transit visa requirements
TRANSIT_VISA = {
    "PEK": True, "PVG": True,  # China: visa usually required
    "ICN": False, "NRT": False, "HND": False, "SIN": False,
    "BKK": False, "KUL": False, "HKG": False, "TPE": False,
    "IST": False, "DOH": False, "DXB": False, "AMS": False,
}

# Layover quality ratings
LAYOVER_QUALITY = {
    "IST": "Excellent (lounges, transit hotel, shops 24/7)",
    "SIN": "Excellent (Jewel, free city tour, transit hotel)",
    "ICN": "Excellent (transit hotel, culture center, spa)",
    "DOH": "Very Good (Al Maha lounge, transit hotel)",
    "NRT": "Good (lounges, shops, but can feel dated)",
    "TPE": "Good (lounges, efficient layout)",
    "HKG": "Good (but terminal changes can be long)",
    "BKK": "Good (but terminal change is tiring)",
    "KUL": "Good (KLIA2 for LCCs is basic)",
    "DXB": "Very Good (extensive shopping, lounges)",
}


def classify_route(origin, destination):
    """Determine region pair for hub lookup."""
    origin_region = AIRPORT_REGIONS.get(origin)
    dest_region = AIRPORT_REGIONS.get(destination)
    return (origin_region, dest_region)


def get_hub_candidates(origin, destination):
    """Get relevant hub airports for this route."""
    region_pair = classify_route(origin, destination)
    candidates = HUB_DATABASE.get(region_pair, [])

    # Also check reverse for return routing
    reverse_pair = (region_pair[1], region_pair[0]) if region_pair[0] and region_pair[1] else None
    if reverse_pair and reverse_pair in HUB_DATABASE:
        candidates = candidates or HUB_DATABASE[reverse_pair]

    return candidates


def search_hub_route_api(origin, hub, destination, date, adults=1):
    """Try to get real price for hub route via API."""
    if not KIWI_API_KEY:
        return None

    try:
        from kiwi_client import search_flights

        def to_kiwi(d):
            parts = d.split("-")
            return f"{parts[2]}/{parts[1]}/{parts[0]}"

        # Search origin → destination via hub
        result = search_flights(
            fly_from=origin,
            fly_to=destination,
            date_from=to_kiwi(date),
            date_to=to_kiwi(date),
            adults=adults,
            limit=5,
        )

        # Filter for results that go through our hub
        for itin in result.get("data", []):
            routes = itin.get("route", [])
            stop_airports = [r.get("flyTo", "") for r in routes[:-1]]
            if hub in stop_airports:
                return {
                    "price": float(itin.get("price", 0)),
                    "duration_minutes": int(itin.get("duration", {}).get("total", 0)) // 60,
                    "source": "kiwi_api",
                }
        return None
    except Exception:
        return None


def analyze_hub_routes(origin, destination, baseline_price, baseline_duration_min,
                       date=None, adults=1, max_alternatives=5):
    """Analyze all hub alternatives and compute savings metrics."""
    candidates = get_hub_candidates(origin, destination)

    if not candidates:
        return {
            "baseline": {
                "route": f"{origin} → {destination}",
                "price": baseline_price,
                "duration": format_duration(baseline_duration_min),
            },
            "alternatives": [],
            "message": f"No strategic hubs found for {origin} → {destination}. Direct route is recommended.",
        }

    alternatives = []
    for hub_info in candidates:
        hub = hub_info["hub"]

        # Try API first
        api_result = None
        if date:
            api_result = search_hub_route_api(origin, hub, destination, date, adults)

        if api_result:
            price = api_result["price"]
            duration_min = api_result["duration_minutes"]
            source = "api"
        else:
            # Estimate based on typical patterns
            price = round(baseline_price * (1 - hub_info["typical_savings_pct"] / 100), 2)
            duration_min = baseline_duration_min + int(hub_info["typical_extra_hours"] * 60)
            source = "estimate"

        extra_hours = (duration_min - baseline_duration_min) / 60
        savings = calculate_savings(baseline_price, price)

        if savings["amount"] <= 0:
            continue  # Skip if no savings

        savings_per_hour = round(savings["amount"] / extra_hours, 2) if extra_hours > 0 else float("inf")

        # Rating
        if savings_per_hour >= 100:
            rating = "Excellent"
            rating_stars = 3
        elif savings_per_hour >= 50:
            rating = "Good"
            rating_stars = 2
        elif savings_per_hour >= 25:
            rating = "Acceptable"
            rating_stars = 1
        else:
            rating = "Poor"
            rating_stars = 0

        alternatives.append({
            "hub": hub,
            "hub_name": hub_info["name"],
            "route": f"{origin} → {hub} → {destination}",
            "price": price,
            "duration_minutes": duration_min,
            "duration": format_duration(duration_min),
            "extra_hours": round(extra_hours, 1),
            "savings_usd": savings["amount"],
            "savings_pct": savings["percentage"],
            "savings_per_hour": savings_per_hour,
            "rating": rating,
            "rating_stars": rating_stars,
            "transit_visa_required": TRANSIT_VISA.get(hub, "Unknown"),
            "layover_quality": LAYOVER_QUALITY.get(hub, "No data"),
            "ground_transport_needed": False,
            "data_source": source,
        })

    # Sort by savings per hour
    alternatives.sort(key=lambda x: x["savings_per_hour"], reverse=True)
    alternatives = alternatives[:max_alternatives]

    return {
        "baseline": {
            "route": f"{origin} → {destination}",
            "price": baseline_price,
            "duration": format_duration(baseline_duration_min),
            "duration_minutes": baseline_duration_min,
        },
        "alternatives": alternatives,
        "best_value": alternatives[0] if alternatives else None,
    }


def main():
    parser = argparse.ArgumentParser(description="Route optimization analyzer")
    parser.add_argument("--origin", required=True, help="Origin IATA code")
    parser.add_argument("--dest", required=True, help="Destination IATA code")
    parser.add_argument("--baseline-price", type=float, required=True, help="Direct flight price USD")
    parser.add_argument("--baseline-duration", type=int, required=True, help="Direct flight duration minutes")
    parser.add_argument("--date", help="Travel date YYYY-MM-DD (for API lookup)")
    parser.add_argument("--adults", type=int, default=1)
    parser.add_argument("--max", type=int, default=5, help="Max alternatives")
    args = parser.parse_args()

    result = analyze_hub_routes(
        origin=args.origin,
        destination=args.dest,
        baseline_price=args.baseline_price,
        baseline_duration_min=args.baseline_duration,
        date=args.date,
        adults=args.adults,
        max_alternatives=args.max,
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
