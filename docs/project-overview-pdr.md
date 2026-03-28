# Project Overview & Product Development Requirements

## Executive Summary

**Travel Optimization Engine** is a Claude Code skill plugin that delivers flight cost optimization through a coordinated system of 8 specialized AI skills. The system saves users 30-66% on personal travel and 10-15% on corporate bookings by analyzing pricing from multiple angles: dates, routes, hidden fees, deals, flexibility, and corporate negotiation strategies.

This is a **decision support system**, not a booking engine. It provides analysis, recommendations, and exact next steps for users to book confidently.

### Key Facts

- **Platform:** Claude Code (plugin/skill system)
- **Skills:** 8 specialized sub-skills
- **Modes:** AI-Knowledge (no API) + API-Enhanced (Kiwi Tequila, Amadeus)
- **Target Users:** Individual travelers, corporate travel managers, travel agencies
- **Version:** 1.0.0 (released 2026-03-28)
- **License:** MIT (open source)

## Product Vision

Empower travelers and corporate travel programs to make data-driven flight booking decisions by coordinating specialized AI analysis across pricing, fees, routing, deals, and negotiation strategies.

## Core Capabilities

### 1. Date Optimization
Analyze price fluctuations across flexible date ranges to identify the cheapest travel windows. Returns a date matrix with savings opportunities.

**Inputs:** Origin, destination, baseline date, flexibility window (±5-14 days)
**Output:** Ranked dates by price, trend analysis

### 2. Flight Search
Search flights across multiple sources (Amadeus, Kiwi Tequila) with virtual interlining detection. Combines carrier-specific flights into lowest-cost itineraries.

**Inputs:** Origin, destination, dates, passengers, preferences
**Output:** Top 20 options with routing (direct, 1-stop, interlining)

### 3. Route Optimization
Discover cheaper hub-based alternatives (e.g., HAN→ICN→SFO instead of HAN→SFO direct). Analyzes alliance routing and connects pricing.

**Inputs:** Flight options from skill 2
**Output:** Hub-based alternatives with savings breakdown

### 4. Fee Analysis
Deconstruct hidden fees (seat selection, baggage, fuel surcharges, change fees). Recalculates true total cost including all fees.

**Inputs:** Flight options from skill 2
**Output:** Fee breakdown per option, true total cost, fee avoidance strategies

### 5. Deals Verification
Searches for applicable promo codes, flash sales, loyalty bonuses, and corporate discounts. Tags each deal with confidence level (HIGH/MEDIUM/LOW/EXPIRED).

**Inputs:** Route, airline, booking type (personal/corporate)
**Output:** Applicable deals, confidence levels, booking instructions

### 6. Flexibility Analysis
Assesses refundable vs non-refundable break-even analysis. Calculates risk score based on schedule certainty and change probability.

**Inputs:** Selected option, booking timeline, schedule certainty
**Output:** Risk assessment, refundable vs non-refundable recommendation

### 7. Negotiation Email
Generates corporate discount email templates with data attachments (volume, route concentration, competitor pricing). Includes follow-up talking points.

**Inputs:** Corporate profile (volume, routes, preferred airlines)
**Output:** Email template, talking points, follow-up strategy

### 8. Hidden City Strategy
Analyzes skiplagging opportunities with full risk disclosure, eligibility check, and airline enforcement tracking. Manual invocation only, requires explicit consent.

**Inputs:** Route, origin, destination, eligibility confirmation
**Output:** Skiplagging options, enforcement risk rating, legal disclaimer

## Functional Requirements

### FR-1: Profile Collection
- **Requirement:** System must collect traveler profile with required and optional fields
- **Required Fields:** origin, destination, departure_date, passengers
- **Optional Fields:** return_date, flexibility, baggage, booking_type, loyalty_programs, risk_tolerance, cabin_class
- **Acceptance Criteria:**
  - Infer defaults for optional fields if not provided
  - Validate IATA codes or resolve city names to IATA codes
  - Parse passenger counts and types (adult, child, infant)

