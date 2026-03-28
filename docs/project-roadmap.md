# Project Roadmap

## Vision

Travel Optimization Engine is evolving from a specialized flight optimization skill to a comprehensive travel cost management platform. The roadmap balances feature expansion with reliability, safety, and user value.

## Current State (v1.0)

**Release Date:** 2026-03-28

### Completed Features
- 8 specialized flight optimization skills
- AI-knowledge mode (no APIs required)
- Basic 5-phase workflow orchestration
- Report generation with savings breakdown
- Safety gates for hidden city strategy
- Comprehensive documentation
- GitHub repository with MIT license

### Known Limitations
- Flight search only (no hotels, ground transport)
- Single city-pair routing (no multi-city)
- AI-knowledge mode estimates (not real-time)
- No direct booking integration
- Limited to Claude Code platform

## Phase 1: API Enhancement (v1.1, Q2 2026)

**Timeline:** April—June 2026
**Status:** Not started
**Estimated Effort:** 2-3 weeks

### Goals
Integrate real-time flight data via Kiwi Tequila and Amadeus APIs for accurate pricing and expanded options.

### Features

#### 1.1.1: Kiwi Tequila Integration
- [ ] Implement real-time flight search via Kiwi API
- [ ] Add virtual interlining detection
- [ ] Support 90-day price trend analysis
- [ ] Implement rate limit handling and backoff
- [ ] Add caching layer for common routes

**Files to Create:**
- Enhanced `scripts/kiwi_tequila.py` with caching
- `scripts/kiwi_rate_limiter.py` — Rate limit management
- `skills/flight-search/references/kiwi-integration-guide.md`

**Success Criteria:**
- Flight search returns real-time results within 10 seconds
- Virtual interlining options included automatically
- 95% success rate on API calls (with 5% fallback to AI-knowledge)

#### 1.1.2: Amadeus OAuth2 Integration
- [ ] Implement OAuth2 authentication flow
- [ ] Real-time seat map queries
- [ ] Airline fee rules lookup
- [ ] Corporate pricing support

**Files to Create:**
- `scripts/amadeus_oauth.py` — OAuth2 handler
- `scripts/amadeus_corporate_pricing.py` — B2B pricing
- `skills/fee-analysis/references/amadeus-fee-rules.md`

**Success Criteria:**
- OAuth2 token refresh automatic
- 99% uptime for authenticated requests
- Corporate pricing available for registered airlines

#### 1.1.3: API Testing & Monitoring
- [ ] Unit tests for API clients
- [ ] Integration tests with mock API responses
- [ ] Error handling tests (timeout, rate limit, auth)
- [ ] Monitoring and alerting

**Files to Create:**
- `tests/test_kiwi_client.py`
- `tests/test_amadeus_client.py`
- `scripts/health_check.py` — API health monitor

**Success Criteria:**
- 90%+ code coverage for API clients
- All error scenarios tested
- Health check available for monitoring

### Dependencies
- Kiwi Tequila API key (free tier available)
- Amadeus API access (paid or partnership)
- Rate limit strategy implementation

### Risk Assessment
- **Risk:** API rate limits during peak load
  - **Mitigation:** Implement queuing and caching
- **Risk:** OAuth2 token expiry during long sessions
  - **Mitigation:** Auto-refresh token before expiry

---

## Phase 2: Corporate Negotiation Tools (v1.2, Q3 2026)

**Timeline:** July—September 2026
**Status:** Not started
**Estimated Effort:** 2-3 weeks

### Goals
Empower corporate travel managers with negotiation data and deal analysis tools.

### Features

#### 1.2.1: Volume Discount Calculator
- [ ] Aggregate volume metrics from historical bookings
- [ ] Compare against negotiated rates
- [ ] Identify renegotiation opportunities
- [ ] Generate savings reports

**Files to Create:**
- `skills/negotiation-email/scripts/volume_calculator.py`
- `skills/negotiation-email/references/discount-benchmarks.md`

**Success Criteria:**
- Volume calculation accurate to within 5%
- Identify 2-3 renegotiation opportunities per 100 bookings
- Savings report generated in <5 seconds

