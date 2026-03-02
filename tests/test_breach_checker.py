"""Tests for the BreachChecker module."""
import pytest
from breach_checker import BreachChecker


class TestBreachChecker:
    def setup_method(self):
        self.checker = BreachChecker()

    # --- Known breached passwords ---

    def test_detects_password(self):
        result = self.checker.check('password')
        assert result['found'] is True

    def test_detects_123456(self):
        result = self.checker.check('123456')
        assert result['found'] is True

    def test_detects_qwerty(self):
        result = self.checker.check('qwerty')
        assert result['found'] is True

    # --- Non-breached passwords ---

    def test_unique_password_not_found(self):
        result = self.checker.check('X9$kL!mP2@qW7#nRvBzY')
        assert result['found'] is False

    def test_random_string_not_found(self):
        result = self.checker.check('j8K#mQ!pZ2$nR@wL5')
        assert result['found'] is False

    # --- Result structure ---

    def test_result_has_required_keys(self):
        result = self.checker.check('test')
        assert 'found' in result
        assert 'hash_prefix' in result
        assert 'model' in result
        assert 'note' in result

    def test_hash_prefix_is_5_chars(self):
        result = self.checker.check('anypassword')
        assert len(result['hash_prefix']) == 5

    def test_model_is_k_anonymity(self):
        result = self.checker.check('test')
        assert 'k-anonymity' in result['model']

    def test_note_contains_api_url(self):
        result = self.checker.check('test')
        assert 'pwnedpasswords.com' in result['note']

    # --- K-anonymity simulation ---

    def test_matches_returned_key_exists(self):
        result = self.checker.check('password')
        assert 'matches_returned' in result

    def test_matches_returned_is_non_negative(self):
        result = self.checker.check('password')
        assert result['matches_returned'] >= 0

    # --- Hash info ---

    def test_get_hash_info_structure(self):
        info = self.checker.get_hash_info('test')
        assert 'sha1_full' in info
        assert 'prefix_sent' in info
        assert 'suffix_kept_local' in info

    def test_hash_info_prefix_is_5_chars(self):
        info = self.checker.get_hash_info('test')
        assert len(info['prefix_sent']) == 5

    def test_hash_info_full_is_40_chars(self):
        info = self.checker.get_hash_info('test')
        assert len(info['sha1_full']) == 40

    def test_prefix_plus_suffix_equals_full(self):
        info = self.checker.get_hash_info('test')
        assert info['prefix_sent'] + info['suffix_kept_local'] == info['sha1_full']
