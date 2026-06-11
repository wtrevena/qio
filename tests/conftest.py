"""pytest path setup for the qio test suite.

Makes the repository's computation packages importable regardless of where
pytest is invoked from.  No fixtures are defined: every test in
test_theorems.py is a plain function with plain asserts, so the suite also
runs under the zero-dependency fallback runner (run_tests.py).
"""
import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TESTS_DIR)

for _sub in ("direction_A", os.path.join("newwork", "two_ideal")):
    _p = os.path.join(REPO_ROOT, _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)
