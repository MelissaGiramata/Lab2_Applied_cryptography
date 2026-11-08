"""Compare euler_totient(p*q) with (p-1)*(q-1) for primes p, q (Problem 7).

Run from the repository root:
    python Problem_5_7/app/product_of_primes.py
"""

import os
import sys
import time

# Running a script puts the script's own folder (Problem_5_7/app) on the
# import path, not the repository root. Work out the root from this file's
# location: file -> app -> Problem_5_7 -> root.
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROBLEM_DIR = os.path.dirname(APP_DIR)
REPO_ROOT = os.path.dirname(PROBLEM_DIR)
sys.path.insert(0, REPO_ROOT)

# Reuse Problem_2's primality test (imported, never re-written here) and the
# euler_totient from Problem 6.
from Problem_2.app.prime_test import is_prime  # noqa: E402
from Problem_5_7.app.totient import euler_totient  # noqa: E402

RESULTS_FILE = os.path.join(PROBLEM_DIR, "results", "totient_results.txt")


def find_primes(low, high):
    """Return the primes from low to high (both included), in increasing order."""
    primes = []
    for number in range(low, high + 1):
        if is_prime(number):
            primes.append(number)
    return primes


def choose_pairs(primes):
    """Choose the five (p, q) pairs by position in the list of primes."""
    mid = len(primes) // 2
    return [
        (primes[0], primes[1]),        # the smallest pair
        (primes[0], primes[-1]),       # a pair with the largest prime
        (primes[1], primes[2]),
        (primes[-2], primes[-1]),      # the two largest primes
        (primes[mid], primes[mid + 1]),  # a pair from the middle
    ]


def compare_pair(p, q):
    """Compare euler_totient(p*q) with (p-1)*(q-1).

    Works for any p and q. Returns (product, totient, formula, equal, runtime),
    where runtime is the seconds taken by the euler_totient call only.
    """
    product = p * q

    # Time only the totient computation.
    start = time.perf_counter()
    totient = euler_totient(product)
    runtime = time.perf_counter() - start

    formula = (p - 1) * (q - 1)
    equal = (totient == formula)
    return product, totient, formula, equal, runtime


def format_pair(label, p, q, result):
    """Return one line of text for a pair."""
    product, totient, formula, equal, runtime = result
    return (
        f"{label}: p={p}, q={q}, p*q={product}, euler_totient={totient}, "
        f"(p-1)*(q-1)={formula}, equal: {'yes' if equal else 'no'}, "
        f"runtime {runtime:.2f} s"
    )


def main():
    """Run the five pairs and the p = q check, print and save the output."""
    primes = find_primes(2000, 3000)
    pairs = choose_pairs(primes)

    lines = []
    all_equal = True

    # One line per pair.
    for number, (p, q) in enumerate(pairs, start=1):
        result = compare_pair(p, q)
        lines.append(format_pair(f"Pair {number}", p, q, result))
        if not result[3]:
            all_equal = False

    # The summary line.
    if all_equal:
        lines.append(
            f"Summary: (p-1)*(q-1) matched euler_totient(p*q) for all {len(pairs)} pairs."
        )
    else:
        lines.append(
            "Summary: (p-1)*(q-1) did NOT match euler_totient(p*q) for every pair."
        )

    # The p = q check: with the same prime twice, the totient is p*(p-1),
    # not (p-1)*(p-1), so the formula does not hold.
    p = primes[0]
    product, totient, formula, equal, runtime = compare_pair(p, p)
    lines.append(
        f"Same prime twice: p=q={p}, p*p={product}, euler_totient={totient}, "
        f"p*(p-1)={p * (p - 1)}, (p-1)*(p-1)={formula}, "
        f"equal: {'yes' if equal else 'no'}, runtime {runtime:.2f} s"
    )

    # Print the output.
    for line in lines:
        print(line)

    # Save the same text; mode "w" replaces any old content.
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    with open(RESULTS_FILE, "w") as f:
        f.write("\n".join(lines) + "\n")


# Run main() only when the file is run as a script, not when it is imported.
if __name__ == "__main__":
    main()
