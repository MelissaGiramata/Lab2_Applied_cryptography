"""Tests for Problem_5_7/app/product_of_primes.py
(run with: python Problem_5_7/tests/test_product_of_primes.py).

This file stays fast: it never computes the totient of a product of primes
from 2000 to 3000. Those pairs run only in the main program.
"""

import os
import sys
import unittest

# Folder paths, worked out from this file's location.
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROBLEM_DIR = os.path.dirname(TESTS_DIR)
REPO_ROOT = os.path.dirname(PROBLEM_DIR)

# Import from the repository root, the same way the other problems' tests do.
sys.path.insert(0, REPO_ROOT)
from Problem_5_7.app.product_of_primes import (  # noqa: E402
    choose_pairs,
    compare_pair,
    find_primes,
)


class TestComparisonLogic(unittest.TestCase):
    def test_small_primes_5_and_7(self):
        product, totient, formula, equal, runtime = compare_pair(5, 7)
        self.assertEqual(product, 35)
        self.assertEqual(totient, 24)
        self.assertEqual(formula, 24)
        self.assertTrue(equal)
        self.assertGreaterEqual(runtime, 0)

    def test_same_prime_twice_with_5(self):
        product, totient, formula, equal, runtime = compare_pair(5, 5)
        self.assertEqual(product, 25)
        self.assertEqual(totient, 20)
        self.assertEqual(totient, 5 * 4)      # p * (p - 1)
        self.assertEqual(formula, 16)         # (p - 1) * (p - 1)
        self.assertFalse(equal)


class TestPrimesAndPairs(unittest.TestCase):
    def test_primes_between_2000_and_3000(self):
        primes = find_primes(2000, 3000)
        self.assertEqual(len(primes), 127)
        self.assertEqual(primes[0], 2003)
        self.assertEqual(primes[-1], 2999)

    def test_pair_choice_by_position(self):
        primes = find_primes(2000, 3000)
        mid = len(primes) // 2
        pairs = choose_pairs(primes)
        self.assertEqual(
            pairs,
            [
                (primes[0], primes[1]),
                (primes[0], primes[-1]),
                (primes[1], primes[2]),
                (primes[-2], primes[-1]),
                (primes[mid], primes[mid + 1]),
            ],
        )
        # The first three are the pairs from the requirements' examples.
        self.assertEqual(pairs[0], (2003, 2011))
        self.assertEqual(pairs[1], (2003, 2999))
        self.assertEqual(pairs[2], (2011, 2017))
        # Every pair has two different primes.
        for p, q in pairs:
            self.assertNotEqual(p, q)


if __name__ == "__main__":
    unittest.main(verbosity=2)
