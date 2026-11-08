# Problem 4 – Interrogation

## Question 1
My graph shows the share of primes up to N, but Problem 3 measured the density near N. Is that difference why my measured line sits above 100/ln N? What approximation would match the "up to N" share more closely?

**Summary of the answer**
- Yes. Problem 3 measured the density near N, which the prime number theorem puts at about 1/ln N. Problem 4 measures π(N)/N, the average density over all integers from 1 to N. Small numbers are denser in primes (1/ln x is larger for small x), so the average sits above the density at N. The measured line is above the dashed line at every sample point.
- The gap is not constant: about 1.6 percentage points at N = 5,000, 0.9 at 100,000, and 0.49 at 5,000,000.
- Closer approximations (percent of integers up to N that are prime, measured value first):

  | N | Measured | 100/ln N | 100/(ln N − 1) | Li(N)/N | 1/L + 1/L² + 2/L³ |
  |---|---|---|---|---|---|
  | 5,000 | 13.380 | 11.741 | 13.303 | 13.665 | 13.443 |
  | 100,000 | 9.592 | 8.686 | 9.512 | 9.629 | 9.571 |
  | 1,000,000 | 7.850 | 7.238 | 7.803 | 7.863 | 7.838 |
  | 5,000,000 | 6.970 | 6.483 | 6.932 | 6.973 | 6.958 |

  (L = ln N; the last column is written as a percentage.)
- Li(N)/N, where Li(N) is the logarithmic integral (the sum of 1/ln t from 2 to N), is the best match: within 0.003 points at N = 5,000,000. It is exactly the average of the local density. 100/(ln N − 1) is a simple one-term fix, within about 0.04 points. The series 1/L + 1/L² + 2/L³ is accurate to about 0.01 points at N = 5,000,000.
- These values came from a throwaway script. No project files were changed. The dashed 100/ln N line is still correct as the density near N.

## Question 2
Explain why the single-pass design is so much faster than restarting from 0 for each sample point. Roughly how many is_prime calls does each approach make?

**Summary of the answer**
- The numbers tested for N = 10,000 include all those tested for N = 5,000, so a restart tests them again. A sample point only needs the number of primes up to N, which the running `prime_count` already holds. The single pass tests every candidate once and reads the count as the loop passes each sample point.
- Calls to `is_prime` (candidates 6k−1 and 6k+1 up to 5,000,000), counted exactly by a script:

  | Approach | Calls |
  |---|---|
  | Single pass | 1,666,666 |
  | Restart for each of the 1000 sample points | 834,165,667 |

  The restart approach makes about 500 times as many calls. In general, with J sample points it makes (J + 1) / 2 times as many.
- Time (estimated, the restart version was not run): the single pass took about 47 s. A call costs roughly in proportion to √n, and summing that model gives a ratio of about 400, so the restart version would take roughly 19,000 s, about five hours. The calls to `is_prime` are the cost; recording and graphing take almost no time in either design.
