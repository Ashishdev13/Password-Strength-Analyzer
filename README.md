# Password-Strength-Analyzer

A Python-based cybersecurity tool that analyzes password strength, detects common and weak passwords, simulates breach database checks using the HIBP k-anonymity model, and provides actionable security recommendations.

> **Educational use only.**

## Demo

```
============================================================
       PASSWORD STRENGTH ANALYZER
       Cybersecurity Tool | Educational Use Only
============================================================

  Password      : M***!
  Length        : 18

  --- Strength Breakdown ---
    Length Score        : 20/25
    Uppercase Score     : 6/10
    Lowercase Score     : 10/10
    Digit Score         : 9/10
    Special Char Score  : 12/15
    Bonus (variety)     : +10
    Penalty (patterns)  : -0

    TOTAL SCORE  : 67/100   [STRONG]

  --- Entropy ---
    Character Pool Size : 94
    Bits of Entropy     : 117.8 bits

  --- Pattern Analysis ---
  ✓ No keyboard walk pattern (qwerty, asdf...)
  ✓ No repeated characters (aaa, 111...)
  ✓ No sequential numbers (1234, 5678...)
  ✓ No sequential letters (abcd, efgh...)
  ✓ No obvious date patterns (2024, 0101...)
  ✓ Mixed character cases used

  --- Common Password Check ---
  ✓ Not found in common passwords list

  --- Breach Check (Simulated HIBP) ---
  ✓ Password hash prefix not found in simulated breach list

  --- Recommendations ---
  ✓ Password meets all recommended criteria!
```

## Security Concepts Demonstrated

- **Password Entropy Calculation** — Shannon entropy (E = L x log2(R)) to measure password randomness
- **K-Anonymity Model** — Simulates the Have I Been Pwned (HIBP) API approach where only the first 5 characters of a SHA-1 hash are sent, keeping the full password private
- **Pattern Detection** — Identifies keyboard walks (qwerty, asdfgh), sequential characters, repeated characters, and date patterns
- **Common Password Lists** — Checks against the top 1000 most common passwords from real breach databases
- **Strength Scoring** — Multi-factor scoring with bonuses for character variety and penalties for weak patterns

## Features

- Strength scoring on a 0-100 scale with 5 levels
- Shannon entropy calculation with character pool analysis
- Common password detection (top 1000 list)
- Pattern detection (keyboard walks, dates, repeated/sequential chars)
- Breach check simulation (HIBP k-anonymity model)
- Colored CLI output (cross-platform via colorama)
- Batch mode for analyzing multiple passwords from a file
- Secure interactive mode with hidden input (getpass)

## Project Structure

```
Password-Strength-Analyzer/
├── analyzer.py              # Main CLI entry point
├── strength_checker.py      # Core strength analysis engine
├── entropy.py               # Entropy & character set calculations
├── pattern_detector.py      # Weak pattern detection
├── breach_checker.py        # Simulated HIBP k-anonymity lookup
├── common_passwords.txt     # Top 1000 most common passwords
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Dev/test dependencies
├── pytest.ini               # Pytest configuration
├── tests/
│   ├── conftest.py              # Shared test fixtures
│   ├── test_analyzer.py         # CLI & display tests
│   ├── test_strength_checker.py # Core scoring tests
│   ├── test_entropy.py          # Entropy calculation tests
│   ├── test_pattern_detector.py # Pattern detection tests
│   └── test_breach_checker.py   # Breach checker tests
└── README.md
```

## Tech Stack

- **Language:** Python 3.8+
- **Dependencies:** colorama (colored terminal output)
- **Testing:** pytest, pytest-cov
- **Standard Library:** hashlib, re, math, os, argparse, getpass

## Installation

```bash
git clone https://github.com/Ashishdev13/Password-Strength-Analyzer.git
cd Password-Strength-Analyzer
pip install -r requirements.txt
```

## Usage

```bash
# Interactive mode (password hidden from terminal)
python analyzer.py

# Analyze a specific password
python analyzer.py --password "MyP@ssw0rd!"

# Batch mode — analyze passwords from a file
python analyzer.py --file passwords.txt
```

## Strength Levels

| Score  | Level       |
|--------|-------------|
| 80-100 | Very Strong |
| 60-79  | Strong      |
| 40-59  | Moderate    |
| 20-39  | Weak        |
| 0-19   | Very Weak   |

## How It Works

**Entropy:** `E = L x log2(R)` where L = password length, R = character pool size

**Scoring Breakdown:**
| Category      | Max Points |
|---------------|-----------|
| Length         | 25        |
| Uppercase     | 10        |
| Lowercase     | 10        |
| Digits        | 10        |
| Special Chars | 15        |
| Variety Bonus | 10        |
| **Max Total** | **80**    |

Penalties are subtracted for repeated chars (-10), sequential numbers (-5), sequential letters (-5), and keyboard walks (-10 each).

**Breach Check (K-Anonymity):** Only the first 5 characters of the SHA-1 hash are used for lookup — the full password is never exposed.

## Test Suite

**88 tests** across 5 test files with **94% code coverage**.

```
tests/test_strength_checker.py  — 30 tests (scoring, levels, bonuses, penalties, recommendations)
tests/test_pattern_detector.py  — 22 tests (keyboard walks, repeats, sequences, dates, case)
tests/test_breach_checker.py    — 15 tests (breach detection, k-anonymity, hash info)
tests/test_entropy.py           — 13 tests (pool size, entropy bits, ratings)
tests/test_analyzer.py          — 8 tests  (CLI output, batch mode, display)
```

Run tests:
```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
python -m pytest tests/ --cov=. --cov-report=term-missing
```

## Code Review Summary

| Category | Issues Found | Issues Fixed |
|----------|-------------|-------------|
| Critical | 2 | 2 |
| High     | 5 | 5 |
| Medium   | 3 | 3 |

**Key fixes applied:**
- Fixed k-anonymity simulation to properly filter by hash prefix before matching suffix (was bypassing prefix filter)
- Fixed unreachable "VERY STRONG" level (max score was 80, threshold was 81)
- Added security warning for `--password` CLI flag (visible in shell history)
- Fixed edge case in password masking for short passwords
- Refactored nested ternary expressions into readable if/elif chains
- Added type hints across all modules
- Split multi-imports to PEP 8 compliant format
- Replaced cryptic single-letter variable names with descriptive names

## Dependencies

- **colorama** — colored terminal output (cross-platform)
- **hashlib, re, math** — Python standard library

## Resources

- [OWASP Password Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [Have I Been Pwned API](https://haveibeenpwned.com/API/v3)

## Disclaimer

This tool is for **educational and authorized security testing purposes only**. Do not use this tool to analyze passwords you do not own or have explicit permission to test. The simulated breach database is for demonstration only and does not represent real breach data. Always use a password manager for storing real credentials.

## License

MIT License
