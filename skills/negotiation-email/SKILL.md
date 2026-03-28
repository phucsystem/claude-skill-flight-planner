---
name: negotiation-email
description: Use when a company wants to negotiate corporate flight discounts with airlines. Triggers on corporate rate, bulk discount, airline negotiation, volume pricing, company travel budget.
---

# Negotiation Email - Email Thương Lượng Giá

## Purpose

Companies flying 100+ trips per year have real negotiating power but rarely use it. This skill crafts professional emails that airlines' sales teams take seriously - with market evidence, volume data, and strategic urgency.

## Input Required

- `company_name` from corporate profile
- `annual_flight_volume` (number of flights/year)
- `annual_spend` (total spend in USD)
- `target_airline` (who to negotiate with)
- `primary_routes` (most frequent routes)
- `competitor_pricing` (optional - prices from other airlines)
- `loyalty_status` (current tier with this airline, if any)

## Eligibility Check

Before generating, verify the company has negotiating leverage:

| Factor | Minimum for Leverage | Strong Position |
|--------|---------------------|----------------|
| Annual flights | 50+ | 200+ |
| Annual spend | $50,000+ | $200,000+ |
| Route concentration | 3+ routes with same airline | 5+ routes |
| Loyalty status | Silver tier | Gold/Platinum |

If below minimum: inform user that individual negotiation is unlikely to succeed. Suggest alternatives (credit card deals, group booking, corporate travel agency).

## Execution Steps

### Step 1: Identify Recipient

| Recipient | When to Use | Tone |
|-----------|-------------|------|
| Sales Manager / Corporate Sales | Volume > 100 flights/year | Professional, data-driven |
| Reservations Team Lead | Volume 50-100 | Polite, relationship-focused |
| Key Account Manager | Existing relationship | Collaborative, renewal-style |

Provide:
- Suggested department: "Corporate Sales" or "Key Accounts"
- Generic email format: corporatesales@airline.com
- LinkedIn approach: Search "[Airline] Corporate Sales Manager [Country]"

### Step 2: Build Email Structure

**Subject Line** (create curiosity without revealing max budget):
- "[Company] - [Volume] Annual Flights - Partnership Inquiry"
- "Corporate Rate Discussion - [City Pair] Route Focus"
- NOT: "Discount Request" (too weak)

**Opening (2 sentences)**:
- Who you are + company profile (1 line)
- Specific volume metric that demonstrates value

**Body** (3 paragraphs):

1. **Value proposition**: What the airline gets (guaranteed volume, route commitment, advance booking, off-peak flexibility)

2. **Market evidence**: Current alternatives you're evaluating
   - Reference competitor pricing without naming specific amounts
   - Mention that you're "evaluating proposals from carriers on [route]"
   - NEVER reveal your maximum acceptable price

3. **Specific ask**: Clear, reasonable request
   - "10-15% reduction on published fares for [route]"
   - Volume commitment in exchange
   - No long-term contract requirement (initially)

**Closing**:
- Deadline: "We're finalizing our Q3 travel arrangements by [date 2-3 weeks out]"
- Next step: "I'd welcome a brief call to discuss potential terms"
- CC suggestion: Your Finance Director or CEO (shows authority)

### Step 3: Generate Email

```
Subject: [Company Name] - [Volume] Annual Business Flights - Partnership Discussion

Dear [Corporate Sales Team / Mr./Ms. Last Name],

I'm [Name], [Title] at [Company Name]. We're currently evaluating our airline 
partnerships for [Year], with approximately [Volume] flights annually, primarily 
on [Route 1] and [Route 2].

Our team has been loyal [Airline] customers, and [X]% of our 2025 bookings were 
with your airline. As we plan our [Year] travel budget of approximately $[Range, 
not exact], we're reviewing proposals from several carriers to ensure competitive 
rates for our team.

We're seeking a [10-15]% improvement on published Economy/Business fares for our 
primary routes, in exchange for a commitment of [X flights/month] over the next 
12 months. We value the [specific benefit: direct routes, schedule reliability, 
lounge access] your airline provides and would prefer to consolidate our bookings 
with a single carrier.

Could we schedule a brief call before [date, 2-3 weeks out] to discuss potential 
terms? We're finalizing our travel arrangements for [next quarter] and want to 
ensure we make the right partnership choice.

Best regards,
[Name]
[Title], [Company]
[Phone] | [Email]

CC: [Finance Director / Travel Manager]
```

### Step 4: Follow-Up Strategy

If no response within 5 business days:

```
Subject: Re: [Original Subject] - Following up

Dear [Name],

Following up on my email from [date]. We're in the final stages of selecting 
our airline partner for [Year] and would value the opportunity to discuss 
terms with [Airline].

Our decision timeline is [date]. I'd appreciate even a brief response on 
whether corporate rates are available for our volume.

Best regards,
[Name]
```

### Step 5: Talking Points (if phone follow-up)

Prepare user with key points if airline calls back:
1. Lead with volume, not price complaints
2. Mention competitor by category ("several LCC options") not by name
3. Be willing to commit to minimum 60% share-of-wallet
4. Ask about soft benefits too: lounge access, priority boarding, dedicated booking line
5. Don't accept first offer - ask "Is that the best you can do for this volume?"

## Output Package

1. Email draft (ready to copy-paste)
2. CC suggestion with rationale
3. Timing recommendation (best day/time to send)
4. Follow-up email draft
5. Phone talking points (if call happens)
6. Counter-offer strategy (if airline's first response is weak)

## Important Notes

- NEVER include the company's maximum acceptable rate in the email
- NEVER name specific competitor prices (say "competitive alternatives exist")
- Emails work best when sent Tuesday-Thursday, 9-11 AM recipient's timezone
- Some airlines require minimum 12-month commitment for corporate rates
- Corporate rates usually apply to specific routes, not system-wide
