# Problem 2 – Interrogation

## Question 1
Why is it enough to check divisors up to floor(√n)? If n had a factor above √n, why would we still catch it?

**Summary of the answer**
- If n is composite, n = a × b. Both factors cannot be bigger than √n, because their product would then be bigger than n. So the smaller factor is at most √n, and since it is a whole number, at most floor(√n).
- A factor b above √n always has a partner a = n / b below √n, and that partner also divides n. The search tests every candidate up to floor(√n), so it finds the partner and never needs to test b.
- Examples: 147 = 3 × 49 is caught by the 3 (early check). 91 = 7 × 13 is caught at 7, and 13 is never looked at.
- Going in descending order is still safe: all candidates are tested, only the order differs. It affects speed, not correctness.
- The 6k±1 step is safe for a separate reason: a divisor that is not of the form 6k±1 (and is not 2 or 3) has a factor of 2 or 3 itself. If it divided n, then 2 or 3 would divide n too, and the early checks have already ruled that out.

## Question 2
Walk me through is_prime line by line for n = 49. What is limit, what is the first i, and why does it stop where it does?

**Summary of the answer**
- The type check passes (49 is an int, not a bool). 49 is not below 2, not 2 or 3, and not divisible by 2 or 3 (49 % 2 = 1, 49 % 3 = 1).
- `limit = math.isqrt(49) = 7`, which is not below 5, so the search runs.
- `7 % 6 = 1`, so the start value is `i = limit = 7` (6×1 + 1).
- First pass of the loop: 7 ≥ 5, 7 is recorded in the trace list if one was passed, and `49 % 7 == 0`, so `is_prime` returns `False` immediately.
- The loop stops there because 7 is a divisor, not because `i` reached 5. The −2/−4 step never runs. The trace for 49 is `[7]`, which `test_composite_stops_at_first_divisor` checks.
- 49 = 7 × 7 is a perfect square, so it shows why the limit is floor(√n) and not one less: stopping at 6 would miss 7 and call 49 prime.
