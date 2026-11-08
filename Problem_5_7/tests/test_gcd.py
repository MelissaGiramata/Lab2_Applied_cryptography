"""Tests for Problem_5_7/app/gcd.py (run with: python Problem_5_7/tests/test_gcd.py)."""

import math
import os
import sys
import unittest

# Folder paths, worked out from this file's location.
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROBLEM_DIR = os.path.dirname(TESTS_DIR)
REPO_ROOT = os.path.dirname(PROBLEM_DIR)

# Import from the repository root, the same way the other problems' tests do.
sys.path.insert(0, REPO_ROOT)
from Problem_5_7.app.gcd import gcd  # noqa: E402


class TestGcdCases(unittest.TestCase):
    def test_part_1_cases(self):
        cases = [
            (12, 8, 4),
            (8, 12, 4),
            (17, 5, 1),
            (100, 75, 25),
            (7, 7, 7),
            (1, 1, 1),
            (1071, 462, 21),
            # Two consecutive Fibonacci numbers: the slowest case for the
            # Euclidean algorithm (about 88 steps).
            (2880067194370816120, 1779979416004714189, 1),
        ]
        for a, b, expected in cases:
            self.assertEqual(gcd(a, b), expected, (a, b))

    def test_zero(self):
        self.assertEqual(gcd(5, 0), 5)
        self.assertEqual(gcd(0, 0), 0)


class TestGcdErrors(unittest.TestCase):
    def test_type_error(self):
        for bad in ["7", 7.0, True, False]:
            with self.assertRaises(TypeError):
                gcd(bad, 5)
            with self.assertRaises(TypeError):
                gcd(5, bad)

    def test_negative_is_value_error(self):
        with self.assertRaises(ValueError):
            gcd(-4, 6)
        with self.assertRaises(ValueError):
            gcd(4, -6)


class TestAgainstMathGcd(unittest.TestCase):
    def test_every_pair_0_to_40(self):
        # math.gcd is used here only, as an independent check.
        for a in range(0, 41):
            for b in range(0, 41):
                self.assertEqual(gcd(a, b), math.gcd(a, b), (a, b))


if __name__ == "__main__":
    unittest.main(verbosity=2)
