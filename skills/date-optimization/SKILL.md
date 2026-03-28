---
name: date-optimization
description: "Use when traveler has flexible dates and wants to find the cheapest departure/return combination. Triggers on: cheapest day to fly, flexible dates, when to book, price calendar."
allowed-tools: Bash(python *), Read
---

# Date Optimization - Quét Ngày Bay Tối Ưu

## Purpose

Find the optimal departure and return dates within a flexible range. Instead of checking prices day-by-day, this skill builds a complete price matrix and identifies the cheapest combinations with clear explanations.

## Input Required

From orchestrator profile:
- `origin`, `destination` (IATA codes)
- `departure_date` (target)
- `return_date` (target, if round-trip)
- `flexibility`: low (±2d) | medium (±7d) | high (±14d)

## Execution Steps

### Step 1: Build Date Range

Calculate the full search window:
- Depart window: `departure_date - flex_days` to `departure_date + flex_days`
- Return window: `return_date - flex_days` to `return_date + flex_days`
- Total combinations: `(flex_days * 2 + 1)²` for round-trip

Example (±7 days): 15 × 15 = 225 date combinations to evaluate.

### Step 2: Apply Pricing Patterns (AI-Knowledge Mode)

Use these established pricing patterns to estimate relative costs:

**Day-of-week patterns:**
- Tuesday, Wednesday: typically 15-25% cheaper (lowest demand)
- Friday, Sunday: typically 10-20% more expensive (weekend travel peaks)
- Saturday departure: sometimes cheap (contra-flow)

**Seasonal patterns:**
- Refer to `references/pricing-patterns.md` for route-specific seasonality

**Advance purchase effect:**
- 21+ days ahead: best domestic fares
- 45-60 days ahead: best international fares
- < 7 days: premium pricing (last-minute surge)
- Exception: LCCs sometimes release last-minute deals

**Holiday surcharges:**
- Vietnamese holidays: Tet (+50-100%), 30/4-1/5 (+30-50%), 2/9 (+20-30%)
- US holidays: Thanksgiving, Christmas, July 4th (+30-60%)
- School holidays: June-August (+20-40% on leisure routes)

### Step 3: Score Each Combination

For each date pair, calculate a relative price score (1-10):
```
score = base_pattern + day_of_week_factor + seasonal_factor + advance_purchase_factor
```

### Step 4: Generate Output

**Format: Price Heatmap (text-based)**

```
           Return →  Mon  Tue  Wed  Thu  Fri  Sat  Sun
Depart ↓
  Mon 15/6           $$   $    $    $$   $$$  $$   $$$
  Tue 16/6           $    $    $    $    $$   $$   $$
  Wed 17/6           $    $    $    $    $$   $$   $$$
  Thu 18/6           $$   $    $    $$   $$$  $$   $$$
  Fri 19/6           $$$  $$   $$   $$   $$$  $$$  $$$
```

Legend: `$` = cheapest tier, `$$` = mid-range, `$$$` = most expensive

**TOP 3 Recommendations:**

For each recommendation, provide:
1. Specific dates (depart + return)
2. Estimated savings vs target date
3. WHY this combination is cheap (not just "it's cheaper")
   - Example: "Tuesday departure avoids weekend premium. Mid-week return catches post-business-travel low."
4. Trade-off: what user gives up (e.g., "1 fewer weekend day at destination")

### Step 5: Pass Forward

Send to `flight-search` skill:
```
optimal_dates: [
  {depart: "2026-06-16", return: "2026-06-25", confidence: "high"},
  {depart: "2026-06-17", return: "2026-06-24", confidence: "high"},
  {depart: "2026-06-15", return: "2026-06-23", confidence: "medium"}
]
```

## API-Enhanced Mode

When Kiwi Tequila API is available, replace Step 2-3 with real price data:
- Use `/v2/search` with `date_from` and `date_to` parameters
- Set `fly_days` to cover the full flexibility range
- Real prices replace pattern-based estimates

## Limitations

- AI-Knowledge mode provides relative rankings, not exact prices
- Holiday pricing can be unpredictable (flash sales, last-minute changes)
- Pattern accuracy decreases for niche routes with irregular schedules
