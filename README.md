# Password Strength Analyzer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Purpose](https://img.shields.io/badge/Purpose-Educational%20%2F%20Authorized%20Use-orange)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

> **For educational and authorized security research only.**
> Do not use this tool to analyze passwords you do not own or have explicit permission to test.

---

## What Is This?

The **Password Strength Analyzer** is a modular, Python-based CLI tool that evaluates password security through multi-factor scoring, entropy analysis, pattern detection, common password matching, and a simulated breach database check using the HIBP k-anonymity model.

This project was built to demonstrate how security professionals and developers assess password strength - the same principles used by password managers, identity platforms, and NIST-aligned authentication systems to enforce secure credential policies.

---

## Security Concepts Demonstrated

| Concept | Description |
|---------|-------------|
| **Shannon Entropy** | Calculates information entropy (E = L x log2(R)) to quantify password randomness - higher bits means more brute-force resistance |
| **K-Anonymity Model** | Simulates the Have I Been Pwned (HIBP) API approach where only the first 5 characters of a SHA-1 hash are sent, so the full password is never transmitted |
| **Pattern Detection** | Identifies keyboard walks (qwerty, asdfgh), sequential characters (abc, 123), repeated characters (aaa), and date patterns (2024, 0101) |
| **Common Password Lists** | Checks against the top 1000 most common passwords from real-world breach databases - passwords found are immediately capped to a low score |
| **Multi-Factor Scoring** | Scores based on length, character variety (upper/lower/digit/special), with bonuses for mixing all types and penalties for weak patterns |
| **Secure Input Handling** | Interactive mode uses `getpass` to hide password input from the terminal - prevents shoulder surfing and terminal history leakage |
| **Modular Architecture** | Each analysis technique is an independent module - entropy, patterns, breach checking, and scoring are all decoupled and independently testable |

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.8+ | Core runtime |
| **Scoring** | `strength_checker.py` | Multi-factor password strength analysis engine |
| **Entropy** | `entropy.py` | Shannon entropy calculation with character pool analysis |
| **Patterns** | `pattern_detector.py` | Keyboard walk, sequence, repeat, and date detection |
| **Breach Check** | `breach_checker.py` | Simulated HIBP k-anonymity SHA-1 prefix matching |
| **Hashing** | `hashlib` (stdlib) | SHA-1 hashing for breach simulation |
| **Regex** | `re` (stdlib) | Pattern matching for weak password detection |
| **Math** | `math` (stdlib) | Logarithmic entropy calculations |
| **CLI** | `argparse` (stdlib) | Command-line interface with interactive and batch modes |
| **Secure Input** | `getpass` (stdlib) | Hidden password input in interactive mode |
| **Terminal UI** | `colorama` | Cross-platform colored output |
| **Testing** | `pytest` + `pytest-cov` | Unit tests with 94% coverage |

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/Ashishdev13/Password-Strength-Analyzer.git
cd Password-Strength-Analyzer

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
# Interactive mode (password hidden from terminal)
python analyzer.py

# Analyze a specific password (WARNING: visible in shell history)
python analyzer.py --password "MyP@ssw0rd!"

# Batch mode - analyze multiple passwords from a file
python analyzer.py --file passwords.txt
```

### CLI Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--password` | `-p` | Password to analyze (visible in shell history - prefer interactive mode) |
| `--file` | `-f` | File containing passwords to analyze (one per line) |

### Sample Output

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

---

## How It Works

### Scoring Breakdown

| Category | Max Points | How It's Calculated |
|----------|-----------|---------------------|
| Length | 25 | 5 pts at 8 chars, scaling to 25 at 20+ chars |
| Uppercase | 10 | 3 pts per uppercase letter (capped at 10) |
| Lowercase | 10 | 2 pts per lowercase letter (capped at 10) |
| Digits | 10 | 3 pts per digit (capped at 10) |
| Special Chars | 15 | 4 pts per special character (capped at 15) |
| Variety Bonus | 10 | +10 for all 4 types, +5 for 3 types |
| **Max Total** | **80** | Before penalties |

### Penalties

| Pattern | Penalty |
|---------|---------|
| Repeated characters (aaa, 111) | -10 |
| Sequential numbers (123, 456) | -5 |
| Sequential letters (abc, def) | -5 |
| Keyboard walks (qwerty, asdfgh) | -10 each |

### Strength Levels

| Score | Level |
|-------|-------|
| 80-100 | Very Strong |
| 60-79 | Strong |
| 40-59 | Moderate |
| 20-39 | Weak |
| 0-19 | Very Weak |