### FR-2: Parallel Date & Flight Search
- **Requirement:** Execute date-optimization and flight-search skills simultaneously
- **Acceptance Criteria:**
  - Date optimization completes within 5 seconds (AI-knowledge mode)
  - Flight search completes within 10 seconds (API mode) or 30 seconds (AI-knowledge)
  - Pass optimal dates from skill 1 to skill 2 for refinement
  - Return top 20 options sorted by true_total

### FR-3: Fee Deconstruction
- **Requirement:** Calculate true total cost including all hidden fees
- **Fees to Include:** Taxes, baggage, seat selection, fuel surcharges, change fees, insurance
- **Acceptance Criteria:**
  - Show advertised price → true total comparison
  - Provide fee-by-fee breakdown
  - Suggest fee avoidance strategies (airline choices, baggage selection, etc.)

### FR-4: Hub-Based Route Analysis
- **Requirement:** Discover cheaper alternatives via hub routing
- **Major Hubs:** SFO, DFW, NRT, ICN, DUB, IST, DOH, SIN
- **Acceptance Criteria:**
  - Analyze 2-3 hub alternatives per route
  - Calculate connection time and risk
  - Show savings vs direct routing
  - Warn about missed connection risk for virtual interlining

### FR-5: Deal Verification
- **Requirement:** Search and verify applicable promo codes and discounts
- **Deal Sources:** Airline websites, flash sales, loyalty programs, corporate contracts, bank partnerships
- **Acceptance Criteria:**
  - Tag deals with confidence level (HIGH/MEDIUM/LOW/EXPIRED)
  - Provide booking instructions and expiry dates
  - Calculate actual savings per deal

### FR-6: Corporate Negotiation Email
- **Requirement:** Generate email templates for corporate volume discounts
- **Acceptance Criteria:**
  - Include volume metrics, route concentration, competitor pricing
  - Provide follow-up talking points
  - Include sample deal packages
  - Never reveal max budget to airline

### FR-7: Consolidated Report Output
- **Requirement:** Generate comprehensive comparison report
- **Report Sections:** Executive summary, date analysis, top 5 options, route alternatives, deals applied, risk assessment, action items
- **Acceptance Criteria:**
  - Show advertised price vs true total for each option
  - Tag each option with routing type ([DIRECT], [1-STOP], [INTERLINING], [LCC], [LEGACY])
  - Provide exact booking links or search instructions
  - Format in user's preferred currency

## Non-Functional Requirements

### NFR-1: Performance
- Date-optimization: Complete within 5 seconds (AI-knowledge), 8 seconds (API)
- Flight-search: Complete within 10 seconds (API), 30 seconds (AI-knowledge)
- Full report: Complete within 60 seconds

### NFR-2: Accuracy
- Price data must be current within 24 hours
- True cost calculation must be accurate within 2%
- Deals must be verified before inclusion (no expired or false claims)

### NFR-3: Availability
- System operates in two modes without API keys (degraded but functional)
- Graceful fallback if API is unavailable
- Cache pricing data for common routes

### NFR-4: Security
- API keys stored in environment variables, never in code
- OAuth2 for Amadeus authentication
- No sensitive user data logged
- Hidden city strategy requires explicit consent before analysis

### NFR-5: Usability
- Natural language interface (user speaks normally)
- Auto-trigger appropriate skills based on user intent
- Clear explanations of all recommendations
- Transparent about data sources and confidence levels

### NFR-6: Maintainability
- Each skill is independent and can be updated without affecting others
- Clear separation of concerns (scripts, references, assets)
- Comprehensive documentation for each skill
- Version tracking in CHANGELOG.md

## Safety & Ethics Requirements

### SR-1: Hidden City Strategy Gate
- Require explicit user consent before analyzing skiplagging
- Perform eligibility check (visa requirements, luggage rules, etc.)
- Provide full legal risk disclaimer
- Warn about airline enforcement (bans, account closures)
- Only show when user explicitly asks or confirms understanding

### SR-2: Virtual Interlining Warnings
- Always warn about missed connection risk
- Note that baggage may not connect through intermediate segments
- Explain that delays in first segment could cause missed connection
- Provide delay insurance recommendations

