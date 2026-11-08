# Problem 2 – Design

Based on `Requirements_v2.md`. The algorithm is unchanged from the requirements.

## Folder layout

```
Problem_2/
  Requirements_v1.md
  Requirements_v2.md
  Design.md
  app/
    prime_test.py        # is_prime, main
  tests/
    test_prime.py        # unittest: small cases, Piazza cases, trace tests, error tests
  results/
    unittest_output.txt  # output of the unittest run
    piazza_results.txt   # prime / not prime for each of the four Piazza numbers
    trace_127.txt        # divisors tested for n = 127
```

The Piazza results and the 127 trace are written during the test run.

## Libraries
All standard library, nothing to install.
- `math`: `math.isqrt` for the integer floor of the square root.
- `sys`: `sys.argv` for the command-line arguments, `sys.exit` for the usage exit.
- `unittest`: the tests.

## Functions

### `is_prime(n, tested=None)`
- Input:
  - `n`: the number to test.
  - `tested`: optional. If a list is passed, the main loop appends each divisor it tests, in order. Normal calls (including Problem_3) do not pass it.
- Output: `True` if n is prime, `False` otherwise.
- Raises `TypeError` if n is not an `int` or if n is a `bool`.
- The main loop is written directly inside this function; there is no separate helper.
- Steps:
  1. n is not an int, or is a bool → `TypeError`.
  2. n < 2 → `False`.
  3. n is 2 or 3 → `True`.
  4. n divisible by 2 or 3 → `False`.
  5. `limit = math.isqrt(n)`. If `limit < 5` → `True`.
  6. Set `i` to the start value (table below).
  7. While `i >= 5`: if `tested` is not None, append `i` to it. If `n % i == 0` → `False`. Then step `i` down by 2 or 4.
  8. → `True`.
- The divisor is appended before the divisibility check, so `tested` includes the divisor that was found (e.g. 49 gives `[7]`). Early returns (steps 2–5) leave `tested` empty.

### `main()`
- Input: `sys.argv`.
- Output: prints a clear message such as `37 is prime` or `36 is not prime`.
- If the script receives anything other than exactly one argument, or the argument cannot be converted to an integer, it prints `Usage: python prime_test.py <n>` and exits without a traceback.
- Called only under `if __name__ == "__main__":`, so importing the module never runs it.

## How the loop avoids building a list of candidates

The loop keeps a single number, `i`. Each pass tests `i`, then changes `i` by subtracting 2 or 4, and goes round again. Only the current `i` exists at any time; the other candidates are never stored, so memory use is a few numbers whatever the size of n. For n around 10^15, floor(√n) is about 3.2 × 10^7, and a list of the 1-or-5-mod-6 candidates below it would hold over ten million values. The loop never makes that list.

The early exit is kept too: the first `i` that divides n makes `is_prime` return `False` immediately, and the candidates below that `i` are never computed. The `tested` list, when passed, grows by one entry per pass, so it only holds what was actually tested (it is for tracing small n; it is not passed for large n).

## How the descending 6k±1 loop works

Every prime above 3 is 6k−1 or 6k+1, i.e. has remainder 5 or 1 when divided by 6, so only those divisors need testing.

1. **Limit.** `limit = math.isqrt(n)`. Integer arithmetic, no rounding error for large n.
2. **Small limit.** If `limit < 5`, there is nothing to test: return prime.
3. **Start value.** i is the largest number ≤ limit with remainder 1 or 5 mod 6. From limit's remainder:

   | limit % 6 | start i |
   |-----------|---------|
   | 0 | limit − 1 |
   | 1 | limit |
   | 2 | limit − 1 |
   | 3 | limit − 2 |
   | 4 | limit − 3 |
   | 5 | limit |

   Because limit ≥ 5, the start value is always ≥ 5.
4. **Loop** while `i >= 5`:
   - If `tested` was passed, append `i` to it.
   - If `n % i == 0` → not prime.
   - If `i % 6 == 1`, `i -= 2` (6k+1 → 6k−1). Otherwise (remainder 5), `i -= 4` (6k−1 → 6(k−1)+1).
5. **End.** The step from 5 gives 1, which is below 5, so the loop ends. Every divisor tested was ≥ 5. If none divided n, return prime.

Worked example, n = 127: limit = 11 (11 % 6 = 5, so start i = 11). Tests 11, then 11 − 4 = 7, then 7 − 2 = 5, then 5 − 4 = 1 and stop. `tested` ends as `[11, 7, 5]`. None divides 127, so it is prime.

## Tests (`tests/test_prime.py`, `unittest`)
- Piazza numbers: 1000000000000037 and 1000000000000223 prime; 1000000000000001 and 1000000000000005 not prime. Results written to `results/piazza_results.txt`.
- Small cases: 0, 1, 4, 25, 49 not prime; 2, 3, 29 prime.
- Edge cases: a negative number, divisibility by 2 and by 3, floor(√n) < 5.
- `TypeError` for a string, a float, `True` and `False`.
- Trace tests: call `is_prime(n, tested=lst)` with an empty list and check `lst`.
  - Every entry has remainder 1 or 5 mod 6, and the entries are strictly descending.
  - For prime n with floor(√n) ≥ 5, the last entry is 5 (not applicable to composite n, where the loop stops at the first divisor found).
  - `is_prime(127, tested=lst)` leaves `lst == [11, 7, 5]`. This trace is also written to `results/trace_127.txt`.
- Command-line script: no argument, two arguments, and a non-integer argument each give the usage message and no traceback.
- The `unittest` output is saved to `results/unittest_output.txt`.

## How Problem_3 imports `is_prime`

Problem_3 must re-use the same code, not copy it.

- `Problem_2/app/prime_test.py` defines `is_prime`. The module has no side effects on import (the command-line code is behind the `__main__` guard).
- Run Problem_3 from the repository root (`Lab2_Applied_cryptography/`) and use `from Problem_2.app.prime_test import is_prime`, then call `is_prime(n)` without the `tested` argument. `Problem_2` and `app` are valid Python names, and Python 3 resolves them as namespace packages from the repository root, so no `__init__.py` files are required.
- If Problem_3 is run from another directory, add the repository root (or `Problem_2/app`) to `sys.path` before importing; with `Problem_2/app` on the path the import becomes `from prime_test import is_prime`.
