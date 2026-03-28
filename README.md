# Travel Optimization Engine — Claude Code Skill

> Decision support system for flight cost optimization. Save 30-66% on personal travel, 10-15% on corporate bookings.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills: 8](https://img.shields.io/badge/Skills-8-blue.svg)](#available-skills)
[![Platform: Claude Code](https://img.shields.io/badge/Platform-Claude_Code-blue.svg)](https://code.claude.com)

## Quick Start

### Installation

```bash
git clone https://github.com/phucsystem/claude-skill-flight-planner.git
claude --add-dir /path/to/claude-skill-flight-planner
```

### Usage

Just tell Claude your travel plans:

```
"I want to fly from Hanoi to San Francisco, 2 adults + 1 child,
mid-June 2026, flexible ±1 week on dates"
```

Claude automatically triggers the appropriate skills to analyze pricing, fees, routes, and deals.

## Available Skills

| Command | Description |
|---------|-------------|
| `/flight-planner` | Full optimization pipeline (orchestrator) |
| `/date-optimization` | Find cheapest travel dates within flexibility window |
| `/flight-search` | Multi-source flight search with virtual interlining |
| `/fee-analysis` | Hidden fee analysis and true cost calculation |
| `/route-optimization` | Hub-based route alternatives |
| `/deals-verification` | Promo codes and discount verification |
| `/flexibility-analysis` | Refundable vs non-refundable break-even analysis |
| `/negotiation-email` | Corporate discount email templates |
| `/hidden-city-strategy` | Skiplagging analysis (manual invoke, legal risk disclosure) |

## How It Works

### 5-Phase Workflow

**Phase 1: Collect** — Gather origin, destination, dates, passengers, preferences

**Phase 2: Search** (Parallel)
- Date optimization: Find cheapest dates
- Flight search: Search across multiple sources
- Results merged for best options

**Phase 3: Analyze** (Sequential)
- Route optimization: Find cheaper hub alternatives
- Fee analysis: Deconstruct hidden fees, recalculate true total
- Deals verification: Find applicable promo codes

**Phase 4: Assess** (Conditional)
- Flexibility analysis: Refundable vs non-refundable risk
- Negotiation email: Corporate volume discounts (if corporate booking)
- Hidden city strategy: Skiplagging analysis (if user asks + consent)

**Phase 5: Output** — Generate consolidated comparison report with savings breakdown

## Two Operating Modes

### AI-Knowledge Mode (No API Required)

- Uses AI training data for flight pricing, trends, airline policies
- Sufficient for most use cases
- Works immediately without setup

### API-Enhanced Mode (Real-Time Data)

Configure API keys for real-time pricing and expanded options:

```bash
# macOS/Linux
export KIWI_API_KEY="your_api_key"
export AMADEUS_API_KEY="your_amadeus_key"
export AMADEUS_API_SECRET="your_amadeus_secret"

# Windows PowerShell
$env:KIWI_API_KEY="your_api_key"
$env:AMADEUS_API_KEY="your_amadeus_key"
$env:AMADEUS_API_SECRET="your_amadeus_secret"
```

Register free at [Kiwi Tequila](https://tequila.kiwi.com/), [Amadeus](https://developers.amadeus.com).

## Example Output

```
╔════════════════════════════════════════════════╗
║  TRAVEL OPTIMIZATION REPORT                    ║
║  HAN → SFO, 2A+1C, Jun 15-25, 2026           ║
╠════════════════════════════════════════════════╣
║                                                ║
║  BEST OPTION: Korean Air via ICN               ║
║  True Total: $2,115 ($705/person)              ║
║  Saved: $885 vs baseline direct (-30%)         ║
║                                                ║
║  Savings Breakdown:                            ║
║  - Optimal date shift:        -$240            ║
║  - Hub routing via ICN:       -$345            ║
║  - Bank card promo:           -$120            ║
║  - Deal "KE Global Sale":     -$180            ║
║                                                ║
║  Flexibility: 65/100 (Economy Plus)            ║
║  Risk: Low (schedule 90% certain)              ║
╚════════════════════════════════════════════════╝
```

## Key Features

### For Personal Travel

- Compare 20+ flight options with true cost (all fees included)
- Find cheapest dates within your flexibility window
- Discover cheaper hub-based alternatives
- Identify applicable promo codes and flash sales
- Assess refundable vs non-refundable risk

### For Corporate Travel

- Generate negotiation emails with volume data
- Track competitor pricing and market trends
- Analyze savings opportunities per route
- Build business case for rate renegotiation
- Match negotiated rates to market

## Safety & Ethics

- **Hidden City Strategy:** Requires explicit consent + eligibility check + full legal risk disclosure
- **Virtual Interlining:** Warns about missed connection risk and baggage rules
- **Deal Verification:** All deals tagged with confidence level (HIGH/MEDIUM/LOW/EXPIRED)
- **Corporate Negotiation:** Never reveals customer's max budget to airlines

## Documentation

- **Getting Started:** See [README.md](README.md) (this file)
- **Project Overview & Requirements:** See [docs/project-overview-pdr.md](docs/project-overview-pdr.md)
- **System Architecture:** See [docs/system-architecture.md](docs/system-architecture.md)
- **Code Standards:** See [docs/code-standards.md](docs/code-standards.md)
- **Codebase Summary:** See [docs/codebase-summary.md](docs/codebase-summary.md)
- **Project Roadmap:** See [docs/project-roadmap.md](docs/project-roadmap.md)

## Architecture

```
travel-optimization-engine/
├── SKILL.md                    # Root orchestrator
├── README.md                   # This file
├── CHANGELOG.md                # Release history
├── docs/                       # Comprehensive documentation
│   ├── codebase-summary.md
│   ├── project-overview-pdr.md
│   ├── code-standards.md
│   ├── system-architecture.md
│   └── project-roadmap.md
├── scripts/                    # Shared Python utilities
│   ├── config.py               # API credential management
│   ├── kiwi_client.py          # Kiwi API wrapper
│   ├── kiwi_tequila.py         # Advanced Kiwi integration
│   ├── amadeus_client.py       # Amadeus API client
│   └── normalize.py            # Price normalization
├── references/                 # Shared reference data
│   ├── airport-codes.md        # Hub airports, IATA codes
│   ├── glossary.md             # Aviation terminology
│   ├── user-profile-schema.md  # Traveler data structure
│   ├── amadeus-api.md          # Amadeus API reference
│   └── kiwi-api.md             # Kiwi API reference
├── skills/                     # 8 specialized sub-skills
│   ├── date-optimization/
│   ├── flight-search/
│   ├── fee-analysis/
│   ├── route-optimization/
│   ├── deals-verification/
│   ├── flexibility-analysis/
│   ├── negotiation-email/
│   └── hidden-city-strategy/
├── assets/
│   ├── flow-diagram.html       # Interactive workflow
│   └── report-template.md      # Report template
└── examples/
    ├── flight-optimization-report-HAN-SFO-Jun2026.md
    └── flight-optimization-report-HAN-SFO-Jun2026.html
```

## Contributing

Issues and pull requests welcome! See [CHANGELOG.md](CHANGELOG.md) for release history.

To contribute:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear description
4. Ensure code follows standards in [docs/code-standards.md](docs/code-standards.md)

## Credits

Built by [Minh Đỗ](https://github.com/phucsystem) with Antigravity Skill Architecture Standards.

Real-time flight data powered by [Kiwi Tequila](https://tequila.kiwi.com/) and [Amadeus](https://amadeus.com/).

## License

[MIT](LICENSE)
