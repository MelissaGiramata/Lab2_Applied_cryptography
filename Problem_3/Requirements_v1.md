
Write a Python program that estimates the average number of random integers that must be generated from an interval before one of them is prime.

## Input and Output

Input:
- The program uses two fixed experiments, each defined by an interval and a number of trials.
    - Experiment 1: interval 5,000,000 to 6,000,000, 1000 trials.
    - Experiment 2: interval 500,000,000,000 to 500,001,000,000, 250 trials.
- Interval ends are inclusive.

Output:
- The program prints, for each experiment: its interval, number of trials, average count (2 decimal places), and runtime in seconds.
- The program prints the random seed used.
- The same output is saved to Problem_3/results/averages.txt.

## Test

- The program must import and reuse is_prime(n) from Problem_2/app/prime_test.py, using the same import as Problem_2's tests: from Problem_2.app.prime_test import is_prime. It must not contain a second.
- is_prime(n) returns True if n is prime and False otherwise. Its method (descending 6k±1 search from floor(√n) down to 5) is specified in Problem_2/Requirements_v2.md.
- The program is run from the repository root so the import works.



## Algorithm
 
1. For each experiment (interval, number of trials):
   a. Set total to 0.
   b. Repeat for each trial:
      i.   Set count to 0.
      ii.  Generate a random integer in the interval (inclusive) and add 1 to count.
      iii. If the integer is not prime, go back to step ii.
      iv.  Add count to total.
   c. Average is total divided by the number of trials.
2. Print the average for each experiment.
 





