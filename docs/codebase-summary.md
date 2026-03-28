# Codebase Summary — Travel Optimization Engine

> Generated from repomix output. Last updated: 2026-03-28.

## Project Overview

**Travel Optimization Engine** is a Claude Code skill plugin that provides a decision support system for flight ticket cost optimization. It coordinates 8 specialized sub-skills to analyze flight pricing, fees, dates, routes, deals, and corporate negotiation strategies.

- **Type:** Claude Code Skill Plugin
- **Total Files:** 45 files
- **Total Tokens:** ~74,666 (repomix)
- **Language:** Python 3 (scripts) + Markdown (skill definitions)
- **License:** MIT

## Directory Structure

```
travel-optimization-engine/
├── SKILL.md                          # Root orchestrator (flight-planner)
├── README.md                         # Getting started guide
├── CHANGELOG.md                      # Release history
├── LICENSE                           # MIT License
├── .gitignore                        # Git ignore rules
├── .claude/
│   └── settings.local.json           # Claude Code permissions
├── scripts/                          # Shared Python utilities
│   ├── config.py                     # API credential management
│   ├── kiwi_client.py                # Kiwi Tequila API wrapper
│   ├── kiwi_tequila.py               # Advanced Kiwi integration
│   ├── amadeus_client.py             # Amadeus API client (OAuth2)
│   └── normalize.py                  # Price normalization utilities
├── references/                       # Shared reference documentation
│   ├── user-profile-schema.md        # Traveler data structure
│   ├── airport-codes.md              # Hub airports, IATA codes, alliances
│   ├── glossary.md                   # Aviation terminology
│   ├── amadeus-api.md                # Amadeus API reference
│   └── kiwi-api.md                   # Kiwi Tequila API reference
├── skills/                           # 8 sub-skills
│   ├── date-optimization/            # Find cheapest travel dates
│   ├── flight-search/                # Multi-source search + virtual interlining
│   ├── fee-analysis/                 # Hidden fee deconstruction
│   ├── route-optimization/           # Hub-based routing alternatives
│   ├── deals-verification/           # Promo codes, flash sales
│   ├── flexibility-analysis/         # Refundable vs non-refundable
│   ├── negotiation-email/            # Corporate discount email generator
│   └── hidden-city-strategy/         # Skiplagging analysis (consent-gated)
├── assets/
│   ├── flow-diagram.html             # Interactive workflow visualization
│   └── report-template.md            # Report formatting template
├── examples/                         # Sample outputs
│   ├── flight-optimization-report-HAN-SFO-Jun2026.md
│   └── flight-optimization-report-HAN-SFO-Jun2026.html
└── docs/                             # This documentation
    ├── codebase-summary.md           # This file
    ├── project-overview-pdr.md       # Project overview & PDR
    ├── code-standards.md             # Code standards & conventions
    ├── system-architecture.md        # Architecture diagrams
    └── project-roadmap.md            # Future roadmap
```

## Core Skills Structure

Each skill is self-contained with:
- `SKILL.md` — Skill definition (name, description, instructions)
- `references/` — Reference documentation (optional)
- `scripts/` — Python utility scripts (optional)
- `assets/` — Templates and templates (optional)

### 1. date-optimization
- **Purpose:** Find cheapest travel dates within a flexibility window
- **Files:**
  - `SKILL.md` — Main skill definition
  - `scripts/date_matrix.py` — Price matrix calculator
  - `references/pricing-patterns.md` — Pricing trend analysis

### 2. flight-search
- **Purpose:** Multi-source flight search with virtual interlining
- **Files:**
  - `SKILL.md` — Main skill definition
  - `scripts/parallel_search.py` — Parallel API search coordinator
  - `references/virtual-interlining.md` — Interlining strategy guide
  - `references/api-integration.md` — API integration details

### 3. fee-analysis
- **Purpose:** Hidden fee deconstruction and true cost calculation
- **Files:**
  - `SKILL.md` — Main skill definition
  - `scripts/fee_calculator.py` — Fee breakdown engine
  - `references/airline-fee-matrix.md` — Airline fee database
  - `references/avoidance-strategies.md` — Fee avoidance tips

### 4. route-optimization
- **Purpose:** Hub-based route alternatives and cheaper connections
- **Files:**
  - `SKILL.md` — Main skill definition
  - `scripts/route_analyzer.py` — Route alternative finder
  - `references/hub-analysis.md` — Hub airport strategies

### 5. deals-verification
- **Purpose:** Promo codes, flash sales, and discount verification
- **Files:**
  - `SKILL.md` — Main skill definition
  - `references/deal-sources.md` — Deal sources and confidence ratings

### 6. flexibility-analysis
- **Purpose:** Refundable vs non-refundable risk assessment
- **Files:**
  - `SKILL.md` — Main skill definition
  - `references/fare-class-rules.md` — Fare class rules and flexibility

### 7. negotiation-email
- **Purpose:** Corporate discount email generator
- **Files:**
  - `SKILL.md` — Main skill definition
  - `assets/email-templates.md` — Email templates

### 8. hidden-city-strategy
- **Purpose:** Skiplagging analysis (consent-gated, legal risk warning)
- **Files:**
  - `SKILL.md` — Main skill definition (disable-model-invocation: true)
  - `references/eligibility-check.md` — Eligibility criteria
  - `references/enforcement-levels.md` — Airline enforcement tracking

## Shared Python Scripts

