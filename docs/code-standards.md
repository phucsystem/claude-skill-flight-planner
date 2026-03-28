# Code Standards & Conventions

## Overview

This document defines coding standards for the Travel Optimization Engine project across Python, Markdown, and Skill definitions.

## Python Code Standards

### File Organization

**File Naming:**
- Use `snake_case` for all Python files (e.g., `kiwi_client.py`, `date_matrix.py`)
- Descriptive names that convey purpose (e.g., `fee_calculator.py` not `calc.py`)
- Organize files by function in skill directories

**File Structure:**
```python
"""Module docstring describing purpose and main functions."""

import standard_library
import third_party
from local_module import something

# Constants (UPPER_CASE)
DEFAULT_TIMEOUT = 30
API_ENDPOINTS = {...}

# Classes
class DataProcessor:
    """Class docstring."""
    pass

# Functions
def main_function():
    """Function docstring."""
    pass

if __name__ == "__main__":
    main_function()
```

### Python Style

**General Principles:**
- Follow PEP 8 for readability and consistency
- Use descriptive variable names (no single letters except `i` in short loops)
- Write for clarity first, optimization second
- Comment non-obvious logic only

**Naming Conventions:**
```python
# Variables and functions: snake_case
user_profile = {}
def calculate_total_cost():
    pass

# Classes: PascalCase
class FlightOption:
    pass

# Constants: UPPER_CASE
MAX_PASSENGERS = 9
TIMEOUT_SECONDS = 30

# Private members: leading underscore
_internal_helper_function()
self._private_attribute = None
```

**Type Hints (Recommended):**
```python
from typing import Dict, List, Optional

def search_flights(
    origin: str,
    destination: str,
    date: str,
    passengers: int = 1
) -> List[Dict[str, any]]:
    """Search flights and return options."""
    pass
```

**Error Handling:**
```python
try:
    result = api_call()
except requests.exceptions.Timeout:
    logger.error("API timeout", exc_info=True)
    return fallback_result()
except Exception as err:
    logger.exception("Unexpected error: %s", err)
    raise
```

**Configuration Management:**
```python
# Load from environment variables
import os

API_KEY = os.getenv("KIWI_API_KEY")
if not API_KEY:
    logger.warning("KIWI_API_KEY not set, using AI-knowledge mode")
    API_KEY = None
```

### Python Scripts Checklist

- [ ] Descriptive module docstring at top
- [ ] Imports organized (stdlib → third-party → local)
- [ ] All functions have docstrings
- [ ] Type hints on function signatures
- [ ] Error handling with try/except blocks
- [ ] Logging instead of print() for debug output
- [ ] Configuration via environment variables, never hardcoded
- [ ] Unit tests for critical logic (optional but recommended)
- [ ] No API keys or credentials in code

## Markdown Standards

### File Organization

**File Naming:**
- Use `kebab-case` for all Markdown files (e.g., `user-profile-schema.md`)
- Descriptive names (e.g., `virtual-interlining.md` not `vi.md`)

**File Structure:**
```markdown
# Title (H1 — one per file)

> Brief one-liner summary or quote

## Section 1

Content here.

### Subsection 1a

More content.

## Section 2

- Bullet point 1
- Bullet point 2

| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |

## References

- [Link Text](https://example.com)
```

### Markdown Style

**General Principles:**
- One H1 (`#`) per file
- Hierarchy: H1 → H2 → H3 → H4 (max)
- Use sections to break up long content
- Lead with purpose, not background

**Formatting:**
- `code` for inline code (functions, variables, file names)
- ````python` code blocks with language hints
- **bold** for emphasis
- *italic* for terms
- `> blockquote` for tips or important notes

**Lists:**
```markdown
## Unordered List
- Item 1
- Item 2
  - Nested item 2a
  - Nested item 2b
- Item 3

## Ordered List
1. Step 1
2. Step 2
3. Step 3

## Checklist
- [x] Completed task
- [ ] Incomplete task
```

**Tables:**
```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