### SR-3: Deal Confidence Levels
- Tag all deals with explicit confidence levels (HIGH/MEDIUM/LOW/EXPIRED)
- Never suggest expired deals without clear marking
- Provide confidence reasoning (e.g., "HIGH: Verified 2 hours ago")
- Update deal status at booking time

### SR-4: Corporate Negotiation Ethics
- Never disclose individual customer's max budget to airline
- Use only aggregate volume and route data
- Follow corporate compliance policies
- Warn about antitrust concerns with competitor pricing

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Cost Savings | 30-66% personal, 10-15% corporate | Compare booked price vs baseline options |
| User Satisfaction | >4.5/5 | Post-booking feedback survey |
| Deal Accuracy | >95% | Verify deals at booking time |
| Report Completion Time | <60 seconds | Time from profile collection to report output |
| API Uptime | 99.5% | Monitoring and alerts |
| Feature Adoption | >50% users use 5+ skills | Usage analytics |

## In-Scope Features (MVP)

- 8 specialized skills fully functional
- AI-knowledge mode (no API required)
- API-enhanced mode (Kiwi Tequila + Amadeus)
- 5-phase workflow orchestration
- Report generation with savings breakdown
- Safety gates for hidden city strategy

## Out-of-Scope (Future)

- Booking integration (direct ticket purchase)
- Mobile app (web interface only via Claude Code)
- Airline status matching
- Group bookings (> 9 passengers)
- Custom corporate contracts
- Real-time airport operations (delays, gate info)
- Travel insurance quote integration

## Technical Constraints

1. **Claude Code Platform:** System operates within Claude Code's plugin architecture and tool restrictions
2. **API Rate Limits:** Kiwi Tequila (50 req/sec), Amadeus (varies by plan)
3. **Data Freshness:** Prices may change at checkout; estimates are snapshot-based
4. **Currency Support:** Major currencies (USD, EUR, GBP, JPY, VND); conversion via market rates
5. **Route Limitations:** Only supports city-pair routing (no multi-city bookings in v1.0)

## Dependencies

### External APIs
- **Kiwi Tequila:** Flight search, virtual interlining, price trends
- **Amadeus:** Real-time pricing, seat maps, airline rules, OAuth2

### Libraries
- **Python 3.8+** runtime
- **requests** library for HTTP calls
- Claude Code platform

### Data References
- IATA airport codes (static, ~7500 airports)
- Airline fee matrices (updated monthly)
- Hub routing rules (static, updated quarterly)
- Promo code database (updated daily)

## Implementation Timeline

### Phase 1 (Complete)
- 8 skills fully implemented
- AI-knowledge mode tested
- Documentation complete

### Phase 2 (v1.1, Q2 2026)
- API-enhanced mode (Kiwi Tequila integration)
- Real-time pricing
- Virtual interlining optimization

### Phase 3 (v1.2, Q3 2026)
- Amadeus integration (corporate pricing)
- Corporate negotiation email templates
- Volume discount calculator

### Phase 4 (v2.0, Q4 2026)
- Multi-city routing support
- Hotel + ground transport optimization
- Travel insurance quote integration

## Acceptance Criteria Summary

The project is considered complete when:

1. All 8 skills are implemented and independently functional
2. 5-phase workflow executes end-to-end without errors
3. Generated reports include: executive summary, date analysis, top 5 options, route alternatives, deals applied, risk assessment, action items
4. Hidden city strategy includes: explicit consent gate, eligibility check, risk disclosure
5. Virtual interlining options include: clear warnings, connection risk assessment
6. True cost calculation is accurate within 2%
7. Report generation completes within 60 seconds
8. System works in AI-knowledge mode (no APIs) and API-enhanced mode
9. All documentation is complete and current
10. Code follows standards in `code-standards.md`

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-28 | Initial release with 8 skills, AI-knowledge mode, MVP features |

## References

- `codebase-summary.md` — Full file inventory and structure
- `code-standards.md` — Code standards and conventions
- `system-architecture.md` — Architecture diagrams and design
- `project-roadmap.md` — Future phases and roadmap
- `SKILL.md` — Root orchestrator skill definition
- `README.md` — Getting started guide
