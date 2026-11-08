"""Non-recursive greatest common divisor (Problem 5)."""


def gcd(a, b):
    """Return the greatest common divisor of a and b (both >= 0).

    Uses the Euclidean algorithm with a loop (no recursion).
    Raises TypeError if a or b is not an int (or is a bool),
    and ValueError if a or b is negative.
    """
    # Check the types first. bool is a kind of int in Python, so it has to be
    # rejected separately.
    for value in (a, b):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("a and b must be int (not bool)")

    # Then check the values.
    if a < 0 or b < 0:
        raise ValueError(f"a and b must not be negative, got a={a} and b={b}")

    # Repeat until the remainder is 0.
    while b != 0:
        # Python works out the whole right-hand side with the OLD a and b
        # first, and only then assigns both. So the new a is the old b, and
        # the new b is the old a divided by the old b (remainder).
        a, b = b, a % b

    # The last non-zero value is the gcd. If b was 0 from the start, this
    # returns a (so gcd(5, 0) = 5 and gcd(0, 0) = 0).
    return a
