Write a Python program with a non-recursive greatest common divisor function, an Euler totient function built on it, and a test that compares the totient of a product of two primes with a formula.
Greatest common divisor:
- gcd(a, b) is the largest positive integer that divides both a and b.
- Euclidean algorithm, for a > b:
    - Divide a by b to get a = q1*b + r1. Any number that divides both a and b also divides r1, so gcd(a, b) = gcd(b, r1).
    - Repeat with b and r1: b = q2*r1 + r2, so gcd(b, r1) = gcd(r1, r2).
    - Continue until a remainder is 0. The last non-zero remainder is the gcd.

Euler totient:
- The Euler totient of n, written phi(n), is the number of integers less than n whose greatest common divisor with n is 1.
- Example: phi(12) = 4, because 1, 5, 7 and 11 are the integers less than 12 that share no factor with 12.


## Part 1: Non-Recursive GCD

Input:
- Two positive integers a and b.

Output:
- The greatest common divisor of a and b.

Requirements:
- The function is named gcd and takes two arguments.
- The function does not call itself and does not use recursion, so the number of steps does not use up the call stack for large inputs.
- The function uses the Euclidean algorithm with a loop.
- The function returns the correct result whether a is greater than, less than, or equal to b.
- If b is 0, the function returns a.
- The function does not call math.gcd.

Algorithm:
1. While b is not 0:
   a. Compute the new values from the current a and b at the same time: the new a is the current b, and the new b is the remainder of the current a divided by the current b.
   b. Do not update a first and then use the updated a to compute the remainder; that gives a wrong result.
2. Return a.

Worked example, gcd(12, 8):
- a = 12, b = 8  -> new a = 8, new b = 12 % 8 = 4
- a = 8,  b = 4  -> new a = 4, new b = 8 % 4 = 0
- b is 0, return 4.

Test cases:
- gcd(12, 8) = 4
- gcd(8, 12) = 4
- gcd(17, 5) = 1
- gcd(100, 75) = 25
- gcd(7, 7) = 7
- gcd(1, 1) = 1
- gcd(1071, 462) = 21
- gcd(2880067194370816120, 1779979416004714189) = 1
  (two consecutive Fibonacci numbers, which is the slowest case for the Euclidean algorithm, so it checks that a large number of steps works without error)


## Part 2: Euler Totient

Input:
- A positive integer n.

Output:
- phi(n), the number of integers less than n whose gcd with n is 1.

Requirements:
- The function is named euler_totient and takes one argument.
- The function calls the non-recursive gcd function from Part 1 and does not use math.gcd or any other gcd.
- The function counts the integers i from 1 to n - 1 for which gcd(i, n) is 1.
- If n is 1, the function returns 1. Taken literally, the lab's definition ("integers less than n") would count nothing for n = 1 and give 0. The standard convention is phi(1) = 1, because many definitions count integers from 1 to n inclusive, and gcd(1, 1) = 1. I follow the standard convention and handle n = 1 as a special case.

Algorithm:
1. If n is 1, return 1.
2. Set count to 0.
3. For each integer i from 1 to n - 1:
   a. If gcd(i, n) is 1, add 1 to count.
4. Return count.

Test cases:
- euler_totient(1) = 1
- euler_totient(2) = 1
- euler_totient(7) = 6
- euler_totient(9) = 6
- euler_totient(10) = 4
- euler_totient(12) = 4
- euler_totient(15) = 8
- euler_totient(100) = 40


## Part 3: Totient of a Product of Two Primes

Input:
- Two distinct prime numbers p and q, each between 2000 and 3000.

Output:
- For each pair tested, the program prints p, q, the product p*q, euler_totient(p*q), the value (p-1)*(q-1), and whether the two values are equal.

Requirements:
- The primes are found by the program from the range 2000 to 3000, not typed in by hand.
- Primality is checked by importing and reusing is_prime(n) from Problem_2/app/prime_test.py (from Problem_2.app.prime_test import is_prime). The program does not contain a second primality test. As in Problems 3 and 4, the script adds the repository root to sys.path and is run from the repository root.
- The program tests at least 5 different pairs of primes, including the smallest pair and a pair that includes the largest prime in the range.
- euler_totient from Part 2 is used to compute the totient of p*q.
- The program prints a clear summary stating whether (p-1)*(q-1) matched euler_totient(p*q) for every pair.

Algorithm:
1. Find all primes between 2000 and 3000 by calling is_prime on each integer in that range.
2. Choose at least 5 distinct pairs (p, q) with p different from q.
3. For each pair:
   a. Compute n as p * q.
   b. Compute euler_totient(n).
   c. Compute (p - 1) * (q - 1).
   d. Print the values and whether they are equal.
4. Print whether all pairs matched.

Expected results:
- The two values are equal for every pair of distinct primes. Examples:
    p = 2003, q = 2011: p*q = 4028033, expected totient = 4024020.
    p = 2003, q = 2999: p*q = 6006997, expected totient = 6001996.
    p = 2011, q = 2017: p*q = 4056187, expected totient = 4052160.

Extra check:
- Use the same prime twice (p = q). Then euler_totient(p*p) equals p*(p-1), not (p-1)*(p-1), so the formula does not hold. The program may print this case to show why p and q must be different.