# Problem 4 – Requirements v2

Write a Python program that tests every number of the form 6k-1 and 6k+1 for primality, and graphs the percentage of numbers up to N that are prime as N grows.

## Files and running
- Program: `Problem_4/app/prime_percentage.py`.
- Tests: `Problem_4/tests/test_prime_percentage.py`.
- Run from the repository root: `python Problem_4/app/prime_percentage.py`.
- Library: `matplotlib` (not part of the standard library; installed with `pip install matplotlib`). It is used with a non-interactive backend so no window opens.

## Input and Output

Input:
- The upper limit of the search is fixed at 5,000,000.
- N is sampled at regular steps from 5,000 to 5,000,000 (every 5,000, giving 1000 sample points).

Output:
- A graph with N on the horizontal axis and the percentage of integers up to N that are prime on the vertical axis.
- The graph has a title, labelled axes, and a legend, and shows two lines:
    - the measured percentage (solid line)
    - 100 / ln(N) for comparison (dashed line)
- The graph is saved as `Problem_4/results/prime_percentage.png`. It is not displayed in a window, so the program never pauses.
- The program prints the percentage at the first and last sample points, with 2 decimals, for example:
    - `N = 5,000: 13.38%`
    - `N = 5,000,000: 6.97%`
- The same printed lines are saved to `Problem_4/results/prime_percentages.txt`. The file is overwritten on each run.

## Candidate Numbers

- Candidates are generated starting at k = 1 and increasing k by 1 each time: 5, 7, 11, 13, 17, 19, 23, 25, ...
- Both 6k-1 and 6k+1 are produced for each k, in increasing order.
- Candidates are generated until they exceed 5,000,000.
- Every prime greater than 3 has this form, so no prime above 3 is missed.
- 2 and 3 do not have this form but are prime, so they are counted separately.

## Primality Test

- The program must import and reuse `is_prime(n)` from `Problem_2/app/prime_test.py`, using: `from Problem_2.app.prime_test import is_prime`. It must not contain a second primality test.
- As in Problem_3, the script adds the repository root to `sys.path` so the import works.
- `is_prime(n)` returns `True` if n is prime and `False` otherwise. Its method is specified in `Problem_2/Requirements_v2.md`.

## Percentage Calculation

- The percentage for a given N is (number of primes less than or equal to N) divided by N, multiplied by 100.
- The prime count includes 2 and 3.
- The program makes a single pass through the candidates in increasing order and keeps a running count of primes found.
- When the current candidate passes a sample point N, the running count is used to record the percentage for that N.
- The count does not restart from 0 for each N. Every candidate is tested exactly once.

## Algorithm (unchanged from v1)

1. Set prime_count to 2 (for the primes 2 and 3).
2. Set the next sample point to 5,000.
3. For k = 1, 2, 3, ... while 6k-1 is at most 5,000,000:
   a. For each candidate in 6k-1, then 6k+1 (skipping any candidate above 5,000,000):
      i.  Before testing the candidate, if the candidate is greater than the next sample point, record
          (sample point, prime_count / sample point * 100) and move the next sample point up by 5,000.
          Repeat while the candidate is still greater than the next sample point.
      ii. If is_prime(candidate), add 1 to prime_count.
4. After the last candidate, record any remaining sample points up to 5,000,000 with the final prime_count.
5. Print the first and last recorded percentages and draw the graph from the recorded points.

## Verification
Tests use `unittest` (standard library):
- Known counts: the running count at N = 5,000 is 669 primes, and at N = 5,000,000 is 348,513 primes. The recorded percentages are 669 / 5,000 × 100 and 348,513 / 5,000,000 × 100.
- Small-case run: the same single-pass logic run with a small limit and step (e.g. limit 100, step 10) gives recorded counts that match a brute-force count of the primes up to each sample point.

To make the small-case test possible, the single-pass logic must be usable with any limit and step, not only 5,000,000 and 5,000.
