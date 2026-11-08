# Why φ(pq) = (p − 1)(q − 1)

For distinct primes p and q, an integer from 1 to pq shares a factor with pq only if it is a multiple of p (there are q of these) or a multiple of q (there are p of these), and pq itself is counted in both, so p + q − 1 numbers are not coprime to pq. That leaves pq − (p + q − 1) = (p − 1)(q − 1) numbers that are coprime.

When p = q, n = p² and the only non-coprime numbers are the p multiples of p, so φ(p²) = p(p − 1), which is p − 1 larger than (p − 1)². The derivation fails because the multiples of p and the multiples of q are the same set, so they are subtracted twice. For example, φ(9) = 6 but (3 − 1)² = 4.

This matters for RSA because the public modulus is n = pq, and the private key needs φ(n). Whoever knows p and q gets φ(n) with one multiplication, while anyone who only knows n would have to count coprime integers, which is impossible for a 2048-bit n; knowing φ(n) would also reveal p and q, so computing it is as hard as factoring n. The primes must be different because with p = q the formula gives the wrong value, and n = p² could be factored instantly with a square root.