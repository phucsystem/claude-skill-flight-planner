# Amadeus Self-Service API Reference

## Authentication

OAuth2 Client Credentials flow:
```
POST /v1/security/oauth2/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id={API_KEY}&client_secret={API_SECRET}
```
Response: `{ "access_token": "...", "expires_in": 1799 }`

All subsequent requests: `Authorization: Bearer {access_token}`

## Endpoints Used

### 1. Flight Offers Search v2
`GET /v2/shopping/flight-offers`

| Param | Required | Description |
|-------|----------|-------------|
| originLocationCode | Yes | IATA code (e.g., "HAN") |
| destinationLocationCode | Yes | IATA code (e.g., "SFO") |
| departureDate | Yes | YYYY-MM-DD |
| returnDate | No | YYYY-MM-DD (omit for one-way) |
| adults | Yes | 1-9 |
| children | No | 0-8 |
| travelClass | No | ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST |
| nonStop | No | "true" for direct flights only |
| currencyCode | No | ISO 4217 (default: EUR) |
| max | No | Max results 1-250 (default: 250) |

Response structure:
```json
{
  "data": [
    {
      "id": "1",
      "itineraries": [{
        "duration": "PT13H45M",
        "segments": [{
          "departure": {"iataCode": "HAN", "at": "2024-06-15T08:00:00"},
          "arrival": {"iataCode": "NRT", "at": "2024-06-15T15:00:00"},
          "carrierCode": "VN",
          "number": "302",
          "numberOfStops": 0
        }]
      }],
      "price": {
        "currency": "USD",
        "total": "856.00",
        "base": "720.00",
        "grandTotal": "856.00"
      },
      "travelerPricings": [{
        "fareDetailsBySegment": [{
          "cabin": "ECONOMY",
          "includedCheckedBags": {"quantity": 1}
        }]
      }]
    }
  ],
  "dictionaries": {
    "carriers": {"VN": "Vietnam Airlines"}
  }
}
```

### 2. Flight Cheapest Date Search
`GET /v1/shopping/flight-dates`

| Param | Required | Description |
|-------|----------|-------------|
| origin | Yes | IATA code |
| destination | Yes | IATA code |
| departureDate | No | YYYY-MM-DD (default: today) |
| oneWay | No | "true"/"false" |
| viewBy | No | "DATE", "DURATION", "WEEK" |

Returns cheapest prices for each available date in the range.

### 3. Flight Inspiration Search
`GET /v1/shopping/flight-destinations`

| Param | Required | Description |
|-------|----------|-------------|
| origin | Yes | IATA code |
| maxPrice | No | Max price filter |

Returns cheapest destinations from a given origin — useful for discovering cheap hub connections.

## Rate Limits
- **Test:** 1 request per 100ms, 10 requests/second
- **Production:** Higher limits based on plan
- Response header `X-RateLimit-Remaining` tracks quota

## Error Codes
| Code | Meaning | Action |
|------|---------|--------|
| 401 | Token expired | Refresh token and retry |
| 429 | Rate limited | Wait `Retry-After` seconds |
| 400 | Bad request | Check parameters |
| 500 | Server error | Retry with backoff |

## Test Environment
- Base URL: `https://test.api.amadeus.com`
- Returns realistic but synthetic data
- Free, no credit card required
- Register at: developers.amadeus.com
