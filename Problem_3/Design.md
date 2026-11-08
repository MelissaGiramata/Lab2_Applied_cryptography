# Problem 3 – Design

Based on `Requirements_v2.md`. The algorithm is unchanged from the requirements.

## Folder layout

Same layout as Problem_2: `app/` for the program, `tests/` next to it (not inside `app/`), `results/` for output.

```
Problem_3/
  Requirements_v1.md
  Requirements_v2.md
  Design.md
  app/
    average_attempts.py          # the program
  tests/
    test_average_attempts.py     # unittest
  results/
    averages.txt                 # written by the program, overwritten on each run
```

- There is no `app/data/` because Problem_3 has no input data.
- There is only one test folder, `Problem_3/tests/`.
- The empty `Problem_3/app/data/` and `Problem_3/app/tests/` folders that exist on disk are not part of this layout and are removed when the code is written.
- `Problem_2/app/data/` and `Problem_2/app/tests/` also exist on disk as empty folders. This design does not touch Problem_2.
- The test file name `test_average_attempts.py` is confirmed.

## Libraries
All standard library, nothing to install.
- `random`: `random.seed` and `random.randint` (both ends included).
- `time`: `time.perf_counter` for the runtime.
- `os` and `sys`: to find the repository root and add it to `sys.path`.
- `unittest`: the tests.
- `is_prime` comes from Problem_2 (see below). It is imported, never re-written.

## Importing `is_prime` from Problem_2

The script is run as `python Problem_3/app/average_attempts.py`. Python then puts the script's own folder (`Problem_3/app`) on the import path, not the repository root, so `Problem_2` could not be found. To fix this, the first lines of the script (before the import):

1. Take the script's own location: `os.path.abspath(__file__)`, which is `.../Problem_3/app/average_attempts.py`.
2. Go up three levels with `os.path.dirname`: file → `app` → `Problem_3` → repository root.
3. Insert that root at the front of `sys.path`.
4. Only then run `from Problem_2.app.prime_test import is_prime`.

This is the same import line Problem_2's tests use. `Problem_2` and `app` are found as namespace packages (no `__init__.py` needed). Because the root is worked out from the file's location, not from the current folder, the import works from any working directory. The requirements still say to run from the repository root, and that is how the program is documented.

## Functions

### `count_until_prime(low, high, drawn=None)`
- Input:
  - `low`, `high`: the interval, both ends included.
  - `drawn`: optional list. If a list is passed, each random number drawn is appended to it, in order. Normal calls do not pass it. (Same idea as `tested` in Problem_2's `is_prime`.)
- Output: `count`, the number of random integers generated up to and including the first prime.
- Steps (algorithm step 1.b.i–iii):
  1. `count = 0`.
  2. Draw `number = random.randint(low, high)` and add 1 to `count`. If `drawn` was passed, append `number`.
  3. If `is_prime(number)` is `True`, return `count`. Otherwise go back to step 2.

### `estimate_average(low, high, trials, counts=None)`
- Input:
  - `low`, `high`: the interval, both ends included.
  - `trials`: how many times to repeat.
  - `counts`: optional list. If a list is passed, the count of each trial is appended to it. Normal calls do not pass it.
- Output: the average count, as a float (`total / trials`).
- Steps (algorithm step 1.a–c):
  1. `total = 0`.
  2. Repeat `trials` times: call `count_until_prime(low, high)`, add the result to `total` (and append it to `counts` if given).
  3. Return `total / trials`.
- It works with any interval and number of trials, so the tests can use small ones.

### `main()`
- Input: none. The two experiments are fixed in the program:
  - Experiment 1: 5,000,000 to 6,000,000, 1000 trials.
  - Experiment 2: 500,000,000,000 to 500,001,000,000, 250 trials.
- Output: prints the results and saves the same text to `Problem_3/results/averages.txt`.
- Steps:
  1. `random.seed(42)`, once, at the start, before Experiment 1. Experiment 2 continues the same random stream.
  2. Start a list of output lines. The first line gives the seed: `Random seed: 42`.
  3. For each experiment: note the time, call `estimate_average`, note the time again, then add a line with the interval, the number of trials, the average with 2 decimals (`f"{average:.2f}"`), and the runtime in seconds.
  4. Print every line.
  5. Create `Problem_3/results/` if it is missing, and write the same lines to `averages.txt` (opened with mode `"w"`, which replaces any old content). The path is built from the repository root found above.
- Called only under `if __name__ == "__main__":`, so importing the module (as the tests do) does not start the experiments and does not set the seed.

## Where `random.seed(42)` is called
Only inside `main()`, once, before Experiment 1. It is not at the top of the file, so importing the module has no effect on the random generator. The tests call `random.seed(...)` themselves when they need a repeatable run.

## How the runtime is measured
Per experiment, with `time.perf_counter()` (a steady clock meant for timing):
1. `start = time.perf_counter()` just before `estimate_average`.
2. `elapsed = time.perf_counter() - start` just after it.
3. `elapsed` is printed in seconds, e.g. with 2 decimals.

Only the estimation is timed. Printing and file writing are not. (Rough expectation, not a requirement: Experiment 1 is fast; Experiment 2 is slower because each prime found takes up to about 240,000 passes of the `is_prime` loop.)

## Output format
Plain text, one block per experiment, for example (numbers are placeholders):

```
Random seed: 42
Experiment 1: interval 5,000,000 to 6,000,000, trials 1000, average count 15.xx, runtime x.xx s
Experiment 2: interval 500,000,000,000 to 500,001,000,000, trials 250, average count 2x.xx, runtime x.xx s
```

This output wording is confirmed. Interval ends are printed with thousands separators. The requirements fix which items are printed and that the average has 2 decimal places.

## Tests (`tests/test_average_attempts.py`, `unittest`)
The test file adds the repository root to `sys.path` the same way Problem_2's tests do, then imports `from Problem_3.app.average_attempts import ...`.

| Requirement | Test |
|---|---|
| Every count ≥ 1 | Call `estimate_average` on a small interval with a `counts` list; check every entry is ≥ 1. |
| Drawn numbers stay in the interval, both ends inclusive | Call `count_until_prime` many times on a small interval with a `drawn` list; check every number is between `low` and `high`, and that both `low` and `high` appear among the draws (small interval, many draws, fixed seed). |
| Same seed gives identical averages | `random.seed(42)`, run `estimate_average`; `random.seed(42)` again, run it again; check the two averages are equal. |
| `is_prime` is the one from Problem_2 | Check `average_attempts.is_prime is prime_test.is_prime` (imported from Problem_2), and that `average_attempts.py` contains no `def is_prime`. |
| Known answer | `estimate_average(7, 7, 10, counts=lst)`: 7 is the only possible number and it is prime, so `lst` is ten 1s and the average is 1.00. |

There is no expected value for the real averages.
