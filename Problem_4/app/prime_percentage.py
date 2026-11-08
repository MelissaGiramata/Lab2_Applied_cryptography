"""Graph the percentage of integers up to N that are prime (Problem 4).

Every number of the form 6k-1 and 6k+1 is tested once, in a single pass, with
a running count of primes.

Run from the repository root:
    python Problem_4/app/prime_percentage.py
"""

import math
import os
import sys

import matplotlib

# Use the "Agg" backend (draws into a file only) so no window ever opens.
# This must be done before pyplot is imported.
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# Running a script puts the script's own folder (Problem_4/app) on the import
# path, not the repository root. Work out the root from this file's location:
# file -> app -> Problem_4 -> root.
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROBLEM_DIR = os.path.dirname(APP_DIR)
REPO_ROOT = os.path.dirname(PROBLEM_DIR)
sys.path.insert(0, REPO_ROOT)

# Reuse Problem_2's primality test. It is imported, never re-written here.
from Problem_2.app.prime_test import is_prime  # noqa: E402

LIMIT = 5_000_000
STEP = 5_000
RESULTS_DIR = os.path.join(PROBLEM_DIR, "results")
PNG_FILE = os.path.join(RESULTS_DIR, "prime_percentage.png")
TEXT_FILE = os.path.join(RESULTS_DIR, "prime_percentages.txt")


def record_percentages(limit, step):
    """Test every 6k-1 and 6k+1 up to limit once, recording the prime count
    at each sample point (step, 2*step, ..., limit).

    Returns a list of (sample_point, prime_count, percentage) tuples.
    """
    # Check the assumptions before doing any work. The step check comes first
    # so that step = 0 never causes a division by zero below.
    if step < 5:
        raise ValueError(f"step must be at least 5, got {step}")
    if limit % step != 0:
        raise ValueError(
            f"limit must be a multiple of step, got limit={limit} and step={step}"
        )

    records = []

    # Step 1: 2 and 3 are prime but not of the form 6k-1 or 6k+1.
    prime_count = 2

    # Step 2: the first sample point.
    next_sample = step

    # Step 3: k = 1, 2, 3, ... while 6k-1 is within the limit.
    k = 1
    while 6 * k - 1 <= limit:
        for candidate in (6 * k - 1, 6 * k + 1):
            # Skip a candidate above the limit (only 6k+1 can be).
            if candidate > limit:
                continue

            # 3a-i: the candidate is past the sample point, so every number up
            # to the sample point has been counted. Record it and move on.
            # Repeat in case the candidate jumped past several sample points.
            while candidate > next_sample:
                percentage = prime_count / next_sample * 100
                records.append((next_sample, prime_count, percentage))
                next_sample += step

            # 3a-ii: test the candidate once and keep the running count.
            if is_prime(candidate):
                prime_count += 1

        k += 1

    # Step 4: record the sample points no candidate got past (including the
    # limit itself), using the final count.
    while next_sample <= limit:
        percentage = prime_count / next_sample * 100
        records.append((next_sample, prime_count, percentage))
        next_sample += step

    return records


def summary_lines(records):
    """Return two lines: the percentage at the first and last sample points."""
    lines = []
    for sample_point, _count, percentage in (records[0], records[-1]):
        lines.append(f"N = {sample_point:,}: {percentage:.2f}%")
    return lines


def draw_graph(records, filename):
    """Draw the measured percentage and 100 / ln(N), and save it to filename."""
    sample_points = [r[0] for r in records]
    measured = [r[2] for r in records]
    expected = [100 / math.log(n) for n in sample_points]

    plt.figure(figsize=(10, 6))
    plt.plot(sample_points, measured, "-", label="Measured percentage of primes up to N")
    plt.plot(sample_points, expected, "--", label="100 / ln(N)")
    plt.title("Percentage of integers up to N that are prime")
    plt.xlabel("N")
    plt.ylabel("Percentage that are prime (%)")
    plt.legend()
    plt.grid(True)

    plt.savefig(filename, dpi=150)
    plt.close()


def main():
    """Run the real experiment, print and save the lines, and save the graph."""
    records = record_percentages(LIMIT, STEP)

    lines = summary_lines(records)
    for line in lines:
        print(line)

    # Mode "w" replaces any old content.
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(TEXT_FILE, "w") as f:
        f.write("\n".join(lines) + "\n")

    draw_graph(records, PNG_FILE)


# Run main() only when the file is run as a script, not when it is imported.
if __name__ == "__main__":
    main()
