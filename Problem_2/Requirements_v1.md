


Write A Python program that determines whether a given positive integer n is prime. 


## Input and Output

Input:
- The program accepts a single positive integer n.

Output:
- The program reports whether n is prime or not prime (for example, True/False or a clear message).

Edge cases:
- If n is less than 2 (including 1), n is not prime.
- If n is 2 or 3, n is prime.

Initial divisibility checks
- If n is divisible by 2, n is not prime.
- If n is divisible by 3, n is not prime.
- These checks are performed before the main search.

Search limit
-  The search runs in descending order, starting at the floor of the square root of n and moving down to 5.
- The floor of the square root is computed using integer arithmetic (math.isqrt), not floating point, to avoid rounding errors for large n.


Algorithm
1. If n < 2, return not prime.
2. If n is 2 or 3, return prime.
3. If n is divisible by 2 or by 3, return not prime.
4. Set limit to the floor of the square root of n.
5. If limit < 5, return prime.
6. Set i to the largest number less than or equal to limit whose remainder when divided by 6 is 1 or 5 .
7. While i >= 5:
   a. If n is divisible by i, return not prime.
   b. If i has remainder 1 when divided by 6, decrease i by 2. Otherwise (remainder 5), decrease i by 4.
8. Return prime.

Test Cases
The program must return the following results.
1000000000000037,
1000000000000223,
1000000000000001,
1000000000000005

