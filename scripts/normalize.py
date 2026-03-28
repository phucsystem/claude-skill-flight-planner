#!/usr/bin/env python3
"""Shared normalization utilities: price standardization, deduplication, formatting."""

import json
from datetime import datetime


# --- Unified Flight Object Schema ---
# All functions output/expect this format:
# {
#   "id": str,                    # Unique identifier
#   "source": "amadeus"|"kiwi",   # Data source
#   "airlines": [str],            # Operating carrier codes
#   "flight_numbers": [str],      # e.g., ["VN302", "UA870"]
#   "origin": str,                # IATA code
#   "destination": str,           # IATA code
#   "departure": str,             # ISO datetime
#   "arrival": str,               # ISO datetime
#   "duration_minutes": int,      # Total travel time
#   "stops": int,                 # Number of stops
#   "stop_airports": [str],       # IATA codes of stop airports
#   "cabin_class": str,           # ECONOMY, BUSINESS, etc.
#   "price_total": float,         # All-inclusive price in target currency
#   "price_currency": str,        # Currency code
#   "price_breakdown": {          # Detailed breakdown
#       "base": float,
#       "taxes": float,
#       "fees": float,
#   },
#   "segments": [dict],           # Raw segment data
#   "booking_url": str|None,      # Direct booking link if available
#   "booking_token": str|None,    # Kiwi booking token
#   "virtual_interlining": bool,  # True if multi-airline combo
#   "baggage_included": str|None, # Included baggage info
#   "raw": dict,                  # Original API response for this offer
# }


def normalize_amadeus_offer(offer, dictionaries=None):
    """Convert Amadeus flight offer to unified format."""
    segments = []
    flight_numbers = []
    airlines = set()
    stop_airports = []

    for itin in offer.get("itineraries", []):
        for seg in itin.get("segments", []):
            carrier = seg.get("carrierCode", "")
            airlines.add(carrier)
            flight_numbers.append(f"{carrier}{seg.get('number', '')}")
            segments.append(seg)
            if seg.get("numberOfStops", 0) > 0:
                for stop in seg.get("stops", []):
                    stop_airports.append(stop.get("iataCode", ""))

    first_seg = segments[0] if segments else {}
    last_seg = segments[-1] if segments else {}

    price_data = offer.get("price", {})
    traveler_prices = offer.get("travelerPricings", [{}])
    base = float(price_data.get("base", 0))
    total = float(price_data.get("grandTotal", price_data.get("total", 0)))
    taxes = total - base

    # Parse duration from first itinerary
    duration_str = offer.get("itineraries", [{}])[0].get("duration", "PT0H0M")
    duration_minutes = _parse_iso_duration(duration_str)

    total_stops = sum(
        len(itin.get("segments", [])) - 1
        for itin in offer.get("itineraries", [])
    )

    return {
        "id": f"amadeus_{offer.get('id', '')}",
        "source": "amadeus",
        "airlines": sorted(airlines),
        "flight_numbers": flight_numbers,
        "origin": first_seg.get("departure", {}).get("iataCode", ""),
        "destination": last_seg.get("arrival", {}).get("iataCode", ""),
        "departure": first_seg.get("departure", {}).get("at", ""),
        "arrival": last_seg.get("arrival", {}).get("at", ""),
        "duration_minutes": duration_minutes,
        "stops": total_stops,
        "stop_airports": stop_airports,
        "cabin_class": traveler_prices[0].get("fareDetailsBySegment", [{}])[0].get("cabin", "ECONOMY"),
        "price_total": total,
        "price_currency": price_data.get("currency", "USD"),
        "price_breakdown": {"base": base, "taxes": taxes, "fees": 0},
        "segments": segments,
        "booking_url": None,
        "booking_token": None,
        "virtual_interlining": False,
        "baggage_included": _extract_amadeus_baggage(traveler_prices),
        "raw": offer,
    }


