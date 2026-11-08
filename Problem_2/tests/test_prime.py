"""Tests for Problem_2/app/prime_test.py (run with: python Problem_2/tests/test_prime.py)."""

import os
import subprocess
import sys
import unittest

# Folder paths, worked out from this file's location.
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROBLEM_DIR = os.path.dirname(TESTS_DIR)
REPO_ROOT = os.path.dirname(PROBLEM_DIR)
RESULTS_DIR = os.path.join(PROBLEM_DIR, "results")
SCRIPT = os.path.join(PROBLEM_DIR, "app", "prime_test.py")

# Import exactly the way Problem_3 will: from the repository root.
sys.path.insert(0, REPO_ROOT)
from Problem_2.app.prime_test import is_prime  # noqa: E402

USAGE = "Usage: python prime_test.py <n>"

PIAZZA = [
    (1000000000000037, True),
    (1000000000000223, True),
    (1000000000000001, False),
    (1000000000000005, False),
]


def run_script(*args):
    """Run the command-line script and return (output, return code)."""
    result = subprocess.run(
        [sys.executable, SCRIPT, *args], capture_output=True, text=True
    )
    return result.stdout + result.stderr, result.returncode


class TestSmallCases(unittest.TestCase):
    def test_not_prime(self):
        for n in [0, 1, 4, 25, 49, -7]:
            self.assertFalse(is_prime(n), n)

    def test_prime(self):
        for n in [2, 3, 29]:
            self.assertTrue(is_prime(n), n)

    def test_divisible_by_2_and_3(self):
        self.assertFalse(is_prime(100))
        self.assertFalse(is_prime(99))

    def test_limit_below_5(self):
        # floor(sqrt(n)) < 5 for n < 25, so the loop never runs.
        lst = []
        self.assertTrue(is_prime(23, tested=lst))
        self.assertEqual(lst, [])


class TestPiazza(unittest.TestCase):
    def test_piazza_numbers(self):
        os.makedirs(RESULTS_DIR, exist_ok=True)
        lines = []
        for n, expected in PIAZZA:
            actual = is_prime(n)
            lines.append(f"{n}\t{'Prime' if actual else 'Not prime'}")
            self.assertEqual(actual, expected, n)
        with open(os.path.join(RESULTS_DIR, "piazza_results.txt"), "w") as f:
            f.write("\n".join(lines) + "\n")


class TestTypeError(unittest.TestCase):
    def test_bad_types(self):
        for bad in ["7", 7.0, True, False]:
            with self.assertRaises(TypeError):
                is_prime(bad)


class TestTrace(unittest.TestCase):
    def test_divisors_are_1_or_5_mod_6_and_descending(self):
        for n in [127, 1009, 10007, 49, 1000003]:
            lst = []
            is_prime(n, tested=lst)
            self.assertTrue(len(lst) > 0, n)
            for d in lst:
                self.assertIn(d % 6, (1, 5), (n, d))
            self.assertEqual(lst, sorted(lst, reverse=True), n)
            self.assertEqual(len(lst), len(set(lst)), n)

    def test_last_divisor_is_5_for_primes(self):
        # Only for prime n with floor(sqrt(n)) >= 5.
        for n in [29, 127, 1009, 10007, 1000003]:
            lst = []
            self.assertTrue(is_prime(n, tested=lst))
            self.assertEqual(lst[-1], 5, n)

    def test_composite_stops_at_first_divisor(self):
        lst = []
        self.assertFalse(is_prime(49, tested=lst))
        self.assertEqual(lst, [7])

    def test_trace_127(self):
        lst = []
        self.assertTrue(is_prime(127, tested=lst))
        self.assertEqual(lst, [11, 7, 5])
        os.makedirs(RESULTS_DIR, exist_ok=True)
        with open(os.path.join(RESULTS_DIR, "trace_127.txt"), "w") as f:
            f.write("n = 127, floor(sqrt(127)) = 11\n")
            f.write("divisors tested, in order: " + ", ".join(map(str, lst)) + "\n")
            f.write("result: prime\n")


class TestCommandLine(unittest.TestCase):
    def test_valid(self):
        out, code = run_script("37")
        self.assertEqual(out.strip(), "37 is prime")
        out, code = run_script("36")
        self.assertEqual(out.strip(), "36 is not prime")

    def test_no_argument(self):
        out, code = run_script()
        self.assertEqual(out.strip(), USAGE)
        self.assertNotIn("Traceback", out)

    def test_two_arguments(self):
        out, code = run_script("7", "9")
        self.assertEqual(out.strip(), USAGE)
        self.assertNotIn("Traceback", out)

    def test_non_integer(self):
        out, code = run_script("abc")
        self.assertEqual(out.strip(), USAGE)
        self.assertNotIn("Traceback", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
