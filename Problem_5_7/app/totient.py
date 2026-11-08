"""Euler totient built on the non-recursive gcd (Problem 6)."""

# The repository root must already be on sys.path (the run script and the
# test files make sure of that).
from Problem_5_7.app.gcd import gcd


def euler_totient(n):
    """Return phi(n): how many integers from 1 to n - 1 have gcd 1 with n.

    phi(1) is 1 by the standard convention.
    Raises TypeError if n is not an int (or is a bool), ValueError if n < 1.
    """
    # Check the input. bool is a kind of int in Python, so reject it too.
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int (not bool)")
    if n < 1:
        raise ValueError(f"n must be at least 1, got {n}")

    # Step 1: special case. Taken literally "integers less than 1" would
    # give 0, but the standard convention is phi(1) = 1.
    if n == 1:
        return 1

    # Steps 2-4: count the integers from 1 to n - 1 that share no factor
    # with n (their gcd with n is 1).
    count = 0
    for i in range(1, n):
        if gcd(i, n) == 1:
            count += 1
    return count
