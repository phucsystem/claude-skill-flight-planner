#!/usr/bin/env python3
"""Shared configuration for Travel Optimization Engine API clients."""

import os
import sys

# --- API Credentials (from environment variables) ---
AMADEUS_API_KEY = os.environ.get("AMADEUS_API_KEY", "")
AMADEUS_API_SECRET = os.environ.get("AMADEUS_API_SECRET", "")
KIWI_API_KEY = os.environ.get("KIWI_API_KEY", "")

# --- Base URLs ---
# Amadeus: switch to production by setting AMADEUS_ENV=production
AMADEUS_ENV = os.environ.get("AMADEUS_ENV", "test")
AMADEUS_BASE_URL = (
    "https://api.amadeus.com" if AMADEUS_ENV == "production"
    else "https://test.api.amadeus.com"
)

# Kiwi Tequila
KIWI_BASE_URL = "https://api.tequila.kiwi.com"

# --- Default Search Parameters ---
DEFAULTS = {
    "adults": 1,
    "children": 0,
    "infants": 0,
    "currency": "USD",
    "max_stops": 2,
    "cabin_class": "ECONOMY",  # ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST
    "max_results": 20,
    "request_timeout": 30,  # seconds
    "max_retries": 3,
}


def validate_keys(*required_keys):
    """Check that required API keys are set. Exit with message if missing."""
    missing = []
    key_map = {
        "amadeus": (AMADEUS_API_KEY, AMADEUS_API_SECRET),
        "kiwi": (KIWI_API_KEY,),
    }
    for key_name in required_keys:
        values = key_map.get(key_name, ())
        if any(not v for v in values):
            missing.append(key_name.upper())
    if missing:
        print(f"ERROR: Missing API keys for: {', '.join(missing)}", file=sys.stderr)
        print("Set environment variables: AMADEUS_API_KEY, AMADEUS_API_SECRET, KIWI_API_KEY", file=sys.stderr)
        sys.exit(1)
