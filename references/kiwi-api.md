# Kiwi Tequila API Reference

## Authentication

API key in header: `apikey: {KIWI_API_KEY}`

Register at: tequila.kiwi.com/portal

## Key Feature: Virtual Interlining

Kiwi's unique capability — combines flights from different airlines into a single itinerary that no airline or standard aggregator sells as one ticket. Example: VietJet HAN→BKK + Scoot BKK→SIN as one booking.

This is the primary reason to use Kiwi alongside Amadeus.

## Endpoints Used

### 1. Search Flights
`GET /v2/search`

| Param | Required | Description |
|-------|----------|-------------|
| fly_from | Yes | IATA code, city code, or "lat-lng-radius" |
| fly_to | Yes | Same format as fly_from |
| date_from | Yes | DD/MM/YYYY (departure range start) |
| date_to | Yes | DD/MM/YYYY (departure range end) |
| return_from | No | DD/MM/YYYY (return range start) |
| return_to | No | DD/MM/YYYY (return range end) |
| adults | No | Default: 1 |
| children | No | Ages 2-11 |
| infants_in_seat | No | Ages 0-2 |
| selected_cabins | No | M (economy), W (premium), C (business), F (first) |
| max_stopovers | No | Max connections (default: unlimited) |
| curr | No | Currency code (default: EUR) |
| limit | No | Max results |
| sort | No | "price", "duration", "quality" |
| asc | No | 1 ascending, 0 descending |
| vehicle_type | No | "aircraft" to exclude buses/trains |

**Date format note:** Kiwi uses DD/MM/YYYY, NOT YYYY-MM-DD.

Response structure:
```json
{
  "data": [
    {
      "id": "abc123",
      "price": 456,
      "currency": "USD",
      "deep_link": "https://www.kiwi.com/deep?...",
      "booking_token": "token...",
      "duration": {"total": 49500, "departure": 49500, "return": 0},
      "route": [
        {
          "flyFrom": "HAN",
          "flyTo": "BKK",
          "local_departure": "2024-06-15T08:00:00.000Z",
          "local_arrival": "2024-06-15T10:30:00.000Z",
          "airline": "VJ",
          "flight_no": 901
        },
        {
          "flyFrom": "BKK",
          "flyTo": "SIN",
          "local_departure": "2024-06-15T13:00:00.000Z",
          "local_arrival": "2024-06-15T16:20:00.000Z",
          "airline": "TR",
          "flight_no": 615
        }
      ],
      "bags_price": {"1": 35.5, "2": 70.0},
      "availability": {"seats": 5}
    }
  ],
  "search_id": "search_abc",
  "currency": "USD"
}
```

### 2. Check Flights
`GET /v2/booking/check_flights`

Validates that a specific itinerary is still available and confirms current price.

| Param | Required | Description |
|-------|----------|-------------|
| booking_token | Yes | From search results |
| bnum | Yes | Number of adults |
| children | No | Number of children |
| infants | No | Number of infants |
| currency | No | Currency code |

### 3. Search Locations
`GET /locations/query`

| Param | Required | Description |
|-------|----------|-------------|
| term | Yes | Search text (e.g., "hanoi") |
| location_types | No | "airport", "city", "country" |
| limit | No | Max results |

## Rate Limits
- Free tier: ~100 searches/day
- Paid plans available for higher volume
- No `Retry-After` header — use exponential backoff on 429

## Important Notes
- Prices are always **all-inclusive** (taxes + fees included)
- `bags_price` shows additional cost per checked bag (not included in base)
- `deep_link` opens the booking page on kiwi.com
- `booking_token` is needed for `check_flights` validation
- Virtual interlining itineraries have multiple airlines in the `route` array
