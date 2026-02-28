# Password-Strength-Analyzer

A Python-based cybersecurity tool that analyzes password strength, detects common and weak passwords, simulates breach database checks, and provides actionable security recommendations.

> **Educational use only.**

## Features

- Strength Scoring (0-100 scale)
- Entropy Calculation
- Common Password Detection (top 1000 list)
- Pattern Detection (keyboard walks, dates, repeated chars)
- Breach Check Simulation (HIBP k-anonymity model)
- Colored CLI Output
- Batch mode for multiple passwords

## Project Structure

```
Password-Strength-Analyzer/
├── analyzer.py            # Main CLI entry point
├── strength_checker.py    # Core strength analysis engine
├── entropy.py             # Entropy & character set calculations
├── pattern_detector.py    # Weak pattern detection
├── breach_checker.py      # Simulated HIBP k-anonymity lookup
├── common_passwords.txt   # Top 1000 most common passwords
├── requirements.txt       # Python dependencies
└── README.md
```

## Installation

```bash
git clone https://github.com/Ashishdev13/Password-Strength-Analyzer.git
cd Password-Strength-Analyzer
pip install -r requirements.txt
```

## Usage

```bash
# Interactive mode
python analyzer.py

# Analyze a specific password
python analyzer.py --password "MyP@ssw0rd!"

# Batch mode
python analyzer.py --file passwords.txt
```

## Strength Levels

| Score  | Level       |
|--------|-------------|
| 0-20   | Very Weak   |
| 21-40  | Weak        |
| 41-60  | Moderate    |
| 61-80  | Strong      |
| 81-100 | Very Strong |

## How It Works

**Entropy:** E = L x log2(R) where L = length, R = character pool size

**Breach Check (K-Anonymity):** Only the first 5 chars of the SHA-1 hash are used, so the full password is never exposed.

## Dependencies

- colorama - colored terminal output
- hashlib, re, math (standard library)

## Resources

- [OWASP Password Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [Have I Been Pwned API](https://haveibeenpwned.com/API/v3)

## Disclaimer

For educational purposes only. Do not use against passwords you do not own.

## License

MIT License