#### 1.2.2: Competitive Intelligence
- [ ] Track competitor pricing on corporate routes
- [ ] Identify market trends (price increases/decreases)
- [ ] Suggest timing for negotiations
- [ ] Compare negotiated rates to market

**Files to Create:**
- `skills/negotiation-email/scripts/competitive_analysis.py`
- `skills/negotiation-email/references/market-trends.md`

**Success Criteria:**
- Market trend analysis available for 500+ corporate routes
- Trend accuracy within 10% (historical validation)
- Competitive intelligence updated weekly

#### 1.2.3: Deal Template Library
- [ ] Expand email templates (5 → 15 templates)
- [ ] Add dealing scenarios (renewal, expansion, new airline)
- [ ] Include talking points and objection handling
- [ ] Provide follow-up strategies

**Files to Update:**
- `skills/negotiation-email/assets/email-templates.md` (expanded)
- `skills/negotiation-email/references/negotiation-strategy.md` (new)

**Success Criteria:**
- At least 15 templates covering common scenarios
- Each template has specific talking points
- Follow-up strategies documented

### Dependencies
- Historical booking data (requires corporate partner integration)
- Competitive pricing data (via Kiwi, Amadeus, GDS)
- Market trend analysis tools

### Risk Assessment
- **Risk:** Access to competitor pricing data
  - **Mitigation:** Use only public market data
- **Risk:** Antitrust concerns with negotiation strategies
  - **Mitigation:** Counsel only on own negotiation tactics, not collusion

---

## Phase 3: Multi-City & Ground Transport (v2.0, Q4 2026)

**Timeline:** October—December 2026
**Status:** Not started
**Estimated Effort:** 4-6 weeks

### Goals
Expand from flight-only optimization to comprehensive trip cost management including hotels and ground transport.

### Features

#### 2.0.1: Multi-City Flight Routing
- [ ] Support multi-city bookings (e.g., HAN → SFO → NYC → BOS)
- [ ] Optimize routing across multiple legs
- [ ] Recommend stopover cities
- [ ] Calculate round-trip vs one-way vs open-jaw savings

**New Skill:** `multi-city-optimization`
- Inputs: Multiple origin-destination pairs, dates
- Output: Optimal routing with savings

**Files to Create:**
- `skills/multi-city-optimization/SKILL.md`
- `skills/multi-city-optimization/scripts/routing_engine.py`
- `skills/multi-city-optimization/references/stopover-strategies.md`

**Success Criteria:**
- Support up to 5-city itineraries
- Identify stopover cities that reduce total cost
- Routing analysis completes in <15 seconds

#### 2.0.2: Hotel Integration
- [ ] Search hotel prices across trip dates
- [ ] Match hotel quality to airline class
- [ ] Calculate total accommodation cost
- [ ] Identify hotel loyalty program opportunities

**New Skill:** `hotel-optimization`
- Inputs: Destination cities, stay dates, star preference
- Output: Hotel options ranked by value

**Files to Create:**
- `skills/hotel-optimization/SKILL.md`
- `skills/hotel-optimization/scripts/hotel_client.py` (integration with Booking.com or Expedia API)
- `skills/hotel-optimization/references/hotel-loyalty-programs.md`

**Success Criteria:**
- Hotel search returns results within 5 seconds
- Top 10 options ranked by value (price ÷ star rating)
- Loyalty program benefits calculated

#### 2.0.3: Ground Transport Integration
- [ ] Search taxi, rental car, public transit options
- [ ] Calculate cost per transport method
- [ ] Match transport to trip urgency
- [ ] Identify transit + flight package deals

**New Skill:** `ground-transport-optimization`
- Inputs: Cities, dates, trip urgency
- Output: Transport options ranked by cost-convenience tradeoff

**Files to Create:**
- `skills/ground-transport-optimization/SKILL.md`
- `skills/ground-transport-optimization/scripts/transport_client.py` (Uber, Lyft, rental car APIs)
- `skills/ground-transport-optimization/references/transport-strategies.md`

**Success Criteria:**
- 3-4 transport options per trip leg
- Cost calculated including tolls, parking, tips
- Integration with flight schedules (arrival/departure times)

