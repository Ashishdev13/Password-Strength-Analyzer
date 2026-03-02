"""Tests for the EntropyCalculator module."""
import pytest
from entropy import EntropyCalculator


class TestEntropyCalculator:
    def setup_method(self):
        self.calc = EntropyCalculator()

    # --- Pool size tests ---

    def test_lowercase_pool(self):
        result = self.calc.calculate('abcdef')
        assert result['pool_size'] == 26

    def test_uppercase_pool(self):
        result = self.calc.calculate('ABCDEF')
        assert result['pool_size'] == 26

    def test_mixed_case_pool(self):
        result = self.calc.calculate('AbCdEf')
        assert result['pool_size'] == 52

    def test_alphanumeric_pool(self):
        result = self.calc.calculate('Abc123')
        assert result['pool_size'] == 62

    def test_full_pool_with_special(self):
        result = self.calc.calculate('Abc1!')
        assert result['pool_size'] == 94  # 26+26+10+32

    def test_unicode_extends_pool(self):
        result = self.calc.calculate('hello\u00e9')
        assert result['pool_size'] > 26  # includes 128 for unicode

    # --- Entropy bits tests ---

    def test_empty_password_zero_entropy(self):
        result = self.calc.calculate('')
        assert result['bits'] == 0.0

    def test_longer_password_more_entropy(self):
        short = self.calc.calculate('abc')
        long = self.calc.calculate('abcdefghijklm')
        assert long['bits'] > short['bits']

    def test_more_char_types_more_entropy(self):
        simple = self.calc.calculate('abcdefgh')
        complex_ = self.calc.calculate('AbCd12!@')
        assert complex_['bits'] > simple['bits']

    def test_entropy_positive_for_nonempty(self):
        result = self.calc.calculate('a')
        assert result['bits'] > 0

    # --- Rating tests ---

    def test_rating_very_weak(self):
        result = self.calc.calculate('abc')
        assert 'Weak' in result['rating'] or 'Very Weak' in result['rating']

    def test_rating_excellent(self):
        result = self.calc.calculate('X9$kL!mP2@qW7#nRvBzY')
        assert 'Excellent' in result['rating'] or 'Strong' in result['rating']

    def test_rating_none_for_empty(self):
        result = self.calc.calculate('')
        assert result['rating'] == 'None'
