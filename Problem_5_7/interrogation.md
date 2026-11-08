# Problems 5–7 – Interrogation

## Question 1
Show me step by step what goes wrong in gcd(12, 8) if a is updated before the remainder is computed, and how a, b = b, a % b avoids it.

**Summary of the answer**
- Buggy version: `a = b` and then `b = a % b`. Starting with a = 12, b = 8: after `a = b`, a is 8 and the old a (12) is gone. Then `b = a % b` computes 8 % 8 = 0, not 12 % 8. The loop ends and the function returns 8. The correct answer is 4.
- The bug is not a one-off. After `a = b`, the next line is always `b % b`, which is always 0, so the loop runs once and returns the original b whatever the inputs. For example, `gcd(17, 5)` would return 5 instead of 1, and `gcd(8, 12)` would return 12 instead of 4.
- Fix: `a, b = b, a % b`. Python works out the whole right-hand side with the old a and b first, `(8, 12 % 8) = (8, 4)`, and only then assigns both. The next pass gives `(4, 8 % 4) = (4, 0)`, b is 0, and the function returns 4.
- The same fix with a temporary variable: `old_a = a`, `a = b`, `b = old_a % b`. The tuple form does the saving in one line.

## Question 2
For n = pq, why does knowing φ(n) let you find p and q? Why does that make RSA's security depend on factoring?

**Summary of the answer**
- Why φ(n) gives p and q: φ(n) = (p − 1)(q − 1) = n − (p + q) + 1, so p + q = n − φ(n) + 1. Knowing the sum and the product (n) of p and q, they are the roots of x² − (p + q)·x + n = 0, so p, q = ((p + q) ± √((p + q)² − 4n)) / 2.
- Example from Problem 7: n = 4,028,033 and φ(n) = 4,024,020 give p + q = 4,014. Then 4,014² − 4 × 4,028,033 = 64, with square root 8, so the roots are (4,014 ± 8) / 2 = 2,011 and 2,003.
- Link to RSA: the public key is (n, e) and the private exponent d is the inverse of e modulo φ(n). Whoever can compute φ(n) can compute d. Computing φ(n) from n alone gives the factors, so it is no easier than factoring n. Conversely, factoring n gives φ(n) = (p − 1)(q − 1) and then d.
- The brute-force `euler_totient` from Part 2 loops over all n − 1 numbers, which is far slower than trial division up to √n. For a 2048-bit n, the only known efficient route to φ(n) is through factoring, which no one knows how to do at that size.
- Precision: what is proven is that recovering the private key (d, or φ(n)) is equivalent to factoring n. Whether breaking RSA encryption in another way, by computing e-th roots modulo n without the key, would also require factoring is an open question. "RSA's security depends on factoring" is true in the sense that factoring would break it, and no better attack is known.
