# Traveler Profile Schema

## Contents
- [JSON Schema](#json-schema)
- [Required Fields](#required-fields)
- [Optional Fields](#optional-fields)
- [Corporate-Only Fields](#corporate-only-fields)
- [Profile Inference Rules](#profile-inference-rules)
- [Collection Strategy](#collection-strategy)
- [How Skills Use Profile](#how-skills-use-profile)

## Overview

The traveler profile is collected once by the Orchestrator and passed to all sub-skills. Each skill uses relevant fields to customize its analysis.

## JSON Schema

```json
{
  "trip": {
    "origin": "HAN",              // * IATA code or city name
    "destination": "SFO",         // * IATA code or city name
    "departure_date": "2026-07-15",  // * YYYY-MM-DD or descriptive ("mid-June")
    "return_date": null,          // YYYY-MM-DD or null for one-way
    "trip_type": "round_trip"     // "one_way" | "round_trip" | "multi_city"
  },
  "passengers": {
    "adults": 1,                  // * 1-9
    "children": 0,                // Ages 2-11
    "infants": 0                  // Ages 0-2
  },
  "baggage": "carry_on",         // "carry_on" | "checked_1" | "checked_2" | "oversize"
  "cabin_class": "economy",      // "economy" | "premium_economy" | "business" | "first"
  "flexibility": "medium",       // "low" (±2d) | "medium" (±7d) | "high" (±14d)
  "risk_tolerance": "moderate",  // "conservative" | "moderate" | "aggressive"
  "budget_max": null,            // Max total price USD, null = no limit
  "loyalty_programs": [],        // Airline IATA codes: ["VN", "UA"]
  "preferred_airlines": [],      // IATA codes, empty = no preference
  "avoided_airlines": [],        // IATA codes to exclude
  "booking_type": "personal",    // "personal" | "corporate"
  "travel_purpose": "leisure",   // "business" | "leisure" | "remote_work"
  "corporate": {                 // Only when booking_type = "corporate"
    "company_name": "",
    "annual_flight_volume": 0,   // Total company flights/year
    "annual_spend": 0,           // USD
    "corporate_card": false,
    "travel_policy_restrictions": []
  }
}
```

## Field Reference

### Required Fields

| Field | Type | Example | Used By |
|-------|------|---------|---------|
| `origin` | string (IATA/city) | "HAN" or "Hanoi" | All skills |
| `destination` | string (IATA/city) | "SFO" or "San Francisco" | All skills |
| `departure_date` | date or range | "2026-06-15" or "mid-June" | date-optimization, flight-search |
| `passengers` | object | `{adults: 2, children: 1, infants: 1}` | flight-search, fee-analysis |

### Optional Fields

| Field | Default | Options | Used By |
|-------|---------|---------|---------|
| `return_date` | null (one-way) | Any date after departure | date-optimization, flight-search |
| `flexibility` | medium | low (±2d), medium (±7d), high (±14d) | date-optimization |
| `baggage` | carry_on | carry_on, checked_1, checked_2, oversize | fee-analysis |
| `booking_type` | personal | personal, corporate | negotiation-email |
| `loyalty_programs` | [] | Airline IATA codes | fee-analysis, flexibility |
| `risk_tolerance` | moderate | conservative, moderate, aggressive | flexibility-analysis, hidden-city |
| `cabin_class` | economy | economy, premium_economy, business, first | flight-search |
| `travel_purpose` | leisure | business, leisure, remote_work | route-optimization |
| `budget_max` | null | Any positive number (USD) | All search skills |

### Corporate-Only Fields

| Field | Type | Example | Used By |
|-------|------|---------|---------|
| `company_name` | string | "TechCorp Vietnam" | negotiation-email |
| `annual_flight_volume` | number | 120 | negotiation-email |
| `annual_spend` | number | 500000 (USD) | negotiation-email |
| `corporate_card` | boolean | true | hidden-city (eligibility gate) |
| `travel_policy_restrictions` | string[] | ["economy only", "max 1 stop"] | All skills |

## Profile Inference Rules

When user gives minimal input, infer intelligently:

1. **"HAN to SFO next month"** → origin=HAN, destination=SFO, departure=next month mid, flexibility=medium, passengers=1 adult
2. **"Family trip to Phu Quoc"** → assume 2 adults + 2 children, baggage=checked_1, purpose=leisure
3. **"Business trip SGN-HAN weekly"** → booking_type=corporate, flexibility=low, baggage=carry_on
4. **"Cheapest way to get to Bangkok"** → risk_tolerance=aggressive, flexibility=high, cabin=economy

## Collection Strategy

Collect in 2 rounds for better UX:

**Round 1 (required):** origin, destination, dates, number of travelers
**Round 2 (if optimizing):** baggage, flexibility, loyalty, budget, travel purpose

For quick searches, Round 1 is sufficient. Full optimization benefits from both rounds.

## How Skills Use Profile

| Skill | Key Fields | How Used |
|-------|-----------|----------|
| date-optimization | flexibility, departure_date | Determines search window width |
| flight-search | All required + cabin, preferred/avoided airlines | Filters and sorts results |
| route-optimization | travel_purpose, risk_tolerance | Weighs time vs money tradeoff |
| fee-analysis | baggage, loyalty_programs | Calculates true_total per option |
| deals-verification | loyalty_programs, booking_type | Matches eligible deals |
| negotiation-email | Corporate fields | Builds negotiation leverage |
| flexibility-analysis | risk_tolerance | Calibrates break-even threshold |
| hidden-city-strategy | baggage, corporate_card, loyalty | Eligibility gate checks |
