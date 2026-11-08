# Problem 4 – Design

Based on `Requirements_v2.md`. The algorithm is unchanged from the requirements.

## Folder layout

Same layout as Problem_2 and Problem_3: `app/` for the program, `tests/` next to it, `results/` for output.

```
Problem_4/
  Requirements_v1.md
  Requirements_v2.md
  Design.md
  app/
    prime_percentage.py          # the program
  tests/
    test_prime_percentage.py     # unittest
  results/
    prime_percentage.png         # the graph, written by the program
    prime_percentages.txt        # the two printed lines, overwritten on each run
```

- There is no `app/data/` (no input data) and only one test folder, `Problem_4/tests/`.
- The empty `Problem_4/app/data/` and `Problem_4/app/tests/` folders that exist on disk are not part of this layout and are removed when the code is written.

## Libraries
- `math` (standard library): `math.log` for the 100 / ln(N) line.
- `os`, `sys` (standard library): to find the repository root and add it to `sys.path`, and to create `results/`.
- `matplotlib` (third-party, installed with `pip install matplotlib` when the code is written): draws and saves the graph.
  - Non-interactive backend: `matplotlib.use("Agg")` is called before `matplotlib.pyplot` is imported. The Agg backend only draws into a file, so no window opens and the program never pauses. The graph is saved with `savefig`; `plt.show()` is never called.
- `unittest` (standard library): the tests.
- `is_prime` comes from Problem_2 (see below). It is imported, never re-written.

## Importing `is_prime` from Problem_2

Same as Problem_3. Running `python Problem_4/app/prime_percentage.py` puts `Problem_4/app` on the import path, not the repository root, so the script adds the root itself before the import:

1. Take the script's own location: `os.path.abspath(__file__)`.
2. Go up three levels with `os.path.dirname`: file → `app` → `Problem_4` → repository root.
3. Insert that root at the front of `sys.path`.
4. Only then run `from Problem_2.app.prime_test import is_prime`.

The root is worked out from the file's location, not the current folder, so the import works from any working directory. The program is documented as run from the repository root.

## Functions

### `record_percentages(limit, step)`
This is the single-pass logic. `limit` and `step` are parameters, not hardcoded, so the tests can use small values (limit 100, step 10) and `main()` uses the real ones (limit 5,000,000, step 5,000).

- Input:
  - `limit`: the upper limit of the search (5,000,000 in the real run).
  - `step`: the spacing of the sample points (5,000 in the real run). The first sample point is `step`, and the sample points are `step`, `2 × step`, … up to `limit`.
- Output: a list with one entry per sample point, in increasing order. Each entry is `(sample_point, prime_count, percentage)`, where `percentage = prime_count / sample_point * 100`.
  - The list is `limit / step` long (1000 entries in the real run).
  - `prime_count` is returned as well as the percentage so the tests can check exact counts instead of comparing floating-point numbers.
- Checked at the start, before any work is done (both hold for 5,000,000 / 5,000 and for 100 / 10):
  - If `step < 5`, raise `ValueError("step must be at least 5, got ...")`. The count starts at 2 for the primes 2 and 3, so a sample point below 5 would be recorded wrongly. (This check comes first, so `step = 0` gives this error and never a division by zero.)
  - If `limit` is not a multiple of `step` (`limit % step != 0`), raise `ValueError("limit must be a multiple of step, got limit=... and step=...")`.
  - The messages include the values received.
- The steps are in "The single-pass loop" below.

### `summary_lines(records)`
- Input: the list returned by `record_percentages`.
- Output: a list of two strings, for the first and last sample points, with thousands separators and 2 decimals, for example `N = 5,000: 13.38%` and `N = 5,000,000: 6.97%`.

### `draw_graph(records, filename)`
- Input: the list returned by `record_percentages`, and the path of the PNG file to write.
- Output: nothing returned; the PNG file is written.
- Steps:
  1. Take the sample points as the horizontal values and the percentages as the vertical values.
  2. Plot the measured percentage as a solid line, labelled `Measured percentage of primes up to N`.
  3. Plot `100 / math.log(N)` for each sample point as a dashed line, labelled `100 / ln(N)`.
  4. Add the title `Percentage of integers up to N that are prime`, the axis labels `N` and `Percentage that are prime (%)`, and a legend.
  5. Save to `filename` and close the figure.

The title, axis labels and legend wording above are design choices; the requirements only say that a title, labelled axes and a legend are present.