### config.py
Manages API credentials:
- Loads `AMADEUS_API_KEY`, `AMADEUS_API_SECRET`, `KIWI_API_KEY` from environment
- Provides configuration object for all API clients

### kiwi_client.py
Wraps Kiwi Tequila API:
- Flight search with date flexibility
- Virtual interlining detection
- Real-time pricing

### kiwi_tequila.py
Advanced Kiwi integration:
- Multi-city search support
- Route alternatives
- Price trend analysis

### amadeus_client.py
Amadeus API client:
- OAuth2 authentication
- Real-time flight pricing
- Airline fee rules
- Seat availability

### normalize.py
Price normalization utilities:
- Currency conversion
- Fee deconstruction
- True cost calculation
- Savings breakdown

## Shared References

### user-profile-schema.md
Defines traveler profile structure:
- REQUIRED: origin, destination, departure_date, passengers
- OPTIONAL: return_date, flexibility, baggage, booking_type, loyalty_programs, risk_tolerance, cabin_class

### airport-codes.md
Comprehensive airport reference:
- Hub airports (SFO, DFW, NRT, HAN, ICN, etc.)
- IATA codes
- Alliance information (Star Alliance, OneWorld, SkyTeam)
- Strategic routing tips

### glossary.md
Aviation terminology:
- Airline terms (LCC, FSC, codeshare, virtual interlining, etc.)
- Pricing terms (base fare, taxes, fees, surcharges, etc.)
- Booking terms (skiplagging, throwaway ticket, hidden city, etc.)

### amadeus-api.md
Amadeus API reference:
- Authentication (OAuth2)
- Endpoints (flight search, pricing, seat map, etc.)
- Response formats
- Rate limits

### kiwi-api.md
Kiwi Tequila API reference:
- Authentication (API key)
- Endpoints (search, location, airlines, etc.)
- Virtual interlining data
- Response formats

## Workflow Orchestration

The root `SKILL.md` (flight-planner) orchestrates a 5-phase workflow:

**Phase 1: Collect Profile**
- Gather origin, destination, dates, passengers
- Infer defaults for optional fields

**Phase 2: Search (Parallel)**
- Run date-optimization + flight-search simultaneously
- Pass optimal dates to flight search for refinement

**Phase 3: Analyze (Sequential)**
- route-optimization → fee-analysis → deals-verification
- Each step refines options from previous step

**Phase 4: Assess (Conditional)**
- flexibility-analysis (if schedule uncertainty)
- negotiation-email (if corporate booking)
- hidden-city-strategy (only if user explicitly asks)

**Phase 5: Output**
- Generate consolidated comparison report
- Include savings breakdown, top 5 options, risk assessment
- Provide exact booking instructions

## Configuration & Setup

### Environment Variables
```bash
export KIWI_API_KEY="your_kiwi_key_here"
export AMADEUS_API_KEY="your_amadeus_key_here"
export AMADEUS_API_SECRET="your_amadeus_secret_here"
```

### Installation
```bash
git clone https://github.com/phucsystem/claude-skill-flight-planner.git
claude --add-dir /path/to/claude-skill-flight-planner
```

### Dependencies
- Python 3.8+
- `requests` library (for API calls)
- Claude Code platform

## Key Design Principles

1. **Modular Skills** — Each skill is independent and can be invoked standalone
2. **Two Modes** — AI-Knowledge (no API) and API-Enhanced (real-time data)
3. **Decision Support** — Never auto-books; always provides analysis and recommendations
4. **Safety Gates** — Hidden city strategy requires explicit consent + eligibility check
5. **Transparency** — All prices show advertised → true total; all deals tagged with confidence levels
6. **Corporate Focus** — Special negotiation skill for volume bookings

## Technology Stack

| Layer | Tech |
|-------|------|
| **Platform** | Claude Code (skill plugin system) |
| **Language** | Python 3 (scripts), Markdown (skill definitions) |
| **APIs** | Kiwi Tequila, Amadeus |
| **HTTP** | requests library |
| **Auth** | API keys, OAuth2 (Amadeus) |
| **Execution** | Claude Code orchestrator |

## File Inventory

| File | Type | Purpose |
|------|------|---------|
| SKILL.md | Markdown | Root orchestrator |
| README.md | Markdown | Getting started |
| CHANGELOG.md | Markdown | Release history |
| LICENSE | Text | MIT License |
| .gitignore | Text | Git ignore rules |
| config.py | Python | API configuration |
| kiwi_client.py | Python | Kiwi API wrapper |
| kiwi_tequila.py | Python | Advanced Kiwi integration |
| amadeus_client.py | Python | Amadeus API client |
| normalize.py | Python | Price normalization |
| user-profile-schema.md | Markdown | Profile schema |
| airport-codes.md | Markdown | Airport reference |
| glossary.md | Markdown | Aviation terminology |
| amadeus-api.md | Markdown | Amadeus API docs |
| kiwi-api.md | Markdown | Kiwi API docs |
| flow-diagram.html | HTML | Interactive workflow |
| report-template.md | Markdown | Report format |
| 8x SKILL.md files | Markdown | Individual skills |
| 8x skill references | Markdown | Skill-specific docs |
| 4x skill scripts | Python | Skill utilities |
| Examples | MD + HTML | Sample outputs |

## Version & History

- **Current Version:** 1.0.0 (released 2026-03-28)
- **License:** MIT
- **Repository:** https://github.com/phucsystem/claude-skill-flight-planner

## Next Steps

See `project-roadmap.md` for planned enhancements and future phases.
