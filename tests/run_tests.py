#!/usr/bin/env python3
"""Zero-dependency fallback runner for tests/test_theorems.py.

Prefer `python -m pytest tests/ -q` when pytest is available.  This runner
exists so the suite can be executed in minimal environments (python3 + numpy
only): it runs every test_* function in definition order, prints PASS/FAIL
per test, and exits nonzero if anything fails.
"""
import os
import sys
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_theorems as T  # noqa: E402


def main():
    tests = [(name, fn) for name, fn in vars(T).items()
             if name.startswith("test_") and callable(fn)]
    failures = 0
    t0 = time.time()
    for name, fn in tests:
        t1 = time.time()
        try:
            fn()
            print(f"PASS  {name}  ({time.time() - t1:.2f}s)")
        except Exception:
            failures += 1
            print(f"FAIL  {name}")
            traceback.print_exc()
    n = len(tests)
    print(f"{n - failures} passed, {failures} failed in {time.time() - t0:.2f}s")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