def normalize_kiwi_itinerary(itin):
    """Convert Kiwi itinerary to unified format."""
    routes = itin.get("route", [])
    airlines = set()
    flight_numbers = []
    stop_airports = []

    for route in routes:
        carrier = route.get("airline", "")
        airlines.add(carrier)
        flight_numbers.append(f"{carrier}{route.get('flight_no', '')}")

    first_route = routes[0] if routes else {}
    last_route = routes[-1] if routes else {}

    # Stopovers (exclude first departure and last arrival)
    if len(routes) > 1:
        stop_airports = [r.get("flyTo", "") for r in routes[:-1]]

    total = float(itin.get("price", 0))
    bags_price = itin.get("bags_price", {})

    return {
        "id": f"kiwi_{itin.get('id', '')}",
        "source": "kiwi",
        "airlines": sorted(airlines),
        "flight_numbers": flight_numbers,
        "origin": first_route.get("flyFrom", ""),
        "destination": last_route.get("flyTo", ""),
        "departure": first_route.get("local_departure", ""),
        "arrival": last_route.get("local_arrival", ""),
        "duration_minutes": int(itin.get("duration", {}).get("total", 0)) // 60,
        "stops": len(routes) - 1,
        "stop_airports": stop_airports,
        "cabin_class": "ECONOMY",  # Kiwi defaults; check route-level for upgrades
        "price_total": total,
        "price_currency": itin.get("currency", "USD") if isinstance(itin.get("currency"), str) else "USD",
        "price_breakdown": {
            "base": total,  # Kiwi prices are all-inclusive
            "taxes": 0,
            "fees": 0,
        },
        "segments": routes,
        "booking_url": itin.get("deep_link", None),
        "booking_token": itin.get("booking_token", None),
        "virtual_interlining": len(airlines) > 1,
        "baggage_included": f"Checked bag: +${bags_price.get('1', 'N/A')}" if bags_price else None,
        "raw": itin,
    }


def deduplicate_flights(flights):
    """
    Remove duplicate flights from combined results.
    Same flight = same flight numbers + same departure time.
    Keep the one with lower price.
    """
    seen = {}
    for f in flights:
        key = (
            tuple(f["flight_numbers"]),
            f["departure"][:16],  # Match to the minute
        )
        if key not in seen or f["price_total"] < seen[key]["price_total"]:
            seen[key] = f
    return list(seen.values())


def sort_by_price(flights):
    """Sort flights by total price ascending."""
    return sorted(flights, key=lambda f: f["price_total"])


def calculate_savings(baseline_price, alternative_price):
    """Calculate savings amount and percentage."""
    savings = baseline_price - alternative_price
    pct = (savings / baseline_price * 100) if baseline_price > 0 else 0
    return {
        "amount": round(savings, 2),
        "percentage": round(pct, 1),
        "baseline": round(baseline_price, 2),
        "alternative": round(alternative_price, 2),
    }


def format_duration(minutes):
    """Convert minutes to human-readable duration."""
    if minutes <= 0:
        return "N/A"
    hours = minutes // 60
    mins = minutes % 60
    if hours == 0:
        return f"{mins}m"
    if mins == 0:
        return f"{hours}h"
    return f"{hours}h {mins}m"


def format_results_table(flights, top_n=None):
    """Format flight results as a markdown table."""
    if top_n:
        flights = flights[:top_n]

    lines = [
        "| # | Airlines | Route | Departure | Duration | Stops | Price | Source |",
        "|---|----------|-------|-----------|----------|-------|-------|--------|",
    ]
    for i, f in enumerate(flights, 1):
        route = f"{f['origin']} → {f['destination']}"
        dep = f["departure"][:16].replace("T", " ") if f["departure"] else "N/A"
        dur = format_duration(f["duration_minutes"])
        airlines = ", ".join(f["airlines"])
        price = f"${f['price_total']:,.0f}"
        source = f["source"]
        vi = " 🔗" if f.get("virtual_interlining") else ""
        lines.append(f"| {i} | {airlines} | {route} | {dep} | {dur} | {f['stops']} | {price} | {source}{vi} |")

    return "\n".join(lines)


# --- Internal helpers ---

def _parse_iso_duration(duration_str):
    """Parse ISO 8601 duration (e.g., PT13H45M) to minutes."""
    if not duration_str or not duration_str.startswith("PT"):
        return 0
    duration_str = duration_str[2:]  # Remove "PT"
    hours = 0
    minutes = 0
    if "H" in duration_str:
        h_part, duration_str = duration_str.split("H")
        hours = int(h_part)
    if "M" in duration_str:
        m_part = duration_str.replace("M", "")
        minutes = int(m_part) if m_part else 0
    return hours * 60 + minutes


def _extract_amadeus_baggage(traveler_pricings):
    """Extract baggage info from Amadeus traveler pricing."""
    if not traveler_pricings:
        return None
    segments = traveler_pricings[0].get("fareDetailsBySegment", [])
    if not segments:
        return None
    bags = segments[0].get("includedCheckedBags", {})
    if bags.get("quantity"):
        return f"{bags['quantity']} checked bag(s) included"
    if bags.get("weight"):
        return f"{bags['weight']}{bags.get('weightUnit', 'KG')} checked baggage"
    return "No checked baggage included"
