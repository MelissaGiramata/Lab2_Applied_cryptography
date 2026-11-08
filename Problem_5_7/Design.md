# Problems 5–7 – Design

Based on `Requirements_v2.md`. The algorithms are unchanged from the requirements.

## Folder layout

Same layout as Problems 2–4: `app/` for the programs, `tests/` next to it, `results/` for output.

```
Problem_5_7/
  Requirements_v1.md
  Requirements_v2.md
  Design.md
  app/
    gcd.py                       # Problem 5: gcd
    totient.py                   # Problem 6: euler_totient (uses gcd)
    product_of_primes.py         # Problem 7: the Part 3 run (uses euler_totient and is_prime)
  tests/
    test_gcd.py
    test_totient.py
    test_product_of_primes.py
  results/
    totient_results.txt          # written by product_of_primes.py, overwritten on each run
```

- One module per lab problem, one test file per module.
- The empty `Problem_5_7/app/data/` and `Problem_5_7/app/tests/` folders that exist on disk are not part of this layout and are removed when the code is written. `design_v1.md` and `interrogation.md` (empty files already in the folder) are left alone.
- The folder name has an underscore (not a hyphen) so Python can import from it, like `Problem_2`.

## Libraries
- Program: `time` (`time.perf_counter` for the runtime), `os` and `sys` (find the repository root, add it to `sys.path`, create `results/`). All standard library. `gcd.py` and `totient.py` need no libraries.
- Tests: `unittest`. `math` is used in `test_gcd.py` only, for `math.gcd` as an independent check. The program never uses it.
- Nothing to install.

## Imports between the modules

```
gcd.py                   (imports nothing)
   ^
   |  from Problem_5_7.app.gcd import gcd
totient.py               (euler_totient)
   ^
   |  from Problem_5_7.app.totient import euler_totient
product_of_primes.py     (the run)  --  from Problem_2.app.prime_test import is_prime
```

- All imports start from the repository root (`Problem_5_7.app...`, `Problem_2.app...`), which Python finds as namespace packages (no `__init__.py` needed).
- `product_of_primes.py` is the only script that is run. As in Problems 2–4, it first adds the repository root to `sys.path`: take `os.path.abspath(__file__)`, go up three levels with `os.path.dirname` (file → `app` → `Problem_5_7` → root), and insert that at the front of `sys.path`. Only then does it import `is_prime` and `euler_totient`.
- `gcd.py` and `totient.py` are libraries, not scripts. `totient.py` relies on the repository root already being on `sys.path`, which `product_of_primes.py` and the test files make sure of.
- Each test file adds the repository root to `sys.path` the same way, then imports the module it tests.
- `is_prime` is imported from Problem_2, never re-written. `euler_totient` calls the `gcd` from `gcd.py`, not `math.gcd`.

## Functions

### `gcd(a, b)` — in `app/gcd.py` (Problem 5)
- Input: two ints `a` and `b`, with `a >= 0` and `b >= 0`.
- Output: the greatest common divisor.
- Raises `TypeError` if `a` or `b` is not an `int` or is a `bool`; raises `ValueError` if either is negative. (Type is checked first.)
- Steps:
  1. Check the inputs.
  2. While `b != 0`: set `a, b = b, a % b`. Python works out the whole right-hand side with the *old* `a` and `b` first, and only then assigns both, so this is the "new values at the same time" the algorithm asks for.
  3. Return `a`.
- It is a loop and never calls itself. `gcd(5, 0)` returns 5 (the loop does not run) and `gcd(0, 0)` returns 0.
- Order does not matter: if `a < b`, the first pass of the loop swaps them (`a % b` is `a`).

### `euler_totient(n)` — in `app/totient.py` (Problem 6)
- Input: a positive int `n`.
- Output: phi(n), the number of integers from 1 to n − 1 whose gcd with n is 1 (and 1 for n = 1).
- Raises `TypeError` if `n` is not an `int` or is a `bool`; raises `ValueError` if `n < 1`.
- Steps:
  1. Check the input.
  2. If `n == 1`, return 1.
  3. `count = 0`.
  4. For each `i` from 1 to `n - 1`: if `gcd(i, n) == 1`, add 1 to `count`.
  5. Return `count`.

### In `app/product_of_primes.py` (Problem 7)

**`find_primes(low, high)`**
- Input: the two ends of the range (both included).
- Output: a list of the primes in the range, in increasing order, found by calling the imported `is_prime` on every integer. (2000 and 3000 are not prime, so including both ends changes nothing.)

**`choose_pairs(primes)`**
- Input: the list from `find_primes`.
- Output: a list of five `(p, q)` pairs, chosen by position, with `mid = len(primes) // 2`:
  1. `(primes[0], primes[1])`
  2. `(primes[0], primes[-1])`
  3. `(primes[1], primes[2])`
  4. `(primes[-2], primes[-1])`
  5. `(primes[mid], primes[mid + 1])`
