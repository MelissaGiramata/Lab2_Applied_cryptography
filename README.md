# Applied Cryptography – Lab 2

Python solutions to Lab 2 (`Lab 2.pdf`). Run every command below **from the repository root**.

## Folders

Each problem folder has `app/` (the program), `tests/` (`unittest`), `results/` (saved output), and its documents: `Requirements_v*.md`, `Design.md`, `interrogation.md`.

| Folder | Contents |
|---|---|
| `Problem_1` | Paper problem; no files. |
| `Problem_2` | `is_prime(n)`: primality test, descending 6k±1 search. |
| `Problem_3` | Average number of random draws before a prime, for two intervals. |
| `Problem_4` | Graph of the percentage of primes up to N, with 100 / ln(N) for comparison. |
| `Problem_5_7` | `gcd` (Problem 5), `euler_totient` (Problem 6), and the check of φ(p·q) = (p−1)(q−1) (Problem 7). |

**Problems 3, 4 and 5_7 import `is_prime` from `Problem_2/app/prime_test.py`** (`from Problem_2.app.prime_test import is_prime`). They do not contain their own copy, so keep `Problem_2` in place. Each script adds the repository root to `sys.path`, which is why you run from the root.

## Install

Python 3. Only Problem 4 needs a third-party package (matplotlib); everything else is standard library.

```
pip install -r requirements.txt
```

## Run

| Problem | Run the program | Run the tests |
|---|---|---|
| 2 | `python Problem_2/app/prime_test.py <n>` | `python Problem_2/tests/test_prime.py` |
| 3 | `python Problem_3/app/average_attempts.py` | `python Problem_3/tests/test_average_attempts.py` |
| 4 | `python Problem_4/app/prime_percentage.py` | `python Problem_4/tests/test_prime_percentage.py` |
| 5–7 | `python Problem_5_7/app/product_of_primes.py` | `python Problem_5_7/tests/test_gcd.py`, `test_totient.py`, `test_product_of_primes.py` |

`gcd.py` and `totient.py` in `Problem_5_7/app/` are libraries and are not run directly.

Rough runtimes: Problem 3 about 30 s, Problem 4 about 50 s (its tests about 45 s), Problem 5–7 about 20 s. The other tests take well under a second.

## Results

| Problem | Where |
|---|---|
| 2 | `Problem_2/results/`: `unittest_output.txt`, `piazza_results.txt`, `trace_127.txt`. The test run writes the last two. `unittest_output.txt` is the saved test output (`python Problem_2/tests/test_prime.py > Problem_2/results/unittest_output.txt 2>&1`). |
| 3 | `Problem_3/results/averages.txt` (seed, averages and runtimes; overwritten each run). |
| 4 | `Problem_4/results/`: `prime_percentage.png` (the graph) and `prime_percentages.txt` (first and last percentages). |
| 5–7 | `Problem_5_7/results/totient_results.txt` (table of pairs with runtimes, summary, and the p = q case). |
