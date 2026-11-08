# Problem 2 – Requirements v2

Write a Python program that determines whether a given positive integer n is prime.

## Interface
- File: `Problem_2/prime_test.py`.
- An importable function `is_prime(n)` that returns `True` (prime) or `False` (not prime). Problem 3 must re-use this function.
- A script that reads n from a command-line argument, calls the function, and prints a clear message (e.g. "37 is prime" / "36 is not prime").
- If the command-line argument is missing, print `Usage: python prime_test.py <n>` and exit without a traceback.

## Input and Output
Input:
- A single integer n, passed as a command-line argument.

Output:
- Function: `True` / `False`.
- Script: a clear printed message stating whether n is prime or not prime.

Invalid input:
- Any integer less than 2 (including 1, 0 and negatives) is not prime.
- A non-integer input raises an error.

Edge cases:
- If n is less than 2 (including 1), n is not prime.
- If n is 2 or 3, n is prime.

Initial divisibility checks
- If n is divisible by 2, n is not prime.
- If n is divisible by 3, n is not prime.
- These checks are performed before the main search.

Search limit
- The search runs in descending order, starting at the floor of the square root of n and moving down to 5.
- The floor of the square root is computed using integer arithmetic (math.isqrt), not floating point, to avoid rounding errors for large n.

## Algorithm (unchanged from v1)
1. If n < 2, return not prime.
2. If n is 2 or 3, return prime.
3. If n is divisible by 2 or by 3, return not prime.
4. Set limit to the floor of the square root of n.
5. If limit < 5, return prime.
6. Set i to the largest number less than or equal to limit whose remainder when divided by 6 is 1 or 5.
7. While i >= 5:
   a. If n is divisible by i, return not prime.
   b. If i has remainder 1 when divided by 6, decrease i by 2. Otherwise (remainder 5), decrease i by 4.
8. Return prime.

## Test Cases (numbers posted on Piazza)
The program must return the following results.

| n | Expected |
|---|----------|
| 1000000000000037 | Prime |
| 1000000000000223 | Prime |
| 1000000000000001 | Not prime |
| 1000000000000005 | Not prime |

## Small Test Cases
| n | Expected |
|---|----------|
| 0 | Not prime |
| 1 | Not prime |
| 2 | Prime |
| 3 | Prime |
| 4 | Not prime |
| 25 | Not prime |
| 49 | Not prime |
| 29 | Prime |

(29 is the small prime above 25.)

## Verification
- A test file covering the four Piazza numbers, the small test cases above, and the edge cases (n < 2, including 1, 0 and a negative; n = 2; n = 3; divisibility by 2 and by 3; limit < 5).
- A trace check confirming the main loop visits only values with remainder 1 or 5 modulo 6, in descending order.
- The "last divisor tested is 5" check applies only when n is prime and floor(√n) ≥ 5. (For composite n the loop stops at the first divisor found.)
- A trace test for n = 127 (prime, floor(√127) = 11), showing the −4/−2 alternation. The divisors tested, in order, must be: 11, 7, 5.
