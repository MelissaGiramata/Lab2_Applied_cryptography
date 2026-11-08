# Problem 3 – Requirements v2

Write a Python program that estimates the average number of random integers that must be generated from an interval before one of them is prime.

## Files and running
- Program: `Problem_3/app/average_attempts.py`.
- Run from the repository root: `python Problem_3/app/average_attempts.py`.
- Running a script puts its own folder (`Problem_3/app`), not the repository root, on Python's import path. So the script first adds the repository root to `sys.path` (as Problem_2's tests do), so that the import below works.

## Input and Output

Input:
- The program uses two fixed experiments, each defined by an interval and a number of trials.
    - Experiment 1: interval 5,000,000 to 6,000,000, 1000 trials.
    - Experiment 2: interval 500,000,000,000 to 500,001,000,000, 250 trials.
- Interval ends are inclusive.

Random seed:
- The seed is fixed at 42, so every run gives the same results.
- The seed is set once, at program start, before Experiment 1. Experiment 2 continues the same random stream.

Output:
- The program prints, for each experiment: its interval, number of trials, average count (2 decimal places), and runtime in seconds.
- The program prints the random seed used.
- The same output is saved to `Problem_3/results/averages.txt`. The file is overwritten on each run.

## Reuse of is_prime
- The program must import and reuse `is_prime(n)` from `Problem_2/app/prime_test.py`, using the same import as Problem_2's tests: `from Problem_2.app.prime_test import is_prime`. It must not contain a second primality test.
- `is_prime(n)` returns `True` if n is prime and `False` otherwise. Its method (descending 6k±1 search from floor(√n) down to 5) is specified in `Problem_2/Requirements_v2.md`.

## Algorithm (unchanged from v1)
1. For each experiment (interval, number of trials):
   a. Set total to 0.
   b. Repeat for each trial:
      i.   Set count to 0.
      ii.  Generate a random integer in the interval (inclusive) and add 1 to count.
      iii. If the integer is not prime, go back to step ii.
      iv.  Add count to total.
   c. Average is total divided by the number of trials.
2. Print the average for each experiment.

## Verification
Tests use `unittest` (standard library). There is no expected value for the real averages. The tests are:
- Every count is ≥ 1.
- Drawn numbers stay inside the interval, with both ends inclusive.
- The same seed gives identical averages on two runs.
- `is_prime` used by the program is the one imported from Problem_2 (no second primality test).
- Known-answer test: interval [7, 7] with 10 trials gives a count of 1 on every trial and an average of 1.00.

To make these tests possible, the estimation must be usable with any interval and number of trials, not only the two fixed experiments.