### Entropy

`E = L x log2(R)` where L = password length and R = character pool size (26 lowercase + 26 uppercase + 10 digits + 32 special + 128 unicode if present).

### Breach Check (K-Anonymity)

1. Hash the password with SHA-1
2. Take the first 5 characters of the hex hash
3. Query only those 5 chars against the database
4. Match the suffix locally - the full hash is never exposed
5. In production, this queries `https://api.pwnedpasswords.com/range/{prefix}`

---

## Testing

The project includes a comprehensive **pytest** test suite covering all modules with a focus on security-critical code paths.

### Quick Start

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=term-missing
```

### Coverage Summary

| Module | Coverage | Key Tests |
|--------|----------|-----------|
| `breach_checker.py` | 100% | K-anonymity prefix filtering, hash info structure, known breach detection |
| `entropy.py` | 100% | Pool size calculation, entropy bits scaling, rating thresholds |
| `pattern_detector.py` | 100% | Keyboard walks, repeated chars, sequential nums/alpha, date patterns, case mixing |
| `strength_checker.py` | 97% | Score bounds, level classification, length/char scoring, bonus/penalty, recommendations |
| `analyzer.py` | 73% | CLI output formatting, batch mode, file-not-found handling |
| **Overall** | **94%** | **88 tests, all passing** |

### Security-Critical Tests

These tests verify the fixes for vulnerabilities found during code review:

- **K-anonymity correctness** - breach check properly filters by hash prefix before matching suffix (verifies dead code fix)
- **Unreachable level fix** - "VERY STRONG" level is achievable with max score (verifies threshold alignment)
- **Short password masking** - passwords under 3 chars are fully masked, preventing information leakage
- **Common password cap** - passwords found in breach lists are immediately capped to score 15 regardless of complexity
- **Hash prefix isolation** - prefix + suffix always reconstructs the full SHA-1 hash (verifies k-anonymity model integrity)

---

## Code Review Summary

| Category | Issues Found | Issues Fixed |
|----------|-------------|-------------|
| Critical | 2 | 2 |
| High | 5 | 5 |
| Medium | 3 | 3 |

Key fixes applied:

- **K-anonymity simulation** - was bypassing prefix filter and checking full database directly; fixed to properly filter by prefix then match suffix
- **Unreachable strength level** - max score was 80 but "VERY STRONG" threshold was 81; aligned thresholds
- **CLI security warning** - `--password` flag exposes password in shell history; added warning in help text
- **Short password masking** - edge case for passwords under 3 chars; now fully masks instead of partial display
- **Code quality** - refactored nested ternaries, added type hints, split multi-imports (PEP 8), replaced cryptic variable names

---

## Project Structure

```
Password-Strength-Analyzer/
├── analyzer.py              # Main CLI entry point + display
├── strength_checker.py      # Core strength analysis engine
├── entropy.py               # Shannon entropy calculations
├── pattern_detector.py      # Weak pattern detection (keyboard walks, sequences, dates)
├── breach_checker.py        # Simulated HIBP k-anonymity breach lookup
├── common_passwords.txt     # Top 1000 most common passwords
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Test dependencies (pytest, coverage)
├── pytest.ini               # Pytest configuration
├── tests/
│   ├── conftest.py              # Shared fixtures (strong/weak/common passwords)
│   ├── test_analyzer.py         # CLI output and batch mode tests
│   ├── test_strength_checker.py # Core scoring and recommendation tests
│   ├── test_entropy.py          # Entropy calculation and rating tests
│   ├── test_pattern_detector.py # Pattern detection tests
│   └── test_breach_checker.py   # Breach checker and k-anonymity tests
└── README.md
```

---

## Resources

- [OWASP Password Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [NIST SP 800-63B - Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [Have I Been Pwned API v3](https://haveibeenpwned.com/API/v3)
- [Shannon Entropy - Wikipedia](https://en.wikipedia.org/wiki/Entropy_(information_theory))

---

## Disclaimer

> **This tool is provided for educational and authorized security research purposes only.**
>
> The techniques demonstrated in this project - including password entropy analysis, breach database simulation, and pattern detection - are standard methods used by password managers, identity platforms, and security auditors to enforce strong credential policies.
>
> **Do not use this tool to analyze passwords you do not own or have explicit permission to test.** The simulated breach database is for demonstration only and does not represent real breach data. Always use a password manager for storing real credentials.
>
> The author assumes no liability for misuse of this software. By using this tool, you confirm that you are operating within the bounds of the law and with proper authorization.

---

## License

MIT License - see [LICENSE](LICENSE) for details.
