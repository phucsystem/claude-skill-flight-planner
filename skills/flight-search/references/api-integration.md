# Kiwi Tequila API Integration Guide

## Overview

Kiwi Tequila API is the primary data source for real-time flight search with virtual interlining support. Free for developers.

## Setup

1. Register at https://tequila.kiwi.com/
2. Create an application → get API key
3. Store API key in environment variable: `KIWI_API_KEY`

## Key Endpoints

### Search Flights
```
GET https://api.tequila.kiwi.com/v2/search
```

**Parameters:**
| Param | Required | Example | Description |
|-------|----------|---------|-------------|
| fly_from | Yes | HAN | Origin IATA code |
| fly_to | Yes | SFO | Destination IATA code |
| date_from | Yes | 15/06/2026 | Start of departure range (dd/mm/yyyy) |
| date_to | Yes | 30/06/2026 | End of departure range |
| return_from | No | 25/06/2026 | Start of return range |
| return_to | No | 10/07/2026 | End of return range |
| adults | No | 2 | Number of adults (default: 1) |
| children | No | 1 | Number of children (2-11) |
| infants | No | 0 | Number of infants (< 2) |
| selected_cabins | No | M | M=economy, W=premium_eco, C=business, F=first |
| curr | No | USD | Currency code |
| locale | No | en | Language |
| max_stopovers | No | 2 | Maximum number of stops |
| max_fly_duration | No | 30 | Max flight time in hours |
| sort | No | price | Sort by: price, duration, quality |
| limit | No | 20 | Max results (default: 200) |

**Response structure** (key fields):
```json
{
  "data": [{
    "id": "flight_id",
    "price": 520,
    "airlines": ["VJ", "UA"],
    "route": [{
      "flyFrom": "HAN",
      "flyTo": "ICN",
      "airline": "VJ",
      "flight_no": 123,
      "local_departure": "2026-06-16T08:00:00",
      "local_arrival": "2026-06-16T14:30:00"
    }, {
      "flyFrom": "ICN",
      "flyTo": "SFO",
      "airline": "UA",
      "flight_no": 892,
      "local_departure": "2026-06-16T18:00:00",
      "local_arrival": "2026-06-16T12:00:00"
    }],
    "duration": {"departure": 64800, "return": 0, "total": 64800},
    "bags_price": {"1": 45, "2": 80},
    "availability": {"seats": 5},
    "virtual_interlining": true,
    "deep_link": "https://www.kiwi.com/deep?..."
  }]
}
```

### Location Search
```
GET https://api.tequila.kiwi.com/locations/query
```

Use to resolve city names to IATA codes:
```
?term=Ho Chi Minh City&location_types=airport
```

## Rate Limits & Best Practices

- No hard published rate limit, but use responsibly
- Cache results for 15 minutes (prices don't change by the second)
- Use `sort=price` and `limit=20` to reduce payload
- Include `curr=USD` for consistent price comparison
- The `deep_link` field provides a direct booking URL on Kiwi.com

## Error Handling

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 200 | Success | Parse results |
| 400 | Bad request | Check parameters |
| 401 | Unauthorized | Verify API key |
| 429 | Rate limited | Wait 60 seconds, retry |
| 500 | Server error | Retry after 30 seconds |

## Script Usage

```bash
python scripts/kiwi_search.py --from HAN --to SFO --depart 2026-06-16 --return 2026-06-25 --adults 2 --children 1
```

Output: JSON file with normalized results ready for skill consumption.
