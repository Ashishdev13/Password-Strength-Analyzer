"""Shared fixtures for Password-Strength-Analyzer tests."""
import sys
import os
import pytest

# Add project root to path so modules can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def strong_password():
    return 'C0mpl3x!P@ss#2024'


@pytest.fixture
def weak_password():
    return 'password'


@pytest.fixture
def empty_password():
    return ''


@pytest.fixture
def short_password():
    return 'Ab1!'


@pytest.fixture
def common_password():
    return 'qwerty'