#### 2.0.4: Trip-Level Optimization
- [ ] Consolidate flight + hotel + ground transport
- [ ] Calculate total trip cost
- [ ] Identify trip-level discounts (packages)
- [ ] Provide comprehensive trip recommendations

**New Skill:** `trip-optimizer` (replaces flight-planner as new orchestrator)
- Orchestrates: flight, hotel, ground-transport optimizations
- Outputs: Consolidated trip report with total cost savings

**Files to Create:**
- `SKILL.md` (updated to `trip-optimizer`)
- `SKILL-flight-planner.md` (deprecated, kept for backward compatibility)

**Success Criteria:**
- Full trip analysis completes in <60 seconds
- Savings breakdown shows flight + hotel + transport contributions
- Package deals identified and applied automatically

### Dependencies
- Hotel booking APIs (Booking.com, Expedia, or proprietary)
- Ground transport APIs (Uber, Lyft, car rental, transit)
- Multi-leg route optimization algorithms

### Risk Assessment
- **Risk:** Complexity increase (many more variables)
  - **Mitigation:** Start with domestic US routes, expand to international
- **Risk:** API dependencies (more integrations = more failure points)
  - **Mitigation:** Graceful fallback if hotel/transport APIs unavailable
- **Risk:** Cost explosion (flight + hotel + transport = larger matrix)
  - **Mitigation:** Implement smart caching and pre-filtering

---

## Phase 4: Travel Insurance & Advanced Analytics (v2.1, Q1 2027)

**Timeline:** January—March 2027
**Status:** Not started
**Estimated Effort:** 3-4 weeks

### Features

#### 2.1.1: Travel Insurance Integration
- [ ] Quote travel insurance policies
- [ ] Compare coverage and cost
- [ ] Recommend insurance based on trip risk
- [ ] Integrate insurance cost into trip total

**New Skill:** `insurance-optimizer`

#### 2.1.2: Advanced Price Analytics
- [ ] Predict price trends (ML-based)
- [ ] Recommend optimal booking windows
- [ ] Estimate price probability distribution
- [ ] Alert when prices drop below target

**New Skill:** `price-predictor`

#### 2.1.3: Sustainability Metrics
- [ ] Calculate carbon footprint per routing option
- [ ] Recommend lowest-carbon alternatives
- [ ] Support carbon offset booking
- [ ] Sustainability report generation

**New Skill:** `sustainability-analyzer`

---

## Phase 5: Mobile & Booking Integration (v3.0, 2027+)

**Timeline:** 2027 and beyond
**Status:** Not started
**Estimated Effort:** 6-8 weeks

### Goals
Expand platform to mobile devices and integrate with booking engines.

### Features
- Native iOS/Android apps
- Direct booking integration with major GDS
- One-click booking with saved payment methods
- Real-time price alerts and notifications
- Trip management and itinerary tracking

---

## Metrics & Success Tracking

### Key Performance Indicators

| Metric | v1.0 Target | v1.1 Target | v2.0 Target |
|--------|-------------|-------------|-------------|
| Cost Savings (Personal) | 30-66% | 35-70% | 40-75% |
| Cost Savings (Corporate) | 10-15% | 12-18% | 15-22% |
| Report Gen Time | <60s | <60s | <90s |
| API Uptime | N/A | 99.5% | 99.8% |
| User Satisfaction | N/A | >4.5/5 | >4.7/5 |
| Feature Adoption | N/A | >50% | >70% |
| Support Tickets | N/A | <5/week | <3/week |

### Adoption Targets

| Phase | Personal Users | Corporate Users | Monthly Reports |
|-------|----------------|-----------------|-----------------|
| v1.0 | 100-500 | 5-10 | 500-2000 |
| v1.1 | 500-2000 | 20-50 | 2000-8000 |
| v2.0 | 2000-10k | 100-500 | 10k-50k |
| v3.0 | 10k-50k | 500-2000 | 50k-250k |

---

## Priority Framework

### High Priority
- API integration (v1.1) — Unlocks real-time pricing
- Safety/security improvements — Protect users
- Documentation maintenance — Enables adoption
- Bug fixes — Stability first

### Medium Priority
- Multi-city routing (v2.0) — Expand use cases
- Corporate tools (v1.2) — B2B market
- Analytics improvements — Data-driven decisions

