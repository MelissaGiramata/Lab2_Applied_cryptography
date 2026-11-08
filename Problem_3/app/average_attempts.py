"""Estimate how many random integers must be drawn from an interval
before one of them is prime (Problem 3).

Run from the repository root:
    python Problem_3/app/average_attempts.py
"""

import os
import random
import sys
import time

# Running a script puts the script's own folder (Problem_3/app) on the import
# path, not the repository root, so "Problem_2" could not be found. Work out
# the root from this file's location: file -> app -> Problem_3 -> root.
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROBLEM_DIR = os.path.dirname(APP_DIR)
REPO_ROOT = os.path.dirname(PROBLEM_DIR)
sys.path.insert(0, REPO_ROOT)

# Reuse Problem_2's primality test. It is imported, never re-written here.
from Problem_2.app.prime_test import is_prime  # noqa: E402

SEED = 42
RESULTS_FILE = os.path.join(PROBLEM_DIR, "results", "averages.txt")

# The two fixed experiments: (name, low, high, trials). Ends are inclusive.
EXPERIMENTS = [
    ("Experiment 1", 5_000_000, 6_000_000, 1000),
    ("Experiment 2", 500_000_000_000, 500_001_000_000, 250),
]


def count_until_prime(low, high, drawn=None):
    """Draw random integers from [low, high] until one is prime.

    Returns count: how many numbers were drawn, including the prime one.
    drawn: optional list. If passed, each drawn number is appended to it.
    """
    count = 0
    while True:
        # Draw a random integer (both ends included) and count it.
        number = random.randint(low, high)
        count += 1
        if drawn is not None:
            drawn.append(number)

        # Stop as soon as the number is prime; otherwise draw again.
        if is_prime(number):
            return count


def estimate_average(low, high, trials, counts=None):
    """Repeat count_until_prime `trials` times and return the average count.

    counts: optional list. If passed, each trial's count is appended to it.
    """
    total = 0
    for _ in range(trials):
        count = count_until_prime(low, high)
        total += count
        if counts is not None:
            counts.append(count)

    return total / trials


def main():
    """Run both experiments, print the results and save them to a file."""
    # Seed the random generator once, before Experiment 1. Experiment 2
    # continues the same random stream.
    random.seed(SEED)

    lines = [f"Random seed: {SEED}"]

    for name, low, high, trials in EXPERIMENTS:
        # Time only the estimation (not the printing or file writing).
        start = time.perf_counter()
        average = estimate_average(low, high, trials)
        elapsed = time.perf_counter() - start

        lines.append(
            f"{name}: interval {low:,} to {high:,}, trials {trials}, "
            f"average count {average:.2f}, runtime {elapsed:.2f} s"
        )

    # Print the results.
    for line in lines:
        print(line)

    # Save the same text; mode "w" replaces any old content.
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    with open(RESULTS_FILE, "w") as f:
        f.write("\n".join(lines) + "\n")


# Run main() only when the file is run as a script, not when it is imported.
if __name__ == "__main__":
    main()
