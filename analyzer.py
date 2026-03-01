#!/usr/bin/env python3
"""
Password Strength Analyzer - Main CLI Entry Point
A cybersecurity tool to analyze password strength and security.
Educational use only.
"""

import argparse
import sys
import getpass
from strength_checker import StrengthChecker
from breach_checker import BreachChecker

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS = True
except ImportError:
    COLORS = False
    class Fore:
        RED = YELLOW = GREEN = CYAN = WHITE = MAGENTA = ""
    class Style:
        BRIGHT = RESET_ALL = ""


def colorize(text, color):
    if COLORS:
        return color + text + Style.RESET_ALL
    return text


def print_banner():
    banner = """
============================================================
       PASSWORD STRENGTH ANALYZER
       Cybersecurity Tool | Educational Use Only
============================================================"""
    print(colorize(banner, Fore.CYAN))


def get_level_color(score):
    if score >= 81:
        return Fore.GREEN
    elif score >= 61:
        return Fore.CYAN
    elif score >= 41:
        return Fore.YELLOW
    elif score >= 21:
        return Fore.RED
    else:
        return Fore.RED


def display_results(password, result):
    """Display analysis results in a formatted way."""
    masked = password[0] + '*' * (len(password) - 2) + password[-1] if len(password) > 2 else '***'

    print()
    print(colorize(f"  Password      : {masked}", Fore.WHITE))
    print(colorize(f"  Length        : {len(password)}", Fore.WHITE))
    print()
    print(colorize("  --- Strength Breakdown ---", Style.BRIGHT))
    print(f"    Length Score        : {result['scores']['length']}/25")
    print(f"    Uppercase Score     : {result['scores']['uppercase']}/10")
    print(f"    Lowercase Score     : {result['scores']['lowercase']}/10")
    print(f"    Digit Score         : {result['scores']['digits']}/10")
    print(f"    Special Char Score  : {result['scores']['special']}/15")
    print(f"    Bonus (variety)     : +{result['scores']['bonus']}")
    print(f"    Penalty (patterns)  : -{result['scores']['penalty']}")

    score = result['total_score']
    level = result['level']
    level_color = get_level_color(score)
    print()
    print(colorize(f"    TOTAL SCORE  : {score}/100   [{level}]", level_color + Style.BRIGHT))

    print()
    print(colorize("  --- Entropy ---", Style.BRIGHT))
    print(f"    Character Pool Size : {result['entropy']['pool_size']}")
    print(f"    Bits of Entropy     : {result['entropy']['bits']:.1f} bits")

    print()
    print(colorize("  --- Pattern Analysis ---", Style.BRIGHT))
    for check, passed, msg in result['patterns']:
        icon = colorize("  ✓", Fore.GREEN) if passed else colorize("  ✗", Fore.RED)
        print(f"{icon} {msg}")

    print()
    print(colorize("  --- Common Password Check ---", Style.BRIGHT))
    if result['is_common']:
        print(colorize("  ✗ This password appears in the common passwords list!", Fore.RED))
    else:
        print(colorize("  ✓ Not found in common passwords list", Fore.GREEN))

    print()
    print(colorize("  --- Breach Check (Simulated HIBP) ---", Style.BRIGHT))
    breach = BreachChecker().check(password)
    if breach['found']:
        print(colorize(f"  ✗ Password hash found in simulated breach database!", Fore.RED))
    else:
        print(colorize("  ✓ Password hash prefix not found in simulated breach list", Fore.GREEN))

    print()
    print(colorize("  --- Recommendations ---", Style.BRIGHT))
    if result['recommendations']:
        for rec in result['recommendations']:
            print(colorize(f"  • {rec}", Fore.YELLOW))
    else:
        print(colorize("  ✓ Password meets all recommended criteria!", Fore.GREEN))

    print()
    print("=" * 60)


def analyze_password(password):
    checker = StrengthChecker()
    result = checker.analyze(password)
    display_results(password, result)


def batch_analyze(filepath):
    try:
        with open(filepath, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
        print(colorize(f"\n  Analyzing {len(passwords)} passwords from {filepath}...\n", Fore.CYAN))
        for pwd in passwords:
            analyze_password(pwd)
    except FileNotFoundError:
        print(colorize(f"  Error: File '{filepath}' not found.", Fore.RED))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Password Strength Analyzer - Educational Cybersecurity Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Examples:\n  python analyzer.py\n  python analyzer.py --password "MyPass123!"\n  python analyzer.py --file passwords.txt'
    )
    parser.add_argument('--password', '-p', type=str, help='Password to analyze')
    parser.add_argument('--file', '-f', type=str, help='File containing passwords (one per line)')
    args = parser.parse_args()

    print_banner()

    if args.file:
        batch_analyze(args.file)
    elif args.password:
        analyze_password(args.password)
    else:
        print(colorize("\n  Enter a password to analyze (input is hidden):", Fore.CYAN))
        try:
            password = getpass.getpass("  Password: ")
            if not password:
                print(colorize("  Error: Password cannot be empty.", Fore.RED))
                sys.exit(1)
            analyze_password(password)
        except KeyboardInterrupt:
            print(colorize("\n\n  Cancelled by user.", Fore.YELLOW))
            sys.exit(0)


if __name__ == '__main__':
    main()
