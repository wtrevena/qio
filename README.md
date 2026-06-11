# qio — no-go results and edge-sector coupling reconstruction

Code, data, and manuscripts for a five-paper series that asks, and mostly answers
negatively, whether gauge coupling constants can be read off from vacuum
entanglement data. Papers 1 and 2 are a no-go ladder: the naive "coupling
hierarchy from three-qubit vacuum entanglement" conjecture is shown to be
underconstrained and gauge-frame dependent (Paper 1, `paper/`), and its
gauge-invariant reformulation in the minimal fermionic toy model yields a
sharper no-go — the invariant data is purely classical superselection (edge)
data (Paper 2, `paper2/`). Paper 3 (`paper3/`, with computations in `ym2/`) is
the one positive result, in the one exactly solvable setting: in 2d Yang-Mills
the boundary-flux sector distribution is an exponential family in the coupling,
so its entropy derivative, Fisher information, and coupling-estimation
sensitivity are exactly linked, and the coupling is genuinely reconstructible
from gauge-invariant flux statistics. Papers 4 and 5 are drafted extensions:
"Room for Three Couplings, and Only the Room: The Gauge-Invariant Algebra of
a One-Generation Chiral Fock Space" (Paper 4, `paper4/`, computations in
`newwork/two_ideal/`) — the two-ideal/chiral arena on which the full SM gauge
group acts — and "Fisher Information in Compact U(1) Flux Sectors: Asymptotic
Exponential Families, a Crossover Obstruction, and a Topological Zero-Mode
Bridge to Four Dimensions" (Paper 5, `paper5/`, computations in
`newwork/u1_4d/`). None of this derives
any Standard Model coupling value; the series is a cartography of what
entanglement data can and cannot determine.

## Setup

```
python -m pip install -r requirements.txt
```

Verified environment: Python 3.10.12, numpy 2.2.6, matplotlib 3.10.9 (exact
versions pinned in `requirements.txt`). scipy is needed only by a minority of
scripts (flagged below and in `requirements.txt`); several scripts were
deliberately written to run without it.

All sampling scripts use fixed seeds (`numpy.random.default_rng` with the seed
recorded in each output JSON: 42 and 7 for the Paper 1 experiments, 20260609
for Papers 2–3, 20260610 for the `newwork/` computations), so every stored
JSON in the repository is exactly reproducible. The exact-diagonalization
scripts in `newwork/u1_4d/` are RNG-free.

## Reproducing each paper

Every script writes its results (JSON, figures) next to itself or into a
`results/` subfolder and asserts its own claims at runtime. The commands below
regenerate the stored outputs in place.

### Paper 1 (`paper/main.tex`) — experiments and figures

```
cd experiments && python verify_numbers.py && python verify_wfamily.py && python exp1_matching_manifold.py && python exp2_algebraic_families.py && python controls.py && python exp3_entropy_flow.py && python exp4_dynamics_toys.py && python exp5_furey_jw.py && python exp6_rotor_robustness.py && python make_figures.py && python make_fig2.py
```

`verify_numbers.py` recomputes every numerical claim in the manuscript;
`verify_wfamily.py` is the standalone, sampling-free check of the weighted-W
matching-family lemma (r_S = 1.8174 exactly along the analytic curve, ~4 s,
numpy-only). `exp1_matching_manifold.py` is the long job (default N = 10^7
Haar samples; pass a smaller N as the first argument for a quick run).
Requires scipy for `verify_numbers.py`, `exp1_matching_manifold.py`, and
`exp2_algebraic_families.py`; matplotlib for the two figure scripts. Outputs
land in `experiments/results/`; findings are summarized in
`experiments/RESULTS.md` and `PIVOT.md`.

### Paper 2 (`paper2/main.tex`) — commutants and algebraic entropy tables

```
cd direction_A && python run_direction_A.py && python strengthen.py
```

`run_direction_A.py` (seed 20260609, writes `results.json`) verifies the CAR
machinery, computes the gauge-invariant commutants (U(3) → C^4, SU(3) →
M2⊕C⊕C, U(1) → dimension 20) and the BKOV entropy tables.
`strengthen.py` (~10 s, writes `strengthen_results.json`) machine-checks the
SU(2)_L obstruction lemma and the follow-ups written up in
`paper2/VERIFICATIONS.md`. Both need scipy (`run_direction_A.py` runs its
first sections — CAR, commutants, entropy tables, gauge invariance — on numpy
alone and imports `scipy.special.digamma` only for its later section).

### Paper 3 (`paper3/main.tex`) — 2d Yang-Mills coupling reconstruction

```
cd ym2 && python ym2_flux.py && python ym2_su3.py && cd ../paper3 && python weak_coupling_check.py && python mle_bias_ci.py
```

`ym2_flux.py` (~8 s; U(1) and SU(2), entropy/Fisher/capacity identities, MLE
demo, Figure 1) and `ym2_su3.py` (~3 s; SU(3) extension, n-interval analysis,
Figure 2) need scipy and matplotlib; formulas and primary-source citations are
in `ym2/FORMULAS.md`. `weak_coupling_check.py` (<1 s, numpy-only) verifies the
weak-coupling asymptotics of the appendix. `mle_bias_ci.py` (numpy-only, runs
with or without scipy via a built-in Brent fallback) is the long job of the
series — 27 (group, t*, N) cells with 2000 Monte-Carlo batches each; expect
minutes, not seconds. Seed 20260609 throughout.

