---
name: deals-verification
description: Use when looking for airline promo codes, flash sales, or credit card discounts before booking. Triggers on promo code, discount, sale, deal, coupon, cashback, loyalty discount.
---

# Deals Verification - Liệt Kê Deal Tiềm Năng

## Purpose

Stop wasting 30 minutes searching expired promo codes on Google. This skill leverages AI knowledge of airline promotional patterns, credit card partnerships, and seasonal deals to compile a curated list of potential savings, each tagged with a confidence level.

## Critical Disclaimer

> **⚠️ MANDATORY DISCLAIMER** (must appear in every output):
> All deals listed are based on AI knowledge of airline programs and promotional patterns. They have NOT been verified through live booking APIs. Always test at checkout before relying on any code. Expiry dates and conditions may have changed since AI's training data.

## Input Required

- `airlines[]` from flight-search results
- `route` (origin → destination)
- `travel_dates`
- `booking_type` (personal/corporate)
- `loyalty_programs[]` from profile
- `payment_methods` (credit cards available)

## Execution Steps

### Step 1: Categorize Deal Sources

Search knowledge across these categories (ordered by reliability):

**Category A: Airline Official Programs** (High confidence)
- Airline's own sales (e.g., VietJet "Vé 0 đồng", AirAsia "Big Sale")
- Early bird pricing (usually 60-90 days ahead)
- Airline birthday/anniversary sales (recurring dates)
- Route launch promotions
- Companion fares for loyalty members

**Category B: Card & Partner Deals** (Medium confidence)
- Credit card airline partners (e.g., Techcombank-VN Airlines)
- Bank points redemption programs
- Corporate partner rates
- Travel aggregator exclusive codes

**Category C: Public Coupon Codes** (Low confidence)
- Aggregator coupon sites (RetailMeNot, etc.)
- Social media flash codes
- Email newsletter exclusive codes
- Influencer/affiliate codes

### Step 2: Match Deals to Route and Dates

For each potential deal, verify applicability:

1. Does it apply to this `route`?
2. Does it apply to these `travel_dates`?
3. Does it apply to this `fare_class`?
4. Is the `booking_window` still open?
5. Are there `minimum_spend` requirements?

### Step 3: Output Format

```
DEALS FOUND FOR: VietJet, HAN → SGN, Jun 15-25, 2026

#  Deal                          Confidence  Savings   Conditions
─────────────────────────────────────────────────────────────────
1  VietJet SkyBoss Upgrade       HIGH        10-15%    Book through app, 
   Promo (recurring monthly)                           available first week
   
2  Techcombank Visa Payment      MEDIUM      5-8%      Pay with Techcombank
   Discount                                            Visa credit card
   
3  VietJet "0 VND base fare"     HIGH        70-90%    Base fare only,
   Flash Sale (quarterly)                              specific dates, 
                                                       limited inventory,
                                                       tax/fees still apply
                                                       
4  RetailMeNot: VJETFLY10        LOW         $10 off   Unverified, possibly
                                                       expired, US bookings
                                                       only?

5  [EXPIRED] VietJet Tet 2026    EXPIRED     Was 20%   Ended Feb 15, 2026
   Early Bird                                          Listed for reference
```

### Step 4: Recurring Sale Calendar

Provide a calendar of known recurring airline sales:

**Vietnamese Carriers:**
| Airline | Sale Type | Typical Timing | Discount |
|---------|-----------|---------------|----------|
| VietJet | Flash Sale "0 VND" | Monthly (varies) | 70-90% base fare |
| VietJet | Birthday Sale (Dec) | December | 15-30% |
| VN Airlines | "Bay La Yeu" | Seasonal | 10-20% |
| VN Airlines | Tet Early Bird | Oct-Nov | 15-25% for Tet travel |
| Bamboo | Route Launch | Varies | 30-50% for new routes |

**International Carriers:**
| Airline | Sale Type | Typical Timing | Discount |
|---------|-----------|---------------|----------|
| AirAsia | Big Sale | Quarterly (Mar, Jun, Sep, Nov) | 20-50% |
| Scoot | Take-Off Tuesday | Tuesdays | 10-30% |
| Korean Air | Global Sale | 2-3x per year | 15-25% |
| Singapore Airlines | Early Bird | 45-60 days ahead | 10-15% |
| Turkish Airlines | Spring/Fall Campaign | Mar-Apr, Sep-Oct | 15-25% |

### Step 5: Credit Card Deal Matching

If user has credit card information:

| Card Bank | Airline Partner | Benefit |
|-----------|----------------|---------|
| Techcombank Visa | Vietnam Airlines | 5-8% discount, bonus miles |
| Vietcombank JCB | VietJet | Payment cashback 3-5% |
| HSBC Premier | Multiple | Airport lounge access, insurance |
| Citibank Prestige | Global | 4th night free hotel, airline credits |

### Step 6: Actionable Recommendations

For the top 3 most promising deals:
1. Exact steps to apply the deal
2. Booking channel required (app/web/phone)
3. Deadline to act
4. What to do if the code doesn't work at checkout

## Important Notes

- NEVER guarantee a deal will work - always qualify with confidence level
- Expired deals are listed as `[EXPIRED]` but kept for reference (pattern recognition)
- AI knowledge has a training cutoff - newest promotions may be missed
- Recommend user also check: airline's social media, email newsletters, fare alert services
