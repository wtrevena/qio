# QIO Computational Experiments

Executes the Section 6 program of draft.md. Python 3, numpy/scipy/matplotlib.

- `qio_lib.py` — shared: Haar states, entropies, r_S, 3-tangle, concurrences
- `verify_numbers.py` — recomputes every numerical claim in the draft
- `exp1_matching_manifold.py [N]` — Experiment 1 (default N=1e7, seed 42)
- `exp2_algebraic_families.py` — Experiment 2 (octonion table via Cayley-Dickson)
- `controls.py` — null controls A-D (seed 7)
- `make_figures.py` — Figure 1
- `results/` — JSON summaries, matched-state archive, figure
- Findings: `RESULTS.md`