**Code Blocks:**
Use language hints for syntax highlighting:
```python
def calculate_savings(base_price, discount_price):
    return base_price - discount_price
```

```json
{
  "origin": "HAN",
  "destination": "SFO",
  "passengers": 3
}
```

**Links:**
- Internal links: `[Text](./relative/path.md)` (use relative paths in docs/)
- External links: `[Text](https://example.com)`
- Never link to files without verifying they exist

### Markdown Checklist

- [ ] One H1 title at top
- [ ] Table of contents for long files (>500 lines)
- [ ] Links are relative paths (docs/) or external (https://)
- [ ] Code blocks have language hints
- [ ] No trailing whitespace
- [ ] Consistent heading hierarchy
- [ ] Tables properly formatted
- [ ] Lists use consistent symbols (- for bullets, 1. for ordered)

## Skill Definition Standards (SKILL.md)

### Frontmatter

Every `SKILL.md` must start with YAML frontmatter:

```yaml
---
name: skill-name
description: "Clear description of what skill does, when to use it."
argument-hint: "[origin] [destination] [dates]"
allowed-tools: Bash(python *), Read, Glob, Grep
---
```

**Fields:**
- `name` (required): Lowercase kebab-case, unique skill identifier
- `description` (required): One sentence describing purpose + when to use it
- `argument-hint` (optional): Example arguments user might provide
- `allowed-tools` (optional): Tools skill is permitted to use
- `disable-model-invocation: true` (optional): For gated skills like hidden-city-strategy
- `context: fork` (optional): For high-risk skills requiring isolated context

### Content Structure

```markdown
---
name: skill-name
description: "..."
---

# Skill Name

> One-sentence summary.

## Purpose

Paragraph explaining what skill does and when to use it.

## Inputs

Describe expected input:
- `field_name`: Description
- `optional_field`: Description (optional)

## Process

Numbered steps:
1. First step
2. Second step
3. Final step

## Output

Describe output:
- `output_field`: Description
- `recommendations`: Always include actionable recommendations

## Example

Provide concrete example:
```
Input: HAN → SFO, dates 2026-06-15 to 2026-06-25
Output: Date matrix showing 2026-06-17 as cheapest (-$120 vs baseline)
```

## Important Notes

- Safety/ethics considerations
- Limitations or caveats
- Edge cases

## References

- [Link to related docs](./references/file.md)
- [External API](https://example.com)
```

### Skill Definition Checklist

- [ ] Frontmatter with name, description, allowed-tools
- [ ] Clear purpose statement
- [ ] Inputs section with field descriptions
- [ ] Process section with numbered steps
- [ ] Output section with field descriptions
- [ ] Concrete example
- [ ] Important notes (safety, limits, edge cases)
- [ ] References to related documentation

## API Client Standards

### Configuration Pattern

```python
# config.py
import os
from typing import Dict, Optional

class APIConfig:
    """Centralized API configuration."""

    def __init__(self):
        self.kiwi_api_key = os.getenv("KIWI_API_KEY")
        self.amadeus_api_key = os.getenv("AMADEUS_API_KEY")
        self.amadeus_secret = os.getenv("AMADEUS_API_SECRET")

    def is_api_available(self) -> bool:
        """Check if APIs are configured."""
        return bool(self.kiwi_api_key or self.amadeus_api_key)

config = APIConfig()
```

### HTTP Request Pattern

```python
# client.py
import requests
from requests.exceptions import Timeout, ConnectionError

class APIClient:
    """Base API client with error handling."""

    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout
        self.base_url = "https://api.example.com/v1"

    def request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make HTTP request with error handling."""
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except Timeout:
            raise APIError(f"Request timeout after {self.timeout}s")
        except ConnectionError:
            raise APIError("Connection failed, check network")
        except requests.exceptions.HTTPError as err:
            raise APIError(f"API error: {err.response.status_code}")
```

## Reference Document Standards

### Glossary Pattern

```markdown
# Glossary

## Abbreviations

### LCC
Low-cost carrier (e.g., AirAsia, Southwest)

### FSC
Full-service carrier (e.g., United, Lufthansa)

## Terms

### Virtual Interlining
Combining flights from different airlines...

### Skiplagging
Intentionally booking through a city to reach...
```

### API Reference Pattern

```markdown
# API Reference

## Base URL
`https://api.example.com/v1`

## Authentication
- Type: API Key
- Header: `Authorization: Bearer {API_KEY}`
- Register: https://example.com/register

## Endpoints

### Search Flights
- **Method:** GET
- **Path:** `/search`
- **Query Params:**
  - `origin` (required): IATA code
  - `destination` (required): IATA code
  - `date` (required): YYYY-MM-DD

**Response:**
```json
{
  "flights": [
    {
      "id": "FL001",
      "airline": "AA",
      "price": 500
    }
  ]
}
```

**Errors:**
- 400: Invalid parameters
- 401: Authentication failed
- 429: Rate limit exceeded
```

## Documentation Standards

### docs/ Directory Structure

```
docs/
├── codebase-summary.md        # Full file inventory
├── project-overview-pdr.md    # Vision, requirements, acceptance criteria
├── code-standards.md          # This file
├── system-architecture.md     # Architecture diagrams
├── project-roadmap.md         # Timeline, phases, future work
└── README.md                  # Getting started guide (in root)
```

### Documentation Checklist

- [ ] All docs in English
- [ ] Each file under 800 lines (split if needed)
- [ ] Code examples verified to exist in codebase
- [ ] All links are relative or external (https://)
- [ ] No API keys or credentials in examples
- [ ] Tables properly formatted
- [ ] Consistent heading hierarchy
- [ ] Proper YAML frontmatter for SKILL.md files

## Git Commit Standards

### Commit Message Format

Use conventional commits:
```
feat: add date optimization skill
fix: correct fee calculation for taxes
docs: update API reference
refactor: simplify flight search logic
test: add unit tests for price normalization
chore: update dependencies
```

**Rules:**
- Start with type: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- Use imperative mood ("add" not "added")
- First line under 70 characters
- Reference issue numbers if applicable: `fix: #123`
- No AI references in commit messages

### Git Checklist

- [ ] Focused commit (one feature or fix per commit)
- [ ] Clear commit message
- [ ] No API keys in commit
- [ ] All tests pass before pushing
- [ ] Documentation updated for new features

## Code Review Checklist

When reviewing code:

### Python Scripts
- [ ] No hardcoded API keys or credentials
- [ ] Error handling with try/except
- [ ] Type hints on public functions
- [ ] Docstrings on classes and functions
- [ ] Follows PEP 8 style guide
- [ ] No unused imports or variables
- [ ] Logging used instead of print()

### Markdown Documents
- [ ] One H1 title per file
- [ ] Links verified (relative or https://)
- [ ] Code examples match actual codebase
- [ ] Consistent formatting and style
- [ ] No trailing whitespace
- [ ] Tables properly aligned

### Skill Definitions
- [ ] Frontmatter complete (name, description, allowed-tools)
- [ ] Clear inputs/outputs sections
- [ ] Numbered process steps
- [ ] Concrete examples provided
- [ ] Safety notes included if applicable
- [ ] References to related docs

## Version Control Standards

### Branching Strategy
- `main` or `master` — production-ready code
- `develop` — development branch
- Feature branches: `feature/brief-description`
- Bug fixes: `fix/brief-description`

### Release Process
1. Update `CHANGELOG.md`
2. Update version numbers
3. Create release commit
4. Tag release: `v1.0.0`
5. Push to GitHub

## Maintenance Guidelines

### Regular Updates
- **Monthly:** Update deal sources and promo codes
- **Quarterly:** Review hub routing strategies
- **Bi-annually:** Update airline fee matrices
- **Annually:** Review entire documentation

### Deprecation Process
1. Mark feature as "deprecated" in code comments
2. Add warning to documentation
3. Provide migration path
4. Wait one release cycle
5. Remove deprecated feature

## References

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Skill Definition Template](../SKILL.md)
