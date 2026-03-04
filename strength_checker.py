#!/usr/bin/env python3
"""
Strength Checker Module - Core password strength analysis engine.
"""
import os
import re
from typing import Any

from entropy import EntropyCalculator
from pattern_detector import PatternDetector

COMMON_PASSWORDS_FILE = os.path.join(os.path.dirname(__file__), 'common_passwords.txt')


def load_common_passwords() -> set[str]:
    try:
        with open(COMMON_PASSWORDS_FILE, 'r') as f:
            return set(line.strip().lower() for line in f if line.strip())
    except FileNotFoundError:
        return set()


COMMON_PASSWORDS = load_common_passwords()


class StrengthChecker:
    MAX_SCORE = 100
    SPECIAL_CHARS = set('!@#$%^&*()_+-=[]{}|;<>?,./~`"')

    def __init__(self) -> None:
        self.entropy_calc = EntropyCalculator()
        self.pattern_detector = PatternDetector()

    def analyze(self, password: str) -> dict[str, Any]:
        scores = self._calc_scores(password)
        penalty = self._calc_penalty(password)
        bonus = self._calc_bonus(password)
        raw = sum(scores.values()) + bonus - penalty
        total = max(0, min(100, raw))
        scores['bonus'] = bonus
        scores['penalty'] = penalty
        entropy = self.entropy_calc.calculate(password)
        patterns = self.pattern_detector.check_all(password)
        is_common = password.lower() in COMMON_PASSWORDS
        if is_common:
            total = min(total, 15)
        return {
            'total_score': total,
            'level': self._level(total),
            'scores': scores,
            'entropy': entropy,
            'patterns': patterns,
            'is_common': is_common,
            'recommendations': self._recommendations(password, scores, patterns, is_common, entropy)
        }

    def _calc_scores(self, password: str) -> dict[str, int]:
        scores: dict[str, int] = {}
        length = len(password)

        if length >= 20:
            scores['length'] = 25
        elif length >= 16:
            scores['length'] = 20
        elif length >= 12:
            scores['length'] = 15
        elif length >= 10:
            scores['length'] = 10
        elif length >= 8:
            scores['length'] = 5
        else:
            scores['length'] = max(0, length - 4)

        upper_count = sum(1 for c in password if c.isupper())
        lower_count = sum(1 for c in password if c.islower())
        digit_count = sum(1 for c in password if c.isdigit())
        special_count = sum(1 for c in password if c in self.SPECIAL_CHARS)

        scores['uppercase'] = min(10, upper_count * 3) if upper_count else 0
        scores['lowercase'] = min(10, lower_count * 2) if lower_count else 0
        scores['digits'] = min(10, digit_count * 3) if digit_count else 0
        scores['special'] = min(15, special_count * 4) if special_count else 0
        return scores

    def _calc_bonus(self, password: str) -> int:
        char_types = sum([
            any(c.isupper() for c in password),
            any(c.islower() for c in password),
            any(c.isdigit() for c in password),
            any(c in self.SPECIAL_CHARS for c in password),
        ])
        if char_types == 4:
            return 10
        if char_types == 3:
            return 5
        return 0

    def _calc_penalty(self, password: str) -> int:
        penalty = 0
        if re.search(r'(.)\1{2,}', password):
            penalty += 10
        if re.search(r'(012|123|234|345|456|567|678|789|987|876|765|654|543|432|321|210)', password):
            penalty += 5
        if re.search(
            r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)',
            password.lower()
        ):
            penalty += 5
        for walk in ['qwerty', 'asdfgh', 'zxcvbn', 'qazwsx']:
            if walk in password.lower():
                penalty += 10
        return penalty

    def _level(self, score: int) -> str:
        if score >= 80:
            return 'VERY STRONG'
        if score >= 60:
            return 'STRONG'
        if score >= 40:
            return 'MODERATE'
        if score >= 20:
            return 'WEAK'
        return 'VERY WEAK'

    def _recommendations(self, password: str, scores: dict, patterns: list,
                         is_common: bool, entropy: dict) -> list[str]:
        recs: list[str] = []
        if is_common:
            recs.append('This password is in common breach lists — change it immediately')
        if len(password) < 12:
            recs.append('Use at least 12 characters (16+ recommended)')
        if scores['uppercase'] == 0:
            recs.append('Add uppercase letters (A-Z)')
        if scores['lowercase'] == 0:
            recs.append('Add lowercase letters (a-z)')
        if scores['digits'] == 0:
            recs.append('Add numbers (0-9)')
        if scores['special'] == 0:
            recs.append('Add special characters (!@#$%^&*)')
        if entropy['bits'] < 50:
            recs.append('Increase complexity — entropy is too low (<50 bits)')
        for _, ok, msg in patterns:
            if not ok:
                recs.append(f'Avoid: {msg}')
        if not recs:
            recs.append('Great password! Store it securely in a password manager.')
        return recs[:5]
