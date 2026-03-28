---
name: hidden-city-strategy
description: Use when user explicitly asks about hidden city ticketing, skiplagging, or throwaway ticketing. Requires explicit consent before analysis. Triggers on hidden city, skiplag, get off at layover.
---

# Hidden City Strategy - Chiến Lược Vé Hidden City

## Purpose

Hidden city ticketing means buying a ticket to city C (cheaper) but getting off at city B (your actual destination), which is a layover on the way to city C. This skill provides NEUTRAL analysis - it doesn't encourage or discourage the practice. It gives you complete information to make your own informed decision.

## Critical Design Principles

> **ETHICAL GUARDRAILS:**
> 1. This skill NEVER auto-recommends hidden city booking
> 2. This skill ALWAYS requires explicit human consent before showing analysis
> 3. This skill ALWAYS presents full risk disclosure before savings data
> 4. Final decision is ALWAYS the user's responsibility

## Input Required

- Route (origin → actual destination)
- Flight options from flight-search
- Traveler profile (baggage, loyalty, corporate card)

## Execution Steps

### Step 1: Consent Gate

Before ANY analysis, ask:

```
⚠️ HIDDEN CITY TICKETING ANALYSIS

Hidden city ticketing violates airline contracts of carriage.
It is not illegal, but airlines enforce penalties including:
- Account suspension
- Mileage forfeiture  
- Future ticket cancellation
- Potential fare difference charges

Do you want to proceed with this analysis? 
This decision is entirely yours. [Yes / No]
```

If No → Stop. Suggest alternatives (route-optimization for hub-based savings).

### Step 2: Eligibility Gate (Must ALL pass)

Check these conditions BEFORE running savings analysis:

| # | Condition | Required | Why |
|---|-----------|----------|-----|
| 1 | No checked baggage | ✅ MUST | Checked bags route to final destination |
| 2 | No frequent flyer number on booking | ✅ MUST | Airlines track by FF account |
| 3 | No corporate travel card | ✅ MUST | Corporate accounts get flagged faster |
| 4 | One-way ticket only | ✅ MUST | Round-trip: missing leg 1 cancels return |
| 5 | No corporate travel policy prohibiting | ✅ MUST | Policy violation = disciplinary action |
| 6 | No connecting flight after hidden city | ✅ MUST | Missing first leg kills all subsequent |
| 7 | Non-frequent route (not weekly) | ⚠️ WARN | Patterns trigger detection |

**Output if any condition fails:**

```
❌ ELIGIBILITY CHECK FAILED

Condition failed: #4 - Round-trip booking
Reason: If you don't board the HAN→SFO→LAX segment, 
        the airline cancels your LAX→SFO→HAN return.

This means hidden city is NOT viable for your itinerary.

ALTERNATIVE: Consider route-optimization skill for hub-based 
savings that don't carry these risks.
```

### Step 3: Savings Analysis (only if eligible)

Compare:
```
Direct ticket:      HAN → SFO     = $750
Hidden city ticket: HAN → SFO → LAX = $520 (you exit at SFO)
Gross savings:      $230 (31%)
```

But factor in costs of hidden city:
```
Net savings calculation:
  Gross savings:                    $230
  - Travel insurance (recommended): -$30
  - One-way ticket premium:         -$0 (sometimes one-ways cost more)
  - Risk-adjusted penalty cost:     -$X (see Step 4)
  = Net expected savings:           $200 (estimated)
```

### Step 4: Risk Assessment by Airline

Read `references/enforcement-levels.md` for current enforcement data.

Present airline-specific risk:

```
ENFORCEMENT RISK: United Airlines
Level: HIGH 🔴

- AI detection system launched 2025 for skiplag detection
- Actively tracks passengers who don't board final segments
- Known to charge fare difference retroactively
- Frequent flyer account at risk of suspension
- Delta dedicating resources at Atlanta hub specifically

If caught: Fare difference charge ($230+), possible account ban
Probability of detection: MODERATE-HIGH for this route
```

### Step 5: Full Risk Disclosure

Present ALL risks in clear format:

```
COMPLETE RISK DISCLOSURE

✅ What goes right (best case):
   You save $230 and nobody notices.

⚠️ What could go wrong:
   1. Gate agent notices and re-routes you to LAX
   2. Airline charges fare difference ($230+) retroactively
   3. Frequent flyer account suspended (if accidentally linked)
   4. Future bookings on this airline scrutinized
   5. If flight diverts/cancels, you're rebooked to LAX, not SFO
   6. Carry-on could be gate-checked to LAX at busy gate

🔴 Worst case:
   Airline bans you from future bookings + charges premium fare
   + forfeits any miles in your account

💡 Mitigations:
   - Use airline's website directly (OTAs may flag unusual patterns)
   - Don't add frequent flyer number
   - Arrive early, board early (avoid gate-check of carry-on)
   - Have backup plan if flight is cancelled/rerouted
```

### Step 6: Decision Framework

Don't recommend - present framework for user to decide:

```
DECISION MATRIX

                    Hidden City         Direct Booking
Cost:               $520                $750
Savings:            $230 (31%)          Baseline
Risk level:         HIGH (United)       None
Baggage:            Carry-on only       Any
Rebooking if delay: To LAX (wrong)      To SFO (correct)
Miles earned:       None (risky)        Full earning
Insurance:          Recommended (+$30)  Standard

YOUR CALL: Given these trade-offs, the decision is entirely yours.
This skill has presented neutral information. 
We do not recommend for or against this strategy.
```

## References

- `references/enforcement-levels.md` - Airline-by-airline enforcement data
- `references/eligibility-check.md` - Detailed eligibility conditions

## Important Notes

- Hidden city ticketing is explicitly prohibited in airline Contracts of Carriage
- It is NOT illegal (no law prohibits it), but it IS a contract violation
- Airlines have successfully sued travel agencies (not individuals) promoting it
- Skiplagged.com lawsuit was dismissed but demonstrates airline hostility
- Frequency of use increases detection risk dramatically
- This skill exists for informational purposes only
