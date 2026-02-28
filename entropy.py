#!/usr/bin/env python3
import math

class EntropyCalculator:
    def calculate(self, password):
        pool_size = self._get_pool_size(password)
        length = len(password)
        if pool_size == 0 or length == 0:
            return {'bits': 0.0, 'pool_size': 0, 'rating': 'None'}
        bits = length * math.log2(pool_size)
        return {'bits': round(bits, 2), 'pool_size': pool_size, 'rating': self._rating(bits)}

    def _get_pool_size(self, password):
        pool = 0
        if any(c.islower() for c in password): pool += 26
        if any(c.isupper() for c in password): pool += 26
        if any(c.isdigit() for c in password): pool += 10
        if any(not c.isalnum() for c in password): pool += 32
        if any(ord(c) > 127 for c in password): pool += 128
        return pool

    def _rating(self, bits):
        if bits >= 128: return 'Excellent (>=128 bits)'
        if bits >= 80:  return 'Strong (80-127 bits)'
        if bits >= 60:  return 'Good (60-79 bits)'
        if bits >= 40:  return 'Fair (40-59 bits)'
        if bits >= 28:  return 'Weak (28-39 bits)'
        return 'Very Weak (<28 bits)'
