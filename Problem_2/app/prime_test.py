"""Primality test using the descending 6k+1 / 6k-1 search (Problem 2)."""

import math
import sys


def is_prime(n, tested=None):
    """Return True if n is prime, False otherwise.

    tested: optional list. If a list is passed, every divisor the main loop
    tests is appended to it, in order (used by the trace tests). Normal calls
    do not pass it.
    """
    # Step 1: only real ints are allowed. bool is a kind of int in Python,
    # so it has to be rejected separately.
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int (not a bool)")

    # Step 2: numbers below 2 (0, 1, negatives) are not prime.
    if n < 2:
        return False

    # Step 3: 2 and 3 are prime.
    if n == 2 or n == 3:
        return True

    # Step 4: any other multiple of 2 or 3 is not prime.
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Step 5: the floor of the square root, using integer arithmetic.
    # If it is below 5 there is nothing left to test.
    limit = math.isqrt(n)
    if limit < 5:
        return True

    # Step 6: start at the largest number <= limit that leaves remainder
    # 1 or 5 when divided by 6.
    remainder = limit % 6
    if remainder == 0 or remainder == 2:
        i = limit - 1
    elif remainder == 3:
        i = limit - 2
    elif remainder == 4:
        i = limit - 3
    else:  # remainder is 1 or 5: limit itself already fits
        i = limit

    # Step 7: go downwards, one divisor at a time (no list of candidates is
    # ever built), and stop as soon as a divisor is found.
    while i >= 5:
        # Record the divisor if the caller asked for a trace.
        if tested is not None:
            tested.append(i)

        # A divisor was found, so n is not prime.
        if n % i == 0:
            return False

        # Move to the next candidate: 6k+1 -> 6k-1 is a step of 2,
        # 6k-1 -> 6(k-1)+1 is a step of 4.
        if i % 6 == 1:
            i -= 2
        else:
            i -= 4

    # Step 8: no divisor was found, so n is prime.
    return True


def main():
    """Read n from the command line and print whether it is prime."""
    usage = "Usage: python prime_test.py <n>"

    # Exactly one argument is required (sys.argv[0] is the script name).
    if len(sys.argv) != 2:
        print(usage)
        sys.exit(1)

    # The argument must be an integer.
    try:
        n = int(sys.argv[1])
    except ValueError:
        print(usage)
        sys.exit(1)

    if is_prime(n):
        print(f"{n} is prime")
    else:
        print(f"{n} is not prime")


# Run main() only when the file is run as a script, not when it is imported.
if __name__ == "__main__":
    main()