### Low Priority
- Mobile apps (v3.0) — Future expansion
- Advanced ML features (v2.1) — Nice-to-have
- Luxury integrations — Niche markets

---

## Risk & Mitigation

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| API rate limits during load spikes | High | Medium | Implement queuing, caching, request batching |
| OAuth2 token expiry bugs | Medium | High | Comprehensive token refresh testing |
| Multi-API coordination complexity | High | Medium | Start with Kiwi only, add Amadeus incrementally |
| Data consistency across APIs | Medium | High | Implement transaction-style coordination |

### Business Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| Competitive pressure from Kayak/Skyscanner | High | Medium | Focus on niche (corporate, integration) |
| API pricing increases | Medium | High | Diversify API sources, negotiate contracts |
| Regulatory changes (GDPR, etc.) | Low | High | Maintain compliance audit trail |

### Operational Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| Key team member departure | Low | High | Cross-train, document processes |
| GitHub/Git infrastructure downtime | Low | Medium | Regular backups, disaster recovery plan |
| Security breach / API key leak | Low | High | Secrets management, access controls, monitoring |

---

## Backlog

### Requested Features (Community)
- [ ] Mobile app (iOS/Android)
- [ ] Booking integration (direct purchase)
- [ ] Group booking support (9+ passengers)
- [ ] Airline seat map visualization
- [ ] Price alert notifications
- [ ] Loyalty program point calculations
- [ ] Travel visa requirements checker

### Technical Debt
- [ ] Refactor Phase 2 skill sequencing for parallelization
- [ ] Add comprehensive error telemetry
- [ ] Optimize route-optimization for large hub networks
- [ ] Implement response caching layer
- [ ] Expand test coverage to 95%+ on Python scripts

### Documentation Updates
- [ ] Create video tutorials for each skill
- [ ] Expand API integration guides
- [ ] Add corporate onboarding guide
- [ ] Create troubleshooting wiki

---

## Release Schedule

```
┌─────────────────────────────────────────────────────────────────┐
│                    2026 Release Calendar                         │
├─────────────┬──────────────┬─────────────┬──────────────────────┤
│ Q1 2026     │ Q2 2026      │ Q3 2026     │ Q4 2026              │
├─────────────┼──────────────┼─────────────┼──────────────────────┤
│ v1.0 (3/28) │ v1.1 API Enh │ v1.2 Corp   │ v2.0 Multi-City      │
│ 8 Skills    │ Real-time    │ Negotiation │ Hotel/Ground         │
│ AI-Knowledge│ Kiwi+Amadeus │ Tools       │ Integration          │
└─────────────┴──────────────┴─────────────┴──────────────────────┘
```

---

## Governance & Decision-Making

### Feature Requests
1. Community votes on feature request
2. Core team evaluates feasibility and priority
3. Feature added to backlog with estimation
4. Scheduled in next available phase

### Release Criteria
- [ ] All tests passing (>90% coverage)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Code reviewed (2+ reviewers)
- [ ] Performance benchmarks met
- [ ] No critical security issues

### Version Numbering
- Major: Significant new features or breaking changes (v1.0, v2.0)
- Minor: New features without breaking changes (v1.1, v1.2)
- Patch: Bug fixes and small improvements (v1.0.1, v1.1.1)

---

## How to Contribute

### To Request a Feature
1. Open GitHub issue with label `feature-request`
2. Include: motivation, proposed solution, alternative approaches
3. Community votes (thumbs up/down)
4. Core team evaluates and schedules

### To Contribute Code
1. Fork repository
2. Create feature branch: `feature/short-description`
3. Implement and test
4. Submit PR with description and test results
5. Code review (2+ reviewers)
6. Merge to develop, test in staging
7. Release in next scheduled version

### To Report Issues
1. GitHub issue with label `bug`
2. Include: reproduction steps, expected vs actual behavior
3. Core team triages and schedules fix

---

## References

- `project-overview-pdr.md` — Project requirements and scope
- `system-architecture.md` — Current architecture design
- `code-standards.md` — Coding standards
- `CHANGELOG.md` — Release history
- `README.md` — Getting started guide
