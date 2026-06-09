# QIO Computational Experiments

Executes the Section 6 program of draft.md. Python 3, numpy/scipy/matplotlib.

- `qio_lib.py` — shared: Haar states, entropies, r_S, 3-tangle, concurrences
- `verify_numbers.py` — recomputes every numerical claim in the draft
- `exp1_matching_manifold.py [N]` — Experiment 1 (default N=1e7, seed 42)
- `exp2_algebraic_families.py` — Experiment 2 (octonion table via Cayley-Dickson)
- `controls.py` — null controls A-D (seed 7)
- `exp3_entropy_flow.py` — entropy-flow map: feasible (A,B) region, crossings, asymmetry
- `exp4_dynamics_toys.py` — octonion-algebra Hamiltonians (corrected: Hermitian iL_aL_b)
- `exp5_furey_jw.py` — Jordan-Wigner bridge, CAR verification, gauge-frame test
- `exp6_rotor_robustness.py` — rotor vacuum: 128 sign gauges, 5040 relabelings, algebra variants
- `make_figures.py`, `make_fig2.py` — Figures 1 and 2
- `results/` — JSON summaries, matched-state archive, figures
- Findings: `RESULTS.md` (experiments 1-2, controls) and `../PIVOT.md` (experiments 3-6)
