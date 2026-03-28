---
name: route-optimization
description: Use when direct flights are expensive and traveler is open to layovers. Triggers on cheaper route, alternative routing, transit hub, is a layover worth it, save money with connection.
---

# Route Optimization - Tối Ưu Lộ Trình Qua Điểm Trung Chuyển

## Purpose

Most travelers search for direct flights by default. They don't know that routing through a strategic hub can save $200-500 with only 2-3 extra hours. This skill quantifies that trade-off precisely: "Is $350 savings worth 2.5 extra hours?"

## Input Required

- `origin`, `destination` (IATA codes)
- `baseline_price` and `baseline_duration` from flight-search (direct/fastest option)
- `travel_purpose` from profile (business travelers value time more)
- `risk_tolerance` from profile

## Execution Steps

### Step 1: Establish Baseline

The baseline is the direct or fastest route found by flight-search:

```
BASELINE: HAN → SFO
  Price: $1,100 | Duration: 13.5h (direct, VN Airlines)
  This is the benchmark everything else is compared against.
```

### Step 2: Identify Strategic Hubs

Based on the origin-destination pair, select top hub candidates:

**Decision logic for hub selection:**

| O&D Region | Top Hubs to Check | Why |
|-----------|-------------------|-----|
| Vietnam → US West | ICN, NRT, TPE, HKG | Short detour, competitive pricing |
| Vietnam → US East | DOH, IST, ICN | Middle East hubs or Pacific routing |
| Vietnam → Europe | IST, DOH, DXB, BKK | Turkish=cheapest, Gulf=quality |
| Vietnam → Oceania | SIN, KUL, BKK | LCC connections available |
| Vietnam → Japan | TPE, HKG | Short detour for cheaper fares |
| Intra-Vietnam | No hubs needed | Direct always optimal |

### Step 3: Calculate Each Alternative Route

For each hub route, compute:

```
savings_usd     = baseline_price - hub_route_price
extra_hours     = hub_route_duration - baseline_duration
savings_per_hour = savings_usd / extra_hours
```

**Value rating system:**

| $/hour saved | Rating | Recommendation |
|-------------|--------|---------------|
| > $100/hr | ⭐⭐⭐ Excellent | Always worth it |
| $50-100/hr | ⭐⭐ Good | Worth it for most travelers |
| $25-50/hr | ⭐ Acceptable | Worth it if flexible |
| < $25/hr | ❌ Poor | Only for extreme budget |

### Step 4: Flag Special Considerations

For each alternative route, check:

1. **Transit visa required?**
   - China (PEK/PVG): YES - Transit visa needed for most nationalities
   - Japan (NRT/HND): NO - Transit without visa up to 72h
   - Korea (ICN): NO - Transit without visa, KTAV required
   - Singapore (SIN): NO - Transit up to 96h
   - Turkey (IST): NO - Most nationalities okay

2. **Ground transportation needed?**
   - Some "hub" routes require train/bus between airports
   - Flag with cost estimate (e.g., "Train FRA→city center €4, taxi €35")

3. **Minimum connection time?**
   - International-International: min 2h (recommended 3h)
   - Different terminal: add 1h buffer
   - Immigration required at hub: add 1.5h

4. **Layover quality?**
   - IST: Excellent (lounges, transit hotel, long opening hours)
   - SIN: Excellent (Jewel, free city tour)
   - ICN: Excellent (transit hotel, culture center)
   - DOH: Very good (Al Maha lounge, transit hotel)
   - BKK: Good but terminal change can be tiring

### Step 5: Present Results

```
ROUTE ALTERNATIVES vs BASELINE: HAN → SFO ($1,100, 13.5h)

#  Via Hub    Price   Saved   Extra Time  $/Hour   Rating
1  ICN       $750    $350    +3.0h       $117/hr  ⭐⭐⭐ Excellent
2  NRT       $820    $280    +2.5h       $112/hr  ⭐⭐⭐ Excellent
3  TPE       $790    $310    +4.0h       $78/hr   ⭐⭐ Good
4  IST       $680    $420    +8.0h       $53/hr   ⭐⭐ Good
5  BKK+NRT   $620    $480    +12.0h      $40/hr   ⭐ Acceptable

RECOMMENDATION (moderate risk tolerance):
  Route via ICN: Best value at $117/hr saved.
  You save $350 and only add 3 hours (1 layover at Incheon, one of Asia's
  best airports with transit hotel and free showers).

NOTE: Route 5 involves ground+air combination. See details below.
```

### Step 6: Ground Transport Flag

If any route involves non-flight segments:

```
⚠️ GROUND TRANSPORT REQUIRED:
  Route 5 (BKK+NRT): Requires separate VietJet HAN→BKK, then
  overnight in Bangkok, then BKK→NRT→SFO next day.
  Additional costs: Hotel $30-50, airport transfer $10-15
  Net savings after ground costs: $415-445
```

## Traveler Type Adjustments

| Profile | Threshold | Recommendation Bias |
|---------|-----------|-------------------|
| Business | > $100/hr | Only recommend ⭐⭐⭐ routes |
| Leisure | > $50/hr | Recommend ⭐⭐ and above |
| Budget/Remote | > $25/hr | All rated options |
| Family w/ kids | > $75/hr | Penalize 2+ stop routes, long layovers |

## Limitations

- Hub pricing is estimated in AI-Knowledge mode
- Actual hub connections depend on schedule alignment (checked by flight-search if API active)
- Ground transport costs are approximate and vary by time of day
