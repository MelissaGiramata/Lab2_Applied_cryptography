"""Tests for Problem_3/app/average_attempts.py
(run with: python Problem_3/tests/test_average_attempts.py)."""

import os
import random
import sys
import unittest

# Folder paths, worked out from this file's location.
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROBLEM_DIR = os.path.dirname(TESTS_DIR)
REPO_ROOT = os.path.dirname(PROBLEM_DIR)

# Import from the repository root, the same way Problem_2's tests do.
sys.path.insert(0, REPO_ROOT)
from Problem_2.app import prime_test  # noqa: E402
from Problem_3.app import average_attempts  # noqa: E402
from Problem_3.app.average_attempts import (  # noqa: E402
    count_until_prime,
    estimate_average,
)


class TestCounts(unittest.TestCase):
    def test_every_count_is_at_least_1(self):
        random.seed(1)
        counts = []
        estimate_average(100, 200, 50, counts=counts)
        self.assertEqual(len(counts), 50)
        for c in counts:
            self.assertGreaterEqual(c, 1)


class TestInterval(unittest.TestCase):
    def test_draws_stay_inside_and_both_ends_are_used(self):
        # 8, 9, 10 are not prime and 11 is, so many draws from [8, 11]
        # include both ends.
        random.seed(1)
        drawn = []
        for _ in range(200):
            count_until_prime(8, 11, drawn=drawn)
        for number in drawn:
            self.assertGreaterEqual(number, 8)
            self.assertLessEqual(number, 11)
        self.assertIn(8, drawn)
        self.assertIn(11, drawn)


class TestSeed(unittest.TestCase):
    def test_same_seed_gives_same_average(self):
        random.seed(42)
        first = estimate_average(100, 200, 30)
        random.seed(42)
        second = estimate_average(100, 200, 30)
        self.assertEqual(first, second)


class TestIsPrimeReuse(unittest.TestCase):
    def test_is_prime_is_the_one_from_problem_2(self):
        self.assertIs(average_attempts.is_prime, prime_test.is_prime)

    def test_no_second_primality_test_in_the_program(self):
        with open(average_attempts.__file__) as f:
            source = f.read()
        self.assertNotIn("def is_prime", source)


class TestKnownAnswer(unittest.TestCase):
    def test_interval_7_to_7(self):
        # 7 is the only possible number and it is prime.
        counts = []
        average = estimate_average(7, 7, 10, counts=counts)
        self.assertEqual(counts, [1] * 10)
        self.assertEqual(f"{average:.2f}", "1.00")


if __name__ == "__main__":
    unittest.main(verbosity=2)
