#!/usr/bin/env python3
"""
Breach Checker - Simulates the HIBP (Have I Been Pwned) k-anonymity model.

HOW THE REAL HIBP API WORKS:
  1. Hash the password with SHA-1
  2. Take the first 5 characters of the hex hash
  3. Send ONLY those 5 chars to the API
  4. The API returns all hashes starting with those 5 chars
  5. Check if your full hash is in the returned list
  => The actual password is NEVER sent over the network

This module simulates that process locally for educational purposes.
"""
import hashlib

# Simulated breach database - SHA-1 hashes of extremely common passwords
# In a real implementation, this would query https://api.pwnedpasswords.com/range/{prefix}
SIMULATED_BREACH_HASHES = {
    '5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8',  # password
    'B1B3773A05C0ED0176787A4F1574FF0075F7521E',  # qwerty
    '7C4A8D09CA3762AF61E59520943DC26494F8941B',  # 123456
    'F7C3BC1D808E04732ADF679965CCC34CA7AE3441',  # 1234567890
    '3D4F2BF07DC1BE38B20CD6E46949A1071F9D0E3D',  # iloveyou
    '5031F43C29C40B22B26F04DB2A2F68B1C5D7EA50',  # abc123
    'C32511D1C33449B98CE6D8D8B01B8E0E7EA21234',  # password123
    '8CB2237D0679CA88DB6464EAC60DA96345513964',  # 12345
    'D0BEAB4F380DCADDEDFD5F58A397BAD47D8A3C52',  # monkey
    'A94A8FE5CCB19BA61C4C0873D391E987982FBBD3',  # test
}

class BreachChecker:
    """Simulates k-anonymity breach checking."""

    def check(self, password: str) -> dict:
        """
        Check if a password appears in the simulated breach database.
        Uses the k-anonymity model: only SHA-1 prefix is compared.
        """
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]

        # Simulate querying the API: get all hashes with same prefix
        matching_hashes = {h for h in SIMULATED_BREACH_HASHES if h.startswith(prefix)}

        found = sha1_hash in SIMULATED_BREACH_HASHES
        return {
            'found': found,
            'hash_prefix': prefix,
            'model': 'k-anonymity (simulated)',
            'note': 'Real check: https://api.pwnedpasswords.com/range/' + prefix
        }

    def get_hash_info(self, password: str) -> dict:
        """Return hash details for educational display."""
        sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
        return {
            'sha1_full': sha1,
            'prefix_sent': sha1[:5],
            'suffix_kept_local': sha1[5:]
        }
