---
name: fee-analysis
description: "Use when advertised flight price seems too good, or when comparing LCC vs legacy carrier total costs. Triggers on: hidden fees, baggage cost, true price, real cost, checkout surprise."
allowed-tools: Read
---

# Fee Analysis - Phân Tích và Loại Bỏ Phí Phụ Thu

## Purpose

Airlines - especially LCCs - intentionally show low base fares then add fees at checkout. This skill strips away the deception, calculates what you'll actually pay, and re-ranks options by true cost. A $89 Spirit ticket that becomes $275 after fees loses to a $189 Southwest that includes everything.

## Input Required

- `flight_options[]` from flight-search skill
- `baggage` from traveler profile (carry_on | checked_1 | checked_2)
- `loyalty_programs[]` from traveler profile
- `preferred_payment` (credit card type, if known)

## Execution Steps

### Step 1: Load Airline Fee Matrix

Read `references/airline-fee-matrix.md` for comprehensive fee data by airline.

### Step 2: Calculate True Total for Each Option

For each flight option, compute:

```
true_total = base_fare
           + taxes_and_surcharges
           + carry_on_fee          (if LCC and carry_on not included)
           + checked_bag_fee       (× number of bags × number of passengers)
           + seat_selection_fee    (if desired, per passenger)
           + meal_fee              (if not included, long-haul)
           + change_fee_risk       (weighted by probability from flexibility-analysis)
           + payment_surcharge     (credit card fee if applicable)
```

### Step 3: Fee Breakdown Table

Present each option with full fee breakdown:

```
Fee Breakdown: HAN → SFO, 2 Adults + 1 Child

                    Option A (VietJet)    Option B (VN Airlines)   Option C (Korean Air)
Base Fare           $380 × 3 = $1,140     $620 × 3 = $1,860       $580 × 3 = $1,740
Tax & Surcharge     $95 × 3 = $285        $120 × 3 = $360         $110 × 3 = $330
Carry-on (7kg)      Included              Included                 Included
Checked Bag (23kg)  $45 × 3 = $135        Included                 Included
Seat Selection      $12 × 3 = $36         Free                     $15 × 3 = $45
Meal                Not included          Included                 Included
Payment Fee         $0 (debit)            $0                       $0
─────────────────────────────────────────────────────────────────────────
TRUE TOTAL          $1,596                $2,220                   $2,115
Per Person          $532                  $740                     $705
Rank Change         Was #1 → Still #1    Was #3 → Now #3          Was #2 → Now #2
```

### Step 4: Identify Rank Reversals

**Critical insight**: When true_total changes the ranking from advertised price:

```
⚠️ RANK REVERSAL DETECTED:
  Option X was ranked #3 by advertised price ($89)
  After fees, it's actually #5 ($275)
  Option Y was ranked #5 by advertised price ($189)
  After fees, it's actually #2 ($189) - no hidden fees!
```

### Step 5: Fee Avoidance Strategies

For each applicable fee, provide actionable avoidance advice:

**Carry-on Fee (LCC)**:
- Pack within airline's free personal item dimensions
- VietJet: 7kg carry-on included; Spirit: personal item only (45×35×20cm)
- Consider: Is the carry-on fee still cheaper than a legacy carrier total?

**Checked Bag Fee**:
- Airline credit card: Many waive first bag (e.g., United Explorer card)
- Status match: Silver/Gold loyalty = free bags
- Pre-pay online: Always cheaper than airport counter (20-50% savings)
- Ship luggage separately: Services like LuggageForward for long trips

**Seat Selection Fee**:
- Skip it: Accept random assignment for savings
- Check in exactly at 24h mark: Best free seats available
- Back of plane: Often free even when front costs extra

**Change/Cancel Fee**:
- Book with credit card that offers trip protection
- Some airlines (Southwest, JetBlue) offer free changes
- 24-hour rule: Most US carriers allow free cancellation within 24h of booking

**Payment Surcharge**:
- Use debit card (many airlines waive surcharge)
- Some airlines charge extra for credit card (Ryanair, AirAsia)
- PayPal sometimes adds processing fees

### Step 6: Cabin Bag Size Reference

Include for options with strict carry-on policies:

| Airline | Personal Item | Cabin Bag | Weight Limit |
|---------|--------------|-----------|-------------|
| VietJet | 36×23×56cm | 7kg total | 7kg |
| AirAsia | 40×30×10cm | 54×38×23cm (paid) | 7kg |
| Spirit | 45×35×20cm | 56×46×25cm (paid) | None stated |
| Ryanair | 40×20×25cm | 55×40×20cm (paid) | 10kg |
| Southwest | No limit | 61×41×28cm | None stated |
| Vietnam Airlines | 56×36×23cm | 12kg (economy) | 12kg |

### Step 7: Output Summary

```
ORIGINAL RANKING (by advertised price):
  1. VietJet $380    2. Korean $580    3. VN Airlines $620

TRUE RANKING (all fees included):
  1. VietJet $532    2. Korean $705    3. VN Airlines $740

VERDICT: VietJet remains cheapest even after fees (+$152 in extras).
However, VN Airlines includes lounge access with Business Saver 
that isn't captured in this analysis.
```

## Limitations

- Fee data is based on published policies - airlines may change without notice
- Some fees vary by route, booking channel, or time of purchase
- Loyalty status benefits are estimated - check your specific tier
- Meal costs for LCCs are not included (varies too widely)
