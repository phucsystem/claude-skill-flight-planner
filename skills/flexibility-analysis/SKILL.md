---
name: flexibility-analysis
description: Use when deciding between flexible and non-refundable tickets, or when travel plans might change. Triggers on refundable vs non-refundable, cancel risk, change fee, should I buy flexible ticket.
---

# Flexibility Analysis - Phân Tích Rủi Ro Linh Hoạt

## Purpose

Prevent the "$150 savings that costs $720" scenario. When travelers buy non-refundable tickets to save money, they're making an implicit bet that their plans won't change. This skill makes that bet explicit with break-even probability analysis.

## Input Required

- `flight_options[]` with fare classes from flight-search
- `risk_tolerance` from profile
- `schedule_certainty` (user estimate: "How sure are you this trip happens as planned?")
  - 95-100%: Very certain (confirmed meetings, events)
  - 80-94%: Likely but could change
  - 50-79%: Uncertain (tentative plans)
  - < 50%: Very uncertain

## Execution Steps

### Step 1: Score Each Option (Flexibility Score 0-100)

Calculate based on fare rules:

```
flex_score = change_score (0-30)
           + cancel_score (0-30)
           + rebooking_score (0-20)
           + protection_score (0-20)
```

**Change Score (0-30):**
- Free unlimited changes: 30
- Free change, fare diff only: 25
- Change with fee < $50: 20
- Change with fee $50-100: 15
- Change with fee $100-200: 10
- Change with high fee (> $200): 5
- No changes allowed: 0

**Cancel Score (0-30):**
- Full cash refund: 30
- Full credit voucher (12+ months): 20
- Partial refund (50%+): 15
- Credit voucher (< 12 months): 10
- Cancel fee > 50% of ticket: 5
- Non-refundable, no credit: 0

**Rebooking Score (0-20):**
- Same fare class guaranteed: 20
- Subject to availability, same cabin: 15
- Subject to availability, any cabin: 10
- Rebooked on different airline: 5
- No rebooking: 0

**Protection Score (0-20):**
- Covered by travel insurance included: 20
- 24-hour free cancellation applies: 10
- Credit card trip protection: 10
- No protection: 0

### Step 2: Scenario Costing

For each option, calculate cost under 3 scenarios:

| Scenario | What Happens | Cost |
|----------|-------------|------|
| **As planned** | Nothing changes | ticket_price |
| **Date change ±2 days** | Need to shift by 2 days | change_fee + fare_diff_estimate |
| **Full cancellation** | Trip doesn't happen | ticket_price - refund_amount |
| **No-show** | Miss the flight | ticket_price (total loss) |

Present as table:

```
SCENARIO COSTING: HAN → SFO

                    Saver ($750)     Flex ($920)      Refundable ($1,100)
As planned          $750             $920             $1,100
Change ±2 days      $750+$100+diff   $920+$0+diff     $1,100+$0+diff
Full cancel         $750 → $0 lost   $920 → $750 credit  $1,100 → $1,050 refund
No-show             $750 lost        $920 lost**      $1,100 → $900 credit**

** Some airlines forfeit no-show even on flex tickets
```

### Step 3: Break-Even Analysis

The key calculation: "At what probability of needing to change does the flexible ticket become the better deal?"

```
Formula:
  premium = flex_price - saver_price
  loss_if_cancel = saver_price - saver_refund
  break_even_probability = premium / loss_if_cancel × 100

Example:
  Saver: $750 (refund: $0)
  Flex:  $920 (refund: $750 credit)
  
  Premium: $920 - $750 = $170
  Loss if cancel saver: $750 - $0 = $750
  
  Break-even: $170 / $750 = 22.7%
  
  → If there's more than a 23% chance your plans change,
    the Flex ticket is the smarter financial decision.
```

### Step 4: Hidden Terms Alert

Flag terms that travelers often miss:

- **Minimum stay**: Some fares require staying minimum 3 nights or including a Saturday
- **Blackout dates**: Fare not valid during peak periods
- **Credit voucher validity**: Often 12 months from issue date, not from original travel date
- **Name change**: Most tickets don't allow name changes (affects corporate rebooking)
- **Route restriction**: Credit may only apply to same route
- **Fare class on rebooking**: Original fare class may not be available at change time
- **No-show penalty**: Even Flex tickets may forfeit value on no-show (must cancel BEFORE departure)

### Step 5: Recommendation

Based on break-even analysis + user's schedule_certainty:

```
FLEXIBILITY RECOMMENDATION:

Your schedule certainty: 75% (uncertain)
Break-even probability: 23%
Your implied change probability: 25% (100% - 75%)

Since 25% > 23% → BUY THE FLEX TICKET ($920)

Expected cost calculation:
  Saver: 75% × $750 + 25% × $750(lost) = $750 guaranteed, but
         risk-adjusted: $750 + 25% × $750 = $938 expected cost
  Flex:  $920 guaranteed, with $750 credit if canceled
         risk-adjusted: 75% × $920 + 25% × $170 = $733 expected cost

  Flex ticket saves you $205 in expected value.
```

### Step 6: Output Scorecard

```
FLEXIBILITY SCORECARD

Option              Price   Flex Score   Break-even   Recommendation
Saver Economy       $750    15/100       -            Only if 95%+ certain
Flex Economy        $920    65/100       23%          ✅ Best for your profile
Full Refundable     $1,100  95/100       47%          Only if < 53% certain
Business Flex       $2,400  90/100       N/A          Overkill for this trip
```

## Reference

Read `references/fare-class-rules.md` for airline-specific fare class breakdown.

## Limitations

- Fare difference on rebooking is unpredictable (estimated at ±$50-200)
- Break-even assumes binary outcome (trip happens or doesn't)
- In reality, partial changes (date shift) have different costs than full cancel
- Corporate travel policies may override personal preference
