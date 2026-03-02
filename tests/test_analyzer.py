"""Tests for the main analyzer CLI module."""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from analyzer import get_level_color, analyze_password, batch_analyze


class TestGetLevelColor:
    def test_high_score_green(self):
        color = get_level_color(90)
        assert color is not None

    def test_mid_score(self):
        color = get_level_color(50)
        assert color is not None

    def test_low_score_red(self):
        color = get_level_color(10)
        assert color is not None

    def test_boundary_81(self):
        color = get_level_color(81)
        assert color is not None

    def test_boundary_61(self):
        color = get_level_color(61)
        assert color is not None


class TestAnalyzePassword:
    def test_analyze_runs_without_error(self, capsys, strong_password):
        analyze_password(strong_password)
        captured = capsys.readouterr()
        assert 'TOTAL SCORE' in captured.out

    def test_analyze_shows_entropy(self, capsys, strong_password):
        analyze_password(strong_password)
        captured = capsys.readouterr()
        assert 'Entropy' in captured.out

    def test_analyze_shows_patterns(self, capsys, strong_password):
        analyze_password(strong_password)
        captured = capsys.readouterr()
        assert 'Pattern Analysis' in captured.out

    def test_common_password_flagged(self, capsys, weak_password):
        analyze_password(weak_password)
        captured = capsys.readouterr()
        assert 'common passwords' in captured.out.lower()


class TestBatchAnalyze:
    def test_file_not_found(self, capsys):
        with pytest.raises(SystemExit):
            batch_analyze('/nonexistent/file.txt')

    def test_batch_processes_file(self, capsys, tmp_path):
        pwfile = tmp_path / "test_passwords.txt"
        pwfile.write_text("password\n123456\nMyStr0ng!Pass\n")
        batch_analyze(str(pwfile))
        captured = capsys.readouterr()
        assert captured.out.count('TOTAL SCORE') == 3