- No totient is computed here, so it is fast and can be tested on its own.

**`compare_pair(p, q)`**
- Input: two numbers `p` and `q`. It works for any p and q (not only primes from 2000 to 3000), so the tests can use small ones.
- Output: a tuple `(product, totient, formula, equal, runtime)`:
  - `product = p * q`
  - `totient = euler_totient(product)`
  - `formula = (p - 1) * (q - 1)`
  - `equal = (totient == formula)`
  - `runtime` = seconds taken by the `euler_totient` call only (`time.perf_counter()` just before and just after it).
- With `p = q` the same function is used, and `equal` comes out `False`.

**`format_pair(label, p, q, result)`**
- Input: a label such as `Pair 1`, p, q, and the tuple from `compare_pair`.
- Output: one line of text with p, q, the product, the totient, the formula value, `equal: yes/no`, and the runtime with 2 decimals.

**`main()`**
- Input: none.
- Output: prints the lines below and saves the same text to `Problem_5_7/results/totient_results.txt`.
- Steps:
  1. `primes = find_primes(2000, 3000)`.
  2. `pairs = choose_pairs(primes)`.
  3. For each pair: `result = compare_pair(p, q)`, add `format_pair(...)` to the output lines, and remember whether `equal` was `True`.
  4. Add a summary line saying whether `(p-1)*(q-1)` matched `euler_totient(p*q)` for every pair.
  5. The `p = q` check, with `p = primes[0]` (2003): `result = compare_pair(p, p)`. Add lines showing `euler_totient(p*p)`, `p*(p-1)` (equal to the totient) and `(p-1)*(p-1)` (different), and the runtime.
  6. Print every line. Create `results/` if missing and write the same lines to `totient_results.txt` (mode `"w"`, which replaces any old content).
- Called only under `if __name__ == "__main__":`, so importing the module (as the tests do) does not run anything.

## What goes in `results/`
Only `totient_results.txt`, overwritten on each run. It has the printed output, in this order:
1. One line per pair (five lines), each with p, q, p*q, `euler_totient(p*q)`, `(p-1)*(q-1)`, whether they are equal, and the runtime.
2. The summary line.
3. The p = q lines.

Example of the shape (runtimes are placeholders):
```
Pair 1: p=2003, q=2011, p*q=4028033, euler_totient=4024020, (p-1)*(q-1)=4024020, equal: yes, runtime x.xx s
Pair 2: p=2003, q=2999, p*q=6006997, euler_totient=6001996, (p-1)*(q-1)=6001996, equal: yes, runtime x.xx s
Pair 3: p=2011, q=2017, p*q=4056187, euler_totient=4052160, (p-1)*(q-1)=4052160, equal: yes, runtime x.xx s
Pair 4: ...
Pair 5: ...
Summary: (p-1)*(q-1) matched euler_totient(p*q) for all 5 pairs.
Same prime twice: p=q=2003, p*p=4012009, euler_totient=4010006, p*(p-1)=4010006, (p-1)*(p-1)=4008004, equal: no, runtime x.xx s
```
The exact wording is a design choice; the requirements fix which items are printed.

## Tests (`unittest`, one file per module)
Each is run from the repository root, e.g. `python Problem_5_7/tests/test_gcd.py`.

| File | What it checks |
|---|---|
| `test_gcd.py` | The 8 Part 1 cases (12/8, 8/12, 17/5, 100/75, 7/7, 1/1, 1071/462, and the two Fibonacci numbers), `gcd(5, 0) = 5`, `gcd(0, 0) = 0`. `TypeError` for a string, a float, `True` and `False`; `ValueError` for a negative number. A comparison with `math.gcd` for every pair of numbers from 0 to 40 (in the test only). |
| `test_totient.py` | The 8 Part 2 cases (1, 2, 7, 9, 10, 12, 15, 100). `TypeError` for a string, a float, `True` and `False`; `ValueError` for 0 and a negative number. |
| `test_product_of_primes.py` | `compare_pair(5, 7)`: totient 24 equals formula 24. `compare_pair(5, 5)`: totient 20 equals `5 * 4`, formula 16, `equal` is `False`. `find_primes(2000, 3000)` gives 127 primes, first 2003, last 2999. `choose_pairs` on that list gives the five pairs above (checks the positions only). |

`test_product_of_primes.py` does not compute the totient of any product of primes from 2000 to 3000, so it stays fast. The three expected-result examples (2003/2011, 2003/2999, 2011/2017) are checked against the main program's output in `totient_results.txt`.

## Running time
Each `euler_totient` call makes about p·q calls to `gcd` (4 to 9 million). With five pairs and the p = q case that is about 33 million `gcd` calls, so the main program is expected to take roughly one to two minutes. This is a rough estimate, not measured. The tests are fast.
