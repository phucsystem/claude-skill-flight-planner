---
name: flight-search
description: Use when searching for flights, comparing airlines, or finding virtual interlining combinations across multiple carriers. Triggers on find flights, search routes, compare airlines, best price.
---

# Flight Search - Tìm Route Combination Ẩn

## Purpose

Find the best flight options by searching across multiple data sources, including virtual interlining combinations that standard search engines don't show. This is where the biggest savings happen - a combination of two separate tickets from different airlines can be 30-40% cheaper than any single-airline itinerary.

## Input Required

From orchestrator:
- `origin`, `destination` (IATA codes)
- `departure_date`, `return_date`
- `passengers` (count + types)
- `cabin_class`
- `preferred_airlines`, `avoided_airlines` (optional)
- `optimal_dates` from date-optimization (if available)

## Execution Steps

### Step 1: Determine Search Strategy

Based on route type, choose data sources:

| Route Type | Primary Source | Secondary | Virtual Interlining |
|-----------|---------------|-----------|-------------------|
| Domestic VN | AI Knowledge (VN carriers) | Kiwi Tequila | Low value |
| Intra-Asia | Kiwi Tequila | AI Knowledge | HIGH value |
| Intercontinental | Kiwi Tequila | AI Knowledge | HIGHEST value |

### Step 2: AI-Knowledge Search

For each route, generate estimated options using airline knowledge:

**Known carrier pricing tiers** (estimate ranges):

| Carrier Type | Example | Domestic VN | Asia Short-haul | Intercontinental |
|-------------|---------|------------|----------------|-----------------|
| LCC | VietJet, AirAsia | $30-80 | $50-200 | $300-600 |
| Mid-tier | Bamboo, Scoot | $50-120 | $80-300 | $400-800 |
| Legacy | VN Airlines, SQ | $80-200 | $150-500 | $600-1500 |
| Premium | Emirates, QR | N/A | $200-600 | $800-2500 |

Adjust estimates based on:
- Season and day-of-week (from date-optimization)
- Route competition level (more carriers = lower prices)
- Advance purchase timing

### Step 3: Virtual Interlining Analysis

This is the KEY differentiator. Identify potential virtual interlining combinations:

**Pattern**: Route A→B has no cheap direct option, but:
- Carrier X has cheap A→C (transit hub)
- Carrier Y has cheap C→B
- Combined: A→C + C→B on separate tickets = cheaper than any A→B single ticket

**Common virtual interlining opportunities**:

| Origin | Destination | Via Hub | Typical Savings |
|--------|------------|---------|----------------|
| HAN | SFO | ICN (Korean Air/Asiana → United/Alaska) | 20-35% |
| SGN | CDG | BKK (VietJet → Thai/AF) | 15-30% |
| HAN | SYD | SIN (VietJet → Scoot/Jetstar) | 25-40% |
| SGN | NRT | TPE (VietJet → Peach/Vanilla) | 20-35% |

**Virtual interlining risks to flag:**
- No protection if first flight is delayed (buy travel insurance)
- Separate check-in required at transit point
- Must self-transfer baggage
- Need sufficient layover time (minimum 3 hours international, 2 hours domestic)

### Step 4: Normalize and Deduplicate Results

For ALL options regardless of source:

1. **Price normalization**: Ensure every price includes:
   - Base fare
   - Mandatory taxes and surcharges
   - Fuel surcharge
   - Airport fees
   - Currency conversion to user's preferred currency

2. **Deduplication**: If same flight appears from multiple sources:
   - Keep entry with lowest price
   - Note the source in metadata

3. **Tag each option**:
   - `[DIRECT]` - Point-to-point, no stops
   - `[1-STOP]` - One connection, same airline/alliance
   - `[2-STOP]` - Two connections
   - `[INTERLINING]` - Virtual interlining (separate tickets)
   - `[LCC]` - Low-cost carrier
   - `[LEGACY]` - Full-service carrier

### Step 5: Sort and Present

Sort by `true_total_price` (ascending). Present top 10:

```
#  Route                    Airlines        Adv.Price  True Total  Tags
1. HAN→ICN→SFO             VJ+UA           $520       $595        [INTERLINING][LCC+LEGACY]
2. HAN→NRT→SFO             VN+UA           $680       $710        [1-STOP][LEGACY]
3. HAN→BKK→SFO             VJ+CX+UA        $490       $620        [2-STOP][INTERLINING]
4. HAN→SFO                 VN              $1,100     $1,100      [DIRECT][LEGACY]
5. HAN→TPE→SFO             VJ+EVA           $550       $630        [INTERLINING][LCC+LEGACY]
```

Highlight: "Options 1, 3, 5 are virtual interlining - NOT available on Google Flights or standard aggregators."

### Step 6: Pass Forward

Send to downstream skills:
- `flight_options[]` → fee-analysis (for true cost calculation)
- `baseline_direct` → route-optimization (for comparison)
- `fare_classes[]` → flexibility-analysis

## API-Enhanced Mode (Kiwi Tequila)

When API is configured, execute:
1. Read `references/api-integration.md` for setup
2. Run `../../scripts/kiwi_client.py` with parameters
3. Merge API results with AI-knowledge estimates
4. Real prices override estimates for matching routes

## Important Notes

- Virtual interlining is NOT codeshare - user buys separate tickets
- Always warn: "If flight 1 is delayed, flight 2 is NOT protected"
- Recommend: "Consider travel insurance for virtual interlining itineraries"
- For families with children < 2: virtual interlining adds significant complexity
