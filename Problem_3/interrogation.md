# Problem 3 – Interrogation

## Question 1
Your sanity check said ln(500 billion) is about 27.9. I calculated about 26.9. Which is right? Where does the "average draws ≈ ln N" rule come from, and why does it work?

**Answer**

**Correction.** The user is right. ln(500 billion) = 26.94, not 27.9. I also gave ln(5.5 million) as 15.6; the correct value is 15.52. Both were stated from memory without checking. With the correct values:
- Experiment 2: measured 27.51, expected about 26.94. The difference is +0.57, about a third of one standard error (about 1.7 for 250 trials), so it is within chance.
- Experiment 1: measured 15.15, expected about 15.52. The difference is −0.37, within one standard error (about 0.47 for 1000 trials).

**Where the rule comes from**
1. The prime number theorem: the number of primes up to x is about x / ln x, so the chance that a random integer near x is prime is about 1 / ln x.
2. The program draws with replacement, so each draw has the same chance p ≈ 1 / ln N of being prime, independent of earlier draws.
3. The number of draws until the first success is geometric, with mean 1/p ≈ ln N.

The program's `count` includes the draw that turned out prime, which matches the geometric count. Counting only the failures would give about ln N − 1.

**Why it works here**
- Direct check: there are 64,336 primes in [5,000,000, 6,000,000], a density of 0.0643, so 1/p = 15.54, just above ln(5.5 million) = 15.52.
- The intervals are narrow compared to N, so the density barely changes across them.
- Even numbers are drawn too, which is why the average is ln N and not about half of it.

## Question 2
Experiment 2 took about 130 times longer than Experiment 1. Using how is_prime works, explain where that extra time comes from. How much is due to the larger √n, and how much to drawing more numbers per trial?

**Answer**

I re-ran the same seeded draws and counted loop passes using the `tested` list (nothing was saved or changed). The time is almost entirely passes of the `while i >= 5` loop.

| | Experiment 1 | Experiment 2 | Ratio |
|---|---|---|---|
| Trials | 1000 | 250 | 0.25 |
| Draws per trial | 15.15 | 27.51 | 1.82 |
| Loop passes per draw | 202 | 60,409 | 299 |
| Total loop passes | 3.06 million | 415 million | 136 |
| Time | 0.23 s | 29.29 s | about 127 |

The factors multiply to the total: 0.25 × 1.82 × 299 ≈ 136. A pass costs about 70 ns in both runs. The time ratio (about 127) is a little below 136, mostly because 0.23 s is rounded.

- **Larger √n (factor of about 299).** A number that passes the 2 and 3 checks is tested against every 1-or-5-mod-6 divisor from floor(√n) down, about √n / 3 values. For a prime the loop runs to the bottom: 780 passes per prime in Experiment 1 and 235,702 in Experiment 2, matching √n / 3. √n grows by about 300 (707,107 / 2,345).
- **More draws per trial (factor of about 1.82).** A trial draws about ln N numbers: 27.5 instead of 15.1.
- Per trial the cost grows by 299 × 1.82 ≈ 544. On a log scale, about 90% of that growth is the larger √n and about 10% is the extra draws. Experiment 2 has 4 times fewer trials, which divides the total by 4 and gives the overall 136.

**Composites cost more than primes.**
- Experiment 2: 59 million loop passes were spent on primes and 357 million on composites. Experiment 1: 0.78 million on primes and 2.28 million on composites.
- About two thirds of draws are even or divisible by 3 and cost nothing, since they exit at the early checks.
- The other composites (about 1,980 draws in Experiment 2) averaged about 180,000 passes each, roughly three quarters of a prime's cost. The search goes downward and stops at the largest divisor it reaches, so a number like 5 × (large prime) or 7 × (large prime) runs almost to the bottom before its small factor is found.
- This is a consequence of the descending order the algorithm specifies. The algorithm was not changed. An ascending search would find those small factors almost immediately.
