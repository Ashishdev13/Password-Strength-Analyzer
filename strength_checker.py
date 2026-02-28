#!/usr/bin/env python3
"""
Strength Checker Module - Core password strength analysis engine.
"""
import re, os
from entropy import EntropyCalculator
from pattern_detector import PatternDetector

COMMON_PASSWORDS_FILE = os.path.join(os.path.dirname(__file__), 'common_passwords.txt')

def load_common_passwords():
    try:
        with open(COMMON_PASSWORDS_FILE, 'r') as f:
            return set(line.strip().lower() for line in f if line.strip())
    except FileNotFoundError:
        return set()

COMMON_PASSWORDS = load_common_passwords()

class StrengthChecker:
    MAX_SCORE = 100
    SPECIAL_CHARS = set('!@#$%^&*()_+-=[]{}|;<>?,./~`"')

    def __init__(self):
        self.entropy_calc = EntropyCalculator()
        self.pattern_detector = PatternDetector()

    def analyze(self, password):
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

    def _calc_scores(self, p):
        s = {}
        n = len(p)
        s['length'] = 25 if n >= 20 else (20 if n >= 16 else (15 if n >= 12 else (10 if n >= 10 else (5 if n >= 8 else max(0, n-4)))))
        uc = sum(1 for c in p if c.isupper())
        lc = sum(1 for c in p if c.islower())
        dc = sum(1 for c in p if c.isdigit())
        sc = sum(1 for c in p if c in self.SPECIAL_CHARS)
        s['uppercase'] = min(10, uc * 3) if uc else 0
        s['lowercase'] = min(10, lc * 2) if lc else 0
        s['digits'] = min(10, dc * 3) if dc else 0
        s['special'] = min(15, sc * 4) if sc else 0
        return s

    def _calc_bonus(self, p):
        types = sum([any(c.isupper() for c in p), any(c.islower() for c in p),
                     any(c.isdigit() for c in p), any(c in self.SPECIAL_CHARS for c in p)])
        return 10 if types == 4 else (5 if types == 3 else 0)

    def _calc_penalty(self, p):
        pen = 0
        if re.search(r'(.)\1{2,}', p): pen += 10
        if re.search(r'(012|123|234|345|456|567|678|789)', p): pen += 5
        if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', p.lower()): pen += 5
        for w in ['qwerty','asdfgh','zxcvbn','qazwsx']:
            if w in p.lower(): pen += 10
        return pen

    def _level(self, score):
        if score >= 81: return 'VERY STRONG'
        if score >= 61: return 'STRONG'
        if score >= 41: return 'MODERATE'
        if score >= 21: return 'WEAK'
        return 'VERY WEAK'

    def _recommendations(self, p, scores, patterns, is_common, entropy):
        r = []
        if is_common: r.append('This password is in common breach lists — change it immediately')
        if len(p) < 12: r.append('Use at least 12 characters (16+ recommended)')
        if scores['uppercase'] == 0: r.append('Add uppercase letters (A-Z)')
        if scores['digits'] == 0: r.append('Add numbers (0-9)')
        if scores['special'] == 0: r.append('Add special characters (!@#$%^&*)')
        if entropy['bits'] < 50: r.append('Increase complexity — entropy is too low (<50 bits)')
        for _, ok, msg in patterns:
            if not ok: r.append(f'Avoid: {msg}')
        if not r: r.append('Great password! Store it securely in a password manager.')
        return r[:5]
