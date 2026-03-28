---
name: flight-planner
description: "Flight cost optimization with 8 specialized skills. Use when planning flights, comparing ticket prices, or asking about flight costs, airline fees, travel dates, route options. Triggers on: booking flights, cheap tickets, flight search, vé máy bay, săn vé rẻ, tối ưu chi phí bay, đặt vé, virtual interlining, or any flight-related cost question."
argument-hint: "[origin] [destination] [dates]"
allowed-tools: Bash(python *), Read, Glob, Grep
---

# Travel Optimization Engine

A decision support system for flight ticket cost optimization. Coordinates 8 specialized skills to analyze every angle of flight pricing before you book.

## Setup

API keys required as environment variables (optional — skills work in AI-knowledge mode without APIs):
- `AMADEUS_API_KEY` + `AMADEUS_API_SECRET` — register at developers.amadeus.com
- `KIWI_API_KEY` — register at tequila.kiwi.com/portal

Shared API clients: `scripts/amadeus_client.py`, `scripts/kiwi_client.py`, `scripts/normalize.py`

## Phase 1: Collect Traveler Profile

Before running any analysis, gather this profile (ask only what's missing). See `references/user-profile-schema.md` for full schema.

```
REQUIRED:
- origin: IATA code or city name (e.g., HAN, "Hanoi")
- destination: IATA code or city name (e.g., SFO, "San Francisco")
- departure_date: target date or range
- passengers: number + types (adult/child/infant)

OPTIONAL (improves accuracy):
- return_date: one-way if empty
- flexibility: low (±2 days) | medium (±7 days) | high (±14 days)
- baggage: carry_on | checked_1 | checked_2
- booking_type: personal | corporate
- loyalty_programs: airline codes (e.g., VN, QR)
- risk_tolerance: conservative | moderate | aggressive
- cabin_class: economy | premium_economy | business | first
```

If user provides minimal input (e.g., "HAN to SFO next month"), infer defaults:
- flexibility: medium, baggage: carry_on, booking_type: personal, cabin: economy

## Phase 2: Search (Parallel)

Run these two skills simultaneously:

1. **Read** `skills/date-optimization/SKILL.md` — find cheapest travel dates in ±5-14 day window
2. **Read** `skills/flight-search/SKILL.md` — search flights across Amadeus + Kiwi with virtual interlining

Pass optimal dates from skill 1 into skill 2 for refined results.

## Phase 3: Analyze

With search results in hand, run sequentially:

3. **Read** `skills/route-optimization/SKILL.md` — find cheaper hub-based routes
4. **Read** `skills/fee-analysis/SKILL.md` — deconstruct hidden fees, re-rank by true cost
5. **Read** `skills/deals-verification/SKILL.md` — check available deals and promo codes

## Phase 4: Assess (Conditional)

Based on profile and context:

6. If `booking_type == corporate` → **Read** `skills/negotiation-email/SKILL.md`
7. If schedule uncertainty exists or `risk_tolerance != conservative` → **Read** `skills/flexibility-analysis/SKILL.md`
8. **Only if user explicitly asks** about hidden city / throwaway ticketing → **Read** `skills/hidden-city-strategy/SKILL.md` (requires explicit user consent)

## Phase 5: Output

Generate a consolidated comparison report:

### Report Structure
1. **Executive Summary**: Best option + savings vs naive booking
2. **Date Analysis**: Optimal travel window with savings breakdown
3. **Top 5 Options**: Ranked by true_total (all fees included)
4. **Route Alternatives**: Hub-based savings if applicable
5. **Deals Applied**: Verified discounts with confidence levels
6. **Risk Assessment**: Flexibility scores per option
7. **Action Items**: Exact next steps to book

### Formatting Rules
- All prices in user's preferred currency (default: USD for international, VND for domestic VN)
- Always show: `advertised_price` → `true_total` comparison
- Tag each option: `[DIRECT]` `[1-STOP]` `[INTERLINING]` `[LCC]` `[LEGACY]`
- Include booking links or search instructions where possible

## Quick Dispatch

For users who only need one specific skill:

| User Intent | Skill to Load |
|------------|---------------|
| "When is cheapest to fly?" | `skills/date-optimization/SKILL.md` |
| "Find flights HAN→SFO" | `skills/flight-search/SKILL.md` |
| "Is there a cheaper route?" | `skills/route-optimization/SKILL.md` |
| "What's the real price with fees?" | `skills/fee-analysis/SKILL.md` |
| "Any promo codes?" | `skills/deals-verification/SKILL.md` |
| "Help me negotiate with airline" | `skills/negotiation-email/SKILL.md` |
| "Should I buy flexible ticket?" | `skills/flexibility-analysis/SKILL.md` |
| "Tell me about hidden city" | `skills/hidden-city-strategy/SKILL.md` |

## References

- `references/amadeus-api.md` — Amadeus Self-Service API endpoints and auth
- `references/kiwi-api.md` — Kiwi Tequila API with virtual interlining
- `references/airport-codes.md` — Hub airports, alliances, strategic routing tips
- `references/user-profile-schema.md` — Full profile field documentation

## Important Notes

- This skill is a **Decision Support System** — it helps users make informed choices, never auto-books
- All prices from AI-Knowledge mode are estimates based on historical patterns
- When API mode is enabled (Amadeus + Kiwi), prices are real-time but may change at checkout
- Hidden city strategy (skill 8) always requires explicit human consent before analysis
