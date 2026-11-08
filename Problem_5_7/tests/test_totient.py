"""Tests for Problem_5_7/app/totient.py (run with: python Problem_5_7/tests/test_totient.py)."""

import os
import sys
import unittest

# Folder paths, worked out from this file's location.
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROBLEM_DIR = os.path.dirname(TESTS_DIR)
REPO_ROOT = os.path.dirname(PROBLEM_DIR)

# Import from the repository root, the same way the other problems' tests do.
sys.path.insert(0, REPO_ROOT)
from Problem_5_7.app.totient import euler_totient  # noqa: E402


class TestTotientCases(unittest.TestCase):
    def test_part_2_cases(self):
        cases = {1: 1, 2: 1, 7: 6, 9: 6, 10: 4, 12: 4, 15: 8, 100: 40}
        for n, expected in cases.items():
            self.assertEqual(euler_totient(n), expected, n)


class TestTotientErrors(unittest.TestCase):
    def test_type_error(self):
        for bad in ["7", 7.0, True, False]:
            with self.assertRaises(TypeError):
                euler_totient(bad)

    def test_value_error(self):
        for bad in [0, -5]:
            with self.assertRaises(ValueError):
                euler_totient(bad)


if __name__ == "__main__":
    unittest.main(verbosity=2)
