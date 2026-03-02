"""Tests for the PatternDetector module."""
import pytest
from pattern_detector import PatternDetector


class TestPatternDetector:
    def setup_method(self):
        self.detector = PatternDetector()

    def _get_result(self, password, check_name):
        results = self.detector.check_all(password)
        for name, passed, msg in results:
            if name == check_name:
                return passed
        return None

    # --- Keyboard walk detection ---

    def test_detects_qwerty(self):
        assert self._get_result('myqwertypass', 'keyboard_walk') is False

    def test_detects_asdfgh(self):
        assert self._get_result('asdfgh123', 'keyboard_walk') is False

    def test_no_keyboard_walk(self):
        assert self._get_result('X9$kL!mP', 'keyboard_walk') is True

    def test_detects_iloveyou(self):
        assert self._get_result('iloveyou99', 'keyboard_walk') is False

    # --- Repeated characters ---

    def test_detects_repeated_chars(self):
        assert self._get_result('aaa12345', 'repeated_chars') is False

    def test_no_repeated_chars(self):
        assert self._get_result('abcdef', 'repeated_chars') is True

    def test_two_repeated_ok(self):
        assert self._get_result('aabbc', 'repeated_chars') is True

    # --- Sequential numbers ---

    def test_detects_sequential_nums(self):
        assert self._get_result('abc1234xyz', 'sequential_nums') is False

    def test_detects_reverse_sequential(self):
        assert self._get_result('abc9876xyz', 'sequential_nums') is False

    def test_no_sequential_nums(self):
        assert self._get_result('a1b3c7d9', 'sequential_nums') is True

    # --- Sequential alpha ---

    def test_detects_sequential_alpha(self):
        assert self._get_result('xxabcdyy', 'sequential_alpha') is False

    def test_no_sequential_alpha(self):
        assert self._get_result('xbmqz', 'sequential_alpha') is True

    def test_case_insensitive_sequential(self):
        assert self._get_result('ABCD1234', 'sequential_alpha') is False

    # --- Date patterns ---

    def test_detects_year_pattern(self):
        assert self._get_result('pass2024word', 'date_pattern') is False

    def test_detects_date_mmdd(self):
        assert self._get_result('pass0125word', 'date_pattern') is False

    def test_no_date_pattern(self):
        assert self._get_result('X9$kL!mP', 'date_pattern') is True

    # --- Same case detection ---

    def test_all_lowercase_flagged(self):
        assert self._get_result('abcdefgh', 'all_same_case') is False

    def test_all_uppercase_flagged(self):
        assert self._get_result('ABCDEFGH', 'all_same_case') is False

    def test_mixed_case_ok(self):
        assert self._get_result('AbCdEfGh', 'all_same_case') is True

    def test_no_letters_ok(self):
        assert self._get_result('12345!@#', 'all_same_case') is True

    # --- General ---

    def test_check_all_returns_six_checks(self):
        results = self.detector.check_all('testpassword')
        assert len(results) == 6

    def test_check_all_tuple_structure(self):
        results = self.detector.check_all('testpassword')
        for name, passed, msg in results:
            assert isinstance(name, str)
            assert isinstance(passed, bool)
            assert isinstance(msg, str)
