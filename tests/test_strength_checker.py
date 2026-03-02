"""Tests for the StrengthChecker module."""
import pytest
from strength_checker import StrengthChecker


class TestStrengthChecker:
    def setup_method(self):
        self.checker = StrengthChecker()

    # --- Score range tests ---

    def test_score_within_bounds(self, strong_password):
        result = self.checker.analyze(strong_password)
        assert 0 <= result['total_score'] <= 100

    def test_empty_password_score_zero(self):
        result = self.checker.analyze('')
        assert result['total_score'] == 0

    def test_very_strong_password(self):
        result = self.checker.analyze('X9$kL!mP28@qW7#nR!!vBzY')
        assert result['total_score'] >= 80
        assert result['level'] == 'VERY STRONG'

    def test_weak_password(self, weak_password):
        result = self.checker.analyze(weak_password)
        assert result['total_score'] <= 15  # common password cap
        assert result['level'] == 'VERY WEAK'

    # --- Level classification tests ---

    def test_level_very_weak(self):
        result = self.checker.analyze('ab')
        assert result['level'] == 'VERY WEAK'

    def test_level_moderate(self):
        result = self.checker.analyze('MyPass123')
        assert result['level'] in ('WEAK', 'MODERATE')

    # --- Length scoring ---

    def test_length_score_short(self):
        result = self.checker.analyze('abc')
        assert result['scores']['length'] == 0  # max(0, 3-4) = 0

    def test_length_score_8_chars(self):
        result = self.checker.analyze('abcdefgh')
        assert result['scores']['length'] == 5

    def test_length_score_12_chars(self):
        result = self.checker.analyze('abcdefghijkl')
        assert result['scores']['length'] == 15

    def test_length_score_20_plus(self):
        result = self.checker.analyze('a' * 20)
        assert result['scores']['length'] == 25

    # --- Character type scoring ---

    def test_uppercase_scoring(self):
        result = self.checker.analyze('ABCDEFGH')
        assert result['scores']['uppercase'] > 0
        assert result['scores']['lowercase'] == 0

    def test_lowercase_scoring(self):
        result = self.checker.analyze('abcdefgh')
        assert result['scores']['lowercase'] > 0
        assert result['scores']['uppercase'] == 0

    def test_digit_scoring(self):
        result = self.checker.analyze('12345678')
        assert result['scores']['digits'] > 0

    def test_special_char_scoring(self):
        result = self.checker.analyze('!@#$%^&*')
        assert result['scores']['special'] > 0

    # --- Bonus scoring ---

    def test_all_four_types_bonus(self):
        result = self.checker.analyze('Aa1!')
        assert result['scores']['bonus'] == 10

    def test_three_types_bonus(self):
        result = self.checker.analyze('Aa1')
        assert result['scores']['bonus'] == 5

    def test_two_types_no_bonus(self):
        result = self.checker.analyze('Aa')
        assert result['scores']['bonus'] == 0

    # --- Penalty scoring ---

    def test_repeated_chars_penalty(self):
        result = self.checker.analyze('aaa12345')
        assert result['scores']['penalty'] >= 10

    def test_sequential_numbers_penalty(self):
        result = self.checker.analyze('xx123yy')
        assert result['scores']['penalty'] >= 5

    def test_keyboard_walk_penalty(self):
        result = self.checker.analyze('myqwertypass')
        assert result['scores']['penalty'] >= 10

    # --- Common password detection ---

    def test_common_password_detected(self, common_password):
        result = self.checker.analyze(common_password)
        assert result['is_common'] is True
        assert result['total_score'] <= 15

    def test_uncommon_password_not_flagged(self):
        result = self.checker.analyze('X9$kL!mP2@qW7#nR')
        assert result['is_common'] is False

    # --- Recommendations ---

    def test_recommendations_for_weak_password(self):
        result = self.checker.analyze('abc')
        assert len(result['recommendations']) > 0

    def test_no_excess_recommendations(self):
        result = self.checker.analyze('a')
        assert len(result['recommendations']) <= 5

    def test_strong_password_congratulated(self):
        result = self.checker.analyze('X9$kL!mP2@qW7#nRvB')
        if result['total_score'] >= 81:
            recs = result['recommendations']
            assert any('Great' in r or 'password manager' in r for r in recs) or len(recs) == 0

    # --- Result structure ---

    def test_result_keys(self, strong_password):
        result = self.checker.analyze(strong_password)
        expected_keys = {'total_score', 'level', 'scores', 'entropy', 'patterns', 'is_common', 'recommendations'}
        assert set(result.keys()) == expected_keys

    def test_scores_keys(self, strong_password):
        result = self.checker.analyze(strong_password)
        expected = {'length', 'uppercase', 'lowercase', 'digits', 'special', 'bonus', 'penalty'}
        assert set(result['scores'].keys()) == expected
