#!/usr/bin/env python3
import re

class PatternDetector:
    KEYBOARD_WALKS = ['qwerty','qwertyuiop','asdfgh','asdfghjkl','zxcvbn','zxcvbnm',
                      'qazwsx','1qaz2wsx','password','letmein','iloveyou']
    DATE_PATTERN = re.compile(r'(19|20)\d{2}|(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])')
    REPEAT_PATTERN = re.compile(r'(.)\1{2,}')
    SEQ_NUM = re.compile(r'(0123|1234|2345|3456|4567|5678|6789|9876|8765|7654|6543|5432|4321|3210)')
    SEQ_ALPHA = re.compile(r'(abcd|bcde|cdef|defg|efgh|fghi|ghij|hijk|ijkl|jklm|klmn|lmno|mnop|nopq|opqr|pqrs|qrst|rstu|stuv|tuvw|uvwx|vwxy|wxyz)', re.IGNORECASE)

    def check_all(self, password):
        results = []
        results.append(('keyboard_walk', not self._has_keyboard_walk(password), 'No keyboard walk pattern (qwerty, asdf...)'))
        results.append(('repeated_chars', not bool(self.REPEAT_PATTERN.search(password)), 'No repeated characters (aaa, 111...)'))
        results.append(('sequential_nums', not bool(self.SEQ_NUM.search(password)), 'No sequential numbers (1234, 5678...)'))
        results.append(('sequential_alpha', not bool(self.SEQ_ALPHA.search(password)), 'No sequential letters (abcd, efgh...)'))
        results.append(('date_pattern', not bool(self.DATE_PATTERN.search(password)), 'No obvious date patterns (2024, 0101...)'))
        results.append(('all_same_case', not self._all_same_case(password), 'Mixed character cases used'))
        return results

    def _has_keyboard_walk(self, password):
        p = password.lower()
        return any(walk in p for walk in self.KEYBOARD_WALKS)

    def _all_same_case(self, password):
        letters = [c for c in password if c.isalpha()]
        if not letters: return False
        return all(c.isupper() for c in letters) or all(c.islower() for c in letters)
