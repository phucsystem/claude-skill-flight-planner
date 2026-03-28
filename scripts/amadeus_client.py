#!/usr/bin/env python3
"""Amadeus Self-Service API client with OAuth2 token management."""

import time
import json
import requests
from pathlib import Path

# Import config from same directory
import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import AMADEUS_API_KEY, AMADEUS_API_SECRET, AMADEUS_BASE_URL, DEFAULTS

# --- Token Cache ---
_token_cache = {"access_token": None, "expires_at": 0}


def get_token():
    """Get OAuth2 access token, refreshing if expired."""
    if _token_cache["access_token"] and time.time() < _token_cache["expires_at"] - 60:
        return _token_cache["access_token"]

    resp = requests.post(
        f"{AMADEUS_BASE_URL}/v1/security/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": AMADEUS_API_KEY,
            "client_secret": AMADEUS_API_SECRET,
        },
        timeout=DEFAULTS["request_timeout"],
    )
    resp.raise_for_status()
    data = resp.json()
    _token_cache["access_token"] = data["access_token"]
    _token_cache["expires_at"] = time.time() + data.get("expires_in", 1799)
    return _token_cache["access_token"]


def _request(method, endpoint, params=None, json_body=None, retries=None):
    """Make authenticated request with retry on 401/429."""
    if retries is None:
        retries = DEFAULTS["max_retries"]

    for attempt in range(retries + 1):
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}

        try:
            resp = requests.request(
                method,
                f"{AMADEUS_BASE_URL}{endpoint}",
                headers=headers,
                params=params,
                json=json_body,
                timeout=DEFAULTS["request_timeout"],
            )
        except requests.Timeout:
            if attempt < retries:
                time.sleep(2 ** attempt)
                continue
            raise

        if resp.status_code == 401:
            _token_cache["access_token"] = None  # Force refresh
            continue

        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 2 ** attempt))
            time.sleep(retry_after)
            continue

        resp.raise_for_status()
        return resp.json()

    raise Exception(f"Amadeus API failed after {retries + 1} attempts")


def search_flights(origin, destination, departure_date, adults=None, return_date=None,
                   cabin_class=None, max_results=None, non_stop=False):
    """
    Flight Offers Search v2 (GET).

    Args:
        origin: IATA airport code (e.g., "HAN")
        destination: IATA airport code (e.g., "SFO")
        departure_date: "YYYY-MM-DD"
        adults: Number of adult travelers (default from config)
        return_date: "YYYY-MM-DD" for round trip, None for one-way
        cabin_class: ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST
        max_results: Max number of results
        non_stop: If True, only direct flights

    Returns:
        dict with "data" (list of flight offers) and "dictionaries" (carrier codes, etc.)
    """
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": adults or DEFAULTS["adults"],
        "travelClass": cabin_class or DEFAULTS["cabin_class"],
        "max": max_results or DEFAULTS["max_results"],
        "currencyCode": DEFAULTS["currency"],
        "nonStop": "true" if non_stop else "false",
    }
    if return_date:
        params["returnDate"] = return_date

    return _request("GET", "/v2/shopping/flight-offers", params=params)


def search_date_matrix(origin, destination, departure_date=None, one_way=False,
                       view_by="DATE"):
    """
    Flight Cheapest Date Search.

    Args:
        origin: IATA code
        destination: IATA code
        departure_date: "YYYY-MM-DD" (optional, defaults to today)
        one_way: If True, one-way only
        view_by: "DATE" or "DURATION" or "WEEK"

    Returns:
        dict with "data" (list of cheapest date offers)
    """
    params = {
        "origin": origin,
        "destination": destination,
        "oneWay": "true" if one_way else "false",
        "viewBy": view_by,
    }
    if departure_date:
        params["departureDate"] = departure_date

    return _request("GET", "/v1/shopping/flight-dates", params=params)


def get_inspiration(origin, max_price=None):
    """
    Flight Inspiration Search - discover cheapest destinations from origin.

    Args:
        origin: IATA code
        max_price: Maximum price filter (USD)

    Returns:
        dict with "data" (list of cheapest destination offers)
    """
    params = {"origin": origin}
    if max_price:
        params["maxPrice"] = max_price

    return _request("GET", "/v1/shopping/flight-destinations", params=params)


if __name__ == "__main__":
    # Quick test
    from config import validate_keys
    validate_keys("amadeus")
    print("Token:", get_token()[:20] + "...")
    print("Amadeus client ready. Base URL:", AMADEUS_BASE_URL)