### `main()`
- Input: none. The fixed values are the limit 5,000,000 and the step 5,000.
- Output: prints two lines, saves the same two lines to `results/prime_percentages.txt`, and saves the graph to `results/prime_percentage.png`.
- Steps:
  1. `records = record_percentages(5_000_000, 5_000)`.
  2. `lines = summary_lines(records)`; print each line.
  3. Create `Problem_4/results/` if it is missing. Write the same lines to `prime_percentages.txt` (opened with mode `"w"`, which replaces any old content).
  4. `draw_graph(records, Problem_4/results/prime_percentage.png)`.
- Called only under `if __name__ == "__main__":`, so importing the module (as the tests do) does not start the run.

## The single-pass loop (inside `record_percentages`)

1. `prime_count = 2` (for the primes 2 and 3, which are not of the form 6k±1). `records = []`.
2. `next_sample = step`.
3. For `k = 1, 2, 3, …` while `6k − 1 <= limit`:
   a. For each `candidate` in `6k − 1`, then `6k + 1`; skip any candidate above `limit` (this can only happen to `6k + 1`):
      i. While `candidate > next_sample`: every number up to `next_sample` has already been tested, so record `(next_sample, prime_count, prime_count / next_sample * 100)`, then add `step` to `next_sample`. (This runs more than once if the candidate jumps past several sample points; with a step of 5,000 it normally runs 0 or 1 time per candidate.)
      ii. If `is_prime(candidate)`, add 1 to `prime_count`.
4. After the last candidate: while `next_sample <= limit`, record `(next_sample, prime_count, prime_count / next_sample * 100)` with the final `prime_count`, and add `step` to `next_sample`. This records the sample points that no candidate got past, including `limit` itself (the last candidate, 4,999,997 or 4,999,999, never exceeds 5,000,000).
5. Return `records`.

Why this is one pass: `k` only goes up, every candidate is tested once, and `prime_count` is never reset. Each sample point just reads the count at the moment the loop passes it.

Why the recording is correct: candidates arrive in increasing order. When a candidate is greater than `next_sample`, all earlier candidates were less than or equal to it, so every candidate up to `next_sample` has been counted and no larger one has. A candidate equal to a sample point is tested first (the test is "greater than"), and recorded when the next candidate arrives, so `prime_count` means "primes less than or equal to N".

Worked example, `limit = 100`, `step = 10`:
- Start: `prime_count = 2`, `next_sample = 10`.
- Candidates 5 and 7 are prime (`prime_count` 3, then 4). Candidate 11 is greater than 10, so record `(10, 4, 40.0)`, set `next_sample = 20`, then test 11 (prime, count 5).
- Candidates 13, 17 and 19 are prime (count 8). Candidate 23 is greater than 20, so record `(20, 8, 40.0)`.
- … candidate 91 is the first one greater than 90 (the candidates before it are …, 85, 89). Before testing it, record `(90, 24, 26.67)`. Later, candidate 97 is prime, and the count ends at 25.
- No candidate is greater than 100, so step 4 records `(100, 25, 25.0)`.

## What gets written to `results/`
- `prime_percentage.png`: the graph, two lines (measured solid, 100 / ln(N) dashed), with title, labelled axes and a legend.
- `prime_percentages.txt`: the two printed lines, first and last sample points, e.g. `N = 5,000: 13.38%` and `N = 5,000,000: 6.97%`. Overwritten on each run.

## Tests (`tests/test_prime_percentage.py`, `unittest`)
The test file adds the repository root to `sys.path` the same way Problem_2's and Problem_3's tests do, then imports `from Problem_4.app.prime_percentage import ...`.

| Requirement | Test |
|---|---|
| Known counts | `records = record_percentages(5_000_000, 5_000)`. The first entry is `(5000, 669, ...)` with percentage 669 / 5000 × 100; the last entry is `(5000000, 348513, ...)` with percentage 348,513 / 5,000,000 × 100. Also check there are 1000 entries. This test runs the full 5,000,000 search, so it takes a while (roughly a minute). |
| Small-case run | `records = record_percentages(100, 10)`. Check there are 10 entries, and that each entry's `prime_count` equals a brute-force count of the primes up to its sample point. The brute-force count is written in the test file only, with simple trial division (the program itself still has no second primality test). |
| Invalid parameters | `record_percentages(100, 4)` and `record_percentages(100, 0)` raise `ValueError` (step below 5). `record_percentages(105, 10)` and `record_percentages(100, 7)` raise `ValueError` (limit not a multiple of step). The message is also checked for the word `step` or `multiple` as appropriate. |

## Running time
About 1.7 million candidates are passed to `is_prime`, and composites with a small factor cost nearly a full loop each (see `Problem_3/interrogation.md`), so the real run is expected to take roughly a minute. The requirements do not ask for the runtime to be printed, so it is not.
