"""Tests for Problem_4/app/prime_percentage.py
(run with: python Problem_4/tests/test_prime_percentage.py)."""

import os
import sys
import unittest

# Folder paths, worked out from this file's location.
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROBLEM_DIR = os.path.dirname(TESTS_DIR)
REPO_ROOT = os.path.dirname(PROBLEM_DIR)

# Import from the repository root, the same way the other problems' tests do.
sys.path.insert(0, REPO_ROOT)
from Problem_4.app.prime_percentage import record_percentages  # noqa: E402


def brute_force_count(n):
    """Count the primes up to n with simple trial division (test only)."""
    count = 0
    for number in range(2, n + 1):
        is_p = True
        d = 2
        while d * d <= number:
            if number % d == 0:
                is_p = False
                break
            d += 1
        if is_p:
            count += 1
    return count


class TestKnownCounts(unittest.TestCase):
    def test_real_run(self):
        # Runs the full 5,000,000 search, so this test is slow.
        records = record_percentages(5_000_000, 5_000)
        self.assertEqual(len(records), 1000)

        n, count, percentage = records[0]
        self.assertEqual((n, count), (5000, 669))
        self.assertAlmostEqual(percentage, 669 / 5000 * 100)

        n, count, percentage = records[-1]
        self.assertEqual((n, count), (5_000_000, 348_513))
        self.assertAlmostEqual(percentage, 348_513 / 5_000_000 * 100)


class TestSmallCase(unittest.TestCase):
    def test_limit_100_step_10(self):
        records = record_percentages(100, 10)
        self.assertEqual(len(records), 10)
        for n, count, percentage in records:
            self.assertEqual(count, brute_force_count(n), n)
            self.assertAlmostEqual(percentage, count / n * 100)
        self.assertEqual([r[0] for r in records], list(range(10, 101, 10)))


class TestInvalidParameters(unittest.TestCase):
    def test_step_below_5(self):
        for step in (4, 0):
            with self.assertRaises(ValueError) as context:
                record_percentages(100, step)
            self.assertIn("step", str(context.exception))

    def test_limit_not_a_multiple_of_step(self):
        for limit, step in ((105, 10), (100, 7)):
            with self.assertRaises(ValueError) as context:
                record_percentages(limit, step)
            self.assertIn("multiple", str(context.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