### Paper 4 (`paper4/main.tex`, drafted) — the two-ideal / chiral arena

```
cd newwork/two_ideal && python run_rep.py && python run_full.py && python run_crosscheck.py
```

About 20 s total, numpy-only, seed 20260610. `run_rep.py` (<1 s) builds the
exact decomposition of the 2^15-dimensional one-generation Fock space under
SU(3)×SU(2)×U(1) (250 sectors, commutant dimension 57062, 28 invariant
vectors, Z6 congruence). `run_full.py` (~12 s) verifies every multiplicity by
explicit Schur analysis and runs the three-parameter test. `run_crosscheck.py`
(~3 s) reruns the `direction_A` commutant pipeline as an independent
cross-check and computes the first nonzero quantum (bulk) pieces. Findings:
`newwork/two_ideal/REPORT.md`.

### Paper 5 (`paper5/main.tex`, drafted) — compact U(1) flux sectors in higher d

```
cd newwork/u1_4d && python u1_2d_baseline.py && python u1_chain_ed.py grid && python u1_chain_ed.py fisher && python u1_chain_ed.py conv1 && python u1_chain_ed.py conv2 && python analyze_chain.py && python u1_dipole_gas.py
```

All numpy-only and RNG-free; each `u1_chain_ed.py` stage takes well under a
minute. `u1_2d_baseline.py` is the exact 2d anchor; `u1_chain_ed.py` is the
exact diagonalization of compact U(1) on a 2+1d plaquette strip (87 stored
ground states in `results_chain.json`); `analyze_chain.py` runs the
exponential-family rank and Fisher-information tests; `u1_dipole_gas.py` is
the analytic model of the two 3+1d limits. `ed2p1.py`, `gauss4d.py`, and the
`mc_row_*.json` / `results_2d.json` / `results_gauss*.json` files predate the
final report and are retained for provenance only. Findings:
`newwork/u1_4d/REPORT.md`, `DERIVATION.md`, `LITERATURE.md`.

## Tests

A theorem-level regression suite (numpy-only, ~2 s) covers the claims the
manuscripts state as theorems or conventions: CAR relations, the commutant
dimensions 4/6/20, the vanishing quantum piece of the algebraic entropy in the
one-ideal toy, the weighted-W identity r_S = 1.8174, the 2d Yang-Mills
identities dS/dt = −(t/4)Var(C₂) and I = ¼Var(C₂), the SU(3) Casimir
convention C₂(fund) = 4/3, and the stored two-ideal headline numbers.

```
python -m pytest tests/ -q        # preferred
python tests/run_tests.py         # zero-dependency fallback (python3 + numpy)
```

## Folder map

| Path | Contents | Status |
|---|---|---|
| `paper/` | Paper 1 manuscript (`main.tex`, figures, `arxiv_submission/`) | active |
| `paper2/` | Paper 2 manuscript + `VERIFICATIONS.md`, critic round notes | active |
| `paper3/` | Paper 3 manuscript + `mle_bias_ci.py`, `weak_coupling_check.py` | active |
| `paper4/` | Paper 4 manuscript (two-ideal arena; `arxiv_submission/`) | drafted |
| `paper5/` | Paper 5 manuscript (compact U(1), higher d; `arxiv_submission/`) | drafted |
| `experiments/` | Paper 1 computations (`qio_lib.py`, exp1–exp6, controls, verifiers, `results/`) | active |
| `direction_A/` | Paper 2 computations (`alg_entanglement.py`, `run_direction_A.py`, `strengthen.py`) | active; its `REPORT.md` is superseded by `paper2/` |
| `direction_B/` | Edge-mode / contact-term literature verification (`LITERATURE_REVIEW.md`, `SOURCES.md`) | reference material |
| `ym2/` | Paper 3 base computations (`ym2_flux.py`, `ym2_su3.py`, `FORMULAS.md`) | active |
| `newwork/two_ideal/` | Paper 4 computations and `REPORT.md` | active |
| `newwork/u1_4d/` | Paper 5 computations, `REPORT.md`, `DERIVATION.md`, `LITERATURE.md` | active |
| `tests/` | Theorem-level pytest suite | active |
| `draft.md` | Original Paper 1 markdown draft | superseded by `paper/main.tex` (mapping in `paper/RESTRUCTURE_MAP.md`) |
| `PIVOT.md`, `SYNTHESIS.md` | Working notes for the reformulation and the A/B synthesis | historical record |
| `REVIEW.md`, `CRITIC_RESPONSE.md`, `new_review.txt`, `20260610.10.48_PM_PST_revision_feedback.txt` | Independent verification log: referee-style review rounds and point-by-point responses (see also `paper2/CRITIC_ROUND2.md`, `paper3/CRITIC_ROUND1.md`) | record |
| `PROJECT_NOTES.md` | Running project log | internal |

## Release process

Each manuscript receives a frozen git tag at submission time
(`paper1-v1-submission`, `paper2-v1-submission`, …, `paper5-v1-submission`)
and an archival snapshot with a Zenodo DOI minted from that tag. Paper-level
citation entries will be added to `CITATION.cff` as tags are created; until
then, cite the repository as a whole (see `CITATION.cff`). Code is MIT
licensed (`LICENSE`).
